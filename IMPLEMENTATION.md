# Davis Higgins profile implementation

This directory is a production-ready replacement for the
`DavisHiggins/DavisHiggins` profile repository. It includes the current
`assets/dh-logo.png` brand mark and replaces the profile presentation with a
coordinated Carolina-blue SVG system.

## Included

- A complete `README.md`
- A large editorial-grotesk animated hero
- Five individually clickable contact/navigation controls
- Animated section headers, glass panels, perimeter traces, fades, pulses, scans,
  moving copy, chart growth, and system-map wires
- A system map centered on `davishiggins.com`, with the Higgins Digital branch and
  its CrownCodeAI and Higgins Digital Labs nodes
- Ten individually clickable project cards, with Cade first
- An accessible text project directory
- Statistics Overview, experience route, stack, contribution snake, and CTA footer
- Reduced-motion fallbacks in every animated SVG
- A dependency-free asset generator

## Install

1. Copy the contents of this directory into the root of
   `DavisHiggins/DavisHiggins`.
2. Confirm `assets/dh-logo.png` is present; the branded copy is included here.
3. Regenerate the SVG system if desired:

   ```bash
   python scripts/generate_profile_assets.py
   ```

4. Commit the README, generated assets, script, and workflow.
5. Push to a feature branch and open a pull request into `main`.
6. Run the **Generate contribution snake** workflow once from the Actions tab.
   It creates the `output` branch referenced by the README; after that it refreshes
   automatically each day.

## Content maintenance

The canonical project inventory lives in `PROJECTS` inside
`scripts/generate_profile_assets.py`. Edit a project's name, status, description,
stack, or URL there and rerun the generator. Project links in `README.md` must
also be updated because GitHub intentionally does not make separate regions
inside an embedded SVG clickable.

The system-map copy is intentionally link-free, as requested. Its source is the
`build_system_map()` function.

## GitHub rendering constraints

GitHub profile READMEs do not run custom JavaScript and do not provide a
repository-level stylesheet. The implementation therefore uses linked SVG assets
with internal CSS animation. This provides motion, glassmorphism, line traces,
fades, scanning effects, and text movement without unsupported runtime code.

True per-element hover animation is not reliable inside an SVG loaded through an
HTML `<img>` element on GitHub. Every project card and primary call to action is
wrapped in a normal GitHub-safe link, while the internal motion runs continuously
and respects `prefers-reduced-motion`.

## Brand system

| Token | Value | Use |
|---|---|---|
| Carolina Blue | `#7BAFD4` | Primary trace, state, and identity color |
| Ice Blue | `#C8E7FA` | Highlights, active copy, luminous edges |
| Ink | `#03070B` | Primary background |
| Panel | `#08111B` | Glass-panel base |
| White | `#F7FBFF` | Display typography |
| Muted | `#8EA2B4` | Supporting copy |
| Structural line | `#193142` | Rules, borders, and diagram scaffolding |

Display typography uses a heavy editorial grotesk stack:
`Arial Black`, `Helvetica Neue`, `Inter`, and `Arial`. Supporting copy uses a
neutral sans-serif stack, while technical labels use the system monospace stack.

## Pre-merge checklist

- Confirm every project URL still resolves.
- Confirm `assets/dh-logo.png` remains in place.
- Run the generator and verify there are no uncommitted generated changes.
- Open `README.md` in GitHub's preview.
- Trigger the snake workflow and confirm the `output` branch contains both SVGs.
- Check both light and dark GitHub themes.
- Test with reduced motion enabled.
