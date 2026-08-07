#!/usr/bin/env python3
"""Generate the contour bands used on the site.

Same principle as the marks in foundation_lab: the drawing is generated, not
hand-drawn, and the irregularity is deliberate. The lines are not perfectly
parallel — each carries its own phase drift — because a regularised version
reads as sterile. See docs/brand.md in foundation_lab.

Two bands are emitted:

  hero   a contour section under the hero, lines only
  seam   a boundary between two schemes: the ground changes colour along a
         contour line, and the lines carry on across it, so the two halves of
         the lab meet on a drawn edge rather than a rectangle

Run:  python3 assets/brand/contours.py
Paste the output into index.html. The SVG has to be inline — it reads
currentColor and the scheme custom properties, which an <img> cannot.
"""

import math

W = 1440


def curve(base, amp, phase, drift, height, n=96):
    """One contour line sampled across the width, as an SVG path.

    `drift` tilts the line slightly end to end so no two are parallel.
    """
    pts = []
    for i in range(n + 1):
        x = W * i / n
        t = x / W
        y = (
            base
            + amp * math.sin(2 * math.pi * 0.9 * t + phase)
            + amp * 0.45 * math.sin(2 * math.pi * 2.3 * t + phase * 1.7)
            + amp * 0.22 * math.sin(2 * math.pi * 4.1 * t + phase * 0.6)
            + drift * (t - 0.5)
        )
        pts.append((x, max(-40.0, min(height + 40.0, y))))
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.2f}"
    for x, y in pts[1:]:
        d += f"L{x:.0f} {y:.2f}"
    return d


def band(base, gap, count, amp, height, direction=1, phase0=0.0):
    """A family of contour lines marching away from `base`."""
    out = []
    for k in range(count):
        # Gap widens slightly with distance: aerial perspective, not a grid.
        offset = sum(gap * (1 + 0.13 * j) for j in range(k))
        out.append(
            curve(
                base=base + direction * offset,
                amp=amp * (1 - 0.05 * k),
                phase=phase0 + 0.34 * k,
                drift=7 - 2.4 * k,
                height=height,
            )
        )
    return out


def hero():
    """Lines only, fading downward. Sits under the hero copy."""
    h = 150
    lines = band(base=52, gap=13, count=7, amp=13, height=h, phase0=0.4)
    parts = []
    for i, d in enumerate(lines):
        parts.append(f'<path d="{d}" opacity="{1 - i * 0.115:.2f}"/>')
    return (
        f'<svg class="contours" viewBox="0 0 {W} {h}" preserveAspectRatio="none" '
        f'aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.6" '
        f'stroke-linecap="round">{"".join(parts)}</g></svg>'
    )


def seam(flip=False):
    """A scheme boundary drawn as a contour.

    The filled path is the destination ground; its top edge IS a contour line.
    Lines above it belong to the outgoing scheme, lines below to the incoming
    one, so the drawing crosses the join.
    """
    h = 118
    base = 62
    edge = curve(base=base, amp=11, phase=0.9, drift=6, height=h)

    above = band(base=base - 11, gap=12, count=5, amp=11, height=h,
                 direction=-1, phase0=1.24)
    below = band(base=base + 13, gap=12, count=4, amp=10.5, height=h,
                 direction=1, phase0=1.6)

    a = "".join(
        f'<path d="{d}" opacity="{0.78 - i * 0.13:.2f}"/>' for i, d in enumerate(above)
    )
    b = "".join(
        f'<path d="{d}" opacity="{0.5 - i * 0.1:.2f}"/>' for i, d in enumerate(below)
    )

    ground = f'{edge}L{W} {h}L0 {h}Z'
    cls = "seam seam--up" if flip else "seam"
    return (
        f'<svg class="{cls}" viewBox="0 0 {W} {h}" preserveAspectRatio="none" '
        f'aria-hidden="true">'
        f'<path class="seam-ground" d="{ground}"/>'
        f'<g class="seam-from" fill="none" stroke-width="2.4" stroke-linecap="round">{a}</g>'
        f'<g class="seam-to" fill="none" stroke-width="2.4" stroke-linecap="round">{b}</g>'
        f"</svg>"
    )


if __name__ == "__main__":
    print("<!-- hero -->")
    print(hero())
    print()
    print("<!-- seam -->")
    print(seam())
