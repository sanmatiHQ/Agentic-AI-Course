"""Streamlit Community Cloud entry point."""

import streamlit as st

from shared.ui import inject_material_theme

st.set_page_config(
    page_title="Abhishek Jain · Agentic AI",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_material_theme()

about = st.Page(
    "pages/1_👤_Abhishek_Jain.py",
    title="Abhishek Jain",
    icon="👤",
    default=True,
)
concept = st.Page(
    "pages/2_🧠_Concept_Explainer.py",
    title="Concept Explainer",
    icon="🧠",
)

st.navigation([about, concept]).run()
