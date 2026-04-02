"""
Audit Trail Page — Decision trace viewer.

Displays the complete audit trail for a processed expense:
- Extraction results and confidence
- Policy traversal path
- Auditor verdict with cited rules
- Fraud score and flags
- Compliance Judge decision
- Remediation conversation log (if applicable)
"""

import streamlit as st


def render_audit_trail(expense_id: str, trace_data: dict) -> None:
    """Render the audit trail for an expense."""
    st.subheader(f"Audit Trail: {expense_id}")

    events = trace_data.get("events", [])

    if not events:
        st.warning("No audit events found for this expense.")
        return

    for event in events:
        with st.expander(f"🔹 {event.get('event_type', 'Unknown')} — {event.get('agent_name', 'system')}"):
            st.json(event.get("payload", {}))
            st.caption(f"Timestamp: {event.get('created_at', 'N/A')}")
