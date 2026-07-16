# Elmtrackr — Release report

**Date:** 2026-07-16
**Branch:** `claude/technical-seo-foundation-fzqrk0`
**Product source of truth:** `Dorvad/elmtrackr` `Main` HEAD `df98c3e` (re-verified).
**Scope:** technical SEO foundation, a bilingual product-information site,
educational guides, media accessibility, legal/trust accuracy, a vendor-neutral
analytics layer, and a repeatable automated quality gate.

This report summarizes the state of the site at release and the steps to take
after it goes live. It is a status document, not legal advice; items needing a
human decision are listed explicitly.

---

## 1. Routes

The site grew from a single landing page into a small, crawlable, bilingual
product-information site. At release the route manifest
(`scripts/seo_manifest.json`) defines **33 pages**: **30 indexable** (in the
sitemap) and **3 intentionally non-indexable** utility/legal pages.

**Indexable (30):**

| Group | English | Hebrew |
|---|---|---|
| Home | `/` | `/he/` |
| Product pages (7) | `/shift-tracker-android/`, `/hourly-pay-tracker/`, `/overtime-pay-tracker/`, `/wear-os-shift-tracker/`, `/receipt-expense-tracker/`, `/work-hours-reports/`, `/task-time-tracking/` | each with a `/he/…` pair |
| Guides hub | `/guides/` | `/he/guides/` |
| Guides (4) | `/guides/how-to-track-work-hours/`, `/guides/how-to-estimate-hourly-pay/`, `/guides/overtime-vs-premium-pay/`, `/guides/how-to-review-work-hours-against-a-payslip/` | each with a `/he/…` pair |
| Educational | `/privacy-and-security/` | `/he/privacy-and-security/` |
| Account deletion | `/delete-account/` | `/he/delete-account/` |

**Non-indexable (3):** `/privacy.html` and `/terms.html` (formal legal pages,
`noindex, follow` by documented decision; the indexable counterpart is
`/privacy-and-security/`), and `/404.html` (error page, added this release).

---

## 2. Metadata summary

Every page carries: a unique `<title>` and unique `<meta name="description">`,
a self-referencing `<link rel="canonical">`, a `robots` directive consistent
with its indexability, a complete Open Graph + Twitter card set
(`og:type/title/description/url/image` with dimensions and alt), correct
`og:locale`, and light/dark `theme-color`. Hebrew pages declare
`<html lang="he" dir="rtl">`; English pages declare `lang="en"`.

The comprehensive audit (`scripts/audit_site.py`) enforces uniqueness of titles
and descriptions across the whole site, self-canonical correctness, and that no
English page carries Hebrew metadata (or vice-versa).

---

## 3. Structured-data summary

- **Home (en + he):** a single JSON-LD `@graph` with `Organization`, `WebSite`,
  `SoftwareApplication`, and `VideoObject`.
- **Product & guide pages:** `WebPage`/article node, `BreadcrumbList`, and
  `FAQPage` where a visible FAQ exists.
- **No rating or review schema anywhere.** Store rating and review count are not
  verifiable, so `aggregateRating`/`Review` are deliberately absent — and the
  audit fails the build if any is introduced.
- Every JSON-LD block parses as valid JSON (verified in CI), and every
  `FAQPage` question has a matching visible question on the page.

---

## 4. English / Hebrew parity

- **15 indexable English pages and 15 indexable Hebrew pages** — full 1:1 parity.
- Reciprocal `hreflang` (`en`, `he`, `x-default`) is generated from the manifest
  and validated by `check_locales.py` and the audit; every language-switch link
  points at the correct counterpart.
- Hebrew renders RTL with a system Hebrew font stack; `.ltr` isolation is used
  for embedded Latin tokens.
- Hebrew localization on the **app** is described as "full Hebrew support" but
  not literal 100% parity (6 widget-preview strings are untranslated — recorded
  in `product-facts.md`).

---

## 5. Sitemap

- `sitemap.xml` contains **30 `<loc>` entries** — exactly the indexable routes,
  no more. It is generated from the manifest (never hand-edited) and CI verifies
  it is up to date and well-formed XML.
- `robots.txt` references the sitemap and does not block crawlable content.
- The 3 non-indexable pages are correctly **excluded** from the sitemap; the
  audit fails if a `noindex` page ever appears in it, or an indexable page is
  missing from it.

---

## 6. Crawlability results

`make ci` passes with **0 errors and 0 warnings across 33 pages**. Verified:

