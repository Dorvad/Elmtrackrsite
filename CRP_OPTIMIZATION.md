# Critical Rendering Path Optimization — Home Page (en + he)

Internal engineering note. Excluded from the published site (see `Makefile` →
`INTERNAL`). Follow-up to `LCP_DIAGNOSIS.md`.

## Objective

Reduce time-to-first-visible-content (FCP ≈ 4.0 s, Speed Index ≈ 5.9 s as
originally reported) by fixing what happens *before* First Contentful Paint,
without redesigning the page or manipulating the metric.

## What the measurement showed (before)

Measured against the actual `make dist` output (`_site/`), Lighthouse mobile
profile, `simulate` throttling, Chromium 141.

- **TTFB (server-response-time): 7 ms** locally — not a factor in this build.
- **Render-blocking resources: none.** All CSS is inline; there are no external
  stylesheets on the critical path.
- **Fonts:** `archivo-latin.woff2` is preloaded (one request, correctly mapped to
  the fingerprinted file — no duplicate) and loads at High priority.
  `plex-mono-600-latin.woff2` is *not* preloaded and loads later; both use
  `font-display: swap`. This is already correct (see "Fonts" below).
- **Scripts:** the only render-relevant third party is Google's
  `adsbygoogle.js` (Auto Ads + Funding Choices/consent), `async` in `<head>`.
  The three first-party scripts (`widget-choreography`, `lazy-video`,
  `analytics-loader`) are all `defer` + Low priority and self-gate on
  IntersectionObserver / `load` + `requestIdleCallback`.
- **DOM / CSS:** ~511 elements, ~7 KB of inline `<style>`, ~30 KB of per-element
  `style=` attributes. Not oversized.
- **Main-thread Style & Layout: 629 ms** — the single largest addressable cost,
  driven by laying out the whole (mostly below-the-fold) page up front.
- **`he/index.html` regression:** the Hebrew home page had never received the
  hero opacity-0 fix from `LCP_DIAGNOSIS.md`, so it still faded its LCP
  candidates from `opacity: 0` (a latent `NO_LCP` on that locale).

Conclusion: the *code-level* critical path was already largely clean (no
render-blocking CSS, deferred scripts, preloaded above-fold font). The reported
4.0 s comes primarily from the measuring environment (real-network TTFB and the
live AdSense/Funding Choices execution, which is blocked in this sandbox and so
cannot be reproduced here). The addressable in-repo wins were main-thread
rendering cost, deferred nonessential JS, and the `he` hero regression.

## Changes implemented

All changes were applied to **both** `index.html` and `he/index.html`.

1. **`he/` hero LCP fix (parity with `index.html`).** `settlePhone` is now
   transform-only; a transform-only `heroRise` keyframe replaces `riseIn` on the
   hero `<h1>` and `<p>`. The Hebrew hero no longer fades from `opacity: 0`, so it
   is a valid LCP candidate. (Requirements: hero in initial HTML, visible without
   JS, LCP not tied to an animation timeline.)

2. **`content-visibility: auto` on below-the-fold sections** (`#overview`,
   `#method`, `#premiums`, `#estimate`, `#watch`, `#steps`, `#explore`, `#faq`,
   `#price`). The browser skips their layout/paint until they approach the
   viewport, cutting initial Style & Layout. `contain-intrinsic-size: auto 900px`
   uses the `auto` keyword so each section's real height is remembered after first
   render — no scrollbar jump, no layout shift. Excluded: `#widgets` (its scroll
   choreography reads live geometry) and `#film` (lazy video). It is a no-op where
   `content-visibility` is unsupported (progressive enhancement).

3. **Idle-deferred nonessential enhancement** (item 13). The inline enhancement
   script now runs its first `paint()` immediately (so displayed values stay
   consistent with the static HTML → no CLS), then defers the once-a-second live
   tick (`setInterval`) and the hover wiring behind
   `requestIdleCallback(…, { timeout: 2000 })` with a `setTimeout(…, 1200)`
   fallback. This keeps that work off the critical window.

