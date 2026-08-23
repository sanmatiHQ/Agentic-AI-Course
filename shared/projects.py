"""Portfolio project definitions — single source of truth."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ShippedApp:
    """An app shipped inside the Agentic AI Course portfolio."""

    name: str
    gist: str
    page_path: str | None = None


@dataclass(frozen=True)
class Project:
    name: str
    status: str
    accent: str
    icon: str
    gist: str
    industry: str
    beneficiaries: str
    shipped_apps: tuple[ShippedApp, ...] = ()


# ── Course portfolio (this Streamlit repo — public) ───────────────────────────
COURSE_PORTFOLIO = Project(
    name="Agentic AI Course Portfolio",
    status="Live · Streamlit Cloud",
    accent="#1A73E8",
    icon="🎓",
    gist=(
        "IITM Pravartak × FutureSense — AI Agent Workflows & Agentic Systems. "
        "Each course module ships as a live Streamlit app here; assignments stay "
        "deployable and portfolio-ready from day one."
    ),
    industry="EdTech · AI upskilling · enterprise L&D",
    beneficiaries=(
        "Working professionals building agentic AI skills, instructors evaluating "
        "demonstrable capstone work, and hiring managers reviewing live portfolio apps."
    ),
    shipped_apps=(
        ShippedApp(
            name="Concept Explainer",
            gist="Assignment 1 — BYOK tutor for SMEs, experts & engineers with chat + export.",
            page_path="pages/2_🧠_Concept_Explainer.py",
        ),
    ),
)

# ── Independent ventures (private codebases — no repo links in UI) ─────────────
INDEPENDENT_PROJECTS: list[Project] = [
    Project(
        name="GeM Bid System",
        status="In production · Private",
        accent="#34A853",
        icon="🏛️",
        gist=(
            "Multi-agent procurement intelligence for India's Government e-Marketplace — "
            "harvests bids, contracts, and marketplace catalogue; extracts structured truth "
            "from bid PDFs; delivers Cortex briefs, price benchmarks, and spec matching; "
            "live tenant dashboard at gem.sanmatitraders.com."
        ),
        industry="GovTech · B2B procurement · MSME commerce",
        beneficiaries=(
            "MSME bid managers chasing GeM tenders, procurement consultants, and analysts "
            "tracking ministry spend and contract outcomes."
        ),
    ),
    Project(
        name="Bharat Quant",
        status="Research · paper-first · Private",
        accent="#FBBC04",
        icon="📈",
        gist=(
            "Autonomous NSE trading research stack — Zerodha Kite Connect, 52+ event-driven "
            "strategies, Sortino/Calmar promotion gates, PPO reinforcement learning with "
            "shadow backtest, and a FastAPI ops dashboard."
        ),
        industry="FinTech · quantitative finance · capital markets",
        beneficiaries=(
            "Prop traders and quants building systematic, risk-gated strategies for Indian "
            "equities — paper trading validated before any live capital."
        ),
    ),
    Project(
        name="Clerk",
        status="Early build · local-first · Private",
        accent="#EA4335",
        icon="📬",
        gist=(
            "Personal ops console — local-first Gmail and Drive workflows for bids, "
            "trainings, meetings, document filing, and OEM price tracking. Sensitive "
            "mail and files stay on your machine, not in the cloud."
        ),
        industry="Productivity · SMB operations · personal knowledge work",
        beneficiaries=(
            "Founders buried in admin, sales teams tracking OEM pricing, and operators who "
            "need a private assistant without cloud data exposure."
        ),
    ),
    Project(
        name="IntelliMatrix",
        status="In development · Private",
        accent="#9334E6",
        icon="🔮",
        gist=(
            "Self-hosted OSINT intelligence platform — cases, entity graph, geospatial views, "
            "and reports, with an integrated Camera Vision module (CCTV analytics, LPR, face "
            "gallery) that runs entirely on-prem."
        ),
        industry="OSINT · security operations · on-prem analytics",
        beneficiaries=(
            "Investigators, security teams, and analysts who need cross-source intelligence "
            "and video analytics without sending biometrics to the cloud."
        ),
    ),
    Project(
        name="Race Management",
        status="In development · Private",
        accent="#E37400",
        icon="🏃",
        gist=(
            "End-to-end race operations — bib assignment, participant registry, and "
            "event-day management for running and cycling events."
        ),
        industry="Sports tech · event operations",
        beneficiaries=(
            "Race organizers, timing crews, and event volunteers managing participant "
            "logistics on race day."
        ),
    ),
    Project(
        name="Daily Reporting System",
        status="In development · Private",
        accent="#5F6368",
        icon="📋",
        gist=(
            "Structured daily reporting workflow — capture field updates, review submissions, "
            "and roll up operational status for team visibility."
        ),
        industry="Enterprise ops · reporting · team coordination",
        beneficiaries=(
            "Managers and field teams who need consistent, auditable daily status capture "
            "across distributed operations."
        ),
    ),
]

ALL_PROJECTS: list[Project] = [COURSE_PORTFOLIO, *INDEPENDENT_PROJECTS]
