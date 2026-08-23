"""Agentic AI Course — home view."""

import streamlit as st

st.title("Agentic AI Course")
st.caption("Agentic AI portfolio · IITM Pravartak / FutureSense")

st.markdown(
    """
### What I am building

This workspace is my **hands-on lab** for the *AI Agent Workflows and Agentic Systems*
programme. Each module becomes a working Streamlit app — not slideware — so concepts
stick through build-and-ship practice.

### How I develop

| Step | Approach |
|------|----------|
| **Design** | Break the assignment into user flows (input → LLM → output) before coding |
| **Build** | Python 3.11 + Streamlit multipage apps, shared helpers in `shared/` |
| **Integrate** | Bring-your-own-key for OpenAI & Claude — keys stay in the browser session only |
| **Ship** | Push to GitHub → auto-deploy on **Streamlit Community Cloud** |
| **Tooling** | **Cursor** with the latest model for pair-programming and iteration |

### Apps in this portfolio

#### 🧠 Concept Explainer *(live)*

Multi-audience tutor for any concept or keyword (e.g. NLP, RAG, agentic workflows).

- Validate **OpenAI** or **Claude** API keys with a real request
- List available models with **reference pricing**
- Explain for **SMEs**, **domain experts**, and **technical practitioners**
- Analogies + business impact + technical depth
- Follow-up chat and **download conversation** as text

→ Open **Concept Explainer** from the sidebar.

#### 🔜 Coming next (course roadmap)

| Module theme | Planned app |
|--------------|-------------|
| LangChain agents | Tool-calling agent with trace viewer |
| Multi-agent systems | Orchestrator demo (sequential & parallel) |
| LangGraph / AutoGen | Workflow builder with state diagram |
| Monitoring & observability | Agent run log + cost/latency dashboard |

Each new module adds a page here as it ships.
"""
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Platform", "Streamlit")
with col2:
    st.metric("Python", "3.11")
with col3:
    st.metric("Live apps", "1")

st.divider()
st.caption(
    "Built by Abhishek Jain as part of Assignment on 23rd August 2026 "
    "on Cursor using the latest model."
)
