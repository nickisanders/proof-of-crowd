#!/usr/bin/env python3
"""The supply figure in the $LAPTOP audit.

Numbers come from the reconstruction in reports/LAPTOP-2026-10-07.md: every one
of the 1,964,431 Transfer events since deployment, reconciling to exactly
1,000,000,000. Same paper palette and Charter as the rest of the site; figures
in a monospace because an audit's numbers should read as measured.

Usage: python3 assets/make_laptop_chart.py
"""

import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARP = "/Users/nicki/lunarcrush-projects/projects/crowd-size/node_modules/sharp"
FONT = "Charter, Georgia, serif"
MONO = "Menlo, ui-monospace, monospace"
GROUND, INK, SUB, RULE = "#ffffff", "#15171c", "#6e6a60", "#ded8cd"
NEUTRAL, OK, BAD, BRAND = "#8d8578", "#236440", "#a33228", "#1b3a6b"


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


W, H = 1200, 760
L, R = 60, 1140
BANDS = [("$10k or more", 49, NEUTRAL), ("$1k - $10k", 167, NEUTRAL),
         ("$100 - $1k", 971, BRAND), ("$10 - $100", 3_715, NEUTRAL),
         ("$1 - $10", 6_424, NEUTRAL), ("under $1", 22_297, BAD)]

b = [txt(L, 58, 36, INK, "33,623 holders. 1,187 of them hold $100 or more.", 700),
     txt(L, 92, 20, SUB,
         "$LAPTOP wallets by position size, rebuilt from all 1,964,431 transfers since deployment")]

# A log scale, because 49 and 22,297 do not share a linear axis legibly. Counts
# are printed beside every bar so the scale never has to be trusted.
import math
TOP, ROW = 140, 62
BAR_X, BAR_MAX = 350, 620
peak = math.log10(max(n for _, n, _ in BANDS))
for i, (label, n, col) in enumerate(BANDS):
    y = TOP + i * ROW
    # Bars stop short of the right margin so the count beside the longest one
    # still fits: at full width "22,297" ran off the canvas and printed "22,2".
    w = BAR_MAX * (math.log10(n) / peak)
    b.append(txt(330, y + 26, 21, INK, label, 400, "end"))
    b.append(f'<rect x="{BAR_X}" y="{y}" width="{max(w,4):.0f}" height="34" rx="4" fill="{col}"/>')
    b.append(txt(BAR_X + max(w, 4) + 14, y + 27, 23, INK, f"{n:,}", 700, "start", MONO))

y = TOP + len(BANDS) * ROW + 14
b.append(f'<rect x="{L}" y="{y}" width="{R-L}" height="1.5" fill="{RULE}"/>')
b.append(txt(L, y + 46, 24, INK,
             "Two thirds of the holder count holds less than one dollar.", 700))
b.append(txt(L, y + 80, 20, SUB,
             "Dust is normal for any ERC-20 and is not evidence of anything on its own. It does mean"))
b.append(txt(L, y + 106, 20, SUB,
             "a headline holder number counts those addresses the same as the ones with money at stake."))
b.append(txt(L, y + 152, 22, BRAND,
             "Top ten addresses hold 91.7% of supply. 90.1 of those points sit in contracts,", 700))
b.append(txt(L, y + 180, 22, BRAND,
             "multisigs and the burn address.", 700))
b.append(txt(L, H - 26, 17, SUB, "Proof of Crowd  ·  audited 2026-10-07  ·  Base"))
b.append(txt(R, H - 26, 17, SUB, "proofofcrowd.com", 400, "end"))

render("laptop-supply", W, H, "".join(b))
