"""In-session chat archive — past threads for Concept Explainer."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

import streamlit as st

from shared.chat_persistence import persist

MAX_SAVED_CHATS = 25


def _now_id() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid4().hex[:6]


def chat_title(messages: list[dict[str, str]], *, max_len: int = 42) -> str:
    for msg in messages:
        if msg.get("role") == "user":
            text = msg.get("content", "").strip()
            if len(text) > max_len:
                return text[: max_len - 1] + "…"
            return text or "Untitled chat"
    return "Untitled chat"


def format_markdown(
    messages: list[dict[str, str]],
    *,
    title: str = "",
    input_tokens: int = 0,
    output_tokens: int = 0,
    term_maps: list[dict] | None = None,
) -> str:
    heading = title or chat_title(messages)
    lines = [
        f"# Concept Explainer — {heading}",
        "",
        f"_Exported {datetime.now().isoformat(timespec='seconds')}_  ",
        "_Abhishek Jain · [iamabyjain.com](https://iamabyjain.com)_",
        "",
    ]
    if input_tokens or output_tokens:
        lines.append(f"**Tokens:** {input_tokens + output_tokens:,} ({input_tokens:,} in · {output_tokens:,} out)")
        lines.append("")
    if term_maps:
        from shared.term_mapping import term_maps_to_markdown

        lines.append(term_maps_to_markdown(term_maps))
    lines.append("---")
    lines.append("")
    for msg in messages:
        role = msg["role"]
        if role == "user":
            lines.append(f"## You")
        else:
            lines.append(f"## Assistant")
        lines.append("")
        lines.append(msg["content"])
        lines.append("")
    return "\n".join(lines)


def format_transcript(
    messages: list[dict[str, str]],
    *,
    title: str = "",
    input_tokens: int = 0,
    output_tokens: int = 0,
) -> str:
    lines = [
        f"Concept Explainer — {title or chat_title(messages)}",
        f"Exported {datetime.now().isoformat(timespec='seconds')}",
        "Abhishek Jain · iamabyjain.com",
    ]
    if input_tokens or output_tokens:
        lines.append(f"Tokens: {input_tokens + output_tokens:,} ({input_tokens:,} in · {output_tokens:,} out)")
    lines.extend(["=" * 60, ""])
    for msg in messages:
        lines.append(f"[{msg['role'].upper()}]")
        lines.append(msg["content"])
        lines.append("")
    return "\n".join(lines)


def archive_list() -> list[dict[str, Any]]:
    return st.session_state.setdefault("ce_chat_archive", [])


def active_chat_id() -> str | None:
    return st.session_state.get("ce_active_chat_id")


def set_active_chat_id(chat_id: str | None) -> None:
    st.session_state.ce_active_chat_id = chat_id


def snapshot_current_chat() -> dict[str, Any]:
    return {
        "id": active_chat_id() or _now_id(),
        "title": chat_title(st.session_state.ce_messages),
        "created_at": st.session_state.get("ce_chat_started_at") or datetime.now().isoformat(timespec="seconds"),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "messages": list(st.session_state.ce_messages),
        "active_concept": st.session_state.get("ce_active_concept", ""),
        "active_audiences": list(st.session_state.get("ce_active_audiences", [])),
        "input_tokens": int(st.session_state.get("ce_input_tokens", 0)),
        "output_tokens": int(st.session_state.get("ce_output_tokens", 0)),
        "request_count": int(st.session_state.get("ce_request_count", 0)),
        "term_maps": list(st.session_state.get("ce_term_maps", [])),
    }


def upsert_current_chat() -> None:
    """Persist the active thread into the in-session archive."""
    if not st.session_state.ce_messages:
        return
    snap = snapshot_current_chat()
    chats = archive_list()
    chat_id = snap["id"]
    set_active_chat_id(chat_id)
    for i, existing in enumerate(chats):
        if existing["id"] == chat_id:
            chats[i] = snap
            return
    chats.insert(0, snap)
    del chats[MAX_SAVED_CHATS:]
    persist()


def load_chat(chat_id: str) -> None:
    for item in archive_list():
        if item["id"] != chat_id:
            continue
        st.session_state.ce_messages = list(item["messages"])
        st.session_state.ce_active_concept = item.get("active_concept", "")
        st.session_state.ce_active_audiences = list(item.get("active_audiences", []))
        st.session_state.ce_input_tokens = int(item.get("input_tokens", 0))
        st.session_state.ce_output_tokens = int(item.get("output_tokens", 0))
        st.session_state.ce_request_count = int(item.get("request_count", 0))
        st.session_state.ce_chat_started_at = item.get("created_at")
        st.session_state.ce_term_maps = list(item.get("term_maps", []))
        set_active_chat_id(chat_id)
        persist()
        return


def start_new_chat() -> None:
    upsert_current_chat()
    st.session_state.ce_messages = []
    st.session_state.ce_active_concept = ""
    st.session_state.ce_input_tokens = 0
    st.session_state.ce_output_tokens = 0
    st.session_state.ce_request_count = 0
    st.session_state.ce_chat_started_at = None
    st.session_state.ce_term_maps = []
    set_active_chat_id(None)
    persist()


def on_first_message() -> None:
    if not st.session_state.get("ce_chat_started_at"):
        st.session_state.ce_chat_started_at = datetime.now().isoformat(timespec="seconds")
    if not active_chat_id():
        set_active_chat_id(_now_id())
