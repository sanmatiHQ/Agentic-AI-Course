"""Reference pricing per 1M tokens (USD) — update as providers change."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelPrice:
    input_per_1m: float | None
    output_per_1m: float | None

    def label(self) -> str:
        if self.input_per_1m is None and self.output_per_1m is None:
            return "Pricing N/A"
        inp = f"${self.input_per_1m:.2f}/1M in" if self.input_per_1m is not None else "in N/A"
        out = f"${self.output_per_1m:.2f}/1M out" if self.output_per_1m is not None else "out N/A"
        return f"{inp} · {out}"


# Approximate public list prices (Aug 2026 — verify on provider sites).
OPENAI_PRICES: dict[str, ModelPrice] = {
    "gpt-4o": ModelPrice(2.50, 10.00),
    "gpt-4o-mini": ModelPrice(0.15, 0.60),
    "gpt-4.1": ModelPrice(2.00, 8.00),
    "gpt-4.1-mini": ModelPrice(0.40, 1.60),
    "gpt-4.1-nano": ModelPrice(0.10, 0.40),
    "o3-mini": ModelPrice(1.10, 4.40),
    "o1": ModelPrice(15.00, 60.00),
    "o1-mini": ModelPrice(1.10, 4.40),
}

ANTHROPIC_PRICES: dict[str, ModelPrice] = {
    "claude-opus-4-20250514": ModelPrice(15.00, 75.00),
    "claude-sonnet-4-20250514": ModelPrice(3.00, 15.00),
    "claude-3-5-haiku-20241022": ModelPrice(0.80, 4.00),
    "claude-3-5-sonnet-20241022": ModelPrice(3.00, 15.00),
    "claude-3-opus-20240229": ModelPrice(15.00, 75.00),
    "claude-3-haiku-20240307": ModelPrice(0.25, 1.25),
}


def price_for(provider: str, model_id: str) -> ModelPrice:
    table = OPENAI_PRICES if provider == "openai" else ANTHROPIC_PRICES
    if model_id in table:
        return table[model_id]
    # Prefix match for dated model IDs (e.g. gpt-4o-2024-08-06)
    for key, price in table.items():
        if model_id.startswith(key):
            return price
    return ModelPrice(None, None)
