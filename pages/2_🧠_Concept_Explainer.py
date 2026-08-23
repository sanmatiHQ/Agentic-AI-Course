"""Concept Explainer — multi-audience AI tutor with OpenAI & Claude."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from shared.llm_providers import chat, validate_and_list_models
from shared.prompts import FOLLOWUP_PROMPT, SYSTEM_PROMPT, build_explain_prompt
from shared.secrets_config import (
    access_pin_required,
    access_pin_valid,
    has_hosted_keys,
    hosted_key_for,
    resolve_api_key,
)
from shared.ui import (
    ce_empty_chat,
    ce_topbar,
    inject_material_theme,
    render_html,
    render_sidebar_minimal,
    section_label,
)

EXAMPLE_CONCEPTS = ("RAG", "Agentic AI", "Fine-tuning", "Vector DB")
AUDIENCE_OPTIONS = (
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


def _api_history() -> list[dict[str, str]]:
    """Rebuild provider history: first turn uses full explain prompt."""
    msgs = st.session_state.ce_messages
    if not msgs:
        return []
    concept = st.session_state.get("ce_active_concept", "")
    audiences = st.session_state.get("ce_active_audiences", list(AUDIENCE_OPTIONS))
    history: list[dict[str, str]] = [
        {"role": "user", "content": build_explain_prompt(concept, audiences)}
    ]
    for m in msgs[1:]:
        history.append({"role": m["role"], "content": m["content"]})
    return history


inject_material_theme()

_defaults = {
    "ce_messages": [],
    "ce_validated": False,
    "ce_models": [],
    "ce_provider": "anthropic",
    "ce_byok_key": "",
    "ce_selected_model": None,
    "ce_pin_unlocked": False,
    "ce_concept_prefill": "",
    "ce_active_concept": "",
    "ce_active_audiences": list(AUDIENCE_OPTIONS),
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

_using_hosted = has_hosted_keys()

if access_pin_required() and not st.session_state.ce_pin_unlocked:
    render_html(
        """
        <div class="md-card bento-animate">
            <h3>Concept Explainer</h3>
            <p>Enter access PIN to continue.</p>
        </div>
        """
    )
    pin = st.text_input("Access PIN", type="password", placeholder="PIN from app owner")
    if st.button("Unlock", type="primary"):
        if access_pin_valid(pin):
            st.session_state.ce_pin_unlocked = True
            st.rerun()
        else:
            st.error("Incorrect PIN.")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
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
        st.success("Connected · server keys")
        if not st.session_state.ce_validated:
            _validate_provider(provider, hosted_key)
    else:
        st.caption("Bring your own key")
        byok = st.text_input("API key", type="password", placeholder="Paste key…")
        if byok != st.session_state.ce_byok_key:
            st.session_state.ce_byok_key = byok
            st.session_state.ce_validated = False
        if st.button("Validate & load models", type="primary", use_container_width=True):
            if not byok.strip():
                st.error("Enter an API key.")
            else:
                _validate_provider(provider, byok.strip())

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
        st.session_state.ce_concept_prefill = ""
        st.rerun()

    render_sidebar_minimal()

# ── Main workspace ──────────────────────────────────────────────────────────────
if not st.session_state.ce_validated:
    render_html(
        """
        <div class="md-card bento-animate">
            <h3>Connect a provider</h3>
            <p>Pick OpenAI or Claude in the sidebar — server keys load automatically when configured.</p>
        </div>
        """
    )
    st.stop()

active_key = resolve_api_key(st.session_state.ce_provider, st.session_state.ce_byok_key)
if not active_key:
    st.error("No API key available for this provider.")
    st.stop()

ce_topbar(st.session_state.ce_provider, st.session_state.ce_selected_model or "")

input_col, chat_col = st.columns([2, 3], gap="large")

with input_col:
    with st.container(border=True):
        render_html('<p class="ce-panel-head">What should I explain?</p>')
        concept = st.text_area(
            "Concept",
            value=st.session_state.ce_concept_prefill,
            placeholder="e.g. Retrieval-Augmented Generation, agentic workflows, fine-tuning…",
            height=100,
            label_visibility="collapsed",
        )
        if concept != st.session_state.ce_concept_prefill:
            st.session_state.ce_concept_prefill = concept

        render_html('<p class="ce-panel-head" style="margin-top:0.75rem">Quick examples</p>')
        ex_cols = st.columns(2)
        for i, example in enumerate(EXAMPLE_CONCEPTS):
            with ex_cols[i % 2]:
                if st.button(example, key=f"ex_{example}", use_container_width=True):
                    st.session_state.ce_concept_prefill = example
                    st.rerun()

        render_html('<p class="ce-panel-head" style="margin-top:0.75rem">Audience</p>')
        aud_cols = st.columns(1)
        audiences: list[str] = []
        with aud_cols[0]:
            if st.checkbox(AUDIENCE_OPTIONS[0], value=True):
                audiences.append(AUDIENCE_OPTIONS[0])
            if st.checkbox(AUDIENCE_OPTIONS[1], value=True):
                audiences.append(AUDIENCE_OPTIONS[1])
            if st.checkbox(AUDIENCE_OPTIONS[2], value=True):
                audiences.append(AUDIENCE_OPTIONS[2])

        explain = st.button(
            "Explain →",
            type="primary",
            use_container_width=True,
            disabled=not concept.strip() or not audiences,
        )
        if explain:
            prompt = build_explain_prompt(concept.strip(), audiences)
            with st.spinner("Generating explanation…"):
                reply = chat(
                    provider=st.session_state.ce_provider,
                    api_key=active_key,
                    model=st.session_state.ce_selected_model,
                    messages=[{"role": "user", "content": prompt}],
                    system=SYSTEM_PROMPT,
                )
            st.session_state.ce_active_concept = concept.strip()
            st.session_state.ce_active_audiences = audiences
            st.session_state.ce_messages = [
                {"role": "user", "content": concept.strip()},
                {"role": "assistant", "content": reply},
            ]
            st.rerun()

with chat_col:
    with st.container(border=True):
        render_html('<p class="ce-panel-head">Explanation & follow-up</p>')
        chat_box = st.container(height=460)
        with chat_box:
            if not st.session_state.ce_messages:
                ce_empty_chat()
            else:
                for msg in st.session_state.ce_messages:
                    with st.chat_message(msg["role"]):
                        if msg["role"] == "user":
                            st.markdown(f"**Concept:** {msg['content']}")
                        else:
                            st.markdown(msg["content"])

        follow_up = st.chat_input("Ask a follow-up…")
        if follow_up:
            history = _api_history()
            history.append({"role": "user", "content": follow_up})
            with st.spinner("Thinking…"):
                reply = chat(
                    provider=st.session_state.ce_provider,
                    api_key=active_key,
                    model=st.session_state.ce_selected_model,
                    messages=history,
                    system=FOLLOWUP_PROMPT,
                )
            st.session_state.ce_messages.append({"role": "user", "content": follow_up})
            st.session_state.ce_messages.append({"role": "assistant", "content": reply})
            st.rerun()

        if st.session_state.ce_messages:
            st.download_button(
                "⬇ Download transcript",
                data=_format_transcript(st.session_state.ce_messages),
                file_name=f"concept_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True,
            )

st.caption(
    "Built by Abhishek Jain · IITM Pravartak assignment · "
    "[iamabyjain.com](https://iamabyjain.com)"
)
