"""Material Design 3 — minimal bento layout & micro-interactions."""

from __future__ import annotations

import html
from textwrap import dedent

import streamlit as st

from shared.projects import Project, ShippedApp

C_PRIMARY = "#1A73E8"
C_PRIMARY_CONTAINER = "#D3E3FD"
C_ON_PRIMARY = "#FFFFFF"
C_SURFACE = "#FFFFFF"
C_SURFACE_DIM = "#F8F9FA"
C_SURFACE_CONTAINER = "#F0F4F9"
C_ON_SURFACE = "#1F1F1F"
C_ON_SURFACE_VARIANT = "#444746"
C_OUTLINE_VARIANT = "#C4C7C5"
C_YELLOW = "#F9AB00"
C_TEAL = "#007B83"


def _render_html(fragment: str) -> None:
    st.html(dedent(fragment).strip())


def render_html(fragment: str) -> None:
    _render_html(fragment)


def inject_material_theme() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans+Flex:opsz,wght@6..144,400;6..144,500;6..144;700&family=Roboto:wght@400;500;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Google Sans Flex', 'Roboto', sans-serif !important;
        }}

        .stApp {{
            background: linear-gradient(165deg, #EEF3FC 0%, #FAFAFA 50%, #FFF9F5 100%) !important;
            background-attachment: fixed !important;
        }}
        .block-container {{
            padding-top: 1.25rem;
            max-width: 980px;
        }}

        /* Sidebar — minimal */
        section[data-testid="stSidebar"] {{
            background: {C_SURFACE} !important;
            border-right: 1px solid {C_OUTLINE_VARIANT} !important;
        }}
        [data-testid="stSidebarNav"] > ul > span,
        [data-testid="stSidebarNav"] > ul > small,
        [data-testid="stSidebarNav"] > ul > p {{ display: none !important; }}

        [data-testid="stSidebarNavLink"] {{
            border-radius: 12px !important;
            padding: 0.65rem 1rem !important;
            margin: 0.12rem 0.5rem !important;
            font-weight: 500 !important;
            font-size: 0.84rem !important;
            transition: background 0.2s ease, color 0.2s ease, transform 0.15s ease !important;
        }}
        [data-testid="stSidebarNavLink"]:hover {{
            background: {C_PRIMARY_CONTAINER} !important;
            color: {C_PRIMARY} !important;
            transform: translateX(2px);
        }}
        [data-testid="stSidebarNavLink"][aria-current="page"] {{
            background: {C_PRIMARY_CONTAINER} !important;
            color: {C_PRIMARY} !important;
            font-weight: 600 !important;
        }}

        /* Bento + spatial layout */
        .bento-animate {{
            animation: bentoIn 0.45s cubic-bezier(0.2, 0, 0, 1) both;
        }}
        @keyframes bentoIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .profile-hero {{
            background: linear-gradient(135deg, #1A73E8, #6366F1);
            border-radius: 24px;
            padding: 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 24px rgba(26,115,232,0.2);
            color: #fff;
            transition: box-shadow 0.3s ease;
        }}
        .profile-hero:hover {{ box-shadow: 0 12px 32px rgba(26,115,232,0.28); }}
        .profile-hero .avatar {{
            width: 64px; height: 64px; border-radius: 18px;
            background: rgba(255,255,255,0.2);
            display: flex; align-items: center; justify-content: center;
            font-size: 1.75rem; margin-bottom: 0.85rem;
        }}
        .profile-hero h1 {{ font-size: 1.85rem; font-weight: 600; margin: 0 0 0.3rem; color: #fff !important; }}
        .profile-hero .tagline {{ color: rgba(255,255,255,0.9); margin: 0; line-height: 1.5; font-size: 0.95rem; }}

        .md-hero {{
            background: {C_SURFACE};
            border-radius: 20px;
            padding: 1.5rem 1.75rem;
            margin-bottom: 1rem;
            border: 1px solid {C_OUTLINE_VARIANT};
            box-shadow: 0 1px 2px rgba(60,64,67,0.05);
            transition: box-shadow 0.25s ease, transform 0.25s ease;
        }}
        .md-hero:hover {{ box-shadow: 0 4px 16px rgba(60,64,67,0.08); transform: translateY(-1px); }}
        .md-hero h1 {{ font-size: 1.5rem; font-weight: 600; color: {C_ON_SURFACE} !important; margin: 0 0 0.35rem; }}
        .md-hero p {{ color: {C_ON_SURFACE_VARIANT}; margin: 0; font-size: 0.9rem; line-height: 1.55; }}

        .md-chip {{
            display: inline-flex;
            background: {C_PRIMARY_CONTAINER};
            color: #174EA6;
            border-radius: 999px;
            padding: 0.28rem 0.75rem;
            font-size: 0.75rem;
            font-weight: 500;
            margin: 0.2rem 0.3rem 0.2rem 0;
            transition: transform 0.15s ease;
        }}
        .md-chip:hover {{ transform: scale(1.03); }}
        .profile-hero .md-chip {{
            background: rgba(255,255,255,0.2); color: #fff;
            border: 1px solid rgba(255,255,255,0.3);
        }}

        .bento-metrics {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.75rem;
            margin: 1rem 0;
        }}
        .bento-metric {{
            background: {C_SURFACE};
            border: 1px solid {C_OUTLINE_VARIANT};
            border-radius: 16px;
            padding: 1rem;
            text-align: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .bento-metric:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(60,64,67,0.08); }}
        .bento-metric .val {{ font-size: 1.4rem; font-weight: 600; color: {C_PRIMARY}; }}
        .bento-metric .lbl {{ font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.06em; color: {C_ON_SURFACE_VARIANT}; margin-top: 0.2rem; }}

        .proj-card {{
            background: {C_SURFACE};
            border-radius: 18px;
            margin-bottom: 0.85rem;
            border: 1px solid {C_OUTLINE_VARIANT};
            overflow: hidden;
            transition: transform 0.25s cubic-bezier(0.2,0,0,1), box-shadow 0.25s ease;
        }}
        .proj-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(60,64,67,0.1);
        }}
        .proj-accent {{ height: 4px; }}
        .proj-body {{ padding: 1.15rem 1.25rem 1.25rem; }}
        .proj-head {{ display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; flex-wrap: wrap; }}
        .proj-icon {{ font-size: 1.35rem; }}
        .proj-title {{ font-size: 1rem; font-weight: 600; color: {C_ON_SURFACE}; margin: 0; flex: 1; }}
        .proj-status {{ font-size: 0.68rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 999px; }}
        .proj-gist {{ color: {C_ON_SURFACE_VARIANT}; font-size: 0.875rem; line-height: 1.6; margin: 0 0 0.75rem; }}

        .md-card {{
            background: {C_SURFACE};
            border: 1px solid {C_OUTLINE_VARIANT};
            border-radius: 16px;
            padding: 1.15rem 1.25rem;
            transition: box-shadow 0.2s ease;
        }}
        .md-card:hover {{ box-shadow: 0 4px 14px rgba(60,64,67,0.07); }}
        .md-card h3 {{ margin: 0 0 0.4rem; font-size: 0.95rem; color: {C_ON_SURFACE}; }}
        .md-card p {{ margin: 0; color: {C_ON_SURFACE_VARIANT}; font-size: 0.875rem; line-height: 1.55; }}

        .proj-meta {{ display: grid; gap: 0.5rem; }}
        .proj-meta-row {{
            background: {C_SURFACE_CONTAINER};
            border-radius: 10px;
            padding: 0.6rem 0.85rem;
            border-left: 3px solid;
        }}
        .proj-meta-label {{ font-size: 0.65rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.15rem; }}
        .proj-meta-text {{ font-size: 0.8125rem; color: {C_ON_SURFACE}; line-height: 1.5; margin: 0; }}

        .shipped-apps {{
            background: {C_SURFACE_DIM};
            border-radius: 12px;
            padding: 0.65rem 0.85rem;
            margin-top: 0.5rem;
            border: 1px dashed {C_OUTLINE_VARIANT};
        }}
        .shipped-apps-title {{ font-size: 0.65rem; font-weight: 600; letter-spacing: 0.07em; text-transform: uppercase; color: {C_PRIMARY}; margin: 0 0 0.35rem; }}
        .shipped-app-item {{ padding: 0.35rem 0; border-bottom: 1px solid {C_OUTLINE_VARIANT}; }}
        .shipped-app-item:last-child {{ border-bottom: none; }}
        .shipped-app-name {{ font-weight: 600; font-size: 0.8125rem; color: {C_ON_SURFACE}; }}
        .shipped-app-gist {{ font-size: 0.75rem; color: {C_ON_SURFACE_VARIANT}; margin: 0.1rem 0 0; }}

        .sidebar-minimal {{
            padding: 0.75rem 1rem;
            font-size: 0.72rem;
            color: {C_ON_SURFACE_VARIANT};
            border-top: 1px solid {C_OUTLINE_VARIANT};
            margin-top: auto;
        }}
        .sidebar-minimal a {{ color: {C_PRIMARY}; text-decoration: none; font-weight: 500; }}

        .md-section-label {{
            font-size: 0.65rem; font-weight: 600; letter-spacing: 0.08em;
            text-transform: uppercase; color: {C_ON_SURFACE_VARIANT};
            margin: 1.25rem 0 0.5rem;
        }}

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 18px !important;
            border-color: {C_OUTLINE_VARIANT} !important;
            background: {C_SURFACE} !important;
            transition: box-shadow 0.2s ease !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
            box-shadow: 0 4px 16px rgba(60,64,67,0.06) !important;
        }}

        .stButton > button {{
            transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        }}
        .stButton > button:active {{ transform: scale(0.98) !important; }}
        .stButton > button[kind="primary"] {{
            background: {C_PRIMARY} !important;
            color: {C_ON_PRIMARY} !important;
            border-radius: 999px !important;
            border: none !important;
        }}

        .stTextInput input, .stTextArea textarea {{
            border-radius: 12px !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }}
        .stTextInput input:focus, .stTextArea textarea:focus {{
            border-color: {C_PRIMARY} !important;
            box-shadow: 0 0 0 2px {C_PRIMARY_CONTAINER} !important;
        }}

        [data-testid="stChatMessage"] {{
            background: {C_SURFACE_CONTAINER} !important;
            border-radius: 14px !important;
            border: 1px solid {C_OUTLINE_VARIANT} !important;
            animation: bentoIn 0.3s ease both;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_base_css = inject_material_theme


def _shipped_apps_html(apps: tuple[ShippedApp, ...]) -> str:
    if not apps:
        return ""
    items = "".join(
        dedent(
            f"""
            <div class="shipped-app-item">
                <div class="shipped-app-name">{html.escape(a.name)}</div>
                <p class="shipped-app-gist">{html.escape(a.gist)}</p>
            </div>
            """
        ).strip()
        for a in apps
    )
    return dedent(
        f"""
        <div class="shipped-apps">
            <p class="shipped-apps-title">Live in this repo</p>
            {items}
        </div>
        """
    ).strip()


def render_sidebar_minimal() -> None:
    """One-line footer — use on every page sidebar."""
    _render_html(
        '<div class="sidebar-minimal"><a href="https://iamabyjain.com" target="_blank">iamabyjain.com</a></div>'
    )


def bento_metrics(items: list[tuple[str, str]]) -> None:
    cells = "".join(
        f'<div class="bento-metric bento-animate">'
        f'<div class="val">{html.escape(v)}</div><div class="lbl">{html.escape(l)}</div></div>'
        for v, l in items
    )
    _render_html(f'<div class="bento-metrics">{cells}</div>')


def profile_hero(name: str, tagline: str, pills: list[str] | None = None) -> None:
    chips = ""
    if pills:
        chips = "".join(f'<span class="md-chip">{html.escape(p)}</span>' for p in pills)
        chips = f'<div style="display:flex;flex-wrap:wrap;margin-top:0.85rem">{chips}</div>'
    _render_html(
        f"""
        <div class="profile-hero bento-animate">
            <div class="avatar">👤</div>
            <h1>{html.escape(name)}</h1>
            <p class="tagline">{html.escape(tagline)}</p>
            {chips}
        </div>
        """
    )


def hero(title: str, subtitle: str, pills: list[str] | None = None) -> None:
    chips = ""
    if pills:
        chips = "".join(f'<span class="md-chip">{html.escape(p)}</span>' for p in pills)
        chips = f'<div style="margin-top:0.75rem;display:flex;flex-wrap:wrap">{chips}</div>'
    _render_html(
        f"""
        <div class="md-hero bento-animate">
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(subtitle)}</p>
            {chips}
        </div>
        """
    )


def rich_project_card(project: Project) -> None:
    shipped = _shipped_apps_html(project.shipped_apps)
    repo_line = (
        f'<p style="font-size:0.7rem;color:{C_ON_SURFACE_VARIANT};margin:0.5rem 0 0;">'
        f'{html.escape(project.repo_hint)}</p>'
        if project.repo_hint
        else ""
    )
    _render_html(
        f"""
        <div class="proj-card bento-animate">
            <div class="proj-accent" style="background:{project.accent}"></div>
            <div class="proj-body">
                <div class="proj-head">
                    <span class="proj-icon">{project.icon}</span>
                    <p class="proj-title">{html.escape(project.name)}</p>
                    <span class="proj-status" style="background:{project.accent}18;color:{project.accent}">{html.escape(project.status)}</span>
                </div>
                <p class="proj-gist">{html.escape(project.gist)}</p>
                {shipped}
                <div class="proj-meta" style="margin-top:0.75rem">
                    <div class="proj-meta-row" style="border-color:{C_TEAL}">
                        <div class="proj-meta-label" style="color:{C_TEAL}">Industry</div>
                        <p class="proj-meta-text">{html.escape(project.industry)}</p>
                    </div>
                    <div class="proj-meta-row" style="border-color:{C_YELLOW}">
                        <div class="proj-meta-label" style="color:#B06000">Who benefits</div>
                        <p class="proj-meta-text">{html.escape(project.beneficiaries)}</p>
                    </div>
                </div>
                {repo_line}
            </div>
        </div>
        """
    )


def section_label(text: str) -> None:
    _render_html(f'<p class="md-section-label">{html.escape(text)}</p>')
