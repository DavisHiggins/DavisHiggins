# TASK: Implement Davis Higgins Animated GitHub Profile README

You are working inside the GitHub profile repository for Davis Higgins.

Repository name must be exactly:

```txt
DavisHiggins
```

The goal is to create a polished, animated, professional GitHub profile README that feels like a builder dashboard for Davis Higgins.

## Brand direction

Use this visual identity:

- Dark navy background
- Carolina blue accent
- White text
- Clean dashboard-like layout
- Professional, premium, not childish
- No generic copy-paste developer profile clutter

Core positioning:

```txt
Davis Higgins
Data Science × AI × Web Systems
Building sharper systems for smarter decisions.
```

## Required files

Create or verify these files:

```txt
README.md
assets/profile-hero.svg
assets/terminal-card.svg
assets/section-divider.svg
data/current-focus.json
data/projects.json
data/ship-log.json
data/metrics.json
scripts/update-profile.js
.github/workflows/update-profile.yml
.github/workflows/generate-snake.yml
package.json
.gitignore
SETUP.md
```

## README requirements

The README must include:

1. Animated SVG hero banner at top.
2. Centered positioning line.
3. Links to:
   - davishiggins.com
   - higginsd.com
   - propifyai.davishiggins.com
   - dhiggi15@charlotte.edu
4. Branded badges only. Do not overload the page.
5. Animated terminal intro card.
6. System Status terminal block.
7. Dynamic Currently Building table between markers:

```md
<!-- CURRENT_FOCUS:START -->
...
<!-- CURRENT_FOCUS:END -->
```

8. Dynamic Featured Systems table between markers:

```md
<!-- FEATURED_PROJECTS:START -->
...
<!-- FEATURED_PROJECTS:END -->
```

9. Build Stack section.
10. Operating Principles section.
11. Dynamic Recent Ship Log section between markers:

```md
<!-- SHIP_LOG:START -->
...
<!-- SHIP_LOG:END -->
```

12. GitHub activity cards.
13. Contribution snake image using raw.githubusercontent.com output branch URLs.
14. Final Connect section.

## Automation requirements

### update-profile.yml

This workflow should:

- Run manually with `workflow_dispatch`.
- Run daily on a UTC cron schedule.
- Run on pushes to `data/**`, `scripts/**`, `README.md`, and the workflow itself.
- Use `permissions: contents: write`.
- Checkout repo.
- Set up Node 20.
- Run `npm run update`.
- Commit changed `README.md` only if the file changed.

### generate-snake.yml

This workflow should:

- Run manually with `workflow_dispatch`.
- Run daily on a UTC cron schedule.
- Use `permissions: contents: write`.
- Use `Platane/snk@v3`.
- Generate light and dark snake SVG files.
- Push the generated SVGs to an `output` branch.

## Dynamic script requirements

`scripts/update-profile.js` must:

- Read JSON files from `/data`.
- Regenerate only the marked README sections.
- Preserve all other README content exactly.
- Not require external npm dependencies.
- Work with Node 20.

## Important constraints

- Do not add random GIFs.
- Do not add a huge badge wall.
- Do not make the profile feel like a beginner template.
- Keep the profile tied to Davis's actual projects: Higgins Digital, Propify, DavisHiggins.com, CrownCodeAI.
- Keep the profile useful and impressive to recruiters, clients, and collaborators.

## After implementation

Tell Davis to:

1. Create the public `DavisHiggins` repo if it does not exist.
2. Push all files.
3. Enable repo workflow write permissions.
4. Run both workflows manually once.
5. Edit the JSON data files whenever he wants to update the profile.
