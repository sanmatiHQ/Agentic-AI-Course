"""Agentic AI Course — main Streamlit hub."""

import streamlit as st

st.set_page_config(
    page_title="Agentic AI Course",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Agentic AI Course")
st.caption("Build assignments and projects here with Streamlit.")

st.success("**Concept Explainer** is live — open it from the sidebar (🧠 Concept Explainer).")

st.markdown(
    """
Welcome. This workspace is set up for **IITM Pravartak / FutureSense**
hands-on work. Use the sidebar to open assignment pages, or add new ones
under `pages/`.

### Quick start

1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
2. Run the app:
   ```bash
   bash scripts/run.sh
   ```
   Or: `streamlit run Home.py`

3. For a new assignment, copy `assignments/_template/app.py` into
   `pages/` (or run it standalone from `assignments/`).

### Deploy (Streamlit Community Cloud — free)

1. Push this repo to GitHub.
2. Sign in at [share.streamlit.io](https://share.streamlit.io) with GitHub.
3. **Create app** → pick this repo → main file: `Home.py` → Deploy.

Community Cloud includes **1 private app + unlimited public apps** at no cost.
"""
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Streamlit", st.__version__)

with col2:
    st.metric("Python", "3.11")

with col3:
    page_count = len(list(__import__("pathlib").Path("pages").glob("*.py")))
    st.metric("Pages", page_count)

st.divider()

st.subheader("Status check")
if st.button("Run hello check", type="primary"):
    st.success("Streamlit is working. You're ready to build.")
    st.balloons()
