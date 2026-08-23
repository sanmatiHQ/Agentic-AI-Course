"""About Abhishek Jain — builder profile and active projects."""

import streamlit as st

from shared.ui import hero, inject_material_theme, project_card, render_sidebar_footer

inject_material_theme()

with st.sidebar:
    render_sidebar_footer()

hero(
    "Abhishek Jain",
    "Builder · Strategist · AI & procurement systems",
    pills=["iamabyjain.com", "IITM Pravartak", "Streamlit", "Agentic AI"],
)

st.link_button("Visit my website →", "https://iamabyjain.com", use_container_width=False)

st.markdown(
    """
I'm **Abhishek Jain** — I build production-minded AI systems and turn complex ideas into
shippable products. This Streamlit hub is one slice of that work, developed with **Cursor**
and deployed on **Streamlit Community Cloud**.

My site [**iamabyjain.com**](https://iamabyjain.com) is where I consolidate ventures, ideas,
and collaborations — from operations strategy to deep-tech experiments in Northeast India and beyond.
"""
)

st.divider()
st.markdown(
    """
    <p class="md-section-label">Projects I am building</p>
    """,
    unsafe_allow_html=True,
)

project_card(
    "Agentic AI Course Portfolio",
    "Hands-on Streamlit apps for IITM Pravartak / FutureSense — each course module becomes "
    "a deployable app. **Concept Explainer** (live) is the first shipped assignment: multi-audience "
    "AI tutor with OpenAI & Claude BYOK, model pricing, follow-up chat, and transcript export. "
    "More modules (LangChain agents, multi-agent orchestration, observability) landing here as they ship.",
    "Active · this repo",
)

project_card(
    "GeM Bid System",
    "Multi-agent intelligence platform for India's Government e-Marketplace — automated bid "
    "extraction, enrichment, contract analytics, marketplace intel, and tenant dashboards. "
    "Python/FastAPI mesh on Cloud Run with MongoDB Atlas.",
    "In production",
)

project_card(
    "Bharat Quant",
    "Quantitative research and execution engine focused on Indian markets — systematic signals, "
    "backtesting, and data-driven trading workflows built for Bharat-specific market structure.",
    "In development",
)

project_card(
    "Clerk",
    "Local-first personal ops assistant — mail, meetings, files, and OEM price tracking on your "
    "machine. Lightweight daily workflow bot, separate from the cloud agent mesh.",
    "Early build",
)

project_card(
    "IntelliMatrix",
    "Intelligence layer that connects structured data, embeddings, and decision workflows — "
    "turning raw business signals into actionable matrices for strategy and operations teams.",
    "In design",
)

st.divider()
st.subheader("How I work")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        """
        **Design first**  
        User flow → data → LLM → output before writing code.
        """
    )
with c2:
    st.markdown(
        """
        **Ship early**  
        Streamlit prototypes → GitHub → Community Cloud in one loop.
        """
    )
with c3:
    st.markdown(
        """
        **Build in public**  
        Each assignment is a working app, not a slide deck.
        """
    )

st.divider()
st.caption(
    "Built by Abhishek Jain · Assignment · 23 August 2026 · Cursor · latest model · "
    "[iamabyjain.com](https://iamabyjain.com)"
)
