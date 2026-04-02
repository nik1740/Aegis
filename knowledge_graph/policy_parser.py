"""
Policy Parser — Converts corporate policy documents into structured rules.

Uses LLM-assisted parsing (one-time) to extract structured policy rules
from PDF documents, then outputs JSON for graph_builder to load into Neo4j.
"""

import json
from pathlib import Path
from typing import Optional

import structlog
from pydantic import BaseModel, Field

logger = structlog.get_logger()


class PolicyRule(BaseModel):
    """Structured representation of a single corporate policy rule."""
    rule_id: str
    description: str
    category: str
    limit_amount: float
    limit_currency: str = "GBP"
    limit_period: str = "daily"  # daily | per_item | per_trip
    applicable_roles: list[str] = []
    applicable_locations: list[str] = []
    requires_receipt: bool = True
    requires_preapproval: bool = False
    effective_date: str
    expiry_date: Optional[str] = None
    exemptions: list[dict] = []


class ParsedPolicy(BaseModel):
    """Complete parsed policy document."""
    company_name: str
    policy_version: str
    rules: list[PolicyRule]
    roles: list[dict]
    departments: list[dict]
    locations: list[dict]


class PolicyParser:
    """Parses corporate policy documents into structured rules."""

    async def parse_pdf(self, pdf_path: str) -> ParsedPolicy:
        """
        Parse a PDF policy document into structured rules.

        Uses LLM-assisted extraction with schema enforcement.

        Args:
            pdf_path: Path to the corporate policy PDF.

        Returns:
            ParsedPolicy with all extracted rules, roles, departments.
        """
        # TODO: Implement PDF parsing with VLM/LLM extraction
        # 1. Extract text from PDF (PyPDF2 or similar)
        # 2. Send to LLM with PolicyRule JSON schema
        # 3. Validate extracted rules against Pydantic models
        raise NotImplementedError("PDF policy parsing not yet implemented")

    def parse_json(self, json_path: str) -> ParsedPolicy:
        """
        Parse a pre-structured JSON policy file.

        Args:
            json_path: Path to a structured policy JSON file.

        Returns:
            ParsedPolicy with all rules and organizational data.
        """
        with open(json_path) as f:
            data = json.load(f)

        logger.info("policy_parsed", source=json_path, rule_count=len(data.get("rules", [])))
        return ParsedPolicy(**data)
