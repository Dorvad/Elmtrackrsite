# Elmtrackr — Marketing Website

Static one-page marketing site for Elmtrackr, a work-hours tracking app for Android and Wear OS.

## Structure

- `index.html` — the one-pager. It is a `dc` document rendered at runtime by `support.js` (which loads React from unpkg CDN).
- `support.js` — generated runtime that boots the page. Do not edit by hand.
- `_ds/` — the Elmtrackr design system (tokens, styles, component bundle) referenced by the page.
- `assets/` — logo and app icon.
- `uploads/` — source design images (not referenced by the live page).
- `.nojekyll` — required: it stops GitHub Pages' Jekyll build from dropping the underscore-prefixed `_ds/` folder.

## Deployment (GitHub Pages)

Deployment is automated via `.github/workflows/deploy-pages.yml`: every push to `main` publishes the repository root to GitHub Pages.

One-time setup in the repository settings:

1. Go to **Settings → Pages**.
2. Under **Build and deployment → Source**, select **GitHub Actions**.

After the next push to `main`, the site is served at `https://<owner>.github.io/<repo>/`.

Alternatively, classic branch deployment also works (Settings → Pages → Source: *Deploy from a branch* → `main` / root), since `.nojekyll` is present.

## Local preview

Any static file server works, e.g.:

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000. Note the page needs internet access to fetch React and Google Fonts from their CDNs.
