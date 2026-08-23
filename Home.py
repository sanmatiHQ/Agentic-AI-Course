"""Agentic AI Course — home view."""

import streamlit as st

from shared.ui import hero, inject_material_theme, render_sidebar_footer

inject_material_theme()

with st.sidebar:
    render_sidebar_footer()

hero(
    "Agentic AI Course",
    "Hands-on agentic AI portfolio · IITM Pravartak / FutureSense",
    pills=["Streamlit", "Python 3.11", "OpenAI · Claude", "Community Cloud"],
)

st.markdown(
    """
### What I am building

A **living portfolio** of Streamlit apps — one per course module — so every concept in
*AI Agent Workflows and Agentic Systems* becomes something you can click, use, and ship.

### How I develop

| Step | Approach |
|------|----------|
| **Design** | Map user flows (input → LLM → output) before writing code |
| **Build** | Python 3.11 + Streamlit, shared logic in `shared/` |
| **Integrate** | Bring-your-own-key — API keys stay in your browser session |
| **Ship** | GitHub → Streamlit Community Cloud auto-deploy |
| **Tooling** | Cursor with the latest model |

### Apps in this portfolio *(Agentic AI Course)*

This repo **is** the Agentic AI Course portfolio. Each page is a shipped assignment or module.

| App | Status |
|-----|--------|
| **Concept Explainer** | Live — multi-audience AI tutor (first assignment) |
| **Abhishek Jain** | Profile & wider project map → [iamabyjain.com](https://iamabyjain.com) |

#### 🔜 Coming next *(in this portfolio)*

| Module | Planned app |
|--------|-------------|
| LangChain agents | Tool-calling agent + trace viewer |
| Multi-agent systems | Sequential & parallel orchestrator |
| LangGraph / AutoGen | Workflow builder with state diagram |
| Observability | Agent run log + cost/latency dashboard |
"""
)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Platform", "Streamlit")
with c2:
    st.metric("Python", "3.11")
with c3:
    st.metric("Live apps", "1")

st.divider()
st.caption(
    "Built by [Abhishek Jain](https://iamabyjain.com) · Assignment · 23 August 2026 · Cursor"
)
