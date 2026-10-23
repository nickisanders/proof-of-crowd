#!/usr/bin/env python3
"""The mark laid out in candy, rendered to look photographed.

The geometry comes from assets/logo-mark-bare.svg rather than from an image
model, because the joke only works if the mark is exactly right: 55 dots in
four arcs of 6, 11, 16 and 21 around a centre. A generator will not hold a
count or an arc, and a mark that is nearly the mark is just a pile of sweets.

What makes it read as a photograph rather than a render, in order of how much
each one mattered: the pieces are flattened lenses with a visible side wall,
not domes; each throws a tight contact shadow as well as a soft ambient one;
the side wall shows on the side facing away from the lens, which is what tells
the eye the camera is above the middle; and the table has its own scratches,
blotches and falloff. The first pass had none of that and looked like clip art.

Usage: python3 social/mm_photo.py
"""

import math
import random
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SHARP = Path.home() / "lunarcrush-projects/projects/crowd-size/node_modules/sharp"
W, H = 1400, 1060
SEED = 7              # fixed, so a re-render is the same photograph

# Real plain M&M blue sits brighter and greener than the brand navy. Matching
# the brand would read as a render, so these come from the bag, not the
# palette, and they vary because sweets in one bag vary.
BLUES = [("#2d6ab4", "#7fb0e8", "#14375f"),
         ("#2a62a8", "#76a8e2", "#123257"),
         ("#3576bd", "#89bbee", "#184272"),
         ("#27609f", "#6fa2dd", "#102d4f")]
CENTRE = ("#c45330", "#eb9a76", "#7d2f15")


def dots():
    src = (ROOT / "assets" / "logo-mark-bare.svg").read_text()
    return [(float(x), float(y), float(r)) for x, y, r in
            re.findall(r'cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"', src)]


def table(rng) -> str:
    """Scratches and blotches. An evenly lit, evenly coloured surface is the
    single loudest tell that nothing was ever on a table."""
    out = []
    for _ in range(34):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        ln = rng.uniform(26, 190)
        a = rng.uniform(-0.5, 0.5)
        out.append(
            f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+ln*math.cos(a):.0f}" '
            f'y2="{y+ln*math.sin(a):.0f}" stroke="#ffffff" '
            f'stroke-opacity="{rng.uniform(0.20, 0.55):.2f}" '
            f'stroke-width="{rng.uniform(0.6, 1.5):.1f}"/>')
    for _ in range(16):
        out.append(
            f'<ellipse cx="{rng.uniform(0, W):.0f}" cy="{rng.uniform(0, H):.0f}" '
            f'rx="{rng.uniform(60, 240):.0f}" ry="{rng.uniform(40, 170):.0f}" '
            f'fill="#cfc9bd" opacity="{rng.uniform(0.03, 0.08):.3f}" '
            f'filter="url(#blotch)"/>')
    return "".join(out)


