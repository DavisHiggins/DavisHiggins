#!/usr/bin/env python3
"""Generate the branded SVG system used by Davis Higgins's GitHub profile.

Design rules for this system:

* Calm by default. No traveling dash strokes, no marquees, no looping ambient
  motion. Motion is limited to a single one-shot entrance fade and one status
  dot, so the page reads as composed rather than busy.
* Boxes hold structure and numbers. Prose lives in README.md as real markdown,
  outside the artwork, where it is selectable, searchable, and accessible.
* Section headers are markdown, not artwork, so they sit on GitHub's own
  background instead of inside a panel.

Output is dependency-free and GitHub-safe. Run from the repository root:

    python scripts/generate_profile_assets.py
"""

from __future__ import annotations

import base64
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PROJECT_CARDS = ASSETS / "project-cards"
LOGO = ASSETS / "dh-logo.png"

BG = "#03070B"
PANEL = "#080F18"
BLUE = "#7BAFD4"
BLUE_LIGHT = "#C8E7FA"
WHITE = "#F7FBFF"
MUTED = "#8395A6"
LINE = "#162836"


# Deliberately small. `rise` is a one-shot entrance; `pulse` is used exactly
# once in the whole system (the hero status dot). Nothing else moves.
COMMON_CSS = f"""
    .display {{
      font-family: "Arial Black", "Helvetica Neue", Inter, Arial, sans-serif;
      font-weight: 900;
    }}
    .sans {{ font-family: "Helvetica Neue", Inter, Arial, sans-serif; }}
    .mono {{ font-family: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace; }}
    .rise {{
      opacity: 0;
      animation: rise .7s cubic-bezier(.2,.7,.2,1) forwards;
    }}
    @keyframes rise {{
      from {{ opacity: 0; transform: translateY(8px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}
    .pulse {{ animation: pulse 3.6s ease-in-out infinite; }}
    @keyframes pulse {{ 0%,100% {{ opacity: .5; }} 50% {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .rise, .pulse {{ animation: none !important; opacity: 1 !important; }}
    }}
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def defs(extra: str = "") -> str:
    return f"""
  <defs>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{BLUE}" stop-opacity=".85"/>
      <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="panelFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0D1B2A"/>
      <stop offset="1" stop-color="{PANEL}"/>
    </linearGradient>
    <radialGradient id="blueGlow">
      <stop offset="0" stop-color="{BLUE}" stop-opacity=".20"/>
      <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
    </radialGradient>
    {extra}
  </defs>
"""


def logo_data_uri() -> str:
    """Inline the DH mark so it survives GitHub's image proxy."""
    return "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode("ascii")


def nav_badge(label: str, filename: str) -> None:
    svg = f"""
<svg viewBox="0 0 220 56" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="{escape(label)}">
  {defs()}
  <style>
    {COMMON_CSS}
    .label, .arrow {{ transition: transform .28s ease, fill .28s ease; }}
    svg:hover .label {{ transform: translateX(4px); fill: {BLUE_LIGHT}; }}
    svg:hover .arrow {{ transform: translateX(4px); }}
  </style>
  <rect x="1" y="1" width="218" height="54" rx="14" fill="{PANEL}"
        stroke="{LINE}" stroke-width="1.5"/>
  <text x="30" y="34" class="sans label" fill="{WHITE}" font-size="15"
        font-weight="750" letter-spacing=".4">{escape(label)}</text>
  <text x="192" y="34" class="sans arrow" fill="{BLUE}" font-size="15">&#8599;</text>
</svg>
"""
    write(ASSETS / filename, svg)


