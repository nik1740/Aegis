"""
Contextual Auditor Agent — GraphRAG-powered policy compliance checker.

Responsibilities:
- Receives expense data + policy subgraph from Neo4j traversal
- Compares extracted receipt data against exact policy rules
- Uses LLM (GPT-4o-mini) to evaluate justification against policy
- Returns structured verdict: PASS | FAIL | AMBIGUOUS

Critical Design Rule:
- MUST cite specific PolicyRule.id in reasoning
- MUST NOT infer or estimate policy limits — uses ONLY values from PolicySubgraph
- Uses a DIFFERENT LLM provider than the Compliance Judge
"""

import structlog

logger = structlog.get_logger()

# System prompt loaded from prompts/auditor_system.md
AUDITOR_SYSTEM_PROMPT = """You are a financial compliance auditor. You receive:
1. A structured receipt JSON with extracted merchant, amount, and line items
2. An employee-submitted justification string
3. A PolicySubgraph containing the EXACT policy rules applicable to this employee

Your task: Return a structured verdict with fields:
- verdict: "PASS" | "FAIL" | "AMBIGUOUS"
- reasoning: string explaining your decision
- confidence: float 0.0 to 1.0
- cited_rule_id: the specific PolicyRule.rule_id that applies

Rules:
- You MUST cite the specific PolicyRule.id that applies in your reason
- You MUST identify logical mismatches (e.g., "Client Entertainment" category but receipt shows only 1 person)
- You MUST NOT infer or estimate policy limits — use ONLY the values in PolicySubgraph
- If the policy subgraph is empty or no rule matches, return verdict "AMBIGUOUS"
- Output ONLY valid JSON matching the AgentVerdict schema"""


async def run(state: dict) -> dict:
    """
    Contextual Auditor node logic.

    Args:
        state: Current ExpenseState with extracted_data and policy_subgraph.

    Returns:
        Updated state with audit_verdict.
    """
    expense_id = state.get("expense_id", "unknown")
    logger.info("contextual_auditor_running", expense_id=expense_id)

    extracted_data = state.get("extracted_data", {})
    policy_subgraph = state.get("policy_subgraph", {})
    justification = state.get("submitted_justification", "")

    # TODO: Build LLM prompt with extracted_data + policy_subgraph + justification
    # TODO: Call LLM (GPT-4o-mini) with Instructor for schema enforcement
    # TODO: Parse and validate the AgentVerdict response

    # Placeholder verdict
    verdict = {
        "verdict": "AMBIGUOUS",
        "reasoning": "Auditor not yet implemented — placeholder verdict",
        "confidence": 0.0,
        "cited_rule_id": None,
    }

    logger.info("contextual_auditor_verdict", expense_id=expense_id, verdict=verdict["verdict"])

    return {
        "audit_verdict": verdict,
        "audit_trail": [{
            "event": "AUDITOR_VERDICT",
            "agent": "contextual_auditor",
            "expense_id": expense_id,
            "verdict": verdict["verdict"],
            "confidence": verdict["confidence"],
        }],
    }
