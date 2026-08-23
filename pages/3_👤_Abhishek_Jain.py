"""About Abhishek Jain — builder profile and active projects."""

import streamlit as st

from shared.ui import hero, inject_base_css, project_card

inject_base_css()

hero(
    "Abhishek Jain",
    "Builder · Strategist · AI & procurement systems",
    pills=["iamabyjain.com", "IITM Pravartak", "Streamlit", "Agentic AI"],
)

st.link_button("Visit my website →", "https://iamabyjain.com", use_container_width=False)

st.markdown(
    """
I'm **Abhishek Jain** — I build production-minded AI systems and turn complex ideas into
shippable products. This portfolio is part of my **Agentic AI Course** work, developed with
**Cursor** and deployed on **Streamlit Community Cloud**.

My site [**iamabyjain.com**](https://iamabyjain.com) is where I consolidate ventures, ideas,
and collaborations — from operations strategy to deep-tech experiments in Northeast India and beyond.
"""
)

st.divider()
st.subheader("Projects I am building")

project_card(
    "Concept Explainer",
    "Multi-audience AI tutor — explain any concept for SMEs, domain experts, and engineers. "
    "OpenAI & Claude BYOK, live model pricing, follow-up chat, transcript export.",
    "Live · this repo",
)

project_card(
    "GeM Bid Intelligence System",
    "Multi-agent platform for Government e-Marketplace (GeM) procurement — bid extraction, "
    "enrichment, contracts, marketplace intelligence, and tenant dashboards. "
    "Python/FastAPI mesh on Cloud Run + MongoDB Atlas.",
    "In production",
)

project_card(
    "Agentic AI Course Portfolio",
    "Hands-on Streamlit apps for IITM Pravartak / FutureSense — each course module becomes "
    "a deployable app (LangChain agents, multi-agent orchestration, observability).",
    "Active",
)

project_card(
    "Distributed GeM Crawler",
    "Standalone crawler fleet for parallel GeM data collection — demand via MongoDB, "
    "promoted results back to platform agents.",
    "In design",
)

project_card(
    "Clerk",
    "Local-first assistant for mail, meetings, files, and OEM price tracking — "
    "personal ops bot, separate from the cloud mesh.",
    "Early build",
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