def build_hero() -> None:
    svg = f"""
<svg viewBox="0 0 1200 400" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Davis Higgins — data analyst, AI builder, web developer, and founder">
  {defs()}
  <style>{COMMON_CSS}</style>

  <rect width="1200" height="400" rx="28" fill="{BG}"/>
  <ellipse cx="980" cy="110" rx="360" ry="250" fill="url(#blueGlow)"/>
  <rect x="1" y="1" width="1198" height="398" rx="27" fill="url(#panelFill)"
        fill-opacity=".55" stroke="{LINE}" stroke-width="1.5"/>
  <rect x="64" y="0" width="420" height="2" fill="url(#edge)"/>

  <g class="rise" style="animation-delay:.05s">
    <text x="64" y="86" class="mono" fill="{BLUE}" font-size="13" font-weight="700"
          letter-spacing="3.6">CHARLOTTE, NORTH CAROLINA</text>
  </g>

  <g class="rise" style="animation-delay:.14s">
    <text x="60" y="192" class="display" fill="{WHITE}" font-size="88"
          letter-spacing="-5">DAVIS HIGGINS</text>
    <text x="64" y="240" class="sans" fill="{BLUE_LIGHT}" font-size="24" font-weight="700">
      Data analyst, AI builder, and web developer.
    </text>
  </g>

  <g class="rise" style="animation-delay:.26s">
    <line x1="64" y1="284" x2="700" y2="284" stroke="{LINE}" stroke-width="1.5"/>
    <text x="64" y="322" class="mono" fill="{MUTED}" font-size="13" letter-spacing="2">
      DATA SCIENCE &#183; ARTIFICIAL INTELLIGENCE &#183; WEB SYSTEMS
    </text>
    <circle cx="70" cy="352" r="5" fill="{BLUE}" class="pulse"/>
    <text x="88" y="357" class="mono" fill="{BLUE_LIGHT}" font-size="13" letter-spacing="1.6">
      AVAILABLE FOR OPPORTUNITIES
    </text>
  </g>

  <g class="rise" style="animation-delay:.20s">
    <image href="{logo_data_uri()}" x="892" y="96" width="228" height="228"
           preserveAspectRatio="xMidYMid meet"/>
  </g>
</svg>
"""
    write(ASSETS / "hero.svg", svg)


def build_about() -> None:
    """A slim fact strip. The narrative prose lives in README.md."""
    facts = [
        ("LOCATION", "Charlotte, NC"),
        ("STUDYING", "Data Science + AI"),
        ("ANALYST", "Kewaunee Scientific"),
        ("FOUNDER", "Higgins Digital"),
    ]
    cells = ""
    for i, (label, value) in enumerate(facts):
        x = 24 + i * 292
        cells += f"""
  <g class="rise" style="animation-delay:{.08 + i * .07:.2f}s">
    <rect x="{x}" y="24" width="272" height="118" rx="18" fill="{PANEL}"
          stroke="{LINE}" stroke-width="1.5"/>
    <rect x="{x + 24}" y="24" width="52" height="2" fill="url(#edge)"/>
    <text x="{x + 24}" y="68" class="mono" fill="{BLUE}" font-size="11"
          font-weight="700" letter-spacing="2.4">{escape(label)}</text>
    <text x="{x + 24}" y="106" class="sans" fill="{WHITE}" font-size="19"
          font-weight="750">{escape(value)}</text>
  </g>
"""
    svg = f"""
<svg viewBox="0 0 1200 166" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Davis Higgins at a glance: Charlotte NC, studying Data Science and AI, analyst at Kewaunee Scientific, founder of Higgins Digital">
  {defs()}
  <style>{COMMON_CSS}</style>
  <rect width="1200" height="166" rx="24" fill="{BG}"/>
  {cells}
</svg>
"""
    write(ASSETS / "about.svg", svg)


def map_node(x: int, y: int, w: int, title: str, description: str,
             delay: float, core: bool = False) -> str:
    fill = "#0E1E2E" if core else PANEL
    stroke = BLUE if core else LINE
    return f"""
  <g class="rise" style="animation-delay:{delay:.2f}s">
    <rect x="{x}" y="{y}" width="{w}" height="100" rx="18" fill="{fill}"
          stroke="{stroke}" stroke-width="1.5"/>
    <rect x="{x + 24}" y="{y}" width="44" height="2" fill="url(#edge)"/>
    <text x="{x + 24}" y="{y + 46}" class="display" fill="{WHITE}"
          font-size="19" letter-spacing="-.6">{escape(title)}</text>
    <text x="{x + 24}" y="{y + 74}" class="sans" fill="{MUTED}"
          font-size="13.5">{escape(description)}</text>
  </g>
"""


