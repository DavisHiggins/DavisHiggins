#!/usr/bin/env python3
"""Generate the branded SVG system used by Davis Higgins's GitHub profile.

The output is intentionally dependency-free and GitHub-safe: SVG, CSS keyframes,
SMIL-free motion, and reduced-motion fallbacks. Run from the repository root:

    python scripts/generate_profile_assets.py
"""

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PROJECT_CARDS = ASSETS / "project-cards"

BG = "#03070B"
PANEL = "#08111B"
PANEL_2 = "#0B1622"
BLUE = "#7BAFD4"
BLUE_LIGHT = "#C8E7FA"
WHITE = "#F7FBFF"
MUTED = "#8EA2B4"
LINE = "#193142"


COMMON_CSS = f"""
    :root {{
      --bg: {BG};
      --panel: {PANEL};
      --panel-2: {PANEL_2};
      --blue: {BLUE};
      --blue-light: {BLUE_LIGHT};
      --white: {WHITE};
      --muted: {MUTED};
      --line: {LINE};
    }}
    .display {{
      font-family: "Arial Black", "Helvetica Neue", Inter, Arial, sans-serif;
      font-weight: 900;
    }}
    .sans {{
      font-family: "Helvetica Neue", Inter, Arial, sans-serif;
    }}
    .mono {{
      font-family: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
    }}
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
      opacity: 1;
      animation: rise .8s cubic-bezier(.2,.7,.2,1) forwards;
    }}
    .fade {{
      animation: fade 4.8s ease-in-out infinite;
    }}
    .float {{
      animation: float 5.5s ease-in-out infinite;
    }}
    .pulse {{
      animation: pulse 3.4s ease-in-out infinite;
    }}
    .sweep {{
      animation: sweep 7s linear infinite;
    }}
    @keyframes trace {{ to {{ stroke-dashoffset: -604; }} }}
    @keyframes wire {{ to {{ stroke-dashoffset: -320; }} }}
    @keyframes rise {{
      from {{ opacity: 0; transform: translateY(12px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes fade {{
      0%,100% {{ opacity: .28; }}
      50% {{ opacity: 1; }}
    }}
    @keyframes float {{
      0%,100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(-10px); }}
    }}
    @keyframes pulse {{
      0%,100% {{ opacity: .45; }}
      50% {{ opacity: 1; }}
    }}
    @keyframes sweep {{
      from {{ transform: translateX(-240px); }}
      to {{ transform: translateX(1440px); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .trace,.trace-slow,.wire,.rise,.fade,.float,.pulse,.sweep {{
        animation: none !important;
      }}
      .rise {{ opacity: 1; }}
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
    <linearGradient id="panelFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#122235" stop-opacity=".94"/>
      <stop offset=".55" stop-color="{PANEL}" stop-opacity=".9"/>
      <stop offset="1" stop-color="#050B12" stop-opacity=".96"/>
    </linearGradient>
    <radialGradient id="blueGlow">
      <stop offset="0" stop-color="{BLUE}" stop-opacity=".28"/>
      <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
    </radialGradient>
    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="grid" width="42" height="42" patternUnits="userSpaceOnUse">
      <path d="M42 0H0V42" fill="none" stroke="{BLUE}" stroke-opacity=".055"/>
    </pattern>
    {extra}
  </defs>
"""


def section_header(number: str, title: str, caption: str, filename: str) -> None:
    svg = f"""
<svg viewBox="0 0 1200 150" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Section {escape(number)}: {escape(title)}">
  {defs()}
  <style>{COMMON_CSS}</style>
  <rect width="1200" height="150" rx="24" fill="{BG}"/>
  <rect x="1" y="1" width="1198" height="148" rx="23" fill="url(#panelFill)"
        stroke="{LINE}" stroke-width="2"/>
  <rect class="trace" x="1" y="1" width="1198" height="148" rx="23" fill="none"
        stroke="{BLUE_LIGHT}" stroke-width="2.5"/>
  <circle cx="54" cy="50" r="5" fill="{BLUE}" class="pulse"/>
  <text x="78" y="57" class="mono" fill="{BLUE}" font-size="15" font-weight="700"
        letter-spacing="3.5">{escape(number)}</text>
  <text x="52" y="115" class="display" fill="{WHITE}" font-size="54"
        letter-spacing="-2.5">{escape(title.upper())}</text>
  <text x="1148" y="108" class="sans" fill="{MUTED}" font-size="16"
        text-anchor="end">{escape(caption)}</text>
  <rect x="920" y="126" width="228" height="2" rx="1" fill="url(#blueLine)"/>
</svg>
"""
    write(ASSETS / filename, svg)


