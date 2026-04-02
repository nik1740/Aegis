"""
Policy Explorer Page — Visual Neo4j graph explorer.

Uses pyvis to render an interactive network visualization of the
policy knowledge graph, allowing finance managers to explore
employee → role → rule → category relationships.
"""

import streamlit as st


def render_policy_explorer() -> None:
    """Render the policy graph explorer."""
    st.subheader("Policy Knowledge Graph")

    # TODO: Query Neo4j for graph data
    # TODO: Build pyvis network
    # TODO: Render as HTML component in Streamlit

    st.info(
        "The policy graph explorer will show an interactive visualization "
        "of the Neo4j knowledge graph. Nodes represent employees, roles, "
        "departments, locations, and policy rules. Edges show relationships "
        "like HAS_ROLE, SUBJECT_TO, ENFORCED_BY."
    )
