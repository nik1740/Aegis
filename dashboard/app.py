"""
Aegis Dashboard — Streamlit Finance Manager UI.

Main application entry point. Provides:
- Pending Review: Table of expenses under review with fraud scores
- Policy Explorer: Visual Neo4j graph explorer
- Audit Trail: Decision trace viewer with full agent logs
- Analytics: 30/60/90-day spend by category, department, location
"""

import os

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Aegis — Semantic Spend Orchestrator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")

# ============================================================
# Sidebar
# ============================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.title("🛡️ Aegis")
    st.caption("Semantic Spend Orchestrator")
    st.divider()

    st.markdown("### Navigation")
    page = st.radio(
        "Select Page",
        options=["📊 Dashboard", "📋 Pending Review", "🔍 Policy Explorer", "📜 Audit Trail"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### System Status")
    st.metric("Gateway", "🟢 Online")
    st.metric("Agent Server", "🟡 Starting")
    st.metric("Neo4j", "🟢 Online")

# ============================================================
# Main Content
# ============================================================

if page == "📊 Dashboard":
    st.title("📊 Expense Analytics Dashboard")
    st.markdown("---")

    # KPI metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Submissions", "0", help="Expenses submitted this month")
    with col2:
        st.metric("Auto-Approved", "0", "0%", help="Approved without human intervention")
    with col3:
        st.metric("Fraud Flags", "0", help="Expenses flagged for potential fraud")
    with col4:
        st.metric("Avg. Processing Time", "—", help="Average end-to-end decision time")

    st.markdown("---")

    # Placeholder charts
    st.subheader("Spend by Category (30 Days)")
    st.info("📈 Charts will populate once expense data flows through the system.")

    st.subheader("Approval Rates by Department")
    st.info("📊 Department-level analytics will appear here.")

elif page == "📋 Pending Review":
    st.title("📋 Pending Review")
    st.markdown("Expenses awaiting human review or under fraud investigation.")
    st.markdown("---")

    # TODO: Fetch pending expenses from gateway API
    st.info("No expenses pending review. Submit an expense via the API to get started.")

elif page == "🔍 Policy Explorer":
    st.title("🔍 Policy Graph Explorer")
    st.markdown("Interactive visualization of the Neo4j policy knowledge graph.")
    st.markdown("---")

    # TODO: Connect to Neo4j and render graph with pyvis
    st.info("Connect Neo4j to explore the policy graph. Use `scripts/seed_neo4j.py` to populate.")

elif page == "📜 Audit Trail":
    st.title("📜 Audit Trail Viewer")
    st.markdown("Full decision trace for any processed expense.")
    st.markdown("---")

    expense_id = st.text_input("Enter Expense ID", placeholder="EXP-2026-XXXXX")

    if expense_id:
        # TODO: Fetch audit trail from gateway API
        st.warning(f"Expense {expense_id} not found. Enter a valid expense ID.")
    else:
        st.info("Enter an expense ID above to view its full audit trail.")
