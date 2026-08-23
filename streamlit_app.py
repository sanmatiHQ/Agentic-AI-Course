"""Streamlit Community Cloud entry point."""

import streamlit as st

st.set_page_config(
    page_title="Agentic AI Course",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

home = st.Page("Home.py", title="Home", icon="🤖", default=True)
concept = st.Page(
    "pages/2_🧠_Concept_Explainer.py",
    title="Concept Explainer",
    icon="🧠",
)

st.navigation([home, concept]).run()
