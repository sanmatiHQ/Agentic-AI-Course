"""Brilliant portfolio UI — bento spatial layout, glass cards, micro-interactions."""

from __future__ import annotations

import html
from textwrap import dedent

import streamlit as st

from shared.projects import Project, ShippedApp

# ── Design tokens ─────────────────────────────────────────────────────────────
C_PRIMARY = "#2563EB"
C_VIOLET = "#7C3AED"
C_CYAN = "#06B6D4"
C_ROSE = "#F43F5E"
C_AMBER = "#F59E0B"
C_SURFACE = "#FFFFFF"
C_ON_SURFACE = "#0F172A"
C_ON_SURFACE_VARIANT = "#475569"
C_OUTLINE = "rgba(148, 163, 184, 0.35)"


def _render_html(fragment: str) -> None:
    st.html(dedent(fragment).strip())


def render_html(fragment: str) -> None:
    _render_html(fragment)


def inject_material_theme() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
            -webkit-font-smoothing: antialiased;
        }}

        /* ── Aurora mesh background ── */
        .stApp {{
            background: #F0F4FF !important;
            background-image:
                radial-gradient(ellipse 80% 60% at 10% 0%, rgba(37,99,235,0.18) 0%, transparent 55%),
                radial-gradient(ellipse 70% 50% at 90% 10%, rgba(124,58,237,0.16) 0%, transparent 50%),
                radial-gradient(ellipse 60% 45% at 50% 100%, rgba(6,182,212,0.12) 0%, transparent 55%),
                radial-gradient(ellipse 50% 40% at 80% 80%, rgba(244,63,94,0.08) 0%, transparent 50%),
                linear-gradient(180deg, #EEF2FF 0%, #FAFAFF 40%, #FFF7ED 100%) !important;
            background-attachment: fixed !important;
        }}
        .block-container {{
            padding-top: 1.5rem;
            max-width: 1040px;
        }}

        /* ── Sidebar glass ── */
        section[data-testid="stSidebar"] {{
            background: rgba(255,255,255,0.72) !important;
            backdrop-filter: blur(20px) saturate(1.4) !important;
            -webkit-backdrop-filter: blur(20px) saturate(1.4) !important;
            border-right: 1px solid {C_OUTLINE} !important;
        }}
        [data-testid="stSidebarNav"] > ul > span,
        [data-testid="stSidebarNav"] > ul > small,
        [data-testid="stSidebarNav"] > ul > p {{ display: none !important; }}

        [data-testid="stSidebarNavLink"] {{
            border-radius: 14px !important;
            padding: 0.7rem 1rem !important;
            margin: 0.15rem 0.55rem !important;
            font-weight: 600 !important;
            font-size: 0.84rem !important;
            transition: all 0.22s cubic-bezier(0.2,0,0,1) !important;
        }}
        [data-testid="stSidebarNavLink"]:hover {{
            background: linear-gradient(135deg, rgba(37,99,235,0.12), rgba(124,58,237,0.1)) !important;
            color: {C_PRIMARY} !important;
            transform: translateX(3px);
            box-shadow: 0 2px 8px rgba(37,99,235,0.1) !important;
        }}
        [data-testid="stSidebarNavLink"][aria-current="page"] {{
            background: linear-gradient(135deg, rgba(37,99,235,0.15), rgba(124,58,237,0.12)) !important;
            color: {C_PRIMARY} !important;
            font-weight: 700 !important;
            box-shadow: inset 0 0 0 1px rgba(37,99,235,0.2) !important;
        }}

        /* ── Motion ── */
        .bento-animate {{
            animation: bentoIn 0.55s cubic-bezier(0.16, 1, 0.3, 1) both;
        }}
        .bento-animate:nth-child(2) {{ animation-delay: 0.06s; }}
        .bento-animate:nth-child(3) {{ animation-delay: 0.12s; }}
        .bento-animate:nth-child(4) {{ animation-delay: 0.18s; }}
        @keyframes bentoIn {{
            from {{ opacity: 0; transform: translateY(16px) scale(0.98); }}
            to {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}
        @keyframes shimmer {{
            0% {{ background-position: 200% center; }}
            100% {{ background-position: -200% center; }}
        }}
        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-4px); }}
        }}

        /* ── Profile hero ── */
        .profile-hero {{
            position: relative;
            background: linear-gradient(135deg, #1D4ED8 0%, #6366F1 35%, #7C3AED 70%, #0891B2 100%);
            border-radius: 28px;
            padding: 2.25rem 2.5rem;
            margin-bottom: 1.25rem;
            color: #fff;
            overflow: hidden;
            box-shadow:
                0 20px 50px rgba(37,99,235,0.28),
                0 0 0 1px rgba(255,255,255,0.15) inset;
            transition: transform 0.35s ease, box-shadow 0.35s ease;
        }}
        .profile-hero::before {{
            content: "";
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 20% 80%, rgba(255,255,255,0.15) 0%, transparent 40%),
                radial-gradient(circle at 80% 20%, rgba(255,255,255,0.12) 0%, transparent 35%);
            pointer-events: none;
        }}
        .profile-hero::after {{
            content: "";
            position: absolute;
            top: -50%; right: -20%;
            width: 60%; height: 200%;
            background: linear-gradient(105deg, transparent 40%, rgba(255,255,255,0.08) 50%, transparent 60%);
            animation: shimmer 8s linear infinite;
            pointer-events: none;
        }}
        .profile-hero:hover {{
            transform: translateY(-2px);
            box-shadow: 0 28px 60px rgba(37,99,235,0.35);
        }}
        .profile-hero .hero-inner {{ position: relative; z-index: 1; }}
        .profile-hero .avatar {{
            width: 72px; height: 72px; border-radius: 22px;
            background: rgba(255,255,255,0.18);
            backdrop-filter: blur(8px);
            border: 2px solid rgba(255,255,255,0.35);
            display: flex; align-items: center; justify-content: center;
            font-size: 2rem; margin-bottom: 1rem;
            animation: float 4s ease-in-out infinite;
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }}
        .profile-hero h1 {{
            font-size: 2.1rem; font-weight: 800; margin: 0 0 0.35rem;
            color: #fff !important; letter-spacing: -0.02em;
        }}
        .profile-hero .tagline {{
            color: rgba(255,255,255,0.92); margin: 0;
            line-height: 1.55; font-size: 1rem; font-weight: 500;
        }}

        /* ── Page hero (Concept Explainer etc.) ── */
        .md-hero {{
            position: relative;
            background: rgba(255,255,255,0.75);
            backdrop-filter: blur(16px);
            border-radius: 24px;
            padding: 1.75rem 2rem;
            margin-bottom: 1.25rem;
            border: 1px solid rgba(255,255,255,0.8);
            box-shadow: 0 8px 32px rgba(37,99,235,0.08), 0 1px 0 rgba(255,255,255,0.9) inset;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .md-hero::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; height: 4px;
            background: linear-gradient(90deg, {C_PRIMARY}, {C_VIOLET}, {C_CYAN});
        }}
        .md-hero:hover {{
            transform: translateY(-2px);
            box-shadow: 0 16px 40px rgba(37,99,235,0.12);
        }}
        .md-hero h1 {{
            font-size: 1.65rem; font-weight: 800; color: {C_ON_SURFACE} !important;
            margin: 0.5rem 0 0.4rem; letter-spacing: -0.02em;
        }}
        .md-hero p {{ color: {C_ON_SURFACE_VARIANT}; margin: 0; font-size: 0.95rem; line-height: 1.6; }}

        /* ── Chips ── */
        .md-chip {{
            display: inline-flex; align-items: center;
            background: linear-gradient(135deg, rgba(37,99,235,0.1), rgba(124,58,237,0.08));
            color: #1D4ED8;
            border: 1px solid rgba(37,99,235,0.15);
            border-radius: 999px;
            padding: 0.32rem 0.85rem;
            font-size: 0.75rem; font-weight: 600;
            margin: 0.25rem 0.35rem 0.25rem 0;
            transition: all 0.2s ease;
        }}
        .md-chip:hover {{
            transform: translateY(-1px) scale(1.04);
            box-shadow: 0 4px 12px rgba(37,99,235,0.15);
            background: linear-gradient(135deg, rgba(37,99,235,0.15), rgba(124,58,237,0.12));
        }}
        .profile-hero .md-chip {{
            background: rgba(255,255,255,0.16); color: #fff;
            border: 1px solid rgba(255,255,255,0.28);
            backdrop-filter: blur(4px);
        }}
        .profile-hero .md-chip:hover {{
            background: rgba(255,255,255,0.26);
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        }}

        /* ── Intro strip ── */
        .intro-strip {{
            background: rgba(255,255,255,0.65);
            backdrop-filter: blur(12px);
            border: 1px solid {C_OUTLINE};
            border-radius: 18px;
            padding: 1.1rem 1.35rem;
            margin: 0.75rem 0 1rem;
            font-size: 0.925rem;
            line-height: 1.65;
            color: {C_ON_SURFACE_VARIANT};
            box-shadow: 0 4px 16px rgba(15,23,42,0.04);
        }}
        .intro-strip strong {{ color: {C_ON_SURFACE}; font-weight: 700; }}

        /* ── Bento metrics ── */
        .bento-metrics {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.85rem;
            margin: 1.1rem 0 1.25rem;
        }}
        .bento-metric {{
            position: relative;
            background: rgba(255,255,255,0.8);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.9);
            border-radius: 20px;
            padding: 1.15rem 1rem;
            text-align: center;
            overflow: hidden;
            transition: all 0.28s cubic-bezier(0.2,0,0,1);
            box-shadow: 0 4px 20px rgba(15,23,42,0.05);
        }}
        .bento-metric::before {{
            content: "";
            position: absolute;
            inset: 0;
            opacity: 0;
            transition: opacity 0.3s ease;
            background: linear-gradient(135deg, rgba(37,99,235,0.06), rgba(124,58,237,0.06));
        }}
        .bento-metric:hover {{
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 12px 32px rgba(37,99,235,0.12);
        }}
        .bento-metric:hover::before {{ opacity: 1; }}
        .bento-metric .val {{
            font-size: 1.75rem; font-weight: 800; letter-spacing: -0.03em;
            background: linear-gradient(135deg, {C_PRIMARY}, {C_VIOLET});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
        }}
        .bento-metric .lbl {{
            font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.1em;
            color: {C_ON_SURFACE_VARIANT}; margin-top: 0.25rem; font-weight: 600;
            position: relative;
        }}

        /* ── Project cards ── */
        .proj-card {{
            position: relative;
            background: rgba(255,255,255,0.82);
            backdrop-filter: blur(14px);
            border-radius: 22px;
            margin-bottom: 0.9rem;
            border: 1px solid rgba(255,255,255,0.95);
            overflow: hidden;
            transition: all 0.32s cubic-bezier(0.2,0,0,1);
            box-shadow: 0 4px 24px rgba(15,23,42,0.06);
        }}
        .proj-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 48px rgba(15,23,42,0.1);
        }}
        .proj-accent {{
            height: 5px;
            background: var(--proj-accent, {C_PRIMARY}) !important;
        }}
        .proj-body {{ padding: 1.25rem 1.35rem 1.35rem; }}
        .proj-head {{
            display: flex; align-items: center; gap: 0.65rem;
            margin-bottom: 0.65rem; flex-wrap: wrap;
        }}
        .proj-icon-wrap {{
            width: 44px; height: 44px; border-radius: 14px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.35rem; flex-shrink: 0;
            background: var(--proj-accent-bg, rgba(37,99,235,0.1));
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: transform 0.25s ease;
        }}
        .proj-card:hover .proj-icon-wrap {{ transform: scale(1.08) rotate(-3deg); }}
        .proj-title {{
            font-size: 1.05rem; font-weight: 700; color: {C_ON_SURFACE};
            margin: 0; flex: 1; letter-spacing: -0.01em;
        }}
        .proj-status {{
            font-size: 0.65rem; font-weight: 700; padding: 0.28rem 0.7rem;
            border-radius: 999px; letter-spacing: 0.02em;
            white-space: nowrap;
        }}
        .proj-gist {{
            color: {C_ON_SURFACE_VARIANT}; font-size: 0.875rem;
            line-height: 1.65; margin: 0 0 0.85rem;
        }}

        .md-card {{
            background: rgba(255,255,255,0.8);
            backdrop-filter: blur(14px);
            border: 1px solid {C_OUTLINE};
            border-radius: 20px;
            padding: 1.35rem 1.5rem;
            box-shadow: 0 8px 28px rgba(37,99,235,0.07);
            transition: all 0.28s ease;
        }}
        .md-card:hover {{
            box-shadow: 0 16px 40px rgba(37,99,235,0.11);
            transform: translateY(-2px);
        }}
        .md-card h3 {{
            margin: 0 0 0.45rem; font-size: 1rem; font-weight: 700;
            color: {C_ON_SURFACE}; letter-spacing: -0.01em;
        }}
        .md-card p {{ margin: 0; color: {C_ON_SURFACE_VARIANT}; font-size: 0.875rem; line-height: 1.6; }}

        .proj-meta {{ display: grid; gap: 0.55rem; }}
        .proj-meta-row {{
            background: linear-gradient(135deg, rgba(248,250,252,0.9), rgba(241,245,249,0.8));
            border-radius: 12px;
            padding: 0.7rem 0.95rem;
            border-left: 3px solid;
            transition: transform 0.2s ease;
        }}
        .proj-meta-row:hover {{ transform: translateX(3px); }}
        .proj-meta-label {{
            font-size: 0.62rem; font-weight: 700; letter-spacing: 0.08em;
            text-transform: uppercase; margin-bottom: 0.2rem;
        }}
        .proj-meta-text {{
            font-size: 0.8125rem; color: {C_ON_SURFACE}; line-height: 1.55; margin: 0;
        }}

        .shipped-apps {{
            background: linear-gradient(135deg, rgba(37,99,235,0.05), rgba(124,58,237,0.04));
            border-radius: 14px;
            padding: 0.75rem 0.95rem;
            margin-top: 0.55rem;
            border: 1px dashed rgba(37,99,235,0.2);
        }}
        .shipped-apps-title {{
            font-size: 0.62rem; font-weight: 700; letter-spacing: 0.09em;
            text-transform: uppercase;
            background: linear-gradient(90deg, {C_PRIMARY}, {C_VIOLET});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 0.4rem;
        }}
        .shipped-app-item {{ padding: 0.4rem 0; border-bottom: 1px solid rgba(148,163,184,0.2); }}
        .shipped-app-item:last-child {{ border-bottom: none; }}
        .shipped-app-name {{ font-weight: 700; font-size: 0.8125rem; color: {C_ON_SURFACE}; }}
        .shipped-app-gist {{ font-size: 0.75rem; color: {C_ON_SURFACE_VARIANT}; margin: 0.12rem 0 0; }}

        .sidebar-minimal {{
            padding: 0.85rem 1rem;
            font-size: 0.72rem;
            color: {C_ON_SURFACE_VARIANT};
            border-top: 1px solid {C_OUTLINE};
            margin-top: auto;
        }}
        .sidebar-minimal a {{
            color: {C_PRIMARY}; text-decoration: none; font-weight: 700;
            transition: color 0.2s ease;
        }}
        .sidebar-minimal a:hover {{ color: {C_VIOLET}; }}

        .md-section-label {{
            display: flex; align-items: center; gap: 0.65rem;
            font-size: 0.7rem; font-weight: 800; letter-spacing: 0.12em;
            text-transform: uppercase; color: {C_ON_SURFACE};
            margin: 1.5rem 0 0.75rem;
        }}
        .md-section-label::after {{
            content: "";
            flex: 1; height: 2px;
            background: linear-gradient(90deg, rgba(37,99,235,0.35), transparent);
            border-radius: 2px;
        }}

        /* ── Streamlit widgets ── */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 20px !important;
            border: 1px solid {C_OUTLINE} !important;
            background: rgba(255,255,255,0.78) !important;
            backdrop-filter: blur(12px) !important;
            box-shadow: 0 6px 24px rgba(15,23,42,0.05) !important;
            transition: box-shadow 0.25s ease, transform 0.25s ease !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
            box-shadow: 0 12px 36px rgba(37,99,235,0.09) !important;
        }}

        .stButton > button {{
            font-weight: 700 !important;
            letter-spacing: 0.01em !important;
            transition: all 0.22s cubic-bezier(0.2,0,0,1) !important;
            border-radius: 14px !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(37,99,235,0.2) !important;
        }}
        .stButton > button:active {{ transform: scale(0.97) !important; }}
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, {C_PRIMARY} 0%, {C_VIOLET} 100%) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 14px !important;
            box-shadow: 0 4px 16px rgba(37,99,235,0.35) !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            box-shadow: 0 8px 28px rgba(124,58,237,0.4) !important;
        }}
        .stLinkButton > a {{
            border-radius: 14px !important;
            font-weight: 700 !important;
            transition: all 0.22s ease !important;
        }}
        .stLinkButton > a:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(15,23,42,0.1) !important;
        }}

        .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {{
            border-radius: 14px !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }}
        .stTextInput input:focus, .stTextArea textarea:focus {{
            border-color: {C_PRIMARY} !important;
            box-shadow: 0 0 0 3px rgba(37,99,235,0.15) !important;
        }}

        [data-testid="stChatMessage"] {{
            background: rgba(255,255,255,0.85) !important;
            backdrop-filter: blur(8px) !important;
            border-radius: 16px !important;
            border: 1px solid {C_OUTLINE} !important;
            animation: bentoIn 0.35s ease both;
            box-shadow: 0 2px 12px rgba(15,23,42,0.04) !important;
        }}
        [data-testid="stChatMessage"]:hover {{
            box-shadow: 0 6px 20px rgba(37,99,235,0.08) !important;
        }}

        details[data-testid="stExpander"] {{
            background: rgba(255,255,255,0.6) !important;
            border-radius: 16px !important;
            border: 1px solid {C_OUTLINE} !important;
        }}

        .stCaption, [data-testid="stCaptionContainer"] {{
            color: {C_ON_SURFACE_VARIANT} !important;
        }}

        /* ── Concept Explainer workspace ── */
        .ce-topbar {{
            display: flex; align-items: center; justify-content: space-between;
            gap: 1rem; flex-wrap: wrap;
            background: rgba(255,255,255,0.82);
            backdrop-filter: blur(16px);
            border: 1px solid {C_OUTLINE};
            border-radius: 20px;
            padding: 1rem 1.35rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 28px rgba(37,99,235,0.08);
        }}
        .ce-topbar h1 {{
            font-size: 1.35rem; font-weight: 800; margin: 0;
            letter-spacing: -0.02em; color: {C_ON_SURFACE};
        }}
        .ce-topbar p {{ margin: 0.15rem 0 0; font-size: 0.82rem; color: {C_ON_SURFACE_VARIANT}; }}
        .ce-model-badge {{
            display: inline-flex; align-items: center; gap: 0.4rem;
            background: linear-gradient(135deg, rgba(37,99,235,0.1), rgba(124,58,237,0.08));
            border: 1px solid rgba(37,99,235,0.15);
            border-radius: 999px; padding: 0.35rem 0.85rem;
            font-size: 0.72rem; font-weight: 700; color: #1D4ED8;
        }}
        .ce-model-dot {{
            width: 7px; height: 7px; border-radius: 50%;
            background: #22C55E; box-shadow: 0 0 0 3px rgba(34,197,94,0.25);
        }}
        .ce-panel-head {{
            font-size: 0.68rem; font-weight: 800; letter-spacing: 0.1em;
            text-transform: uppercase; color: {C_ON_SURFACE_VARIANT};
            margin: 0 0 0.65rem;
        }}
        .ce-empty {{
            text-align: center; padding: 1.5rem 1rem 0.5rem;
            color: {C_ON_SURFACE_VARIANT};
        }}
        .ce-empty .icon {{ font-size: 2rem; margin-bottom: 0.4rem; }}
        .ce-empty h3 {{ margin: 0 0 0.25rem; color: {C_ON_SURFACE}; font-size: 0.95rem; font-weight: 700; }}
        .ce-empty p {{ margin: 0; font-size: 0.82rem; line-height: 1.5; }}
        .ce-audience-hint {{
            font-size: 0.78rem; color: {C_ON_SURFACE_VARIANT};
            margin: -0.35rem 0 0.85rem; line-height: 1.45;
        }}
        .ce-audience-hint strong {{ color: {C_ON_SURFACE}; font-weight: 600; }}
        .ce-usage-strip {{
            display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem 0.85rem;
            background: rgba(255,255,255,0.75);
            border: 1px solid {C_OUTLINE};
            border-radius: 14px;
            padding: 0.55rem 0.9rem;
            margin: 0 0 0.85rem;
            font-size: 0.75rem;
        }}
        .ce-usage-label {{
            font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em;
            color: {C_ON_SURFACE_VARIANT};
        }}
        .ce-usage-val {{ font-weight: 800; color: {C_PRIMARY}; }}
        .ce-usage-detail {{ color: {C_ON_SURFACE_VARIANT}; }}
        .ce-usage-cost {{
            font-weight: 700; color: #059669;
            background: rgba(5,150,105,0.1); padding: 0.15rem 0.5rem; border-radius: 999px;
        }}
        .ce-usage-turns {{
            margin-left: auto; font-weight: 600; color: {C_ON_SURFACE_VARIANT};
        }}
        .ce-limits-caption {{
            font-size: 0.7rem; color: {C_ON_SURFACE_VARIANT}; margin: 0.35rem 0 0;
        }}
        .ce-past-panel {{
            background: rgba(255,255,255,0.78);
            border: 1px solid {C_OUTLINE};
            border-radius: 14px;
            padding: 0.65rem 0.9rem;
            margin: 0 0 0.85rem;
        }}
        .ce-past-label {{
            font-size: 0.68rem; font-weight: 800; letter-spacing: 0.08em;
            text-transform: uppercase; color: {C_ON_SURFACE_VARIANT};
        }}
        .ce-past-chips {{
            display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.45rem;
        }}
        .ce-past-chip {{
            font-size: 0.75rem; font-weight: 600; color: {C_ON_SURFACE};
            background: {C_SURFACE_CONTAINER};
            border: 1px solid {C_OUTLINE};
            border-radius: 999px; padding: 0.25rem 0.65rem;
        }}
        .ce-past-chip-active {{
            border-color: rgba(37,99,235,0.35);
            background: rgba(37,99,235,0.08); color: {C_PRIMARY};
        }}
        .ce-past-chip em {{
            font-style: normal; font-weight: 500; color: {C_ON_SURFACE_VARIANT};
            font-size: 0.68rem; margin-left: 0.25rem;
        }}
        .ce-past-note {{
            display: block; margin-top: 0.4rem;
            font-size: 0.68rem; color: {C_ON_SURFACE_VARIANT};
        }}

        div[data-testid="stVerticalBlockBorderWrapper"] .ce-panel-title {{
            margin-top: -0.25rem;
        }}
        [data-testid="stChatMessage"][data-testid="user"] {{
            background: linear-gradient(135deg, rgba(37,99,235,0.08), rgba(124,58,237,0.06)) !important;
        }}
        [data-testid="stChatMessageContent"] p {{
            line-height: 1.65 !important;
        }}
        .stCheckbox label span {{ font-size: 0.82rem !important; font-weight: 600 !important; }}
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
            <p class="shipped-apps-title">Live in this portfolio</p>
            {items}
        </div>
        """
    ).strip()


def render_sidebar_minimal() -> None:
    """One-line footer — use on every page sidebar."""
    _render_html(
        '<div class="sidebar-minimal">'
        '<a href="https://iamabyjain.com" target="_blank">iamabyjain.com</a>'
        " · Abhishek Jain"
        "</div>"
    )


def bento_metrics(items: list[tuple[str, str]]) -> None:
    cells = "".join(
        f'<div class="bento-metric bento-animate">'
        f'<div class="val">{html.escape(v)}</div><div class="lbl">{html.escape(l)}</div></div>'
        for v, l in items
    )
    _render_html(f'<div class="bento-metrics">{cells}</div>')


def intro_strip(text: str) -> None:
    """Styled intro paragraph; wrap phrases in ** for bold."""
    parts = text.split("**")
    chunks: list[str] = []
    for i, part in enumerate(parts):
        escaped = html.escape(part)
        chunks.append(f"<strong>{escaped}</strong>" if i % 2 == 1 else escaped)
    _render_html(f'<div class="intro-strip bento-animate">{"".join(chunks)}</div>')


def profile_hero(name: str, tagline: str, pills: list[str] | None = None) -> None:
    chips = ""
    if pills:
        chips = "".join(f'<span class="md-chip">{html.escape(p)}</span>' for p in pills)
        chips = f'<div style="display:flex;flex-wrap:wrap;margin-top:1rem">{chips}</div>'
    _render_html(
        f"""
        <div class="profile-hero bento-animate">
            <div class="hero-inner">
                <div class="avatar">👤</div>
                <h1>{html.escape(name)}</h1>
                <p class="tagline">{html.escape(tagline)}</p>
                {chips}
            </div>
        </div>
        """
    )


def hero(title: str, subtitle: str, pills: list[str] | None = None) -> None:
    chips = ""
    if pills:
        chips = "".join(f'<span class="md-chip">{html.escape(p)}</span>' for p in pills)
        chips = f'<div style="margin-top:0.85rem;display:flex;flex-wrap:wrap">{chips}</div>'
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
    accent = project.accent
    _render_html(
        f"""
        <div class="proj-card bento-animate" style="--proj-accent:{accent};--proj-accent-bg:{accent}18">
            <div class="proj-accent" style="background:{accent}"></div>
            <div class="proj-body">
                <div class="proj-head">
                    <div class="proj-icon-wrap" style="background:{accent}15">{project.icon}</div>
                    <p class="proj-title">{html.escape(project.name)}</p>
                    <span class="proj-status" style="background:{accent}18;color:{accent}">{html.escape(project.status)}</span>
                </div>
                <p class="proj-gist">{html.escape(project.gist)}</p>
                {shipped}
                <div class="proj-meta" style="margin-top:0.85rem">
                    <div class="proj-meta-row" style="border-color:{C_CYAN}">
                        <div class="proj-meta-label" style="color:#0891B2">Industry</div>
                        <p class="proj-meta-text">{html.escape(project.industry)}</p>
                    </div>
                    <div class="proj-meta-row" style="border-color:{C_AMBER}">
                        <div class="proj-meta-label" style="color:#D97706">Who benefits</div>
                        <p class="proj-meta-text">{html.escape(project.beneficiaries)}</p>
                    </div>
                </div>
            </div>
        </div>
        """
    )


def section_label(text: str) -> None:
    _render_html(f'<p class="md-section-label">{html.escape(text)}</p>')


def ce_topbar(provider: str, model: str) -> None:
    label = "OpenAI" if provider == "openai" else "Claude"
    _render_html(
        f"""
        <div class="ce-topbar bento-animate">
            <div>
                <h1>Concept Explainer</h1>
                <p>Multi-audience explanations · chat · export</p>
            </div>
            <span class="ce-model-badge">
                <span class="ce-model-dot"></span>
                {html.escape(label)} · {html.escape(model)}
            </span>
        </div>
        """
    )


def ce_empty_chat() -> None:
    _render_html(
        """
        <div class="ce-empty bento-animate">
            <div class="icon">💬</div>
            <h3>What would you like explained?</h3>
            <p>Type below or tap an example to start.</p>
        </div>
        """
    )


def ce_audience_hint(audiences: list[str]) -> None:
    labels = ", ".join(html.escape(a) for a in audiences)
    _render_html(
        f'<p class="ce-audience-hint">Explaining for: <strong>{labels}</strong> · change in sidebar</p>'
    )


def ce_usage_strip(
    input_tokens: int,
    output_tokens: int,
    cost_usd: float | None,
    *,
    turns: int,
    max_turns: int,
) -> None:
    total = input_tokens + output_tokens
    cost = f'<span class="ce-usage-cost">~${cost_usd:.4f}</span>' if cost_usd is not None else ""
    _render_html(
        f"""
        <div class="ce-usage-strip bento-animate">
            <span class="ce-usage-label">Session use</span>
            <span class="ce-usage-val">{total:,} tokens</span>
            <span class="ce-usage-detail">{input_tokens:,} in · {output_tokens:,} out</span>
            {cost}
            <span class="ce-usage-turns">{turns}/{max_turns} turns</span>
        </div>
        """
    )


def ce_limits_caption(max_terms: int, max_chars: int, max_context: int) -> None:
    _render_html(
        f'<p class="ce-limits-caption">Limits: {max_terms} terms · {max_chars} chars · '
        f"last {max_context} follow-ups in context</p>"
    )


def ce_past_chats_panel(chats: list[dict], active_id: str | None) -> None:
    """Visible past-chat list on the main canvas (browser session only)."""
    if not chats:
        return
    rows = []
    for item in chats[:8]:
        title = html.escape(str(item.get("title", "Chat")))
        updated = html.escape(str(item.get("updated_at", ""))[:16].replace("T", " "))
        active = item.get("id") == active_id
        dot = "● " if active else ""
        rows.append(
            f'<span class="ce-past-chip{" ce-past-chip-active" if active else ""}">'
            f"{dot}{title} <em>{updated}</em></span>"
        )
    _render_html(
        f"""
        <div class="ce-past-panel bento-animate">
            <span class="ce-past-label">Past chats ({len(chats)})</span>
            <div class="ce-past-chips">{"".join(rows)}</div>
            <span class="ce-past-note">Open or download any chat from the sidebar → Past chats</span>
        </div>
        """
    )


def inject_ce_chat_layout() -> None:
    """Fluid, responsive chat workspace — scales from mobile to ultrawide."""
    st.markdown(
        f"""
        <style>
        /* ── Fluid page shell ── */
        .main .block-container {{
            max-width: min(1320px, 94vw) !important;
            padding-top: 1rem !important;
            padding-bottom: 7rem !important;
            padding-left: clamp(0.75rem, 2.5vw, 2rem) !important;
            padding-right: clamp(0.75rem, 2.5vw, 2rem) !important;
        }}

        .main .block-container .ce-chat-workspace-marker {{
            display: none;
        }}

        /* ── Chat messages: full usable width (Concept Explainer page) ── */
        .main .block-container [data-testid="stChatMessage"] {{
            width: 100% !important;
            max-width: 100% !important;
            margin-bottom: 0.85rem !important;
            padding: clamp(0.85rem, 1.5vw, 1.15rem) clamp(1rem, 2vw, 1.35rem) !important;
        }}

        /* ── Topbar scales ── */
        .ce-topbar {{
            padding: clamp(0.85rem, 2vw, 1.25rem) clamp(1rem, 2.5vw, 1.75rem) !important;
        }}
        .ce-topbar h1 {{ font-size: clamp(1.15rem, 2.2vw, 1.45rem) !important; }}

        /* ── Example chips ── */
        .main .block-container [data-testid="column"] {{
            min-width: 0 !important;
        }}

        /* User turns — compact bubble on wide screens */
        @media (min-width: 768px) {{
            .main .block-container [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {{
                max-width: min(520px, 72%) !important;
                margin-left: auto !important;
                margin-right: 0 !important;
            }}
        }}

        /* Assistant turns — full prose column */
        .main .block-container [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {{
            max-width: 100% !important;
        }}

        /* ── Readable long-form markdown in answers ── */
        .main .block-container [data-testid="stMarkdownContainer"] {{
            max-width: none !important;
        }}
        .main .block-container [data-testid="stMarkdownContainer"] h1,
        .main .block-container [data-testid="stMarkdownContainer"] h2 {{
            font-size: clamp(1.05rem, 1.8vw, 1.3rem) !important;
            font-weight: 700 !important;
            margin: 1.1rem 0 0.45rem !important;
            color: {C_ON_SURFACE} !important;
            letter-spacing: -0.01em;
        }}
        .main .block-container [data-testid="stMarkdownContainer"] h3 {{
            font-size: clamp(0.95rem, 1.4vw, 1.1rem) !important;
            font-weight: 700 !important;
            margin: 0.85rem 0 0.35rem !important;
        }}
        .main .block-container [data-testid="stMarkdownContainer"] p,
        .main .block-container [data-testid="stMarkdownContainer"] li {{
            font-size: clamp(0.875rem, 1.05vw, 0.95rem) !important;
            line-height: 1.7 !important;
            color: {C_ON_SURFACE_VARIANT} !important;
        }}
        .main .block-container [data-testid="stMarkdownContainer"] ul,
        .main .block-container [data-testid="stMarkdownContainer"] ol {{
            padding-left: 1.25rem !important;
            margin: 0.35rem 0 0.65rem !important;
        }}
        .main .block-container [data-testid="stMarkdownContainer"] strong {{
            color: {C_ON_SURFACE} !important;
        }}

        /* ── Pinned chat input matches content width ── */
        [data-testid="stBottomBlock"] {{
            max-width: min(1320px, 94vw) !important;
            margin: 0 auto !important;
            padding-left: clamp(0.75rem, 2.5vw, 2rem) !important;
            padding-right: clamp(0.75rem, 2.5vw, 2rem) !important;
        }}
        [data-testid="stChatInput"] {{
            border-radius: 16px !important;
        }}
        [data-testid="stChatInput"] textarea {{
            font-size: clamp(0.875rem, 1vw, 0.95rem) !important;
            min-height: 52px !important;
        }}

        /* ── Ultrawide: optional two-tone reading column ── */
        @media (min-width: 1400px) {{
            .main .block-container {{
                max-width: min(1480px, 88vw) !important;
            }}
            .main .block-container [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {{
                padding-left: clamp(1rem, 2vw, 1.5rem) !important;
                padding-right: clamp(1rem, 3vw, 2.5rem) !important;
            }}
        }}

        @media (max-width: 640px) {{
            .ce-topbar {{
                flex-direction: column;
                align-items: flex-start !important;
            }}
            .ce-audience-hint {{ font-size: 0.72rem !important; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

