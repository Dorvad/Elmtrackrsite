# LCP Diagnosis — Home Page (`index.html`)

Investigation of the `NO_LCP` result reported by Lighthouse on the Elmtrackr
home page, and the correction applied. This is an internal engineering note; it
is excluded from the published site (see `Makefile` → `INTERNAL`).

## Summary

Lighthouse reported `Largest Contentful Paint: Error — NO_LCP` (and, as a
consequence, `Total Blocking Time: NO_LCP`) even though the page renders
complete, visible hero content. The cause was **not** an asset-size problem and
not a slow image. It was a *measurement* problem: every large element in the
hero began its entrance animation from `opacity: 0`, and Chrome's LCP algorithm
excludes any element first painted while animating opacity up from zero. With no
eligible candidate, Chrome emitted no LCP entry at all, so the trace contained
no LCP node and Lighthouse's trace engine failed with `NO_LCP`.

The fix keeps the exact same visual entrance (rise + 3-D settle) but drives it
with `transform` only, so the hero text and phone image stay fully opaque and
remain valid LCP candidates. No redesign; appearance and content are unchanged.

## 1. Expected LCP element

In the initial mobile viewport the largest contentful element is the hero
paragraph:

```html
<p style="…font:500 19px/1.55 'Archivo',sans-serif;color:rgba(24,21,48,.62);…">
  Clock in from your phone or watch. Elmtrackr tracks your hours … not an official record.
</p>
```

Measured paint size ≈ **59,640 px²** at ≈ 150–170 ms. Depending on viewport the
`<h1>` ("Every shift, measured") or the hero phone image
(`assets/elmtrackr-home-screen*.webp/.jpg`) are the next-largest candidates; on
wider (desktop) viewports the phone image was historically the LCP element. All
three sit inside the initial HTML and are visible without JavaScript.

## 2. Why Lighthouse produced `NO_LCP`

Confirmed empirically (not inferred) — see §5 for the measurement harness.

- A `PerformanceObserver` for `largest-contentful-paint` (`buffered: true`),
  installed before any page script, recorded **zero entries** after 6 s, even
  though all hero elements were fully painted and opaque by then. The observer
  itself registered without error.
- Lighthouse's trace engine threw `LanternError: NO_LCP` on **3 of 3** runs
  because the collected trace contained no `largestContentfulPaint::Candidate`
  node.

Root cause: every sizeable hero element animated its opacity from `0`:

| Element | Inline animation | Keyframe start |
| --- | --- | --- |
| `<h1>` hero headline | `animation: riseIn …` | `riseIn` `from { opacity: 0 }` |
| `<p>` hero paragraph (expected LCP) | `animation: riseIn …` | `riseIn` `from { opacity: 0 }` |
| Phone container (historical LCP) | `animation: settlePhone …` | `settlePhone` `0% { opacity: 0 }` |

Chrome deliberately **does not report an element as an LCP candidate if its first
paint occurs while it is animating opacity up from 0** (a guard against
fade-in tricks that would otherwise game the metric). Because *every* large
element in the hero started at `opacity: 0`, Chrome never registered any
candidate → no LCP entry → `NO_LCP` in the trace engine.

Controlled proof: re-running the page with **only** the opacity-from-0 hero
animations neutralized (nothing else changed — the infinite float animations and
all scripts still ran) made a valid LCP entry appear immediately:

```
=== CONTROLLED (opacity animations neutralized) LCP ENTRIES ===
[ { "time": 168, "size": 59640, "tag": "P", … } ]
```

This isolates the opacity-from-0 entrance as the sole cause. The infinite
`floatPhone`/`floatWatch`/`tickPulse` animations, the AdSense request, fonts,
image decoding, CSP, redirects and hydration were all ruled out (see §6).

## 3. Source files involved

- `index.html`
  - `@keyframes settlePhone` (inline `<style>`) — began `0% { opacity: 0 }`.
  - `@keyframes riseIn` (inline `<style>`) — `from { opacity: 0 }`; used by the
    hero `<h1>` and `<p>` (and, separately, by below-the-fold scroll reveals).
  - Hero `<h1>` and `<p>` `style="…animation: riseIn …"`.
  - Phone image markup: a single `<picture><img …fetchpriority="high"></picture>`
    inside the `settlePhone` container.

## 4. Implemented correction

Surgical, CSS-only; no markup, content, or layout changes.

1. **`settlePhone` is now transform-only.** Removed `opacity: 0` (0%) and
   `opacity: 1` (100%) from the keyframe. The phone still translates and rotates
   into place, but is opaque throughout — so it is a valid LCP candidate and is
   visible even if the animation never runs.
2. **New `heroRise` keyframe (transform-only)** —
   `@keyframes heroRise { from { transform: translateY(26px) } to { transform: translateY(0) } }`
   — applied to the hero `<h1>` and `<p>` in place of `riseIn`. Same rise motion,
   no opacity fade. The `riseIn` keyframe is left untouched so below-the-fold
   scroll-reveal animations keep their existing fade.

