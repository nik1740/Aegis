"""
Agent Graph — LangGraph state machine definition.

Defines the multi-agent orchestration graph:
  extract_policy → [contextual_auditor, fraud_detective] → compliance_judge
  → (conditional) → record_decision | remediation_agent → (cycle back)

This is the core of the Aegis agent system. The graph supports:
- Parallel fan-out (auditor + fraud detective run concurrently)
- Conditional routing based on compliance decision
- Cyclic re-entrant loops for remediation/negotiation
- Persistent checkpointing via PostgreSQL
"""

import structlog
from langgraph.graph import END, StateGraph

from state import ExpenseState

logger = structlog.get_logger()


# ============================================================
# Node Functions (imported from nodes/ package)
# ============================================================

def extract_policy_subgraph(state: ExpenseState) -> dict:
    """
    Layer 2 Node: Query Neo4j for the policy subgraph applicable to this expense.

    Performs deterministic Cypher traversal:
    Employee → Role → PolicyRule ← ExpenseCategory
    """
    logger.info("extract_policy_started", expense_id=state["expense_id"])

    # TODO: Call GraphQueryEngine.get_policy_subgraph()
    # TODO: Cache result in Redis

    return {
        "policy_subgraph": {},
        "applicable_rules": [],
        "audit_trail": [{
            "event": "POLICY_TRAVERSAL",
            "agent": "graph_engine",
            "expense_id": state["expense_id"],
        }],
    }


def run_contextual_auditor(state: ExpenseState) -> dict:
    """
    Layer 3 Node: Contextual Auditor agent.

    Compares extracted expense data against the policy subgraph
    using an LLM (GPT-4o-mini) with the exact policy rules provided.
    """
    logger.info("contextual_auditor_started", expense_id=state["expense_id"])

    # TODO: Import and run the contextual auditor node
    # from nodes.contextual_auditor import run

    return {
        "audit_verdict": {
            "verdict": "PASS",
            "reasoning": "Placeholder — auditor not yet implemented",
            "confidence": 0.0,
        },
        "audit_trail": [{
            "event": "AUDITOR_VERDICT",
            "agent": "contextual_auditor",
            "expense_id": state["expense_id"],
        }],
    }


def run_fraud_detective(state: ExpenseState) -> dict:
    """
    Layer 3 Node: Fraud Detective agent.

    Runs Isolation Forest anomaly detection and CLIP image embedding
    duplicate detection on the expense.
    """
    logger.info("fraud_detective_started", expense_id=state["expense_id"])

    # TODO: Import and run the fraud detective node
    # from nodes.fraud_detective import run

    return {
        "fraud_score": 0.0,
        "fraud_flags": [],
        "audit_trail": [{
            "event": "FRAUD_SCORE",
            "agent": "fraud_detective",
            "expense_id": state["expense_id"],
        }],
    }


def run_compliance_judge(state: ExpenseState) -> dict:
    """
    Layer 3 Node: Compliance Judge agent.

    Adversarial review using a DIFFERENT LLM provider than the auditor.
    Combines auditor verdict + fraud score to make final decision.
    """
    logger.info("compliance_judge_started", expense_id=state["expense_id"])

    # TODO: Import and run the compliance judge node
    # from nodes.compliance_judge import run

    return {
        "compliance_decision": "APPROVED",
        "compliance_reasoning": "Placeholder — judge not yet implemented",
        "audit_trail": [{
            "event": "COMPLIANCE_DECISION",
            "agent": "compliance_judge",
            "expense_id": state["expense_id"],
        }],
    }


