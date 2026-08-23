# Agentic AI Course

Streamlit portfolio for IITM Pravartak / FutureSense agentic AI coursework.

## Live apps *(this portfolio)*

| App | Description |
|-----|-------------|
| **Concept Explainer** | First shipped assignment — multi-audience AI tutor (OpenAI / Claude, pricing, chat, export) |
| **Abhishek Jain** | Builder profile — also covers GeM Bid System, Bharat Quant, Clerk, IntelliMatrix |

## Planned *(this portfolio)*

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
