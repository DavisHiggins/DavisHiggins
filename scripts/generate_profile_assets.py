#!/usr/bin/env python3
"""Generate the branded SVG system used by Davis Higgins's GitHub profile.

Design rules for this system:

* Motion is deliberate, not ambient. Traveling strokes are reserved for a small
  number of structural elements — the hero frame, the two system-map cores, the
  map's connective wiring, and the two full-width panels. Individual cards hold
  a static border so the page reads as composed rather than busy.
* Section headers are markdown, not artwork, so they sit on GitHub's own
  background instead of inside a panel.
* Narrative prose lives in README.md, outside the artwork, where it stays
  selectable, searchable, and accessible.

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
PANEL = "#08111B"
PANEL_2 = "#0B1622"
BLUE = "#7BAFD4"
BLUE_LIGHT = "#C8E7FA"
WHITE = "#F7FBFF"
MUTED = "#8EA2B4"
LINE = "#193142"


COMMON_CSS = f"""
    .display {{
      font-family: "Arial Black", "Helvetica Neue", Inter, Arial, sans-serif;
      font-weight: 900;
    }}
    .sans {{ font-family: "Helvetica Neue", Inter, Arial, sans-serif; }}
    .mono {{ font-family: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace; }}
    .trace {{
      stroke-dasharray: 42 260;
      animation: trace 6.5s linear infinite;
    }}
    .trace-slow {{
      stroke-dasharray: 74 440;
      animation: trace 10s linear infinite reverse;
    }}
    .wire {{
      stroke-dasharray: 8 12;
      animation: wire 16s linear infinite;
    }}
    .rise {{
      opacity: 0;
      animation: rise .7s cubic-bezier(.2,.7,.2,1) forwards;
    }}
    .pulse {{ animation: pulse 3.6s ease-in-out infinite; }}
    @keyframes trace {{ to {{ stroke-dashoffset: -604; }} }}
    @keyframes wire {{ to {{ stroke-dashoffset: -320; }} }}
    @keyframes rise {{
      from {{ opacity: 0; transform: translateY(8px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes pulse {{ 0%,100% {{ opacity: .5; }} 50% {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .trace, .trace-slow, .wire, .rise, .pulse {{
        animation: none !important;
        opacity: 1 !important;
      }}
    }}
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def defs(extra: str = "") -> str:
    return f"""
  <defs>
    <linearGradient id="blueLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{BLUE}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{BLUE_LIGHT}" stop-opacity="1"/>
      <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{BLUE}" stop-opacity=".85"/>
      <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="panelFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#122235" stop-opacity=".94"/>
      <stop offset=".55" stop-color="{PANEL}" stop-opacity=".9"/>
      <stop offset="1" stop-color="#050B12" stop-opacity=".96"/>
    </linearGradient>
    <radialGradient id="blueGlow">
      <stop offset="0" stop-color="{BLUE}" stop-opacity=".24"/>
      <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="42" height="42" patternUnits="userSpaceOnUse">
      <path d="M42 0H0V42" fill="none" stroke="{BLUE}" stroke-opacity=".055"/>
    </pattern>
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
    """Two traveling strokes: the outer frame and the rule under the name."""
    svg = f"""
<svg viewBox="0 0 1200 400" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Davis Higgins — data analyst, AI builder, web developer, and founder">
  {defs()}
  <style>{COMMON_CSS}</style>

  <rect width="1200" height="400" rx="28" fill="{BG}"/>
  <rect width="1200" height="400" rx="28" fill="url(#grid)"/>
  <ellipse cx="980" cy="110" rx="360" ry="250" fill="url(#blueGlow)"/>
  <rect x="18" y="18" width="1164" height="364" rx="24" fill="url(#panelFill)"
        stroke="{LINE}" stroke-width="1.5"/>
  <rect class="trace-slow" x="18" y="18" width="1164" height="364" rx="24"
        fill="none" stroke="{BLUE_LIGHT}" stroke-width="2.5"/>

  <g class="rise" style="animation-delay:.05s">
    <text x="64" y="88" class="mono" fill="{BLUE}" font-size="13" font-weight="700"
          letter-spacing="3.6">CHARLOTTE, NORTH CAROLINA</text>
  </g>

  <g class="rise" style="animation-delay:.14s">
    <text x="60" y="192" class="display" fill="{WHITE}" font-size="86"
          letter-spacing="-5">DAVIS HIGGINS</text>
    <text x="64" y="240" class="sans" fill="{BLUE_LIGHT}" font-size="24" font-weight="700">
      Data analyst, AI builder, and web developer.
    </text>
  </g>

  <rect x="64" y="272" width="660" height="3" rx="2" fill="{LINE}"/>
  <rect class="trace" x="64" y="271" width="660" height="5" rx="2"
        fill="none" stroke="{BLUE_LIGHT}" stroke-width="3"/>

  <g class="rise" style="animation-delay:.26s">
    <text x="64" y="318" class="mono" fill="{MUTED}" font-size="13" letter-spacing="2">
      DATA SCIENCE &#183; ARTIFICIAL INTELLIGENCE &#183; WEB SYSTEMS
    </text>
    <circle cx="70" cy="350" r="5" fill="{BLUE}" class="pulse"/>
    <text x="88" y="355" class="mono" fill="{BLUE_LIGHT}" font-size="13" letter-spacing="1.6">
      AVAILABLE FOR OPPORTUNITIES
    </text>
  </g>

  <g class="rise" style="animation-delay:.20s">
    <circle cx="1006" cy="200" r="126" fill="none" stroke="{BLUE}" stroke-opacity=".16"/>
    <image href="{logo_data_uri()}" x="898" y="92" width="216" height="216"
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
    """Original node geometry. Only the two cores keep a traveling border."""
    h = 116 if core else 104
    fill = "#102033" if core else PANEL
    title_size = 21 if core else 18
    moving_border = (
        f'\n    <rect class="trace-slow" x="{x}" y="{y}" width="{w}" height="{h}" rx="20"'
        f'\n          fill="none" stroke="{BLUE_LIGHT}" stroke-width="2.5"/>'
        if core
        else ""
    )
    dot = (
        f'\n    <circle cx="{x + 26}" cy="{y + 29}" r="5" fill="{BLUE}" class="pulse"/>'
        if core
        else f'\n    <circle cx="{x + 26}" cy="{y + 29}" r="4" fill="{BLUE}" fill-opacity=".85"/>'
    )
    return f"""
  <g class="rise" style="animation-delay:{delay:.2f}s">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}"
          stroke="{BLUE if core else LINE}" stroke-width="{2 if core else 1.5}"/>{moving_border}{dot}
    <text x="{x + 44}" y="{y + 36}" class="display" fill="{WHITE}" font-size="{title_size}"
          letter-spacing="-.5">{escape(title)}</text>
    <text x="{x + 26}" y="{y + 72}" class="sans" fill="{MUTED}" font-size="14">{escape(description)}</text>
    <rect x="{x + 26}" y="{y + h - 18}" width="{max(44, w - 52)}" height="2" rx="1"
          fill="url(#blueLine)" opacity=".55"/>
  </g>
"""


def build_system_map() -> None:
    nodes = [
        map_node(48, 64, 280, "Cade", "Personal agentic operating system", .12),
        map_node(460, 64, 280, "Portfolio", "Interactive project showcase", .18),
        map_node(872, 64, 280, "Propify", "Sports analytics platform", .24),
        map_node(48, 286, 280, "Curated Notes", "Writing and editorial archive", .30),
        map_node(872, 286, 280, "Photos & Frames", "Photography and gallery archive", .36),
        map_node(48, 508, 280, "Chaplain Platform", "Leadership resource system", .42),
        map_node(872, 508, 280, "davishiggins.com V2", "Personal platform rebuild", .48),
        map_node(48, 690, 280, "AI Workflow OS", "Practical AI learning guides", .54),
        map_node(420, 690, 360, "higginsd.com", "Higgins Digital Web Agency", .70, True),
        map_node(48, 910, 300, "CrownCodeAI", "AI website generation tool", .82),
        map_node(852, 910, 300, "Higgins Digital Labs", "Experimental product studio", .90),
    ]
    points = [
        ((600, 358), (188, 168)),
        ((600, 358), (600, 168)),
        ((600, 358), (1012, 168)),
        ((600, 358), (188, 338)),
        ((600, 358), (1012, 338)),
        ((600, 358), (188, 560)),
        ((600, 358), (1012, 560)),
        ((600, 416), (188, 690)),
        ((600, 416), (600, 690)),
        ((600, 806), (198, 910)),
        ((600, 806), (1002, 910)),
    ]
    wires = "\n".join(
        f'  <path d="M{x1} {y1} L{x2} {y2}" class="wire" stroke="{BLUE}" '
        f'stroke-opacity=".5" stroke-width="1.5" fill="none"/>'
        for (x1, y1), (x2, y2) in points
    )
    svg = f"""
<svg viewBox="0 0 1200 1080" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="System map of the Davis Higgins digital ecosystem, with davishiggins.com as the hub">
  {defs()}
  <style>{COMMON_CSS}</style>
  <rect width="1200" height="1080" rx="28" fill="{BG}"/>
  <rect width="1200" height="1080" rx="28" fill="url(#grid)"/>
  <ellipse cx="600" cy="410" rx="420" ry="340" fill="url(#blueGlow)" opacity=".75"/>
  {wires}
  {map_node(420, 300, 360, "davishiggins.com", "Complete Digital Hub", .04, True)}
  {''.join(nodes)}
  <text x="56" y="1054" class="mono" fill="{MUTED}" font-size="12" letter-spacing="2.2">
    ONE IDENTITY / MULTIPLE PURPOSE-BUILT SURFACES
  </text>
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
    """Static border, accent rail, and a hover state. Ten of these tile the
    page, so none of them carry a traveling stroke."""
    live = project["status"] == "LIVE"
    status_color = BLUE_LIGHT if live else MUTED
    svg = f"""
<svg viewBox="0 0 570 166" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="{escape(project['name'])}: {escape(project['description'])}">
  {defs()}
  <style>
    {COMMON_CSS}
    .panel, .view, .rail {{ transition: stroke .3s ease, transform .3s ease, fill .3s ease, opacity .3s ease; }}
    svg:hover .panel {{ stroke: {BLUE}; }}
    svg:hover .view {{ transform: translateX(4px); fill: {WHITE}; }}
    svg:hover .rail {{ opacity: 1; }}
  </style>
  <rect width="570" height="166" rx="20" fill="{BG}"/>
  <rect class="panel" x="1.5" y="1.5" width="567" height="163" rx="19"
        fill="url(#panelFill)" stroke="{LINE}" stroke-width="1.5"/>
  <rect class="rail" x="28" y="1" width="72" height="2" fill="url(#edge)" opacity=".7"/>

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


def metric_card(x: int, y: int, w: int, number: str, label: str,
                note: str, delay: float) -> str:
    """Original metric geometry, static border."""
    return f"""
  <g class="rise" style="animation-delay:{delay:.2f}s">
    <rect x="{x}" y="{y}" width="{w}" height="154" rx="22" fill="url(#panelFill)"
          stroke="{LINE}" stroke-width="1.5"/>
    <rect x="{x + 28}" y="{y}" width="52" height="2" fill="url(#edge)"/>
    <text x="{x + 28}" y="{y + 67}" class="display" fill="{WHITE}" font-size="52"
          letter-spacing="-2">{escape(number)}</text>
    <text x="{x + 28}" y="{y + 101}" class="mono" fill="{BLUE_LIGHT}" font-size="12"
          font-weight="700" letter-spacing="2">{escape(label)}</text>
    <text x="{x + 28}" y="{y + 130}" class="sans" fill="{MUTED}" font-size="13">{escape(note)}</text>
  </g>
"""


def build_statistics() -> None:
    metrics = "".join(
        [
            metric_card(24, 24, 268, "20+", "DASHBOARDS BUILT", "Power BI · Zoho Analytics", .10),
            metric_card(316, 24, 268, "15+", "WEBSITES LAUNCHED", "Personal + client builds", .18),
            metric_card(608, 24, 268, "10", "ACTIVE PROJECTS", "Web · AI · analytics · writing", .26),
            metric_card(900, 24, 276, "3.89", "ACADEMIC GPA", "Data Science + AI", .34),
        ]
    )
    svg = f"""
<svg viewBox="0 0 1200 440" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Statistics overview: 20+ dashboards built, 15+ websites launched, 10 active projects, 3.89 GPA, five-time Chancellor's List">
  {defs()}
  <style>
    {COMMON_CSS}
    .bar {{ transform:scaleX(0); transform-origin:left; animation:grow 1.4s cubic-bezier(.2,.7,.2,1) forwards; }}
    @keyframes grow {{ to {{ transform:scaleX(1); }} }}
    @media (prefers-reduced-motion: reduce) {{ .bar {{ animation:none; transform:scaleX(1); }} }}
  </style>
  <rect width="1200" height="440" rx="28" fill="{BG}"/>
  {metrics}
  <rect x="24" y="202" width="1152" height="214" rx="22" fill="url(#panelFill)"
        stroke="{LINE}" stroke-width="1.5"/>
  <rect class="trace-slow" x="24" y="202" width="1152" height="214" rx="22"
        fill="none" stroke="{BLUE_LIGHT}" stroke-width="2"/>

  <text x="54" y="244" class="mono" fill="{BLUE}" font-size="12" letter-spacing="2.6">WORK SURFACE</text>
  <text x="54" y="291" class="display" fill="{WHITE}" font-size="36">DATA &#8594; DECISION &#8594; EXPERIENCE</text>
  <text x="54" y="328" class="sans" fill="{MUTED}" font-size="16">Analytics, intelligent automation, product engineering, and brand systems.</text>

  <g transform="translate(670 236)">
    <text x="0" y="0" class="mono" fill="{MUTED}" font-size="11" letter-spacing="2">DATA + ANALYTICS</text>
    <rect x="0" y="14" width="400" height="7" rx="4" fill="{LINE}"/>
    <rect class="bar" x="0" y="14" width="362" height="7" rx="4" fill="{BLUE}" style="animation-delay:.2s"/>
    <text x="0" y="55" class="mono" fill="{MUTED}" font-size="11" letter-spacing="2">AI + AUTOMATION</text>
    <rect x="0" y="69" width="400" height="7" rx="4" fill="{LINE}"/>
    <rect class="bar" x="0" y="69" width="330" height="7" rx="4" fill="{BLUE_LIGHT}" style="animation-delay:.35s"/>
    <text x="0" y="110" class="mono" fill="{MUTED}" font-size="11" letter-spacing="2">WEB + PRODUCT</text>
    <rect x="0" y="124" width="400" height="7" rx="4" fill="{LINE}"/>
    <rect class="bar" x="0" y="124" width="378" height="7" rx="4" fill="{BLUE}" style="animation-delay:.5s"/>
  </g>

  <circle cx="54" cy="382" r="5" fill="{BLUE}" class="pulse"/>
  <text x="72" y="387" class="mono" fill="{BLUE_LIGHT}" font-size="12" letter-spacing="1.5">
    5&#215; CHANCELLOR&#8217;S LIST &#183; EXCELLENCE IN WRITING
  </text>
</svg>
"""
    write(ASSETS / "statistics-overview.svg", svg)


def position_row(y: int, date: str, title: str, organization: str,
                 detail: list[str], delay: float) -> str:
    """Original timeline-row geometry, with the detail allowed to wrap."""
    lines = "".join(
        f'<tspan x="126" dy="{0 if i == 0 else 23}">{escape(line)}</tspan>'
        for i, line in enumerate(detail)
    )
    return f"""
  <g class="rise" style="animation-delay:{delay:.2f}s">
    <circle cx="88" cy="{y}" r="8" fill="{BG}" stroke="{BLUE}" stroke-width="3"/>
    <circle cx="88" cy="{y}" r="3" fill="{BLUE_LIGHT}" class="pulse"/>
    <text x="126" y="{y - 19}" class="mono" fill="{BLUE}" font-size="12"
          font-weight="700" letter-spacing="2">{escape(date)}</text>
    <text x="126" y="{y + 14}" class="display" fill="{WHITE}" font-size="22"
          letter-spacing="-.8">{escape(title)}</text>
    <text x="1148" y="{y + 14}" class="sans" fill="{BLUE_LIGHT}" font-size="17"
          font-weight="700" text-anchor="end">{escape(organization)}</text>
    <text x="126" y="{y + 45}" class="sans" fill="{MUTED}" font-size="15">{lines}</text>
  </g>
"""


CURRENT_POSITIONS = [
    (
        "JUN 2025 – PRESENT",
        "Data Analyst",
        "Kewaunee Scientific",
        [
            "Data analytics work spanning Power BI and Zoho Analytics dashboards, KPI reporting,",
            "CRM/estimating auditing, and data governance.",
        ],
    ),
    (
        "JAN 2026 – PRESENT",
        "Founder & Web Developer",
        "Higgins Digital",
        [
            "Founder of a web design and development studio building high-performance,",
            "brand-forward websites for real businesses.",
        ],
    ),
    (
        "JULY 2026 – PRESENT",
        "Creative Director & Digital Commerce Lead",
        "Lakeside Sport Club",
        [
            "Founded and manage a premium e-commerce apparel brand, leading brand strategy,",
            "product development, website experience, merchandising, and digital commerce operations.",
        ],
    ),
    (
        "SEP 2025 – PRESENT",
        "VP of Philanthropy & Chaplain",
        "Phi Delta Theta",
        [
            "Chapter leadership across philanthropy and the chaplain role, including a custom digital",
            "resource hub for Bible studies, leadership notes, and faith-centered materials.",
        ],
    ),
]


def build_current_positions() -> None:
    rows = "".join(
        position_row(92 + i * 140, date, title, org, detail, .10 + i * .12)
        for i, (date, title, org, detail) in enumerate(CURRENT_POSITIONS)
    )
    summary = "; ".join(f"{t} at {o}, {d}" for d, t, o, _ in CURRENT_POSITIONS)
    svg = f"""
<svg viewBox="0 0 1200 660" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Current positions: {escape(summary)}">
  {defs()}
  <style>{COMMON_CSS}</style>
  <rect width="1200" height="660" rx="28" fill="{BG}"/>
  <rect x="24" y="24" width="1152" height="612" rx="24" fill="url(#panelFill)"
        stroke="{LINE}" stroke-width="1.5"/>
  <rect class="trace-slow" x="24" y="24" width="1152" height="612" rx="24"
        fill="none" stroke="{BLUE}" stroke-width="2.5"/>
  <line x1="88" y1="70" x2="88" y2="592" stroke="{LINE}" stroke-width="3"/>
  <line x1="88" y1="70" x2="88" y2="592" class="wire" stroke="{BLUE}" stroke-width="2"/>
  {rows}
</svg>
"""
    write(ASSETS / "current-positions.svg", svg)


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
    <rect x="{x}" y="{y}" width="368" height="144" rx="19" fill="url(#panelFill)"
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
        stroke="{LINE}" stroke-width="1.5"/>
  <rect class="trace-slow" x="1" y="1" width="1198" height="198" rx="25"
        fill="none" stroke="{BLUE_LIGHT}" stroke-width="2"/>

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
    """Remove artwork replaced by markdown headers or renamed."""
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
    build_current_positions()
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
