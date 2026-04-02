"""
Agent Service Tests — Unit tests for the LangGraph agent system.
"""

import pytest


class TestExpenseState:
    """Test the ExpenseState schema."""

    def test_state_creation(self):
        """Test that ExpenseState can be created with required fields."""
        from agents.state import ExpenseState

        state: ExpenseState = {
            "expense_id": "EXP-2026-001",
            "extracted_data": {"merchant": "Test", "amount": 50.0},
            "employee_id": "E-1042",
            "submitted_justification": "Business lunch",
            "policy_subgraph": {},
            "applicable_rules": [],
            "audit_verdict": None,
            "fraud_score": None,
            "fraud_flags": [],
            "compliance_decision": None,
            "compliance_reasoning": None,
            "remediation_messages": [],
            "negotiation_round": 0,
            "max_negotiation_rounds": 3,
            "final_decision": None,
            "audit_trail": [],
        }
        assert state["expense_id"] == "EXP-2026-001"
        assert state["max_negotiation_rounds"] == 3


class TestRoutingFunctions:
    """Test the graph routing logic."""

    def test_route_compliance_approved(self):
        """Test routing for APPROVED decision."""
        from agents.graph import route_compliance_decision

        state = {"compliance_decision": "APPROVED"}
        assert route_compliance_decision(state) == "approved"

    def test_route_compliance_rejected(self):
        """Test routing for REJECTED decision."""
        from agents.graph import route_compliance_decision

        state = {"compliance_decision": "REJECTED"}
        assert route_compliance_decision(state) == "rejected"

    def test_route_compliance_remediation(self):
        """Test routing for NEEDS_REMEDIATION decision."""
        from agents.graph import route_compliance_decision

        state = {"compliance_decision": "NEEDS_REMEDIATION"}
        assert route_compliance_decision(state) == "needs_remediation"

    def test_route_remediation_escalate(self):
        """Test remediation escalation when max rounds exceeded."""
        from agents.graph import route_remediation_outcome

        state = {"negotiation_round": 3, "max_negotiation_rounds": 3}
        assert route_remediation_outcome(state) == "escalate"

    def test_route_remediation_re_evaluate(self):
        """Test remediation re-evaluation when rounds remain."""
        from agents.graph import route_remediation_outcome

        state = {"negotiation_round": 1, "max_negotiation_rounds": 3}
        assert route_remediation_outcome(state) == "re_evaluate"


class TestAgentServer:
    """Test the agent server endpoints."""

    def test_health_check(self):
        from fastapi.testclient import TestClient
        from agents.server import app

        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
