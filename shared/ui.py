"""Shared UI helpers — CSS and layout primitives."""

from __future__ import annotations

import streamlit as st

ACCENT = "#6366f1"
ACCENT_SOFT = "rgba(99, 102, 241, 0.15)"
SURFACE = "#1a1d29"
BORDER = "rgba(255, 255, 255, 0.08)"


def inject_base_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}
        .hero {{
            background: linear-gradient(135deg, {ACCENT_SOFT} 0%, rgba(15, 23, 42, 0.6) 100%);
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 1.75rem 2rem;
            margin-bottom: 1.25rem;
        }}
        .hero h1 {{
            font-size: 2rem;
            font-weight: 700;
            margin: 0 0 0.35rem 0;
            background: linear-gradient(90deg, #e2e8f0, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero p {{
            color: #94a3b8;
            margin: 0;
            font-size: 1rem;
        }}
        .pill {{
            display: inline-block;
            background: {ACCENT_SOFT};
            color: #c7d2fe;
            border: 1px solid rgba(99, 102, 241, 0.35);
            border-radius: 999px;
            padding: 0.25rem 0.75rem;
            font-size: 0.78rem;
            font-weight: 500;
            margin-right: 0.4rem;
            margin-bottom: 0.35rem;
        }}
        .card {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 0.75rem;
        }}
        .card h3 {{
            margin: 0 0 0.5rem 0;
            font-size: 1.05rem;
            color: #e2e8f0;
        }}
        .card p {{
            margin: 0;
            color: #94a3b8;
            font-size: 0.92rem;
            line-height: 1.55;
        }}
        .stat {{
            text-align: center;
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: 1rem;
        }}
        .stat .num {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #a5b4fc;
        }}
        .stat .lbl {{
            font-size: 0.78rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        div[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0f1117 0%, #151821 100%);
        }}
        .block-container {{
            padding-top: 1.5rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, pills: list[str] | None = None) -> None:
    pills_html = ""
    if pills:
        pills_html = "".join(f'<span class="pill">{p}</span>' for p in pills)
        pills_html = f'<div style="margin-top:0.85rem">{pills_html}</div>'
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p>{pills_html}</div>',
        unsafe_allow_html=True,
    )


def project_card(title: str, description: str, status: str = "Live") -> None:
    st.markdown(
        f"""
        <div class="card">
            <h3>{title} <span style="color:#6366f1;font-size:0.75rem;font-weight:500;">· {status}</span></h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