def nav_badge(label: str, filename: str) -> None:
    svg = f"""
<svg viewBox="0 0 220 58" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="{escape(label)}">
  {defs()}
  <style>
    {COMMON_CSS}
    .label,.arrow {{ transition: transform .28s ease, fill .28s ease; }}
    svg:hover .label {{ transform: translateX(5px); fill: {BLUE_LIGHT}; }}
    svg:hover .arrow {{ transform: translateX(4px); }}
  </style>
  <rect x="1" y="1" width="218" height="56" rx="15" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>
  <rect class="trace" x="1" y="1" width="218" height="56" rx="15" fill="none"
        stroke="{BLUE}" stroke-width="2"/>
  <circle cx="28" cy="29" r="5" fill="{BLUE}" class="pulse"/>
  <text x="48" y="35" class="sans label" fill="{WHITE}" font-size="15" font-weight="750"
        letter-spacing=".6">{escape(label)}</text>
  <text x="194" y="35" class="sans arrow" fill="{BLUE_LIGHT}" font-size="16">↗</text>
</svg>
"""
    write(ASSETS / filename, svg)


def build_hero() -> None:
    svg = f"""
<svg viewBox="0 0 1200 520" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Davis Higgins — data analyst, AI builder, web developer, and founder">
  {defs()}
  <style>
    {COMMON_CSS}
    .word1 {{ animation: word1 9s ease-in-out infinite; }}
    .word2 {{ animation: word2 9s ease-in-out infinite; opacity:0; }}
    .word3 {{ animation: word3 9s ease-in-out infinite; opacity:0; }}
    .scan {{ animation: scan 8s ease-in-out infinite; }}
    .hero-name {{ transition: letter-spacing .35s ease, transform .35s ease; }}
    svg:hover .hero-name {{ letter-spacing: -2px; transform: translateX(8px); }}
    @keyframes word1 {{ 0%,28%,100%{{opacity:1;transform:translateY(0)}} 34%,94%{{opacity:0;transform:translateY(-10px)}} }}
    @keyframes word2 {{ 0%,28%,62%,100%{{opacity:0;transform:translateY(10px)}} 34%,56%{{opacity:1;transform:translateY(0)}} }}
    @keyframes word3 {{ 0%,60%,94%,100%{{opacity:0;transform:translateY(10px)}} 66%,88%{{opacity:1;transform:translateY(0)}} }}
    @keyframes scan {{ 0%,100%{{transform:translateX(-120px);opacity:0}} 15%,85%{{opacity:.7}} 50%{{transform:translateX(1120px);opacity:.25}} }}
    @media (prefers-reduced-motion: reduce) {{
      .word1,.word2,.word3,.scan {{ animation:none; }}
      .word1{{opacity:1}} .word2,.word3{{opacity:0}}
    }}
  </style>
  <rect width="1200" height="520" rx="34" fill="{BG}"/>
  <rect width="1200" height="520" rx="34" fill="url(#grid)"/>
  <ellipse cx="1020" cy="88" rx="330" ry="230" fill="url(#blueGlow)" class="fade"/>
  <rect x="24" y="24" width="1152" height="472" rx="30" fill="url(#panelFill)"
        stroke="{LINE}" stroke-width="2"/>
  <rect class="trace-slow" x="24" y="24" width="1152" height="472" rx="30"
        fill="none" stroke="{BLUE_LIGHT}" stroke-width="3"/>
  <rect class="trace" x="38" y="38" width="1124" height="444" rx="24"
        fill="none" stroke="{BLUE}" stroke-opacity=".55" stroke-width="1.5"/>

  <g class="rise" style="animation-delay:.12s">
    <text x="70" y="90" class="mono" fill="{BLUE}" font-size="15" font-weight="700"
          letter-spacing="4">DAVIS / DIGITAL SYSTEMS / CHARLOTTE, NC</text>
    <circle cx="1100" cy="82" r="6" fill="{BLUE}" class="pulse"/>
    <text x="1082" y="88" class="mono" fill="{BLUE_LIGHT}" font-size="13"
          text-anchor="end" letter-spacing="2">AVAILABLE FOR OPPORTUNITIES</text>
  </g>

  <text x="64" y="228" class="display hero-name" fill="{WHITE}" font-size="96"
        letter-spacing="-6">DAVIS HIGGINS</text>
  <rect x="68" y="252" width="730" height="3" rx="2" fill="{LINE}"/>
  <rect class="trace" x="68" y="251" width="730" height="5" rx="2"
        fill="none" stroke="{BLUE_LIGHT}" stroke-width="3"/>

  <g class="sans" font-size="27" font-weight="720">
    <text class="word1" x="68" y="306" fill="{BLUE_LIGHT}">Building sharper systems for smarter decisions.</text>
    <text class="word2" x="68" y="306" fill="{BLUE_LIGHT}">Data, AI, interfaces, and brands—built as one system.</text>
    <text class="word3" x="68" y="306" fill="{BLUE_LIGHT}">Analyze. Create. Improve. Repeat.</text>
  </g>

  <g class="rise" style="animation-delay:.45s">
    <text x="70" y="372" class="mono" fill="{MUTED}" font-size="13" letter-spacing="2.8">CURRENT</text>
    <text x="70" y="404" class="sans" fill="{WHITE}" font-size="19" font-weight="700">Data Analyst · Kewaunee Scientific</text>
    <text x="478" y="372" class="mono" fill="{MUTED}" font-size="13" letter-spacing="2.8">STUDIO</text>
    <text x="478" y="404" class="sans" fill="{WHITE}" font-size="17" font-weight="700">Founder · Higgins Digital</text>
    <text x="840" y="372" class="mono" fill="{MUTED}" font-size="13" letter-spacing="2.8">FOCUS</text>
    <text x="840" y="404" class="sans" fill="{WHITE}" font-size="17" font-weight="700">Data · AI · Web Systems</text>
  </g>

  <g class="float">
    <text x="1018" y="306" class="display" fill="{BLUE}" fill-opacity=".13"
          stroke="{BLUE}" stroke-opacity=".3" font-size="168" text-anchor="middle"
          letter-spacing="-10">DH</text>
    <circle cx="1018" cy="250" r="116" fill="none" stroke="{BLUE}" stroke-opacity=".13"/>
    <circle cx="1018" cy="250" r="96" fill="none" stroke="{BLUE_LIGHT}" stroke-opacity=".13"
            stroke-dasharray="4 14" class="wire"/>
  </g>

  <g class="scan">
    <rect x="0" y="38" width="130" height="444" fill="url(#blueLine)" opacity=".12"/>
    <rect x="128" y="38" width="2" height="444" fill="{BLUE_LIGHT}" opacity=".75"/>
  </g>

  <text x="70" y="462" class="mono" fill="{MUTED}" font-size="12" letter-spacing="2.2">
    DAVISHIGGINS.COM  /  DATA SCIENCE + ARTIFICIAL INTELLIGENCE  /  2026
  </text>
</svg>
"""
    write(ASSETS / "hero.svg", svg)


