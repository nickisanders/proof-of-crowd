#!/usr/bin/env python3
"""The two figures in the $FET sample report.

Numbers are the ones published in sample-fet.html, so this script is the record
of how the figures were drawn. Same paper palette and Charter as the rest of
the site; figures in a monospace because an audit's numbers should read as
measured.

Usage: python3 assets/make_fet_charts.py
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


# ------------------------------------------------- the five spikes, and the crowd
SPIKES = [("Sep 21", 1_317_530, 421), ("Sep 24", 1_044_228, 465),
          ("Sep 25", 1_602_991, 538), ("Sep 26", 1_003_405, 591),
          ("Oct 4", 1_675_803, 684)]
BASE_I, BASE_P = 476_729, 311

body = [txt(60, 56, 36, INK, "Five spikes, a bigger crowd each time", 700),
        txt(60, 90, 21, SUB, "$FET daily interactions and people posting, against its own 30-day normal")]
L, BASE, TOP = 70, 440, 150
peak = max(v for _, v, _ in SPIKES)
step = (1130 - L) / len(SPIKES)
for i, (day, inter, people) in enumerate(SPIKES):
    x = L + i * step
    h = (BASE - TOP) * inter / peak
    body.append(f'<rect x="{x:.0f}" y="{BASE-h:.0f}" width="{step-70:.0f}" height="{h:.0f}" rx="4" fill="{BRAND}"/>')
    body.append(txt(x + (step-70)/2, BASE - h - 14, 23, BRAND, f"{inter/1e6:.2f}M", 700, "middle", MONO))
    body.append(txt(x + (step-70)/2, BASE + 26, 19, SUB, day, 400, "middle"))
    body.append(txt(x + (step-70)/2, BASE + 58, 26, OK, f"{people}", 700, "middle", MONO))
body.append(f'<rect x="{L}" y="{BASE}" width="{1130-L}" height="1.5" fill="{RULE}"/>')
body.append(f'<rect x="{L}" y="{BASE-(BASE-TOP)*BASE_I/peak:.0f}" width="{1130-L}" height="1.5" fill="{SUB}" opacity="0.4"/>')
body.append(txt(L, 138, 17, SUB, f"30-day normal {BASE_I/1e6:.2f}M"))
body.append(txt(L, 86 + 440, 19, SUB, f"people posting  ·  30-day normal {BASE_P}"))
body.append(txt(60, 580, 22, INK, "Between the spikes, attention sits 2.4x where it did two months ago.", 700))
body.append(txt(60, 610, 18, SUB, "The crowd is not round-tripping. Price is up 54% over the same stretch."))
render("fet-spikes", 1200, 650, "".join(body))

# ------------------------------------------- conversion: spike vs ordinary days
body = [txt(60, 56, 36, INK, "The attention peaks did not bring buyers", 700),
        txt(60, 90, 21, SUB, "first-time onchain holders per million interactions, 45-day window")]
bars = [("ordinary days", 479.4, 192, NEUTRAL), ("spike days", 182.6, 264, BAD)]
BASE2, TOP2 = 400, 150
for i, (label, perM, perDay, col) in enumerate(bars):
    x = 120 + i * 480
    h = (BASE2 - TOP2) * perM / 479.4
    body.append(f'<rect x="{x}" y="{BASE2-h:.0f}" width="300" height="{h:.0f}" rx="4" fill="{col}"/>')
    body.append(txt(x + 150, BASE2 - h - 16, 36, col, f"{perM:.0f}", 700, "middle", MONO))
    body.append(txt(x + 150, BASE2 + 30, 22, INK, label, 400, "middle"))
    body.append(txt(x + 150, BASE2 + 58, 18, SUB, f"{perDay} new holders a day", 400, "middle"))
body.append(f'<rect x="90" y="{BASE2}" width="1020" height="1.5" fill="{RULE}"/>')
body.append(txt(60, 520, 22, INK, "Spike days carried 3.6x the attention and 1.37x the new holders.", 700))
body.append(txt(60, 550, 18, SUB, "The extra attention converted at 0.38x the ordinary rate."))
body.append(txt(60, 590, 17, SUB, "Caveat: ~99.9% of $FET volume is on exchanges, where a buyer creates no onchain transfer."))
render("fet-conversion", 1200, 630, "".join(body))


# ------------------------------------------ the holder base: distribution and retention
BUCKETS = [("$10k+", 1_455), ("$1k - $10k", 10_203), ("$100 - $1k", 33_594),
           ("$10 - $100", 42_171), ("$1 - $10", 31_722), ("under $1", 40_068)]
WALLETS, HEADLINE, EVER = 159_213, 165_574, 507_165
MEANINGFUL = 45_252

body = [txt(60, 56, 36, INK, "165,574 holders, 45,252 with a real position", 700),
        txt(60, 90, 21, SUB, "$FET wallets by position size, contracts and custody excluded")]
L, TOP, ROW = 300, 140, 56
widest = max(n for _, n in BUCKETS)
for i, (label, n) in enumerate(BUCKETS):
    y = TOP + i * ROW
    w = 720 * n / widest
    meaningful = label in ("$10k+", "$1k - $10k", "$100 - $1k")
    body.append(txt(L - 20, y + 20, 20, INK if meaningful else SUB, label, 700 if meaningful else 400, "end"))
    body.append(f'<rect x="{L}" y="{y}" width="{w:.0f}" height="28" rx="3" '
                f'fill="{BRAND if meaningful else NEUTRAL}"/>')
    body.append(txt(L + w + 14, y + 20, 19, INK, f"{n:,}", 700, "start", MONO))
body.append(f'<rect x="60" y="{TOP + len(BUCKETS)*ROW + 16}" width="1080" height="1.5" fill="{RULE}"/>')
yb = TOP + len(BUCKETS) * ROW + 56
body.append(txt(60, yb, 22, INK, f"Only {MEANINGFUL:,} hold $100 or more, 27% of the headline count.", 700))
body.append(txt(60, yb + 30, 19, SUB, "A quarter of all holders hold under a dollar."))
body.append(txt(60, yb + 74, 22, BAD, f"Retention: 32.6%", 700))
body.append(txt(260, yb + 74, 19, SUB, f"{EVER:,} addresses have held $FET. {HEADLINE:,} still do."))
render("fet-holders", 1200, yb + 110, "".join(body))
