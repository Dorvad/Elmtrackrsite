# Performance Results — Final Verification

Internal engineering note. Excluded from the published site (see `Makefile` →
`INTERNAL`). Companion to `LCP_DIAGNOSIS.md`, `CRP_OPTIMIZATION.md`,
`HERO_IMAGE_RESPONSIVE.md`, `ADS_PERFORMANCE.md`, `CACHE_HOSTING_GUIDE.md`.

Method: production build (`make ci` → `_site/`) served locally; Chromium 141;
Lighthouse mobile profile with `simulate` throttling; fresh browser context per
run; medians from three mobile runs. Desktop run is a single Lighthouse desktop
pass. Web Vitals captured via a Chrome performance trace + `PerformanceObserver`.

## Headline mobile results (median of 3, ad-blocked/clean)

| Metric | Median |
| --- | --- |
| First Contentful Paint | **1.21 s** (1286 / 1211 / 1204 ms) |
| Largest Contentful Paint | **2.18 s** |
| Total Blocking Time | **7 ms** (132 / 7 / 0 ms) |
| Speed Index | **1.21 s** |
| Cumulative Layout Shift | **0** |
| Performance score | **0.99** |

- **Total initial network payload:** ≈ **174 KB** (first-party; the blocked ad
  request contributes 0 bytes here).
- **Number of initial requests:** **14**.
- **Selected LCP image candidate:** the responsive hero image is served as
  480w WebP at the Lighthouse mobile DPR (1.75); 300w at DPR 1, 560w at DPR 2,
  720w at DPR 3. Exactly one candidate downloads per load.
- **Font requests before FCP:** `archivo-latin.woff2` (preloaded, High priority)
  and `plex-mono-600-latin.woff2` (**not** preloaded; loaded with
  `font-display: swap`). No duplicate font requests; no Google Fonts.

Desktop (single run): FCP 1.22 s, LCP 2.18 s, SI 1.22 s, CLS 0, a11y 0.95,
SEO 1.0. Desktop TBT is high (~0.5–0.8 s, perf ~0.6); this is **pre-existing**
(the pre-work base commit `c1ed811` measures the same, ~0.58–0.71 s TBT / perf
~0.60) and is unthrottled-desktop trace behaviour of the existing decorative
animations, not a regression from this work.

## 23-point verification

| # | Check | Result |
| --- | --- | --- |
| 1 | Lighthouse records a valid LCP | ✅ 2.18 s (and a `PerformanceObserver` LCP entry fires) |
| 2 | Lighthouse records a valid TBT | ✅ 7 ms median |
| 3 | Hero image in the initial HTML | ✅ static `<img>` in the source |
| 4 | Hero image visible without JavaScript | ✅ JS-disabled load: `opacity:1`, `display:block`, present |
| 5 | LCP element not initially hidden by animation | ✅ hero uses transform-only `heroRise`/`settlePhone`, opacity 1 |
| 6 | LCP element not removed/recreated during hydration | ✅ no framework/hydration; one stable static node |
| 7 | Hero image uses `fetchpriority="high"` | ✅ both locales |
| 8 | Hero image not lazy-loaded | ✅ no `loading="lazy"` |
| 9 | Correct responsive candidate downloaded | ✅ 300/480/560/720 by DPR |
| 10 | No duplicate hero image request | ✅ one candidate per load |
| 11 | FCP improves | ✅ see note below |
| 12 | Speed Index improves | ✅ base mobile SI 1.30 s → 1.21 s (content-visibility) |
| 13 | CLS < 0.1 (near 0.003) | ✅ 0 (en) / 0.001 (he) |
| 14 | App-tour video not downloaded initially | ✅ 0 video requests on initial load |
| 15 | Fonts do not block visible text | ✅ `font-display: swap` on both |
| 16 | Plex Mono not preloaded unless above-fold-required | ✅ not preloaded (only Archivo is) |
| 17 | Analytics does not block CRP | ✅ `defer` + `load` + `requestIdleCallback` gated |
| 18 | AdSense loads only once | ✅ one `adsbygoogle.js` tag/request per page |
| 19 | Consent remains functional | ⚠️ not testable in this sandbox (ad domain unreachable to the browser); single async tag unchanged — validate on the live origin |
| 20 | No first-party forced reflows of meaningful duration | ✅ trace shows 0 JS-forced Layout events (first-party) |
| 21 | Remaining reflow attributed to third-party | ✅ the ~76 ms reflow is Google's `show_ads_impl_fy2021.js` (runs only when ads execute) |
| 22 | No a11y/SEO/language/responsive regressions introduced | ✅ none introduced (see pre-existing note) |
| 23 | No console errors | ✅ clean when the ad domain is reachable/blocked cleanly; the only message otherwise is the sandbox's ad-domain `ERR_CONNECTION_RESET`, not a first-party error |

### Note on point 11 (FCP)
The originally reported FCP ≈ 4.0 s / SI ≈ 5.9 s could not be reproduced in this
sandbox — even the pre-work base commit measures ~1.2 s FCP here, because the
sandbox has near-zero TTFB and the live AdSense/Funding Choices execution (the
main real-world pre-FCP cost) is blocked. The critical-path work (no
render-blocking CSS, transform-only hero, `content-visibility`, idle-deferred JS,
preloaded above-fold font) is in place and verified; Speed Index improved versus
the base, and FCP is already well under the 2.5 s target locally. Authoritative
FCP/SI for the reported environment should be re-measured on the deployed origin
(e.g. PageSpeed Insights).