def run_remediation(state: ExpenseState) -> dict:
    """
    Layer 4 Node: Remediation Agent.

    Handles autonomous negotiation with the employee for minor discrepancies.
    Can cycle back to extract_policy for re-evaluation.
    """
    logger.info("remediation_started", expense_id=state["expense_id"], round=state.get("negotiation_round", 0))

    # TODO: Import and run the remediation node
    # from nodes.remediation import run

    return {
        "negotiation_round": state.get("negotiation_round", 0) + 1,
        "remediation_messages": [{
            "agent": "Placeholder remediation message",
            "round": state.get("negotiation_round", 0) + 1,
        }],
        "audit_trail": [{
            "event": "REMEDIATION_SENT",
            "agent": "remediation",
            "expense_id": state["expense_id"],
        }],
    }


def record_to_audit_log(state: ExpenseState) -> dict:
    """
    Final Node: Record the decision to the PostgreSQL audit log.

    Creates immutable audit event with full trace payload.
    """
    logger.info(
        "decision_recorded",
        expense_id=state["expense_id"],
        decision=state.get("compliance_decision"),
    )

    # TODO: Write to PostgreSQL audit_events table

    return {
        "final_decision": state.get("compliance_decision", "ESCALATED"),
        "audit_trail": [{
            "event": "FINAL_DECISION",
            "agent": "system",
            "expense_id": state["expense_id"],
            "decision": state.get("compliance_decision"),
        }],
    }


# ============================================================
# Routing Functions
# ============================================================

def route_compliance_decision(state: ExpenseState) -> str:
    """Route based on the Compliance Judge's decision."""
    decision = state.get("compliance_decision", "").upper()
    if decision == "APPROVED":
        return "approved"
    elif decision == "REJECTED":
        return "rejected"
    elif decision == "NEEDS_REMEDIATION":
        return "needs_remediation"
    else:
        return "approved"  # Default fallback


def route_remediation_outcome(state: ExpenseState) -> str:
    """Route based on remediation outcome (re-evaluate, escalate, or resolved)."""
    current_round = state.get("negotiation_round", 0)
    max_rounds = state.get("max_negotiation_rounds", 3)

    if current_round >= max_rounds:
        return "escalate"

    # TODO: Check actual remediation outcome
    return "re_evaluate"


# ============================================================
# Graph Construction
# ============================================================

def build_expense_graph() -> StateGraph:
    """
    Build and compile the LangGraph expense processing state machine.

    Graph topology:
      extract_policy → [contextual_auditor, fraud_detective] (parallel)
      → compliance_judge
      → APPROVED/REJECTED → record_decision → END
      → NEEDS_REMEDIATION → remediation_agent → (cycle) extract_policy
    """
    builder = StateGraph(ExpenseState)

    # Add nodes
    builder.add_node("extract_policy", extract_policy_subgraph)
    builder.add_node("contextual_auditor", run_contextual_auditor)
    builder.add_node("fraud_detective", run_fraud_detective)
    builder.add_node("compliance_judge", run_compliance_judge)
    builder.add_node("remediation_agent", run_remediation)
    builder.add_node("record_decision", record_to_audit_log)

    # Define edges
    builder.set_entry_point("extract_policy")

    # Parallel fan-out: policy → auditor + fraud detective
    builder.add_edge("extract_policy", "contextual_auditor")
    builder.add_edge("extract_policy", "fraud_detective")

    # Both converge into compliance judge
    builder.add_edge("contextual_auditor", "compliance_judge")
    builder.add_edge("fraud_detective", "compliance_judge")

    # Conditional routing from Compliance Judge
    builder.add_conditional_edges(
        "compliance_judge",
        route_compliance_decision,
        {
            "approved": "record_decision",
            "rejected": "record_decision",
            "needs_remediation": "remediation_agent",
        },
    )

    # Remediation can cycle back (THIS IS WHY LANGGRAPH IS REQUIRED)
    builder.add_conditional_edges(
        "remediation_agent",
        route_remediation_outcome,
        {
            "re_evaluate": "extract_policy",   # ← CYCLE
            "escalate": "record_decision",
            "resolved": "record_decision",
        },
    )

    # Terminal edge
    builder.add_edge("record_decision", END)

    return builder


# Build the graph (can be compiled with a checkpointer later)
expense_graph_builder = build_expense_graph()
