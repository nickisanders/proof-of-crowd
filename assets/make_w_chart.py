#!/usr/bin/env python3
"""The supply figure in the $W audit.

Numbers come from reports/W-2026-10-12.md: a top-50 sample covering 59.2% of the
Ethereum contract's supply, and that contract's own totalSupply against the
token's 10bn global total. Same paper palette and Charter as the rest of the
site; figures in a monospace because an audit's numbers should read as measured.

Usage: python3 assets/make_w_chart.py
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


W, H = 1200, 740
L, R = 60, 1140

b = [txt(L, 58, 36, INK, "Nearly half of it is two addresses.", 700),
     txt(L, 92, 20, SUB,
         "Where the $W on Ethereum actually sits, from a sample covering 59.2% of that supply")]

# One stacked bar: the whole Ethereum contract, split by who holds it. A single
# bar rather than separate ones, because the point is that these are shares of
# one thing.
SEGS = [("vesting lockup contract", 24.2, BRAND),
        ("exchange custody", 20.5, NEUTRAL),
        ("other contracts", 8.3, "#b9b2a4"),
        ("everything else", 47.0, "#e6e1d6")]
BX, BY, BW, BH = L, 150, R - L, 86
x = BX
for label, pct, col in SEGS:
    w = BW * pct / 100
    b.append(f'<rect x="{x:.0f}" y="{BY}" width="{w:.0f}" height="{BH}" fill="{col}"/>')
    if pct >= 9:
        b.append(txt(x + w / 2, BY + 52, 27, "#ffffff" if col in (BRAND, NEUTRAL) else INK,
                     f"{pct:.1f}%", 700, "middle", MONO))
    x += w
y = BY + BH + 42
for label, pct, col in SEGS:
    b.append(f'<rect x="{L}" y="{y-16}" width="18" height="18" rx="3" fill="{col}"/>')
    b.append(txt(L + 30, y, 21, INK, label))
    y += 34

y += 18
b.append(f'<rect x="{L}" y="{y}" width="{R-L}" height="1.5" fill="{RULE}"/>')
b.append(txt(L, y + 46, 25, INK,
             "The top 50 holders, excluding contracts and exchanges, hold 6.2% of supply.", 700))

rows = [("Holders on Ethereum", "9,556"),
        ("Holding $100 or more", "2,064"),
        ("Addresses that are contracts", "1,117"),
        ("Share of the 10bn token on this chain", "10.6%")]
y += 86
for label, val in rows:
    b.append(txt(L, y, 21, SUB, label))
    b.append(txt(R, y, 23, INK, val, 700, "end", MONO))
    b.append(f'<rect x="{L}" y="{y+12}" width="{R-L}" height="1" fill="{RULE}"/>')
    y += 44

b.append(txt(L, H - 26, 17, SUB, "Proof of Crowd  ·  audited 2026-10-12  ·  Ethereum"))
b.append(txt(R, H - 26, 17, SUB, "proofofcrowd.com", 400, "end"))

render("w-supply", W, H, "".join(b))
