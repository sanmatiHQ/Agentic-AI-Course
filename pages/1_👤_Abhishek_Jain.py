"""About Abhishek Jain — landing page & project portfolio."""

import streamlit as st

from shared.projects import ALL_PROJECTS, COURSE_PORTFOLIO, INDEPENDENT_PROJECTS
from shared.ui import (
    inject_material_theme,
    profile_hero,
    render_sidebar_footer,
    render_sidebar_projects,
    rich_project_card,
    section_label,
)

inject_material_theme()

with st.sidebar:
    render_sidebar_projects()
    render_sidebar_footer()

profile_hero(
    "Abhishek Jain",
    "Builder of agentic AI systems, GovTech intelligence, and tools that turn complexity into clarity.",
    pills=["iamabyjain.com", "IITM Pravartak × FutureSense", "Cursor", "Streamlit Cloud"],
)

col_a, col_b = st.columns(2)
with col_a:
    st.link_button("🌐 iamabyjain.com", "https://iamabyjain.com", use_container_width=True)
with col_b:
    if st.button("🧠 Concept Explainer", use_container_width=True, type="primary"):
        st.switch_page("pages/2_🧠_Concept_Explainer.py")

st.markdown(
    """
I'm **Abhishek Jain** — I ship production AI across **government procurement**, **quant finance**,
**agentic AI education**, and **personal productivity**. This Streamlit hub is my **live course portfolio**;
everything else listed below is built in parallel across separate codebases.
"""
)

section_label("① Course portfolio · this repo")
rich_project_card(COURSE_PORTFOLIO)

section_label("② Independent ventures")
for proj in INDEPENDENT_PROJECTS:
    rich_project_card(proj)

st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total projects", len(ALL_PROJECTS))
with c2:
    st.metric("Live apps", len(COURSE_PORTFOLIO.shipped_apps))
with c3:
    st.metric("Course", "IITM Pravartak")

with st.expander("📚 Course orientation notes (merged from FutureSense repo)"):
    st.markdown(
        "Full orientation notes for *AI Agent Workflows and Agentic Systems* — 16 modules, "
        "schedule, LMS links, evaluation criteria — are in "
        "`docs/course-orientation-notes.md` in this repo."
    )

st.caption(
    "Abhishek Jain · 23 Aug 2026 · Cursor · [iamabyjain.com](https://iamabyjain.com) · "
    "Merged: Agentic-AI-Course + FutureSense notes"
)