def build_about() -> None:
    svg = f"""
<svg viewBox="0 0 1200 430" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="About Davis Higgins">
  {defs()}
  <style>{COMMON_CSS}</style>
  <rect width="1200" height="430" rx="26" fill="{BG}"/>
  <rect x="22" y="22" width="770" height="386" rx="24" fill="url(#panelFill)"
        stroke="{LINE}" stroke-width="2"/>
  <rect class="trace-slow" x="22" y="22" width="770" height="386" rx="24"
        fill="none" stroke="{BLUE}" stroke-width="2.5"/>
  <rect x="816" y="22" width="362" height="386" rx="24" fill="url(#panelFill)"
        stroke="{LINE}" stroke-width="2"/>
  <rect class="trace" x="816" y="22" width="362" height="386" rx="24"
        fill="none" stroke="{BLUE_LIGHT}" stroke-width="2.5"/>

  <g class="rise" style="animation-delay:.12s">
    <text x="60" y="78" class="mono" fill="{BLUE}" font-size="13" font-weight="700"
          letter-spacing="3">PROFILE / ABOUT</text>
    <text x="60" y="135" class="display" fill="{WHITE}" font-size="37"
          letter-spacing="-1.6">DATA. INTELLIGENCE. CRAFT.</text>
    <text x="60" y="184" class="sans" fill="{BLUE_LIGHT}" font-size="21" font-weight="700">
      I turn complex ideas into useful digital products.
    </text>
    <text x="60" y="230" class="sans" fill="{MUTED}" font-size="18">
      <tspan x="60" dy="0">I’m a data analyst, AI builder, and web developer working across</tspan>
      <tspan x="60" dy="29">analytics, automation, full-stack products, and high-craft design.</tspan>
      <tspan x="60" dy="29">I study Data Science and AI at UNC Charlotte, build business</tspan>
      <tspan x="60" dy="29">intelligence at Kewaunee Scientific, and lead Higgins Digital.</tspan>
    </text>
    <text x="60" y="366" class="mono" fill="{WHITE}" font-size="13" letter-spacing="1.8">
      BUILDING SYSTEMS THAT FEEL CLEAR, USEFUL, AND MEMORABLE.
    </text>
  </g>

  <g class="rise" style="animation-delay:.38s">
    <text x="852" y="72" class="mono" fill="{BLUE}" font-size="12" letter-spacing="3">SIGNAL</text>
    <line x1="852" y1="92" x2="1142" y2="92" stroke="{LINE}"/>
    <text x="852" y="132" class="mono" fill="{MUTED}" font-size="12" letter-spacing="2">LOCATION</text>
    <text x="1142" y="132" class="sans" fill="{WHITE}" font-size="17" font-weight="700" text-anchor="end">Charlotte, NC</text>
    <text x="852" y="184" class="mono" fill="{MUTED}" font-size="12" letter-spacing="2">ROLE</text>
    <text x="1142" y="184" class="sans" fill="{WHITE}" font-size="17" font-weight="700" text-anchor="end">Data Analyst</text>
    <text x="852" y="236" class="mono" fill="{MUTED}" font-size="12" letter-spacing="2">STUDIO</text>
    <text x="1142" y="236" class="sans" fill="{WHITE}" font-size="17" font-weight="700" text-anchor="end">Higgins Digital</text>
    <text x="852" y="288" class="mono" fill="{MUTED}" font-size="12" letter-spacing="2">DISCIPLINES</text>
    <text x="1142" y="288" class="sans" fill="{WHITE}" font-size="17" font-weight="700" text-anchor="end">Data · AI · Web</text>
    <line x1="852" y1="316" x2="1142" y2="316" stroke="{LINE}"/>
    <circle cx="862" cy="354" r="5" fill="{BLUE}" class="pulse"/>
    <text x="880" y="360" class="mono" fill="{BLUE_LIGHT}" font-size="12" letter-spacing="1.5">OPEN TO INTERNSHIP + PROJECT WORK</text>
  </g>
</svg>
"""
    write(ASSETS / "about.svg", svg)


