#!/usr/bin/env python3
"""Generate every SVG surface used by the Davis Higgins profile README.

Run from the repository root:

    python scripts/generate_profile_assets.py

Design rules for this system:

* Every surface paints its own white base. GitHub themes the README background,
  so any block rendered as plain markdown turns dark for readers on the dark
  theme. Section bodies, tables, and link rows are therefore artwork, not
  markdown, and the page stays white end to end.
* Cards are glass: near-white gradient face, soft navy shadow, hairline border,
  bright top highlight, carolina-to-navy accent rail.
* Anything clickable is a standalone file so README.md can wrap it in an <a>
  that opens in a new tab.
* Motion is ambient only. Nothing starts hidden, because GitHub serves these
  through an <img> element where a card that begins at opacity:0 can paint
  blank.
"""

from __future__ import annotations

from html import escape

import profile_content as C
from profile_kit import (
    ASSETS, BLUE, BLUE_DEEP, BLUE_PALE, INK, LINE, LOGO_MARK_H, LOGO_VIEW_H,
    LOGO_VIEW_W, MIST, MONO, MUTED, NAVY, NAVY_SOFT, arrow, glass, logo_paths,
    n, pill, status_dot, svg, sweep, text_width, wrap, write,
)

PAGE = 900.0
MARGIN = 56.0
CONTENT = PAGE - MARGIN * 2  # 788


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------

def build_hero() -> None:
    """The monogram holds the card's top-right corner, where the availability
    chip used to sit."""
    height = 340.0
    name = "DAVIS HIGGINS"
    name_size = 62.0
    tracking = -2.2
    baseline = 176.0

    # Sized against the name's cap height, a little smaller than the lockup that
    # previously sat beside the wordmark, and right-aligned to the card's inner
    # edge on the chip's old centre line.
    cap = name_size * 0.716
    scale = (cap * 1.1) / LOGO_MARK_H
    logo_x = PAGE - MARGIN - 12 - LOGO_VIEW_W * scale
    logo_y = 86 - LOGO_VIEW_H * scale / 2

    beam, beam_css = sweep("heroBeam", MARGIN + 12, 203, CONTENT - 24, width=160, seconds=7)

    meta = ""
    cells = [
        ("CURRENT", "Data Analyst", "Kewaunee Scientific"),
        ("STUDIO", "Higgins Digital", "Web + brand systems"),
        ("FOCUS", "Data / AI", "Dashboards, tools, agents"),
    ]
    for i, (key, value, note) in enumerate(cells):
        x = MARGIN + 12 + i * 258
        meta += (
            f'<g><line x1="{n(x)}" y1="242" x2="{n(x + 230)}" y2="242" class="rule"/>'
            f'<text class="metaK" x="{n(x)}" y="262">{escape(key)}</text>'
            f'<text class="metaV" x="{n(x)}" y="284">{escape(value)}</text>'
            f'<text class="metaS" x="{n(x)}" y="303">{escape(note)}</text></g>'
        )

    tagline = ("Data Analyst | Data Science &amp; AI | Python, SQL, Power BI, "
               "Machine Learning | Web Development &amp; Digital Solutions")
    body = f"""
{glass(MARGIN * .5, 20, PAGE - MARGIN, height - 44, rx=22)}
<text class="eyebrow" x="{n(MARGIN + 12)}" y="86">CHARLOTTE, NORTH CAROLINA</text>
<text class="name" x="{n(MARGIN + 12)}" y="{n(baseline)}">{escape(name)}</text>
<g class="logo" transform="translate({n(logo_x)},{n(logo_y)}) scale({n(scale)})">{logo_paths()}</g>
<line class="sweepline" x1="{n(MARGIN + 12)}" y1="204" x2="{n(PAGE - MARGIN - 12)}" y2="204"/>
{beam}
<text class="tag" x="{n(MARGIN + 12)}" y="228">{tagline}</text>
{meta}
"""
    css = f"""
    .name {{ font-size:{n(name_size)}px; font-weight:800; letter-spacing:{n(tracking)}px; fill:{INK}; }}
    .tag {{ font-size:14px; fill:{NAVY_SOFT}; }}
    .logo {{ animation: logo 3.2s ease-in-out infinite; }}
    @keyframes logo {{ 0%,100% {{ opacity:1 }} 50% {{ opacity:.45 }} }}
    .sweepline {{ stroke:{NAVY}; stroke-width:2; }}
    .metaK {{ font-family:{MONO}; font-size:9px; letter-spacing:2.2px; fill:{MUTED}; }}
    .metaV {{ font-size:14px; font-weight:700; fill:{NAVY}; }}
    .metaS {{ font-size:12px; fill:{MUTED}; }}{beam_css}
"""
    write(ASSETS / "hero.svg",
          svg(PAGE, height, "Davis Higgins - Data Analyst; Data Science and AI; Python, SQL, "
                            "Power BI, Machine Learning; Web Development and Digital Solutions",
              body, css))


