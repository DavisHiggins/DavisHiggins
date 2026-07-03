# Davis Higgins GitHub Profile System — Exact Setup

This folder is a complete GitHub profile README system.

It includes:

- `README.md` — the profile README GitHub will display.
- `assets/profile-hero.svg` — animated hero banner.
- `assets/terminal-card.svg` — animated terminal card.
- `assets/section-divider.svg` — animated divider.
- `data/current-focus.json` — edit this to change the Currently Building section.
- `data/projects.json` — edit this to change Featured Systems.
- `data/ship-log.json` — edit this to change Recent Ship Log.
- `scripts/update-profile.js` — regenerates dynamic README sections.
- `.github/workflows/update-profile.yml` — updates README from data files.
- `.github/workflows/generate-snake.yml` — generates the contribution snake animation.

---

## 1. Create the special GitHub profile repository

On GitHub, create a **public** repository named exactly:

```txt
DavisHiggins
```

The repository name must match your GitHub username exactly for the README to appear on your GitHub profile.

If your username is not `DavisHiggins`, rename the repo and replace every `DavisHiggins` reference in these files.

---

## 2. Add these files to the repo

### Option A — GitHub website upload

1. Open your new `DavisHiggins` repository.
2. Click **Add file**.
3. Upload the full contents of this folder.
4. Commit to `main`.

### Option B — command line

```bash
git clone https://github.com/DavisHiggins/DavisHiggins.git
cd DavisHiggins

# Copy the files from this package into this folder.
# Then run:

git add .
git commit -m "Build animated profile README system"
git push origin main
```

---

## 3. Enable workflow write access

Go to:

```txt
Repo → Settings → Actions → General → Workflow permissions
```

Choose:

```txt
Read and write permissions
```

Then click **Save**.

This allows the workflows to commit README updates and push the generated snake SVG to the `output` branch.

---

## 4. Run the workflows manually once

Open the repo on GitHub.

Go to:

```txt
Actions → Update Profile README → Run workflow
```

Then run:

```txt
Actions → Generate Contribution Snake → Run workflow
```

The snake may not show until the `output` branch exists. Running the workflow once creates it.

---

## 5. Customize the profile

Edit these files whenever you want to update the profile content:

```txt
data/current-focus.json
data/projects.json
data/ship-log.json
data/metrics.json
```

Then either:

```bash
npm run update
```

or let GitHub Actions regenerate the README automatically.

---

## 6. Replace private repo links later

In `data/projects.json`, add repo URLs when you want them public.

Example:

```json
"repo": "https://github.com/DavisHiggins/propify"
```

If you leave `repo` blank, the README shows only the live link.

---

## 7. Optional: self-host GitHub stats later

The included README uses public GitHub stats cards for simplicity. For a more professional setup, fork/self-host the stats service on Vercel and replace the stat image URLs in `README.md` with your own endpoint.

---

## 8. Design notes

Your visual system here is intentionally:

- Navy / Carolina blue / white
- Builder-dashboard themed
- Sharp but not gimmicky
- Focused on real systems, not random badges

Do not add 30 badges, random GIFs, or generic profile widgets. This profile should look like a serious builder's command center.