def node(x: int, y: int, w: int, title: str, description: str, delay: float, core: bool = False) -> str:
    h = 116 if core else 104
    fill = "#102033" if core else PANEL
    title_size = 21 if core else 18
    trace_class = "trace-slow" if core else "trace"
    return f"""
  <g class="rise" style="animation-delay:{delay:.2f}s">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}"
          stroke="{LINE}" stroke-width="2"/>
    <rect class="{trace_class}" x="{x}" y="{y}" width="{w}" height="{h}" rx="20"
          fill="none" stroke="{BLUE_LIGHT if core else BLUE}" stroke-width="{3 if core else 2}"/>
    <circle cx="{x + 26}" cy="{y + 29}" r="5" fill="{BLUE}" class="pulse"/>
    <text x="{x + 44}" y="{y + 36}" class="display" fill="{WHITE}" font-size="{title_size}"
          letter-spacing="-.5">{escape(title)}</text>
    <text x="{x + 26}" y="{y + 72}" class="sans" fill="{MUTED}" font-size="14">{escape(description)}</text>
    <rect x="{x + 26}" y="{y + h - 18}" width="{max(44, w - 52)}" height="2" rx="1"
          fill="url(#blueLine)" opacity=".7"/>
  </g>
"""


def build_system_map() -> None:
    nodes = [
        node(48, 64, 280, "Cade", "Personal agentic operating system", .12),
        node(460, 64, 280, "Portfolio", "Interactive project showcase", .18),
        node(872, 64, 280, "Propify", "Sports analytics platform", .24),
        node(48, 286, 280, "Curated Notes", "Writing and editorial archive", .30),
        node(872, 286, 280, "Photos & Frames", "Photography and gallery archive", .36),
        node(48, 508, 280, "Chaplain Platform", "Leadership resource system", .42),
        node(872, 508, 280, "davishiggins.com V2", "Personal platform rebuild", .48),
        node(48, 690, 280, "AI Workflow OS", "Practical AI learning guides", .54),
        node(420, 690, 360, "higginsd.com", "Higgins Digital Web Agency", .70, True),
        node(48, 910, 300, "CrownCodeAI", "AI website generation tool", .82),
        node(852, 910, 300, "Higgins Digital Labs", "Experimental product studio", .90),
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
        f'stroke-opacity=".55" stroke-width="2" fill="none"/>'
        for (x1, y1), (x2, y2) in points
    )
    svg = f"""
<svg viewBox="0 0 1200 1080" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Davis Higgins digital ecosystem system map">
  {defs()}
  <style>{COMMON_CSS}</style>
  <rect width="1200" height="1080" rx="28" fill="{BG}"/>
  <rect width="1200" height="1080" rx="28" fill="url(#grid)"/>
  <ellipse cx="600" cy="410" rx="420" ry="340" fill="url(#blueGlow)" opacity=".75"/>
  {wires}
  {node(420, 300, 360, "davishiggins.com", "Complete Digital Hub", .04, True)}
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
        "description": "Personal agentic operating system with persistent, structured memory.",
        "stack": "CLAUDE · OBSIDIAN · NEXT.JS · GSAP",
        "url": "https://cade.davishiggins.com",
    },
    {
        "name": "Higgins Digital",
        "type": "WEB STUDIO",
        "status": "LIVE",
        "description": "High-performance website and digital branding company.",
        "stack": "NEXT.JS · TYPESCRIPT · FRAMER MOTION · VERCEL",
        "url": "https://higginsd.com",
    },
    {
        "name": "Propify",
        "type": "SPORTS ANALYTICS",
        "status": "LIVE",
        "description": "Sports analytics and projection platform.",
        "stack": "PYTHON · FASTAPI · NEXT.JS · MACHINE LEARNING",
        "url": "https://propifyai.davishiggins.com",
    },
    {
        "name": "CrownCodeAI",
        "type": "AI TOOL",
        "status": "BUILDING",
        "description": "AI-powered website generation concept and tool.",
        "stack": "CLAUDE API · NEXT.JS · TYPESCRIPT · TAILWIND",
        "url": "https://crowncode.higginsd.com",
    },
    {
        "name": "Davis Higgins Portfolio",
        "type": "PERSONAL PLATFORM",
        "status": "LIVE",
        "description": "Personal platform and project hub.",
        "stack": "REACT · VITE · FRAMER MOTION · CLAUDE API",
        "url": "https://portfolio.davishiggins.com",
    },
    {
        "name": "Phi Delta Theta Chaplain Platform",
        "type": "COMMUNITY TOOL",
        "status": "LIVE",
        "description": "Chapter leadership and spiritual growth platform.",
        "stack": "REACT · VITE · CONTENT SYSTEM · VERCEL",
        "url": "https://chaplain.davishiggins.com",
    },
    {
        "name": "Photos & Frames",
        "type": "PHOTOGRAPHY",
        "status": "LIVE",
        "description": "Photography and gallery project.",
        "stack": "PHOTOGRAPHY · GALLERY · DIGITAL ARCHIVE",
        "url": "https://photos.davishiggins.com",
    },
    {
        "name": "Curated Notes",
        "type": "WRITING",
        "status": "LIVE",
        "description": "Blog and article platform with self-written entries.",
        "stack": "NEXT.JS · MDX · EDITORIAL DESIGN · VERCEL",
        "url": "https://notes.davishiggins.com",
    },
    {
        "name": "davishiggins.com V2",
        "type": "PERSONAL PLATFORM",
        "status": "BUILDING",
        "description": "Full rebuild of the personal site and portfolio.",
        "stack": "ASTRO · TYPESCRIPT · GSAP · SCSS",
        "url": "https://v2.davishiggins.com",
    },
    {
        "name": "AI Workflow OS",
        "type": "AI EDUCATION",
        "status": "BUILDING",
        "description": "Curated AI courses and guides for people new to AI.",
        "stack": "AI WORKFLOWS · CLAUDE CODE · GUIDES · VERCEL",
        "url": "https://ai.davishiggins.com",
    },
]


def project_card(project: dict[str, str], index: int) -> None:
    accent = BLUE_LIGHT if index == 1 else BLUE
    svg = f"""
