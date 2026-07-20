#!/usr/bin/env python3
"""
Turn a photo into a monochrome ASCII-art portrait rendered as an animated SVG
that "types" itself in row by row.

Source image resolution order:
  1. --image PATH  (CLI arg)
  2. assets/me.jpg / me.jpeg / me.png  (commit your photo here)
  3. GitHub avatar for GITHUB_USER (downloaded; works on Actions runners)

Optional background removal via `rembg` if installed (pip install rembg).
Contrast boost via OpenCV CLAHE if installed; falls back to a plain stretch.
"""

import os
import sys
import html
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import theme as T

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT = ASSETS / "avi-ascii.svg"

GITHUB_USER = os.environ.get("GITHUB_USER", "Akarshit-Bansal")

# Density ramp: dark -> light background is #0d1117, so brighter subject => denser glyph
RAMP = "  .`:-=+*csoOIF#%@"          # index 0 = darkest area of page
COLS = 78                              # ASCII columns
CHAR_ASPECT = 0.52                     # monospace glyph h/w correction

BG = T.BG
INK = T.GREEN         # neon green glow
INK_DIM = T.GREEN2


def load_source() -> Image.Image | None:
    # explicit CLI path
    if len(sys.argv) > 1 and sys.argv[1] not in ("-", ""):
        p = Path(sys.argv[1])
        if p.exists():
            return Image.open(p)
    # committed photo
    for name in ("me.jpg", "me.jpeg", "me.png", "portrait.jpg", "portrait.png"):
        p = ASSETS / name
        if p.exists():
            print(f"using {p}")
            return Image.open(p)
    # fall back to GitHub avatar (network; fine on Actions)
    try:
        import requests
        url = f"https://github.com/{GITHUB_USER}.png?size=600"
        print(f"downloading avatar {url}")
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        from io import BytesIO
        return Image.open(BytesIO(r.content))
    except Exception as e:  # pragma: no cover
        print(f"avatar download failed: {e}", file=sys.stderr)
        return None


def remove_bg(img: Image.Image) -> Image.Image:
    try:
        from rembg import remove
        print("rembg: removing background")
        return remove(img)
    except Exception as e:
        print(f"rembg unavailable ({e}); keeping background")
        return img


def to_gray_matrix(img: Image.Image) -> np.ndarray:
    img = img.convert("RGBA")
    # composite onto white so removed/transparent background reads as page
    white = Image.new("RGBA", img.size, (255, 255, 255, 255))
    img = Image.alpha_composite(white, img).convert("L")

    arr = np.asarray(img)

    # contrast boost (CLAHE) if OpenCV present
    try:
        import cv2
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        arr = clahe.apply(arr)
    except Exception:
        lo, hi = np.percentile(arr, (2, 98))
        arr = np.clip((arr.astype(np.float32) - lo) * 255.0 / max(hi - lo, 1), 0, 255).astype(np.uint8)

    return arr


def resize_matrix(arr: np.ndarray, cols: int) -> np.ndarray:
    h, w = arr.shape
    rows = max(1, int(cols * (h / w) * CHAR_ASPECT))
    img = Image.fromarray(arr).resize((cols, rows), Image.LANCZOS)
    return np.asarray(img)


def matrix_to_rows(arr: np.ndarray) -> list[str]:
    # subject is dark-on-white grayscale; invert so bright subject -> dense glyph
    inv = 255 - arr
    idx = (inv.astype(np.float32) / 255.0 * (len(RAMP) - 1)).round().astype(int)
    return ["".join(RAMP[i] for i in row) for row in idx]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def build_svg(rows: list[str]) -> str:
    fs = 11              # font size px
    lh = fs             # line height (dense)
    cw = fs * 0.6       # monospace char width
    ncols = max(len(r) for r in rows)
    W = int(ncols * cw) + 28
    H = int(len(rows) * lh) + 28

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-label="ASCII portrait">',
        f"<defs>{T.defs(glow_color=T.GREEN, blur=1.4, key='p')}</defs>",
        "<style>"
        "@keyframes typerow{from{clip-path:inset(0 100% 0 0);opacity:0}"
        "to{clip-path:inset(0 0 0 0);opacity:1}}"
        "@keyframes pulse{0%,100%{opacity:.85}50%{opacity:1}}"
        "@keyframes scanmove{from{transform:translateY(0)}to{transform:translateY(6px)}}"
        ".row{opacity:0;animation:typerow .35s steps(24,end) forwards;white-space:pre}"
        f"text{{font-family:{T.font_stack()};font-size:{fs}px;letter-spacing:0}}"
        ".art{filter:url(#glowp);animation:pulse 3.5s ease-in-out infinite}"
        "</style>",
        f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="12" fill="url(#vigp)" '
        f'stroke="url(#borderp)" stroke-width="2.5" filter="url(#glowp)"/>',
        '<g class="art">',
    ]
    y = fs + 12
    for i, row in enumerate(rows):
        delay = 0.4 + i * 0.045
        col = INK if (i % 3) else INK_DIM
        out.append(
            f'<text class="row" x="14" y="{y}" fill="{col}" '
            f'style="animation-delay:{delay:.2f}s" xml:space="preserve">{esc(row)}</text>'
        )
        y += lh
    out.append("</g>")
    # scanline overlay + moving beam
    out.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="12" fill="url(#scanp)"/>')
    out.append(f'<rect x="2" width="{W-4}" height="14" fill="{T.CYAN}" opacity="0.10">'
               f'<animate attributeName="y" values="2;{H-16};2" dur="4.5s" repeatCount="indefinite"/></rect>')
    out.append("</svg>")
    return "".join(out)


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    img = load_source()
    if img is None:
        print("no source image; skipping portrait", file=sys.stderr)
        return 1
    if os.environ.get("REMBG", "0") == "1":
        img = remove_bg(img)
    arr = to_gray_matrix(img)
    arr = resize_matrix(arr, COLS)
    rows = matrix_to_rows(arr)
    OUT.write_text(build_svg(rows), encoding="utf-8")
    print(f"wrote {OUT}  ({OUT.stat().st_size} bytes, {len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
