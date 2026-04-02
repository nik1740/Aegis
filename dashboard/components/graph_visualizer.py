"""
Graph Visualizer Component — pyvis network rendering for Neo4j data.
"""

import streamlit as st
import streamlit.components.v1 as components


def render_graph(nodes: list[dict], edges: list[dict], height: int = 600) -> None:
    """
    Render a Neo4j subgraph as an interactive pyvis network.

    Args:
        nodes: List of node dictionaries with keys: id, label, color, group
        edges: List of edge dictionaries with keys: from, to, label
        height: Height of the visualization in pixels
    """
    try:
        from pyvis.network import Network

        net = Network(height=f"{height}px", width="100%", bgcolor="#1a1a2e", font_color="white")
        net.barnes_hut()

        # Color scheme for different node types
        colors = {
            "Employee": "#4ecdc4",
            "Role": "#ff6b6b",
            "Department": "#45b7d1",
            "Location": "#96ceb4",
            "PolicyRule": "#ff6b6b",
            "ExpenseCategory": "#feca57",
            "Exemption": "#dfe6e9",
        }

        for node in nodes:
            group = node.get("group", "default")
            color = colors.get(group, "#888888")
            net.add_node(
                node["id"],
                label=node.get("label", node["id"]),
                color=color,
                title=str(node),
            )

        for edge in edges:
            net.add_edge(
                edge["from"],
                edge["to"],
                label=edge.get("label", ""),
                color="#636e72",
            )

        # Save to temporary HTML file and render
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w") as f:
            net.save_graph(f.name)
            with open(f.name) as html_file:
                html_content = html_file.read()
                components.html(html_content, height=height + 50)

    except ImportError:
        st.error("pyvis is required for graph visualization. Run: pip install pyvis")
