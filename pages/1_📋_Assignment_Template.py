"""Starter assignment page — duplicate and rename for each new task."""

import streamlit as st

st.set_page_config(page_title="Assignment Template", page_icon="📋")
st.title("Assignment Template")
st.info("Duplicate this file in `pages/` when you start a new assignment.")

name = st.text_input("Your name", placeholder="Enter your name")
topic = st.text_area("Assignment topic", placeholder="What are you building?")

if st.button("Submit"):
    if name and topic:
        st.success(f"Got it, {name}! Topic: {topic}")
    else:
        st.warning("Fill in both fields.")

with st.expander("Tips"):
    st.markdown(
        """
- Rename the file: `2_🧠_Module_Name.py` (number controls sidebar order).
- Put reusable logic in `shared/`.
- Add extra packages to `requirements.txt`, then `pip install -r requirements.txt`.
- For API keys, use `.streamlit/secrets.toml` locally (never commit secrets).
        """
    )
