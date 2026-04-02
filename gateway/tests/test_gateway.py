"""
Gateway Service Tests — Unit tests for the ingestion pipeline.
"""

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_health_check(self):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "aegis-gateway"

    def test_dependency_health(self):
        response = client.get("/api/v1/health/dependencies")
        assert response.status_code == 200
        data = response.json()
        assert "dependencies" in data


class TestExpenseEndpoints:
    """Test expense submission and retrieval endpoints."""

    def test_get_nonexistent_expense(self):
        response = client.get("/api/v1/expenses/EXP-FAKE-001")
        assert response.status_code == 404

    def test_list_expenses_empty(self):
        response = client.get("/api/v1/expenses/")
        assert response.status_code == 200
        data = response.json()
        assert data["data"] == []
        assert data["has_more"] is False


class TestSchemas:
    """Test Pydantic schema validation."""

    def test_extracted_expense_valid(self):
        from extractors.schemas import ExtractedExpense

        expense = ExtractedExpense(
            merchant_name_raw="Uber Trip",
            transaction_date="2026-04-01",
            currency="GBP",
            subtotal=12.50,
            total_amount=12.50,
            category_inferred="transport",
            confidence_score=0.95,
        )
        assert expense.currency == "GBP"
        assert expense.confidence_score == 0.95

    def test_extracted_expense_invalid_currency(self):
        from extractors.schemas import ExtractedExpense

        with pytest.raises(Exception):
            ExtractedExpense(
                merchant_name_raw="Test",
                transaction_date="2026-04-01",
                currency="INVALID",  # Must be 3 uppercase letters
                subtotal=10.0,
                total_amount=10.0,
                category_inferred="other",
                confidence_score=0.5,
            )
