#!/usr/bin/env python3
"""Content for the profile README artwork.

Everything the generated SVGs say lives here so the builders stay layout-only.
`slug` values become filenames and are referenced from README.md, so changing
one means updating the README link that points at it.
"""

from __future__ import annotations

SECTIONS = [
    ("01", "PROFILE", "Who I am and what I build"),
    ("02", "ACTIVITY", "Contributions across the past four months"),
    ("03", "STACK", "Tools I reach for"),
    ("04", "WORK", "Project showcases and live builds"),
]

NAV = [
    ("website", "Website", "davishiggins.com", "https://davishiggins.com"),
    ("studio", "Studio", "higginsd.com", "https://higginsd.com"),
    ("linkedin", "LinkedIn", "in/davishiggins", "https://www.linkedin.com/in/davishiggins/"),
    ("email", "Email", "davishiggins@icloud.com", "mailto:davishiggins@icloud.com"),
    ("portfolio", "Portfolio", "portfolio.davishiggins.com", "https://portfolio.davishiggins.com"),
]

PROFILE_PARAGRAPHS = [
    "I'm Davis Higgins — a data analyst, AI builder, and web developer who turns "
    "complex ideas into useful digital products.",
    "I work across data, technology, and design to uncover insights, build "
    "intelligent tools, and create polished digital experiences that are both "
    "functional and memorable. My work spans analytics dashboards, agentic AI "
    "systems, full-stack applications, and brand-forward web experiences.",
    "Data Science and Artificial Intelligence student at UNC Charlotte, Data "
    "Analyst at Kewaunee Scientific, and founder of Higgins Digital. Actively "
    "seeking internship and project opportunities in data science, analytics, "
    "AI, and business intelligence.",
]

PROFILE_FACTS = [
    ("BASED IN", "Charlotte, NC", "UNC Charlotte '27"),
    ("STUDYING", "Data Science", "Artificial Intelligence"),
    ("ANALYST", "Kewaunee Scientific", "Power BI · Zoho"),
    ("FOUNDER", "Higgins Digital", "Web + brand systems"),
]

STATISTICS = [
    ("3.89", "GPA", "Data Science · AI"),
    ("5×", "CHANCELLOR'S LIST", "Consecutive semesters"),
    ("10", "ACTIVE PROJECTS", "Web · AI · analytics"),
    ("20+", "DASHBOARDS BUILT", "Power BI · Zoho"),
    ("15+", "WEBSITES LAUNCHED", "Personal + client"),
    ("2027", "GRADUATION", "UNC Charlotte"),
]

