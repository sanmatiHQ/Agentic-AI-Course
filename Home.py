"""Agentic AI Course — home view."""

import streamlit as st

from shared.ui import hero, inject_base_css

inject_base_css()

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

### Apps in this portfolio

→ **Concept Explainer** — multi-audience AI tutor (live)  
→ **Abhishek Jain** — builder profile & projects at [iamabyjain.com](https://iamabyjain.com)

#### 🔜 Coming next

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