- build existence for every manifest route;
- exactly one `<h1>` per page; valid `lang`; `dir="rtl"` on Hebrew;
- self-canonical; reciprocal hreflang; complete Open Graph;
- no unresolved `{{ … }}` template placeholders in shipped HTML;
- no broken in-page anchors, no broken internal links, no missing image files;
- indexability consistent across page `robots`, the manifest, and the sitemap;
- no accidental staging/preview URLs;
- every Play Store link carries the verified application id
  (`com.elmlaunch.myapp`) — no generic store links;
- no duplicate titles, descriptions, or page bodies.

---

## 7. Accessibility results

Structural accessibility is enforced automatically and passes: a skip link, one
`H1` and a logical heading order, `alt` on every image (`alt=""` only for
decorative), explicit `width`/`height` on content images (limits layout shift),
native accessible `<video>` controls with a captions track and a visible
transcript, keyboard-operable FAQ (`<details>`), and a text equivalent for the
privacy/security data-flow figure.

**Perceived** accessibility (focus order, screen-reader narration, reduced
motion, JavaScript-disabled resilience, contrast in light/dark) is covered by
the **manual QA matrix** (`docs/seo/qa-matrix.md`), which must be run before
release. The Lighthouse accessibility budget is a **hard gate** (≥ 0.95).

---

## 8. Performance results

Performance is measured by optional Lighthouse CI against six representative
pages (English/Hebrew home, English/Hebrew product, a guide, privacy/security).
Budgets are documented in `docs/seo/performance-budgets.md`:

- **Hard gates:** Accessibility ≥ 0.95, SEO ≥ 0.95, CLS ≤ 0.10.
- **Warnings (surfaced, non-blocking):** Performance ≥ 0.85, Best-practices
  ≥ 0.90, transfer/image/script weight, console errors.

Performance is intentionally a *warning*, not a hard gate: the homepage carries
a product film and marketing renders on purpose, and the marketing site runs
Google AdSense. We do not want CI to pressure anyone into deleting useful media
or accessibility features to chase a score. Media weight is controlled with WebP
`<picture>` derivatives, `loading="lazy"`, and explicit dimensions.

> Lighthouse numbers depend on a headless-Chrome runner and network conditions;
> capture the actual scores from the CI "lighthouse-report" artifact at release
> and paste them here for the record.

---

## 9. Product facts reverified

The Android app repository was re-cloned and its `Main` HEAD (`df98c3e`) is the
**same commit** the product-facts registry was built from — so no implemented
behavior has changed. Each flagged claim was re-checked against source and
matches: version 1.1.0 (code 10), Android 8.0+ / Wear OS 3+, application id
`com.elmlaunch.myapp`, no billing and no price string, five Glance widgets, Wear
tile + complication, on-device OCR (ML Kit Latin + Tesseract Hebrew), SQLCipher
at-rest encryption, biometric lock, optional Sentry (`isSendDefaultPii = false`),
optional Supabase sync, in-app `delete_own_account`, and six regional presets.
Details and evidence are in `docs/seo/product-facts.md` (see its
"Re-verification (2026-07-16)" section). The only edit was correcting one line
citation (deletion RPC 189 → 193).

Facts that remain **unverifiable from source** and must not be published as
fact: live Play-listing availability, price/monetization, and store
rating/review count.

---

## 10. Privacy issues resolved

- `privacy.html` now cleanly separates **App data** from **Website data**. It
  discloses Google AdSense honestly, scopes "no ads / no analytics SDK" claims
  to the *app*, and describes SQLCipher as local-database encryption **at rest**
  (explicitly not end-to-end).
- `/delete-account/` (+ Hebrew) documents in-app deletion, cloud-vs-local data,
  and uninstall behavior, and states plainly that there is **no** web deletion
  form.
- A data-flow diagram with a text equivalent was added to `/privacy-and-security/`.
- The vendor-neutral analytics layer (`assets/analytics.js`) sends no page copy,
  emails or full URLs, respects consent, embeds no analytics ID, and no-ops when
  no provider is configured. A privacy-data inventory and a legal-review list
  are in `docs/seo/privacy-data-inventory.md`.

---

## 11. Unresolved manual decisions

These require a human (product / legal / owner) decision — none is resolvable
from source and none has been assumed:

1. **AdSense consent (EEA/UK)** — the site loads AdSense with no consent
   mechanism. Decide whether a CMP is required and wire `window.__elmtrackrConsent`
   to it. (Documented blocker; no banner was invented.)
