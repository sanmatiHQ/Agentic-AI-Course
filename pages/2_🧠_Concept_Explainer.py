"""Concept Explainer — chat-first multi-audience tutor."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from shared.chat_persistence import hydrate, persist, persistence_mode_label
from shared.chat_store import (
    MAX_SAVED_CHATS,
    archive_list,
    format_transcript,
    load_chat,
    on_first_message,
    start_new_chat,
    upsert_current_chat,
)
from shared.limits import (
    MAX_CONCEPT_CHARS,
    MAX_CONTEXT_TURNS,
    MAX_FOLLOWUP_CHARS,
    MAX_TERMS,
    MAX_USER_TURNS,
    trim_api_history,
    validate_user_input,
)
from shared.llm_providers import chat, validate_and_list_models
from shared.pricing import estimate_cost_usd
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
    ce_limits_caption,
    ce_topbar,
    ce_usage_strip,
    ce_past_chats_panel,
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
    return format_transcript(
        messages,
        input_tokens=st.session_state.ce_input_tokens,
        output_tokens=st.session_state.ce_output_tokens,
    )


def _user_turn_count() -> int:
    return sum(1 for m in st.session_state.ce_messages if m["role"] == "user")


def _session_cost_usd() -> float | None:
    return estimate_cost_usd(
        st.session_state.ce_provider,
        st.session_state.ce_selected_model or "",
        st.session_state.ce_input_tokens,
        st.session_state.ce_output_tokens,
    )


def _record_usage(input_tokens: int, output_tokens: int) -> None:
    st.session_state.ce_input_tokens += input_tokens
    st.session_state.ce_output_tokens += output_tokens
    st.session_state.ce_request_count += 1


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
    return trim_api_history(history)


def _reply(user_text: str, active_key: str) -> bool:
    """Send one chat turn. Returns True if a reply was added."""
    text = user_text.strip()
    is_first = not st.session_state.ce_messages

    if err := validate_user_input(text, is_first_message=is_first):
        st.warning(err)
        return False

    if _user_turn_count() >= MAX_USER_TURNS:
        st.warning(f"Session limit reached ({MAX_USER_TURNS} questions). Start a new chat.")
        return False

    audiences = _selected_audiences()

    if is_first:
        on_first_message()
        st.session_state.ce_active_concept = text
        st.session_state.ce_active_audiences = audiences
        api_messages = [{"role": "user", "content": build_explain_prompt(text, audiences)}]
        system = SYSTEM_PROMPT
    else:
        api_messages = _api_history()
        api_messages.append({"role": "user", "content": text})
        system = FOLLOWUP_PROMPT

    with st.spinner("Thinking…"):
        result = chat(
            provider=st.session_state.ce_provider,
            api_key=active_key,
            model=st.session_state.ce_selected_model,
            messages=api_messages,
            system=system,
        )

    _record_usage(result.input_tokens, result.output_tokens)
    st.session_state.ce_messages.append({"role": "user", "content": text})
    st.session_state.ce_messages.append({"role": "assistant", "content": result.content})
    upsert_current_chat()
    return True


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
    "ce_input_tokens": 0,
    "ce_output_tokens": 0,
    "ce_request_count": 0,
    "ce_chat_archive": [],
    "ce_active_chat_id": None,
    "ce_chat_started_at": None,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

hydrate()
if not st.session_state.get("ce_hydrated"):
    st.rerun()

if access_pin_required() and not st.session_state.ce_pin_unlocked:
    render_html('<div class="md-card"><h3>Concept Explainer</h3><p>Enter access PIN.</p></div>')
    pin = st.text_input("PIN", type="password")
    if st.button("Unlock", type="primary") and access_pin_valid(pin):
        st.session_state.ce_pin_unlocked = True
        st.rerun()
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
    st.checkbox(AUDIENCES[0], key="ce_aud_sme")
    st.checkbox(AUDIENCES[1], key="ce_aud_expert")
    st.checkbox(AUDIENCES[2], key="ce_aud_tech")

    section_label("Past chats")
    st.caption(persistence_mode_label())
    saved = archive_list()
    if not saved:
        st.caption("No saved chats yet — start one below.")
    else:
        st.caption(f"{len(saved)} chat(s) this browser session")
        for item in saved[:MAX_SAVED_CHATS]:
            label = item.get("title", "Chat")
            updated = item.get("updated_at", "")[:16].replace("T", " ")
            turns = sum(1 for m in item.get("messages", []) if m.get("role") == "user")
            is_active = item["id"] == st.session_state.get("ce_active_chat_id")
            row1, row2 = st.columns([2, 1])
            with row1:
                btn_label = f"{'● ' if is_active else ''}{label}"
                if st.button(btn_label, key=f"load_{item['id']}", use_container_width=True):
                    load_chat(item["id"])
                    st.rerun()
            with row2:
                st.download_button(
                    "⬇",
                    data=format_transcript(
                        item["messages"],
                        title=item.get("title", ""),
                        input_tokens=int(item.get("input_tokens", 0)),
                        output_tokens=int(item.get("output_tokens", 0)),
                    ),
                    file_name=f"chat_{item['id']}.txt",
                    key=f"dl_{item['id']}",
                    use_container_width=True,
                )
            st.caption(f"{updated} · {turns} turn(s)")

    section_label("Session use")
    total_tok = st.session_state.ce_input_tokens + st.session_state.ce_output_tokens
    st.metric("Tokens", f"{total_tok:,}")
    cost = _session_cost_usd()
    if cost is not None:
        st.metric("Est. cost", f"${cost:.4f}")
    st.caption(f"{_user_turn_count()}/{MAX_USER_TURNS} turns · {st.session_state.ce_request_count} API calls")

    section_label("Limits")
    st.caption(
        f"≤{MAX_TERMS} terms · ≤{MAX_CONCEPT_CHARS} chars (concept) · "
        f"≤{MAX_FOLLOWUP_CHARS} chars (follow-up) · last {MAX_CONTEXT_TURNS} turns in context"
    )

    if st.session_state.ce_messages:
        st.download_button(
            "Download chat",
            data=_format_transcript(st.session_state.ce_messages),
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            use_container_width=True,
        )
    if st.button("New chat", use_container_width=True):
        start_new_chat()
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

if st.session_state.ce_request_count > 0:
    ce_usage_strip(
        st.session_state.ce_input_tokens,
        st.session_state.ce_output_tokens,
        _session_cost_usd(),
        turns=_user_turn_count(),
        max_turns=MAX_USER_TURNS,
    )
else:
    ce_limits_caption(MAX_TERMS, MAX_CONCEPT_CHARS, MAX_CONTEXT_TURNS)

ce_past_chats_panel(archive_list(), st.session_state.get("ce_active_chat_id"))

if st.session_state.ce_messages:
    dl1, dl2 = st.columns([3, 1])
    with dl2:
        st.download_button(
            "⬇ Download this chat",
            data=_format_transcript(st.session_state.ce_messages),
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            use_container_width=True,
        )

render_html('<span class="ce-chat-workspace-marker"></span>')

if not st.session_state.ce_messages:
    ce_empty_chat()
    ex1, ex2, ex3, ex4 = st.columns(4)
    for col, example in zip((ex1, ex2, ex3, ex4), EXAMPLES):
        with col:
            if st.button(example, key=f"ex_{example}", use_container_width=True):
                if _reply(example, active_key):
                    st.rerun()

for msg in st.session_state.ce_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

chat_placeholder = (
    "Explain a concept (max 400 chars)…"
    if not st.session_state.ce_messages
    else "Follow-up (max 600 chars)…"
)
if prompt := st.chat_input(chat_placeholder, max_chars=MAX_FOLLOWUP_CHARS):
    if _reply(prompt, active_key):
        st.rerun()
