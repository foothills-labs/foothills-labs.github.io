#!/usr/bin/env python3
"""Generate the fold-line art used on the site.

Replaces contours.py, which drew terrain. Same principle as the marks in
foundation_lab: the drawing is generated, not hand-drawn, and the slight
irregularity is deliberate — a regularised version reads as sterile. See
docs/brand.md in foundation_lab.

Two pieces are emitted:

  creases  a crease field under the hero. Straight segments meeting at fold
           intersections, not smooth curves — that is the whole difference
           between a crease and a contour. Follows the origami drafting
           convention: VALLEY folds dashed, MOUNTAIN folds solid. The
           convention is real, so the drawing means something to anyone who
           has ever followed a fold diagram.

  seam     a boundary between two schemes, drawn as a pleated edge: the
           accordion the house mark is made of, seen along its length. The
           incoming scheme's ground fills below the zigzag and the pleat
           returns are drawn in, so the seam is the mark's own construction
           at page scale.

Everything is seeded, so re-running produces byte-identical output.

Run:  python3 assets/brand/folds.py
Paste the output into index.html. The SVG has to be inline — it reads
currentColor and the scheme custom properties, which an <img> cannot.
"""

import math
import random

W = 1440
CAP = 3.0  # breathing room for round line caps, in viewBox units


def path(pts):
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.2f}"
    for x, y in pts[1:]:
        d += f"L{x:.0f} {y:.2f}"
    return d


def crease(y0, angles, rng, jitter=1.6):
    """One crease: straight runs that change angle at fold intersections.

    `angles` is a list of (fraction_of_width, slope) — the slope changes at
    each intersection, which is what a crease does and a contour never does.
    """
    pts = [(0.0, y0)]
    x, y = 0.0, y0
    for frac, slope in angles:
        nx = min(W, x + W * frac)
        ny = y + (nx - x) * slope
        pts.append((nx, ny + rng.uniform(-jitter, jitter)))
        x, y = nx, ny
    if x < W:
        pts.append((W, y + (W - x) * angles[-1][1]))
    return pts


def fit(groups):
    """Shift everything so the topmost point sits at CAP; return viewBox height."""
    ys = [y for g in groups for pts, _ in g for _, y in pts]
    ymin, ymax = min(ys), max(ys)
    dy = CAP - ymin
    for g in groups:
        for i, (pts, kind) in enumerate(g):
            g[i] = ([(x, y + dy) for x, y in pts], kind)
    return math.ceil(ymax + dy + CAP)


def creases(seed=11):
    """The crease field under the hero. Lines only, fading downward.

    Slopes are deliberately steep and varied: a crease changes direction at
    an intersection and runs at an angle, which is exactly what separates it
    from a contour. Shallow near-parallel lines read as a smudge.
    """
    rng = random.Random(seed)
    lines = []
    y = 0.0
    for k in range(6):
        angles = [
            (rng.uniform(0.18, 0.30), rng.uniform(-0.16, -0.06)),
            (rng.uniform(0.22, 0.34), rng.uniform(0.05, 0.15)),
            (rng.uniform(0.18, 0.28), rng.uniform(-0.13, -0.03)),
            (rng.uniform(0.16, 0.26), rng.uniform(0.02, 0.11)),
        ]
        lines.append((crease(y, angles, rng, jitter=2.4),
                      "valley" if k % 2 else "mountain"))
        y += 21 * (1 + 0.06 * k)
    # Corner folds crossing the long creases at a steeper angle — the lines
    # that make a crease pattern read as foldable rather than as ruled paper.
    for _ in range(7):
        x0 = rng.uniform(40, W - 200)
        yy = rng.uniform(0, 96)
        run = rng.uniform(150, 320)
        drop = rng.uniform(38, 92) * rng.choice((-1, 1))
        lines.append(([(x0, yy), (x0 + run, yy + drop)],
                      rng.choice(("valley", "mountain"))))
    h = fit([lines])

    parts = []
    for i, (pts, kind) in enumerate(lines):
        dash = ' stroke-dasharray="11 8"' if kind == "valley" else ""
        parts.append(f'<path d="{path(pts)}" opacity="{max(0.24, 1 - i * 0.075):.2f}"{dash}/>')
    return (
        f'<svg class="creases" viewBox="0 0 {W} {h}" preserveAspectRatio="none" '
        f'aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.4" '
        f'stroke-linecap="round" stroke-linejoin="round">{"".join(parts)}</g></svg>'
    )


def seam(seed=7):
    """A scheme boundary drawn as a pleated paper edge.

    The zigzag is the accordion the house mark is folded from. Each facet is
    filled separately and alternates tone — that alternation is what makes
    folded paper legible; an outline alone reads as a sawtooth graph. The
    bases sit on the incoming ground, so pleat and ground stay continuous.
    style.css sets the two tones and the ink per seam direction.
    """
    rng = random.Random(seed)
    h = 176

    pts = [(-40.0, h)]
    x = -40.0
    up = True
    while x < W + 60:
        x += rng.uniform(104, 176)
        y = (h - rng.uniform(86, 152)) if up else (h - rng.uniform(10, 40))
        pts.append((x, y))
        up = not up
    pts.append((x + 60, h))

    # One filled quad per facet, alternating tone: apex -> next apex -> base.
    facets = []
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        cls = "fold-fill" if i % 2 == 0 else "fold-facet"
        d = f"M{x0:.0f} {y0:.2f}L{x1:.0f} {y1:.2f}L{x1:.0f} {h}L{x0:.0f} {h}Z"
        facets.append(f'<path class="{cls}" stroke="none" d="{d}"/>')

    crest = path(pts)
    returns = [
        f'<path d="M{px:.0f} {py:.2f}L{px:.0f} {h}"/>'
        for px, py in pts[1:-1] if py < h - 46
    ]

    return (
        f'<svg class="seam" viewBox="0 0 {W} {h}" preserveAspectRatio="none" '
        f'aria-hidden="true"><g stroke-linejoin="round" stroke-linecap="round">'
        f'{"".join(facets)}'
        f'<g class="fold-return" fill="none" stroke-width="1.4">{"".join(returns)}</g>'
        f'<path class="fold-crease" fill="none" stroke-width="2.4" d="{crest}"/>'
        f'</g></svg>'
    )


if __name__ == "__main__":
    print("<!-- creases -->")
    print(creases())
    print()
    print("<!-- seam down -->")
    print(seam(seed=7))
    print()
    print("<!-- seam up -->")
    print(seam(seed=23))
