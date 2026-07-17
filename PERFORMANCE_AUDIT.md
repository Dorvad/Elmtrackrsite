# Elmtrackr performance audit

Baseline date: 2026-07-17. This is an evidence-only audit. No website markup, styling, scripts, or media were changed.

## Executive summary

Elmtrackr is a static, framework-free site. The English and Hebrew homepages are handwritten HTML with inline CSS and vanilla JavaScript; secondary pages are generated from JSON by standard-library Python. There is no React, Next.js, Vite, bundler, dependency graph, or asset optimization pipeline.

The largest performance risk is `assets/elmtrackr-tour.mp4` at 11,471,838 bytes (10.94 MiB). The other confirmed issues are a non-responsive LCP image, five font subset requests on the English homepage, eagerly loaded Google advertising code, and a perpetual `requestAnimationFrame` loop that measures layout every frame. Production is served directly by GitHub Pages, which currently returns `Cache-Control: max-age=600` for first-party assets and does not provide repository-level per-file header configuration.

## 1. Stack and deployment model

| Area | Current implementation |
| --- | --- |
| Rendering | Static HTML. `index.html` and `he/index.html` are complete standalone pages. |
| Framework | None. No React, Next.js, Vite, Astro, Vue, or other client framework. `support.js` is historical, generated, and unused. |
| Build | `Makefile` orchestrates standard-library Python: `scripts/build_content_pages.py` generates 28 locale pages, and `scripts/build_sitemap.py` generates `sitemap.xml`. |
| Content sources | `content/pages/**/*.json` plus `templates/*.html`; the two homepages are not generated from these templates. |
| Production artifact | `make dist` copies site files into `_site/` with `tar`. Assets are copied byte-for-byte. |
| Deployment | `.github/workflows/deploy-pages.yml` publishes to GitHub Pages using `actions/upload-pages-artifact` and `actions/deploy-pages`. The workflow publishes the repository root after removing selected internal directories; committed generated HTML is therefore the deployed HTML. |
| Jekyll | Disabled by `.nojekyll`. |
| Asset naming | Fixed human-readable filenames. No first-party production asset is content-hashed. |
| Hosting headers | Live assets identify `Server: GitHub.com`, `Via: 1.1 varnish`, and `Cache-Control: max-age=600`. GitHub Pages supports the custom domain, but this deployment does not expose per-file custom response-header rules. |

Official deployment references: [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) and [GitHub Pages custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages).

### Build baseline

GNU Make is not installed in this Windows environment, so the documented targets were run through their underlying commands and the `_site` copy was assembled according to `Makefile:70-79`.

- Generated 28 English/Hebrew content pages and a 30-URL sitemap.
- `build_content_pages.py --check`, `build_sitemap.py --check`, `validate_seo.py`, `check_locales.py`, and `check_static_html.py` passed.
- `_site/` contains 78 files and 33 HTML pages, totaling 22,118,066 bytes (21.09 MiB).
- The artifact total is not page weight: 8.47 MiB is unlinked source material under `uploads/`, and the artifact also contains unused `support.js`.

## 2. Source ownership by reported issue

There are no source “components” in a framework sense. The relevant components are literal HTML blocks.

| Finding | Exact source |
| --- | --- |
| 11.9 MB page / 11.2 MB video | Binary: `assets/elmtrackr-tour.mp4`. English video: `index.html:844-847`; Hebrew video: `he/index.html:851-854`. The inline video controller is `index.html:1040-1069` and `he/index.html:1047-1076`. |
| Tour video renderer | Raw `<video controls preload="metadata">` and `<source>` elements in the two homepage files above. JSON-LD mentions at `index.html:105` and `he/index.html:112` do not initiate media download. |
| Oversized home-screen image | Binary sources: `assets/elmtrackr-home-screen.webp` and `.jpg`. Homepage `<picture>`: `index.html:534` and `he/index.html:541`. The same image is also an authored content-page image in `content/pages/{hourly-pay-tracker,shift-tracker-android}.json` and their Hebrew equivalents. |
| LCP priority | The homepage `<img>` lines above have no `fetchpriority` and no responsive `srcset`/`sizes`. They are eager by default because there is no `loading="lazy"`. |
| Short first-party caching | `.github/workflows/deploy-pages.yml:24-42` deploys directly to GitHub Pages. There is no `_headers`, `netlify.toml`, `vercel.json`, server config, or edge-worker config. |
| Critical fonts | Homepage declarations: `index.html:121-360` and `he/index.html:128-367`. Shared generated-page declarations: `assets/content-pages.css:6-11`. Other standalone declarations: `privacy.html:24-26`, `terms.html:22-91`, and `404.html:24`. |
| AdSense / DoubleClick / Funding Choices | The only authored advertising tag is the async AdSense loader at `index.html:117-118` and `he/index.html:124-125`. DoubleClick, ad-quality scripts, iframes, and region/account-dependent Funding Choices are injected by that Google loader; there is no authored Funding Choices tag in the repository. |
| First-party analytics | `assets/analytics.js`, loaded with `defer` at `index.html:1077`, `he/index.html:1084`, and `templates/page.html:46` (which places it on all 28 generated pages). |
| Main-thread work | Authored homepage CSS/JS plus Google-injected scripts. The continuous widget animation is `index.html:1014-1037` / `he/index.html:1021-1044`; the one-second text/ring update is `index.html:983-1003` / `he/index.html:990-1010`; layout-affecting CSS animations are `index.html:366-367` / `he/index.html:373-374`. |
| Forced reflow | `stage.getBoundingClientRect()` at `index.html:1025` and `he/index.html:1032`. Lighthouse reports this as zero-based line 1024 for the English page. |

