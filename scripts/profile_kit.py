#!/usr/bin/env python3
"""Shared design system for the Davis Higgins profile README artwork.

Every surface in this system is white. GitHub themes the page background, so
anything that must stay white is rendered as an SVG that paints its own
`#FFFFFF` base rect. Markdown prose and markdown tables are deliberately not
used for content blocks, because GitHub paints those on the viewer's theme
background and they turn dark for anyone reading in dark mode.

Cards use a glassmorphism treatment: a near-white vertical gradient, a soft
navy drop shadow, a hairline border, and a bright inner highlight along the
top edge. Links are rendered as these glass cards and wrapped in `<a>` tags in
README.md so they stay clickable and open in a new tab.
"""

from __future__ import annotations

import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
LOGO_SVG = ASSETS / "dh-logo.svg"

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

WHITE = "#FFFFFF"
INK = "#0A162C"
NAVY = "#13294B"
NAVY_SOFT = "#2C4C7C"
BLUE = "#4B9CD3"
BLUE_DEEP = "#3D7FB5"
BLUE_LIGHT = "#9ACEE7"
BLUE_PALE = "#C9E4F3"
MIST = "#EDF3F9"
LINE = "#E3E7EE"
LINE_GLASS = "#DCE6F2"
MUTED = "#6B7A93"

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

# Nothing in this system may start hidden. GitHub renders these files through an
# HTML <img> element, and a card that begins at opacity:0 can be painted before
# its animation ever advances, which reads as a blank card.
BASE_CSS = f"""
    text {{ font-family: {SANS}; }}
    .mono {{ font-family: {MONO}; }}
    .eyebrow {{ font-family: {MONO}; font-size: 10px; letter-spacing: 2.4px; fill: {MUTED}; }}
    .rule {{ stroke: {LINE}; stroke-width: 1; }}
    .pulse {{ animation: pulse 3.2s ease-in-out infinite; }}
    @keyframes pulse {{ 0%,100% {{ opacity:1 }} 50% {{ opacity:.35 }} }}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; opacity: 1 !important; }}
    }}
"""


def glass_defs(uid: str = "g") -> str:
    """Gradients, highlight, and shadow that give the cards their glass feel."""
    return f"""<defs>
  <linearGradient id="{uid}Face" x1="0" y1="0" x2=".25" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/>
    <stop offset=".52" stop-color="#F8FBFE"/>
    <stop offset="1" stop-color="#EDF3FA"/>
  </linearGradient>
  <linearGradient id="{uid}Edge" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{BLUE}" stop-opacity=".85"/>
    <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="{uid}Accent" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BLUE_LIGHT}"/>
    <stop offset="1" stop-color="{NAVY}"/>
  </linearGradient>
  <linearGradient id="{uid}Gloss" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset=".5" stop-color="#FFFFFF" stop-opacity=".95"/>
    <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <filter id="{uid}Shadow" x="-12%" y="-24%" width="124%" height="156%">
    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="{NAVY}" flood-opacity=".10"/>
  </filter>
</defs>"""


# ---------------------------------------------------------------------------
# Text metrics (Helvetica/Arial advance widths, per 1000 units)
# ---------------------------------------------------------------------------

_ADVANCE = {
    " ": 278, "!": 278, '"': 355, "#": 556, "$": 556, "%": 889, "&": 667,
    "'": 191, "(": 333, ")": 333, "*": 389, "+": 584, ",": 278, "-": 333,
    ".": 278, "/": 278, ":": 278, ";": 278, "<": 584, "=": 584, ">": 584,
    "?": 556, "@": 1015, "[": 278, "\\": 278, "]": 278, "_": 556, "|": 260,
    "A": 667, "B": 667, "C": 722, "D": 722, "E": 667, "F": 611, "G": 778,
    "H": 722, "I": 278, "J": 500, "K": 667, "L": 556, "M": 833, "N": 722,
    "O": 778, "P": 667, "Q": 778, "R": 722, "S": 667, "T": 611, "U": 722,
    "V": 667, "W": 944, "X": 667, "Y": 667, "Z": 611,
    "a": 556, "b": 556, "c": 500, "d": 556, "e": 556, "f": 278, "g": 556,
    "h": 556, "i": 222, "j": 222, "k": 500, "l": 222, "m": 833, "n": 556,
    "o": 556, "p": 556, "q": 556, "r": 333, "s": 500, "t": 278, "u": 556,
    "v": 500, "w": 722, "x": 500, "y": 500, "z": 500,
    "·": 333, "—": 1000, "–": 556, "’": 191, "→": 800,
    "↗": 800, "×": 584,
}
_DIGIT = 556


def text_width(value: str, size: float, bold: bool = False,
               tracking: float = 0.0) -> float:
    """Estimated rendered width. Deliberately runs a few percent wide so that
    wrapped copy never collides with the card edge."""
    total = 0.0
    for char in value:
        total += _ADVANCE.get(char, _DIGIT if char.isdigit() else 556)
    width = total / 1000.0 * size
    if bold:
        width *= 1.06
    return width + tracking * len(value)


def wrap(value: str, size: float, max_width: float, bold: bool = False) -> list[str]:
    """Greedy word wrap against the estimated metrics above."""
    lines: list[str] = []
    current = ""
    for word in value.split():
        candidate = f"{current} {word}".strip()
        if current and text_width(candidate, size, bold) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------

