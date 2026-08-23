"""Persist Concept Explainer chats beyond page refresh."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

STORAGE_KEY = "ce_chats_v1"
LOCAL_DIR = Path("data/chats")
LOCAL_FILE = LOCAL_DIR / "archive.json"
COLL_NAME = "concept_explainer_sessions"


def _secret_get(key: str) -> str | None:
    try:
        val = st.secrets.get(key)
        return str(val).strip() if val else None
    except (KeyError, FileNotFoundError, TypeError, AttributeError):
        return None


def mongo_uri() -> str | None:
    return _secret_get("MONGODB_URI") or _secret_get("MONGO_URI")


def build_bundle() -> dict[str, Any]:
    return {
        "archive": list(st.session_state.get("ce_chat_archive", [])),
        "active_chat_id": st.session_state.get("ce_active_chat_id"),
        "messages": list(st.session_state.get("ce_messages", [])),
        "active_concept": st.session_state.get("ce_active_concept", ""),
        "active_audiences": list(st.session_state.get("ce_active_audiences", [])),
        "input_tokens": int(st.session_state.get("ce_input_tokens", 0)),
        "output_tokens": int(st.session_state.get("ce_output_tokens", 0)),
        "request_count": int(st.session_state.get("ce_request_count", 0)),
        "chat_started_at": st.session_state.get("ce_chat_started_at"),
    }


def apply_bundle(bundle: dict[str, Any]) -> None:
    st.session_state.ce_chat_archive = list(bundle.get("archive", []))
    st.session_state.ce_active_chat_id = bundle.get("active_chat_id")
    st.session_state.ce_messages = list(bundle.get("messages", []))
    st.session_state.ce_active_concept = bundle.get("active_concept", "")
    st.session_state.ce_active_audiences = list(bundle.get("active_audiences", []))
    st.session_state.ce_input_tokens = int(bundle.get("input_tokens", 0))
    st.session_state.ce_output_tokens = int(bundle.get("output_tokens", 0))
    st.session_state.ce_request_count = int(bundle.get("request_count", 0))
    st.session_state.ce_chat_started_at = bundle.get("chat_started_at")


def _save_local_file(bundle: dict[str, Any]) -> None:
    try:
        LOCAL_DIR.mkdir(parents=True, exist_ok=True)
        LOCAL_FILE.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


def _load_local_file() -> dict[str, Any] | None:
    try:
        if LOCAL_FILE.is_file():
            return json.loads(LOCAL_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        pass
    return None


def _mongo_client():
    from pymongo import MongoClient

    uri = mongo_uri()
    if not uri:
        return None, None
    client = MongoClient(uri, serverSelectionTimeoutMS=4000)
    db_name = _secret_get("MONGODB_DB") or "agentic_ai_course"
    return client, client[db_name]


def _save_mongo(bundle: dict[str, Any]) -> None:
    session_key = st.session_state.get("ce_storage_key")
    if not session_key:
        return
    try:
        client, db = _mongo_client()
        if db is None:
            return
        db[COLL_NAME].update_one(
            {"_id": session_key},
            {
                "$set": {
                    "bundle": bundle,
                    "updated_at": bundle.get("archive", [{}])[0].get("updated_at") if bundle.get("archive") else None,
                }
            },
            upsert=True,
        )
        client.close()
    except Exception:
        pass


def _load_mongo(session_key: str) -> dict[str, Any] | None:
    try:
        client, db = _mongo_client()
        if db is None:
            return None
        doc = db[COLL_NAME].find_one({"_id": session_key}, {"bundle": 1})
        client.close()
        if doc and doc.get("bundle"):
            return doc["bundle"]
    except Exception:
        pass
    return None


def save_browser_storage(bundle: dict[str, Any]) -> None:
    """Write bundle to browser localStorage (survives refresh, same browser)."""
    try:
        from streamlit_javascript import st_javascript

        payload = json.dumps(json.dumps(bundle, ensure_ascii=False))
        st_javascript(f"localStorage.setItem('{STORAGE_KEY}', {payload}); null", key="ce_save_chats")
    except ImportError:
        pass


def load_browser_storage() -> dict[str, Any] | None:
    try:
        from streamlit_javascript import st_javascript

        raw = st_javascript(f"localStorage.getItem('{STORAGE_KEY}')", key="ce_load_chats")
        if raw and raw not in ("null", "undefined", ""):
            return json.loads(raw)
    except (ImportError, json.JSONDecodeError, TypeError):
        pass
    return None


def ensure_storage_key() -> str:
    """Stable key for Mongo/local — from URL param or new UUID."""
    if st.session_state.get("ce_storage_key"):
        return st.session_state.ce_storage_key
    sid = st.query_params.get("sid")
    if not sid:
        from uuid import uuid4

        sid = uuid4().hex[:12]
        st.query_params["sid"] = sid
    st.session_state.ce_storage_key = sid
    return sid


def hydrate() -> None:
    """Load saved chats once per session (browser → mongo → local file)."""
    if st.session_state.get("ce_hydrated"):
        return

    ensure_storage_key()

    bundle = load_browser_storage()
    if bundle is None:
        bundle = _load_mongo(st.session_state.ce_storage_key)
    if bundle is None:
        bundle = _load_local_file()

    if bundle and (bundle.get("archive") or bundle.get("messages")):
        apply_bundle(bundle)

    if not st.session_state.get("ce_browser_checked"):
        st.session_state.ce_browser_checked = True
        return

    st.session_state.ce_hydrated = True


def persist() -> None:
    """Save chats to browser + optional mongo + local file."""
    if not st.session_state.get("ce_hydrated"):
        return
    bundle = build_bundle()
    save_browser_storage(bundle)
    _save_mongo(bundle)
    _save_local_file(bundle)


def persistence_mode_label() -> str:
    if mongo_uri():
        return "Saved to this browser + MongoDB Atlas"
    return "Saved in this browser (survives refresh)"
