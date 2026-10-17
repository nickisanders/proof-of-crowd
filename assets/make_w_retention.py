#!/usr/bin/env python3
"""The retention figure in the $W audit.

Numbers from section 8 of sample-w.html, measured 2026-10-17 across blocks
19,663,982 to 26,207,480, the contract's full history on Ethereum.

One funnel rather than a bar chart, because the three numbers are nested: every
address holding a real position is also still holding, and everyone still
holding also ever held. Three separate bars would invite reading them as
independent quantities, which they are not.

Same paper palette and Charter as the rest of the site; figures in a monospace
because an audit's numbers should read as measured.

Usage: python3 assets/make_w_retention.py
"""

import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARP = "/Users/nicki/lunarcrush-projects/projects/crowd-size/node_modules/sharp"
FONT = "Charter, Georgia, serif"
MONO = "Menlo, ui-monospace, monospace"
GROUND, INK, SUB, RULE = "#ffffff", "#15171c", "#6e6a60", "#ded8cd"
NEUTRAL, BRAND, HOT = "#8d8578", "#1b3a6b", "#a33228"

EVER, HOLD, REAL = 26_714, 9_598, 1_487


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, size, fill, s, weight=400, anchor="start", font=None):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}" font-family="{font or FONT}">{esc(s)}</text>')


def render(name, w, h, body, scale=2):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{GROUND}"/>{body}</svg>')
    (HERE / f"{name}.svg").write_text(svg)
    subprocess.run(["node", "-e",
        f"const s=require('{SHARP}');s('{HERE}/{name}.svg',{{density:144}})"
        f".resize({w*scale},{h*scale}).png().toFile('{HERE}/{name}.png')"
        f".then(i=>console.log('{name}.png',i.width+'x'+i.height));"], check=True)


W, H = 1200, 880
L, R = 60, 1140

b = [txt(L, 58, 36, INK, "26,714 addresses have held $W.", 700),
     txt(L, 96, 36, INK, "9,598 still do.", 700),
     txt(L, 132, 20, SUB,
         "Every address that ever received the token on Ethereum, across the "
         "contract's full 901-day history.")]

# A nested funnel: each band is a subset of the one above it.
BX, BW, BH, GAP = L, R - L, 86, 26
rows = [("ever received it", EVER, NEUTRAL, "26,714"),
        ("still hold it", HOLD, BRAND, "9,598"),
        ("hold $100 or more", REAL, HOT, "1,487")]
y = 206
for label, n, col, fig in rows:
    w = BW * n / EVER
    b.append(f'<rect x="{BX}" y="{y}" width="{BW}" height="{BH}" fill="#f2efe8"/>')
    b.append(f'<rect x="{BX}" y="{y}" width="{w:.0f}" height="{BH}" fill="{col}"/>')
    # Inside the band when it is wide enough to hold the figure, beside it when not.
    if w > 260:
        b.append(txt(BX + 24, y + 56, 38, "#ffffff", fig, 700, "start", MONO))
        b.append(txt(BX + w - 24, y + 55, 22, "#ffffff", label, 400, "end"))
    else:
        b.append(txt(BX + w + 24, y + 56, 38, col, fig, 700, "start", MONO))
        b.append(txt(BX + w + 190, y + 55, 22, SUB, label))
    y += BH + GAP

y += 18
b.append(f'<line x1="{L}" y1="{y}" x2="{R}" y2="{y}" stroke="{RULE}" stroke-width="2"/>')
# One line per statement: the first render ran the two together, because a
# monospace figure is wider than the offset guessed for it.
y += 48
b.append(txt(L, y, 30, INK, "35.9% retention. 17,116 addresses have left.", 700))
y += 34
b.append(txt(L, y, 21, SUB,
             "About 5.6% of every address that ever touched $W holds a position worth something today."))

# The caveat belongs on the image, not only in the thread under it.
y += 56
b.append(f'<rect x="{L}" y="{y-26}" width="{R-L}" height="74" fill="#fbf7ef"/>')
b.append(f'<rect x="{L}" y="{y-26}" width="5" height="74" fill="{NEUTRAL}"/>')
b.append(txt(L + 26, y, 21, INK,
             "35.9% is not a pass or a fail. This figure has no absolute threshold.", 700))
b.append(txt(L + 26, y + 28, 20, SUB,
             "It is informative against a token's own history and against tokens of a similar size."))

y = H - 50
b.append(f'<line x1="{L}" y1="{y-36}" x2="{R}" y2="{y-36}" stroke="{RULE}" stroke-width="2"/>')
b.append(txt(L, y, 20, SUB, "Uncommissioned. Published in full."))
b.append(txt(R, y, 20, SUB, "proofofcrowd.com  ·  measured 2026-10-17", 400, "end"))

render("w-retention", W, H, "".join(b))