## 3. Major asset sizes

Sizes are repository bytes, not compressed transfer estimates.

| Asset | Bytes | Binary size | Dimensions / note |
| --- | ---: | ---: | --- |
| `assets/elmtrackr-tour.mp4` | 11,471,838 | 10.94 MiB | Dominates possible page transfer. |
| `assets/render-widgets-tablet.jpg` | 151,046 | 147.51 KiB | 1400×933 |
| `assets/render-watch-glance.jpg` | 141,746 | 138.42 KiB | 1100×1100 |
| `assets/render-watch-live.jpg` | 128,335 | 125.33 KiB | 1100×1100 |
| `assets/render-watch-glance.webp` | 71,318 | 69.65 KiB | 1100×1100 |
| `assets/render-widgets-tablet.webp` | 69,764 | 68.13 KiB | 1400×933 |
| `assets/elmtrackr-home-screen.jpg` | 62,485 | 61.02 KiB | 720×1600 fallback |
| `assets/render-watch-live.webp` | 61,088 | 59.66 KiB | 1100×1100 |
| `assets/elmtrackr-home-screen.webp` | 35,250 | 34.42 KiB | 720×1600; selected by the homepage `<picture>` |
| `assets/elmtrackr-app-tour-poster.jpg` | 19,975 | 19.51 KiB | 720×1280; current `<video poster>` |
| `assets/elmtrackr-app-tour-poster.webp` | 4,648 | 4.54 KiB | Existing but not used by the `<video>` |
| `index.html` | 90,466 | 88.35 KiB | Inline CSS and JS included |
| `assets/analytics.js` | 7,843 | 7.66 KiB | Deferred first-party helper |

At a 412×823 viewport, the selected home-screen WebP remained 720×1600 while its rendered box was approximately 343×597 in the browser check. Lighthouse 13 measured a 308×594 box and estimated 29,853 bytes of the 35,250-byte WebP could be avoided with responsive delivery. The image is discoverable and eager, but the LCP discovery audit failed solely because `fetchpriority="high"` is absent.

The video uses `preload="metadata"`, but the media URL was still observed during initial loading and reached `readyState=4` during browser inspection. The supplied Lighthouse run downloaded approximately the entire video; the local rerun ended while the media request was still in progress, so its 535 KiB reported payload must not be interpreted as the full cost of the page.

## 4. Fonts

All faces use `font-display: swap`. There are no `<link rel="preload" as="font">` declarations anywhere in shipped HTML.

### Physical font files

| File | Bytes | KiB |
| --- | ---: | ---: |
| `archivo-latin-ext.woff2` | 32,608 | 31.84 |
| `archivo-latin.woff2` | 34,928 | 34.11 |
| `archivo-vietnamese.woff2` | 13,240 | 12.93 |
| `plex-mono-500-cyrillic-ext.woff2` | 6,972 | 6.81 |
| `plex-mono-500-cyrillic.woff2` | 8,460 | 8.26 |
| `plex-mono-500-latin-ext.woff2` | 13,432 | 13.12 |
| `plex-mono-500-latin.woff2` | 14,888 | 14.54 |
| `plex-mono-500-vietnamese.woff2` | 6,040 | 5.90 |
| `plex-mono-600-cyrillic-ext.woff2` | 7,692 | 7.51 |
| `plex-mono-600-cyrillic.woff2` | 9,352 | 9.13 |
| `plex-mono-600-latin-ext.woff2` | 14,328 | 13.99 |
| `plex-mono-600-latin.woff2` | 15,620 | 15.25 |
| `plex-mono-600-vietnamese.woff2` | 6,932 | 6.77 |