<svg viewBox="0 0 570 180" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="{escape(project['name'])}: {escape(project['description'])}">
  {defs()}
  <style>
    {COMMON_CSS}
    .shift {{ animation: shift 5s ease-in-out infinite; }}
    .shift,.view {{ transition: transform .32s ease, fill .32s ease; }}
    svg:hover .shift {{ animation-play-state: paused; transform: translateX(12px); }}
    svg:hover .view {{ transform: translateX(5px); fill: {WHITE}; }}
    @keyframes shift {{ 0%,100%{{transform:translateX(0)}} 50%{{transform:translateX(8px)}} }}
    @media (prefers-reduced-motion: reduce) {{ .shift {{ animation:none; }} }}
  </style>
  <rect width="570" height="180" rx="22" fill="{BG}"/>
  <rect x="2" y="2" width="566" height="176" rx="20" fill="url(#panelFill)"
        stroke="{LINE}" stroke-width="2"/>
  <rect class="trace" x="2" y="2" width="566" height="176" rx="20" fill="none"
        stroke="{accent}" stroke-width="2.5" style="animation-delay:-{index * .37:.2f}s"/>
  <text x="28" y="34" class="mono" fill="{BLUE}" font-size="11" font-weight="700"
        letter-spacing="2.2">{index:02d} / {escape(project['type'])}</text>
  <text x="540" y="34" class="mono" fill="{BLUE_LIGHT}" font-size="10"
        letter-spacing="1.8" text-anchor="end">{escape(project['status'])}</text>
  <g class="shift" style="animation-delay:-{index * .23:.2f}s">
    <text x="28" y="77" class="display" fill="{WHITE}" font-size="25"
          letter-spacing="-1">{escape(project['name'])}</text>
    <text x="28" y="105" class="sans" fill="{MUTED}" font-size="14">{escape(project['description'])}</text>
  </g>
  <line x1="28" y1="126" x2="542" y2="126" stroke="{LINE}"/>
  <text x="28" y="153" class="mono" fill="{MUTED}" font-size="10.5"
        letter-spacing="1.3">{escape(project['stack'])}</text>
  <text x="542" y="158" class="sans view" fill="{BLUE_LIGHT}" font-size="13"
        font-weight="700" text-anchor="end">VIEW ↗</text>
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


