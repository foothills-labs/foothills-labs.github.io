#!/usr/bin/env python3
"""Generate the contour bands used on the site.

Same principle as the marks in foundation_lab: the drawing is generated, not
hand-drawn, and the irregularity is deliberate. The lines are not perfectly
parallel — each carries its own phase drift — because a regularised version
reads as sterile. See docs/brand.md in foundation_lab.

Two bands are emitted:

  hero   a contour section under the hero, lines only
  seam   a boundary between two schemes, drawn as a mountain range: the
         incoming scheme's ground rises as a line-hatched ridge line into the
         outgoing scheme's sky. Each peak is filled with the incoming ground
         and hatched with nested slope lines converging toward its apex, so
         nearer peaks occlude the ones behind them the way ridges do.

The viewBox is fitted to the drawing after generation, so no line is ever
clipped mid-stroke at the edge of the SVG.

Run:  python3 assets/brand/contours.py
Paste the output into index.html. The SVG has to be inline — it reads
currentColor and the scheme custom properties, which an <img> cannot.
"""

import math
import random

W = 1440
CAP = 3.0  # breathing room for round line caps, in viewBox units


def curve_pts(base, amp, phase, drift, n=96):
    """One contour line sampled across the width, as a point list.

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
        pts.append((x, y))
    return pts


def path(pts):
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.2f}"
    for x, y in pts[1:]:
        d += f"L{x:.0f} {y:.2f}"
    return d


def band(base, gap, count, amp, direction=1, phase0=0.0):
    """A family of contour lines marching away from `base`."""
    out = []
    for k in range(count):
        # Gap widens slightly with distance: aerial perspective, not a grid.
        offset = sum(gap * (1 + 0.13 * j) for j in range(k))
        out.append(
            curve_pts(
                base=base + direction * offset,
                amp=amp * (1 - 0.05 * k),
                phase=phase0 + 0.34 * k,
                drift=7 - 2.4 * k,
            )
        )
    return out


def fit(line_groups):
    """Shift every line down so the topmost point sits at CAP, and return the
    fitted viewBox height. This is what stops lines clipping at either edge."""
    ymin = min(y for lines in line_groups for pts in lines for _, y in pts)
    ymax = max(y for lines in line_groups for pts in lines for _, y in pts)
    dy = CAP - ymin
    for lines in line_groups:
        for i, pts in enumerate(lines):
            lines[i] = [(x, y + dy) for x, y in pts]
    return math.ceil(ymax + dy + CAP)


def hero():
    """Lines only, fading downward. Sits under the hero copy."""
    lines = band(base=0, gap=13, count=7, amp=13, phase0=0.4)
    h = fit([lines])
    parts = []
    for i, pts in enumerate(lines):
        parts.append(f'<path d="{path(pts)}" opacity="{1 - i * 0.115:.2f}"/>')
    return (
        f'<svg class="contours" viewBox="0 0 {W} {h}" preserveAspectRatio="none" '
        f'aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.6" '
        f'stroke-linecap="round">{"".join(parts)}</g></svg>'
    )


def _peak(cx, hw, ph, skew, rng, h):
    """One peak's outline, base-left to apex to base-right, with slope kinks.

    The kinks put a bend in each face the way real ridge profiles have —
    perfectly straight slopes read as a logo triangle, not terrain.
    """
    ax = cx + skew * hw
    apex = (ax, h - ph)
    left, right = (cx - hw, h), (cx + hw, h)
    pts = [left]
    for t in (0.42, 0.74):
        x = left[0] + (apex[0] - left[0]) * t
        y = left[1] + (apex[1] - left[1]) * t + rng.uniform(-0.09, 0.05) * ph
        pts.append((x, y))
    pts.append(apex)
    for t in (0.26, 0.58):
        x = apex[0] + (right[0] - apex[0]) * t
        y = apex[1] + (right[1] - apex[1]) * t + rng.uniform(-0.09, 0.05) * ph
        pts.append((x, y))
    pts.append(right)
    return pts, apex


def seam(seed=7):
    """A scheme boundary drawn as a mountain range.

    Each peak is a filled ridge profile hatched with nested slope lines that
    converge toward the apex. Peaks are drawn in a shuffled order so nearer
    ones occlude the ones behind, and every base sits on the bottom edge, so
    the range is continuous with the incoming scheme's ground below it.
    style.css sets the fill and ink per seam direction.
    """
    rng = random.Random(seed)
    h = 176

    peaks = []
    x = -70.0
    while x < W + 80:
        hw = rng.uniform(105, 215)
        ph = rng.uniform(52, 158)
        skew = rng.uniform(-0.3, 0.3)
        peaks.append(_peak(x + rng.uniform(-28, 28), hw, ph, skew, rng, h))
        x += rng.uniform(112, 152)
    rng.shuffle(peaks)

    parts = []
    for pts, apex in peaks:
        outline = path(pts)
        fill = f"{outline}Z"
        ph = h - apex[1]
        # Nested slope lines: shrunken copies of the outline pulled toward the
        # point below the apex, denser on taller peaks.
        n = 4 + int(ph / 26)
        hatch = []
        for k in range(1, n + 1):
            t = 1 - k / (n + 1.15)
            shrunk = [(apex[0] + (px - apex[0]) * t, h + (py - h) * t)
                      for px, py in pts]
            hatch.append(f'<path d="{path(shrunk)}"/>')
        parts.append(
            f'<path class="range-fill" stroke="none" d="{fill}"/>'
            f'<g class="range-hatch" fill="none" stroke-width="1.5">{"".join(hatch)}</g>'
            f'<path class="range-crest" fill="none" stroke-width="2.4" d="{outline}"/>'
        )

    base = f'<rect class="range-fill" x="0" y="{h - 3}" width="{W}" height="3" stroke="none"/>'
    return (
        f'<svg class="seam" viewBox="0 0 {W} {h}" preserveAspectRatio="none" '
        f'aria-hidden="true"><g stroke-linejoin="round" stroke-linecap="round">'
        f'{"".join(parts)}{base}</g></svg>'
    )


if __name__ == "__main__":
    print("<!-- hero -->")
    print(hero())
    print()
    print("<!-- seam down -->")
    print(seam(seed=7))
    print()
    print("<!-- seam up -->")
    print(seam(seed=23))
