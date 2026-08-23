"""Material Design 3 — bright Google-inspired theme & components."""

from __future__ import annotations

import html
from textwrap import dedent

import streamlit as st

from shared.projects import Project, ShippedApp

# MD3 light palette (Google Material You)
C_PRIMARY = "#1A73E8"
C_PRIMARY_CONTAINER = "#D3E3FD"
C_ON_PRIMARY = "#FFFFFF"
C_SURFACE = "#FFFFFF"
C_SURFACE_DIM = "#F8F9FA"
C_SURFACE_CONTAINER = "#F0F4F9"
C_ON_SURFACE = "#1F1F1F"
C_ON_SURFACE_VARIANT = "#444746"
C_OUTLINE = "#747775"
C_OUTLINE_VARIANT = "#C4C7C5"
C_GREEN = "#188038"
C_YELLOW = "#F9AB00"
C_RED = "#D93025"
C_PURPLE = "#9334E6"
C_TEAL = "#007B83"


def _render_html(fragment: str) -> None:
    """Render HTML via st.html — avoids markdown code-block escaping from indented strings."""
    st.html(dedent(fragment).strip())


def render_html(fragment: str) -> None:
    _render_html(fragment)


def inject_material_theme() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans+Flex:opsz,wght@6..144,400;6..144,500;6..144;700&family=Roboto:wght@400;500;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,1,0');

        html, body, [class*="css"] {{
            font-family: 'Google Sans Flex', 'Roboto', sans-serif !important;
        }}

        /* ── Bright app shell ── */
        .stApp {{
            background: linear-gradient(180deg, #E8F0FE 0%, #F8F9FA 35%, #FFF8F0 100%) !important;
            background-attachment: fixed !important;
        }}
        .block-container {{
            padding-top: 1.5rem;
            max-width: 960px;
        }}

        /* ── Sidebar — MD3 navigation drawer (light) ── */
        section[data-testid="stSidebar"] {{
            background: {C_SURFACE} !important;
            border-right: 1px solid {C_OUTLINE_VARIANT} !important;
            box-shadow: 2px 0 8px rgba(60,64,67,0.08) !important;
        }}
        section[data-testid="stSidebar"] > div {{
            background: transparent !important;
        }}

        [data-testid="stSidebarNav"] > ul > span,
        [data-testid="stSidebarNav"] > ul > small,
        [data-testid="stSidebarNav"] > ul > p {{
            display: none !important;
        }}

        [data-testid="stSidebarNavLink"] {{
            border-radius: 100px !important;
            padding: 0.75rem 1.15rem !important;
            margin: 0.15rem 0.6rem !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            color: {C_ON_SURFACE_VARIANT} !important;
        }}
        [data-testid="stSidebarNavLink"]:hover {{
            background: {C_PRIMARY_CONTAINER} !important;
            color: {C_PRIMARY} !important;
        }}
        [data-testid="stSidebarNavLink"][aria-current="page"] {{
            background: {C_PRIMARY_CONTAINER} !important;
            color: {C_PRIMARY} !important;
            font-weight: 700 !important;
        }}

        /* ── Profile hero ── */
        .profile-hero {{
            background: linear-gradient(135deg, #1A73E8 0%, #4285F4 40%, #9334E6 100%);
            border-radius: 28px;
            padding: 2.25rem 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 8px rgba(60,64,67,0.12), 0 8px 24px rgba(26,115,232,0.25);
            color: #fff;
        }}
        .profile-hero .avatar {{
            width: 76px; height: 76px;
            border-radius: 50%;
            background: rgba(255,255,255,0.25);
            backdrop-filter: blur(8px);
            display: flex; align-items: center; justify-content: center;
            font-size: 2.25rem;
            margin-bottom: 1rem;
            border: 3px solid rgba(255,255,255,0.5);
        }}
        .profile-hero h1 {{
            font-size: 2.125rem; font-weight: 500; margin: 0 0 0.35rem;
            color: #fff !important;
        }}
        .profile-hero .tagline {{
            color: rgba(255,255,255,0.92); font-size: 1.05rem; margin: 0;
            line-height: 1.55;
        }}

        .md-hero {{
            background: {C_SURFACE};
            border-radius: 28px;
            padding: 2rem;
            margin-bottom: 1.25rem;
            border: 1px solid {C_OUTLINE_VARIANT};
            box-shadow: 0 1px 3px rgba(60,64,67,0.08), 0 4px 12px rgba(60,64,67,0.06);
        }}
        .md-hero h1 {{ font-size: 1.85rem; font-weight: 500; color: {C_ON_SURFACE} !important; margin: 0 0 0.4rem; }}
        .md-hero p {{ color: {C_ON_SURFACE_VARIANT}; margin: 0; line-height: 1.6; }}

        .md-chip {{
            display: inline-flex;
            background: {C_PRIMARY_CONTAINER};
            color: #174EA6;
            border-radius: 8px;
            padding: 0.35rem 0.85rem;
            font-size: 0.8125rem;
            font-weight: 500;
            margin: 0.25rem 0.35rem 0.25rem 0;
        }}
        .profile-hero .md-chip {{
            background: rgba(255,255,255,0.22);
            color: #fff;
            border: 1px solid rgba(255,255,255,0.35);
        }}

        /* ── Project cards — MD3 elevated surface ── */
        .proj-card {{
            background: {C_SURFACE};
            border-radius: 20px;
            margin-bottom: 1.25rem;
            border: 1px solid {C_OUTLINE_VARIANT};
            box-shadow: 0 1px 2px rgba(60,64,67,0.06), 0 2px 6px rgba(60,64,67,0.04);
            overflow: hidden;
        }}
        .proj-card:hover {{
            box-shadow: 0 2px 6px rgba(60,64,67,0.1), 0 8px 24px rgba(60,64,67,0.08);
        }}
        .proj-accent {{ height: 5px; }}
        .proj-body {{ padding: 1.35rem 1.5rem 1.5rem; }}
        .proj-head {{ display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.65rem; flex-wrap: wrap; }}
        .proj-icon {{ font-size: 1.6rem; }}
        .proj-title {{ font-size: 1.125rem; font-weight: 600; color: {C_ON_SURFACE}; margin: 0; flex: 1; }}
        .proj-status {{
            font-size: 0.72rem; font-weight: 600;
            padding: 0.25rem 0.75rem; border-radius: 100px;
        }}
        .proj-gist {{ color: {C_ON_SURFACE_VARIANT}; font-size: 0.9375rem; line-height: 1.65; margin: 0 0 1rem; }}

        .md-card {{
            background: {C_SURFACE};
            border: 1px solid {C_OUTLINE_VARIANT};
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(60,64,67,0.08);
        }}
        .md-card h3 {{ margin: 0 0 0.5rem; font-size: 1rem; color: {C_ON_SURFACE}; }}
        .md-card p {{ margin: 0; color: {C_ON_SURFACE_VARIANT}; line-height: 1.6; }}

        .proj-meta {{ display: grid; gap: 0.6rem; }}
        .proj-meta-row {{
            background: {C_SURFACE_CONTAINER};
            border-radius: 12px;
            padding: 0.75rem 1rem;
            border-left: 4px solid;
        }}
        .proj-meta-label {{
            font-size: 0.6875rem; font-weight: 600;
            letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.25rem;
        }}
        .proj-meta-text {{ font-size: 0.875rem; color: {C_ON_SURFACE}; line-height: 1.55; margin: 0; }}

        /* Shipped apps nested inside portfolio */
        .shipped-apps {{
            background: {C_SURFACE_DIM};
            border-radius: 14px;
            padding: 0.85rem 1rem;
            margin-top: 0.75rem;
            border: 1px dashed {C_OUTLINE_VARIANT};
        }}
        .shipped-apps-title {{
            font-size: 0.6875rem; font-weight: 600;
            letter-spacing: 0.08em; text-transform: uppercase;
            color: {C_PRIMARY}; margin: 0 0 0.5rem;
        }}
        .shipped-app-item {{
            display: flex; gap: 0.5rem; align-items: flex-start;
            padding: 0.5rem 0;
            border-bottom: 1px solid {C_OUTLINE_VARIANT};
        }}
        .shipped-app-item:last-child {{ border-bottom: none; }}
        .shipped-app-name {{ font-weight: 600; color: {C_ON_SURFACE}; font-size: 0.875rem; }}
        .shipped-app-gist {{ font-size: 0.8125rem; color: {C_ON_SURFACE_VARIANT}; margin: 0.15rem 0 0; }}

        .sidebar-nav-list {{
            padding: 0.5rem 1rem 0.75rem;
            font-size: 0.8125rem;
            color: {C_ON_SURFACE_VARIANT};
            line-height: 1.8;
        }}
        .sidebar-nav-list strong {{ color: {C_ON_SURFACE}; display: block; margin-bottom: 0.35rem; font-size: 0.6875rem; letter-spacing: 0.06em; text-transform: uppercase; }}
        .sidebar-footer {{
            padding: 1rem;
            border-top: 1px solid {C_OUTLINE_VARIANT};
            font-size: 0.75rem;
            color: {C_ON_SURFACE_VARIANT};
        }}
        .sidebar-footer a {{ color: {C_PRIMARY}; text-decoration: none; font-weight: 500; }}

        .md-section-label {{
            font-size: 0.6875rem; font-weight: 600;
            letter-spacing: 0.08em; text-transform: uppercase;
            color: {C_PRIMARY}; margin: 1.5rem 0 0.75rem;
        }}

        div[data-testid="stMetric"] {{
            background: {C_SURFACE};
            border: 1px solid {C_OUTLINE_VARIANT};
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 1px 2px rgba(60,64,67,0.06);
        }}
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{ color: {C_PRIMARY} !important; }}

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 20px !important;
            border-color: {C_OUTLINE_VARIANT} !important;
            background: {C_SURFACE} !important;
            box-shadow: 0 1px 3px rgba(60,64,67,0.06) !important;
        }}

        .stButton > button[kind="primary"] {{
            background: {C_PRIMARY} !important;
            color: {C_ON_PRIMARY} !important;
            border: none !important;
            border-radius: 100px !important;
            font-weight: 500 !important;
            box-shadow: 0 1px 3px rgba(60,64,67,0.15) !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            background: #1557B0 !important;
            box-shadow: 0 2px 8px rgba(26,115,232,0.35) !important;
        }}

        .stTextInput input, .stTextArea textarea {{
            border-radius: 12px !important;
            background: {C_SURFACE} !important;
            border: 1px solid {C_OUTLINE_VARIANT} !important;
            color: {C_ON_SURFACE} !important;
        }}

        [data-testid="stChatMessage"] {{
            background: {C_SURFACE_CONTAINER} !important;
            border-radius: 16px !important;
            border: 1px solid {C_OUTLINE_VARIANT} !important;
        }}

        h1, h2, h3 {{ color: {C_ON_SURFACE} !important; }}
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
                <span>▸</span>
                <div>
                    <div class="shipped-app-name">{html.escape(a.name)}</div>
                    <p class="shipped-app-gist">{html.escape(a.gist)}</p>
                </div>
            </div>
            """
        ).strip()
        for a in apps
    )
    return dedent(
        f"""
        <div class="shipped-apps">
            <p class="shipped-apps-title">Live apps in this portfolio</p>
            {items}
        </div>
        """
    ).strip()


def render_sidebar_projects() -> None:
    from shared.projects import ALL_PROJECTS

    lines = "".join(f"<div>{html.escape(p.icon)} {html.escape(p.name)}</div>" for p in ALL_PROJECTS)
    _render_html(f'<div class="sidebar-nav-list"><strong>All projects</strong>{lines}</div>')


def render_sidebar_footer() -> None:
    _render_html(
        """
        <div class="sidebar-footer">
            <a href="https://iamabyjain.com" target="_blank">iamabyjain.com</a><br>
            Abhishek Jain · Cursor · Aug 2026
        </div>
        """
    )


def profile_hero(name: str, tagline: str, pills: list[str] | None = None) -> None:
    chips = ""
    if pills:
        chips = "".join(f'<span class="md-chip">{html.escape(p)}</span>' for p in pills)
        chips = f'<div style="display:flex;flex-wrap:wrap;margin-top:1rem">{chips}</div>'
    _render_html(
        f"""
        <div class="profile-hero">
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
        chips = f'<div style="margin-top:1rem;display:flex;flex-wrap:wrap">{chips}</div>'
    _render_html(
        f"""
        <div class="md-hero">
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(subtitle)}</p>
            {chips}
        </div>
        """
    )


def rich_project_card(project: Project) -> None:
    shipped = _shipped_apps_html(project.shipped_apps)
    repo_line = (
        f'<p style="font-size:0.75rem;color:{C_ON_SURFACE_VARIANT};margin:0.75rem 0 0;">'
        f'📁 {html.escape(project.repo_hint)}</p>'
        if project.repo_hint
        else ""
    )
    _render_html(
        f"""
        <div class="proj-card">
            <div class="proj-accent" style="background:linear-gradient(90deg,{project.accent},{project.accent}99)"></div>
            <div class="proj-body">
                <div class="proj-head">
                    <span class="proj-icon">{project.icon}</span>
                    <p class="proj-title">{html.escape(project.name)}</p>
                    <span class="proj-status" style="background:{project.accent}22;color:{project.accent}">{html.escape(project.status)}</span>
                </div>
                <p class="proj-gist">{html.escape(project.gist)}</p>
                {shipped}
                <div class="proj-meta" style="margin-top:1rem">
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
