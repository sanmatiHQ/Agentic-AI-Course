"""About Abhishek Jain — landing page & project portfolio."""

import streamlit as st

from shared.projects import ALL_PROJECTS, COURSE_PORTFOLIO, INDEPENDENT_PROJECTS
from shared.ui import (
    bento_metrics,
    inject_material_theme,
    intro_strip,
    profile_hero,
    render_sidebar_minimal,
    rich_project_card,
    section_label,
)

inject_material_theme()

with st.sidebar:
    render_sidebar_minimal()

profile_hero(
    "Abhishek Jain",
    "Agentic AI · GovTech · Quant · Productivity systems",
    pills=["iamabyjain.com", "IITM Pravartak", "Cursor"],
)

c1, c2 = st.columns(2)
with c1:
    st.link_button("Website", "https://iamabyjain.com", use_container_width=True)
with c2:
    if st.button("Concept Explainer →", use_container_width=True, type="primary"):
        st.switch_page("pages/2_🧠_Concept_Explainer.py")

intro_strip(
    "Production AI builder — procurement intelligence, quant finance, OSINT, agentic education, "
    "and personal ops. **This app** is the public course portfolio; other ventures are private codebases."
)

bento_metrics([
    (str(len(ALL_PROJECTS)), "Projects"),
    (str(len(COURSE_PORTFOLIO.shipped_apps)), "Live apps"),
    ("IITM", "Course"),
])

section_label("Course portfolio")
rich_project_card(COURSE_PORTFOLIO)

section_label("Independent ventures")

# Bento 2-column grid for ventures
rows = [INDEPENDENT_PROJECTS[i : i + 2] for i in range(0, len(INDEPENDENT_PROJECTS), 2)]
for row in rows:
    cols = st.columns(len(row))
    for col, proj in zip(cols, row):
        with col:
            rich_project_card(proj)

with st.expander("Course orientation notes"):
    st.caption("Merged from FutureSense repo → `docs/course-orientation-notes.md`")

st.caption("[iamabyjain.com](https://iamabyjain.com) · Abhishek Jain · Aug 2026")
