#!/usr/bin/env python3
"""
A neon snake teaser that slithers across a grid, eating cells.
This is a self-contained preview effect. On the real profile the README also
wires up Platane/snk (see .github/workflows/snake.yml) for a snake built from
the user's actual contribution graph.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import theme as T

OUT = Path(__file__).resolve().parent.parent / "assets" / "snake.svg"

COLS, ROWS = 34, 7
CELL, GAP = 13, 5
LEFT, TOP = 22, 20
DUR = 9.0
BODY = 9          # snake segments (incl head)
SEG_DT = 0.10     # phase gap between segments


def build():
    W = LEFT * 2 + COLS * (CELL + GAP)
    H = TOP * 2 + ROWS * (CELL + GAP)

    # boustrophedon order of (col,row)
    order = []
    for c in range(COLS):
        rows = range(ROWS) if c % 2 == 0 else range(ROWS - 1, -1, -1)
        for r in rows:
            order.append((c, r))
    N = len(order)

    def center(c, r):
        return (LEFT + c * (CELL + GAP) + CELL / 2,
                TOP + r * (CELL + GAP) + CELL / 2)

    path = "M" + " L".join(f"{center(c,r)[0]:.1f},{center(c,r)[1]:.1f}" for c, r in order)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="contribution snake">']
    p.append(f'<defs>{T.defs(key="k")}<path id="snakepath" d="{path}"/></defs>')
    p.append(f"""<style>text{{font-family:{T.font_stack()}}}</style>""")
    p.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14" fill="url(#vigk)" '
             f'stroke="url(#borderk)" stroke-width="2" filter="url(#glowk)"/>')

    # cells — fade out as the head reaches them, reappear near loop end
    for i, (c, r) in enumerate(order):
        cx, cy = center(c, r)
        a = max(0.001, i / N * 0.9)
        a2 = min(0.93, a + 0.02)
        lvl = 0.20 + 0.8 * ((i * 37) % 5) / 5.0     # varied base brightness
        col = T.GREEN if (i % 3 == 0) else (T.CYAN if i % 3 == 1 else T.GREEN2)
        p.append(
            f'<rect x="{cx-CELL/2:.1f}" y="{cy-CELL/2:.1f}" width="{CELL}" height="{CELL}" rx="3" '
            f'fill="{col}" opacity="{lvl:.2f}">'
            f'<animate attributeName="opacity" '
            f'values="{lvl:.2f};{lvl:.2f};0.06;0.06;{lvl:.2f}" '
            f'keyTimes="0;{a:.3f};{a2:.3f};0.95;1" dur="{DUR}s" repeatCount="indefinite"/></rect>'
        )

    # snake body: trailing glowing circles following the path
    for k in range(BODY):
        begin = -(BODY - k) * SEG_DT
        rad = 7.5 if k == 0 else max(2.5, 7.0 - k * 0.6)
        if k == 0:
            col, op = T.GREEN, 1.0
        else:
            col = T.CYAN if k % 2 else T.GREEN
            op = max(0.25, 1.0 - k * 0.09)
        p.append(
            f'<circle r="{rad:.1f}" fill="{col}" opacity="{op:.2f}" filter="url(#glowk)">'
            f'<animateMotion dur="{DUR}s" begin="{begin:.2f}s" repeatCount="indefinite" '
            f'rotate="auto"><mpath href="#snakepath"/></animateMotion></circle>'
        )
    # bright eye on head
    p.append(f'<circle r="2.4" fill="#ffffff" opacity="0.9">'
             f'<animateMotion dur="{DUR}s" begin="{-BODY*SEG_DT:.2f}s" repeatCount="indefinite">'
             f'<mpath href="#snakepath"/></animateMotion></circle>')

    p.append("</svg>")
    return "".join(p)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} b)")


if __name__ == "__main__":
    main()
