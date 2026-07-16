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

## Listing availability status — UNVERIFIED

`play_store.listing_public` is `false` in the manifest.

Whether `com.elmlaunch.myapp` is **published and publicly reachable** on the
Play Store is **not verifiable from the product source** — publishing steps
were still pending in the Android release checklist, and this cannot be
confirmed from code (see `product-facts.md`, row 7 and "Unresolved facts").

**Decision applied (per the current task):** the site links to the
package-specific canonical URL — the intended destination — rather than
silently sending users to the generic `https://play.google.com` home page.
The generic home-page links have been removed entirely.

**Action for the owner:**

1. Confirm the listing is live and public (open the URL above in a private
   browser session).
2. When confirmed, set `play_store.listing_public` to `true` in
   `scripts/seo_manifest.json` and record the confirmation date here.
3. If the listing is **not** yet public, decide whether to keep the CTA
   pointing at the (pending) listing or to gate it until launch. Until then,
   this file is the single record of that status.

> Do **not** add price, "free", ratings or review counts to the listing
> metadata or structured data — none of those are verified (see
> `product-facts.md`).
