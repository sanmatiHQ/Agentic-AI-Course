"""About Abhishek Jain — landing page & project portfolio."""

import streamlit as st

from shared.projects import PROJECTS
from shared.ui import (
    inject_material_theme,
    profile_hero,
    render_sidebar_footer,
    rich_project_card,
    section_label,
)

inject_material_theme()

with st.sidebar:
    render_sidebar_footer()

profile_hero(
    "Abhishek Jain",
    "I build agentic AI systems, GovTech intelligence, and tools that turn complexity into clarity.",
    pills=["iamabyjain.com", "IITM Pravartak", "Cursor", "Streamlit Cloud"],
)

col_a, col_b = st.columns([1, 1])
with col_a:
    st.link_button("🌐 Visit iamabyjain.com", "https://iamabyjain.com", use_container_width=True)
with col_b:
    if st.button("🧠 Try Concept Explainer", use_container_width=True, type="primary"):
        st.switch_page("pages/2_🧠_Concept_Explainer.py")

st.markdown(
    """
I'm a **builder and strategist** who ships production AI — not slide decks. I work across
**government procurement intelligence**, **quantitative finance**, **agentic AI education**,
and **personal productivity systems**.

This hub is my **live portfolio**: every project below is something actively in motion.
I develop with **Cursor**, deploy on **Streamlit Community Cloud**, and iterate in public
as part of my **Agentic AI Course** at IITM Pravartak / FutureSense.
"""
)

section_label("Projects I am building")

for proj in PROJECTS:
    rich_project_card(
        icon=proj.icon,
        title=proj.name,
        status=proj.status,
        accent=proj.accent,
        gist=proj.gist,
        industry=proj.industry,
        beneficiaries=proj.beneficiaries,
    )

st.divider()
section_label("How I work")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        """
        **🎯 Design first**  
        Map the user, the industry pain, and the outcome before a single line of code.
        """
    )
with c2:
    st.markdown(
        """
        **🚀 Ship early**  
        Streamlit prototype → GitHub → live URL. Real users beat perfect specs.
        """
    )
with c3:
    st.markdown(
        """
        **📖 Explain deeply**  
        Every build must answer: who benefits, which industry, and what's the gist.
        """
    )

st.caption(
    "Abhishek Jain · Assignment · 23 August 2026 · Cursor · latest model · "
    "[iamabyjain.com](https://iamabyjain.com)"
)
