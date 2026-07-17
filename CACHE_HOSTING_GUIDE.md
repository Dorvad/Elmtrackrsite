# Cache Hosting Guide — first-party asset cache lifetime

Internal operations guide. Excluded from the published site (see `Makefile` →
`INTERNAL`).

## Confirmed host (measured, not assumed)

elmtrackr.site is served **directly by GitHub Pages**. Evidence:

- **DNS:** the apex `elmtrackr.site` resolves to GitHub Pages' anycast IPs
  `185.199.108–111.153`; `www.elmtrackr.site` is a CNAME to `dorvad.github.io`.
- **Response headers (live):** `server: GitHub.com`, `via: 1.1 varnish`, and
  **no** `cf-*`, Vercel, or Netlify markers.
- **Deploy workflow:** `.github/workflows/deploy-pages.yml` builds with
  `make ci` and publishes `_site/` via the official
  `actions/upload-pages-artifact` + `actions/deploy-pages`.

There is no Cloudflare/Vercel/Netlify layer in front of it today.

## The finding, and why the repository cannot fix it

Every first-party response — the HTML document **and** the content-hashed assets
under `/assets/fp/` — is returned by GitHub Pages with a fixed:

```
cache-control: max-age=600
```

Confirmed live for all four resource types required by the audit:

| Resource | Live `Cache-Control` |
| --- | --- |
| HTML document (`/`) | `max-age=600` |
| Hashed JS (`/assets/fp/analytics-loader.<hash>.js`) | `max-age=600` |
| Hashed image (`/assets/fp/…home-screen….<hash>.webp`) | `max-age=600` |
| Hashed font (`/assets/fp/fonts/archivo-latin.<hash>.woff2`) | `max-age=600` |

GitHub Pages **does not expose any repository-level control over response
headers**. A `_headers` file, `vercel.json`, `netlify.toml`, or a `<meta>` tag
have **no effect** on GitHub Pages. Therefore this warning cannot be resolved by
committing code; it requires a hosting-layer change. (Per the brief: no fake
`_headers` file is added, and no repository code is claimed to change GitHub
Pages cache headers.)

## What is already complete in the repository (no further code needed)

- **Content-hashed asset names** (`fingerprint_assets.py`): every cacheable CSS,
  JS, font, and image is emitted under `/assets/fp/` with a 12-char SHA-256
  fingerprint. Verified deterministic: two clean builds produce identical
  fingerprints for unchanged files, and a file's hash changes when its bytes
  change (e.g. the hero `-480.webp` hash changed after re-encoding). This makes a
  one-year immutable policy **safe** — a content change yields a new URL.
- **HTML is not cached immutably** — it is `max-age=600` today and must stay
  short/revalidated so a new deploy is picked up promptly.

Because hashing is already in place, the only remaining work is external hosting
configuration.

## Recommended path (simplest supported): proxy the domain through Cloudflare

This keeps GitHub Pages as the origin and the existing deploy workflow unchanged
— the smallest possible change. Cloudflare (free plan) sits in front and sets the
cache headers GitHub Pages cannot.

### Step 1 — Add the site to Cloudflare and move DNS

1. Create a free Cloudflare account and **Add a site** → `elmtrackr.site`.
2. Cloudflare scans existing DNS. Confirm these records exist, then set each to
   **Proxied (orange cloud)**:
   - `A elmtrackr.site 185.199.108.153` (+ `.109`, `.110`, `.111` — all four)
   - `AAAA elmtrackr.site 2606:50c0:8000::153` (+ `:8001/:8002/:8003`)
   - `CNAME www dorvad.github.io`
3. At the **domain registrar**, replace the current nameservers with the two
   Cloudflare nameservers shown in the dashboard. Propagation is typically
   minutes to a few hours.
4. SSL/TLS mode: **Full** (GitHub Pages already serves valid HTTPS).
5. Leave GitHub Pages' custom domain (`www.elmtrackr.site`) and the repo's Pages
   settings exactly as they are.

> Cache Rules require **proxied** DNS. If the records stay "DNS only" (grey
> cloud), no rule below takes effect.

### Step 2 — Cache Rule: make fingerprinted assets cacheable for a year

Cloudflare dashboard → **Caching → Cache Rules → Create rule**.

