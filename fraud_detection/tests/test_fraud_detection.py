"""
Fraud Detection Tests — Unit tests for anomaly detection and image embeddings.
"""

import numpy as np
import pytest

from fraud_detection.models.isolation_forest import FraudModel, FRAUD_FEATURES


class TestIsolationForest:
    """Test the Isolation Forest fraud model."""

    def test_feature_count(self):
        """Verify expected number of features."""
        assert len(FRAUD_FEATURES) == 7

    def test_feature_extraction(self):
        """Test feature extraction from expense data."""
        model = FraudModel()
        expense = {
            "total_amount": 50.0,
            "submission_hour": 14,
            "days_since_last": 2,
            "category": "meals",
            "is_weekend": False,
            "is_international": False,
        }
        features = model.extract_features(expense, historical_avg=45.0)
        assert features.shape == (1, 7)
        assert features[0, 0] == pytest.approx(50.0 / 45.0, rel=0.01)

    def test_untrained_model_returns_default(self):
        """Untrained model should return 0.0 fraud score."""
        model = FraudModel()
        model.model = None  # Force untrained state
        features = np.zeros((1, 7))
        score = model.predict(features)
        assert score == 0.0

    def test_train_and_predict(self):
        """Test training and prediction cycle."""
        model = FraudModel()
        training_data = np.random.randn(100, 7)
        model.train(training_data)

        normal_sample = np.zeros((1, 7))
        score = model.predict(normal_sample)
        assert 0.0 <= score <= 1.0
