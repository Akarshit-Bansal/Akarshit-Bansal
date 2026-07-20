#!/usr/bin/env python3
"""Neon tech-stack chip board SVG, grouped by category, chips glow in with stagger."""
import html, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import theme as T

OUT = Path(__file__).resolve().parent.parent / "assets" / "tech-stack.svg"

GROUPS = [
    ("LANGUAGES", T.CYAN,    ["Python", "Java", "C++", "C", "C#"]),
    ("BACKEND",   T.GREEN,   ["Django", "FastAPI", "REST APIs", "Bootstrap", "HTML/CSS"]),
    ("AI / DATA", T.MAGENTA, ["AWS Bedrock", "TensorFlow", "CUDA", "OpenCV", "pandas"]),
    ("DEVOPS",    T.AMBER,   ["Docker", "Jenkins", "GitHub Actions", "CI/CD", "Git"]),
    ("CLOUD / DB", T.PURPLE, ["AWS EC2/S3", "PostgreSQL", "MySQL", "Linux"]),
]

W = 880
PAD = 24
CHIP_H = 30
GAP = 10
ROW_GAP = 16
LABEL_W = 118
FS = 13.5


def esc(s): return html.escape(s, quote=True)


def chip_w(txt): return int(len(txt) * 8.3 + 26)


def build():
    rows = []  # (label, color, [(x, w, txt)])
    y = PAD + 8
    positions = []
    for label, color, chips in GROUPS:
        x = PAD + LABEL_W
        for c in chips:
            w = chip_w(c)
            if x + w > W - PAD:
                pass  # single row per group (fits within 880)
            positions.append((label, color, x, y, w, c))
            x += w + GAP
        y += CHIP_H + ROW_GAP
    H = y + 6

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="tech stack">']
    p.append(f"<defs>{T.defs(key='t')}</defs>")
    p.append(f"""<style>
      @keyframes chip{{0%{{opacity:0;transform:translateY(8px) scale(.9)}}
        100%{{opacity:1;transform:translateY(0) scale(1)}}}}
      .chip{{opacity:0;transform-box:fill-box;transform-origin:center;
        animation:chip .45s cubic-bezier(.2,.8,.2,1) forwards}}
      text{{font-family:{T.font_stack()}}}
    </style>""")
    p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14" fill="url(#vigt)" '
             f'stroke="url(#bordert)" stroke-width="2.5" filter="url(#glowt)"/>')
    p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14" fill="url(#scant)"/>')

    # category labels (one per group row)
    seen = set()
    for label, color, x, y, w, c in positions:
        if label not in seen:
            seen.add(label)
            p.append(f'<text x="{PAD+6}" y="{y+CHIP_H/2+5}" font-size="12.5" font-weight="700" '
                     f'letter-spacing="1" fill="{color}" filter="url(#glowt)">{esc(label)}</text>')

    for i, (label, color, x, y, w, c) in enumerate(positions):
        d = 0.12 + i * 0.045
        g = (
            f'<g class="chip" style="animation-delay:{d:.2f}s">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{CHIP_H}" rx="8" '
            f'fill="{color}" opacity="0.12"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{CHIP_H}" rx="8" '
            f'fill="none" stroke="{color}" stroke-width="1.4" filter="url(#glowt)"/>'
            f'<circle cx="{x+13}" cy="{y+CHIP_H/2}" r="3.2" fill="{color}" filter="url(#glowt)"/>'
            f'<text x="{x+24}" y="{y+CHIP_H/2+5}" font-size="{FS}" fill="{T.INK}">{esc(c)}</text>'
            f'</g>'
        )
        p.append(g)
    p.append("</svg>")
    return "".join(p)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} b)")


if __name__ == "__main__":
    main()
