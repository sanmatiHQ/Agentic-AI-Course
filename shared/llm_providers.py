"""OpenAI and Anthropic helpers: validate keys, list models, chat."""

from __future__ import annotations

from dataclasses import dataclass

import anthropic
import openai

from shared.pricing import price_for


@dataclass
class ModelInfo:
    id: str
    provider: str
    price_label: str


@dataclass
class ChatResult:
    content: str
    input_tokens: int
    output_tokens: int


def validate_and_list_models(provider: str, api_key: str) -> tuple[list[ModelInfo], str | None]:
    """Validate API key with a minimal call and return chat-capable models."""
    try:
        if provider == "openai":
            return _openai_models(api_key)
        if provider == "anthropic":
            return _anthropic_models(api_key)
        return [], f"Unknown provider: {provider}"
    except Exception as exc:  # noqa: BLE001 — surface provider errors to UI
        return [], str(exc)


def _openai_models(api_key: str) -> tuple[list[ModelInfo], str | None]:
    client = openai.OpenAI(api_key=api_key)
    listed = client.models.list()
    chat_prefixes = ("gpt-", "o1", "o3", "o4", "chatgpt")
    models: list[ModelInfo] = []
    for item in listed.data:
        mid = item.id
        if not any(mid.startswith(p) for p in chat_prefixes):
            continue
        price = price_for("openai", mid)
        models.append(ModelInfo(id=mid, provider="openai", price_label=price.label()))
    models.sort(key=lambda m: m.id)
    if not models:
        return [], "Key valid but no chat models returned."
    return models, None


def _anthropic_models(api_key: str) -> tuple[list[ModelInfo], str | None]:
    client = anthropic.Anthropic(api_key=api_key)
    page = client.models.list(limit=100)
    models: list[ModelInfo] = []
    for item in page.data:
        mid = item.id
        price = price_for("anthropic", mid)
        models.append(ModelInfo(id=mid, provider="anthropic", price_label=price.label()))
    models.sort(key=lambda m: m.id)
    if not models:
        client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1,
            messages=[{"role": "user", "content": "ping"}],
        )
        return [], "Key valid but model list was empty."
    return models, None


def chat(
    provider: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    system: str,
    *,
    max_tokens: int = 2048,
) -> ChatResult:
    if provider == "openai":
        client = openai.OpenAI(api_key=api_key)
        payload = [{"role": "system", "content": system}, *messages]
        resp = client.chat.completions.create(
            model=model,
            messages=payload,
            max_tokens=max_tokens,
        )
        usage = resp.usage
        return ChatResult(
            content=resp.choices[0].message.content or "",
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
        )

    client = anthropic.Anthropic(api_key=api_key)
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    parts = [block.text for block in resp.content if block.type == "text"]
    return ChatResult(
        content="\n".join(parts),
        input_tokens=resp.usage.input_tokens,
        output_tokens=resp.usage.output_tokens,
    )


def embed_texts(api_key: str, texts: list[str], *, model: str = "text-embedding-3-small") -> list[list[float]]:
    if not texts:
        return []
    client = openai.OpenAI(api_key=api_key)
    resp = client.embeddings.create(model=model, input=texts)
    return [row.embedding for row in resp.data]
