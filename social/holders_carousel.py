#!/usr/bin/env python3
"""Instagram carousel for the Proof of Crowd account: what a holder count counts.

The site palette and the serif, not the personal chart house style, because
this runs on the brand account. Layout, wrapping and the overflow guard come
from the crowd-check carousel module; only the colours and the voice change.

Reads the same out/*-wallets.json the holder card does, so the carousel and
the card cannot drift. Shares are taken over wallets, never over the headline
count, because the buckets behind with_100_usd skip every address that is not
a wallet.

Usage: python3 social/holders_carousel.py
"""

import glob
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path.home() / "lunarcrush-projects/projects/crowd-check"))

from carousel import W, H, M, Flow, txt  # noqa: E402

SRC = Path.home() / "proof-of-crowd-tools" / "out"
OUT = HERE / "instagram"
SHARP = Path.home() / "lunarcrush-projects/projects/crowd-size/node_modules/sharp"
TOTAL, STEM = 5, "holders"

# Straight from styles.css, so the carousel and the site cannot drift apart.
BG, PANEL, LINE = "#f6f3ec", "#ffffff", "#ded8cd"
TEXT, SUB, BRAND, BAD = "#15171c", "#6e6a60", "#1b3a6b", "#a33228"
SERIF = "Charter, Georgia, 'Times New Roman', serif"


def frame(n: int, body: str, footer: str = "") -> str:
    dots = "".join(
        f'<circle cx="{W/2 + (i - (TOTAL-1)/2) * 36}" cy="{H-60}" r="7" '
        f'fill="{BRAND if i == n-1 else LINE}"/>' for i in range(TOTAL))
    f = txt(M, H - 112, 27, SUB, footer) if footer else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" font-family="{SERIF}">'
            f'<rect width="{W}" height="{H}" fill="{BG}"/>'
            f'<rect x="0" y="0" width="{W}" height="10" fill="{BRAND}"/>'
            f'{txt(M, 112, 27, SUB, "PROOF OF CROWD", 700)}'
            f'{txt(W-M, 112, 27, SUB, f"{n}/{TOTAL}", 400, "end")}'
            f'{body}{f}{dots}</svg>')


def load():
    rows = []
    for p in sorted(glob.glob(str(SRC / "*-wallets.json"))):
        d = json.loads(Path(p).read_text())
        h, w = d.get("holders_headline") or 0, d.get("wallets") or 0
        if not (h and w):
            continue
        rows.append({"sym": d["symbol"], "holders": h, "wallets": w,
                     "big": d.get("with_100_usd") or 0})
    for r in rows:
        r["big_s"] = r["big"] / r["wallets"]
        r["ghost_s"] = (r["holders"] - r["wallets"]) / r["holders"]
    return rows


def bars(f: Flow, rows, value, hot) -> None:
    BW, BH = W - 2 * M - 190, 54
    top = max(value(r) for r in rows)
    for r in rows:
        v = value(r)
        w = max(BW * v / top, 3)
        col = BAD if r["sym"] in hot else BRAND
        f.raw(txt(M, f.y + 38, 30, TEXT, "$" + r["sym"], 700))
        f.raw(f'<rect x="{M+190}" y="{f.y+8}" width="{BW}" height="{BH}" rx="6" fill="{PANEL}"/>')
        f.raw(f'<rect x="{M+190}" y="{f.y+8}" width="{w:.0f}" height="{BH}" rx="6" fill="{col}"/>')
        inside = w > 125
        f.raw(txt(M + 190 + w - (18 if inside else -14), f.y + 46, 32,
                  BG if inside else TEXT, f"{v*100:.1f}%", 700,
                  "end" if inside else "start"))
        f.y += BH + 16


def slide1(rows) -> str:
    f = Flow(470)
    f.say(60, TEXT, "Every project leads with a holder count.", 700, gap=48)
    f.say(44, SUB, "Almost none say what those holders hold.", gap=72)
    f.say(46, BRAND, "Every balance here was read from the chain.", 700, gap=0)
    return frame(1, f.svg(), "swipe")


def slide2(rows) -> str:
    a = next(r for r in rows if r["sym"] == "AZTEC")
    f = Flow(300)
    f.say(52, TEXT, "The first thing it hides", 700, gap=40)
    f.say(38, SUB, "Not every holder is a person. Contracts, exchange wallets "
                   "and burn addresses all count as one holder each.", gap=56)
    f.raw(txt(M, f.y + 20, 92, SUB, f"{a['holders']:,}", 700))
    f.raw(txt(M, f.y + 70, 32, SUB, "addresses hold $AZTEC"))
    f.y += 150
    f.raw(txt(M, f.y + 20, 92, BRAND, f"{a['wallets']:,}", 700))
    f.raw(txt(M, f.y + 70, 32, SUB, "of them are wallets"))
    f.y += 158
    f.say(40, TEXT, "Three in five were never a person to begin with.", 700, gap=0)
    return frame(2, f.svg())


def slide3(rows) -> str:
    r = sorted(rows, key=lambda x: -x["ghost_s"])
    f = Flow(300)
    f.say(50, TEXT, "Share that is not a wallet", 700, gap=18)
    f.say(32, SUB, "Of the holder count each project quotes.", gap=46)
    bars(f, r, lambda x: x["ghost_s"], ("AZTEC", "ZAMA"))
    return frame(3, f.svg())


def slide4(rows) -> str:
    r = sorted(rows, key=lambda x: -x["big_s"])
    f = Flow(300)
    f.say(50, TEXT, "The second thing it hides", 700, gap=18)
    f.say(32, SUB, "Wallets holding $100 or more, contracts removed.", gap=46)
    bars(f, r, lambda x: x["big_s"], ("APE", "BLUR"))
    return frame(4, f.svg())


def slide5(rows) -> str:
    b = next(r for r in rows if r["sym"] == "BLUR")
    f = Flow(400)
    f.say(52, TEXT, "Put that another way", 700, gap=46)
    f.say(40, TEXT, f"$BLUR reports {b['holders']:,} holders. "
                    f"{b['wallets']:,} are wallets, and {b['big']:,} of those "
                    f"hold $100 or more.", 700, gap=50)
    f.say(36, SUB, "A holder count treats eleven cents exactly as it treats "
                   "eleven thousand dollars.", gap=50)
    f.say(32, SUB, "Dollar thresholds move with price, so a token that has "
                   "fallen shows more residue without its holders having "
                   "changed.", gap=0)
    return frame(5, f.svg(), "proofofcrowd.com")


def main() -> None:
    rows = load()
    OUT.mkdir(parents=True, exist_ok=True)
    for i, fn in enumerate((slide1, slide2, slide3, slide4, slide5), 1):
        p = OUT / f"{STEM}-{i}.svg"
        p.write_text(fn(rows))
        subprocess.run(["node", "-e",
            f"const s=require('{SHARP}');s('{p}',{{density:144}})"
            f".resize({W*2},{H*2}).png().toFile('{OUT}/{STEM}-{i}.png')"
            f".then(r=>console.log('  slide {i}  '+r.width+'x'+r.height));"], check=True)


if __name__ == "__main__":
    main()
