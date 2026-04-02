"""
Compliance Judge Agent — Adversarial review with independent LLM provider.

Responsibilities:
- Reviews combined evidence from Auditor + Fraud Detective
- Uses a DIFFERENT LLM provider than the Contextual Auditor
- Makes final compliance decision: APPROVED | REJECTED | NEEDS_REMEDIATION
- Provides detailed reasoning for auditability

CRITICAL DESIGN RULE:
The Compliance Judge MUST use a different LLM provider than the Contextual Auditor
to guarantee true adversarial independence. If both use GPT-4o, they may share
systematic biases. Default: GPT-4o for Auditor, Claude for Judge.
"""

import structlog

logger = structlog.get_logger()

JUDGE_SYSTEM_PROMPT = """You are an independent compliance judge reviewing expense audit decisions.

You receive:
1. The Contextual Auditor's verdict (PASS/FAIL/AMBIGUOUS with reasoning)
2. The Fraud Detective's score (0.0 to 1.0) and any fraud flags
3. The original PolicySubgraph with exact rules
4. The employee's justification

Your task: Make a FINAL compliance decision.

Output a JSON object with:
- decision: "APPROVED" | "REJECTED" | "NEEDS_REMEDIATION"
- reasoning: detailed explanation citing specific evidence
- confidence: float 0.0 to 1.0
- recommended_action: string (e.g., "auto_approve", "flag_for_review", "request_client_name")

Rules:
- If the Auditor says PASS and fraud_score < 0.3 → lean toward APPROVED
- If the Auditor says FAIL or fraud_score > 0.6 → lean toward REJECTED
- If the discrepancy is minor AND an exemption exists → use NEEDS_REMEDIATION
- You are the FINAL reviewer — your decision is authoritative
- You MUST NOT rubber-stamp the Auditor's verdict — perform independent analysis"""


async def run(state: dict) -> dict:
    """
    Compliance Judge node logic.

    Uses a different LLM provider than the Contextual Auditor for adversarial independence.

    Args:
        state: Current ExpenseState with audit_verdict and fraud_score.

    Returns:
        Updated state with compliance_decision and compliance_reasoning.
    """
    expense_id = state.get("expense_id", "unknown")
    audit_verdict = state.get("audit_verdict", {})
    fraud_score = state.get("fraud_score", 0.0)
    fraud_flags = state.get("fraud_flags", [])

    logger.info(
        "compliance_judge_reviewing",
        expense_id=expense_id,
        auditor_verdict=audit_verdict.get("verdict"),
        fraud_score=fraud_score,
    )

    # TODO: Build prompt combining auditor verdict + fraud score + policy subgraph
    # TODO: Call DIFFERENT LLM provider (Claude if Auditor uses GPT-4o)
    # TODO: Parse and validate the ComplianceDecision response

    # Placeholder decision logic
    decision = "APPROVED"
    reasoning = "Compliance Judge not yet implemented — placeholder approval"

    logger.info("compliance_judge_decided", expense_id=expense_id, decision=decision)

    return {
        "compliance_decision": decision,
        "compliance_reasoning": reasoning,
        "audit_trail": [{
            "event": "COMPLIANCE_DECISION",
            "agent": "compliance_judge",
            "expense_id": expense_id,
            "decision": decision,
            "auditor_verdict": audit_verdict.get("verdict"),
            "fraud_score": fraud_score,
        }],
    }
