# Agentic AI Course

Apps developed in this repository.

## Live apps

| App | Description |
|-----|-------------|
| **Concept Explainer** | Multi-audience AI tutor — OpenAI or Claude, model picker with pricing, concept explanations, follow-up chat, transcript download |
| **Abhishek Jain** | Builder profile, active projects, link to [iamabyjain.com](https://iamabyjain.com) |

## Planned

| App | Description |
|-----|-------------|
| LangChain Agent Lab | Tool-calling agent with trace viewer |
| Multi-Agent Orchestrator | Sequential and parallel agent collaboration demo |
| Workflow Builder | LangGraph / AutoGen state-machine visualiser |
| Agent Observability Dashboard | Run logs, cost, and latency monitoring |

## Local run

```bash
git clone https://github.com/sanmatiHQ/Agentic-AI-Course.git
cd Agentic-AI-Course
python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open `http://localhost:8501` in your browser.

## Cloud deploy

Deploy on [Streamlit Community Cloud](https://share.streamlit.io) — connect the GitHub repo, branch `main`, entry file `streamlit_app.py`.
