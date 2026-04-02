"""
Knowledge Graph Tests — Unit tests for policy parsing and graph operations.
"""

import json
from pathlib import Path

import pytest

from knowledge_graph.policy_parser import PolicyParser, PolicyRule, ParsedPolicy


class TestPolicyParser:
    """Test policy document parsing."""

    def test_parse_sample_policy_json(self):
        """Test parsing the sample policy JSON file."""
        parser = PolicyParser()
        policy_path = Path(__file__).parent.parent / "seed_data" / "sample_policy.json"
        policy = parser.parse_json(str(policy_path))

        assert policy.company_name == "Cymonic Technologies"
        assert len(policy.rules) > 0
        assert len(policy.roles) > 0
        assert len(policy.departments) > 0
        assert len(policy.locations) > 0

    def test_policy_rule_model(self):
        """Test PolicyRule Pydantic model validation."""
        rule = PolicyRule(
            rule_id="TEST-001",
            description="Test rule",
            category="meals",
            limit_amount=50.0,
            limit_currency="GBP",
            limit_period="daily",
            effective_date="2026-01-01",
        )
        assert rule.rule_id == "TEST-001"
        assert rule.limit_amount == 50.0
        assert rule.requires_receipt is True
