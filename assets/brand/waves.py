#!/usr/bin/env python3
"""Generate the wave art used on the site.

Replaces folds.py, whose crease field read as a tangle and whose pleated
seams read as a sawtooth. The language here is a single smooth wave, in the
register Material 3 uses for its wavy dividers and progress tracks: one
wavelength held across the whole drawing, generous amplitude, round caps.

Tidiness is the point, so it is enforced by construction rather than by
taste: every line in a set shares one wavelength and one amplitude law, and
lines are offset in phase rather than redrawn, so no two can ever cross.

  waves  a wave field under the hero. Lines nest, fading downward.
  seam   a boundary between two schemes: the incoming ground is filled to a
         wave edge, the edge itself is inked, and one echo rides above it.

Curves are exact cubic-Bezier sine arches, one per half wavelength. For an
arch of amplitude A over a half period L/2, control points at L/6 and L/3
with height 4A/3 put the curve's midpoint at exactly A, which is the closest
a single cubic gets to a sinusoid.

Everything is deterministic, so re-running produces byte-identical output.

Run:  python3 assets/brand/waves.py
Paste the output into index.html. The SVG has to be inline because it reads
currentColor and the scheme custom properties, which an <img> cannot.
"""

W = 1440


def wave(y, amp, wl, phase=0.0):
    """A smooth sinusoid as cubic Bezier arches, one per half wavelength.

    `phase` shifts the wave left in viewBox units; the SVG viewport clips the
    overhang, which is how lines are offset without changing their shape.
    """
    half = wl / 2.0
    # Whole arches only, so the line always leaves the frame mid-curve.
    n = int((W + phase) / half) + 2
    c = amp * 4.0 / 3.0
    sign = 1.0
    d = [f"M{-phase:.1f} {y:.2f}"]
    for _ in range(n):
        d.append(
            f"c{half / 3:.1f} {-c * sign:.2f} {half * 2 / 3:.1f} "
            f"{-c * sign:.2f} {half:.1f} 0"
        )
        sign = -sign
    return "".join(d)


def wave_area(y, amp, wl, phase, height):
    """The same wave, closed down to the bottom edge: a filled ground."""
    return f"{wave(y, amp, wl, phase)}V{height:.0f}H{-phase - 40:.0f}Z"


def waves(n=6, wl=600.0, amp=16.0, gap=22.0, top=28.0):
    """The wave field under the hero.

    One wavelength, one gap, one amplitude law. Successive lines take a
    constant phase step, so the set nests instead of tangling: the whole
    reason the crease field it replaces looked messy.
    """
    h = int(top + gap * (n - 1) + amp * 2 + 8)
    parts = []
    for k in range(n):
        a = amp * (1 - 0.085 * k)
        d = wave(y=top + gap * k, amp=a, wl=wl, phase=k * 46.0)
        parts.append(f'<path d="{d}" opacity="{1 - k * 0.13:.2f}"/>')
    return (
        f'<svg class="waves" viewBox="0 0 {W} {h}" preserveAspectRatio="none" '
        f'aria-hidden="true"><g fill="none" stroke="currentColor" '
        f'stroke-width="2.4" stroke-linecap="round">{"".join(parts)}</g></svg>'
    )


def seam(wl=232.0, amp=17.0, phase=0.0):
    """A scheme boundary drawn as a squiggle.

    The ground fill carries an explicit `fill` presentation attribute as well
    as its class, so a stale stylesheet degrades to the right colour instead
    of SVG's black default.
    """
    h = 132
    crest = 62.0
    ground = wave_area(crest, amp, wl, phase, h)
    line = wave(crest, amp, wl, phase)
    echo = wave(crest - 26.0, amp * 0.82, wl, phase + 30.0)
    return (
        f'<svg class="seam" viewBox="0 0 {W} {h}" preserveAspectRatio="none" '
        f'aria-hidden="true">'
        f'<path class="wave-ground" fill="currentColor" stroke="none" d="{ground}"/>'
        f'<g fill="none" stroke-linecap="round">'
        f'<path class="wave-echo" stroke-width="2.2" d="{echo}"/>'
        f'<path class="wave-crest" stroke-width="2.6" d="{line}"/>'
        f"</g></svg>"
    )


if __name__ == "__main__":
    print("<!-- waves -->")
    print(waves())
    print()
    print("<!-- seam down -->")
    print(seam())
    print()
    print("<!-- seam up -->")
    print(seam(phase=116.0))
