#!/usr/bin/env python3
"""The Proof of Crowd mark, and every variant the brand actually uses.

The mark is a ring of evenly spaced dots around a solid centre. It reads two
ways on purpose: as a crowd, which is what the product measures, and as a
stamp, which is what the product issues. The even spacing is the point. A real
crowd is many voices carrying roughly equal weight, and that is exactly the
shape the ring draws.

Dot counts are kept low and radii high so the ring still reads at 32px rather
than dissolving into texture. Everything is drawn on a 64-unit grid.

Usage: python3 assets/make_logo.py
"""

import subprocess
from math import cos, pi, sin
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARP = "/Users/nicki/lunarcrush-projects/projects/crowd-size/node_modules/sharp"
BG, GREEN, TEXT, DIM = "#0d1117", "#3fb950", "#e6edf3", "#2d6b3a"
FONT = "system-ui,-apple-system,Helvetica,Arial,sans-serif"


def ring(r, n, rad, fill, phase=-pi / 2):
    return "".join(
        f'<circle cx="{32 + r * cos(phase + 2 * pi * i / n):.2f}" '
        f'cy="{32 + r * sin(phase + 2 * pi * i / n):.2f}" r="{rad}" fill="{fill}"/>'
        for i in range(n))


def mark(accent=GREEN, inner=DIM) -> str:
    """The mark itself, on a 64-unit grid, no background."""
    return (ring(25, 12, 3.4, accent)
            + ring(15.5, 6, 2.6, inner, phase=-pi / 2 + pi / 6)
            + f'<circle cx="32" cy="32" r="6.5" fill="{accent}"/>')


def mark_small() -> str:
    """At 16px the inner ring turns to mush, so the favicon drops it and runs
    eight fatter dots instead of twelve. Same silhouette, one that survives."""
    return ring(24, 8, 5.2, GREEN) + f'<circle cx="32" cy="32" r="7.5" fill="{GREEN}"/>'


def svg(w, h, body, bg=BG) -> str:
    fill = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">{fill}{body}</svg>')


def render(name, source, out_w=None):
    (HERE / f"{name}.svg").write_text(source)
    resize = f".resize({out_w})" if out_w else ""
    subprocess.run(["node", "-e",
        f"const s=require('{SHARP}');s('{HERE}/{name}.svg',{{density:600}}){resize}"
        f".png().toFile('{HERE}/{name}.png').then(()=>0);"], check=True)


def wordmark(accent, text, bg, inner):
    """Horizontal lockup. The two words sit on one line at 56pt on a 480x128
    canvas, which is the proportion the site nav and a LinkedIn banner want."""
    m = f'<g transform="translate(20,32)"><g transform="scale(1)">{mark(accent, inner)}</g></g>'
    return svg(480, 128, m
        + f'<text x="104" y="76" font-size="38" font-weight="700" font-family="{FONT}" '
          f'fill="{text}">Proof of<tspan dx="9" fill="{accent}">Crowd</tspan></text>', bg)


# Square app/avatar mark, on the dark ground, rounded like the favicon.
render("logo-mark", svg(64, 64, f'<rect width="64" height="64" rx="14" fill="{BG}"/>{mark()}'), 512)
# The same mark with no ground, for placing on arbitrary backgrounds.
render("logo-mark-bare", svg(64, 64, mark(), bg=None), 512)
# Horizontal lockups: dark (default), light, and single-colour for documents.
render("logo-wordmark", wordmark(GREEN, TEXT, BG, DIM), 960)
render("logo-wordmark-light", wordmark("#1a7f37", "#0d1117", "#ffffff", "#8fcf9f"), 960)
render("logo-wordmark-mono", wordmark(TEXT, TEXT, BG, "#484f58"), 960)

# Favicons. 180 (Apple touch) keeps the full mark; 16 and 32 use the small one.
SMALL = svg(64, 64, f'<rect width="64" height="64" rx="14" fill="{BG}"/>{mark_small()}')
(HERE / "favicon.svg").write_text(SMALL)
(HERE / "logo-mark-small.svg").write_text(svg(64, 64, mark_small(), bg=None))
for size, src in ((16, "favicon"), (32, "favicon"), (180, "logo-mark")):
    subprocess.run(["node", "-e",
        f"const s=require('{SHARP}');s('{HERE}/{src}.svg',{{density:600}})"
        f".resize({size},{size}).png().toFile('{HERE}/favicon-{size}.png').then(()=>0);"], check=True)
print("wrote", len(list(HERE.glob("logo-*"))) + 4, "files")
