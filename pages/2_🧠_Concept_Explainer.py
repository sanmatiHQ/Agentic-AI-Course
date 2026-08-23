"""Concept Explainer — multi-audience AI tutor with OpenAI & Claude."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from shared.llm_providers import chat, validate_and_list_models
from shared.prompts import FOLLOWUP_PROMPT, SYSTEM_PROMPT


def _format_transcript(messages: list[dict[str, str]]) -> str:
    lines = [
        f"Concept Explainer — {datetime.now().isoformat(timespec='seconds')}",
        "Built by Abhishek Jain · Assignment · 23 August 2026 · Cursor · latest model",
        "=" * 60,
        "",
    ]
    for msg in messages:
        role = msg["role"].upper()
        lines.append(f"[{role}]")
        lines.append(msg["content"])
        lines.append("")
    return "\n".join(lines)


st.set_page_config(page_title="Concept Explainer", page_icon="🧠", layout="wide")

# ── Session defaults ──────────────────────────────────────────────────────────
_defaults = {
    "ce_messages": [],
    "ce_validated": False,
    "ce_models": [],
    "ce_provider": "openai",
    "ce_api_key": "",
    "ce_selected_model": None,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── Sidebar: provider, key, models ─────────────────────────────────────────────
with st.sidebar:
    st.header("Provider & model")
    provider = st.radio(
        "LLM provider",
        options=["openai", "anthropic"],
        format_func=lambda x: "OpenAI" if x == "openai" else "Claude (Anthropic)",
        horizontal=True,
    )
    if provider != st.session_state.ce_provider:
        st.session_state.ce_provider = provider
        st.session_state.ce_validated = False
        st.session_state.ce_models = []
        st.session_state.ce_selected_model = None

    api_key = st.text_input(
        "API key",
        type="password",
        placeholder="sk-… or sk-ant-…",
        help="Stored only in this browser session — never sent to our servers.",
    )

    if st.button("Validate key & load models", type="primary", use_container_width=True):
        if not api_key.strip():
            st.error("Enter an API key first.")
        else:
            with st.spinner("Validating key…"):
                models, err = validate_and_list_models(provider, api_key.strip())
            if err:
                st.session_state.ce_validated = False
                st.session_state.ce_models = []
                st.error(f"Validation failed: {err}")
            else:
                st.session_state.ce_validated = True
                st.session_state.ce_models = models
                st.session_state.ce_api_key = api_key.strip()
                st.session_state.ce_selected_model = models[0].id
                st.success(f"Key valid — {len(models)} model(s) found.")

    if st.session_state.ce_validated and st.session_state.ce_models:
        st.divider()
        st.subheader("Available models")
        model_options = {m.id: f"{m.id}\n{m.price_label}" for m in st.session_state.ce_models}
        selected = st.selectbox(
            "Select model",
            options=list(model_options.keys()),
            format_func=lambda mid: model_options[mid],
            index=(
                list(model_options.keys()).index(st.session_state.ce_selected_model)
                if st.session_state.ce_selected_model in model_options
                else 0
            ),
        )
        st.session_state.ce_selected_model = selected
        price_label = next(m.price_label for m in st.session_state.ce_models if m.id == selected)
        st.caption(price_label)

    st.divider()
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.ce_messages = []
        st.rerun()

# ── Main layout ─────────────────────────────────────────────────────────────────
st.title("Concept Explainer")
st.caption("Explain any concept for SMEs, domain experts, and technical teams.")
st.caption(
    "_Built by Abhishek Jain as part of Assignment on 23rd August 2026 "
    "on Cursor using the latest model._"
)

if not st.session_state.ce_validated:
    st.info("Enter your OpenAI or Claude API key in the sidebar and click **Validate key & load models** to begin.")
    st.stop()

left, right = st.columns([2, 3], gap="large")

with left:
    st.subheader("Concept input")
    concept = st.text_area(
        "Concept or keywords",
        placeholder="e.g. NLP, RAG, vector databases, fine-tuning",
        height=120,
    )
    audiences = st.multiselect(
        "Tailor explanation for",
        options=["SME / business leader", "Domain expert", "Technical practitioner"],
        default=["SME / business leader", "Domain expert", "Technical practitioner"],
    )
    if st.button("Explain concept", type="primary", use_container_width=True, disabled=not concept.strip()):
        audience_note = ", ".join(audiences) if audiences else "all audiences"
        user_msg = f"Explain these concept(s): {concept.strip()}\n\nPrimary audiences: {audience_note}"
        with st.spinner("Generating explanation…"):
            reply = chat(
                provider=st.session_state.ce_provider,
                api_key=st.session_state.ce_api_key,
                model=st.session_state.ce_selected_model,
                messages=[{"role": "user", "content": user_msg}],
                system=SYSTEM_PROMPT,
            )
        st.session_state.ce_messages.append({"role": "user", "content": user_msg})
        st.session_state.ce_messages.append({"role": "assistant", "content": reply})
        st.rerun()

with right:
    st.subheader("Chat")
    chat_box = st.container(height=480)
    with chat_box:
        if not st.session_state.ce_messages:
            st.markdown("*Your explanation will appear here. Ask follow-up questions below.*")
        for msg in st.session_state.ce_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    follow_up = st.chat_input("Ask a follow-up question…")
    if follow_up:
        history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.ce_messages]
        history.append({"role": "user", "content": follow_up})
        with st.spinner("Thinking…"):
            reply = chat(
                provider=st.session_state.ce_provider,
                api_key=st.session_state.ce_api_key,
                model=st.session_state.ce_selected_model,
                messages=history,
                system=FOLLOWUP_PROMPT,
            )
        st.session_state.ce_messages.append({"role": "user", "content": follow_up})
        st.session_state.ce_messages.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.session_state.ce_messages:
        transcript = _format_transcript(st.session_state.ce_messages)
        st.download_button(
            "Download conversation (.txt)",
            data=transcript,
            file_name=f"concept_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

st.divider()
st.caption(
    "Built by Abhishek Jain · Assignment · 23 August 2026 · Cursor · latest model"
)