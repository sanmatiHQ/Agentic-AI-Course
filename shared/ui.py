"""Material Design 3 UI — vibrant Google-inspired theme."""

from __future__ import annotations

import html

import streamlit as st

# Vibrant palette (Google Material + rich dark surfaces)
C_BLUE = "#4285F4"
C_GREEN = "#34A853"
C_YELLOW = "#FBBC04"
C_RED = "#EA4335"
C_PURPLE = "#A142F4"
C_TEAL = "#00BCD4"
C_PRIMARY = "#8AB4F8"
C_ON_SURFACE = "#F1F3F4"
C_ON_VARIANT = "#BDC1C6"
C_SURFACE = "#0d1b2a"
C_SURFACE2 = "#1b263b"
C_SURFACE3 = "#243b55"
C_OUTLINE = "#415a77"


def inject_material_theme() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Flex:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Roboto Flex', 'Roboto', sans-serif !important;
        }}

        /* ── Colourful app background (not flat black) ── */
        .stApp {{
            background: linear-gradient(145deg, #0d1b2a 0%, #1b2838 35%, #1a1a40 70%, #0d2137 100%) !important;
            background-attachment: fixed !important;
        }}
        .block-container {{
            padding-top: 1.75rem;
            padding-bottom: 3rem;
            max-width: 1080px;
        }}

        /* ── Sidebar — teal/navy gradient ── */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #1e3a5f 0%, #1a2744 45%, #16213e 100%) !important;
            border-right: 1px solid rgba(66, 133, 244, 0.25) !important;
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
            border-radius: 14px !important;
            padding: 0.7rem 1rem !important;
            margin: 0.2rem 0.5rem !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            color: {C_ON_VARIANT} !important;
            transition: all 0.2s ease;
        }}
        [data-testid="stSidebarNavLink"]:hover {{
            background: rgba(66, 133, 244, 0.18) !important;
            color: {C_ON_SURFACE} !important;
        }}
        [data-testid="stSidebarNavLink"][aria-current="page"] {{
            background: linear-gradient(90deg, rgba(66,133,244,0.35), rgba(161,66,244,0.2)) !important;
            color: #fff !important;
            font-weight: 600 !important;
            border-left: 3px solid {C_BLUE} !important;
            box-shadow: 0 2px 12px rgba(66,133,244,0.2);
        }}

        /* ── Profile hero (landing) ── */
        .profile-hero {{
            background: linear-gradient(120deg, rgba(66,133,244,0.25) 0%, rgba(161,66,244,0.2) 50%, rgba(52,168,83,0.15) 100%);
            border: 1px solid rgba(138, 180, 248, 0.3);
            border-radius: 24px;
            padding: 2.5rem 2rem;
            margin-bottom: 1.75rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.35);
            position: relative;
            overflow: hidden;
        }}
        .profile-hero::before {{
            content: '';
            position: absolute;
            top: -40%;
            right: -10%;
            width: 280px;
            height: 280px;
            background: radial-gradient(circle, rgba(66,133,244,0.2) 0%, transparent 70%);
            pointer-events: none;
        }}
        .profile-hero .avatar {{
            width: 72px;
            height: 72px;
            border-radius: 50%;
            background: linear-gradient(135deg, {C_BLUE}, {C_PURPLE});
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 20px rgba(66,133,244,0.45);
        }}
        .profile-hero h1 {{
            font-size: 2.25rem;
            font-weight: 600;
            margin: 0 0 0.4rem 0;
            color: #fff;
            letter-spacing: -0.03em;
        }}
        .profile-hero .tagline {{
            color: {C_ON_VARIANT};
            font-size: 1.05rem;
            margin: 0 0 1rem 0;
            line-height: 1.5;
        }}

        /* ── Standard hero ── */
        .md-hero {{
            background: linear-gradient(120deg, rgba(66,133,244,0.22), rgba(161,66,244,0.18));
            border: 1px solid rgba(138,180,248,0.25);
            border-radius: 24px;
            padding: 2rem 2.25rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 6px 24px rgba(0,0,0,0.3);
        }}
        .md-hero h1 {{
            font-size: 2rem;
            font-weight: 600;
            margin: 0 0 0.5rem 0;
            color: #fff;
        }}
        .md-hero p {{
            color: {C_ON_VARIANT};
            margin: 0;
            line-height: 1.6;
        }}

        .md-chip {{
            display: inline-flex;
            background: rgba(66,133,244,0.2);
            color: #c8daff;
            border: 1px solid rgba(66,133,244,0.35);
            border-radius: 20px;
            padding: 0.35rem 0.9rem;
            font-size: 0.8rem;
            font-weight: 500;
            margin: 0.25rem 0.35rem 0.25rem 0;
        }}

        /* ── Rich project card ── */
        .proj-card {{
            background: linear-gradient(135deg, rgba(27,38,59,0.95), rgba(36,59,85,0.85));
            border-radius: 20px;
            padding: 0;
            margin-bottom: 1.1rem;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 4px 16px rgba(0,0,0,0.25);
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .proj-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 28px rgba(0,0,0,0.35);
        }}
        .proj-accent {{
            height: 4px;
            width: 100%;
        }}
        .proj-body {{
            padding: 1.35rem 1.5rem 1.5rem;
        }}
        .proj-head {{
            display: flex;
            align-items: center;
            gap: 0.65rem;
            margin-bottom: 0.75rem;
        }}
        .proj-icon {{
            font-size: 1.5rem;
        }}
        .proj-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #fff;
            margin: 0;
        }}
        .proj-status {{
            font-size: 0.72rem;
            font-weight: 600;
            padding: 0.2rem 0.65rem;
            border-radius: 20px;
            margin-left: auto;
            white-space: nowrap;
        }}
        .proj-gist {{
            color: {C_ON_VARIANT};
            font-size: 0.9rem;
            line-height: 1.65;
            margin: 0 0 1rem 0;
        }}
        .proj-meta {{
            display: grid;
            gap: 0.65rem;
        }}
        .proj-meta-row {{
            background: rgba(0,0,0,0.2);
            border-radius: 12px;
            padding: 0.65rem 0.85rem;
            border-left: 3px solid;
        }}
        .proj-meta-label {{
            font-size: 0.65rem;
            font-weight: 600;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            margin-bottom: 0.2rem;
            opacity: 0.75;
        }}
        .proj-meta-text {{
            font-size: 0.84rem;
            color: {C_ON_SURFACE};
            line-height: 1.55;
            margin: 0;
        }}

        .sidebar-brand {{
            padding: 1.25rem 1rem;
            border-bottom: 1px solid rgba(138,180,248,0.15);
        }}
        .sidebar-brand .logo {{
            width: 44px;
            height: 44px;
            border-radius: 14px;
            background: linear-gradient(135deg, {C_BLUE}, {C_PURPLE});
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 4px 16px rgba(66,133,244,0.4);
        }}
        .sidebar-brand .title {{
            font-size: 1rem;
            font-weight: 600;
            color: #fff;
            margin: 0;
        }}
        .sidebar-brand .subtitle {{
            font-size: 0.72rem;
            color: {C_ON_VARIANT};
            margin: 0.2rem 0 0 0;
        }}
        .sidebar-footer {{
            padding: 1rem;
            border-top: 1px solid rgba(138,180,248,0.12);
            font-size: 0.75rem;
            color: {C_ON_VARIANT};
        }}
        .sidebar-footer a {{ color: {C_PRIMARY}; text-decoration: none; }}

        .md-section-label {{
            font-size: 0.68rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: {C_PRIMARY};
            margin: 1.25rem 0 0.65rem 0;
            padding-left: 0.5rem;
        }}

        div[data-testid="stMetric"] {{
            background: linear-gradient(135deg, rgba(66,133,244,0.15), rgba(161,66,244,0.1));
            border: 1px solid rgba(138,180,248,0.2);
            border-radius: 16px;
            padding: 1rem;
        }}
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
            color: {C_PRIMARY} !important;
        }}

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 18px !important;
            border-color: rgba(138,180,248,0.2) !important;
            background: rgba(27,38,59,0.6) !important;
        }}

        .stButton > button[kind="primary"] {{
            background: linear-gradient(90deg, {C_BLUE}, {C_PURPLE}) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 100px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 14px rgba(66,133,244,0.35) !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            box-shadow: 0 6px 20px rgba(66,133,244,0.5) !important;
        }}

        .stTextInput input, .stTextArea textarea {{
            border-radius: 12px !important;
            background: rgba(27,38,59,0.8) !important;
            border-color: rgba(138,180,248,0.25) !important;
            color: {C_ON_SURFACE} !important;
        }}

        [data-testid="stChatMessage"] {{
            background: rgba(27,38,59,0.7) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(138,180,248,0.15) !important;
        }}

        h1, h2, h3 {{ color: #fff !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_base_css = inject_material_theme


def render_sidebar_brand() -> None:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="logo">👤</div>
            <p class="title">Abhishek Jain</p>
            <p class="subtitle">Agentic AI · Builder portfolio</p>
        </div>
        <p class="md-section-label" style="padding-left:1rem;">What I'm building</p>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_footer() -> None:
    st.markdown(
        """
        <div class="sidebar-footer">
            <a href="https://iamabyjain.com" target="_blank">iamabyjain.com</a><br>
            Built with Cursor · Aug 2026
        </div>
        """,
        unsafe_allow_html=True,
    )


def profile_hero(name: str, tagline: str, pills: list[str] | None = None) -> None:
    chips = ""
    if pills:
        chips = "".join(f'<span class="md-chip">{html.escape(p)}</span>' for p in pills)
        chips = f'<div style="display:flex;flex-wrap:wrap;margin-top:0.5rem">{chips}</div>'
    st.markdown(
        f"""
        <div class="profile-hero">
            <div class="avatar">👤</div>
            <h1>{html.escape(name)}</h1>
            <p class="tagline">{html.escape(tagline)}</p>
            {chips}
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, pills: list[str] | None = None) -> None:
    chips = ""
    if pills:
        chips = "".join(f'<span class="md-chip">{html.escape(p)}</span>' for p in pills)
        chips = f'<div style="margin-top:1rem;display:flex;flex-wrap:wrap">{chips}</div>'
    st.markdown(
        f'<div class="md-hero"><h1>{html.escape(title)}</h1>'
        f'<p>{html.escape(subtitle)}</p>{chips}</div>',
        unsafe_allow_html=True,
    )


def rich_project_card(
    *,
    icon: str,
    title: str,
    status: str,
    accent: str,
    gist: str,
    industry: str,
    beneficiaries: str,
) -> None:
    st.markdown(
        f"""
        <div class="proj-card">
            <div class="proj-accent" style="background:linear-gradient(90deg,{accent},{accent}88)"></div>
            <div class="proj-body">
                <div class="proj-head">
                    <span class="proj-icon">{icon}</span>
                    <p class="proj-title">{html.escape(title)}</p>
                    <span class="proj-status" style="background:{accent}33;color:{accent}">{html.escape(status)}</span>
                </div>
                <p class="proj-gist">{html.escape(gist)}</p>
                <div class="proj-meta">
                    <div class="proj-meta-row" style="border-color:{C_TEAL}">
                        <div class="proj-meta-label" style="color:{C_TEAL}">Industry</div>
                        <p class="proj-meta-text">{html.escape(industry)}</p>
                    </div>
                    <div class="proj-meta-row" style="border-color:{C_YELLOW}">
                        <div class="proj-meta-label" style="color:{C_YELLOW}">Who benefits</div>
                        <p class="proj-meta-text">{html.escape(beneficiaries)}</p>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_label(text: str) -> None:
    st.markdown(f'<p class="md-section-label">{html.escape(text)}</p>', unsafe_allow_html=True)


def project_card(title: str, description: str, status: str = "Live") -> None:
    rich_project_card(
        icon="📌",
        title=title,
        status=status,
        accent=C_BLUE,
        gist=description,
        industry="—",
        beneficiaries="—",
    )
