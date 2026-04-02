"""
Expense Review Page — Detailed view for reviewing flagged expenses.

Shows:
- Expense details with receipt image
- Fraud score and flags
- Auditor and Judge verdicts
- Policy rule that was applied
- Action buttons (approve, reject, escalate)
"""

import streamlit as st


def render_expense_review(expense_id: str, expense_data: dict) -> None:
    """Render the expense review interface."""
    st.subheader(f"Expense: {expense_id}")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### Receipt Details")
        st.json(expense_data.get("extracted", {}))

    with col2:
        st.markdown("#### Decision Summary")
        # TODO: Display audit verdict, fraud score, compliance decision
        st.info("Decision data will appear here.")

    st.markdown("---")
    st.markdown("#### Agent Verdicts")
    # TODO: Display individual agent verdicts in expandable sections
