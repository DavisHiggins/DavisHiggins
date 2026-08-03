#!/usr/bin/env python3
"""Render the contribution snake for the last N months of GitHub activity.

Platane/snk always draws a full year and always uses a GitHub-style palette, so
this builds the animation directly instead. The grid covers only the requested
window (four months by default) and the squares run carolina blue to navy.

    python scripts/generate_contribution_snake.py --user DavisHiggins \
        --months 4 --out assets/contribution-snake.svg

Contribution data comes from the GitHub GraphQL API when GITHUB_TOKEN is set,
and otherwise from the public contributions fragment that github.com serves for
any profile. Both paths return the same (date, level) pairs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path

WHITE = "#FFFFFF"
NAVY = "#13294B"
MUTED = "#6B7A93"
LINE = "#E3E7EE"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

# Level 0 is the empty square; 1-4 run carolina blue into navy.
LEVELS = ["#EDF3F9", "#BFE0F2", "#7AB7D3", "#3D7FB5", "#13294B"]
# Head first, then the tail fading back out to carolina blue.
SNAKE = ["#13294B", "#25507E", "#3D7FB5", "#6BA9CF", "#9ACEE7"]

CELL, GAP = 30.0, 8.0
PITCH = CELL + GAP
# PAD_T leaves room for the caption, its rule, and the month labels; PAD_L and
# PAD_B must each stay wider than one PITCH so the snake's return lane, which
# runs one column left of and one row below the grid, stays inside the viewBox.
PAD_L, PAD_T, PAD_R, PAD_B = 62.0, 84.0, 62.0, 74.0
STEP_SECONDS = 0.11
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

GRAPHQL = """query($login:String!,$from:DateTime!,$to:DateTime!){
  user(login:$login){
    contributionsCollection(from:$from,to:$to){
      contributionCalendar{
        weeks{ contributionDays{ date contributionCount } }
      }
    }
  }
}"""


def months_ago(today: date, months: int) -> date:
    month = today.month - months
    year = today.year
    while month <= 0:
        month += 12
        year -= 1
    day = min(today.day, 28)
    return date(year, month, day)


def level_for(count: int) -> int:
    if count <= 0:
        return 0
    if count <= 2:
        return 1
    if count <= 5:
        return 2
    if count <= 9:
        return 3
    return 4


def fetch_graphql(user: str, start: date, end: date, token: str) -> dict[str, int]:
    payload = json.dumps({
        "query": GRAPHQL,
        "variables": {
            "login": user,
            "from": f"{start.isoformat()}T00:00:00Z",
            "to": f"{end.isoformat()}T23:59:59Z",
        },
    }).encode()
    request = urllib.request.Request(
        "https://api.github.com/graphql", data=payload,
        headers={"Authorization": f"bearer {token}",
                 "Content-Type": "application/json",
                 "User-Agent": "davishiggins-profile"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    if "errors" in data:
        raise RuntimeError(f"GraphQL error: {data['errors']}")
    weeks = (data["data"]["user"]["contributionsCollection"]
             ["contributionCalendar"]["weeks"])
    return {day["date"]: day["contributionCount"]
            for week in weeks for day in week["contributionDays"]}


def fetch_public(user: str, start: date, end: date) -> dict[str, int]:
    """Fallback: the public calendar fragment, which carries data-level already."""
    url = (f"https://github.com/users/{user}/contributions"
           f"?from={start.isoformat()}&to={end.isoformat()}")
    request = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 davishiggins-profile"})
    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", "replace")
    counts: dict[str, int] = {}
    for cell in re.findall(r"<td[^>]*data-date=[^>]*>", html):
        day = re.search(r'data-date="([\d-]+)"', cell)
        if not day:
            continue
        level = re.search(r'data-level="(\d+)"', cell)
        counts[day.group(1)] = [0, 1, 3, 7, 14][int(level.group(1))] if level else 0
    if not counts:
        raise RuntimeError("no contribution cells found in the public calendar")
    return counts


def load_counts(user: str, start: date, end: date, demo: bool) -> dict[str, int]:
    if demo:
        cursor, counts, seed = start, {}, 7
        while cursor <= end:
            seed = (seed * 1103515245 + 12345) % 2147483648
            counts[cursor.isoformat()] = (seed >> 16) % 13 - 4
            cursor += timedelta(days=1)
        return {k: max(0, v) for k, v in counts.items()}
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        try:
            return fetch_graphql(user, start, end, token)
        except (urllib.error.URLError, RuntimeError, KeyError) as error:
            print(f"GraphQL fetch failed ({error}); falling back to the public "
                  f"calendar", file=sys.stderr)
    return fetch_public(user, start, end)


def week_start(day: date) -> date:
    """The Sunday on or before `day`. Python weeks start Monday, so shift."""
    return day - timedelta(days=(day.weekday() + 1) % 7)


def build_grid(counts: dict[str, int], first: date, end: date
               ) -> tuple[list[list[int]], list[date]]:
    """Columns are weeks starting Sunday; rows are Sunday through Saturday."""
    columns: list[list[int]] = []
    starts: list[date] = []
    cursor = first
    while cursor <= end:
        week = []
        for offset in range(7):
            day = cursor + timedelta(days=offset)
            week.append(0 if day > end else level_for(counts.get(day.isoformat(), 0)))
        columns.append(week)
        starts.append(cursor)
        cursor += timedelta(days=7)
    return columns, starts


def path_waypoints(cols: int) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """A closed serpentine tour of every square plus an off-grid return leg, so
    the loop can repeat without the body snapping across the board."""
    eaten: list[tuple[int, int]] = []
    for row in range(7):
        order = range(cols) if row % 2 == 0 else range(cols - 1, -1, -1)
        eaten.extend((col, row) for col in order)

    way = list(eaten)
    last_col = cols - 1
    way.append((last_col, 7))
    way.extend((col, 7) for col in range(last_col - 1, -2, -1))
    way.extend((-1, row) for row in range(6, -1, -1))
    way.append((0, 0))
    return way, eaten


def render(columns: list[list[int]], starts: list[date], counts: dict[str, int],
           user: str, months: int) -> str:
    cols = len(columns)
    width = PAD_L + cols * PITCH - GAP + PAD_R
    height = PAD_T + 8 * PITCH - GAP + PAD_B

    def px(col: int) -> float:
        return PAD_L + col * PITCH

    def py(row: int) -> float:
        return PAD_T + row * PITCH

    way, eaten = path_waypoints(cols)
    steps = len(way) - 1
    total = steps * STEP_SECONDS

    frames = "".join(
        f"{i / steps * 100:.4f}%{{transform:translate({px(c):.1f}px,{py(r):.1f}px)}}"
        for i, (c, r) in enumerate(way)
    )

    squares, eat_css = "", ""
    for index, (col, row) in enumerate(eaten):
        day = starts[col] + timedelta(days=row)
        count = counts.get(day.isoformat(), 0)
        contribution_word = "contribution" if count == 1 else "contributions"
        tooltip = f"{count} {contribution_word} on {day.strftime('%B')} {day.day}, {day.year}"
        level = columns[col][row]
        if level == 0:
            squares += (f'<rect x="{px(col):.1f}" y="{py(row):.1f}" width="{CELL:.0f}" '
                        f'height="{CELL:.0f}" rx="7" fill="{LEVELS[0]}">'
                        f'<title>{tooltip}</title></rect>')
            continue
        mark = index / steps * 100
        name = f"e{index}"
        squares += (f'<rect class="{name}" x="{px(col):.1f}" y="{py(row):.1f}" '
                    f'width="{CELL:.0f}" height="{CELL:.0f}" rx="7" fill="{LEVELS[level]}">'
                    f'<title>{tooltip}</title></rect>')
        eat_css += (f"\n    .{name}{{animation:{name} {total:.2f}s linear infinite}}"
                    f"\n    @keyframes {name}{{0%,{mark:.4f}%{{fill:{LEVELS[level]}}}"
                    f"{min(mark + 0.45, 100):.4f}%,100%{{fill:{LEVELS[0]}}}}}")

    body = ""
    for i, color in enumerate(SNAKE):
        inset = 0 if i == 0 else 2.5
        delay = -(total - i * STEP_SECONDS)
        body += (f'<g class="seg" style="animation-delay:{delay:.2f}s">'
                 f'<rect x="{inset:.1f}" y="{inset:.1f}" width="{CELL - inset * 2:.1f}" '
                 f'height="{CELL - inset * 2:.1f}" rx="{8 - i:.0f}" fill="{color}"/></g>')

    labels = ""
    previous = None
    for col, week_start in enumerate(starts):
        label_month = (week_start + timedelta(days=6)).month
        if label_month != previous:
            labels += (f'<text class="mo" x="{px(col):.1f}" y="{PAD_T - 18:.0f}">'
                       f'{MONTHS[label_month - 1]}</text>')
            previous = label_month

    legend_y = PAD_T + 8 * PITCH - GAP + 40
    total_count = sum(
        counts.get((starts[col] + timedelta(days=row)).isoformat(), 0)
        for col, row in eaten
    )
    legend_x = width - PAD_R - 5 * 20 - 78
    total_markup = (f'<text class="cap" x="{PAD_L:.1f}" y="{legend_y + 12:.1f}">'
                    f'{total_count} CONTRIBUTIONS</text>')
    legend = f'<text class="cap" x="{legend_x - 10:.1f}" y="{legend_y + 12:.1f}" text-anchor="end">LESS</text>'
    for i, color in enumerate(LEVELS):
        legend += (f'<rect x="{legend_x + i * 20:.1f}" y="{legend_y:.1f}" width="14" '
                   f'height="14" rx="4" fill="{color}"/>')
    legend += (f'<text class="cap" x="{legend_x + 5 * 20 + 4:.1f}" y="{legend_y + 12:.1f}">'
               f'MORE</text>')

    words = {3: "THREE", 4: "FOUR", 5: "FIVE", 6: "SIX", 12: "TWELVE"}
    span = f"PAST {words.get(months, str(months))} MONTHS"
    first_label = starts[0].strftime("%b %d").replace(" 0", " ")
    css = f"""
    text {{ font-family: {MONO}; }}
    .mo {{ font-size: 15px; letter-spacing: 1.4px; fill: {MUTED}; }}
    .cap {{ font-size: 12px; letter-spacing: 2px; fill: {MUTED}; }}
    .title {{ font-size: 13px; letter-spacing: 2.6px; fill: {NAVY}; }}
    .seg {{ animation: travel {total:.2f}s linear infinite; pointer-events:none; }}
    @keyframes travel {{ {frames} }}{eat_css}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
    }}
