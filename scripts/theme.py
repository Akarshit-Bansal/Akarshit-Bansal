"""
Shared neon-cyberpunk theme helpers for the profile-art SVG generators.
Every generator writes a self-contained SVG, so these helpers return
<defs> fragments (filters / gradients / patterns) to embed per file.
"""

# ---- palette --------------------------------------------------------------
BG        = "#05070d"
BG2       = "#0a0f18"
PANEL     = "#0b111b"
INK       = "#c9f7e8"
DIM       = "#6f8ea0"

GREEN     = "#39ff14"   # neon green
GREEN2    = "#00e08a"
CYAN      = "#00e5ff"   # neon cyan
MAGENTA   = "#ff2bd6"   # neon magenta
PURPLE    = "#a970ff"
AMBER     = "#ffcc33"
RED       = "#ff5f6d"

ACCENTS = [GREEN, CYAN, MAGENTA, PURPLE, AMBER]


def defs(glow_color: str = CYAN, blur: float = 2.2, key: str = "") -> str:
    """Reusable defs: neon glow filter, scanline pattern, animated border gradient."""
    g = key
    return f"""
    <filter id="glow{g}" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="{blur}" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softglow{g}" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feColorMatrix in="b" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .9 0"/>
    </filter>
    <linearGradient id="border{g}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{CYAN}">
        <animate attributeName="stop-color"
          values="{CYAN};{MAGENTA};{GREEN};{CYAN}" dur="6s" repeatCount="indefinite"/>
      </stop>
      <stop offset="0.5" stop-color="{MAGENTA}">
        <animate attributeName="stop-color"
          values="{MAGENTA};{GREEN};{CYAN};{MAGENTA}" dur="6s" repeatCount="indefinite"/>
      </stop>
      <stop offset="1" stop-color="{GREEN}">
        <animate attributeName="stop-color"
          values="{GREEN};{CYAN};{MAGENTA};{GREEN}" dur="6s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>
    <pattern id="scan{g}" width="3" height="3" patternUnits="userSpaceOnUse">
      <rect width="3" height="3" fill="none"/>
      <rect width="3" height="1" y="0" fill="#ffffff" opacity="0.035"/>
    </pattern>
    <radialGradient id="vig{g}" cx="50%" cy="0%" r="120%">
      <stop offset="0" stop-color="{BG2}"/>
      <stop offset="1" stop-color="{BG}"/>
    </radialGradient>
    """


def font_stack() -> str:
    return ("'JetBrains Mono','Fira Code','SF Mono',ui-monospace,"
            "'Cascadia Code',Consolas,monospace")
