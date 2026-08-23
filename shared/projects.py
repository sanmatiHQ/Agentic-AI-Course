"""Portfolio project definitions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Project:
    name: str
    status: str
    accent: str
    icon: str
    gist: str
    industry: str
    beneficiaries: str
    in_sidebar: bool = True


PROJECTS: list[Project] = [
    Project(
        name="Agentic AI Course Portfolio",
        status="Active",
        accent="#4285F4",
        icon="🎓",
        gist=(
            "A living Streamlit portfolio for IITM Pravartak / FutureSense — each course module "
            "ships as a deployable app. Concept Explainer is the first assignment live in this repo."
        ),
        industry="EdTech · AI upskilling · enterprise L&D",
        beneficiaries=(
            "Working professionals learning agentic AI, course instructors who want demonstrable "
            "assignments, and hiring managers reviewing portfolio-ready work."
        ),
    ),
    Project(
        name="Concept Explainer",
        status="Live app",
        accent="#A142F4",
        icon="🧠",
        gist=(
            "BYOK multi-audience AI tutor — paste OpenAI or Claude keys, pick a model with pricing, "
            "explain any concept with analogies, business impact, and technical depth, then chat and export."
        ),
        industry="EdTech · internal enablement · sales engineering",
        beneficiaries=(
            "SMEs and business leaders who need plain-language clarity, domain experts validating "
            "decisions, and engineers who want depth without jargon overload."
        ),
    ),
    Project(
        name="GeM Bid System",
        status="In production",
        accent="#34A853",
        icon="🏛️",
        gist=(
            "Multi-agent intelligence mesh for India's Government e-Marketplace — harvests bids, "
            "extracts PDFs, enriches with LLMs, links contracts & marketplace data, serves tenant dashboards."
        ),
        industry="GovTech · B2B procurement · MSME commerce",
        beneficiaries=(
            "Bid managers and sales teams chasing GeM tenders, procurement consultants, MSMEs "
            "competing for government contracts, and analysts tracking ministry spend patterns."
        ),
    ),
    Project(
        name="Bharat Quant",
        status="In development",
        accent="#FBBC04",
        icon="📈",
        gist=(
            "Quantitative research engine tuned for Indian markets — systematic signals, backtesting, "
            "and execution workflows designed for NSE/BSE structure, liquidity, and regulatory realities."
        ),
        industry="FinTech · capital markets · quantitative finance",
        beneficiaries=(
            "Retail and prop traders, portfolio managers, research analysts, and fintech teams "
            "building systematic strategies for Bharat-specific market microstructure."
        ),
    ),
    Project(
        name="Clerk",
        status="Early build",
        accent="#EA4335",
        icon="📬",
        gist=(
            "Local-first personal ops bot on your machine — triages mail, meetings, files, and OEM "
            "price sheets without sending sensitive data to the cloud."
        ),
        industry="Productivity · SMB operations · personal knowledge work",
        beneficiaries=(
            "Founders and operators drowning in admin, sales teams tracking OEM pricing, and "
            "anyone who wants an private assistant on their own hardware."
        ),
    ),
    Project(
        name="IntelliMatrix",
        status="In design",
        accent="#00BCD4",
        icon="🔮",
        gist=(
            "Intelligence layer that fuses structured business data, embeddings, and decision rules "
            "into actionable matrices — turning noisy signals into strategy-ready views."
        ),
        industry="Enterprise analytics · strategy consulting · ops intelligence",
        beneficiaries=(
            "Strategy teams, COOs, and data leaders who need connected insight across siloed "
            "sources without standing up a full data warehouse project."
        ),
    ),
]

SIDEBAR_APPS = [p for p in PROJECTS if p.in_sidebar and p.name != "Agentic AI Course Portfolio"]
