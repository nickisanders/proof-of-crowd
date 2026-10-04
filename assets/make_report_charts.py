#!/usr/bin/env python3
"""The two figures in the sample report, in the Dossier palette.

These used to exist only as PNGs with no generator, which meant a palette
change could not reach them. The numbers are the ones published in
sample.html, so this script is the record of how the figures were drawn.

Usage: python3 assets/make_report_charts.py
"""

import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARP = "/Users/nicki/lunarcrush-projects/projects/crowd-size/node_modules/sharp"
FONT = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

GROUND, INK, SUB, RULE = "#ffffff", "#15171c", "#6e6a60", "#ded8cd"
NEUTRAL, OK, BAD = "#8d8578", "#236440", "#a33228"   # all clear 3:1 on white


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def heavy(text, size):
    """librsvg drops word spaces at bold weights, so set them by hand."""
    w = text.split(" ")
    out = [esc(w[0])]
    for prev, nxt in zip(w, w[1:]):
        out.append(f'<tspan dx="{size * (0.45 if prev.endswith("%") else 0.30):.0f}">{esc(nxt)}</tspan>')
    return "".join(out)


def txt(x, y, size, fill, s, weight=400, anchor="start"):
    body = heavy(s, size) if weight >= 700 and " " in s else esc(s)
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}" font-family="{FONT}">{body}</text>')


def render(name, w, h, body, scale=2):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{GROUND}"/>{body}</svg>')
    (HERE / f"{name}.svg").write_text(svg)
    subprocess.run(["node", "-e",
        f"const s=require('{SHARP}');s('{HERE}/{name}.svg',{{density:144}})"
        f".resize({w * scale},{h * scale}).png().toFile('{HERE}/{name}.png')"
        f".then(i=>console.log('{name}.png',i.width+'x'+i.height));"], check=True)


# ---------------------------------------------------------------------- decay
DAYS = [("Jul 27", 325_000, "325k"), ("Jul 28", 484_000, "484k"), ("Jul 29", 359_000, "359k"),
        ("Jul 30", 1_100_000, "1.1M"), ("Jul 31", 2_100_000, "2.1M"), ("Aug 1", 130_000, "130k"),
        ("Aug 2", 68_000, "68k"), ("Aug 3", 57_000, "57k")]
BASE, MAXH, GAP, X0, SPAN = 560, 400, 22, 60, 1080
bw = (SPAN - GAP * (len(DAYS) - 1)) / len(DAYS)
peak = max(v for _, v, _ in DAYS)

body = [txt(60, 58, 38, INK, "$ZAMA: what happened after the spike", 700),
        txt(60, 92, 21, SUB, "daily social interactions · flagged 99/100 on 2026-07-31")]
for i, (day, val, label) in enumerate(DAYS):
    x, h = X0 + i * (bw + GAP), MAXH * val / peak
    flagged = day == "Jul 31"
    body.append(f'<rect x="{x:.1f}" y="{BASE - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="4" '
                f'fill="{BAD if flagged else NEUTRAL}"/>')
    body.append(txt(x + bw / 2, BASE - h - 14, 24, BAD if flagged else INK, label, 700, "middle"))
    body.append(txt(x + bw / 2, 592, 19, SUB, day, 400, "middle"))
body += [f'<rect x="60" y="{BASE}" width="{SPAN}" height="1.5" fill="{RULE}"/>',
         txt(60, 644, 24, INK, "Latest day retains 3% of the spike's volume.", 700),
         txt(60, 676, 17, SUB, "Data: LunarCrush · one-hour half-life is normal for ALL crypto "
                               "attention · methodology in the repo")]
render("zama-decay", 1200, 700, "".join(body))

# ----------------------------------------------------------------- conversion
COLS = [("Ordinary day", "baseline conversion", 979, NEUTRAL),
        ("Jul 23 spike", "1.5M interactions · 449 wallets", 302, OK),
        ("Jul 31 spike", "2.1M interactions · 73 wallets", 35, BAD)]
BASE2, MAXH2, CW = 600, 390, 260
top = max(v for *_, v, _ in COLS)

body = [txt(60, 56, 38, INK, "Attention in, wallets out", 700),
        txt(60, 92, 21, SUB, "new first-time holders per million interactions · $ZAMA · "
                             "Ethereum + BNB Chain"),
        txt(60, 124, 19, SUB, "The flagged spike brought the most attention and the fewest wallets.")]
for i, (label, note, val, color) in enumerate(COLS):
    x = 80 + i * (CW + 130)
    h = max(10, MAXH2 * val / top)
    body.append(f'<rect x="{x}" y="{BASE2 - h:.1f}" width="{CW}" height="{h:.1f}" rx="4" fill="{color}"/>')
    body.append(txt(x + CW / 2, BASE2 - h - 16, 34, color, str(val), 700, "middle"))
    body.append(txt(x + CW / 2, 642, 24, INK, label, 400, "middle"))
    body.append(txt(x + CW / 2, 672, 18, SUB, note, 400, "middle"))
body += [f'<rect x="60" y="{BASE2}" width="1080" height="1.5" fill="{RULE}"/>',
         txt(60, 730, 17, SUB, "First-time token receipts via Dune · Solana deployment not "
                               "measured (see report) · holders are a proxy, not a headcount")]
render("zama-conversion", 1200, 760, "".join(body))