def metric_card(x: int, y: int, w: int, number: str, label: str, note: str, delay: float) -> str:
    return f"""
  <g class="rise" style="animation-delay:{delay:.2f}s">
    <rect x="{x}" y="{y}" width="{w}" height="154" rx="22" fill="url(#panelFill)"
          stroke="{LINE}" stroke-width="2"/>
    <rect class="trace" x="{x}" y="{y}" width="{w}" height="154" rx="22"
          fill="none" stroke="{BLUE}" stroke-width="2"/>
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
     aria-label="Statistics overview: dashboards, websites, active projects, GPA, and honors">
  {defs()}
  <style>
    {COMMON_CSS}
    .bar {{ transform:scaleX(0); transform-origin:left; animation:grow 1.4s cubic-bezier(.2,.7,.2,1) forwards; }}
    @keyframes grow {{ to {{ transform:scaleX(1); }} }}
    @media (prefers-reduced-motion: reduce) {{ .bar{{animation:none;transform:scaleX(1)}} }}
  </style>
  <rect width="1200" height="440" rx="28" fill="{BG}"/>
  {metrics}
  <rect x="24" y="202" width="1152" height="214" rx="22" fill="url(#panelFill)"
        stroke="{LINE}" stroke-width="2"/>
  <rect class="trace-slow" x="24" y="202" width="1152" height="214" rx="22"
        fill="none" stroke="{BLUE_LIGHT}" stroke-width="2"/>

  <text x="54" y="244" class="mono" fill="{BLUE}" font-size="12" letter-spacing="2.6">WORK SURFACE</text>
  <text x="54" y="291" class="display" fill="{WHITE}" font-size="36">DATA → DECISION → EXPERIENCE</text>
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
    5× CHANCELLOR’S LIST · EXCELLENCE IN WRITING
  </text>
</svg>
"""
    write(ASSETS / "statistics-overview.svg", svg)