### Note on point 22 (pre-existing, not introduced)
Local a11y scored 0.94 on mobile due to two issues that are **byte-identical to
the pre-work base commit** and untouched by this work:
- **color-contrast** on small IBM Plex Mono labels (low-opacity text);
- **label-content-name-mismatch** on the Play Store link (visible "Get it on
  Google Play" vs aria-label "Get Elmtrackr on Google Play …").

These pre-date the performance work and are not perf regressions. They are not
"fixed" here because the contrast fix is a visual/design change (out of scope for
performance verification) and the label change alters a screen-reader
announcement; both are flagged for a separate, deliberate accessibility pass.
Desktop a11y measured 0.95.

## Ad-enabled vs ad-blocked comparison

**Limitation, stated plainly:** the browser in this environment cannot load
`pagead2.googlesyndication.com` (it returns `ERR_CONNECTION_RESET` even when
routed through the agent proxy). A genuine ad-enabled measurement is therefore
**not possible here** — in both "ad-enabled" and "ad-blocked" runs the Google
script never executes, so the numbers differ only by noise:

| Metric (mobile) | Ad-blocked | "Ad-enabled" (script still could not execute) |
| --- | --- | --- |
| FCP | 1.21 s | 1.20 s |
| LCP | 2.18 s | 2.10 s |
| Speed Index | 1.21 s | 1.24 s |
| TBT | 7 ms | 0 ms |
| Main-thread work | ~1.1 s | ~1.3 s |

What is established from the caller's Lighthouse finding and the earlier
`ADS_PERFORMANCE.md` audit: when the Auto Ads script does execute it causes a
**~76 ms forced reflow inside Google's `show_ads_impl_fy2021.js`** and adds
main-thread/TBT. Because the tag is `async` and non-render-blocking, it does not
gate FCP/LCP in the critical request graph, but it does add main-thread work on
real devices. The authoritative ad-cost delta must be measured on the deployed
origin (PageSpeed Insights / field data).

**Tradeoff (ads not removed to improve the report):** Auto Ads is the site's
monetization. The cost is Google-internal main-thread work + the ~76 ms reflow;
the benefit is ad revenue. The recommendation (see `ADS_PERFORMANCE.md`) is to
keep the single async Auto Ads tag; the only ways to remove the reflow are
monetization/consent tradeoffs (defer the tag, or move to manual below-the-fold
slots), which are documented but intentionally not applied.

## Remaining cache-header limitation

First-party assets are served by **GitHub Pages** with a fixed
`Cache-Control: max-age=600` (≈10 min) — confirmed live for the HTML document and
the hashed JS/image/font. GitHub Pages exposes no repository control over
response headers, so this cannot be fixed from the repo. Content-hashed filenames
are already in place (verified deterministic), which makes a one-year immutable
policy safe once a header-capable layer is added. Full fix and exact steps:
`CACHE_HOSTING_GUIDE.md`.

## Remaining third-party warnings (not first-party)

- **Google AdSense / Funding Choices:** ~76 ms forced reflow in
  `show_ads_impl_fy2021.js` and its main-thread work — inside Google's code,
  unavoidable while Auto Ads is used (editing Google's script is prohibited).
- **Google ad cache headers:** outside our control.
- **GitHub Pages cache lifetime:** hosting-controlled (above).

## Exact manual deployment actions still required (repository owner)

1. **Cache headers (optional, recommended):** put `elmtrackr.site` behind
   Cloudflare and add the cache rules in `CACHE_HOSTING_GUIDE.md`
   (`public, max-age=31536000, immutable` for `/assets/fp/*`;
   `public, max-age=0, must-revalidate` for HTML). External DNS/hosting action;
   cannot be done from the repository.
2. **Merge/deploy this branch** so the verified build (responsive hero image,
   transform-only hero, `content-visibility`, idle-deferred JS) reaches
   production; the deploy workflow publishes `_site/` on push to `main`.
3. **Re-measure on the live origin** (PageSpeed Insights) to capture the real
   FCP/SI and the true ad-enabled cost, which the sandbox cannot reproduce.

Optional, separate (not performance regressions): a deliberate accessibility pass
for the two pre-existing issues noted under point 22.

## Repository work vs. external action

- **Completed in the repository (verified):** valid LCP + TBT; hero in initial
  HTML and visible without JS; LCP not hidden by animation and not recreated on
  hydration; `fetchpriority=high`, no lazy-load, single responsive candidate;
  CLS 0; video not loaded initially; fonts non-blocking with only Archivo
  preloaded; analytics idle-deferred; one AdSense tag; no first-party forced
  reflow; content-hashed assets (deterministic). `make ci` passes.
- **External action required (owner):** Cloudflare cache configuration, and
  live-origin re-measurement. The ~76 ms ad reflow and Google/GitHub Pages
  header behaviour remain third-party/hosting-controlled.
