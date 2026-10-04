#!/usr/bin/env python3
"""Build the social share card.

A link to this site posted on LinkedIn or X is the main way a buyer arrives,
and without og: tags it renders as a bare URL with no title, image or
description. 1200x630 is the size both platforms crop to.

Usage: python3 assets/make_og.py   (writes assets/og.png)
"""

import importlib.util
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The mark comes from the logo generator rather than a copy, so the card can
# never drift from the favicon and the wordmark.
_spec = importlib.util.spec_from_file_location("make_logo", HERE / "make_logo.py")
_logo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_logo)
BG, TEXT, SUB, GREEN, PANEL = "#f6f3ec", "#15171c", "#6e6a60", "#1b3a6b", "#ffffff"
FONT = "Charter, Georgia, serif"
MONO = "Menlo, ui-monospace, monospace"
W, H = 1200, 630


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# The hand-set word spacing that used to live here is gone. It existed because
# librsvg faked a bold Helvetica by double-striking glyphs, which swallowed the
# spaces. Charter ships a real bold, so real spaces work and the old hack would
# now double them.


def txt(x, y, size, fill, s, weight=400) -> str:
    body = esc(s)
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" font-family="{FONT}">{body}</text>')


svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect x="0" y="0" width="{W}" height="8" fill="{GREEN}"/>
<g transform="translate(866,196) scale(3.5)" opacity="1">{_logo.mark()}</g>
{txt(72, 112, 26, SUB, "PROOF OF CROWD")}
{txt(72, 212, 62, TEXT, "Is that token's", 700)}
{txt(72, 284, 62, TEXT, "community real?", 700)}
{txt(72, 356, 27, SUB, "Evidence-based attention audits. Spam analysis,")}
{txt(72, 396, 27, SUB, "creator concentration, decay signatures.")}
<rect x="72" y="446" width="1056" height="1" fill="#ded8cd"/>
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
