# Elmtrackr Marketing Website

Static one-page marketing site. See `README.md` for structure, deployment, and the local preview command.

## Cursor Cloud specific instructions

- This is a pure static site — there is **no build step, no package manager, and no installable dependencies**. "Running" it just means serving the repo root with a static file server (see the local preview command in `README.md`, e.g. `python3 -m http.server 8000`, then open the site).
- The page renders at runtime by fetching React from the unpkg CDN, so **it needs outbound internet access to render**. Offline, the page will appear blank/unrendered even though the file server returns HTTP 200.
- `support.js` is a generated runtime that boots the page — **do not edit it by hand** (noted in `README.md`).
- There are no automated tests, linters, or build commands in this repo. Verification is manual: load the page in a browser and confirm the hero renders and the live elapsed clock / "pay so far" counter tick up each second.
- `_ds/` holds legacy design-system tokens that are **not referenced** by the current page.
