#!/usr/bin/env python3
"""Build the social share card.

A link to this site posted on LinkedIn or X is the main way a buyer arrives,
and without og: tags it renders as a bare URL with no title, image or
description. 1200x630 is the size both platforms crop to.

Usage: python3 assets/make_og.py   (writes assets/og.png)
"""

import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
BG, TEXT, SUB, GREEN, PANEL = "#0d1117", "#e6edf3", "#8b949e", "#3fb950", "#161b22"
FONT = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
W, H = 1200, 630


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def heavy(text: str, size: int) -> str:
    """librsvg drops word spaces at bold weights, so space the words by hand."""
    words = text.split(" ")
    parts = [esc(words[0])]
    for prev, w in zip(words, words[1:]):
        parts.append(f'<tspan dx="{size * (0.45 if prev.endswith('%') else 0.30):.0f}">{esc(w)}</tspan>')
    return "".join(parts)


def txt(x, y, size, fill, s, weight=400) -> str:
    body = heavy(s, size) if weight >= 700 and " " in s else esc(s)
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" font-family="{FONT}">{body}</text>')


svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect x="0" y="0" width="{W}" height="8" fill="{GREEN}"/>
{txt(72, 112, 26, SUB, "PROOF OF CROWD")}
{txt(72, 212, 62, TEXT, "Is that token's", 800)}
{txt(72, 284, 62, TEXT, "community real?", 800)}
{txt(72, 356, 27, SUB, "Evidence-based attention audits. Spam analysis,")}
{txt(72, 396, 27, SUB, "creator concentration, decay signatures.")}
<rect x="72" y="446" width="1056" height="1" fill="#21262d"/>
{txt(72, 508, 24, TEXT, "Open methodology, published daily.", 700)}
{txt(72, 548, 22, SUB, "The fee buys the audit, not the answer.")}
{txt(72, 592, 22, GREEN, "proofofcrowd.com", 700)}
</svg>"""

(HERE / "og.svg").write_text(svg)
subprocess.run([
    "node", "-e",
    "const s=require('/Users/nicki/lunarcrush-projects/projects/crowd-size/node_modules/sharp');"
    f"s('{HERE}/og.svg',{{density:144}}).resize({W},{H}).png().toFile('{HERE}/og.png')"
    ".then(i=>console.log('og.png',i.width+'x'+i.height));"
], check=True)
