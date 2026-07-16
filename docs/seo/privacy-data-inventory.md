# Elmtrackr — Privacy data inventory & legal-review list

**Date reviewed:** 2026-07-16
**Scope:** the public marketing website (`elmtrackr.site`, GitHub Pages) and,
separately, the Elmtrackr Android/Wear OS application.
**Source of product facts:** `docs/seo/product-facts.md`.

> This document is a factual inventory to support a human privacy/legal
> review. It is **not** legal advice and does not assert regulatory
> compliance. Items that need a product or legal decision are listed in the
> final section.

---

## 1. Website data inventory (`elmtrackr.site`)

The website is a static site served from GitHub Pages. It does not have a
first-party backend, does not run a first-party analytics product, and does not
set its own cookies.

| Data / mechanism | Present on the website? | What it involves | Notes for review |
|---|---|---|---|
| **Google AdSense** | Yes | Third-party ad script that can set cookies / use local storage and receives the visitor's IP address and ad-interaction signals per Google's policies. | This is the only third-party data-collecting component on the site. Consent handling for the EEA/UK is unresolved (see review list). |
| **First-party analytics product** | No | No GA/GTM property is configured on the pages today. | `assets/analytics.js` is a vendor-neutral **no-op** helper: with no `gtag`/`dataLayer` present it sends nothing. See `docs/seo/analytics.md`. |
| **First-party cookies** | No | The site sets no cookies of its own. | Any cookies observed come from AdSense. |
| **Outbound campaign parameters** | Yes (outbound only) | "Get it on Google Play" links carry `utm_*` values in the Play install `referrer`. These are attached to the destination URL; nothing is stored on the site. | Constant source/medium; only `utm_campaign`/`utm_content` vary by page/CTA. |
| **Contact forms / lead capture** | No | The site has no forms; it collects no names, emails, or messages. | Contact is via a published email address only. |
| **Hosting / server logs** | Via GitHub Pages | As with any web host, the hosting provider may process standard request metadata (e.g. IP, user agent) to serve pages. | We do not operate the logs; described cautiously in `privacy.html`. Confirm what GitHub Pages retains. |
| **Self-hosted tour video** | Yes | The homepage video is served from the site's own assets; no third-party video/player embed (e.g. YouTube) is used. | No third-party embed cookies from video. |
| **Third-party fonts / CDNs** | No third-party font CDN | Hebrew uses a system font stack; styles/scripts are first-party. | Confirm no future dependency reintroduces a third-party CDN. |
| **Referral classification** | Category string only | `analytics.js`, when a provider is later connected, derives a referrer *category* from the hostname and never forwards the raw referrer URL. | No PII; documented in `docs/seo/analytics.md`. |

---

## 2. App data inventory (Elmtrackr Android/Wear OS)

Sourced from `docs/seo/product-facts.md`. The app does **not** contain an
advertising SDK or a third-party analytics SDK (Sentry crash reporting is
optional and can be turned off).

| Data | Where it lives | Encryption / handling | Notes for review |
|---|---|---|---|
| Account email; optional display name | Account/sign-in | Standard account handling | Required to create an account. |
| Shifts, breaks, notes, pay rules | Local database (Room) | Local database encrypted **at rest** with SQLCipher (this is at-rest DB encryption, **not** end-to-end encryption) | Core work data. |
| Tasks | Local database (Room) | As above | |
| Reimbursement claims | Local database (Room) | As above | |
| Receipt images | Local storage | As above; text extraction via **on-device OCR** (Latin + Hebrew), which is not perfect | OCR runs on device per product-facts; confirm no cloud OCR path exists. |
| Optional cloud sync | Supabase | Transmitted for sync when the user enables it | Retention/backup specifics on Supabase need confirmation. |
| Crash diagnostics | Sentry (optional) | User can opt out | Confirm what crash payloads include and default state. |
| Account/data deletion | In-app: Settings → Account → Delete account | Deletes cloud-synced data; local data cleared | Confirm whether in-app deletion also wipes the local Room DB, and uninstall behavior. |

The website does not receive or store any of the app's work data.

---

## 3. Public-facing pages that make privacy claims

| Page | Route | Indexable? | Purpose |
|---|---|---|---|
| Privacy Policy | `/privacy.html` | `noindex, follow` (documented decision) | Formal policy; separates App data vs Website data. |
| Terms | `/terms.html` | `noindex, follow` | Formal terms. |
| Privacy & security (educational) | `/privacy-and-security/` (+ `/he/`) | Indexable | Plain-language explanation + data-flow diagram. |
| Delete account | `/delete-account/` (+ `/he/`) | Indexable | How to delete in-app; cloud vs local data; uninstall; help email. States there is **no** web deletion form. |

All four are linked from the site footer (English and Hebrew).

---

## 4. Items requiring human legal / product review

These need a human decision — do not treat any as resolved:

1. **AdSense consent (EEA/UK).** The site loads Google AdSense but has **no
   consent mechanism / CMP**. A privacy/legal owner must decide whether a
   consent banner is required for target regions and, if so, which CMP — then
   `window.__elmtrackrConsent` can be wired to it. Documented as a blocker; no
   banner was invented.
2. **Is AdSense intended at all?** The app is positioned as ad-free. Confirm
   whether running ads on the marketing site is the intended business decision,
   given that positioning.
3. **Formal Hebrew policy/terms.** The formal `privacy.html`/`terms.html` are
   in English. Decide whether legally binding Hebrew versions are required for
   Hebrew-speaking users.
4. **Support address monitoring.** Confirm `support@elmtrackr.site` is
   monitored and is the correct contact for privacy/deletion requests.
5. **Retention & backups.** Confirm retention periods and backup handling for
   Supabase (synced data) and Sentry (crash data); the policy currently avoids
   stating specifics that aren't verified.
6. **Play Data safety alignment.** Ensure the Play Console Data safety form and
   the declared account-deletion URL match `/delete-account/` and the app's
   actual behavior.
7. **In-app deletion scope.** Verify precisely what Settings → Account → Delete
   account removes (cloud only vs cloud + local Room DB) so `/delete-account/`
   stays accurate.
8. **Controller / legal entity identity.** The policy does not name a legal
   entity or data controller. Decide whether one must be published.
9. **GDPR/CCPA request handling.** Decide the process for access/deletion/
   objection requests and whether the current email-only route is sufficient.
10. **On-device OCR confirmation.** Confirm OCR is fully on-device with no cloud
    fallback, so the "on-device" description stays accurate.
11. **GitHub Pages log retention.** Confirm what request metadata the hosting
    provider retains, to keep the hosting-logs description accurate.
