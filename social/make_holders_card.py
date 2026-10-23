#!/usr/bin/env python3
"""Social card for the holder-quality finding, in the site's own palette.

Built for the Proof of Crowd account rather than the personal one, so it
carries the site's colours and the mark rather than the chart house style,
and it ends on the service rather than on the finding.

Reads out/*-wallets.json from proof-of-crowd-tools.

Usage: python3 social/make_holders_card.py
"""

import glob
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path.home() / "proof-of-crowd-tools" / "out"
SHARP = Path.home() / "lunarcrush-projects/projects/crowd-size/node_modules/sharp"

# Straight from styles.css, so the card and the site cannot drift apart.
BG, PANEL, LINE = "#f6f3ec", "#ffffff", "#ded8cd"
TEXT, SUB, BRAND, BAD = "#15171c", "#6e6a60", "#1b3a6b", "#a33228"
SERIF = "Charter, Georgia, 'Times New Roman', serif"
MONO = "Menlo, ui-monospace, monospace"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, size, fill, s, weight=400, anchor="start", font=None):
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}" '
            f'font-family="{font or SERIF}">{esc(s)}</text>')


rows = []
for p in sorted(glob.glob(str(SRC / "*-wallets.json"))):
    d = json.loads(Path(p).read_text())
    h = d.get("holders_headline") or 0
    if h:
        rows.append({"sym": d["symbol"], "holders": h,
                     "big": d.get("with_100_usd") or 0})
for r in rows:
    r["share"] = r["big"] / r["holders"]
rows.sort(key=lambda r: -r["share"])

W, H = 1200, 675
L, R = 64, 1136
b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
     f'<rect x="0" y="0" width="{W}" height="8" fill="{BRAND}"/>',
     txt(L, 58, 18, SUB, "PROOF OF CROWD", 700),
     txt(L, 108, 36, TEXT, "Every project leads with a holder count.", 700),
     txt(L, 150, 36, TEXT, "Almost none say what those holders hold.", 700),
     txt(L, 188, 19, SUB, "Share of holders with a position worth $100 or more.")]

BAR_L, BAR_W, BH = 200, 560, 32
y = 220
for r in rows:
    col = BAD if r["share"] < 0.10 else BRAND
    w = max(BAR_W * r["share"] / 0.40, 3)
    b.append(txt(L, y + BH - 11, 21, TEXT, "$" + r["sym"], 700, "start", MONO))
    b.append(f'<rect x="{BAR_L}" y="{y}" width="{BAR_W}" height="{BH}" fill="{PANEL}"/>')
    b.append(f'<rect x="{BAR_L}" y="{y}" width="{w:.0f}" height="{BH}" fill="{col}"/>')
    inside = w > 92
    b.append(txt(BAR_L + w - (12 if inside else -10), y + BH - 11, 20,
                 PANEL if inside else TEXT, f"{r['share']*100:.1f}%", 700,
                 "end" if inside else "start", MONO))
    b.append(txt(BAR_L + BAR_W + 28, y + BH - 11, 18, SUB,
                 f"{r['holders']:,} holders"))
    y += BH + 6

blur = next(r for r in rows if r["sym"] == "BLUR")
y += 16
b.append(f'<rect x="{L}" y="{y}" width="{R-L}" height="66" fill="{PANEL}"/>')
b.append(f'<rect x="{L}" y="{y}" width="5" height="66" fill="{BAD}"/>')
b.append(txt(L + 24, y + 29, 21, TEXT,
             f"$BLUR reports {blur['holders']:,} holders. {blur['big']:,} of them "
             f"hold more than $100.", 700))
b.append(txt(L + 24, y + 53, 18, SUB,
             "A holder count treats eleven cents exactly as it treats eleven "
             "thousand dollars."))

y += 92
b.append(f'<line x1="{L}" y1="{y}" x2="{R}" y2="{y}" stroke="{LINE}" stroke-width="2"/>')
b.append(txt(L, y + 28, 18, SUB, "Every balance read from the chain. Nothing sampled."))
b.append(txt(R, y + 28, 18, BRAND, "proofofcrowd.com", 700, "end"))

# A social card is a fixed 16:9, so content that runs past the bottom is
# cropped by the renderer rather than flagged. The first build lost the
# callout and the footer that way.
if y + 40 > H:
    raise SystemExit(f"content runs to y={y + 40}, past the {H}px card")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}">{"".join(b)}</svg>')
(HERE / "holders.svg").write_text(svg)
subprocess.run(["node", "-e",
    f"const s=require('{SHARP}');s('{HERE}/holders.svg',{{density:144}})"
    f".resize({W*2},{H*2}).png().toFile('{HERE}/holders.png')"
    f".then(i=>console.log('  holders.png',i.width+'x'+i.height));"], check=True)