Total font directory: 184,492 bytes (180.17 KiB).

### Declarations

- `index.html` and `he/index.html`: 25 faces each. Archivo weights 500/600/700/800/900 are each declared for Vietnamese, Latin Extended, and Latin, even though the same three variable-font files are reused. IBM Plex Mono weights 500 and 600 are each declared for Cyrillic Extended, Cyrillic, Vietnamese, Latin Extended, and Latin.
- `assets/content-pages.css`: six faces—Archivo 100–900 for Latin and Latin Extended; Plex Mono 500 and 600 for Latin and Latin Extended.
- `privacy.html`: Archivo 100–900 for Latin and Latin Extended, plus Plex Mono 600 Latin.
- `terms.html`: Archivo 500/700/800 for Latin and Latin Extended, plus Plex Mono 600 Latin.
- `404.html`: Archivo 100–900 Latin.

### Actual English-homepage font requests

The browser inventory and local Lighthouse agreed on five requests, all at `VeryHigh` priority in Lighthouse:

| Request | Bytes |
| --- | ---: |
| `archivo-latin.woff2` | 34,928 |
| `archivo-latin-ext.woff2` | 32,608 |
| `plex-mono-600-latin.woff2` | 15,620 |
| `plex-mono-600-latin-ext.woff2` | 14,328 |
| `plex-mono-600-cyrillic.woff2` | 9,352 |

## 5. Third-party and first-party scripts

### Google advertising chain

The authored homepage loader is:

`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6818267616933452`

It is `async` and appears only on the two homepages. In the local and live browser inspections it injected:

- `show_ads_impl_fy2021.js` from `pagead2.googlesyndication.com`;
- DoubleClick ad/lookup iframes from `googleads.g.doubleclick.net`;
- `sodar2.js`, configuration calls, and a runner frame from `ep1/ep2.adtrafficquality.google`;
- a Google reCAPTCHA frame.

Funding Choices was not reproduced in the audit session and has no repository source. If present in the supplied Lighthouse trace, it is a conditional part of the AdSense/account/geography chain and can only be controlled indirectly through Google configuration or by changing when AdSense itself loads.

Local Lighthouse attributed 226,527 transferred bytes to Google/DoubleClick Ads and 21,487 bytes to ad-traffic-quality endpoints. Its unused-JavaScript audit estimated 155 KiB savings: 128,419 wasted bytes in `show_ads_impl_fy2021.js` and 30,321 in `adsbygoogle.js`.

### `assets/analytics.js`

The 7.66 KiB script is loaded with `defer`, after the homepage inline enhancement script and at the end of the shared page template. It installs click/aux-click, video, and FAQ listeners. It contains no analytics property ID and sends nothing unless an existing `window.gtag` or `window.dataLayer` provider is present. It does not perform layout measurements.

## 6. Main-thread work and forced reflow

No authored `scroll` or `resize` event listener exists. The main layout-sensitive path is the widget choreography:

1. A `requestAnimationFrame` loop starts immediately and never stops.
2. Every frame reads `window.innerHeight` and calls `stage.getBoundingClientRect()`.
3. The same frame writes `opacity` and `transform` on up to four widget elements.
4. The following frame measures again after the prior mutations. The loop runs even when the widget section is far outside the viewport.

This is the likely source of the supplied 64 ms forced reflow. The local Lighthouse 13.4 rerun independently identified `index.html:1025` (reported as zero-based line 1024, column 27) and measured 97.247 ms total reflow time. The Hebrew duplicate has the same logic at `he/index.html:1032`.

Other authored work that can add style/layout/paint cost:

- the one-second `paint()` interval changes several text nodes and SVG `stroke-dasharray` attributes;
- `floatPhone` and `floatWatch` animate `margin-top`, which is layout-affecting rather than compositor-only;
- video `timeupdate` changes the progress bar's `width` while playing;
- `IntersectionObserver` controls video play/pause and is not itself a forced-reflow concern.