def svg(width: float, height: float, label: str, body: str,
        extra_css: str = "", uid: str = "g") -> str:
    """A white-backed SVG document. The base rect is what keeps every section
    of the README white regardless of the viewer's GitHub theme."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_n(width)} {_n(height)}" width="{_n(width)}" height="{_n(height)}" role="img" aria-label="{escape(label)}">
<title>{escape(label)}</title>
{glass_defs(uid)}
<style>{BASE_CSS}{extra_css}</style>
<rect width="{_n(width)}" height="{_n(height)}" fill="{WHITE}"/>
{body}
</svg>"""


def glass(x: float, y: float, w: float, h: float, rx: float = 16,
          uid: str = "g", accent: bool = True, gloss: bool = True) -> str:
    """One glass panel: shadowed face, hairline border, top highlight, and an
    optional carolina-to-navy accent rail down the left edge."""
    parts = [
        f'<rect x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(h)}" rx="{_n(rx)}" '
        f'fill="url(#{uid}Face)" filter="url(#{uid}Shadow)"/>',
        f'<rect x="{_n(x + .5)}" y="{_n(y + .5)}" width="{_n(w - 1)}" height="{_n(h - 1)}" '
        f'rx="{_n(rx - .5)}" fill="none" stroke="{LINE_GLASS}" stroke-width="1"/>',
    ]
    if gloss:
        parts.append(
            f'<rect x="{_n(x + rx)}" y="{_n(y + 1)}" width="{_n(w - rx * 2)}" height="1" '
            f'fill="url(#{uid}Gloss)"/>'
        )
    if accent:
        parts.append(
            f'<rect x="{_n(x)}" y="{_n(y + 14)}" width="3" height="{_n(h - 28)}" rx="1.5" '
            f'fill="url(#{uid}Accent)"/>'
        )
    return "".join(parts)


def pill(x: float, y: float, label: str, size: float = 11.5,
         pad: float = 14, height: float = 26, fill: str = WHITE,
         stroke: str = LINE_GLASS, color: str = NAVY, mono: bool = False,
         lead: float = 0.0) -> tuple[str, float]:
    """A bordered chip. `lead` reserves room on the left for a status dot and
    switches the label from centred to left-aligned. Returns the markup and the
    width it consumed."""
    font = MONO if mono else SANS
    width = text_width(label, size, bold=not mono) + pad * 2 + lead
    if lead:
        tx, anchor = x + pad + lead, "start"
    else:
        tx, anchor = x + width / 2, "middle"
    markup = (
        f'<g><rect x="{_n(x)}" y="{_n(y)}" width="{_n(width)}" height="{_n(height)}" '
        f'rx="{_n(height / 2)}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        f'<text x="{_n(tx)}" y="{_n(y + height / 2 + size * .36)}" '
        f'text-anchor="{anchor}" font-family="{font}" font-size="{_n(size)}" '
        f'font-weight="{600 if not mono else 500}" fill="{color}">{escape(label)}</text></g>'
    )
    return markup, width


def sweep(name: str, x: float, y: float, span: float, width: float = 130,
          seconds: float = 6.0, thickness: float = 2, uid: str = "g") -> tuple[str, str]:
    """A carolina highlight that travels along a rule. Percentages are avoided
    in the keyframes because CSS percentage transforms on SVG elements depend on
    `transform-box`, which is inconsistent inside an <img> element."""
    css = (f"\n    .{name} {{ animation: {name} {seconds}s linear infinite; }}"
           f"\n    @keyframes {name} {{ from {{ transform: translateX(0) }} "
           f"to {{ transform: translateX({_n(span + width)}px) }} }}")
    # Clipped to the rule it travels along, so the highlight never bleeds into
    # the page margin.
    markup = (f'<clipPath id="{name}Clip"><rect x="{_n(x)}" y="{_n(y - 2)}" '
              f'width="{_n(span)}" height="{_n(thickness + 4)}"/></clipPath>'
              f'<g clip-path="url(#{name}Clip)"><g class="{name}">'
              f'<rect x="{_n(x - width)}" y="{_n(y)}" width="{_n(width)}" '
              f'height="{_n(thickness)}" fill="url(#{uid}Edge)"/></g></g>')
    return markup, css


def status_dot(cx: float, cy: float, color: str = BLUE, r: float = 3.5) -> str:
    return (f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="{_n(r + 3)}" fill="{color}" opacity=".16"/>'
            f'<circle class="pulse" cx="{_n(cx)}" cy="{_n(cy)}" r="{_n(r)}" fill="{color}"/>')


def arrow(x: float, y: float, size: float = 13, color: str = BLUE) -> str:
    """The outbound-link glyph used on every clickable card."""
    return (f'<text x="{_n(x)}" y="{_n(y)}" text-anchor="end" font-family="{MONO}" '
            f'font-size="{_n(size)}" font-weight="700" fill="{color}">&#8599;</text>')


def logo_paths() -> str:
    """Inline the traced monogram so the hero has no external dependency."""
    source = LOGO_SVG.read_text(encoding="utf-8")
    return "".join(re.findall(r"<path\b[^>]*/>", source))


LOGO_VIEW_W = 356.0
LOGO_VIEW_H = 192.0
LOGO_MARK_H = 146.0  # height of the "DH" letterforms, ignoring the swoosh


def _n(value: float) -> str:
    """Trim trailing zeros so the generated markup stays readable."""
    text = f"{float(value):.2f}".rstrip("0").rstrip(".")
    return text if text else "0"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


n = _n