2. **Is AdSense intended at all**, given the app's ad-free positioning?
3. **Live Play-listing availability** — confirm `com.elmlaunch.myapp` is public
   before treating any CTA as a live store link.
4. **Price / monetization** — the app has no price string; any price claim must
   come from the confirmed live listing.
5. **Store rating / reviews** — do not publish until verifiable.
6. **Formal Hebrew policy/terms** — the binding legal pages are English only.
7. **Support address** — confirm `support@elmtrackr.site` is monitored.
8. **Retention / backups** for Supabase and Sentry.
9. **Play Data-safety alignment** with `/delete-account/` as the deletion URL,
   and confirmation of exactly what in-app deletion removes (cloud vs local DB).
10. **Legal entity / data-controller identity** and the GDPR/CCPA request process.
11. **Canonical brand spelling** — the app is "ElmTrackr"; the site mixes forms.

---

## 12. Google Search Console — setup steps

1. Sign in at Google Search Console and add a property. Prefer a **Domain**
   property (`elmtrackr.site`) verified via a DNS TXT record; this covers
   `http`/`https`, `www`/non-`www` and all subpaths in one property.
2. If DNS verification is not possible, add a **URL-prefix** property for the
   exact production origin and verify with the HTML-file or meta-tag method.
3. Submit the sitemap: **Sitemaps → add** `https://elmtrackr.site/sitemap.xml`.
4. Use **URL Inspection** on the homepage and one product page; request indexing
   for the key pages.
5. Confirm the **International Targeting** / hreflang report shows no errors once
   Google has recrawled.
6. Set the property's users so the owner and any maintainers have access.

## 13. Bing Webmaster Tools — setup steps

1. Sign in at Bing Webmaster Tools. You can **import from Google Search Console**
   (fastest) or add `https://elmtrackr.site` manually.
2. If adding manually, verify via DNS CNAME/TXT or the meta-tag/XML-file method.
3. Submit `https://elmtrackr.site/sitemap.xml` under **Sitemaps**.
4. Use **URL Inspection** + **Submit URL** for the homepage and top pages.
5. Bing also powers other engines and some AI assistants, so a healthy Bing
   index helps beyond Bing itself.

## 14. Recommended post-launch indexing checks

- Confirm `robots.txt` is reachable and does not block content:
  `https://elmtrackr.site/robots.txt`.
- Confirm the sitemap loads and lists 30 URLs.
- Spot-check `site:elmtrackr.site` in Google and Bing after ~1–2 weeks; expect
  the indexable pages to begin appearing.
- In Search Console, watch **Pages** for "Crawled – currently not indexed" or
  "Excluded by noindex" — the only expected noindex pages are `/privacy.html`,
  `/terms.html`, and `/404.html`.
- Verify hreflang is recognized (International Targeting report) and that the
  Hebrew pages rank for Hebrew queries, not the English ones.
- Re-run `make ci` and the manual QA matrix on the live URL.
- Check that Play Store CTAs open the correct listing and carry the differentiated
  campaign parameters (see `docs/seo/analytics.md`).
- Watch for `chatgpt`/`bing`/`perplexity` referral categories once an analytics
  provider is connected (see `docs/seo/analytics.md`).

## 15. Rollback instructions

Every change is a static-file edit deployed via GitHub Pages from the default
branch.

- **Single change:** `git revert <commit>` and push; Pages redeploys the prior
  state on the next push to the deployment branch.
- **Whole release:** revert the merge, or reset the deployment branch to the
  last-known-good commit and push. Because the build is deterministic
  (`make build` is idempotent) the regenerated output will match the reverted
  sources.
- **Config-only rollback:** the sitemap and generated pages derive entirely from
  `scripts/seo_manifest.json` + `content/` + `templates/`; reverting those and
  running `make build` restores the previous routes/metadata exactly.
- The deploy workflow strips internal files (`docs/`, `AGENTS.md`, `content/`,
  `templates/`, `scripts/`) from the published artifact, so reverting them never
  affects what is served.

---

## Commands run for this release

```
make ci                 # build + validate + audit + dist (0 errors, 0 warnings)
make check-clean        # confirms generated output matches committed sources
python3 scripts/audit_site.py     # 33 pages audited, PASS
```

See "Limitations" in the accompanying task summary for what could not be
verified in this environment (live Lighthouse scores, live Play listing, and
the human legal-review items in §11).