# ---------------------------------------------------------------------------
# Section headers
# ---------------------------------------------------------------------------

def build_headers() -> None:
    """Oversized numerals and titles. Both are roughly three times the size of
    the small caps headers they replace."""
    for number, title, caption in C.SECTIONS:
        height = 138.0
        num_size = 58.0
        title_size = 40.0
        num_w = text_width(number, num_size, bold=True, tracking=-2)
        divider_x = MARGIN + num_w + 26
        title_x = divider_x + 26
        beam, beam_css = sweep("hdrBeam", MARGIN, 118, CONTENT, width=140, seconds=6.5)
        body = f"""
<text class="num" x="{n(MARGIN)}" y="98">{escape(number)}</text>
<line class="split" x1="{n(divider_x)}" y1="44" x2="{n(divider_x)}" y2="106"/>
<text class="title" x="{n(title_x)}" y="98">{escape(title)}</text>
<text class="cap" x="{n(PAGE - MARGIN)}" y="98" text-anchor="end">{escape(caption)}</text>
<line x1="{n(MARGIN)}" y1="118" x2="{n(PAGE - MARGIN)}" y2="118" class="rule"/>
{beam}
"""
        css = f"""
    .num {{ font-size:{n(num_size)}px; font-weight:800; letter-spacing:-2px; fill:{BLUE}; }}
    .title {{ font-size:{n(title_size)}px; font-weight:800; letter-spacing:1.5px; fill:{INK}; }}
    .split {{ stroke:{LINE}; stroke-width:2; }}
    .cap {{ font-family:{MONO}; font-size:10px; letter-spacing:1.6px; fill:{MUTED}; }}{beam_css}
"""
        write(ASSETS / "headers" / f"{number}-{title.lower()}.svg",
              svg(PAGE, height, f"Section {number} - {title}: {caption}", body, css))


# ---------------------------------------------------------------------------
# 01 Profile
# ---------------------------------------------------------------------------

def build_profile() -> None:
    panel_w = 500.0
    facts_x = MARGIN + panel_w + 20
    facts_w = PAGE - MARGIN - facts_x
    pad = 30.0
    prose_w = panel_w - pad * 2
    size, leading, gap = 14.5, 23.0, 18.0

    lines: list[tuple[str, bool]] = []
    for i, paragraph in enumerate(C.PROFILE_PARAGRAPHS):
        for j, line in enumerate(wrap(paragraph, size, prose_w)):
            lines.append((line, i == 0))
            del j
        if i < len(C.PROFILE_PARAGRAPHS) - 1:
            lines.append(("", False))

    text_h = sum(leading if line else gap for line, _ in lines)
    panel_h = max(300.0, 34 + text_h + 26)
    height = panel_h + 48

    prose = ""
    y = 34 + 24.0
    for line, lead in lines:
        if line:
            prose += (f'<text class="{"lead" if lead else "body"}" x="{n(MARGIN + pad)}" '
                      f'y="{n(y)}">{escape(line)}</text>')
            y += leading
        else:
            y += gap

    fact_h = (panel_h - 3 * 14) / 4
    facts = ""
    for i, (key, value, note) in enumerate(C.PROFILE_FACTS):
        fy = 24 + i * (fact_h + 14)
        facts += (
            glass(facts_x, fy, facts_w, fact_h, rx=14)
            + f'<text class="factK" x="{n(facts_x + 22)}" y="{n(fy + 28)}">{escape(key)}</text>'
            + f'<text class="factV" x="{n(facts_x + 22)}" y="{n(fy + 50)}">{escape(value)}</text>'
            + f'<text class="factN" x="{n(facts_x + 22)}" y="{n(fy + 68)}">{escape(note)}</text>'
        )

    body = f"""
{glass(MARGIN, 24, panel_w, panel_h, rx=18)}
{prose}
{facts}
"""
    css = f"""
    .lead {{ font-size:{n(size)}px; font-weight:600; fill:{INK}; }}
    .body {{ font-size:{n(size)}px; fill:{NAVY_SOFT}; }}
    .factK {{ font-family:{MONO}; font-size:9px; letter-spacing:2px; fill:{MUTED}; }}
    .factV {{ font-size:15px; font-weight:700; fill:{NAVY}; }}
    .factN {{ font-size:11.5px; fill:{MUTED}; }}
"""
    write(ASSETS / "profile.svg",
          svg(PAGE, height, "Profile: data analyst, AI builder, and web developer "
                            "based in Charlotte, North Carolina", body, css))