def build_system_map() -> None:
    surfaces = [
        ("higginsd.com", "Higgins Digital Web Agency", True),
        ("Cade", "Personal agentic operating system", False),
        ("Propify", "Sports analytics platform", False),
        ("Portfolio", "Interactive project showcase", False),
        ("Curated Notes", "Writing and editorial archive", False),
        ("Photos & Frames", "Photography and gallery archive", False),
        ("Chaplain Platform", "Leadership resource system", False),
        ("davishiggins.com V2", "Personal platform rebuild", False),
        ("AI Workflow OS", "Practical AI learning guides", False),
        ("CrownCodeAI", "AI website generation tool", False),
        ("Higgins Digital Labs", "Experimental product studio", False),
    ]
    columns = (48, 428, 808)
    nodes = ""
    for i, (title, description, core) in enumerate(surfaces):
        x = columns[i % 3]
        y = 212 + (i // 3) * 124
        nodes += map_node(x, y, 344, title, description, .18 + i * .05, core)

    svg = f"""
<svg viewBox="0 0 1200 736" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="System map of the Davis Higgins digital ecosystem">
  {defs()}
  <style>{COMMON_CSS}</style>
  <rect width="1200" height="736" rx="26" fill="{BG}"/>
  <ellipse cx="600" cy="80" rx="440" ry="200" fill="url(#blueGlow)"/>

  <g class="rise" style="animation-delay:.06s">
    <rect x="350" y="32" width="500" height="112" rx="20" fill="#0E1E2E"
          stroke="{BLUE}" stroke-width="1.5"/>
    <text x="600" y="78" class="display" fill="{WHITE}" font-size="26"
          text-anchor="middle" letter-spacing="-.8">davishiggins.com</text>
    <text x="600" y="110" class="sans" fill="{BLUE_LIGHT}" font-size="15"
          text-anchor="middle">Complete Digital Hub</text>
  </g>

  <line x1="600" y1="144" x2="600" y2="196" stroke="{LINE}" stroke-width="1.5"/>
  <line x1="48" y1="196" x2="1152" y2="196" stroke="{LINE}" stroke-width="1.5"/>
  {nodes}
</svg>
"""
    write(ASSETS / "system-map.svg", svg)


PROJECTS = [
    {
        "name": "Cade",
        "type": "AGENTIC SYSTEM",
        "status": "LIVE",
        "description": "Personal agentic operating system with persistent memory.",
        "stack": "CLAUDE · OBSIDIAN · NEXT.JS",
        "url": "https://cade.davishiggins.com",
    },
    {
        "name": "Higgins Digital",
        "type": "WEB STUDIO",
        "status": "LIVE",
        "description": "High-performance websites and digital branding.",
        "stack": "NEXT.JS · TYPESCRIPT · VERCEL",
        "url": "https://higginsd.com",
    },
    {
        "name": "Propify",
        "type": "SPORTS ANALYTICS",
        "status": "LIVE",
        "description": "Sports analytics and projection platform.",
        "stack": "PYTHON · FASTAPI · NEXT.JS",
        "url": "https://propifyai.davishiggins.com",
    },
    {
        "name": "CrownCodeAI",
        "type": "AI TOOL",
        "status": "BUILDING",
        "description": "AI-powered website generation tool.",
        "stack": "CLAUDE API · NEXT.JS · TAILWIND",
        "url": "https://crowncode.higginsd.com",
    },
    {
        "name": "Davis Higgins Portfolio",
        "type": "PERSONAL PLATFORM",
        "status": "LIVE",
        "description": "Interactive portfolio and project hub.",
        "stack": "REACT · VITE · CLAUDE API",
        "url": "https://portfolio.davishiggins.com",
    },
    {
        "name": "Phi Delta Theta Chaplain Platform",
        "type": "COMMUNITY TOOL",
        "status": "LIVE",
        "description": "Chapter leadership and spiritual growth platform.",
        "stack": "REACT · VITE · VERCEL",
        "url": "https://chaplain.davishiggins.com",
    },
    {
        "name": "Photos & Frames",
        "type": "PHOTOGRAPHY",
        "status": "LIVE",
        "description": "Photography, gallery, and digital archive.",
        "stack": "PHOTOGRAPHY · GALLERY · ARCHIVE",
        "url": "https://photos.davishiggins.com",
    },
    {
        "name": "Curated Notes",
        "type": "WRITING",
        "status": "LIVE",
        "description": "Editorial platform for original articles and notes.",
        "stack": "NEXT.JS · MDX · VERCEL",
        "url": "https://notes.davishiggins.com",
    },
    {
        "name": "davishiggins.com V2",
        "type": "PERSONAL PLATFORM",
        "status": "BUILDING",
        "description": "Full personal site and portfolio rebuild.",
        "stack": "ASTRO · TYPESCRIPT · GSAP",
        "url": "https://v2.davishiggins.com",
    },
    {
        "name": "AI Workflow OS",
        "type": "AI EDUCATION",
        "status": "BUILDING",
        "description": "Practical courses and guides for people new to AI.",
        "stack": "AI WORKFLOWS · CLAUDE CODE · VERCEL",
        "url": "https://ai.davishiggins.com",
    },
]


def project_card(project: dict[str, str], index: int) -> None:
    live = project["status"] == "LIVE"
    status_color = BLUE_LIGHT if live else MUTED
    svg = f"""
<svg viewBox="0 0 570 166" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="{escape(project['name'])}: {escape(project['description'])}">
  {defs()}
  <style>
    {COMMON_CSS}
    .panel, .view {{ transition: stroke .3s ease, transform .3s ease, fill .3s ease; }}
    svg:hover .panel {{ stroke: {BLUE}; }}
    svg:hover .view {{ transform: translateX(4px); fill: {WHITE}; }}
  </style>
  <rect width="570" height="166" rx="20" fill="{BG}"/>
  <rect class="panel" x="1.5" y="1.5" width="567" height="163" rx="19"
        fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>
  <rect x="28" y="1" width="60" height="2" fill="url(#edge)"/>

  <text x="28" y="38" class="mono" fill="{BLUE}" font-size="11" font-weight="700"
        letter-spacing="2.2">{index:02d} / {escape(project['type'])}</text>
  <text x="542" y="38" class="mono" fill="{status_color}" font-size="10"
        letter-spacing="1.8" text-anchor="end">{escape(project['status'])}</text>

  <text x="28" y="80" class="display" fill="{WHITE}" font-size="24"
        letter-spacing="-1">{escape(project['name'])}</text>
  <text x="28" y="107" class="sans" fill="{MUTED}" font-size="13.5">{escape(project['description'])}</text>

  <line x1="28" y1="128" x2="542" y2="128" stroke="{LINE}"/>
  <text x="28" y="152" class="mono" fill="{MUTED}" font-size="10.5"
        letter-spacing="1.3">{escape(project['stack'])}</text>
  <text x="542" y="152" class="sans view" fill="{BLUE}" font-size="12.5"
        font-weight="700" text-anchor="end">VIEW &#8599;</text>
</svg>
"""
    slug = (
        project["name"]
        .lower()
        .replace("&", "and")
        .replace(".", "")
        .replace(" ", "-")
    )
    write(PROJECT_CARDS / f"{index:02d}-{slug}.svg", svg)


def build_statistics() -> None:
    metrics = [
        ("20+", "DASHBOARDS BUILT", "Power BI · Zoho Analytics"),
        ("15+", "WEBSITES LAUNCHED", "Personal + client builds"),
        ("10", "ACTIVE PROJECTS", "Web · AI · analytics"),
        ("3.89", "ACADEMIC GPA", "Data Science + AI"),
    ]
    cards = ""
    for i, (number, label, note) in enumerate(metrics):
        x = 24 + i * 292
        cards += f"""
  <g class="rise" style="animation-delay:{.08 + i * .07:.2f}s">
    <rect x="{x}" y="24" width="272" height="150" rx="20" fill="{PANEL}"
          stroke="{LINE}" stroke-width="1.5"/>
    <rect x="{x + 26}" y="24" width="52" height="2" fill="url(#edge)"/>
    <text x="{x + 26}" y="90" class="display" fill="{WHITE}" font-size="50"
          letter-spacing="-2">{escape(number)}</text>
    <text x="{x + 26}" y="123" class="mono" fill="{BLUE}" font-size="11.5"
          font-weight="700" letter-spacing="1.9">{escape(label)}</text>
    <text x="{x + 26}" y="150" class="sans" fill="{MUTED}" font-size="13">{escape(note)}</text>
  </g>
"""
    svg = f"""
<svg viewBox="0 0 1200 198" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Statistics overview: 20+ dashboards built, 15+ websites launched, 10 active projects, 3.89 GPA">
  {defs()}
  <style>{COMMON_CSS}</style>
  <rect width="1200" height="198" rx="24" fill="{BG}"/>
  {cards}
</svg>
"""
    write(ASSETS / "statistics-overview.svg", svg)


def build_stack() -> None:
    groups = [
        ("DATA + ANALYTICS", "Python · SQL · R", "Power BI · Zoho · Excel"),
        ("AI + AUTOMATION", "Claude Code · AI workflows", "Prompt systems · Agents"),
        ("FRONTEND", "Next.js · React · TypeScript", "Tailwind · GSAP · Framer Motion"),
        ("BACKEND + PLATFORMS", "Supabase · FastAPI · Vercel", "APIs · Content systems"),
        ("DESIGN + BRAND", "Branding · Editorial design", "SEO · Motion · Identity"),
        ("BUSINESS + STRATEGY", "Digital strategy · Client work", "Systems thinking"),
    ]
    boxes = ""
    for i, (title, line1, line2) in enumerate(groups):
        x = 24 + (i % 3) * 392
        y = 24 + (i // 3) * 168
        boxes += f"""
  <g class="rise" style="animation-delay:{.08 + i * .06:.2f}s">
    <rect x="{x}" y="{y}" width="368" height="144" rx="19" fill="{PANEL}"
          stroke="{LINE}" stroke-width="1.5"/>
    <rect x="{x + 26}" y="{y}" width="48" height="2" fill="url(#edge)"/>
    <text x="{x + 26}" y="{y + 44}" class="mono" fill="{BLUE}" font-size="11.5"
          font-weight="700" letter-spacing="2.2">{escape(title)}</text>
    <line x1="{x + 26}" y1="{y + 62}" x2="{x + 342}" y2="{y + 62}" stroke="{LINE}"/>
    <text x="{x + 26}" y="{y + 92}" class="sans" fill="{WHITE}" font-size="15">{escape(line1)}</text>
    <text x="{x + 26}" y="{y + 119}" class="sans" fill="{MUTED}" font-size="15">{escape(line2)}</text>
  </g>
"""
    svg = f"""
<svg viewBox="0 0 1200 360" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Davis Higgins technology, design, analytics, and strategy stack">
  {defs()}
  <style>{COMMON_CSS}</style>
  <rect width="1200" height="360" rx="24" fill="{BG}"/>
  {boxes}
</svg>
"""
    write(ASSETS / "stack.svg", svg)


def build_footer() -> None:
    svg = f"""
<svg viewBox="0 0 1200 200" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Let's build something sharp — contact Davis Higgins">
  {defs()}
  <style>{COMMON_CSS}</style>
  <rect width="1200" height="200" rx="26" fill="{BG}"/>
  <rect x="1" y="1" width="1198" height="198" rx="25" fill="url(#panelFill)"
        fill-opacity=".55" stroke="{LINE}" stroke-width="1.5"/>
  <rect x="540" y="0" width="120" height="2" fill="url(#edge)"/>

  <g class="rise" style="animation-delay:.08s">
    <text x="600" y="86" class="display" fill="{WHITE}" font-size="40"
          text-anchor="middle" letter-spacing="-1.6">LET&#8217;S BUILD SOMETHING SHARP.</text>
    <text x="600" y="126" class="sans" fill="{BLUE_LIGHT}" font-size="18"
          text-anchor="middle">davishiggins@icloud.com</text>
    <text x="600" y="162" class="mono" fill="{MUTED}" font-size="12"
          text-anchor="middle" letter-spacing="2.4">CHARLOTTE, NC</text>
  </g>
</svg>
"""
    write(ASSETS / "footer.svg", svg)


def prune_retired_assets() -> None:
    """Remove artwork replaced by markdown headers and prose."""
    retired = ["experience.svg"] + [
        f"section-0{n}-{slug}.svg"
        for n, slug in enumerate(
            ["about", "system-map", "projects", "statistics", "route", "stack"], start=1
        )
    ]
    for name in retired:
        (ASSETS / name).unlink(missing_ok=True)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    PROJECT_CARDS.mkdir(parents=True, exist_ok=True)

    if not LOGO.exists():
        raise SystemExit(f"Missing required logo: {LOGO}")

    build_hero()
    build_about()
    build_system_map()
    build_statistics()
    build_stack()
    build_footer()

    nav_badge("Email", "nav-email.svg")
    nav_badge("LinkedIn", "nav-linkedin.svg")
    nav_badge("Website", "nav-website.svg")
    nav_badge("Portfolio", "nav-portfolio.svg")
    nav_badge("Agency", "nav-agency.svg")

    for index, project in enumerate(PROJECTS, start=1):
        project_card(project, index)

    prune_retired_assets()

    print(f"Generated profile assets in {ASSETS}")


if __name__ == "__main__":
    main()