# (slug, index, name, kind, description, stack, status, url)
PROJECTS = [
    ("cade", "01", "Cade", "AGENTIC SYSTEM",
     "Claude-powered personal operating system with persistent, structured memory.",
     "Claude Code · Next.js · GSAP", "LIVE", "https://cade.davishiggins.com"),
    ("propify", "02", "Propify", "SPORTS ANALYTICS",
     "Projection platform with EV analysis and bankroll sizing.",
     "Python · FastAPI · Next.js · ML", "LIVE", "https://propifyai.davishiggins.com/"),
    ("prospectiq", "03", "ProspectIQ", "OPEN SOURCE CLI",
     "Collects, enriches, scores, and exports public lead data across eight sources.",
     "Python · HTTPX · GitHub Actions", "OPEN SOURCE",
     "https://github.com/DavisHiggins/ProspectIQ"),
    ("lattice", "04", "Lattice", "AGENTIC RUNTIME",
     "Controlled agentic operating system and execution layer.",
     "Next.js · Supabase · Agent SDK", "IN DEVELOPMENT",
     "https://github.com/DavisHiggins"),
    ("higgins-digital", "05", "Higgins Digital", "WEB STUDIO",
     "High-performance website and digital branding studio.",
     "Next.js · Framer Motion · Vercel", "LIVE", "https://higginsd.com/"),
    ("crowncodeai", "06", "CrownCodeAI", "AI TOOL",
     "AI-powered website generation tool with guided prompts.",
     "Claude API · Next.js · Tailwind", "BUILDING", "https://crowncode.higginsd.com/"),
    ("curated-notes", "07", "Curated Notes", "WRITING",
     "Editorial writing platform and personal knowledge base.",
     "Next.js · MDX · Vercel", "LIVE", "https://notes.davishiggins.com/"),
    ("ai-workflow-os", "08", "AI Workflow OS", "AI EDUCATION",
     "Curated AI courses and guides for people new to AI.",
     "AI workflows · Claude Code", "BUILDING", "https://ai.davishiggins.com/"),
    ("lakeside-sport-club", "09", "Lakeside Sport Club", "COMMERCE",
     "Premium athletic apparel brand with a custom storefront.",
     "Next.js · Tailwind · Stripe", "LIVE", "https://lakesidesportclub.com"),
    ("portfolio", "10", "Portfolio", "PERSONAL PLATFORM",
     "Personal platform and project hub.",
     "React · Vite · Framer Motion", "LIVE", "https://portfolio.davishiggins.com/"),
    ("davishiggins-v2", "11", "davishiggins.com V2", "PERSONAL PLATFORM",
     "Full rebuild of the personal site and portfolio.",
     "Astro · TypeScript · GSAP · SCSS", "BUILDING", "https://v2.davishiggins.com"),
    ("chaplain-platform", "12", "Chaplain Platform", "COMMUNITY TOOL",
     "Chapter leadership and spiritual growth platform for Phi Delta Theta.",
     "React · Vite · Content system", "LIVE", "https://chaplain.davishiggins.com"),
    ("photos-and-frames", "13", "Photos & Frames", "PHOTOGRAPHY",
     "Photography and gallery archive.",
     "Photography · Gallery · Archive", "LIVE", "https://photos.davishiggins.com"),
]

STACK = [
    ("DATA & ANALYTICS",
     ["Python", "SQL", "R", "Power BI", "Tableau", "Excel", "Pandas", "scikit-learn"]),
    ("AI & AUTOMATION",
     ["Claude Code", "Claude API", "Agent SDK", "Prompt systems", "RAG", "Workflow automation"]),
    ("FRONTEND",
     ["Next.js", "React", "TypeScript", "Astro", "Tailwind CSS", "GSAP", "Framer Motion"]),
    ("BACKEND & PLATFORMS",
     ["FastAPI", "Supabase", "Vercel", "PostgreSQL", "GitHub Actions", "Stripe"]),
    ("DESIGN & STRATEGY",
     ["Branding", "Editorial design", "SEO", "Web analytics", "Systems thinking"]),
]


