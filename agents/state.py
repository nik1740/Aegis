"""
ExpenseState — Shared state schema for the LangGraph agent graph.

This TypedDict defines the complete state that flows through all agent
nodes in the orchestration pipeline. Each agent reads from and writes
to specific fields.
"""

from operator import add
from typing import Annotated, Literal, TypedDict


class ExpenseState(TypedDict):
    """Shared state across all agents in the LangGraph expense processing graph."""

    # ============================================================
    # Input (set by gateway → agent server)
    # ============================================================
    expense_id: str
    extracted_data: dict          # From Layer 1 (VLM extraction)
    employee_id: str
    submitted_justification: str

    # ============================================================
    # Layer 2 outputs (set by extract_policy node)
    # ============================================================
    policy_subgraph: dict         # Nodes/edges from Neo4j traversal
    applicable_rules: list[dict]

    # ============================================================
    # Agent outputs
    # ============================================================
    # Contextual Auditor
    audit_verdict: dict | None    # {verdict: PASS|FAIL|AMBIGUOUS, reasoning, confidence}

    # Fraud Detective
    fraud_score: float | None     # 0.0 (safe) to 1.0 (fraudulent)
    fraud_flags: list[str]        # e.g., ["duplicate_receipt", "weekend_submission"]

    # Compliance Judge
    compliance_decision: str | None   # APPROVED | REJECTED | NEEDS_REMEDIATION
    compliance_reasoning: str | None

    # ============================================================
    # Negotiation (Layer 4)
    # ============================================================
    remediation_messages: Annotated[list[dict], add]  # Conversation log
    negotiation_round: int
    max_negotiation_rounds: int   # Default: 3

    # ============================================================
    # Final Output
    # ============================================================
    final_decision: str | None    # APPROVED | REJECTED | ESCALATED
    audit_trail: Annotated[list[dict], add]  # Immutable event log (append-only)