def experience_row(y: int, date: str, title: str, organization: str, detail: str, delay: float) -> str:
    return f"""
  <g class="rise" style="animation-delay:{delay:.2f}s">
    <circle cx="88" cy="{y}" r="8" fill="{BG}" stroke="{BLUE}" stroke-width="3"/>
    <circle cx="88" cy="{y}" r="3" fill="{BLUE_LIGHT}" class="pulse"/>
    <text x="126" y="{y - 19}" class="mono" fill="{BLUE}" font-size="12"
          font-weight="700" letter-spacing="2">{escape(date)}</text>
    <text x="126" y="{y + 14}" class="display" fill="{WHITE}" font-size="23"
          letter-spacing="-.8">{escape(title)}</text>
    <text x="700" y="{y + 14}" class="sans" fill="{BLUE_LIGHT}" font-size="17"
          font-weight="700">{escape(organization)}</text>
    <text x="126" y="{y + 45}" class="sans" fill="{MUTED}" font-size="15">{escape(detail)}</text>
  </g>
"""


def build_experience() -> None:
    rows = "".join(
        [
            experience_row(92, "JAN 2026 — PRESENT", "Founder & Web Developer", "Higgins Digital", "High-performance, brand-forward websites and digital systems for real businesses.", .10),
            experience_row(222, "SEP 2025 — PRESENT", "VP of Philanthropy & Chaplain", "Phi Delta Theta", "Chapter leadership, philanthropy, and a custom faith-centered digital resource hub.", .22),
            experience_row(352, "JUN 2025 — PRESENT", "Data Analyst", "Kewaunee Scientific", "Power BI and Zoho dashboards, KPI reporting, auditing, and data governance.", .34),
            experience_row(482, "MAY — AUG 2024", "Assistant to Project Manager", "Higgins Building Group", "Project operations, coordination, and documentation across active construction work.", .46),
            experience_row(612, "DEC 2022 — MAY 2024", "Operations Lead", "Teesly LLC", "Daily operations, fulfillment, and process organization for a product business.", .58),
        ]
    )
    svg = f"""
<svg viewBox="0 0 1200 690" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Davis Higgins experience timeline">
  {defs()}
  <style>{COMMON_CSS}</style>
  <rect width="1200" height="690" rx="28" fill="{BG}"/>
  <rect x="24" y="24" width="1152" height="642" rx="24" fill="url(#panelFill)"
        stroke="{LINE}" stroke-width="2"/>
  <rect class="trace-slow" x="24" y="24" width="1152" height="642" rx="24"
        fill="none" stroke="{BLUE}" stroke-width="2.5"/>
  <line x1="88" y1="70" x2="88" y2="634" stroke="{LINE}" stroke-width="3"/>
  <line x1="88" y1="70" x2="88" y2="634" class="wire" stroke="{BLUE}" stroke-width="2"/>
  {rows}
</svg>
"""
    write(ASSETS / "experience.svg", svg)


def stack_box(x: int, y: int, w: int, title: str, items: str, delay: float) -> str:
    return f"""
  <g class="rise" style="animation-delay:{delay:.2f}s">
    <rect x="{x}" y="{y}" width="{w}" height="154" rx="21" fill="url(#panelFill)"
          stroke="{LINE}" stroke-width="2"/>
    <rect class="trace" x="{x}" y="{y}" width="{w}" height="154" rx="21"
          fill="none" stroke="{BLUE}" stroke-width="2"/>
    <text x="{x + 26}" y="{y + 40}" class="mono" fill="{BLUE}" font-size="12"
          font-weight="700" letter-spacing="2.3">{escape(title)}</text>
    <line x1="{x + 26}" y1="{y + 58}" x2="{x + w - 26}" y2="{y + 58}" stroke="{LINE}"/>
    <text x="{x + 26}" y="{y + 88}" class="sans" fill="{WHITE}" font-size="15.5">
      {"".join(f'<tspan x="{x + 26}" dy="{0 if i == 0 else 27}">{escape(line)}</tspan>' for i, line in enumerate(items.split("|")))}
    </text>
  </g>
"""


