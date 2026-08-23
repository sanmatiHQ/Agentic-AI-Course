"""Load LLM keys from Streamlit secrets — never from git or the UI."""

from __future__ import annotations

import streamlit as st


def _secret_get(*paths: str) -> str | None:
    """Read a secret by flat key or nested path (e.g. llm, openai_api_key)."""
    try:
        node: object = st.secrets
        for part in paths:
            node = node[part]  # type: ignore[index]
        text = str(node).strip()
        return text or None
    except (KeyError, FileNotFoundError, TypeError, AttributeError):
        return None


def hosted_openai_key() -> str | None:
    return _secret_get("OPENAI_API_KEY") or _secret_get("llm", "openai_api_key")


def hosted_anthropic_key() -> str | None:
    return _secret_get("ANTHROPIC_API_KEY") or _secret_get("llm", "anthropic_api_key")


def hosted_key_for(provider: str) -> str | None:
    if provider == "openai":
        return hosted_openai_key()
    if provider == "anthropic":
        return hosted_anthropic_key()
    return None


def has_hosted_keys() -> bool:
    return bool(hosted_openai_key() or hosted_anthropic_key())


def access_pin_required() -> bool:
    return bool(_secret_get("PORTFOLIO_ACCESS_PIN"))


def access_pin_valid(entered: str) -> bool:
    expected = _secret_get("PORTFOLIO_ACCESS_PIN")
    return bool(expected) and entered.strip() == expected


def resolve_api_key(provider: str, session_fallback: str) -> str | None:
    """Prefer server secrets; fall back to BYOK session key for local/demo."""
    return hosted_key_for(provider) or (session_fallback.strip() or None)
