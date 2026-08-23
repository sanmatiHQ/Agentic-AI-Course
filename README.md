# Agentic AI Course

Streamlit workspace for **IITM Pravartak / FutureSense** agentic AI coursework —
assignments, labs, and portfolio projects.

**GitHub:** [sanmatiHQ/Agentic-AI-Course](https://github.com/sanmatiHQ/Agentic-AI-Course)

## Prerequisites

- Python **3.11**
- macOS / Linux (Windows: use WSL or adjust paths)

## Local setup (one time)

```bash
cd "/Users/iamabymini/Coding Projects/Agentic AI Course"
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Already done if you cloned after initial scaffold.

## Run the app

```bash
source scripts/activate.sh   # optional — activates .venv in your shell
bash scripts/run.sh
```

Opens **http://localhost:8501** with the multipage hub (`Home.py`).

**Cursor / VS Code:** open `Agentic AI Course.code-workspace` from the Coding Projects folder — the Python interpreter is preconfigured.

Alternative:

```bash
source .venv/bin/activate
streamlit run Home.py
```

## Project layout

```
Agentic AI Course/
├── Home.py                 # Main entry (multipage hub)
├── pages/                  # Sidebar pages — one file per assignment/module
├── assignments/            # Standalone apps (streamlit run assignments/…/app.py)
│   └── _template/          # Copy this for new standalone work
├── shared/                 # Reusable helpers across assignments
├── .streamlit/
│   ├── config.toml         # Theme, port, browser settings
│   └── secrets.toml.example
├── scripts/run.sh
└── requirements.txt
```

### Adding a new assignment (multipage)

1. Copy `pages/1_📋_Assignment_Template.py` → `pages/2_🧠_Your_Topic.py`
2. Edit the file — the number prefix sets sidebar order.
3. Add any new dependencies to `requirements.txt` and reinstall.

### Adding a standalone assignment

1. Copy `assignments/_template/` → `assignments/module_03/`
2. Run: `streamlit run assignments/module_03/app.py`

### API keys / secrets

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml — it is gitignored
```

In code: `st.secrets["openai"]["api_key"]`

## Streamlit Community Cloud (free)

Host apps at **no cost** via [share.streamlit.io](https://share.streamlit.io):

| Tier | Limit |
|------|--------|
| Public apps | Unlimited |
| Private apps | 1 |

### Deploy steps

1. Repo is live: [github.com/sanmatiHQ/Agentic-AI-Course](https://github.com/sanmatiHQ/Agentic-AI-Course)
2. Go to [share.streamlit.io](https://share.streamlit.io) → sign in with GitHub.
3. **Create app** → select your repo → branch `main` → main file **`Home.py`** → Deploy.
4. For private repos: Community Cloud → Settings → authorize private repo access.

Every `git push` redeploys automatically.

## Related repo

Course notes live in sibling folder:
`Agentic-AI-Classes-from-FutureSense/`

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `streamlit: command not found` | `source .venv/bin/activate` |
| Port 8501 in use | `streamlit run Home.py --server.port 8502` |
| Missing package on Cloud | Add to `requirements.txt` and push |
