"""Material Design 3 UI — Google-inspired theme, sidebar, and components."""

from __future__ import annotations

import streamlit as st

# Material 3 dark tokens (Google-inspired)
MD_PRIMARY = "#8AB4F8"
MD_PRIMARY_CONTAINER = "#004A77"
MD_ON_PRIMARY = "#062E47"
MD_SURFACE = "#131314"
MD_SURFACE_CONTAINER = "#1E1F20"
MD_SURFACE_CONTAINER_HIGH = "#282A2C"
MD_SURFACE_CONTAINER_HIGHEST = "#333537"
MD_ON_SURFACE = "#E3E3E3"
MD_ON_SURFACE_VARIANT = "#C4C7C5"
MD_OUTLINE = "#8E918F"
MD_OUTLINE_VARIANT = "#444746"


def inject_material_theme() -> None:
    """Inject Google Material Design 3 styling globally."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Flex:wght@400;500;600&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0');

        html, body, [class*="css"] {{
            font-family: 'Roboto', 'Roboto Flex', sans-serif !important;
            letter-spacing: 0.01em;
        }}

        /* ── App shell ── */
        .stApp {{
            background: {MD_SURFACE};
        }}
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1120px;
        }}
        header[data-testid="stHeader"] {{
            background: transparent;
        }}

        /* ── Sidebar (Material navigation rail / drawer) ── */
        section[data-testid="stSidebar"] {{
            background: {MD_SURFACE_CONTAINER} !important;
            border-right: 1px solid {MD_OUTLINE_VARIANT};
        }}
        section[data-testid="stSidebar"] > div {{
            padding-top: 0.5rem;
        }}

        /* Hide default "streamlit app" section label */
        [data-testid="stSidebarNav"] ul[data-testid="stSidebarNavItems"] ~ *,
        [data-testid="stSidebarNav"] > ul > span,
        [data-testid="stSidebarNav"] > ul > small,
        [data-testid="stSidebarNav"] > ul > p {{
            display: none !important;
        }}

        /* Nav links — MD3 active indicator pill */
        [data-testid="stSidebarNav"] {{
            padding: 0 0.5rem;
        }}
        [data-testid="stSidebarNav"] ul[data-testid="stSidebarNavItems"] {{
            gap: 0.25rem;
        }}
        [data-testid="stSidebarNavLink"] {{
            border-radius: 100px !important;
            padding: 0.65rem 1.1rem !important;
            margin: 0.15rem 0.35rem !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            color: {MD_ON_SURFACE_VARIANT} !important;
            transition: background 0.2s ease, color 0.2s ease;
        }}
        [data-testid="stSidebarNavLink"]:hover {{
            background: {MD_SURFACE_CONTAINER_HIGH} !important;
            color: {MD_ON_SURFACE} !important;
        }}
        [data-testid="stSidebarNavLink"][aria-current="page"] {{
            background: {MD_PRIMARY_CONTAINER} !important;
            color: {MD_PRIMARY} !important;
            font-weight: 600 !important;
        }}

        /* ── Typography scale ── */
        h1, h2, h3 {{
            font-family: 'Roboto Flex', 'Roboto', sans-serif !important;
            font-weight: 500 !important;
            letter-spacing: -0.02em;
        }}
        h1 {{ color: {MD_ON_SURFACE}; font-size: 2rem; }}
        h2 {{ color: {MD_ON_SURFACE}; font-size: 1.35rem; }}
        h3 {{ color: {MD_ON_SURFACE}; font-size: 1.1rem; }}

        /* ── Hero (MD3 prominent banner) ── */
        .md-hero {{
            background: linear-gradient(135deg, {MD_PRIMARY_CONTAINER} 0%, {MD_SURFACE_CONTAINER_HIGHEST} 100%);
            border-radius: 28px;
            padding: 2rem 2.25rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3), 0 4px 12px rgba(0,0,0,0.25);
            border: 1px solid {MD_OUTLINE_VARIANT};
        }}
        .md-hero h1 {{
            font-size: 2.125rem;
            font-weight: 400;
            margin: 0 0 0.5rem 0;
            color: {MD_ON_SURFACE};
            letter-spacing: -0.03em;
        }}
        .md-hero p {{
            color: {MD_ON_SURFACE_VARIANT};
            margin: 0;
            font-size: 1rem;
            line-height: 1.6;
            font-weight: 400;
        }}

        /* ── Chips (MD3 filter chips) ── */
        .md-chip {{
            display: inline-flex;
            align-items: center;
            background: {MD_SURFACE_CONTAINER_HIGH};
            color: {MD_ON_SURFACE};
            border: 1px solid {MD_OUTLINE_VARIANT};
            border-radius: 8px;
            padding: 0.35rem 0.85rem;
            font-size: 0.8125rem;
            font-weight: 500;
            margin: 0.25rem 0.35rem 0.25rem 0;
        }}

        /* ── Cards (MD3 elevated / filled) ── */
        .md-card {{
            background: {MD_SURFACE_CONTAINER};
            border: 1px solid {MD_OUTLINE_VARIANT};
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 0.85rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.2);
            transition: box-shadow 0.2s ease, border-color 0.2s ease;
        }}
        .md-card:hover {{
            box-shadow: 0 2px 6px rgba(0,0,0,0.28);
            border-color: {MD_OUTLINE};
        }}
        .md-card h3 {{
            margin: 0 0 0.45rem 0;
            font-size: 1rem;
            font-weight: 500;
            color: {MD_ON_SURFACE};
        }}
        .md-card .md-badge {{
            color: {MD_PRIMARY};
            font-size: 0.75rem;
            font-weight: 500;
        }}
        .md-card p {{
            margin: 0;
            color: {MD_ON_SURFACE_VARIANT};
            font-size: 0.875rem;
            line-height: 1.6;
        }}

        /* ── Sidebar brand block ── */
        .sidebar-brand {{
            padding: 1.25rem 1rem 1rem 1rem;
            margin-bottom: 0.25rem;
            border-bottom: 1px solid {MD_OUTLINE_VARIANT};
        }}
        .sidebar-brand .logo {{
            width: 40px;
            height: 40px;
            border-radius: 12px;
            background: linear-gradient(135deg, {MD_PRIMARY} 0%, #4285F4 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 2px 8px rgba(66,133,244,0.35);
        }}
        .sidebar-brand .title {{
            font-family: 'Roboto Flex', sans-serif;
            font-size: 1.125rem;
            font-weight: 600;
            color: {MD_ON_SURFACE};
            line-height: 1.3;
            margin: 0;
        }}
        .sidebar-brand .subtitle {{
            font-size: 0.75rem;
            color: {MD_ON_SURFACE_VARIANT};
            margin: 0.25rem 0 0 0;
            font-weight: 400;
        }}
        .sidebar-footer {{
            padding: 1rem;
            margin-top: 1rem;
            border-top: 1px solid {MD_OUTLINE_VARIANT};
            font-size: 0.75rem;
            color: {MD_ON_SURFACE_VARIANT};
        }}
        .sidebar-footer a {{
            color: {MD_PRIMARY};
            text-decoration: none;
        }}

        /* ── Section label (MD3 label large) ── */
        .md-section-label {{
            font-size: 0.6875rem;
            font-weight: 500;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: {MD_ON_SURFACE_VARIANT};
            margin: 1.5rem 0 0.75rem 0;
        }}

        /* ── Streamlit widgets — MD3 polish ── */
        div[data-testid="stMetric"] {{
            background: {MD_SURFACE_CONTAINER};
            border: 1px solid {MD_OUTLINE_VARIANT};
            border-radius: 16px;
            padding: 1rem 1.25rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.15);
        }}
        div[data-testid="stMetric"] label {{
            color: {MD_ON_SURFACE_VARIANT} !important;
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
            color: {MD_PRIMARY} !important;
            font-weight: 500 !important;
        }}

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 16px !important;
            border-color: {MD_OUTLINE_VARIANT} !important;
            background: {MD_SURFACE_CONTAINER} !important;
            padding: 0.5rem !important;
        }}

        .stButton > button[kind="primary"] {{
            background: {MD_PRIMARY} !important;
            color: {MD_ON_PRIMARY} !important;
            border: none !important;
            border-radius: 100px !important;
            font-weight: 500 !important;
            padding: 0.55rem 1.5rem !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            transition: box-shadow 0.2s, filter 0.2s;
        }}
        .stButton > button[kind="primary"]:hover {{
            filter: brightness(1.08);
            box-shadow: 0 2px 8px rgba(138,180,248,0.35);
        }}
        .stButton > button[kind="secondary"] {{
            border-radius: 100px !important;
            border-color: {MD_OUTLINE} !important;
            color: {MD_PRIMARY} !important;
        }}

        .stTextInput input, .stTextArea textarea {{
            border-radius: 12px !important;
            border-color: {MD_OUTLINE_VARIANT} !important;
            background: {MD_SURFACE_CONTAINER_HIGH} !important;
            color: {MD_ON_SURFACE} !important;
        }}
        .stSelectbox div[data-baseweb="select"] > div {{
            border-radius: 12px !important;
            background: {MD_SURFACE_CONTAINER_HIGH} !important;
        }}

        hr {{
            border-color: {MD_OUTLINE_VARIANT} !important;
            margin: 1.75rem 0 !important;
        }}

        [data-testid="stChatMessage"] {{
            background: {MD_SURFACE_CONTAINER} !important;
            border-radius: 16px !important;
            border: 1px solid {MD_OUTLINE_VARIANT} !important;
            padding: 0.75rem 1rem !important;
            margin-bottom: 0.5rem !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Backward-compatible alias
inject_base_css = inject_material_theme


def render_sidebar_brand() -> None:
    """Material-style sidebar header — call from entry script."""
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="logo">🤖</div>
            <p class="title">Agentic AI Course</p>
            <p class="subtitle">IITM Pravartak · FutureSense</p>
        </div>
        <p class="md-section-label" style="padding-left:1rem;margin-top:0.75rem;">Navigate</p>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_footer() -> None:
    st.markdown(
        """
        <div class="sidebar-footer">
            Built by <strong>Abhishek Jain</strong><br>
            <a href="https://iamabyjain.com" target="_blank">iamabyjain.com</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, pills: list[str] | None = None) -> None:
    chips = ""
    if pills:
        chips = "".join(f'<span class="md-chip">{p}</span>' for p in pills)
        chips = f'<div style="margin-top:1.1rem;display:flex;flex-wrap:wrap;">{chips}</div>'
    st.markdown(
        f'<div class="md-hero"><h1>{title}</h1><p>{subtitle}</p>{chips}</div>',
        unsafe_allow_html=True,
    )


def project_card(title: str, description: str, status: str = "Live") -> None:
    st.markdown(
        f"""
        <div class="md-card">
            <h3>{title} <span class="md-badge">· {status}</span></h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_label(text: str) -> None:
    st.markdown(f'<p class="md-section-label">{text}</p>', unsafe_allow_html=True)