def main() -> None:
    rng = random.Random(SEED)
    d = dots()
    xs = [p[0] for p in d]
    ys = [p[1] for p in d]
    span = max(xs) - min(xs)
    scale = (W * 0.78) / span
    ox = (W - span * scale) / 2 - min(xs) * scale
    oy = (H - (max(ys) - min(ys)) * scale) / 2 - min(ys) * scale

    defs = [
        '<filter id="grain"><feTurbulence type="fractalNoise" '
        'baseFrequency="0.85" numOctaves="4"/>'
        '<feColorMatrix type="saturate" values="0"/></filter>',
        '<filter id="blotch" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur stdDeviation="38"/></filter>',
        '<filter id="amb" x="-70%" y="-70%" width="240%" height="240%">'
        '<feGaussianBlur stdDeviation="11"/></filter>',
        '<filter id="contact" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="2.4"/></filter>',
        '<filter id="spec" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="2.2"/></filter>',
        '<filter id="hz" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="1.1"/></filter>',
        '<radialGradient id="table" cx="36%" cy="24%" r="92%">'
        '<stop offset="0" stop-color="#fcfbf9"/>'
        '<stop offset="0.55" stop-color="#f2f0ea"/>'
        '<stop offset="1" stop-color="#d9d4ca"/></radialGradient>',
        '<radialGradient id="vig" cx="50%" cy="46%" r="74%">'
        '<stop offset="0.55" stop-color="#000000" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#241f17" stop-opacity="0.26"/>'
        '</radialGradient>']

    for i, (base, lit, rim) in enumerate(BLUES + [CENTRE]):
        defs.append(
            f'<radialGradient id="c{i}" cx="38%" cy="33%" r="78%">'
            f'<stop offset="0" stop-color="{lit}"/>'
            f'<stop offset="0.30" stop-color="{base}"/>'
            f'<stop offset="0.74" stop-color="{base}"/>'
            f'<stop offset="0.90" stop-color="{rim}" stop-opacity="0.75"/>'
            f'<stop offset="1" stop-color="{rim}"/></radialGradient>')
        defs.append(
            f'<linearGradient id="w{i}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{base}"/>'
            f'<stop offset="1" stop-color="{rim}"/></linearGradient>')

    shadows, bodies = [], []
    for x, y, r in d:
        centre = r > 2.0
        cx = x * scale + ox + rng.uniform(-3.0, 3.0)
        cy = y * scale + oy + rng.uniform(-3.0, 3.0)
        rad = r * scale * (1.17 if centre else rng.uniform(0.89, 1.09))
        gid = 4 if centre else rng.randrange(4)
        tilt = rng.uniform(-30, 30)
        ry = rad * rng.uniform(0.95, 0.99)

        # Direction away from the lens axis. The side wall shows on that side,
        # which is the cue that reads as "photographed from above the middle".
        dx, dy = cx - W / 2, cy - H * 0.47
        m = math.hypot(dx, dy) or 1
        off = min(m / (W * 0.60), 1.0) * rad * 0.17
        wx, wy = dx / m * off, dy / m * off

        o1, o2 = rng.uniform(0.22, 0.36), rng.uniform(0.26, 0.42)
        shadows.append(
            f'<ellipse cx="{cx+rad*0.16:.1f}" cy="{cy+rad*0.24:.1f}" '
            f'rx="{rad*1.14:.1f}" ry="{ry*0.98:.1f}" fill="#564f44" '
            f'opacity="{o1:.2f}" filter="url(#amb)"/>'
            f'<ellipse cx="{cx+rad*0.05:.1f}" cy="{cy+rad*0.09:.1f}" '
            f'rx="{rad*0.97:.1f}" ry="{ry*0.86:.1f}" fill="#3b352c" '
            f'opacity="{o2:.2f}" filter="url(#contact)"/>')

        g = [f'<g transform="rotate({tilt:.1f} {cx:.1f} {cy:.1f})">']
        # side wall, then the glazed top face shifted back over it
        g.append(f'<ellipse cx="{cx+wx:.1f}" cy="{cy+wy:.1f}" rx="{rad:.1f}" '
                 f'ry="{ry:.1f}" fill="url(#w{gid})"/>')
        g.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rad*0.985:.1f}" '
                 f'ry="{ry*0.985:.1f}" fill="url(#c{gid})"/>')
        # tight primary specular, loose secondary, faint bounce at the base
        g.append(f'<ellipse cx="{cx-rad*0.33:.1f}" cy="{cy-ry*0.38:.1f}" '
                 f'rx="{rad*0.20:.1f}" ry="{ry*0.13:.1f}" fill="#ffffff" '
                 f'opacity="{rng.uniform(0.72, 0.92):.2f}" filter="url(#spec)"/>')
        g.append(f'<ellipse cx="{cx-rad*0.16:.1f}" cy="{cy-ry*0.20:.1f}" '
                 f'rx="{rad*0.44:.1f}" ry="{ry*0.30:.1f}" fill="#ffffff" '
                 f'opacity="{rng.uniform(0.10, 0.18):.2f}" filter="url(#hz)"/>')
        g.append(f'<ellipse cx="{cx+rad*0.18:.1f}" cy="{cy+ry*0.46:.1f}" '
                 f'rx="{rad*0.40:.1f}" ry="{ry*0.16:.1f}" fill="#bcd6f2" '
                 f'opacity="0.13" filter="url(#hz)"/>')
        if not centre and rng.random() < 0.40:
            g.append(f'<text x="{cx:.1f}" y="{cy+ry*0.17:.1f}" font-size="{rad*0.62:.1f}" '
                     f'fill="#ffffff" fill-opacity="{rng.uniform(0.30, 0.52):.2f}" '
                     f'text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
                     f'transform="rotate({rng.uniform(-180, 180):.0f} {cx:.1f} {cy:.1f})" '
                     f'filter="url(#hz)">m</text>')
        g.append('</g>')
        bodies.append("".join(g))

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}"><defs>{"".join(defs)}</defs>'
           f'<rect width="{W}" height="{H}" fill="url(#table)"/>'
           f'{table(rng)}'
           f'{"".join(shadows)}{"".join(bodies)}'
           f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
           f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity="0.085"/>'
           f'</svg>')

    out = HERE / "mm-photo.svg"
    out.write_text(svg)
    subprocess.run(["node", "-e",
        f"const s=require('{SHARP}');s('{out}',{{density:220}})"
        f".resize({W*2},{H*2}).png().toFile('{HERE}/mm-photo.png')"
        f".then(r=>console.log('  mm-photo.png '+r.width+'x'+r.height));"], check=True)


if __name__ == "__main__":
    main()