Local Lighthouse main-thread time was 4.23 s: 1.40 s other, 1.28 s style/layout, 0.85 s script evaluation, 0.58 s rendering, 0.07 s script parsing/compilation, and 0.05 s HTML/CSS parsing. It found seven long tasks; the largest first-party task was 257 ms, while AdSense tasks were 148 ms and 126 ms.

## 7. Local mobile Lighthouse baseline

Lighthouse 13.4.0 ran against the locally served `_site/` with the mobile preset, a Moto G Power user agent, 412×823 screen emulation, and DPR 1.75.

The complete 486,730-byte JSON report was written successfully. The CLI then returned a Windows `EPERM` while deleting its temporary Chrome profile; that cleanup error occurred after report generation and does not invalidate the recorded metrics.

| Metric | Result |
| --- | ---: |
| Performance score | 70 |
| First Contentful Paint | 1.4 s |
| Largest Contentful Paint | 6.6 s |
| Speed Index | 1.8 s |
| Total Blocking Time | 310 ms |
| Cumulative Layout Shift | 0.007 |
| Main-thread work | 4.2 s |
| JavaScript bootup | 0.9 s |
| Recorded transfer | 535 KiB |
| Forced reflow | 97.247 ms at `index.html:1025` |

The recorded transfer excludes most of the unfinished video download and the local Python server intentionally had no cache headers. For production cache behavior, use the live header measurements below rather than the local cache audit.

## 8. Prioritized implementation plan

### P0 — largest impact

1. **Stop the tour video from participating in initial page load.** Keep the current poster/controls visually intact, but defer assigning the MP4 source until user intent or until the film is genuinely near the viewport. Produce a materially smaller encode and verify byte/range behavior before choosing variants. Responsible sources: homepage video blocks and controllers plus `assets/elmtrackr-tour.mp4`.
2. **Decide when advertising is allowed to load.** Loading AdSense immediately gives Google, DoubleClick, ad-quality, and conditional Funding Choices work access to the critical path. Gate or defer the single authored AdSense loader according to the product's advertising and consent requirements; measure revenue/behavior separately from the performance implementation.

### P1 — LCP and main-thread path

3. **Deliver a responsive LCP image and add `fetchpriority="high"`.** Generate dimensions that match mobile and desktop display sizes, add `srcset`/`sizes`, retain the existing WebP/JPG fallback semantics, and verify the same crop and appearance. Lighthouse estimated about 29.9 KB avoidable on this 35.3 KB resource.
4. **Remove the per-frame layout read.** Cache stable geometry, update it only when needed, and run animation work only while the widget stage is near the viewport. Preserve the current transforms but ensure a frame does not read layout after prior invalidating writes.
5. **Reduce critical font subsets before considering preloads.** Consolidate the repeated Archivo declarations around the existing variable font, determine which glyphs cause Latin Extended/Cyrillic Plex requests, and ship only the subsets actually needed by each locale. Adding five preloads would compete with the LCP request and is not the first fix.
6. **Move layout animations to compositor-only properties.** Replace the two `margin-top` float animations with visually equivalent transforms, then re-profile style/layout time.

### P2 — delivery and regression protection

7. **Use the smaller existing poster format if compatibility testing permits.** The current 19,975-byte JPG poster is used while a 4,648-byte WebP exists unused.
8. **Exclude non-site payload from the production artifact.** `uploads/` and unused `support.js` do not affect current page load but add roughly 8.9 MiB to the deployed artifact and remain publicly addressable.
9. **Make performance regression checks reliable.** The CI Lighthouse job is `continue-on-error`, performance assertions are warnings, and an unfinished video request can evade the total-byte budget. Add a deterministic static size check for the MP4 and key images in addition to Lighthouse.
10. **Introduce versioned asset URLs if long-lived caching becomes available.** First-party names are currently stable and unhashed, so immutable caching would otherwise risk serving stale files.

## 9. Hosting-level limitation

Read-only HEAD requests to the live MP4, WebP, and `analytics.js` all returned:

- `Server: GitHub.com`
- `Cache-Control: max-age=600`
- `Accept-Ranges: bytes`
- an `ETag`, Fastly/Varnish headers, and a ten-minute `Expires` value

The ten-minute lifetime is controlled by GitHub Pages, not by HTML or the Python build. There is no supported repository file in this deployment that can change GitHub Pages' response headers per asset. Fixing this completely therefore requires an infrastructure decision: place a configurable CDN/proxy in front of Pages or move static hosting to a provider that accepts custom cache rules. Content-hashed filenames can be implemented in this repository, but GitHub Pages would still emit its own short cache policy until the serving layer changes.
