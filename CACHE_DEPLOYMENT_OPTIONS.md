# Cache deployment options

## Current deployment and completed repository work

Elmtrackr is deployed as a static GitHub Pages artifact by
`.github/workflows/deploy-pages.yml`. The production build now:

- writes cacheable CSS, JavaScript, fonts, and images under `/assets/fp/`;
- gives each file a 12-character SHA-256 content fingerprint, for example
  `content-pages.4a51c7617b7d.css`;
- rewrites page and stylesheet references and writes `/asset-manifest.json`;
- leaves HTML, videos, captions, and assets used by stable absolute metadata
  URLs unfingerprinted; and
- publishes `_site/`, not the repository root.

This prevents a new deployment from reusing a stale asset URL. It does not,
by itself, change HTTP cache lifetimes. A `<meta>` element cannot replace an
HTTP `Cache-Control` response header.

GitHub Pages accepts a static artifact but does not expose repository-level
configuration for arbitrary response headers. Therefore no `_headers` file is
included in the GitHub Pages artifact: GitHub Pages would not apply it as
header configuration. Long immutable browser caching requires a proxy or a
different static host.

## Option A — keep GitHub Pages and proxy the domain through Cloudflare

This is the smallest hosting change. Add the domain to Cloudflare and proxy
the DNS records (orange cloud), while GitHub Pages remains the origin. In
Cloudflare, create these rules for both the apex and `www` hostnames.

### 1. Fingerprinted-asset Cache Rule

Expression:

```text
(http.host in {"elmtrackr.site" "www.elmtrackr.site"} and
 http.request.uri.path wildcard "/assets/fp/*")
```

Settings:

- Cache eligibility: **Eligible for cache**
- Edge TTL: **Ignore origin and use 31536000 seconds**
- Browser TTL: **Override origin and use 31536000 seconds**

### 2. Fingerprinted-asset Cache Response Rule

Use the same expression and set the downstream response header to exactly:

```http
Cache-Control: public, max-age=31536000, immutable
```

### 3. HTML Cache Response Rule

Expression:

```text
(http.host in {"elmtrackr.site" "www.elmtrackr.site"} and
 (http.request.uri.path eq "/" or
  http.request.uri.path wildcard "*/" or
  http.request.uri.path.extension eq "html"))
```

Set the response header to exactly:

```http
Cache-Control: public, max-age=0, must-revalidate
```

Cloudflare Cache Rules control edge/browser TTL, while Cache Response Rules
set the actual `Cache-Control` directives returned to clients. Cloudflare's
documentation requires proxied DNS for these rules:
[Cache Rules](https://developers.cloudflare.com/cache/how-to/cache-rules/)
and [Cache Response Rules](https://developers.cloudflare.com/cache/how-to/cache-response-rules/).

## Option B — migrate the static artifact to Cloudflare Pages

Configure the project with build command `make ci` and output directory
`_site`. Then add the following `_headers` file to the Cloudflare Pages build
output (not to the current GitHub Pages deployment):

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

Only `/assets/fp/` receives immutable caching. Stable public URLs such as the
video, captions, Open Graph images, and HTML are deliberately excluded. See
Cloudflare Pages' [custom headers documentation](https://developers.cloudflare.com/pages/configuration/headers/).

## Post-deployment verification

Run these against the canonical hostname, substituting a filename from
`asset-manifest.json` for the first URL:

```sh
curl -I https://elmtrackr.site/assets/fp/fonts/archivo-latin.HASH.woff2
curl -I https://elmtrackr.site/
```

The first response must contain the one-year immutable policy. The HTML
response must contain the revalidation policy and must not be immutable.
