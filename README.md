# Elmtrackr — Marketing Website

Static one-page marketing site for Elmtrackr, a work-hours tracking app for Android and Wear OS.

## Structure

- `index.html` — the landing page ("Every shift, measured"). It is a **self-contained static HTML page**: semantic structure (`header`/`nav`/`main`/`section`/`footer`), one `h1`, a skip link, and complete, meaningful content in the initial markup. Every dynamic value ships with a realistic static fallback and a `data-*`/`id` hook; a small inline vanilla-JS block at the bottom progressively enhances the live elements (ticking clock, pay-so-far counter, progress rings, widget scroll choreography, product film) and applies hover states via `data-hover`. No framework, no runtime template syntax, and no CDN are required to render or read the page — if the script is blocked or fails, the page stays complete.
- `support.js` — the generated DC runtime from an earlier version of the site. **No longer used by `index.html`** (which is now standalone static HTML) and not referenced by any shipped page; retained only for history. It is generated from `dc-runtime/src/*.ts` (source not in this repo) and must not be hand-edited — regenerate with `cd dc-runtime && bun run build` if it is ever needed again.
- `scripts/check_static_html.py` — stdlib-only static-source validator. Fails if a shipped page's initial HTML is incomplete or invalid: raw `{{ }}`, leftover custom template values, missing `lang`/`h1`/`main`, broken internal anchors, images without `alt`, or empty `href`. Run: `python3 scripts/check_static_html.py`.
- `assets/fonts/` — self-hosted webfonts (Archivo + IBM Plex Mono), no Google Fonts request at runtime.
- `assets/` — app icon, logos, the real app screenshot (`app-screenshot.jpg`, shown in the hero phone), web-optimized marketing renders used in the "On every screen" section, and the product film (`elmtrackr-tour.mp4`, faststart-remuxed, with `tour-poster.jpg`) shown in the "07 — The film" section. The film autoplays muted while scrolled into view, pauses off-screen, and unmutes on tap; the wiring lives in the inline script at the bottom of `index.html`.
- `uploads/` — original full-resolution source images.
- `.nojekyll` — stops GitHub Pages' Jekyll build from interfering with the deploy.
- `_ds/` — legacy design-system tokens from an earlier version of the site (not referenced by the current page).

## Deployment (GitHub Pages)

Deployment is automated via `.github/workflows/deploy-pages.yml`: every push to `main` publishes the repository root to GitHub Pages (source: GitHub Actions). Internal, non-site files (`docs/`, `AGENTS.md`) are stripped from the published artifact.

Custom domain: set `www.elmtrackr.site` in Settings → Pages, with a DNS CNAME record `www` → `dorvad.github.io`.

## Local preview

Any static file server works, e.g.:

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000. The page is fully static — no build step, no CDN, and no network access are needed to render it; fonts are self-hosted.
