#!/usr/bin/env python3
"""
Neon stat cards.
  impact.svg  — real, resume-sourced achievement tiles (always accurate)
  streak.svg  — GitHub-style streak card (SAMPLE numbers for local preview;
                the README also embeds the live hosted streak card)
"""
import html, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import theme as T

ASSETS = Path(__file__).resolve().parent.parent / "assets"

IMPACT = [
    ("3,000+", "records in production MIS", T.GREEN),
    ("1,500+", "CRM customers served",      T.CYAN),
    ("~60%",   "queries auto-resolved (AI)", T.MAGENTA),
    ("239+",   "DSA problems solved",        T.AMBER),
]
STREAK = [("1,295", "Total Contributions", T.CYAN),
          ("24",    "Current Streak · days", T.GREEN),
          ("57",    "Longest Streak · days", T.MAGENTA)]


def esc(s): return html.escape(s, quote=True)


def card_frame(p, W, H, key):
    p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14" fill="url(#vig{key})" '
             f'stroke="url(#border{key})" stroke-width="2.5" filter="url(#glow{key})"/>')
    p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14" fill="url(#scan{key})"/>')


def build_impact():
    W, H = 880, 150
    n = len(IMPACT)
    tile_w = (W - 24 * 2 - 18 * (n - 1)) / n
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="impact stats">',
         f"<defs>{T.defs(key='i')}</defs>",
         f"""<style>
           @keyframes rise{{0%{{opacity:0;transform:translateY(14px)}}100%{{opacity:1;transform:translateY(0)}}}}
           @keyframes gl{{0%,100%{{opacity:.8}}50%{{opacity:1}}}}
           .tile{{opacity:0;animation:rise .6s cubic-bezier(.2,.8,.2,1) forwards}}
           .num{{animation:gl 2.6s ease-in-out infinite}}
           text{{font-family:{T.font_stack()}}}
         </style>"""]
    card_frame(p, W, H, "i")
    p.append(f'<text x="24" y="34" font-size="13" font-weight="700" letter-spacing="2" '
             f'fill="{T.DIM}">// IMPACT</text>')
    x = 24
    for i, (num, label, col) in enumerate(IMPACT):
        d = 0.15 + i * 0.12
        cx = x + tile_w / 2
        p.append(f'<g class="tile" style="animation-delay:{d:.2f}s">'
                 f'<rect x="{x}" y="52" width="{tile_w}" height="{H-72}" rx="10" '
                 f'fill="{col}" opacity="0.08"/>'
                 f'<rect x="{x}" y="52" width="{tile_w}" height="{H-72}" rx="10" '
                 f'fill="none" stroke="{col}" stroke-width="1.3" opacity="0.55"/>'
                 f'<text class="num" x="{cx}" y="98" text-anchor="middle" font-size="34" '
                 f'font-weight="800" fill="{col}" filter="url(#glowi)">{esc(num)}</text>'
                 f'<text x="{cx}" y="122" text-anchor="middle" font-size="12" '
                 f'fill="{T.INK}">{esc(label)}</text></g>')
        x += tile_w + 18
    p.append("</svg>")
    return "".join(p)


def build_streak():
    W, H = 880, 170
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="streak card">',
         f"<defs>{T.defs(key='s')}</defs>",
         f"""<style>
           @keyframes fin{{from{{opacity:0}}to{{opacity:1}}}}
           @keyframes ring{{from{{stroke-dashoffset:339}}to{{stroke-dashoffset:64}}}}
           .seg{{opacity:0;animation:fin .8s ease forwards}}
           .rng{{stroke-dasharray:339;stroke-dashoffset:339;animation:ring 1.4s .3s ease forwards}}
           text{{font-family:{T.font_stack()}}}
         </style>"""]
    card_frame(p, W, H, "s")
    col_w = W / 3
    for i, (num, label, col) in enumerate(STREAK):
        cx = col_w * i + col_w / 2
        d = 0.2 + i * 0.15
        if i == 1:  # center = ring
            r = 46
            cy = H / 2 - 8
            p.append(f'<g class="seg" style="animation-delay:{d:.2f}s">'
                     f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#16281f" stroke-width="7"/>'
                     f'<circle class="rng" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" '
                     f'stroke-width="7" stroke-linecap="round" filter="url(#glows)" '
                     f'transform="rotate(-90 {cx} {cy})"/>'
                     f'<text x="{cx}" y="{cy+2}" text-anchor="middle" font-size="30" font-weight="800" '
                     f'fill="{col}" filter="url(#glows)">{esc(num)}</text>'
                     f'<text x="{cx}" y="{H-24}" text-anchor="middle" font-size="11.5" '
                     f'fill="{T.INK}">{esc(label)}</text></g>')
        else:
            p.append(f'<g class="seg" style="animation-delay:{d:.2f}s">'
                     f'<text x="{cx}" y="{H/2-4}" text-anchor="middle" font-size="40" font-weight="800" '
                     f'fill="{col}" filter="url(#glows)">{esc(num)}</text>'
                     f'<text x="{cx}" y="{H/2+24}" text-anchor="middle" font-size="12" '
                     f'fill="{T.INK}">{esc(label)}</text></g>')
        if i < 2:
            lx = col_w * (i + 1)
            p.append(f'<line x1="{lx}" y1="34" x2="{lx}" y2="{H-34}" stroke="{T.CYAN}" '
                     f'stroke-width="1" opacity="0.25"/>')
    p.append("</svg>")
    return "".join(p)


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "impact.svg").write_text(build_impact(), encoding="utf-8")
    (ASSETS / "streak.svg").write_text(build_streak(), encoding="utf-8")
    print("wrote impact.svg + streak.svg")


if __name__ == "__main__":
    main()
