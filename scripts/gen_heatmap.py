#!/usr/bin/env python3
"""
Scrape a user's public GitHub contribution calendar (no token required) and
render it as an animated SVG heatmap that lights up diagonally on load.

Usage:
    python gen_heatmap.py                # scrape GITHUB_USER
    python gen_heatmap.py --sample       # render deterministic sample data
                                         # (used for local previews with no network)
"""

import os
import sys
import html
import datetime as dt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import theme as T

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "contrib-heatmap.svg"
GITHUB_USER = os.environ.get("GITHUB_USER", "Akarshit-Bansal")

# Neon green ramp (level 0..4) on a near-black page
LEVELS = ["#10251c", "#0e6b3f", "#12b866", "#22e07a", "#39ff14"]
BG = T.BG
BORDER = "#1c2a24"
DIM = T.DIM

CELL = 13          # cell size
GAP = 3            # gap between cells
RADIUS = 2
LEFT = 30          # room for weekday labels
TOP = 22           # room for month labels
WEEKS = 53
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def scrape():
    """Return list of (date, level, count) from GitHub's public HTML."""
    import requests
    from bs4 import BeautifulSoup

    url = f"https://github.com/users/{GITHUB_USER}/contributions"
    r = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0 profile-art"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    days = []
    for el in soup.select("[data-date]"):
        date = el.get("data-date")
        if not date:
            continue
        level = el.get("data-level")
        # older markup stored counts in tooltip / data-count
        count = el.get("data-count")
        if count is None:
            txt = (el.get("aria-label") or el.get_text() or "")
            count = "".join(ch for ch in txt.split(" ")[0] if ch.isdigit()) or "0"
        try:
            count = int(count)
        except ValueError:
            count = 0
        if level is None:
            level = min(4, 0 if count == 0 else 1 + min(3, (count - 1) // 3))
        days.append((date, int(level), count))
    if not days:
        raise RuntimeError("no contribution cells found in HTML")
    return days


def sample():
    """Deterministic pseudo-random calendar for offline previews."""
    today = dt.date(2026, 7, 20)
    start = today - dt.timedelta(days=WEEKS * 7 - 1)
    # align start to a Sunday
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)
    days = []
    seed = 1234567
    d = start
    while d <= today:
        seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
        r = seed / 0x7FFFFFFF
        # weekends lighter, a couple of streaky bursts
        wd = (d.weekday() + 1) % 7
        base = 0.55 if wd in (0, 6) else 1.0
        burst = 1.6 if (d.month in (3, 6) and d.day < 12) else 1.0
        v = r * base * burst
        if v < 0.35:
            lvl, cnt = 0, 0
        elif v < 0.6:
            lvl, cnt = 1, 1 + int(r * 2)
        elif v < 0.8:
            lvl, cnt = 2, 4 + int(r * 3)
        elif v < 0.93:
            lvl, cnt = 3, 7 + int(r * 4)
        else:
            lvl, cnt = 4, 12 + int(r * 8)
        days.append((d.isoformat(), lvl, cnt))
        d += dt.timedelta(days=1)
    return days


def to_grid(days):
    """Map days into (week, weekday) columns starting on Sunday."""
    days = sorted(days, key=lambda x: x[0])
    first = dt.date.fromisoformat(days[0][0])
    # column 0 begins on the Sunday on//before first day
    origin = first - dt.timedelta(days=(first.weekday() + 1) % 7)
    grid = {}
    total = 0
    month_at = {}
    for date, level, count in days:
        dd = dt.date.fromisoformat(date)
        wk = (dd - origin).days // 7
        wd = (dd.weekday() + 1) % 7
        if 0 <= wk < WEEKS:
            grid[(wk, wd)] = (level, count, date)
            total += count
            if dd.day <= 7 and wd == 0:
                month_at[wk] = dd.month
    return grid, total, month_at


def esc(s):
    return html.escape(str(s), quote=True)


def build_svg(grid, total, month_at):
    W = LEFT + WEEKS * (CELL + GAP) + 12
    H = TOP + 7 * (CELL + GAP) + 30
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-label="GitHub contribution heatmap">',
        f"<defs>{T.defs(glow_color=T.GREEN, blur=1.6, key='h')}</defs>",
        "<style>"
        "@keyframes pop{0%{opacity:0;transform:scale(.2)}"
        "60%{opacity:1;transform:scale(1.18)}100%{opacity:1;transform:scale(1)}}"
        ".cell{opacity:0;transform-box:fill-box;transform-origin:center;"
        "animation:pop .5s cubic-bezier(.2,.8,.3,1) forwards}"
        ".hot{filter:url(#glowh)}"
        f"text{{font-family:{T.font_stack()};fill:{DIM}}}"
        "</style>",
        f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="12" fill="url(#vigh)" '
        f'stroke="url(#borderh)" stroke-width="2.5" filter="url(#glowh)"/>',
    ]

    # month labels
    for wk, m in sorted(month_at.items()):
        x = LEFT + wk * (CELL + GAP)
        out.append(f'<text x="{x}" y="{TOP-8}" font-size="10">{MONTHS[m-1]}</text>')

    # weekday labels (Mon/Wed/Fri)
    for wd, lbl in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = TOP + wd * (CELL + GAP) + CELL - 2
        out.append(f'<text x="2" y="{y}" font-size="9">{lbl}</text>')

    # cells
    for wk in range(WEEKS):
        for wd in range(7):
            cell = grid.get((wk, wd))
            if cell is None:
                continue
            level, count, date = cell
            x = LEFT + wk * (CELL + GAP)
            y = TOP + wd * (CELL + GAP)
            delay = 0.15 + (wk + wd) * 0.018      # diagonal wave
            cls = "cell hot" if level >= 3 else "cell"
            out.append(
                f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                f'rx="{RADIUS}" fill="{LEVELS[level]}" '
                f'style="animation-delay:{delay:.3f}s">'
                f'<title>{esc(date)}: {esc(count)} contributions</title></rect>'
            )

    # legend + total
    ly = TOP + 7 * (CELL + GAP) + 16
    out.append(f'<text x="{LEFT}" y="{ly}" font-size="10">{total:,} contributions in the last year</text>')
    lx = W - 12 - 5 * (CELL - 2) - 60
    out.append(f'<text x="{lx-24}" y="{ly}" font-size="10">Less</text>')
    for i, c in enumerate(LEVELS):
        out.append(
            f'<rect x="{lx + i*(CELL-1)}" y="{ly-10}" width="{CELL-3}" height="{CELL-3}" '
            f'rx="2" fill="{c}"/>'
        )
    out.append(f'<text x="{lx + 5*(CELL-1) + 4}" y="{ly}" font-size="10">More</text>')

    out.append("</svg>")
    return "".join(out)


def main():
    use_sample = "--sample" in sys.argv
    try:
        days = sample() if use_sample else scrape()
        src = "sample" if use_sample else "live"
    except Exception as e:
        print(f"scrape failed ({e}); using sample data", file=sys.stderr)
        days, src = sample(), "sample-fallback"
    grid, total, month_at = to_grid(days)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_svg(grid, total, month_at), encoding="utf-8")
    print(f"wrote {OUT}  ({OUT.stat().st_size} bytes, source={src}, total={total})")


if __name__ == "__main__":
    main()