def build_stack() -> None:
    boxes = "".join(
        [
            stack_box(24, 24, 366, "DATA + ANALYTICS", "Python · SQL · Power BI|Tableau · Excel · Salesforce", .08),
            stack_box(417, 24, 366, "AI + AUTOMATION", "AI workflows · Claude Code|Prompt systems · Automation", .16),
            stack_box(810, 24, 366, "FRONTEND", "Next.js · React · TypeScript|Tailwind · GSAP · Framer Motion", .24),
            stack_box(24, 202, 366, "BACKEND + PLATFORMS", "Vercel · Supabase · FastAPI|Content systems · APIs", .32),
            stack_box(417, 202, 366, "DESIGN + BRAND", "Branding · SEO · Editorial design|Web analytics · Motion", .40),
            stack_box(810, 202, 366, "BUSINESS + STRATEGY", "Digital strategy · Client websites|Personal branding · Systems thinking", .48),
        ]
    )
    svg = f"""
<svg viewBox="0 0 1200 380" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Davis Higgins technology and strategy stack">
  {defs()}
  <style>{COMMON_CSS}</style>
  <rect width="1200" height="380" rx="28" fill="{BG}"/>
  {boxes}
</svg>
"""
    write(ASSETS / "stack.svg", svg)


def build_footer() -> None:
    svg = f"""
<svg viewBox="0 0 1200 270" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Davis Higgins — analyze, create, improve, repeat">
  {defs()}
  <style>
    {COMMON_CSS}
    .marquee {{ animation: marquee 18s linear infinite; }}
    @keyframes marquee {{ from{{transform:translateX(0)}} to{{transform:translateX(-615px)}} }}
    @media (prefers-reduced-motion: reduce) {{ .marquee{{animation:none}} }}
  </style>
  <rect width="1200" height="270" rx="28" fill="{BG}"/>
  <rect x="1" y="1" width="1198" height="268" rx="27" fill="url(#panelFill)"
        stroke="{LINE}" stroke-width="2"/>
  <rect class="trace-slow" x="1" y="1" width="1198" height="268" rx="27"
        fill="none" stroke="{BLUE_LIGHT}" stroke-width="2.5"/>
  <g clip-path="url(#footerClip)">
    <g class="marquee">
      <text x="22" y="72" class="display" fill="{BLUE}" fill-opacity=".16" font-size="52" letter-spacing="-1">
        ANALYZE · CREATE · IMPROVE · REPEAT · ANALYZE · CREATE · IMPROVE · REPEAT ·
      </text>
      <text x="1248" y="72" class="display" fill="{BLUE}" fill-opacity=".16" font-size="52" letter-spacing="-1">
        ANALYZE · CREATE · IMPROVE · REPEAT · ANALYZE · CREATE · IMPROVE · REPEAT ·
      </text>
    </g>
  </g>
  <text x="600" y="145" class="display" fill="{WHITE}" font-size="44" text-anchor="middle"
        letter-spacing="-1.8">LET’S BUILD SOMETHING SHARP.</text>
  <text x="600" y="184" class="sans" fill="{BLUE_LIGHT}" font-size="18"
        text-anchor="middle">davishiggins@icloud.com</text>
  <circle cx="498" cy="224" r="4" fill="{BLUE}" class="pulse"/>
  <text x="516" y="229" class="mono" fill="{MUTED}" font-size="12" letter-spacing="2">CHARLOTTE, NC · 2026</text>
  <defs>
    <clipPath id="footerClip"><rect x="1" y="1" width="1198" height="92" rx="27"/></clipPath>
  </defs>
</svg>
"""
    write(ASSETS / "footer.svg", svg)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    PROJECT_CARDS.mkdir(parents=True, exist_ok=True)

    build_hero()
    build_about()
    build_system_map()
    build_statistics()
    build_experience()
    build_stack()
    build_footer()

    nav_badge("Email", "nav-email.svg")
    nav_badge("LinkedIn", "nav-linkedin.svg")
    nav_badge("Website", "nav-website.svg")
    nav_badge("Portfolio", "nav-portfolio.svg")
    nav_badge("Agency", "nav-agency.svg")

    section_header("01", "About", "Identity, focus, and current work", "section-01-about.svg")
    section_header("02", "System Map", "One identity. Multiple purpose-built surfaces.", "section-02-system-map.svg")
    section_header("03", "Projects", "Ten live and actively built digital products", "section-03-projects.svg")
    section_header("04", "Statistics Overview", "Measured output across data, web, and academics", "section-04-statistics.svg")
    section_header("05", "Route", "Experience across analytics, leadership, and operations", "section-05-route.svg")
    section_header("06", "Stack", "The tools behind the systems", "section-06-stack.svg")

    for index, project in enumerate(PROJECTS, start=1):
        project_card(project, index)

    print(f"Generated profile assets in {ASSETS}")


if __name__ == "__main__":
    main()
