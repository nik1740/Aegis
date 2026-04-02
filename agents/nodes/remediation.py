"""
Remediation Agent — Autonomous employee negotiation for minor discrepancies.

Responsibilities:
- Sends contextual messages to employees about discrepancies
- Validates employee responses (CRM lookup for client meeting claims)
- Updates context graph with new information
- Triggers re-evaluation or escalation

Guardrails:
- Max negotiation rounds: 3 (configurable)
- Employee response timeout: 48 hours
- Scope restriction: can only ask about the specific discrepancy
- CRM validation required for client exemptions
"""

import structlog

logger = structlog.get_logger()


async def run(state: dict) -> dict:
    """
    Remediation Agent node logic.

    Handles the autonomous negotiation loop for expenses that are
    NEEDS_REMEDIATION (minor discrepancies with possible exemptions).

    Args:
        state: Current ExpenseState with compliance reasoning and discrepancy details.

    Returns:
        Updated state with remediation messages and negotiation round counter.
    """
    expense_id = state.get("expense_id", "unknown")
    current_round = state.get("negotiation_round", 0) + 1
    max_rounds = state.get("max_negotiation_rounds", 3)
    compliance_reasoning = state.get("compliance_reasoning", "")

    logger.info(
        "remediation_agent_running",
        expense_id=expense_id,
        round=current_round,
        max_rounds=max_rounds,
    )

    if current_round > max_rounds:
        logger.warning("remediation_max_rounds_exceeded", expense_id=expense_id)
        return {
            "negotiation_round": current_round,
            "compliance_decision": "ESCALATED",
            "audit_trail": [{
                "event": "REMEDIATION_ESCALATED",
                "agent": "remediation",
                "expense_id": expense_id,
                "reason": "max_negotiation_rounds_exceeded",
            }],
        }

    # TODO: Generate contextual message for the employee based on the discrepancy
    # TODO: Send message via Slack/email/Streamlit chat
    # TODO: Wait for employee response (async — stored in remediation_sessions table)
    # TODO: If employee provides client name → validate via CRM API
    # TODO: Update policy subgraph context with exemption if valid
    # TODO: Return re-evaluate or resolved status

    message = {
        "round": current_round,
        "from": "remediation_agent",
        "to": "employee",
        "content": f"Placeholder: Requesting additional information for expense {expense_id}",
        "discrepancy": compliance_reasoning,
    }

    return {
        "negotiation_round": current_round,
        "remediation_messages": [message],
        "audit_trail": [{
            "event": "REMEDIATION_SENT",
            "agent": "remediation",
            "expense_id": expense_id,
            "round": current_round,
        }],
    }
