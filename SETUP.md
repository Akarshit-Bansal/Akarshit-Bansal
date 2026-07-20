# Neon animated profile README — setup

A terminal / cyberpunk profile built from animated SVGs that GitHub Actions
re-render every day. All animation lives *inside* the SVGs (SMIL / CSS
keyframes) because GitHub strips JavaScript and inline `style=` from READMEs.

## What's in here

```
README.md                       # the profile layout
requirements.txt                # python deps
assets/
  avi-ascii.svg                 # typing ASCII portrait          (generated)
  info-card.svg                 # neofetch info card             (generated)
  contrib-heatmap.svg           # neon contribution heatmap      (generated)
  tech-stack.svg                # tech-stack chip board          (generated)
  impact.svg                    # resume-sourced impact stats    (generated)
  streak.svg                    # streak card (local preview)    (generated)
  snake.svg                     # snake teaser                   (generated)
  wave.svg                      # animated divider               (generated)
  me.jpg                        # <-- drop YOUR photo here (optional)
scripts/
  theme.py                      # shared neon palette + SVG defs
  gen_portrait.py  gen_info_card.py  gen_heatmap.py
  gen_tech_stack.py  gen_waves.py  gen_stats.py  gen_snake.py
.github/workflows/
  update-profile-art.yml        # daily cron: regenerates the SVGs above
  snake.yml                     # daily cron: real snake from your live graph
```

Some pieces are **hosted services** (they render live on GitHub, themed to
match): the typing banner, the GitHub stats card, the streak card, and the
tech-stack shield badges. Nothing to install for those.

## One-time install

1. Create a repo named **exactly** your username: `Akarshit-Bansal/Akarshit-Bansal`.
2. Copy everything in this folder into that repo.
3. **Add your photo:** put a clear, front-facing headshot at `assets/me.jpg`.
   Skip it and the portrait falls back to your GitHub avatar automatically.
4. Commit & push to `main`.
5. **Settings → Actions → General → Workflow permissions → Read and write
   permissions** (lets the Actions commit the refreshed art + push the snake).
6. **Actions** tab → run **"Update profile art"** and **"Generate contribution
   snake"** once via *Run workflow*. The first snake run creates the `output`
   branch that the README's snake image points to.

Done — the profile now shows the animated art and refreshes daily.

## Regenerate locally (optional)

```bash
pip install -r requirements.txt
export GITHUB_USER=Akarshit-Bansal

python scripts/gen_portrait.py assets/me.jpg    # or omit path to use avatar
python scripts/gen_info_card.py
python scripts/gen_heatmap.py                    # live scrape; add --sample offline
python scripts/gen_tech_stack.py
python scripts/gen_waves.py
python scripts/gen_stats.py
python scripts/gen_snake.py
```

Open `preview.html` in a browser to see the whole thing animate together.

## Customising

- **Colours / neon palette:** edit `scripts/theme.py` (one place, all SVGs).
- **Info-card text:** `ROWS` in `scripts/gen_info_card.py`.
- **Tech chips:** `GROUPS` in `scripts/gen_tech_stack.py`.
- **Impact numbers:** `IMPACT` in `scripts/gen_stats.py`.
- **Portrait detail:** `COLS`, `RAMP` in `scripts/gen_portrait.py`; set env
  `REMBG=1` (and uncomment `rembg` in requirements) to knock out the background.
- **Snake colours:** the `color_snake` / `color_dots` query params in
  `.github/workflows/snake.yml`.
- **Cron times:** the `schedule` blocks in each workflow.

## Notes / gotchas

- Keep the heatmap `width` ≈ portrait + card widths so everything lines up.
- Use `<h3>` not `<h1>/<h2>` in the README (big headers add ugly underlines).
- Auto-commit messages contain `[skip ci]` so pushes don't retrigger the job.
- The streak card in `assets/` uses sample numbers for the offline preview; the
  README embeds the **live** hosted streak card, which shows your real streak.
