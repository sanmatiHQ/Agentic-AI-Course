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
    repo_hint: str = ""


# ── Course portfolio (this Streamlit repo) ─────────────────────────────────────
COURSE_PORTFOLIO = Project(
    name="Agentic AI Course Portfolio",
    status="Active · Streamlit",
    accent="#1A73E8",
    icon="🎓",
    gist=(
        "IITM Pravartak × FutureSense — AI Agent Workflows & Agentic Systems. "
        "Each module ships as a live Streamlit app in this repo. "
        "Course orientation notes merged from the legacy FutureSense repo live in docs/."
    ),
    industry="EdTech · AI upskilling · enterprise L&D",
    beneficiaries=(
        "Working professionals building agentic AI skills, instructors needing demonstrable "
        "assignments, and hiring managers evaluating portfolio-ready capstone work."
    ),
    shipped_apps=(
        ShippedApp(
            name="Concept Explainer",
            gist="Assignment 1 — BYOK tutor for SMEs, experts & engineers with chat + export.",
            page_path="pages/2_🧠_Concept_Explainer.py",
        ),
    ),
    repo_hint="sanmatiHQ/Agentic-AI-Course",
)

# ── Independent ventures (outside this repo) ───────────────────────────────────
INDEPENDENT_PROJECTS: list[Project] = [
    Project(
        name="GeM Bid System",
        status="In production",
        accent="#34A853",
        icon="🏛️",
        gist=(
            "Multi-agent intelligence mesh for India's Government e-Marketplace — harvests bids, "
            "extracts PDFs, enriches with LLMs, links contracts & MKP data, powers tenant dashboards."
        ),
        industry="GovTech · B2B procurement · MSME commerce",
        beneficiaries=(
            "Bid managers chasing GeM tenders, MSMEs competing for government contracts, "
            "procurement consultants, and analysts tracking ministry spend."
        ),
        repo_hint="sanmatiHQ/GeM_Bid_System (private monorepo)",
    ),
    Project(
        name="Bharat Quant",
        status="In development",
        accent="#FBBC04",
        icon="📈",
        gist=(
            "Quantitative research engine for Indian markets — systematic signals, backtesting, "
            "and execution workflows tuned for NSE/BSE microstructure and regulatory context."
        ),
        industry="FinTech · capital markets · quantitative finance",
        beneficiaries=(
            "Prop traders, portfolio managers, research analysts, and fintech teams building "
            "systematic strategies for Bharat markets."
        ),
    ),
    Project(
        name="Clerk",
        status="Early build",
        accent="#EA4335",
        icon="📬",
        gist=(
            "Local-first personal ops assistant — mail, meetings, files, and OEM price tracking "
            "on your machine; sensitive data never leaves your hardware."
        ),
        industry="Productivity · SMB operations · personal knowledge work",
        beneficiaries=(
            "Founders buried in admin, sales teams tracking OEM pricing, operators who need "
            "a private assistant without cloud exposure."
        ),
        repo_hint="sanmatiHQ/clerk",
    ),
    Project(
        name="IntelliMatrix",
        status="In design",
        accent="#9334E6",
        icon="🔮",
        gist=(
            "Intelligence layer fusing structured data, embeddings, and decision rules into "
            "actionable matrices — noisy business signals → strategy-ready views."
        ),
        industry="Enterprise analytics · strategy consulting · ops intelligence",
        beneficiaries=(
            "Strategy teams, COOs, and data leaders who need cross-silo insight without a "
            "full data-warehouse programme."
        ),
    ),
]

ALL_PROJECTS: list[Project] = [COURSE_PORTFOLIO, *INDEPENDENT_PROJECTS]
