"""Concept Explainer — chat-first multi-audience tutor."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from shared.llm_providers import chat, validate_and_list_models
from shared.prompts import FOLLOWUP_PROMPT, SYSTEM_PROMPT, build_explain_prompt
from shared.secrets_config import (
    access_pin_required,
    access_pin_valid,
    hosted_key_for,
    resolve_api_key,
)
from shared.ui import (
    ce_audience_hint,
    ce_empty_chat,
    ce_topbar,
    inject_ce_chat_layout,
    inject_material_theme,
    render_html,
    render_sidebar_minimal,
    section_label,
)

EXAMPLES = ("RAG", "Agentic AI", "Fine-tuning", "Vector DB")
AUDIENCES = (
    "SME / business leader",
    "Domain expert",
    "Technical practitioner",
)


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


def _validate_provider(provider: str, api_key: str) -> bool:
    with st.spinner("Connecting…"):
        models, err = validate_and_list_models(provider, api_key)
    if err:
        st.session_state.ce_validated = False
        st.session_state.ce_models = []
        st.error(err)
        return False
    st.session_state.ce_validated = True
    st.session_state.ce_models = models
    st.session_state.ce_selected_model = models[0].id
    return True


def _selected_audiences() -> list[str]:
    picked: list[str] = []
    if st.session_state.get("ce_aud_sme", True):
        picked.append(AUDIENCES[0])
    if st.session_state.get("ce_aud_expert", True):
        picked.append(AUDIENCES[1])
    if st.session_state.get("ce_aud_tech", True):
        picked.append(AUDIENCES[2])
    # Never block — if sidebar unchecked all, explain for everyone
    return picked or list(AUDIENCES)


def _api_history() -> list[dict[str, str]]:
    msgs = st.session_state.ce_messages
    if not msgs:
        return []
    history: list[dict[str, str]] = [
        {
            "role": "user",
            "content": build_explain_prompt(
                st.session_state.ce_active_concept,
                st.session_state.ce_active_audiences,
            ),
        }
    ]
    history.extend({"role": m["role"], "content": m["content"]} for m in msgs[1:])
    return history


def _reply(user_text: str, active_key: str) -> None:
    text = user_text.strip()
    if not text:
        return

    audiences = _selected_audiences()

    if not st.session_state.ce_messages:
        st.session_state.ce_active_concept = text
        st.session_state.ce_active_audiences = audiences
        api_messages = [{"role": "user", "content": build_explain_prompt(text, audiences)}]
        system = SYSTEM_PROMPT
    else:
        api_messages = _api_history()
        api_messages.append({"role": "user", "content": text})
        system = FOLLOWUP_PROMPT

    with st.spinner("Thinking…"):
        reply = chat(
            provider=st.session_state.ce_provider,
            api_key=active_key,
            model=st.session_state.ce_selected_model,
            messages=api_messages,
            system=system,
        )

    st.session_state.ce_messages.append({"role": "user", "content": text})
    st.session_state.ce_messages.append({"role": "assistant", "content": reply})


inject_material_theme()
inject_ce_chat_layout()

_defaults = {
    "ce_messages": [],
    "ce_validated": False,
    "ce_models": [],
    "ce_provider": "anthropic",
    "ce_byok_key": "",
    "ce_selected_model": None,
    "ce_pin_unlocked": False,
    "ce_active_concept": "",
    "ce_active_audiences": list(AUDIENCES),
    "ce_aud_sme": True,
    "ce_aud_expert": True,
    "ce_aud_tech": True,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

if access_pin_required() and not st.session_state.ce_pin_unlocked:
    render_html('<div class="md-card"><h3>Concept Explainer</h3><p>Enter access PIN.</p></div>')
    pin = st.text_input("PIN", type="password")
    if st.button("Unlock", type="primary") and access_pin_valid(pin):
        st.session_state.ce_pin_unlocked = True
        st.rerun()
    st.stop()

# ── Sidebar: settings only ────────────────────────────────────────────────────
with st.sidebar:
    section_label("Provider")
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

    hosted_key = hosted_key_for(provider)
    if hosted_key:
        st.success("Connected")
        if not st.session_state.ce_validated:
            _validate_provider(provider, hosted_key)
    else:
        byok = st.text_input("API key", type="password", placeholder="Paste key…")
        if byok != st.session_state.ce_byok_key:
            st.session_state.ce_byok_key = byok
            st.session_state.ce_validated = False
        if st.button("Validate", type="primary", use_container_width=True):
            _validate_provider(provider, byok.strip()) if byok.strip() else st.error("Enter a key.")

    if st.session_state.ce_validated and st.session_state.ce_models:
        section_label("Model")
        opts = {m.id: m for m in st.session_state.ce_models}
        sel = st.selectbox("Model", list(opts.keys()), label_visibility="collapsed")
        st.session_state.ce_selected_model = sel
        st.caption(opts[sel].price_label)

    section_label("Audience")
    st.caption("Optional — defaults to all three")
    st.checkbox(AUDIENCES[0], key="ce_aud_sme")
    st.checkbox(AUDIENCES[1], key="ce_aud_expert")
    st.checkbox(AUDIENCES[2], key="ce_aud_tech")

    if st.session_state.ce_messages:
        st.download_button(
            "Download chat",
            data=_format_transcript(st.session_state.ce_messages),
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            use_container_width=True,
        )
    if st.button("New chat", use_container_width=True):
        st.session_state.ce_messages = []
        st.session_state.ce_active_concept = ""
        st.rerun()

    render_sidebar_minimal()

# ── Chat ──────────────────────────────────────────────────────────────────────
if not st.session_state.ce_validated:
    render_html('<div class="md-card"><h3>Connect a provider</h3><p>Use the sidebar to connect OpenAI or Claude.</p></div>')
    st.stop()

active_key = resolve_api_key(st.session_state.ce_provider, st.session_state.ce_byok_key)
if not active_key:
    st.error("No API key for this provider.")
    st.stop()

ce_topbar(st.session_state.ce_provider, st.session_state.ce_selected_model or "")
ce_audience_hint(_selected_audiences())
render_html('<span class="ce-chat-workspace-marker"></span>')

if not st.session_state.ce_messages:
    ce_empty_chat()
    ex1, ex2, ex3, ex4 = st.columns(4)
    for col, example in zip((ex1, ex2, ex3, ex4), EXAMPLES):
        with col:
            if st.button(example, key=f"ex_{example}", use_container_width=True):
                _reply(example, active_key)
                st.rerun()

for msg in st.session_state.ce_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Explain a concept or ask a follow-up…"):
    _reply(prompt, active_key)
    st.rerun()