# Project showcases: documentation-only repositories, one per project, each
# linking to its live experience. Order is the profile order; the first six
# are the recommended pins.
# (slug, index, name, focus, summary, stack, status, showcase_repo, live_url, live_label)
SHOWCASES = [
    ("contender", "01", "Contender", "SPORTS ANALYTICS",
     "NBA player-prop analysis that shows its work and keeps its evidence.",
     "Next.js · FastAPI · Supabase", "LIVE", "contender-showcase",
     "https://contender.davishiggins.com", "contender.davishiggins.com"),
    ("flowcast", "02", "Flowcast", "DEMAND FORECASTING",
     "Hourly taxi-demand forecasts for all 262 NYC zones, checked against a baseline.",
     "XGBoost · SageMaker · Next.js", "LIVE", "flowcast-showcase",
     "https://flowcastweb.vercel.app", "flowcastweb.vercel.app"),
    ("cade", "03", "Cade", "PERSISTENT AI SYSTEM",
     "Claude-powered working partner with structured memory and reusable Jobs.",
     "Claude Code · Obsidian · Next.js", "LIVE", "cade-showcase",
     "https://cade.davishiggins.com", "cade.davishiggins.com"),
    ("secondchance", "04", "SecondChance", "PREDICTIVE ANALYTICS",
     "Team research prototype turning shelter long-stay risk into earlier support.",
     "LightGBM · Next.js · Python", "PROTOTYPE", "secondchance-showcase",
     "https://secondc.vercel.app", "secondc.vercel.app"),
    ("dhlm", "05", "DHLM", "PRIVATE AI WORKSPACE",
     "Private Gemini workspace over mail, calendar, and files; public case study.",
     "Next.js · Gemini · Google APIs", "CASE STUDY", "dhlm-showcase",
     "https://dhlm.davishiggins.com", "dhlm.davishiggins.com"),
    ("lakeside-sport-club", "06", "Lakeside Sport Club", "CUSTOM COMMERCE",
     "Branded athletic-lifestyle storefront with Stripe checkout and order tools.",
     "Next.js · Stripe · Postgres", "LIVE", "lakeside-sport-club-showcase",
     "https://lakesidesportclub.com", "lakesidesportclub.com"),
    ("higgins-digital", "07", "Higgins Digital", "SOFTWARE DEVELOPMENT",
     "The site for my software development company: work, services, contact.",
     "Next.js · GSAP · Supabase", "LIVE", "higgins-digital-showcase",
     "https://www.higginsd.com", "higginsd.com"),
    ("higgins-building-group", "08", "Higgins Building Group", "CLIENT WEBSITE",
     "Full rebuild for a custom home builder, led by its own photography.",
     "Next.js · Framer Motion · Resend", "LIVE", "higgins-building-group-showcase",
     "https://www.higginsbuildinggroup.com", "higginsbuildinggroup.com"),
    ("davishiggins-com", "09", "davishiggins.com", "PERSONAL PORTFOLIO",
     "My motion-led editorial portfolio, extended from an open-source base.",
     "Astro · GSAP · Lenis", "LIVE", "davis-higgins-portfolio-showcase",
     "https://davishiggins.com", "davishiggins.com"),
    ("ynot", "10", "Y NOT?", "APPAREL BRAND",
     "Commerce-first streetwear storefront; pre-launch, test-mode checkout.",
     "Next.js · Stripe · Supabase", "PRE-LAUNCH", "ynot-showcase",
     "https://www.ynot.lifestyle", "ynot.lifestyle"),
    ("crowncode-ai", "11", "CrownCode AI", "AI WEB GENERATION",
     "Structured brand intake to a deployable website draft, then guided revision.",
     "Next.js · Claude API", "MVP", "crowncode-ai-showcase",
     "https://crowncode.higginsd.com", "crowncode.higginsd.com"),
    ("chaplain-platform", "12", "Chaplain Platform", "CHAPTER PLATFORM",
     "Weekly Bible study and semester plan for Phi Delta Theta NC Epsilon.",
     "React · Vite · Tailwind", "LIVE", "phi-delta-theta-chaplain-showcase",
     "https://chaplain.davishiggins.com", "chaplain.davishiggins.com"),
    ("curated-notes", "13", "Curated Notes", "KNOWLEDGE PUBLISHING",
     "A public notebook on data science, AI, building, and faith.",
     "Next.js · MDX · Tailwind", "LIVE", "curated-notes-showcase",
     "https://notes.davishiggins.com", "notes.davishiggins.com"),
    ("touch-up-solutions", "14", "Touch Up Solutions", "CATALOG REDESIGN",
     "Repair-product catalog redesign organized by the material being fixed.",
     "HTML · CSS · JavaScript", "CONCEPT", "touch-up-solutions-showcase",
     "https://touchupsolutions.vercel.app", "touchupsolutions.vercel.app"),
    ("photos-and-frames", "15", "photos & frames", "PHOTOGRAPHY",
     "My photography, black and white until you reach for it.",
     "React · Vite · GSAP", "LIVE", "photos-and-frames-showcase",
     "https://photos.davishiggins.com", "photos.davishiggins.com"),
    ("wy-not-pics", "16", "wy_not_pics", "CLIENT PHOTOGRAPHY",
     "Portfolio site for Charlotte photographer Wyatt Bullock.",
     "React · Vite · Framer Motion", "LIVE", "wy-not-pics-showcase",
     "https://wynotpics.vercel.app", "wynotpics.vercel.app"),
    ("dh-portfolio", "17", "DH Portfolio", "CONVERSATIONAL PORTFOLIO",
     "A portfolio you can ask questions, with every section a click away.",
     "React · Vite · Claude API", "LIVE", "dh-conversational-portfolio-showcase",
     "https://portfolio.davishiggins.com", "portfolio.davishiggins.com"),
]