4. **AdSense / Funding Choices left `async` in `<head>` — deliberately.** The
   single Auto Ads tag also delivers Google's consent UI (Funding Choices). Per
   requirement 9 ("do not delay legally required consent UI behind nonessential
   application code") and the standing in-file note not to idle-delay it without a
   consent + Auto Ads review, it was **not** moved or delayed. Analytics
   (requirement 10) is separate and already `load` + idle deferred.

No performance library was added (item 14). No CSS framework or external
stylesheet was introduced. Lighthouse reported no actionable `unused-css-rules`
(the inline CSS is already minimal), so no CSS was removed.

## Results (after)

Lighthouse mobile, `simulate`, 3 runs each, fresh context, from `_site/`.

**English (`/index.html`)** — median of 3:

| Metric | Before | After (median) |
| --- | --- | --- |
| First Contentful Paint | 1.32 s | **1.2 s** |
| Speed Index | 1.59 s | **1.2 s** |
| Largest Contentful Paint | 2.18 s | 2.2 s |
| Total Blocking Time | 108 ms | **0 ms** |
| Cumulative Layout Shift | 0 | **0** |
| Main-thread Style & Layout | 629 ms | **320 ms** |
| Main-thread total | 2.3 s | **1.3 s** |
| Document bootup | 1.71 s | **0.91 s** |

(Runs: FCP 1.3 / 1.2 / 1.2 s; SI 1.5 / 1.2 / 1.2 s. One cold first-run TBT spike
of 400 ms settled to 0 ms on warm runs.)

**Hebrew (`/he/index.html`)** — 3 runs (very stable):

| Metric | After |
| --- | --- |
| First Contentful Paint | **1.5 s** |
| Speed Index | **1.6 s** |
| Largest Contentful Paint | **2.1 s** (valid — was a latent `NO_LCP`) |
| Total Blocking Time | **0 ms** |
| Cumulative Layout Shift | 0.001 |

Both locales are well under the FCP < 2.5 s target under Lighthouse mobile
simulation.

## Critical request chain — before vs after

Unchanged in structure, because it was already optimal: Lighthouse reports **no
critical request chain** on both builds (the HTML document is the only
render-critical resource; there are no render-blocking stylesheets or synchronous
scripts to chain behind it). The improvement is in main-thread work after the
document arrives, not in the request chain.

## Scripts and fonts requested before FCP

Requested (discovered by the preload scanner) before FCP — none of them block it:

**Scripts** (all Low priority; `async`/`defer`, so non-blocking):
- `pagead2.googlesyndication.com/adsbygoogle.js` — third-party, `async` (consent/ads)
- `assets/…/widget-choreography.js` — `defer`, IntersectionObserver-gated
- `assets/…/lazy-video.js` — `defer`, IntersectionObserver + interaction-gated
- `assets/…/analytics-loader.js` — `defer`, `load` + `requestIdleCallback`-gated
- Inline: `documentElement.classList.add('js')` and the progressive-enhancement
  IIFE (nonessential work now idle-deferred).

**Fonts:**
- `archivo-latin.woff2` — preloaded, High priority, the only font genuinely
  required above the fold (the English headline). `font-display: swap`.
- `plex-mono-600-latin.woff2` — **not** preloaded (decorative monospace only);
  loads after the critical resources with `font-display: swap`.
- No duplicate font requests; no Google Fonts request (self-hosted).
- On `/he/`, the visible headline is Hebrew and renders in a system Hebrew font
  (Segoe UI / Arial Hebrew / Noto Sans Hebrew), so no webfont is on its critical
  path; Archivo covers only the Latin wordmark/numerals.

## No new layout shifts or console errors

- CLS: English 0, Hebrew 0.001 — no regression from `content-visibility`.
- Console: the only message is `adsbygoogle.js` → `ERR_CONNECTION_RESET`, which is
  this sandbox's proxy blocking Google's ad domain; it is not a page defect and
  does not occur on the live origin. No JS errors, no CSP errors, no font errors,
  no image-decode errors.

## Requirement checklist

1. Hero text + imagery in initial HTML — yes (both locales).
2. No wait for JS before hero — yes (pure CSS entrance; visible without JS).
3. Body not hidden for fonts/analytics/consent/animation — yes (no `opacity:0`
   on `body`/hero; `font-display: swap`).
4. Only above-the-fold CSS on the critical path — yes (inline; below-fold layout
   now skipped via `content-visibility`).
5. Defer noncritical styles safely — done via `content-visibility` deferral of
   below-fold rendering (there is no separate stylesheet to split).
6. Remove unused CSS — none actionable was reported; CSS is already minimal.
7. No large/duplicated generated inline style blocks — unchanged; additions are
   a few small rules.
8. Noncritical scripts use defer/async/idle — yes.
9. Consent UI not delayed behind app code — respected (AdSense/FC left in head).
10. Analytics delayed until after critical content — yes (already `load` + idle).
11. Below-the-fold interaction scripts gated to viewport — yes (IntersectionObserver).
12. No premature lazy-video / widget / decorative init — yes.
13. `requestIdleCallback` + timeout fallback for nonessential init — added.
14. No large performance library added — none.
15. Accessibility + progressive enhancement preserved — yes.

## Remaining measurement instability / caveats

- The originally reported FCP ≈ 4.0 s / SI ≈ 5.9 s could not be reproduced in this
  sandbox (local FCP was already ~1.3 s pre-change) because the sandbox blocks the
  live AdSense/Funding Choices execution and has near-zero TTFB. The dominant
  real-world pre-FCP cost is therefore expected to be that third-party execution
  plus real-network TTFB — largely outside the page's own critical path, and left
  in place for consent-compliance reasons. **Re-run Lighthouse against the
  deployed origin to confirm the real-environment FCP/SI after this change.**
- First-run TBT can spike (cold JIT); use the median of several runs.