Why this satisfies the constraints:

- **Hero visible by default** — the LCP text/image are opaque from first paint.
- **Progressive enhancement** — the entrance is pure CSS; if scripts fail the
  hero is still complete and visible (unchanged from before — it was never
  JS-gated).
- **LCP element not faded from zero opacity** — `heroRise`/`settlePhone` never
  touch opacity.
- **Decorative elements still animate separately** — the watch (`settleWatch`),
  ribbon draw, and infinite float/tick animations are unchanged.
- **`prefers-reduced-motion` respected** — the existing
  `@media (prefers-reduced-motion: reduce)` rule still collapses all animation
  durations to ~0.
- **Stable image node** — the hero phone is a single static `<img>` in a
  `<picture>`; it is never swapped or recreated (no framework/hydration here), so
  the "one stable image DOM node" requirement already held and is preserved.

No arbitrary delays, fake LCP elements, or hidden text were added.

## 5. Post-fix Lighthouse results (mobile, clean production build)

Environment: Chromium 141, Lighthouse mobile profile (`simulate` throttling),
served from the actual `make dist` output (`_site/`), fresh browser context per
run.

| Run | FCP | LCP | TBT | Speed Index | CLS | Perf score |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1.2 s | **2.2 s** | **0 ms** | 1.3 s | 0 | 0.99 |
| 2 | 1.3 s | **2.1 s** | **10 ms** | 1.4 s | 0 | 0.99 |
| 3 | 1.2 s | **2.2 s** | **160 ms** | 1.4 s | 0 | 0.97 |

`largest-contentful-paint` and `total-blocking-time` now return real numeric
values on every run. The trace-engine `NO_LCP` error count dropped from **3/3
(pre-fix) to 0/3 (post-fix)**. `PerformanceObserver` now reports the hero `<p>`
as the LCP candidate (~150–170 ms; the emulated LCP time is later once network
throttling is applied).

### Development-only instrumentation (added during diagnosis, removed from prod)

The following was inserted early in `<head>`, guarded to `localhost`/`127.0.0.1`
so it is inert in production, used to confirm candidate emission, then **removed**
from `index.html` (verified absent from `_site/`). Kept here for reproducibility:

```html
<script>
(function(){
  var h = location.hostname;
  if (h !== 'localhost' && h !== '127.0.0.1') return; // inert in production
  try {
    new PerformanceObserver(function(list){
      list.getEntries().forEach(function(e){
        console.log('[LCP-CANDIDATE]', Math.round(e.startTime) + 'ms', 'size=' + e.size,
          e.element ? e.element.tagName : '(no element)', e.url || '');
      });
    }).observe({ type: 'largest-contentful-paint', buffered: true });
  } catch (err) { console.warn('[LCP-CANDIDATE] observer unavailable', err); }
})();
</script>
```

Observed on localhost after the fix: `[LCP-CANDIDATE] 152ms size=59640 P`.

## 6. Checks performed and ruled out

- **JavaScript errors / page errors:** none.
- **Failed network requests:** only `pagead2.googlesyndication.com/adsbygoogle.js`
  → `ERR_CONNECTION_RESET`. This is the sandbox proxy blocking Google AdSense; it
  is loaded `async` and is unrelated to LCP (LCP stayed `NO_LCP` regardless, and
  the controlled test restored LCP with AdSense still blocked).
- **CSP errors:** none.
- **Font errors:** none — self-hosted Archivo + IBM Plex Mono (`font-display: swap`).
- **Image decoding errors:** none — hero `<img>` `complete`, `naturalWidth > 0`.
- **AdSense / consent overlays:** no overlay covers the hero; no consent gate.
- **Redirect / reload / route transition:** none — static page, single navigation.
- **Long-running animation / DOM mutation:** the hero has infinite
  `floatPhone`/`floatWatch`/`tickPulse` animations and a per-second clock/counter
  update. These are `transform`-only (compositor) / cheap text updates; they did
  **not** prevent LCP (proven by the controlled test) and TBT remained low
  (0–160 ms). They are expected, existing behaviour and were left unchanged.

## Remaining measurement instability

- **TBT variance:** TBT ranged 0–160 ms across runs — normal single-run
  Lighthouse jitter on this hardware, well within budget. Averaging several runs
  is recommended for trend tracking.
- **Absolute FCP/Speed Index differ from the originally reported numbers**
  (FCP ≈ 4.0 s, SI ≈ 5.9 s). Those depend on the measuring environment
  (CPU/network throttling, live AdSense/analytics on the deployed origin). This
  sandbox is faster and blocks AdSense, so it shows lower absolutes. The
  `NO_LCP` failure, however, reproduced exactly (3/3) and is now resolved (0/3),
  which was the object of this investigation.
- **`largestContentfulPaint::Candidate` in raw Puppeteer traces:** the manual
  `page.tracing` capture did not surface the LCP candidate event (a category
  limitation of that path). The authoritative signals used here are the
  `PerformanceObserver` Web-Vitals entry and Lighthouse's own trace-engine
  result, which agree.