Expression:

```text
(http.host in {"elmtrackr.site" "www.elmtrackr.site"} and http.request.uri.path wildcard "/assets/fp/*")
```

Settings:

- **Cache eligibility:** Eligible for cache
- **Edge TTL:** Ignore origin and use `31536000` seconds
- **Browser TTL:** Override origin and use `31536000` seconds

### Step 3 — Cache Response rule: set the immutable header on those assets

Cloudflare dashboard → **Rules → Overview → Response Header Transform Rules** (or
Caching → Cache Rules’ response-header option), same expression as Step 2. Set a
**static** response header:

```http
Cache-Control: public, max-age=31536000, immutable
```

### Step 4 — Keep HTML revalidated (exclude it from immutable caching)

Create a second response-header rule.

Expression (matches the document routes, not the hashed assets):

```text
(http.host in {"elmtrackr.site" "www.elmtrackr.site"} and (http.request.uri.path eq "/" or ends_with(http.request.uri.path, "/") or http.request.uri.path.extension eq "html"))
```

Set header to exactly:

```http
Cache-Control: public, max-age=0, must-revalidate
```

**Why this HTML policy:** the HTML is the entry point that references the hashed
asset URLs. It must be re-fetched (or revalidated) on every visit so a new deploy
is seen immediately; if HTML were cached immutably, visitors could be pinned to
an old page pointing at old assets. `max-age=0, must-revalidate` gives near-zero
staleness while still allowing a 304 revalidation. (`no-cache` is an acceptable
equivalent.) Only `/assets/fp/*` — whose names change on every content change —
receives the one-year `immutable` policy. Stable public URLs (the video,
captions, Open Graph images) are intentionally left on the origin default.

### Verify

```sh
# hashed asset — expect: cache-control: public, max-age=31536000, immutable
curl -sSI https://elmtrackr.site/assets/fp/fonts/archivo-latin.<HASH>.woff2 | grep -i cache-control

# HTML — expect: cache-control: public, max-age=0, must-revalidate (NOT immutable)
curl -sSI https://elmtrackr.site/ | grep -i cache-control
```

Use a filename from the deployed `/asset-manifest.json` for `<HASH>`. In browser
DevTools → Network, a hard reload then a normal reload should show hashed assets
served **from disk/memory cache** with the year-long lifetime, while the document
still revalidates. Also confirm `cf-cache-status` appears (proxy active).

### Rollback

Fully reversible, no repository change to undo:

1. Fastest: **Caching → Cache Rules** → disable/delete the two rules and the
   response-header rules. Headers revert to GitHub Pages' `max-age=600` within
   minutes.
2. Full removal: at the registrar, restore the original nameservers (or set the
   Cloudflare DNS records back to **DNS only / grey cloud**). Traffic then goes
   straight to GitHub Pages exactly as today.

## Alternative path — Cloudflare Pages (only if leaving GitHub Pages)

If the team prefers not to proxy, deploy the *same* build through Cloudflare
Pages (build command `make ci`, output directory `_site`) and add a `_headers`
file **to that build output** (Cloudflare Pages honours it; GitHub Pages does
not):

```text
/assets/fp/*
  Cache-Control: public, max-age=31536000, immutable
/
  Cache-Control: public, max-age=0, must-revalidate
/*.html
  Cache-Control: public, max-age=0, must-revalidate
/*/
  Cache-Control: public, max-age=0, must-revalidate
```

This is a host migration (DNS points at Cloudflare Pages instead of GitHub Pages)
and changes the deploy target, so it is a bigger change than the proxy path. Do
not add this `_headers` file to the current GitHub Pages artifact — it would ship
as a dead file.

## Status: repository work vs. external action required

- **Completed in the repository:** content-hashed asset pipeline (deterministic,
  verified), HTML kept non-immutable, no fake header files added. Nothing further
  is needed in code.
- **External action still required (account owner):** perform the Cloudflare
  steps above. This is a DNS/hosting change on accounts outside this repository
  and cannot be done from here. Until it is done, first-party assets remain at
  GitHub Pages' `max-age=600` and Lighthouse will keep reporting the ~96 KB
  repeat-visit opportunity — which is expected and not a regression.
