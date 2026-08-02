# Davis Higgins profile implementation

`DavisHiggins/DavisHiggins` renders as an all-white, glassmorphism profile page
with a four-month contribution snake. Everything visible is generated SVG.

## Why the README is artwork instead of markdown

GitHub themes the README background and offers no repository stylesheet, so any
block left as plain markdown — prose, tables, headings — paints on the viewer's
theme background and turns dark for anyone reading in dark mode. Every section
is therefore an SVG that paints its own `#FFFFFF` base, which is what keeps the
page white end to end in both themes.

Two layout rules keep the tiled sections seamless. Both are load-bearing:

- `align="top"` on every `<img>` removes the baseline gap under an inline image.
  Without it the line-box leading shows through as a dark band between rows.
- Images that share a line must total exactly 100% with **no whitespace between
  their tags**. A single space between two 50% images pushes the second onto its
  own line. Each card file therefore carries its own white gutter rather than
  relying on HTML spacing.

Links stay real links: each card is a standalone file wrapped in an `<a>` with
`target="_blank" rel="noopener noreferrer"`, because GitHub does not make
separate regions inside one embedded SVG clickable.

## Layout

| Block | Asset | Width in README |
|---|---|---|
| Hero | `assets/hero.svg` | 100% |
| Top navigation | `assets/links/nav-*.svg` | 20% ×5 |
| Section headers | `assets/headers/NN-*.svg` | 100% |
| Profile, statistics, positions, stack | `assets/*.svg` | 100% |
| Activity | `assets/contribution-snake.svg` | 100% |
| Project and repo cards | `assets/cards/*.svg` | 50% ×2 |
| Connect cards | `assets/links/link-*.svg` | 50% ×2 |
| Divider, footer | `assets/divider.svg`, `assets/footer.svg` | 100% |

`assets/cards/spacer.svg` pairs with the thirteenth project card so that row
still ends on a full white line.

## Regenerating

```bash
python scripts/generate_profile_assets.py
```

- `scripts/profile_content.py` — all copy, links, and slugs.
- `scripts/profile_kit.py` — palette, glass primitives, text metrics, wrapping.
- `scripts/generate_profile_assets.py` — layout for each surface.

Card slugs become filenames referenced from `README.md`, so renaming a project
means updating its README link too.

## Contribution snake

`scripts/generate_contribution_snake.py` renders the animation directly rather
than using `Platane/snk`, which always draws a full year in GitHub's green. This
version covers a rolling four-month window and runs carolina blue into navy.

```bash
python scripts/generate_contribution_snake.py --user DavisHiggins --months 4 \
    --out assets/contribution-snake.svg
```

Contribution data comes from the GitHub GraphQL API when `GITHUB_TOKEN` is set
and from the public contributions fragment otherwise. `--demo` renders synthetic
data for layout checks. `.github/workflows/snake.yml` reruns it daily and commits
the result to `main`.

The snake walks a closed serpentine tour: every square row by row, then an
off-grid return leg one column left of and one row below the grid, so the loop
repeats without the body snapping across the board. `PAD_L` and `PAD_B` must both
stay wider than one `PITCH` to keep that return leg inside the viewBox. Body
segments share the head's keyframes with a negative `animation-delay`, which is
why they trail it exactly.

## Motion constraints

GitHub serves these files through an HTML `<img>`, so scripts, hover states, and
external resources do not work. Motion is ambient CSS only, and **nothing may
start hidden**: a card that begins at `opacity: 0` can be painted before its
animation advances and reads as blank. Every animated element starts in its
visible state, and every file honours `prefers-reduced-motion`.

## Brand system

| Token | Value | Use |
|---|---|---|
| Carolina Blue | `#4B9CD3` | Section numbers, accents, outbound arrows |
| Blue deep | `#3D7FB5` | Labels and secondary emphasis |
| Blue light / pale | `#9ACEE7` / `#C9E4F3` | Accent rails, contribution ramp |
| Navy | `#13294B` | Values, snake head, darkest contribution level |
| Ink | `#0A162C` | Display typography |
| Muted | `#6B7A93` | Supporting copy |
| Line / glass line | `#E3E7EE` / `#DCE6F2` | Rules and card borders |
| White | `#FFFFFF` | Every background |

Contribution levels run `#EDF3F9`, `#BFE0F2`, `#7AB7D3`, `#3D7FB5`, `#13294B`.

## Checklist before pushing

- Run both generators and confirm no unexpected diffs.
- Confirm every project URL still resolves.
- Open `README.md` in GitHub's preview on both the light and dark themes.
- Confirm the top navigation and every card open in a new tab.
- Test with reduced motion enabled.
