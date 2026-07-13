# Elmtrackr — Marketing Website

Static one-page marketing site for Elmtrackr, a work-hours tracking app for Android and Wear OS.

## Structure

- `index.html` — the landing page ("Every shift, measured"). It is a `dc` document rendered at runtime by `support.js` (which loads React from the unpkg CDN). A small script at the bottom of the page drives the live elements: the ticking elapsed clock, pay-so-far counter, and progress rings.
- `support.js` — generated runtime that boots the page. Do not edit by hand.
- `assets/fonts/` — self-hosted webfonts (Archivo + IBM Plex Mono), no Google Fonts request at runtime.
- `assets/` — app icon, logos, the real app screenshot (`app-screenshot.jpg`, shown in the hero phone), web-optimized marketing renders used in the "On every screen" section, and the product film (`elmtrackr-tour.mp4`, faststart-remuxed, with `tour-poster.jpg`) shown in the "07 — The film" section. The film autoplays muted while scrolled into view, pauses off-screen, and unmutes on tap; the wiring lives in the `DCLogic` script at the bottom of `index.html` (`_filmSetup`).
- `uploads/` — original full-resolution source images.
- `.nojekyll` — stops GitHub Pages' Jekyll build from interfering with the deploy.
- `_ds/` — legacy design-system tokens from an earlier version of the site (not referenced by the current page).

## Deployment (GitHub Pages)

Deployment is automated via `.github/workflows/deploy-pages.yml`: every push to `main` or `claude/github-pages-deploy-i6mtq9` publishes the repository root to GitHub Pages (source: GitHub Actions).

Custom domain: set `www.elmtrackr.site` in Settings → Pages, with a DNS CNAME record `www` → `dorvad.github.io`.

## Local preview

Any static file server works, e.g.:

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000. The page needs internet access to fetch React from unpkg; fonts are local.
