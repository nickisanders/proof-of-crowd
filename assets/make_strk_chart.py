#!/usr/bin/env python3
"""The concentration figure in the $STRK audit.

Numbers come from reports/STRK-2026-10-14.md in proof-of-crowd-tools. The strip
is every one of the 39 same-size peers scanned on 2026-10-14, plotted by top-3
creator concentration, because a percentile is a claim and the distribution
behind it is the evidence. Same paper palette and Charter as the rest of the
site; figures in a monospace because an audit's numbers should read as measured.

Usage: python3 assets/make_strk_chart.py
"""

import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARP = "/Users/nicki/lunarcrush-projects/projects/crowd-size/node_modules/sharp"
FONT = "Charter, Georgia, serif"
MONO = "Menlo, ui-monospace, monospace"
GROUND, INK, SUB, RULE = "#ffffff", "#15171c", "#6e6a60", "#ded8cd"
NEUTRAL, OK, BAD, BRAND = "#8d8578", "#236440", "#a33228", "#1b3a6b"

# The 39 band peers, ascending. starknet is the first value.
PEERS = [0.2192, 0.2820, 0.2912, 0.3127, 0.3276, 0.3402, 0.3499, 0.3759,
         0.3886, 0.3905, 0.4005, 0.4313, 0.4423, 0.4661, 0.4732, 0.4779,
         0.4910, 0.5312, 0.5551, 0.5570, 0.5725, 0.5804, 0.5812, 0.6173,
         0.6193, 0.6203, 0.6235, 0.6654, 0.7653, 0.7735, 0.7807, 0.7909,
         0.8518, 0.8636, 0.8704, 0.8930, 0.9043, 0.9743, 0.9986]
STRK, MEDIAN = 0.2192, 0.5570


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


W, H = 1200, 720
L, R = 60, 1140

b = [txt(L, 58, 36, INK, "The week's biggest mover has the flattest crowd in its band.", 700),
     txt(L, 92, 20, SUB,
         "Starknet, up 62% in seven days. Top-3 creator concentration against 39 same-size tokens.")]

# The strip. One dot per peer along a 0-100% axis: the percentile is a claim and
# this is the evidence behind it.
AX, AY, AW = L + 10, 215, R - L - 20


def px(v):
    return AX + AW * v


b.append(f'<line x1="{AX}" y1="{AY}" x2="{AX+AW}" y2="{AY}" stroke="{RULE}" stroke-width="2"/>')
for v in (0, 0.25, 0.5, 0.75, 1.0):
    b.append(f'<line x1="{px(v):.0f}" y1="{AY}" x2="{px(v):.0f}" y2="{AY+10}" stroke="{RULE}" stroke-width="2"/>')
    b.append(txt(px(v), AY + 34, 19, SUB, f"{v*100:.0f}%", 400, "middle", MONO))

for v in PEERS:
    if v == STRK:
        continue
    b.append(f'<circle cx="{px(v):.1f}" cy="{AY-26}" r="9" fill="{NEUTRAL}" fill-opacity="0.5"/>')

# Median marker, so the gap is readable without counting dots.
b.append(f'<line x1="{px(MEDIAN):.0f}" y1="{AY-58}" x2="{px(MEDIAN):.0f}" y2="{AY-4}" '
         f'stroke="{INK}" stroke-width="2" stroke-dasharray="5 4"/>')
b.append(txt(px(MEDIAN), AY - 70, 20, INK, f"peer median {MEDIAN*100:.1f}%", 700, "middle"))

b.append(f'<circle cx="{px(STRK):.1f}" cy="{AY-26}" r="14" fill="{BRAND}"/>')
b.append(txt(px(STRK), AY - 70, 24, BRAND, "$STRK 21.9%", 700, "start"))
b.append(txt(px(STRK), AY - 96, 19, SUB, "lowest of the 39", 400, "start"))
b.append(txt(px(PEERS[-1]), AY - 56, 19, SUB, "VeChain 99.9%", 400, "end"))

# What a flat distribution is made of.
y = AY + 110
b.append(f'<line x1="{L}" y1="{y-42}" x2="{R}" y2="{y-42}" stroke="{RULE}" stroke-width="2"/>')
CARDS = [("119", "accounts across 152 posts,\nmedian one post each"),
         ("5%", "of those accounts have\nunder 1,000 followers"),
         ("3", "platforms carry it:\n66% X, 28% YouTube, 6% TikTok")]
cw = (R - L) / 3
for i, (big, small) in enumerate(CARDS):
    x = L + i * cw
    b.append(txt(x, y + 22, 54, INK, big, 700, "start", MONO))
    for j, ln in enumerate(small.split("\n")):
        b.append(txt(x, y + 60 + j * 27, 20, SUB, ln))

# The signal that argues the other way. An audit that only prints the
# favourable number is marketing.
y += 150
b.append(f'<rect x="{L}" y="{y-34}" width="{R-L}" height="76" fill="#fbf7ef"/>')
b.append(f'<rect x="{L}" y="{y-34}" width="5" height="76" fill="{BAD}"/>')
b.append(txt(L + 26, y, 23, INK, "Spam ran 59.2% against the token's own 35.9% norm, a 1.65x lift.", 700))
b.append(txt(L + 26, y + 30, 20, SUB,
             "The one adverse signal, and 12.9 of the 25 points. Attention of this size attracts ticker spam."))

# Verdict.
y += 128
b.append(f'<line x1="{L}" y1="{y-40}" x2="{R}" y2="{y-40}" stroke="{RULE}" stroke-width="2"/>')
b.append(txt(L, y + 8, 46, OK, "25 / 100", 700, "start", MONO))
b.append(txt(L + 230, y - 4, 26, INK, "organic", 700))
b.append(txt(L + 230, y + 26, 20, SUB, "Under 30 on the published scale. Nothing here looks bought."))
b.append(txt(R, y - 4, 18, SUB, "proofofcrowd.com", 400, "end"))
b.append(txt(R, y + 26, 18, SUB, "audited 2026-10-14", 400, "end"))

render("strk-concentration", W, H, "".join(b))