# ---------------------------------------------------------------------------
# 02 Statistics
# ---------------------------------------------------------------------------

def build_statistics() -> None:
    cols, gap = 3, 19.0
    card_w = (CONTENT - gap * (cols - 1)) / cols
    card_h, row_gap = 116.0, 18.0
    rows = (len(C.STATISTICS) + cols - 1) // cols
    height = 24 + rows * card_h + (rows - 1) * row_gap + 24

    cards = ""
    for i, (number, label, note) in enumerate(C.STATISTICS):
        x = MARGIN + (i % cols) * (card_w + gap)
        y = 24 + (i // cols) * (card_h + row_gap)
        cards += (
            glass(x, y, card_w, card_h, rx=16)
            + f'<text class="num" x="{n(x + 26)}" y="{n(y + 58)}">{escape(number)}</text>'
            + f'<line x1="{n(x + 26)}" y1="{n(y + 72)}" x2="{n(x + card_w - 26)}" '
              f'y2="{n(y + 72)}" class="rule"/>'
            + f'<text class="lab" x="{n(x + 26)}" y="{n(y + 90)}">{escape(label)}</text>'
            + f'<text class="sub" x="{n(x + 26)}" y="{n(y + 106)}">{escape(note)}</text>'
        )

    css = f"""
    .num {{ font-size:38px; font-weight:800; letter-spacing:-1.4px; fill:{NAVY}; }}
    .lab {{ font-family:{MONO}; font-size:9.5px; letter-spacing:1.6px; fill:{BLUE_DEEP}; }}
    .sub {{ font-size:11.5px; fill:{MUTED}; }}
"""
    write(ASSETS / "statistics.svg",
          svg(PAGE, height, "Statistics: 3.89 GPA, five-time Chancellor's List, 10 active "
                            "projects, 20+ dashboards, 15+ websites, class of 2027",
              cards, css))


# ---------------------------------------------------------------------------
# 04 Work / 05 Repositories
# ---------------------------------------------------------------------------

# Two cards fill one line at width="50%", so each file is exactly half the page
# and carries its own white gutter. That is what stops the viewer's dark theme
# from showing through as a seam between cards.
CARD_W = PAGE / 2          # 450
GUTTER = 64.0              # white space between the two cards on a line
CARD_X = GUTTER / 2        # keeps the outer and inner gutters equal
CARD_INNER = CARD_W - GUTTER
VPAD = 20.0                # half the white space between stacked rows


def build_project_cards() -> None:
    for slug, index, name, kind, description, stack, status, url in C.PROJECTS:
        del url
        card_h = 136.0
        height = card_h + VPAD * 2
        left, right = CARD_X + 26, CARD_X + CARD_INNER - 26
        chip, chip_w = pill(0, 0, status, size=9, pad=11, height=21,
                            fill=MIST, stroke=BLUE_PALE, color=BLUE_DEEP, mono=True)
        desc = wrap(description, 12, right - left - 12)[:2]
        desc_markup = "".join(
            f'<text class="desc" x="{n(left)}" y="{n(VPAD + 78 + i * 15)}">{escape(line)}</text>'
            for i, line in enumerate(desc)
        )
        body = f"""
{glass(CARD_X, VPAD, CARD_INNER, card_h, rx=16)}
<text class="kind" x="{n(left)}" y="{n(VPAD + 26)}">{escape(index)} &#183; {escape(kind)}</text>
<g transform="translate({n(right - chip_w)},{n(VPAD + 12)})">{chip}</g>
<text class="name" x="{n(left)}" y="{n(VPAD + 58)}">{escape(name)}</text>
{desc_markup}
<line x1="{n(left)}" y1="{n(VPAD + 106)}" x2="{n(right)}" y2="{n(VPAD + 106)}" class="rule"/>
<text class="stack" x="{n(left)}" y="{n(VPAD + 126)}">{escape(stack)}</text>
{arrow(right, VPAD + 126, 12)}
"""
        css = f"""
    .kind {{ font-family:{MONO}; font-size:9.5px; letter-spacing:1.8px; fill:{BLUE_DEEP}; }}
    .name {{ font-size:20px; font-weight:800; letter-spacing:-.4px; fill:{INK}; }}
    .desc {{ font-size:12px; fill:{MUTED}; }}
    .stack {{ font-family:{MONO}; font-size:9.5px; letter-spacing:1.2px; fill:{NAVY_SOFT}; }}
"""
        write(ASSETS / "cards" / f"work-{index}-{slug}.svg",
              svg(CARD_W, height, f"{name} - {description} Stack: {stack}. Status: {status}.",
                  body, css))


def build_repo_cards() -> None:
    for slug, name, description, url in C.REPOS:
        del url
        card_h = 104.0
        height = card_h + VPAD * 2
        left, right = CARD_X + 26, CARD_X + CARD_INNER - 26
        desc = wrap(description, 11.5, right - left)[:2]
        desc_markup = "".join(
            f'<text class="desc" x="{n(left)}" y="{n(VPAD + 72 + i * 15)}">{escape(line)}</text>'
            for i, line in enumerate(desc)
        )
        body = f"""
{glass(CARD_X, VPAD, CARD_INNER, card_h, rx=16)}
<text class="kind" x="{n(left)}" y="{n(VPAD + 26)}">REPOSITORY</text>
{arrow(right, VPAD + 27, 12)}
<text class="name" x="{n(left)}" y="{n(VPAD + 52)}">{escape(name)}</text>
{desc_markup}
"""
        css = f"""
    .kind {{ font-family:{MONO}; font-size:9.5px; letter-spacing:1.8px; fill:{BLUE_DEEP}; }}
    .name {{ font-family:{MONO}; font-size:15px; font-weight:700; fill:{INK}; }}
    .desc {{ font-size:11.5px; fill:{MUTED}; }}
"""
        write(ASSETS / "cards" / f"repo-{slug}.svg",
              svg(CARD_W, height, f"{name} on GitHub - {description}", body, css))


# ---------------------------------------------------------------------------
# 06 Positions
# ---------------------------------------------------------------------------

def build_positions() -> None:
    row_h, gap = 92.0, 16.0
    height = 24 + len(C.POSITIONS) * row_h + (len(C.POSITIONS) - 1) * gap + 24
    split = MARGIN + 400.0

    rows = ""
    for i, (when, role, org, detail) in enumerate(C.POSITIONS):
        y = 24 + i * (row_h + gap)
        lines = wrap(detail, 12, PAGE - MARGIN - split - 30)[:2]
        detail_markup = "".join(
            f'<text class="desc" x="{n(split)}" y="{n(y + 48 + j * 16)}">{escape(line)}</text>'
            for j, line in enumerate(lines)
        )
        rows += (
            glass(MARGIN, y, CONTENT, row_h, rx=16)
            + status_dot(MARGIN + 30, y + 30, BLUE, 3)
            + f'<text class="when" x="{n(MARGIN + 46)}" y="{n(y + 34)}">{escape(when)}</text>'
            + f'<text class="role" x="{n(MARGIN + 30)}" y="{n(y + 62)}">{escape(role)}</text>'
            + f'<text class="org" x="{n(MARGIN + 30)}" y="{n(y + 80)}">{escape(org)}</text>'
            + f'<line x1="{n(split - 26)}" y1="{n(y + 22)}" x2="{n(split - 26)}" '
              f'y2="{n(y + row_h - 22)}" class="rule"/>'
            + detail_markup
        )

    css = f"""
    .when {{ font-family:{MONO}; font-size:9.5px; letter-spacing:1.8px; fill:{MUTED}; }}
    .role {{ font-size:17px; font-weight:700; fill:{INK}; }}
    .org {{ font-size:13px; font-weight:600; fill:{BLUE_DEEP}; }}
    .desc {{ font-size:12px; fill:{MUTED}; }}
"""
    summary = "; ".join(f"{role} at {org}" for _, role, org, _ in C.POSITIONS)
    write(ASSETS / "positions.svg",
          svg(PAGE, height, f"Current positions: {summary}", rows, css))


# ---------------------------------------------------------------------------
# 07 Stack
# ---------------------------------------------------------------------------

def build_stack() -> None:
    pad, pill_h, pill_gap, row_gap = 28.0, 28.0, 9.0, 10.0
    inner = CONTENT - pad * 2
    panels, y = "", 24.0
    for title, items in C.STACK:
        chips, cx, cy, rows = "", 0.0, 0.0, 1
        for item in items:
            markup, width = pill(0, 0, item, size=12, pad=15, height=pill_h)
            if cx and cx + width > inner:
                cx, cy, rows = 0.0, cy + pill_h + row_gap, rows + 1
            chips += (f'<g transform="translate({n(MARGIN + pad + cx)},'
                      f'{n(y + 46 + cy)})">{markup}</g>')
            cx += width + pill_gap
        panel_h = 46 + rows * pill_h + (rows - 1) * row_gap + 22
        panels += (
            glass(MARGIN, y, CONTENT, panel_h, rx=16)
            + f'<text class="grp" x="{n(MARGIN + pad)}" y="{n(y + 30)}">{escape(title)}</text>'
            + f'<line x1="{n(MARGIN + pad)}" y1="{n(y + 38)}" x2="{n(PAGE - MARGIN - pad)}" '
              f'y2="{n(y + 38)}" class="rule"/>'
            + chips
        )
        y += panel_h + 16

    css = f"""
    .grp {{ font-family:{MONO}; font-size:10px; letter-spacing:2px; fill:{BLUE_DEEP}; }}
"""
    write(ASSETS / "stack.svg",
          svg(PAGE, y + 8, "Stack: data and analytics, AI and automation, frontend, "
                           "backend and platforms, design and strategy", panels, css))


# ---------------------------------------------------------------------------
# Links: top navigation and the connect grid
# ---------------------------------------------------------------------------

def build_nav_buttons() -> None:
    """Five buttons fill one line at width="20%", so each file is a fifth of the
    page. Equal outer and inner gutters fall out of that pitch."""
    w, h = PAGE / 5, 64.0
    inner, x = 140.0, (PAGE / 5 - 140.0) / 2
    for slug, label, detail, url in C.NAV:
        del url
        body = f"""
{glass(x, 12, inner, 40, rx=13, accent=False)}
{status_dot(x + 16, 32, BLUE, 2.6)}
<text class="lab" x="{n(x + 28)}" y="36">{escape(label)}</text>
{arrow(x + inner - 12, 36, 10)}
"""
        css = f"""
    .lab {{ font-size:12.5px; font-weight:700; letter-spacing:.2px; fill:{NAVY}; }}
"""
        write(ASSETS / "links" / f"nav-{slug}.svg",
              svg(w, h, f"{label} - {detail}", body, css))


def build_connect_cards() -> None:
    for slug, label, value, url in C.CONNECT:
        del url
        card_h = 88.0
        height = card_h + VPAD * 2
        left, right = CARD_X + 26, CARD_X + CARD_INNER - 26
        body = f"""
{glass(CARD_X, VPAD, CARD_INNER, card_h, rx=16)}
<text class="lab" x="{n(left)}" y="{n(VPAD + 30)}">{escape(label)}</text>
<text class="val" x="{n(left)}" y="{n(VPAD + 58)}">{escape(value)}</text>
{arrow(right, VPAD + 50, 15)}
"""
        css = f"""
    .lab {{ font-family:{MONO}; font-size:9.5px; letter-spacing:2.2px; fill:{MUTED}; }}
    .val {{ font-size:16px; font-weight:700; fill:{NAVY}; }}
"""
        write(ASSETS / "links" / f"link-{slug}.svg",
              svg(CARD_W, height, f"{label}: {value}", body, css))


def build_spacer() -> None:
    """Pairs with the odd card out so its row still ends on a full white line."""
    write(ASSETS / "cards" / "spacer.svg",
          svg(CARD_W, 176, "Spacer", "", uid="s"))


# ---------------------------------------------------------------------------
# Divider and footer
# ---------------------------------------------------------------------------

def build_divider() -> None:
    height = 40.0
    ticks = ""
    x = MARGIN
    step = 0
    while x <= PAGE - MARGIN:
        tall = step % 4 == 0
        ticks += (f'<rect class="tick" x="{n(x)}" y="{n(15 if tall else 18)}" width="1" '
                  f'height="{n(10 if tall else 4)}"/>')
        x += 8
        step += 1
    beam, beam_css = sweep("divBeam", MARGIN, 15, CONTENT, width=120, seconds=6)
    css = f"""
    .tick {{ fill:{LINE}; }}{beam_css}
"""
    write(ASSETS / "divider.svg", svg(PAGE, height, "Divider", ticks + beam, css))


def build_footer() -> None:
    height, panel_h = 210.0, 162.0
    words = [("Think.", INK), ("Build.", INK), ("Test.", INK), ("Ship.", NAVY)]
    markup, x = "", MARGIN + 34
    for word, color in words:
        markup += (f'<text class="word" x="{n(x)}" y="98" fill="{color}">{escape(word)}</text>')
        x += text_width(word, 42, bold=True, tracking=-1.4) + 26
    body = f"""
{glass(MARGIN, 24, CONTENT, panel_h, rx=20)}
{markup}
<rect class="caret" x="{n(x - 14)}" y="70" width="12" height="30"/>
<line x1="{n(MARGIN + 34)}" y1="126" x2="{n(PAGE - MARGIN - 34)}" y2="126" class="rule"/>
<text class="mail" x="{n(MARGIN + 34)}" y="152">davishiggins@icloud.com</text>
<text class="cap" x="{n(PAGE - MARGIN - 34)}" y="152" text-anchor="end">CHARLOTTE, NC &#183; davishiggins.com</text>
"""
    css = f"""
    .word {{ font-size:42px; font-weight:800; letter-spacing:-1.4px; }}
    .caret {{ fill:{BLUE}; animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 0%,50% {{ opacity:1 }} 51%,100% {{ opacity:0 }} }}
    .mail {{ font-family:{MONO}; font-size:13px; fill:{NAVY}; }}
    .cap {{ font-family:{MONO}; font-size:9.5px; letter-spacing:2px; fill:{MUTED}; }}
"""
    write(ASSETS / "footer.svg", svg(PAGE, height, "Think. Build. Test. Ship.", body, css))


def prune_retired_assets() -> None:
    for name in ["about.svg", "system-map.svg", "current-positions.svg",
                 "statistics-overview.svg", "experience.svg"]:
        (ASSETS / name).unlink(missing_ok=True)
    for stale in ASSETS.glob("nav-*.svg"):
        stale.unlink()
    legacy = ASSETS / "project-cards"
    if legacy.is_dir():
        for stale in legacy.glob("*.svg"):
            stale.unlink()
        legacy.rmdir()


def main() -> None:
    build_hero()
    build_headers()
    build_profile()
    build_statistics()
    build_project_cards()
    build_repo_cards()
    build_positions()
    build_stack()
    build_nav_buttons()
    build_connect_cards()
    build_spacer()
    build_divider()
    build_footer()
    prune_retired_assets()
    print(f"Generated profile assets in {ASSETS}")


if __name__ == "__main__":
    main()
