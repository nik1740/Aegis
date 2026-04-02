"""
Receipt Viewer Component — Displays receipt images with extraction overlay.
"""

import streamlit as st


def render_receipt(image_url: str, extracted_data: dict) -> None:
    """Display a receipt image alongside its extracted data."""
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Receipt Image**")
        if image_url:
            st.image(image_url, use_container_width=True)
        else:
            st.info("No receipt image available.")

    with col2:
        st.markdown("**Extracted Data**")
        st.json(extracted_data)
