#!/usr/bin/env python3
"""The Proof of Crowd mark, and every variant the brand actually uses.

The mark is a fingerprint whose ridges are made of separate dots. Proof drawn
as the oldest proof there is, and built out of a population, because the thing
this product verifies is how many distinct people are really there.

Ridge spacing is held constant rather than dot count, otherwise the outer arcs
go sparse and the eye joins them into straight lines instead of a curve.

A fingerprint does not survive 16px at full detail, so the favicon runs a
three-ridge version with much fatter dots. Same silhouette, one that reads.

Usage: python3 assets/make_logo.py
"""

import subprocess
from math import cos, radians, sin
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARP = "/Users/nicki/lunarcrush-projects/projects/crowd-size/node_modules/sharp"

# Dossier. Paper and ink, so a report looks like a document rather than a
# dashboard screenshot. Verdict colours live in styles.css and never appear in
# the mark: the brand must not imply a verdict just by being on the page.
PAPER, INK, BRAND = "#f6f3ec", "#15171c", "#1b3a6b"
BRAND_ON_DARK = "#7da7e0"   # the navy is unreadable on ink, so it lifts
FONT = "Charter, Georgia, serif"
SWEEP, START = 220, 160     # degrees; the arc is open at the bottom


def ridges(radii, dot, spacing, color) -> str:
    out = []
    for r in radii:
        n = max(3, round(r * radians(SWEEP) / spacing))
        for i in range(n):
            a = radians(START + SWEEP * i / (n - 1))
            out.append(f'<circle cx="{32 + r * cos(a):.2f}" cy="{36 + r * sin(a):.2f}" '
                       f'r="{dot}" fill="{color}"/>')
    return "".join(out)


def mark(color=BRAND) -> str:
    """Full detail. Good from about 48px up."""
    return ridges((7, 13, 19, 25), 1.9, 4.6, color) + f'<circle cx="32" cy="36" r="2.4" fill="{color}"/>'


def mark_small(color=BRAND) -> str:
    """Three ridges, fat dots. For favicons and the nav."""
    return ridges((10, 19, 28), 3.0, 8.0, color) + f'<circle cx="32" cy="36" r="3.4" fill="{color}"/>'


def svg(w, h, body, bg=PAPER) -> str:
    fill = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">{fill}{body}</svg>')


def wordmark(accent, text, bg) -> str:
    """Horizontal lockup, the proportion the site nav and a banner want.

    Weight stays at 700. Charter has a real bold face, so librsvg sets it
    directly instead of faking one by double-striking the glyphs.
    """
    return svg(480, 128,
        f'<g transform="translate(20,30)">{mark(accent)}</g>'
        f'<text x="104" y="76" font-size="38" font-weight="700" font-family="{FONT}" '
        f'fill="{text}">Proof of<tspan dx="12" fill="{accent}">Crowd</tspan></text>', bg)


def render(name, source, out_w=None):
    (HERE / f"{name}.svg").write_text(source)
    resize = f".resize({out_w})" if out_w else ""
    subprocess.run(["node", "-e",
        f"const s=require('{SHARP}');s('{HERE}/{name}.svg',{{density:600}}){resize}"
        f".png().toFile('{HERE}/{name}.png').then(()=>0);"], check=True)


ROUND = f'<rect width="64" height="64" rx="14" fill="{PAPER}"/>'
ROUND_DARK = f'<rect width="64" height="64" rx="14" fill="{INK}"/>'

render("logo-mark", svg(64, 64, ROUND + mark()), 512)
render("logo-mark-dark", svg(64, 64, ROUND_DARK + mark(BRAND_ON_DARK)), 512)
render("logo-mark-bare", svg(64, 64, mark(), bg=None), 512)
render("logo-wordmark", wordmark(BRAND, INK, PAPER), 960)
render("logo-wordmark-dark", wordmark(BRAND_ON_DARK, "#e9eef5", INK), 960)
render("logo-wordmark-mono", wordmark(INK, INK, PAPER), 960)

# Favicons run the simplified mark; the Apple touch icon is big enough for full.
(HERE / "favicon.svg").write_text(svg(64, 64, ROUND + mark_small()))
(HERE / "logo-mark-small.svg").write_text(svg(64, 64, mark_small(), bg=None))
for size, src in ((16, "favicon"), (32, "favicon"), (180, "logo-mark")):
    subprocess.run(["node", "-e",
        f"const s=require('{SHARP}');s('{HERE}/{src}.svg',{{density:600}})"
        f".resize({size},{size}).png().toFile('{HERE}/favicon-{size}.png').then(()=>0);"], check=True)
print("logo set rebuilt")
