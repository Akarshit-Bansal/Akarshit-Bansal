#!/usr/bin/env python3
"""Animated neon wave divider SVG."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import theme as T

OUT = Path(__file__).resolve().parent.parent / "assets" / "wave.svg"
W, H = 880, 60


def wave_path(amp, wl, phase, mid, extra=W):
    pts = []
    x = 0
    while x <= extra + wl:
        y = mid + amp * math.sin((x / wl) * 2 * math.pi + phase)
        pts.append(f"{x:.1f},{y:.1f}")
        x += 8
    return "M" + " L".join(pts)


def build():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="divider">']
    p.append(f"<defs>{T.defs(key='w')}"
             f'<linearGradient id="wg" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{T.CYAN}" stop-opacity="0"/>'
             f'<stop offset="0.5" stop-color="{T.GREEN}"/>'
             f'<stop offset="1" stop-color="{T.MAGENTA}" stop-opacity="0"/>'
             f'</linearGradient></defs>')
    # two waves scrolling opposite directions
    for amp, wl, ph, op, dur, dirn in [(9, 220, 0, 0.9, 7, 1), (6, 160, 1.4, 0.5, 5, -1)]:
        d = wave_path(amp, wl, ph, H/2)
        p.append(f'<path d="{d}" fill="none" stroke="url(#wg)" stroke-width="2.4" '
                 f'opacity="{op}" filter="url(#gloww)">'
                 f'<animateTransform attributeName="transform" type="translate" '
                 f'from="0 0" to="{-wl*dirn} 0" dur="{dur}s" repeatCount="indefinite"/></path>')
    # center diamond node
    p.append(f'<g filter="url(#gloww)">'
             f'<path d="M{W/2-7} {H/2} L{W/2} {H/2-7} L{W/2+7} {H/2} L{W/2} {H/2+7} Z" '
             f'fill="{T.GREEN}"><animate attributeName="opacity" values="0.5;1;0.5" '
             f'dur="2s" repeatCount="indefinite"/></path></g>')
    p.append("</svg>")
    return "".join(p)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} b)")


if __name__ == "__main__":
    main()
