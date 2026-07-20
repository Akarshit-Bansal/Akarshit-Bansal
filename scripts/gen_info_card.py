#!/usr/bin/env python3
"""Neon-cyberpunk "neofetch" info card SVG. Rows reveal line-by-line."""
import html, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import theme as T

OUT = Path(__file__).resolve().parent.parent / "assets" / "info-card.svg"

USER, HOST = "akarshit", "mittalbooks"
ROWS = [
    ("Role",       "Python Developer · Backend & Full-Stack"),
    ("Company",    "Mittal Books  (Jun 2026 → now)"),
    ("Prev",       "Team Lead @ Siddhi Infonet"),
    ("Interned",   "Infosys · NVIDIA · Cisco"),
    ("Education",  "BCA + Diploma in Cybersecurity"),
    ("Location",   "Delhi, India"),
    ("Languages",  "Python · Java · C/C++ · C#"),
    ("Backend",    "Django · FastAPI · REST APIs"),
    ("AI / Gen",   "AWS Bedrock · TensorFlow · CUDA · OpenCV"),
    ("DevOps",     "Docker · Jenkins · GitHub Actions · CI/CD"),
    ("Cloud/DB",   "AWS EC2/S3 · PostgreSQL · MySQL"),
    ("Also",       "DSA 239+ · Cybersecurity (IAM)"),
    ("Portfolio",  "akarshit-portfolio · codebyakarshit"),
    ("Contact",    "bansalakarshit@gmail.com"),
]

W, PAD = 560, 26
TITLE_H, LINE_H = 42, 25.5
TOP = TITLE_H + 30
KEY_COL, VAL_COL = PAD + 6, PAD + 132
H = int(TOP + (len(ROWS) + 3) * LINE_H + 26)


def esc(s): return html.escape(s, quote=True)


def build():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="{esc(USER)}@{esc(HOST)}">']
    p.append(f"<defs>{T.defs(key='c')}</defs>")
    p.append(f"""<style>
      @keyframes rv{{0%{{opacity:0;transform:translateX(-10px)}}100%{{opacity:1;transform:translateX(0)}}}}
      @keyframes bl{{50%{{opacity:0}}}}
      .ln{{opacity:0;animation:rv .5s cubic-bezier(.2,.8,.2,1) forwards}}
      .cur{{animation:bl 1s step-end infinite}}
      text{{font-family:{T.font_stack()}}}
    </style>""")
    # panel
    p.append(f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="14" fill="url(#vigc)" '
             f'stroke="url(#borderc)" stroke-width="2.5" filter="url(#glowc)"/>')
    p.append(f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="14" fill="url(#scanc)"/>')
    # title bar
    p.append(f'<path d="M3 17 A14 14 0 0 1 17 3 H{W-17} A14 14 0 0 1 {W-3} 17 V{TITLE_H} H3 Z" fill="#070b12"/>')
    p.append(f'<line x1="3" y1="{TITLE_H}" x2="{W-3}" y2="{TITLE_H}" stroke="{T.CYAN}" stroke-width="1" opacity=".5"/>')
    for i, c in enumerate([T.RED, T.AMBER, T.GREEN]):
        p.append(f'<circle cx="{24+i*20}" cy="{TITLE_H/2}" r="6" fill="{c}" filter="url(#glowc)"/>')
    p.append(f'<text x="{W/2}" y="{TITLE_H/2+4}" text-anchor="middle" font-size="13" fill="{T.DIM}">'
             f'akarshit@mittalbooks: ~/whoami</text>')

    delay, y = 0.15, TOP
    p.append(f'<g class="ln" style="animation-delay:{delay:.2f}s"><text x="{KEY_COL}" y="{y}" '
             f'font-size="17" font-weight="700" filter="url(#glowc)" fill="{T.GREEN}">{esc(USER)}'
             f'<tspan fill="{T.INK}">@</tspan><tspan fill="{T.CYAN}">{esc(HOST)}</tspan></text></g>')
    y += LINE_H; delay += 0.12
    p.append(f'<g class="ln" style="animation-delay:{delay:.2f}s"><text x="{KEY_COL}" y="{y}" '
             f'font-size="15" fill="{T.MAGENTA}" opacity=".8">{esc("─"*36)}</text></g>')
    y += LINE_H; delay += 0.12
    for i, (k, v) in enumerate(ROWS):
        acc = T.ACCENTS[i % len(T.ACCENTS)]
        p.append(f'<g class="ln" style="animation-delay:{delay:.2f}s">'
                 f'<text x="{KEY_COL}" y="{y}" font-size="14.5" font-weight="700" '
                 f'filter="url(#glowc)" fill="{acc}">{esc(k)}</text>'
                 f'<text x="{VAL_COL}" y="{y}" font-size="14" fill="{T.INK}">'
                 f'<tspan fill="{T.DIM}">: </tspan>{esc(v)}</text></g>')
        y += LINE_H; delay += 0.09
    # palette blocks + cursor
    y += 6; sw = 20
    p.append(f'<g class="ln" style="animation-delay:{delay:.2f}s">')
    for i, c in enumerate([T.GREEN, T.CYAN, T.MAGENTA, T.PURPLE, T.AMBER, T.RED, T.INK, T.DIM]):
        p.append(f'<rect x="{KEY_COL+i*(sw+5)}" y="{y-15}" width="{sw}" height="{sw}" rx="4" '
                 f'fill="{c}" filter="url(#glowc)"/>')
    cx = KEY_COL + 8*(sw+5) + 6
    p.append(f'<rect class="cur" x="{cx}" y="{y-15}" width="11" height="{sw}" fill="{T.GREEN}" filter="url(#glowc)"/>')
    p.append('</g></svg>')
    return "".join(p)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} b)")


if __name__ == "__main__":
    main()