"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" width="{width:.0f}" height="{height:.0f}" role="img" aria-label="GitHub contribution snake for {user}, covering {first_label} to today">
<title>Contribution activity for {user} - the last {months} months</title>
<style>{css}</style>
<rect width="{width:.0f}" height="{height:.0f}" fill="{WHITE}"/>
<text class="title" x="{PAD_L:.0f}" y="34">{span}</text>
<line x1="{PAD_L:.0f}" y1="{PAD_T - 40:.0f}" x2="{width - PAD_R:.0f}" y2="{PAD_T - 40:.0f}" stroke="{LINE}" stroke-width="1"/>
{labels}
<g>{squares}</g>
<g pointer-events="none">{body}</g>
{total_markup}
{legend}
</svg>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", default="DavisHiggins")
    parser.add_argument("--months", type=int, default=4)
    parser.add_argument("--out", default="assets/contribution-snake.svg")
    parser.add_argument("--demo", action="store_true",
                        help="render from synthetic data, for local layout checks")
    args = parser.parse_args()

    end = date.today()
    first = week_start(months_ago(end, args.months))
    counts = load_counts(args.user, first, end, args.demo)
    columns, starts = build_grid(counts, first, end)

    out = Path(args.out)
    if not out.is_absolute():
        out = Path(__file__).resolve().parents[1] / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(columns, starts, counts, args.user, args.months), encoding="utf-8")
    print(f"Wrote {out} ({len(columns)} weeks, {first} to {end})")


if __name__ == "__main__":
    main()
