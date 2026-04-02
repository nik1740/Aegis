"""
Isolation Forest — Unsupervised anomaly detection for expense fraud.

Features used:
- amount_normalized: amount / employee's 30-day average
- submission_hour: 0–23
- days_since_last_submission
- merchant_category_encoded
- amount_round_number_flag: 1 if amount ends in .00
- weekend_submission_flag
- international_flag

Model is retrained weekly on 90 days of approved expenses per employee.
No labeled fraud data is required (unsupervised).
"""

import os
from pathlib import Path
from typing import Optional

import numpy as np
import structlog
from sklearn.ensemble import IsolationForest

logger = structlog.get_logger()

MODEL_DIR = Path(__file__).parent / "saved"

# Feature names for the Isolation Forest model
FRAUD_FEATURES = [
    "amount_normalized",
    "submission_hour",
    "days_since_last_submission",
    "merchant_category_encoded",
    "amount_round_number_flag",
    "weekend_submission_flag",
    "international_flag",
]


class FraudModel:
    """Isolation Forest-based fraud detection model."""

    def __init__(self):
        self.model: Optional[IsolationForest] = None
        self._load_model()

    def _load_model(self) -> None:
        """Load a pre-trained model from disk, or initialize a new one."""
        model_path = MODEL_DIR / "isolation_forest.joblib"
        if model_path.exists():
            import joblib
            self.model = joblib.load(model_path)
            logger.info("fraud_model_loaded", path=str(model_path))
        else:
            logger.warning("fraud_model_not_found", message="Will train on first data batch")

    def train(self, features: np.ndarray) -> None:
        """
        Train the Isolation Forest on historical expense data.

        Args:
            features: NumPy array of shape (n_samples, n_features)
                     with columns matching FRAUD_FEATURES.
        """
        self.model = IsolationForest(
            n_estimators=200,
            contamination=0.02,  # Expect ~2% anomalies
            random_state=42,
            n_jobs=-1,
        )
        self.model.fit(features)

        # Save model
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        import joblib
        joblib.dump(self.model, MODEL_DIR / "isolation_forest.joblib")
        logger.info("fraud_model_trained", n_samples=features.shape[0])

    def predict(self, features: np.ndarray) -> float:
        """
        Score an expense for fraud likelihood.

        Args:
            features: NumPy array of shape (1, n_features).

        Returns:
            Fraud score between 0.0 (safe) and 1.0 (likely fraud).
            Higher values indicate more anomalous expenses.
        """
        if self.model is None:
            logger.warning("fraud_model_not_trained", returning="default_score")
            return 0.0

        # decision_function returns negative scores for outliers
        raw_score = self.model.decision_function(features.reshape(1, -1))[0]

        # Normalize to 0.0–1.0 range (more negative = more anomalous = higher fraud score)
        # Typical range is roughly [-0.5, 0.5]
        fraud_score = max(0.0, min(1.0, 0.5 - raw_score))

        return round(fraud_score, 4)

    def extract_features(self, expense_data: dict, historical_avg: float = 50.0) -> np.ndarray:
        """
        Extract features from expense data for model prediction.

        Args:
            expense_data: Dictionary with expense fields.
            historical_avg: Employee's 30-day average expense amount.

        Returns:
            NumPy array of shape (1, n_features) matching FRAUD_FEATURES.
        """
        amount = expense_data.get("total_amount", 0.0)

        features = np.array([
            amount / max(historical_avg, 1.0),  # amount_normalized
            expense_data.get("submission_hour", 12),  # submission_hour
            expense_data.get("days_since_last", 1),  # days_since_last_submission
            hash(expense_data.get("category", "other")) % 10,  # merchant_category_encoded
            1.0 if amount == int(amount) else 0.0,  # amount_round_number_flag
            1.0 if expense_data.get("is_weekend", False) else 0.0,  # weekend_submission_flag
            1.0 if expense_data.get("is_international", False) else 0.0,  # international_flag
        ]).reshape(1, -1)

        return features
