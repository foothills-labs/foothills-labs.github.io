#!/usr/bin/env python3
"""Check — or refresh — the brand files this repo copies from plicara-brand.

`assets/tokens.css`, `assets/tokens.json`, the marks and the glyphs are COPIES.
They are generated in `plicara-brand` -- the public brand repo, split out of
the private notebook on 2026-08-20 -- and vendored here so the site can be
plain static files with no build step. Nothing enforced that, so they drifted:

  - the site hand-edited `favicon.svg` and the small marks to restore the back
    range, and the edit never went upstream, so the two repos disagreed about
    what the logo was for three days;
  - a palette repaint landed upstream and the site kept shipping the previous
    one, because "vendor the new tokens" is a step a human has to remember.

This script is that step, made mechanical. It is the site's half of the
contract; `tokens/build.py` upstream audits its own tokens.css against its
palette, which is the other half.

    python3 tools/vendor.py --check    # fail if any copy differs (CI)
    python3 tools/vendor.py --sync     # overwrite the copies from upstream
    python3 tools/vendor.py --check --upstream ../plicara-brand

Exit status is 1 on drift, so CI can gate on it.

NOTE ON DIRECTION: this only ever copies upstream -> here. If a copy needs to
change, change it in plicara-brand and re-run with --sync. Editing a vendored
file in this repo is the thing that broke last time; --check will catch it and
tell you to go upstream.
"""

import argparse
import filecmp
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DEFAULT_UPSTREAM = os.path.join(os.path.dirname(SITE), "plicara-brand")

PLANES = [f"plane-{model}{cut}.svg"
          for model in ("canard", "delta", "glider", "hammer")
          for cut in ("", "-dark", "-mono", "-small")]

# (path in plicara-brand, path here)
VENDORED = [
    ("tokens/tokens.css", "assets/tokens.css"),
    ("tokens/tokens.json", "assets/tokens.json"),
    ("logo/favicon.svg", "assets/favicon.svg"),
    ("logo/mark.svg", "assets/brand/mark.svg"),
    ("logo/mark-colour.svg", "assets/brand/mark-colour.svg"),
    ("logo/mark-colour-dark.svg", "assets/brand/mark-colour-dark.svg"),
    ("logo/mark-colour-small.svg", "assets/brand/mark-colour-small.svg"),
    ("logo/mark-colour-small-dark.svg",
     "assets/brand/mark-colour-small-dark.svg"),
    ("logo/png/social-card-1200x630.png", "assets/brand/og.png"),
    ("logo/png/apple-touch-icon-180.png",
     "assets/brand/apple-touch-icon-180.png"),
] + [(f"marks/{f}", f"assets/brand/marks/{f}") for f in PLANES]


def compare(upstream):
    """Returns (missing_upstream, missing_here, differing)."""
    missing_up, missing_here, differ = [], [], []
    for src, dst in VENDORED:
        s, d = os.path.join(upstream, src), os.path.join(SITE, dst)
        if not os.path.exists(s):
            missing_up.append(src)
        elif not os.path.exists(d):
            missing_here.append(dst)
        elif not filecmp.cmp(s, d, shallow=False):
            differ.append((src, dst))
    return missing_up, missing_here, differ


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--upstream", default=DEFAULT_UPSTREAM,
                    help="path to a plicara-brand checkout")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--sync", action="store_true")
    args = ap.parse_args()

    upstream = os.path.abspath(args.upstream)
    if not os.path.isdir(upstream):
        print(f"no plicara-brand checkout at {upstream}", file=sys.stderr)
        return 2

    missing_up, missing_here, differ = compare(upstream)

    if args.sync:
        for src, dst in VENDORED:
            s, d = os.path.join(upstream, src), os.path.join(SITE, dst)
            if not os.path.exists(s):
                continue
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copyfile(s, d)
        n = len(VENDORED) - len(missing_up)
        moved = len(differ) + len(missing_here)
        print(f"synced {n} file(s) from {upstream}; {moved} changed")
        if missing_up:
            print("MISSING UPSTREAM (not synced):")
            for p in missing_up:
                print(f"  {p}")
            return 1
        return 0

    problems = False
    if missing_up:
        problems = True
        print("Missing in plicara-brand — the manifest is out of date:")
        for p in missing_up:
            print(f"  {p}")
    if missing_here:
        problems = True
        print("Missing here — run: python3 tools/vendor.py --sync")
        for p in missing_here:
            print(f"  {p}")
    if differ:
        problems = True
        print("Vendored copies differ from plicara-brand:")
        for src, dst in differ:
            print(f"  {dst}  !=  plicara-brand/{src}")
        print("\nThese files are copies, not sources. If the change belongs,")
        print("make it in plicara-brand and run: python3 tools/vendor.py --sync")
    if problems:
        return 1
    print(f"all {len(VENDORED)} vendored files match {upstream}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
