# foothills-labs.github.io

The Foothills Labs website — a hand-written static site, served by GitHub Pages
at <https://foothills-labs.github.io/>.

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
