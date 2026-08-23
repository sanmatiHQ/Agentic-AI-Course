"""Concept Explainer — multi-audience AI tutor with OpenAI & Claude."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from shared.llm_providers import chat, validate_and_list_models
from shared.prompts import FOLLOWUP_PROMPT, SYSTEM_PROMPT
from shared.ui import hero, inject_material_theme, render_html, render_sidebar_minimal, section_label


def _format_transcript(messages: list[dict[str, str]]) -> str:
    lines = [
        f"Concept Explainer — {datetime.now().isoformat(timespec='seconds')}",
        "Abhishek Jain · iamabyjain.com",
        "=" * 60,
        "",
    ]
    for msg in messages:
        lines.append(f"[{msg['role'].upper()}]")
        lines.append(msg["content"])
        lines.append("")
    return "\n".join(lines)


inject_material_theme()

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

# ── Sidebar: setup only (no project list) ─────────────────────────────────────
with st.sidebar:
    section_label("Setup")
    provider = st.radio(
        "Provider",
        options=["openai", "anthropic"],
        format_func=lambda x: "OpenAI" if x == "openai" else "Claude",
        horizontal=True,
        label_visibility="collapsed",
    )
    if provider != st.session_state.ce_provider:
        st.session_state.ce_provider = provider
        st.session_state.ce_validated = False
        st.session_state.ce_models = []
        st.session_state.ce_selected_model = None

    api_key = st.text_input("API key", type="password", placeholder="Paste key…")

    if st.button("Validate & load models", type="primary", use_container_width=True):
        if not api_key.strip():
            st.error("Enter an API key.")
        else:
            with st.spinner("Connecting…"):
                models, err = validate_and_list_models(provider, api_key.strip())
            if err:
                st.session_state.ce_validated = False
                st.session_state.ce_models = []
                st.error(err)
            else:
                st.session_state.ce_validated = True
                st.session_state.ce_models = models
                st.session_state.ce_api_key = api_key.strip()
                st.session_state.ce_selected_model = models[0].id
                st.success(f"{len(models)} models ready")

    if st.session_state.ce_validated and st.session_state.ce_models:
        section_label("Model")
        model_options = {m.id: m for m in st.session_state.ce_models}
        selected = st.selectbox(
            "Model",
            options=list(model_options.keys()),
            label_visibility="collapsed",
            index=(
                list(model_options.keys()).index(st.session_state.ce_selected_model)
                if st.session_state.ce_selected_model in model_options
                else 0
            ),
        )
        st.session_state.ce_selected_model = selected
        st.caption(model_options[selected].price_label)

    if st.button("Clear chat", use_container_width=True):
        st.session_state.ce_messages = []
        st.rerun()

    render_sidebar_minimal()

# ── Main bento layout ─────────────────────────────────────────────────────────
hero(
    "Concept Explainer",
    "Explain any concept for SMEs, experts, and engineers.",
    pills=["OpenAI", "Claude", "Chat", "Export"],
)

if not st.session_state.ce_validated:
    render_html(
        """
        <div class="md-card bento-animate">
            <h3>Add your API key in the sidebar</h3>
            <p>Keys stay in this browser session only — never stored on the server.</p>
        </div>
        """
    )
    st.stop()

input_tile, chat_tile = st.columns([2, 3], gap="medium")

with input_tile:
    with st.container(border=True):
        st.markdown("**Concept**")
        concept = st.text_area(
            "Concept",
            placeholder="NLP, RAG, agentic workflows…",
            height=88,
            label_visibility="collapsed",
        )
        st.markdown("**Audience**")
        audiences = st.multiselect(
            "Audience",
            options=["SME / business leader", "Domain expert", "Technical practitioner"],
            default=["SME / business leader", "Domain expert", "Technical practitioner"],
            label_visibility="collapsed",
        )
        if st.button("Explain →", type="primary", use_container_width=True, disabled=not concept.strip()):
            audience_note = ", ".join(audiences) if audiences else "all audiences"
            user_msg = f"Explain these concept(s): {concept.strip()}\n\nPrimary audiences: {audience_note}"
            with st.spinner("Generating…"):
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

with chat_tile:
    with st.container(border=True):
        st.markdown("**Conversation**")
        chat_box = st.container(height=420)
        with chat_box:
            if not st.session_state.ce_messages:
                st.caption("Your explanation appears here.")
            for msg in st.session_state.ce_messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        follow_up = st.chat_input("Follow-up question…")
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
            st.download_button(
                "Download transcript",
                data=_format_transcript(st.session_state.ce_messages),
                file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
