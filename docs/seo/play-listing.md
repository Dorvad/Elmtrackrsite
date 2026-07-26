# Elmtrackr — Play Store Listing (canonical URL & status)

**Date reviewed:** 2026-07-16
**Source of truth for the ID:** `docs/seo/product-facts.md`, row 2 (verified
from the Android repository `Dorvad/elmtrackr`).

## Canonical Play Store URL

There is **one** Play Store URL for the whole site. It is defined once in
`scripts/seo_manifest.json` under `play_store.url`, mirrored in the
homepage JSON-LD (`SoftwareApplication.downloadUrl`), and used verbatim on
every "Get it on Google Play" call-to-action.

```
https://play.google.com/store/apps/details?id=com.elmlaunch.myapp&referrer=utm_source%3Delmtrackr.site%26utm_medium%3Dwebsite%26utm_campaign%3Dget_the_app
```

- **Application ID:** `com.elmlaunch.myapp` — verified and permanent. (The
  Kotlin namespace `com.elmtrackr.app` is **not** the store ID and must never
  appear in a link.)
- **Campaign parameters:** attached via Google Play's `referrer` parameter
  (URL-encoded), the mechanism Play uses for install attribution:
  - `utm_source=elmtrackr.site`
  - `utm_medium=website`
  - `utm_campaign=get_the_app`
- **Link safety:** every CTA keeps `target="_blank"` with `rel="noopener"`
  and an `aria-label` ("Get Elmtrackr on Google Play (opens in a new tab)").

## Listing availability status — CONFIRMED PUBLIC

`play_store.listing_public` is `true` in the manifest.

**Confirmed 2026-07-26:** the owner supplied the live listing URL
(`https://play.google.com/store/apps/details?id=com.elmlaunch.myapp`) and an
unauthenticated request to it returned HTTP 200, so the listing for
`com.elmlaunch.myapp` is published and publicly reachable. All site CTAs
already pointed at the package-specific canonical URL above; no link changes
were required.

> Do **not** add price, "free", ratings or review counts to the listing
> metadata or structured data — none of those are verified (see
> `product-facts.md`).
