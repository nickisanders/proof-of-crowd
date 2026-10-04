#!/usr/bin/env python3
"""Profile picture and header for X.

Two constraints drive the layout. X crops the avatar to a circle, so the mark
sits centred on its own bounding box rather than on the 64-unit grid, whose
centre is not where the ink is. And the avatar overlaps the header's lower
left, so everything in that corner has to stay clear: roughly the left 340px
below y=320 is dead space and is deliberately left empty.

Usage: python3 assets/make_social.py
"""

import importlib.util
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARP = "/Users/nicki/lunarcrush-projects/projects/crowd-size/node_modules/sharp"

_spec = importlib.util.spec_from_file_location("make_logo", HERE / "make_logo.py")
_logo = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_logo)

PAPER, PANEL, INK, SUB = "#f6f3ec", "#ffffff", "#15171c", "#6e6a60"
BRAND, BAD, RULE = "#1b3a6b", "#a33228", "#ded8cd"
SERIF, MONO = "Charter, Georgia, serif", "Menlo, ui-monospace, monospace"

# The mark's ink, not its grid. The arch spans x 5..59 and y 9..47, so its
# visual centre sits at (32, 28) and centring on (32, 32) would hang it low.
INK_CX, INK_CY, INK_W = 32.0, 28.0, 54.0


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, size, fill, s, weight=400, anchor="start", font=SERIF, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}" font-family="{font}" {extra}>'
            f'{s if "<tspan" in s else esc(s)}</text>')


def render(name, w, h, body, bg=PAPER):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')
    (HERE / f"{name}.svg").write_text(svg)
    subprocess.run(["node", "-e",
        f"const s=require('{SHARP}');s('{HERE}/{name}.svg',{{density:300}}).resize({w},{h})"
        f".png().toFile('{HERE}/{name}.png').then(i=>console.log('{name}.png',i.width+'x'+i.height));"],
        check=True)


def centred_mark(size, target_w):
    """Place the mark so its ink, not its grid, lands in the middle."""
    k = target_w / INK_W
    return (f'<g transform="translate({size / 2 - INK_CX * k:.1f},{size / 2 - INK_CY * k:.1f}) '
            f'scale({k:.4f})">{_logo.mark()}</g>')


# ------------------------------------------------------- avatar (circle crop)
for px in (400, 1000):
    render(f"x-avatar-{px}", px, px, centred_mark(px, px * 0.63))

# ------------------------------------------------------------ header 1500x500
CARD_X, CARD_Y, CARD_W, CARD_H = 950, 104, 490, 286
header = [
    f'<rect x="0" y="0" width="1500" height="7" fill="{BRAND}"/>',
    # Upper left only. Below y=320 on this side the avatar sits on top.
    t(70, 150, 25, SUB, "EVIDENCE-BASED ATTENTION AUDITS", 400, font=MONO,
      extra='letter-spacing="2"'),
    t(70, 222, 58, INK, f'Proof of<tspan dx="17" fill="{BRAND}">Crowd</tspan>', 700),
    t(70, 272, 26, SUB, "Who is actually talking, how much of it is manufactured,"),
    t(70, 308, 26, SUB, "and whether the crowd survives a spreadsheet."),
    # Right: what the product produces, rather than the logo a second time.
    f'<rect x="{CARD_X}" y="{CARD_Y}" width="{CARD_W}" height="{CARD_H}" rx="14" '
    f'fill="{PANEL}" stroke="{RULE}" stroke-width="1.5"/>',
    t(CARD_X + 30, CARD_Y + 44, 15, SUB, "SAMPLE VERDICT", 400, font=MONO, extra='letter-spacing="1.6"'),
    t(CARD_X + 30, CARD_Y + 104, 44, BAD, "97/100", 700, font=MONO),
    t(CARD_X + 30, CARD_Y + 146, 30, BAD, "manufactured", 700),
    f'<rect x="{CARD_X + 30}" y="{CARD_Y + 170}" width="{CARD_W - 60}" height="1" fill="{RULE}"/>',
    t(CARD_X + 30, CARD_Y + 206, 18, SUB, "Spam vs the token's own norm"),
    t(CARD_X + CARD_W - 30, CARD_Y + 206, 18, INK, "2.0x", 700, "end", MONO),
    t(CARD_X + 30, CARD_Y + 244, 18, SUB, "Top 3 creator share"),
    t(CARD_X + CARD_W - 30, CARD_Y + 244, 18, INK, "98%", 700, "end", MONO),
    t(1440, 440, 25, BRAND, "proofofcrowd.com", 700, "end"),
]
render("x-header", 1500, 500, "".join(header))
