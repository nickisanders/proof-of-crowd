#!/usr/bin/env python3
"""The figure behind the cross-token census.

Reads the census computed over the 130 audited tokens. The point of the chart is
that one number is produced by two unrelated behaviours, so it shows the
distribution of how many tokens a post names, then the two archetypes side by
side.

Usage: python3 assets/make_amplifier_chart.py
"""

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path.home() / "proof-of-crowd-tools/out/amplifier-census.json"
SHARP = "/Users/nicki/lunarcrush-projects/projects/crowd-size/node_modules/sharp"
FONT = "Charter, Georgia, serif"
MONO = "Menlo, ui-monospace, monospace"
GROUND, INK, SUB, RULE = "#ffffff", "#15171c", "#6e6a60", "#ded8cd"
NEUTRAL, BRAND, BAD = "#8d8578", "#1b3a6b", "#a33228"
W, H = 1200, 820
L, R = 60, 1140


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, size, fill, s, weight=400, anchor="start", font=None):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}" font-family="{font or FONT}">{esc(s)}</text>')


d = json.loads(SRC.read_text())
tot = d["total_posts"]

b = [txt(L, 58, 35, INK, "One signal, two different behaviours.", 700),
     txt(L, 92, 20, SUB,
         f"Posts from the 40 accounts appearing across the most of {d['population']} "
         f"audited tokens, by how many tokens each post names")]

# Distribution. The 8+ bar is the one that matters, so it carries the accent.
BARS = [("names 1 token", d["buckets"]["1"], NEUTRAL),
        ("names 2", d["buckets"]["2"], NEUTRAL),
        ("names 3 to 7", d["buckets"]["3-7"], NEUTRAL),
        ("names 8 or more", d["buckets"]["8+"], BRAND)]
TOP, ROW, BX, BW = 150, 62, 300, 560
peak = max(n for _, n, _ in BARS)
for i, (label, n, col) in enumerate(BARS):
    y = TOP + i * ROW
    w = BW * n / peak
    b.append(txt(BX - 20, y + 26, 21, INK, label, 400, "end"))
    b.append(f'<rect x="{BX}" y="{y}" width="{max(w,3):.0f}" height="34" rx="4" fill="{col}"/>')
    b.append(txt(BX + max(w, 3) + 14, y + 27, 22, INK, f"{n/tot*100:.0f}%", 700, "start", MONO))

y = TOP + len(BARS) * ROW + 16
b.append(f'<rect x="{L}" y="{y}" width="{R-L}" height="1.5" fill="{RULE}"/>')
b.append(txt(L, y + 44, 24, INK,
             "A third of their posts name eight tokens or more.", 700))

# The two archetypes, side by side, because the contrast is the finding.
CY = y + 96
for i, (title, line1, line2, col) in enumerate([
    ("The list poster",
     "One post names 28 tickers.",
     "That single post places the account inside dozens of token conversations at once.",
     NEUTRAL),
    ("The serial poster",
     "51 posts, one token each.",
     "Almost no lists. Fifty-one separately written posts, each on the same template.",
     BAD),
]):
    x = L + i * 560
    b.append(f'<rect x="{x}" y="{CY}" width="520" height="150" rx="6" fill="#faf8f4"/>')
    b.append(f'<rect x="{x}" y="{CY}" width="5" height="150" rx="2.5" fill="{col}"/>')
    b.append(txt(x + 26, CY + 40, 23, INK, title, 700))
    b.append(txt(x + 26, CY + 76, 22, col, line1, 700))
    words = line2.split()
    half = len(words) // 2
    b.append(txt(x + 26, CY + 108, 18, SUB, " ".join(words[:half])))
    b.append(txt(x + 26, CY + 132, 18, SUB, " ".join(words[half:])))

b.append(txt(L, CY + 196, 23, INK,
             f"Both register as an account that also posts about other tokens.", 700))
b.append(txt(L, CY + 226, 19, SUB,
             "Which is why the posts behind the number get read before anything is concluded."))
b.append(txt(L, H - 26, 17, SUB,
             f"Proof of Crowd  ·  {d['population']} audited tokens  ·  2026-10-13"))
b.append(txt(R, H - 26, 17, SUB, "proofofcrowd.com", 400, "end"))

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{GROUND}"/>'
       + "".join(b) + "</svg>")
(HERE / "amplifier.svg").write_text(svg)
subprocess.run(["node", "-e",
    f"const s=require('{SHARP}');s('{HERE}/amplifier.svg',{{density:144}})"
    f".resize({W*2},{H*2}).png().toFile('{HERE}/amplifier.png')"
    f".then(i=>console.log('amplifier.png',i.width+'x'+i.height));"], check=True)
