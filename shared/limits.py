"""Concept Explainer — input and context limits."""

from __future__ import annotations

# User-facing caps (tune here)
MAX_CONCEPT_CHARS = 400
MAX_FOLLOWUP_CHARS = 600
MAX_TERMS = 5
MAX_USER_TURNS = 12
MAX_CONTEXT_TURNS = 6  # follow-up pairs kept in API history (after initial explain)


def count_terms(text: str) -> int:
    """Count comma/semicolon-separated concepts, else treat as one phrase."""
    parts = [p.strip() for p in text.replace(";", ",").split(",") if p.strip()]
    return len(parts) if len(parts) > 1 else 1


def validate_user_input(text: str, *, is_first_message: bool) -> str | None:
    """Return error message if input exceeds limits, else None."""
    stripped = text.strip()
    if not stripped:
        return "Enter a concept or question."

    max_chars = MAX_CONCEPT_CHARS if is_first_message else MAX_FOLLOWUP_CHARS
    if len(stripped) > max_chars:
        return f"Keep it under {max_chars} characters ({len(stripped)} now)."

    if is_first_message and count_terms(stripped) > MAX_TERMS:
        return f"Maximum {MAX_TERMS} concepts per request — use fewer comma-separated terms."

    return None


def trim_api_history(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    """Keep the initial explain prompt + the most recent follow-up turns."""
    if len(messages) <= 1:
        return messages
    first = messages[0]
    tail_budget = MAX_CONTEXT_TURNS * 2
    tail = messages[1:]
    if len(tail) > tail_budget:
        tail = tail[-tail_budget:]
    return [first, *tail]
