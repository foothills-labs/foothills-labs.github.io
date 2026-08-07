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
| **Glacier** (dark) / **Atlas** (light) | Default — the hero, the plan, the roadmap, principles. Warm typeset: Fraunces + Newsreader. |
| **Field** (light) | The band holding `#models` and `#code` — the technical half. Typeset: Archivo. |
| **Signal** (dark) | Reserved for benchmark and leaderboard pages. |

Apply with `data-scheme` on any element. Schemes nest and paint their own
ground, so a results table can sit inside a lab page in its own scheme.

**A scheme that paints a ground must be full-bleed and must sit in `.wrap`.**
Use `.band`, which does both. An inset rectangle with text flush to its edge
reads as a mistake rather than a register change — the ground has to run to the
edge of the viewport and the content has to keep the same measure as everything
above it.

### Seams

Where two schemes meet, the ground changes colour **along a contour line**, and
the lines carry on across the join — a change of terrain, drawn rather than cut.
`.seam-wrap` paints the outgoing ground, `.seam-ground` fills the incoming one,
and the two line groups are inked for whichever ground they land on, so no line
is ever drawn on its own colour. `.seam--up` is the same drawing flipped for the
way back out.

This matters most in light mode, where Atlas vellum and Field paper are close
enough that a hard edge would barely register: the drawn boundary is what makes
the transition legible without forcing the two grounds further apart.

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

Abstract mountaineering: line not fill, plan and section rather than scenery.
The hero band is a contour section, drawn in the same language as the mark.
**No horizons, no summits at sunset** — a literal ridge silhouette is the one
thing the identity rules out, because it undoes the argument the mark makes.

The contour bands are **generated, not hand-drawn**, following the same rule as
the marks in `foundation_lab`: change `assets/brand/contours.py` and re-run it,
never the path data. The irregularity is deliberate — each line carries its own
phase drift, so no two are parallel.

```sh
python3 assets/brand/contours.py   # paste the output into index.html
```

They have to be inline SVG rather than `<img>`, because they read `currentColor`
and the scheme custom properties.

### Model glyphs

`assets/brand/marks/` holds the eight contour glyphs, vendored from
`foundation_lab/assets/marks/`. They are applied as CSS masks so they take the
scheme's accent colour:

```html
<span class="glyph" style="--g: url(/assets/brand/marks/contour-everest-small.svg)"></span>
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
404.html          Custom not-found page (Pages serves this automatically)
assets/
  style.css       All styling; light and dark via prefers-color-scheme
  favicon.svg     Site icon
robots.txt        Crawler policy, points at the sitemap
sitemap.xml       Single-URL sitemap
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

## Adding a custom domain later

Not set up, and not needed for the `github.io` address to work. When you want
one (e.g. `foothillslabs.dev`):

1. At the DNS registrar, point the apex at GitHub's Pages IPs with four `A`
   records — `185.199.108.153`, `185.199.109.153`, `185.199.110.153`,
   `185.199.111.153` — and add a `CNAME` for `www` pointing at
   `foothills-labs.github.io`.
2. Enter the domain in **Settings → Pages → Custom domain**. GitHub commits a
   `CNAME` file to this repo for you.
3. Once DNS resolves, tick **Enforce HTTPS**.

Do not hand-create a `CNAME` file before the DNS records exist — Pages will
serve the unresolvable domain and the site goes dark.
