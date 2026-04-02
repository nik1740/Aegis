"""
Train Anomaly Model — Isolation Forest training pipeline.

Generates or loads historical expense data and trains the
Isolation Forest model for anomaly detection.

Usage:
    poetry run python -m fraud_detection.training.train_anomaly
"""

import numpy as np
import structlog

from fraud_detection.models.isolation_forest import FraudModel, FRAUD_FEATURES

logger = structlog.get_logger()


def generate_synthetic_training_data(n_samples: int = 5000) -> np.ndarray:
    """
    Generate synthetic expense data for model training.

    Simulates normal expense patterns with a small fraction of anomalies.

    Args:
        n_samples: Number of synthetic expense records.

    Returns:
        NumPy array of shape (n_samples, n_features).
    """
    np.random.seed(42)

    data = np.column_stack([
        np.random.lognormal(mean=0.0, sigma=0.5, size=n_samples),  # amount_normalized
        np.random.choice(range(8, 20), size=n_samples),             # submission_hour (business hours)
        np.random.exponential(scale=3, size=n_samples),             # days_since_last_submission
        np.random.choice(range(7), size=n_samples),                 # merchant_category_encoded
        np.random.choice([0, 1], size=n_samples, p=[0.7, 0.3]),    # amount_round_number_flag
        np.random.choice([0, 1], size=n_samples, p=[0.85, 0.15]),  # weekend_submission_flag
        np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2]),    # international_flag
    ])

    logger.info("synthetic_data_generated", n_samples=n_samples, n_features=len(FRAUD_FEATURES))
    return data


def train_model() -> None:
    """Train the Isolation Forest model on synthetic or real data."""
    logger.info("training_started")

    # TODO: Load real historical data from PostgreSQL
    # For now, use synthetic data
    training_data = generate_synthetic_training_data(n_samples=5000)

    model = FraudModel()
    model.train(training_data)

    # Test prediction
    test_sample = training_data[0]
    score = model.predict(test_sample)
    logger.info("training_complete", test_fraud_score=score)


if __name__ == "__main__":
    train_model()
