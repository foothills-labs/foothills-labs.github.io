# foothills-labs.github.io

The Foothills Labs website — a hand-written static site, served by GitHub Pages
at <https://foothills-labs.github.io/>.

## Brand

The visual system is defined in
[`foundation_lab`](https://github.com/foothills-labs/foundation_lab), not here:

| | |
| --- | --- |
| Rules | [`docs/brand.md`](https://github.com/foothills-labs/foundation_lab/blob/main/docs/brand.md) |
| Reasoning | [`docs/brand-rationale.md`](https://github.com/foothills-labs/foundation_lab/blob/main/docs/brand-rationale.md) |
| Logo files | [`assets/logo/`](https://github.com/foothills-labs/foundation_lab/tree/main/assets/logo) |

**`assets/tokens.css` and `assets/tokens.json` are copies, not sources.** They
come from `assets/tokens/` in `foundation_lab`. To change a colour or a
typeface, change it there, regenerate the JSON with `build.py`, and copy both
files across — that is what stops the site and the brand guide drifting apart.
The JSON carries the generated contrast matrix and fill guards, so the
"generated rather than asserted" claim in the CSS header holds next to the copy
too. `assets/style.css` holds only site-specific
layout and components, and reads everything else from tokens.

### Schemes on this site

Four schemes, paired by area of the lab, so a reader can tell which half they
are in before reading a word:

| Scheme | Where |
| --- | --- |
| **Twilight** (dark) / **Cel** (light) | Default — the hero, mission, models, principles, contact, and `/models/`. Warm typeset: Fraunces + Newsreader. |
| **Notepad** (light) | The band holding `#tools`, and `/tools/`. Typeset: Archivo. |
| **Blueprint** (dark) | `/benchmarks/`. Typeset: Archivo. |

**`data-scheme` goes on `<body>`, not `<html>`, on the pages that set one.**
`tokens.css` declares its default `:root` block *after* the scheme blocks, so a
scheme on the root element loses the custom-property tie-break and the page
renders Twilight regardless. Moving that default above the scheme blocks
upstream would remove the constraint.

Apply with `data-scheme` on any element. Schemes nest and paint their own
ground, so a results table can sit inside a lab page in its own scheme.

**A scheme that paints a ground must be full-bleed and must sit in `.wrap`.**
Use `.band`, which does both. An inset rectangle with text flush to its edge
reads as a mistake rather than a register change — the ground has to run to the
edge of the viewport and the content has to keep the same measure as everything
above it.

### Seams

Where two schemes meet, the ground changes along a **squiggle**: the incoming
scheme's ground is filled to a smooth wave edge, the edge itself is inked, and
one lower-opacity echo rides above it. Entering the band (`.seam-down`), the
tools' white ground rises into the lab's sky inked in emerald; leaving it
(`.seam-up`), the lab's own ground rises back inked in butterscotch, so no line
ever sits on its own colour.

The register is the one Material 3 uses for its wavy dividers and progress
tracks: one wavelength held across the whole drawing, generous amplitude, round
caps. It replaces two earlier attempts — terrain contours, then origami
pleats — both of which read as noise at page width.

The seam's ground path carries `fill="currentColor"` as a presentation
attribute as well as its class. That is deliberate: if this stylesheet is ever
served stale against newer markup, the fill degrades to the inherited text
colour instead of SVG's black default. An earlier pleated seam had no such
guard, and a cached stylesheet rendered it as solid black sawteeth.

### Case

One rule, both typesets, no exceptions:

| | |
| --- | --- |
| **Headings** (`h1`–`h3`, data-table row headers) | Sentence case — warm and technical alike |
| **Mono labels** (eyebrows, nav, buttons, tags, pills, column heads) | Uppercase, `0.2em` tracking |

Uppercase is what marks a label as a label; spending it on headings too would
leave the two roles looking alike. It would also wreck the package names in the
Code band — `regexbench` and `labloop` are identifiers, and `REGEXBENCH` is a
different string.

`style.css` sets `text-transform: none` on headings explicitly rather than
relying on the initial value, so the rule cannot drift back one heading at a
time.

> **Note:** `tokens.json` currently declares `typeset.technical.display.case:
> "upper"`, and the warm typeset declares no `case` at all. Both are out of step
> with the rule above and with `brand.md`'s Typography table. The fix belongs in
> `foundation_lab` — the site is deliberately not following the declaration here.

### Fonts

Self-hosted in `assets/fonts/`, no external requests. Fraunces and Newsreader
are preloaded because they render the hero; Archivo and JetBrains Mono load
normally. All four are open licence — Fraunces, Newsreader and Archivo are SIL
OFL 1.1, JetBrains Mono is Apache-2.0.

### Illustration

Line not fill, and drawn in the same language as the mark. The hero band is a
**wave field**: one wavelength, one gap, one amplitude law, and a constant
phase step from line to line, so the set nests and no two lines can ever cross.
Tidiness is enforced by construction rather than by taste.

The bands are **generated, not hand-drawn**, following the same rule as the
marks in `foundation_lab`: change `assets/brand/waves.py` and re-run it, never
the path data.

```sh
python3 assets/brand/waves.py   # paste the output into index.html
```

Curves are exact cubic-Bezier sine arches, one per half wavelength: for an arch
of amplitude `A` over a half period `L/2`, control points at `L/6` and `L/3` at
height `4A/3` put the curve's midpoint at exactly `A`. That is the closest a
single cubic gets to a sinusoid, and it keeps the whole file near 5 KB.

They have to be inline SVG rather than `<img>`, because they read
`currentColor` and the scheme custom properties.

### The house mark

**The mark is shown in colour**, so it is a `background-image` rather than a
masked shape: a mask can only take one colour, and the colour build carries
rose, butterscotch and emerald facets under the line. That costs two builds,
because the outline is sumi on light grounds and chalk on dark ones and a
single file cannot be both. `style.css` resolves `--fh-mark` and
`--fh-mark-small` per scheme, so markup just asks for the token.

| Where | File |
| --- | --- |
| Hero, ~132 px | `mark-colour.svg` / `mark-colour-dark.svg` |
| Header, 30 px | `mark-colour-small.svg` / `mark-colour-small-dark.svg` — reduced cut, front range only, heavier stroke |
| Anything CSS must recolour | `mark.svg` — monoline, takes `currentColor` |

Below about 40 px the back range breaks into stray pixels and the valleys silt
up, which is what the reduced cut exists for.

**Never inline the mark's path data into a page.** An earlier hero did, and the
next rebrand swapped `mark.svg` underneath it: the header updated and the hero
kept drawing the previous logo, because an inlined copy is a copy and not a
reference.

### Model glyphs

`assets/brand/marks/` holds the four paper-plane glyphs, generated in
`foundation_lab` and vendored here. They are applied as CSS masks so they take
the scheme's accent colour:

```html
<span class="peak" style="--g: url(/assets/brand/marks/plane-delta-mono.svg); ..."></span>
```

The path **must be root-relative**. A `url()` inside a custom property resolves
against the stylesheet that consumes it, not the document, so a relative path
here resolves against `assets/` and 404s.

## How this repo gets online

This repo is an **organization Pages site**, which is a special case in GitHub
Pages:

- The repo name must be exactly `<org>.github.io`. It is.
- Because the name matches, GitHub enables Pages automatically on the first
  push to the **default branch** (`main`) and serves the **repository root**.
  There is normally no setting to flip.
- The site is served at the org root, `https://foothills-labs.github.io/` — not
  under a `/repo-name/` path the way project sites are.

So the deploy story is: **merge to `main`, wait a minute, reload.** Pushing to
any other branch changes nothing that's live.

If the site ever doesn't appear, check **Settings → Pages** and confirm the
source is `Deploy from a branch` → `main` → `/ (root)`.

### No Jekyll

The `.nojekyll` file at the root tells Pages to publish the files verbatim
instead of running them through Jekyll. That means no Gemfile, no build step,
and nothing that can fail at deploy time — but it also means no Jekyll
templating, includes, or `_layouts`. Plain HTML and CSS only.

If the site later outgrows hand-written HTML, the two options are to delete
`.nojekyll` and adopt Jekyll, or to add a GitHub Actions workflow that builds
whatever generator you prefer and publishes with `actions/deploy-pages`. That
second path also requires switching **Settings → Pages → Source** to
`GitHub Actions`.

## Layout

```
index.html        Landing page
models/           /models/ — base camp page for the model range
tools/            /tools/ — base camp page for the shipped tools (Notepad)
benchmarks/       /benchmarks/ — base camp page, empty results table (Blueprint)
404.html          Custom not-found page (Pages serves this automatically)
assets/
  style.css       All styling; light and dark via prefers-color-scheme
  favicon.svg     Site icon
robots.txt        Crawler policy, points at the sitemap
sitemap.xml       Sitemap: the landing page plus the three section pages
.nojekyll         Publish files as-is, skip the Jekyll build
```

Everything is self-contained: no CDNs, no external fonts, no JavaScript.

## Working on it locally

There's no build step, so opening `index.html` in a browser mostly works.
Absolute paths (`/assets/...` in `404.html`) only resolve over HTTP, so prefer:

```sh
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Custom domain

The site is served at **`foothills-labs.com`**, declared by the `CNAME` file at
the repo root. DNS is managed at Cloudflare. `github.io` redirects to it.

### DNS records

All records are **DNS only (grey cloud)** — see the warning below.

| Type | Name | Value |
| --- | --- | --- |
| `CNAME` | `@` | `foothills-labs.github.io` |
| `CNAME` | `www` | `foothills-labs.github.io` |
| `TXT` | `_github-pages-challenge-foothills-labs` | (token from the org's Pages settings) |

Cloudflare flattens the apex `CNAME` to A records automatically, so there is no
need to hard-code GitHub's four Pages IPs — and the record keeps working if
those IPs ever change. If you ever do need them literally:
`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`,
plus `2606:50c0:8000::153` through `:8003::153` for AAAA.

### The Cloudflare trap

> **Keep the cloud grey.** Cloudflare proxies new records by default (orange
> cloud). While a record is proxied, GitHub cannot see the DNS it needs to
> issue the Let's Encrypt certificate, so **Enforce HTTPS** stays greyed out
> with "your domain is not properly configured to support HTTPS" — and once
> issued, a proxied record breaks the automatic 90-day renewal too.

Leaving it grey is the recommendation, not just a setup step. GitHub Pages
already fronts the site with a CDN and its own TLS, so proxying buys little and
adds a recurring renewal failure.

If you ever do enable the orange cloud, set **SSL/TLS → Full (strict)** first.
`Flexible` makes Cloudflare talk HTTP to GitHub, which already redirects to
HTTPS, and the result is an infinite redirect loop.

### Order of operations

The `CNAME` file makes GitHub redirect `foothills-labs.github.io` to the custom
domain. Commit it **before** DNS resolves and both addresses are dark — the
redirect target does not answer. So:

1. Add the DNS records at Cloudflare, grey cloud.
2. Confirm they resolve: `dig +short foothills-labs.com`.
3. Merge the `CNAME` file to `main`.
4. **Settings → Pages** shows the domain with a DNS check. Wait for the
   certificate, then tick **Enforce HTTPS**.

### Verify the domain

Org **Settings → Pages → Verified domains** gives a TXT record to add. Worth
doing: an unverified domain can be claimed by another GitHub account if the
`CNAME` is ever removed while the DNS still points at GitHub.
