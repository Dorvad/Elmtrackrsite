# Elmtrackr performance verification results

Verified 2026-07-17 against a clean fingerprinted `_site/` build.

## Test method and important comparability note

- The production output was rebuilt from scratch, then served from `_site/`
  with a local static HTTP server.
- Lighthouse 13.4.0 ran in Chrome 150. The three mobile runs used a fresh
  browser profile, 412×823 emulation at DPR 1.75, and the supported DevTools
  throttling profile. The desktop run used the Lighthouse desktop preset.
- A separate clean Chrome profile captured a cold visit, a same-profile warm
  reload, responsive-image selection, and the lazy-video activation request.
- An additional unthrottled mobile diagnostic saved a full performance trace
  specifically for forced-reflow attribution.
- Lighthouse's default simulated-throttling path failed after collection with
  `LanternError: NO_LCP` in both Lighthouse 13.4.0 and 12.8.2. The current
  trace's LCP is text, not the former home-screen image, and the Lantern trace
  processor could not build an image-backed LCP graph. The successful
  DevTools-throttled runs below are therefore the final mobile baseline. They
  are not directly interchangeable with the original simulated baseline, so
  this report does not claim a TBT or main-thread improvement from unlike
  throttling methods.

The clean output contains 66 files and 8,240,976 bytes (7.86 MiB) on disk.
That disk total includes both alternative video formats; it is not the initial
page payload. The original 11,471,838-byte master exists only under
`docs/media-source/`, and `docs/` is excluded from `_site/`.

## Lighthouse results

### Mobile, three cold runs

| Result | Score | FCP | LCP | TBT | Speed Index | Main thread | Transfer | CLS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Run 1 | 70 | 1.67 s | 2.72 s | 1.40 s | 2.07 s | 4.45 s | 453.9 KB | 0 |
| Run 2 | 74 | 1.77 s | 2.34 s | 1.15 s | 2.12 s | 4.36 s | 453.7 KB | 0 |
| Run 3 | 71 | 1.66 s | 2.67 s | 1.25 s | 2.05 s | 4.78 s | 453.5 KB | 0.0047 |
| **Median** | **71** | **1.67 s** | **2.67 s** | **1.25 s** | **2.07 s** | **4.45 s** | **453.7 KB** | **0** |

The median throttled main-thread breakdown was 1.67 s style/layout, 833 ms
script evaluation, 337 ms rendering, and 84 ms script parsing/compilation.
Actual CPU throttling turns several whole-document style/layout tasks into long
tasks; Google Ads also contributed repeatable long tasks.

### Desktop and unthrottled diagnostic

| Profile | Score | FCP | LCP | TBT | Speed Index | Main thread | Style/layout | Transfer |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Desktop, cold | 100 | 575 ms | 575 ms | 0 ms | 942 ms | 1.04 s | 192 ms | 448.0 KB |
| Mobile diagnostic, unthrottled | 99 | 1.70 s | 1.89 s | 0 ms | 1.99 s | 885 ms | 250 ms | 452.9 KB |

The desktop CLS was 0.0000025. The unthrottled diagnostic is included because
it preserves direct source attribution in the trace; it is not substituted for
the required three-run mobile median.

## Before and after

The original baseline is the preserved result in `PERFORMANCE_AUDIT.md`. Its
535 KiB network list did not include the unfinished 11.2 MB video transfer, so
the supplied 11.9 MB full-page figure is used for total payload.

| Metric | Before | Final result | Interpretation |
| --- | ---: | ---: | --- |
| Full initial network payload | ~11.9 MB | 453.7 KB median | **96.2% lower**; the final first-party portion was 173.0 KB. |
| Tour video on initial load | 11,471,838 B | 0 B | Neither MP4 nor WebM was requested before activation. |
| Tour video when needed | 11,471,838 B MP4 | 3,081,539 B WebM or 3,546,353 B MP4 | WebM is 73.1% smaller; MP4 is 69.1% smaller. |
| LCP | 6.6 s | 2.67 s median | **59.5% lower**. The final mobile LCP was the hero paragraph, not the image. |
| Total Blocking Time | 310 ms simulated | 1,246 ms DevTools median; 0 ms unthrottled diagnostic | The final median uses a different, actual-throttling method; no like-for-like reduction claim is made. |
| Speed Index | 1.8 s simulated | 2.07 s DevTools median; 1.99 s unthrottled diagnostic | Method-sensitive; the payload and LCP improvements remain directly observable. |
| Main-thread work | 4.2 s baseline trace | 4.45 s DevTools median; 885 ms unthrottled diagnostic | The diagnostic is 79% below the old total, but the throttled median remains dominated by whole-page layout and Google code. |
| Forced reflow | 97.247 ms at generated `index.html:1025` (64 ms in the supplied trace) | No entry in the unthrottled trace; at most 2.905 ms attributed to first-party code in one throttled run | The old perpetual measurement loop is removed; the remaining first-party attribution is over 95% smaller. |

## Video verification

- Production encodes are 720×1280 at 24 fps, down from the 1080×1920,
  30 fps master. The MP4 is H.264 High Profile/AAC with CRF 26 and fast-start
  metadata; the WebM is VP9/Opus.
- The clean build contains only `assets/elmtrackr-tour.mp4` (3,546,353 bytes)
  and `assets/elmtrackr-tour.webm` (3,081,539 bytes). No file named as an
  original/source master is present in `_site/`.
- On cold and warm initial loads, the video had `preload="none"`, an empty
  `currentSrc`, ready state 0, and two `<source>` elements whose `src`
  attributes were still absent.
- Approaching `#film` attached both compatible choices exactly once. Chrome
  selected and requested only the WebM (3,081,731 transferred bytes including
  response overhead). The interactive browser test reached ready state 4 and
  played from 0 to 6.98 seconds while muted. MP4 was not downloaded in that
  browser.
- The 720×1280 WebP poster is 4,648 bytes and is the only film image requested
  initially. Captions, controls, transcript, aspect ratio, and the no-script
  download fallback remain present.

## LCP image verification

| Candidate | Dimensions | File size |
| --- | ---: | ---: |
| `elmtrackr-home-screen-360.webp` | 360×800 | 16,648 B |
| `elmtrackr-home-screen-480.webp` | 480×1067 | 22,774 B |
| `elmtrackr-home-screen.webp` | 720×1600 | 35,250 B |
| JPEG fallback | 720×1600 | 62,485 B |

- The actual `<img>` has `fetchpriority="high"`, `decoding="async"`, no
  `loading` attribute, meaningful alt text, and intrinsic `width="720"` and
  `height="1600"` values.
- The `<picture>` WebP source has the fingerprinted 360/480/720 `srcset` and
  `sizes="274px"`. The image's CSS layout width is 274 px; the larger rotated
  bounding box comes from its parent composition and does not change the
  source-size calculation.
- Every mobile Lighthouse run and the fresh DPR-1.75 browser selected exactly
  one 480 px candidate. The desktop Lighthouse run at DPR 1 selected the 360
  px candidate. No JPEG fallback or duplicate image candidate was requested.
- Lighthouse's final image-delivery audit reported zero wasted bytes. The LCP
  itself moved to the hero paragraph under the final mobile profile.

## Fonts

The homepage made two font requests on first load:

| Final production font | Size | Homepage request |
| --- | ---: | --- |
| `archivo-latin.8f704806dbed.woff2` | 34,928 B | Yes; the only preloaded font. |
| `plex-mono-500-latin.01d285447409.woff2` | 14,888 B | No; used by content-page figure captions. |
| `plex-mono-600-latin.0d1f0b8d0722.woff2` | 15,620 B | Yes; discovered from CSS, not preloaded. |

No Cyrillic, Latin Extended, Vietnamese, italic, or unused weight file is in
the production build. All self-hosted declarations use `font-display: swap`
and explicit Latin ranges. English rendered with Archivo/Plex; Hebrew rendered
correctly through the declared Segoe UI / Arial Hebrew / Noto Sans Hebrew
system fallbacks. English and Hebrew browser checks had no missing-glyph or
font console errors.

## Cold and warm first-load assets

The fresh-browser CDP trace transferred 449,796 bytes across 24 completed
requests. Its 173,026-byte first-party list was:

| First-party resource | Transfer |
| --- | ---: |
| HTML document | 80,370 B |
| Home-screen 480 WebP | 22,978 B |
| Tour poster WebP | 4,851 B |
| Logo SVG | 763 B |
| Google Play SVG | 783 B |
| Discord SVG | 1,669 B |
| Widget choreography JS | 5,295 B |
| Archivo Latin font | 35,132 B |
| Lazy-video JS | 1,874 B |
| Deferred analytics loader | 1,767 B |
| English caption VTT | 1,720 B |
| Plex Mono 600 Latin font | 15,824 B |
| Cached duplicate logo lookup | 0 B |

The remainder was Google Ads/DoubleClick/traffic-quality code and frames. The
same-profile warm reload transferred 13,481 bytes total and only 105 bytes
first-party (HTML revalidation); all fingerprinted first-party resource timing
entries had zero transfer size.

Production pages reference the content-hashed `/assets/fp/` filenames and
`asset-manifest.json` maps their source names. HTML, video, captions, and stable
metadata/download URLs are intentionally not immutable or fingerprinted.

## Third-party, consent, and analytics findings

- Each advertising homepage contains one asynchronous `adsbygoogle.js` tag
  with the existing publisher ID. Browser and Lighthouse traces saw that one
  loader and one Google-injected `show_ads_impl` implementation request; there
  is no duplicate authored initialization or manual ad-slot request.
- Auto Ads generated the DoubleClick and traffic-quality requests. Those
  scripts account for most remaining transfer, script evaluation, unused JS,
  third-party-cookie, and DevTools Issues warnings. They cannot be edited or
  delayed independently without changing Auto Ads/consent behavior.
- No Funding Choices request appeared in this geography/session. Its regional
  behavior depends on AdSense Privacy & Messaging configuration and must be
  verified in the publisher account and regulated regions after deployment.
- The 1,573-byte fingerprinted analytics loader was requested after the page
  lifecycle boundary. The 7,910-byte `analytics.js` runtime was not requested
  because no provider is configured, so it did not block the critical path.
- Lighthouse best practices scored 77 solely with the current Google
  third-party cookie and Issues-panel findings. No advertising, consent, or
  first-party console error was recorded.

## Reflow, scrolling, resizing, and visual behavior

The original forced reflow came from the generated homepage's perpetual
widget animation loop, which measured `getBoundingClientRect()` every frame
and then mutated styles. The source is now
`assets/widget-choreography.js`: an `IntersectionObserver` activates the work
near the widget section, geometry is cached, invalidated only when needed, DOM
reads precede transform/opacity writes, scroll listeners are passive, and one
animation frame is queued at a time. Phone/watch floating motion also uses
transforms instead of margins.

The final unthrottled trace contains no forced-reflow item. In the three
CPU-throttled traces, two had no first-party source attribution and one
attributed 2.905 ms to the load/font invalidation path. Google Ads contributed
0.6–2.7 ms in two runs. The traces also contain about 410–511 ms marked only as
`[unattributed]`; because it has no script/source location and disappears in
the unthrottled trace, it is documented rather than assigned speculatively to
site code.

Smooth navigation to the film section, widget choreography, video playback,
mobile-to-desktop resize, and top/bottom scrolling completed without console
errors. Mobile 412 px, in-app desktop 1280 px, CDP desktop 1440 px, and
Lighthouse desktop widths had no horizontal overflow.

## Accessibility, SEO, language, and links

- Lighthouse: accessibility 94, best practices 77, SEO 100.
- Repository validators passed for 28 generated content pages, 30 sitemap
  URLs, canonical URLs, metadata, JSON-LD, hreflang reciprocity, locale
  switches, internal links, image alt/dimensions, video captions/transcripts,
  static HTML, ads/analytics constraints, and motion constraints.
- English uses `lang="en"`; Hebrew uses `lang="he" dir="rtl"`. Both were
  visually checked and produced no browser console warnings/errors.
- The accessibility deductions are pre-existing in `HEAD`: low-contrast
  decorative/footer text and two Play-link accessible-name/visible-label
  mismatches. No performance change introduced them, and colors were not
  altered because this task explicitly preserves the visual design.
- The only SEO validator warnings are four pre-existing English guide meta
  descriptions longer than the recommended range and the intentionally
  unverified public Play-listing flag. Canonicals, structured data, language
  handling, and internal routes pass.

## Hosting work still required

GitHub Pages remains the deployment target. It does not support arbitrary
repository-defined response headers and currently serves first-party assets
with a roughly ten-minute cache lifetime. A `<meta>` element and a `_headers`
file cannot fix that on GitHub Pages.

The repository-side part is complete: cacheable JS, CSS, fonts, and images use
content hashes, while HTML is not marked immutable. To obtain
`Cache-Control: public, max-age=31536000, immutable` for `/assets/fp/*` and
revalidation for HTML, the owner must either proxy the existing Pages site
through Cloudflare or migrate `_site/` to Cloudflare Pages. Exact rules and a
ready `_headers` example are in `CACHE_DEPLOYMENT_OPTIONS.md`.

## Deployment verification checklist

- [ ] Deploy the clean `_site/` artifact; confirm `docs/`, `_reports/`, and the
      original 11.47 MB master are absent.
- [ ] In a fresh mobile browser, confirm the first load requests one responsive
      home-screen candidate and no `.mp4`/`.webm`.
- [ ] Scroll to `#film`; confirm one format loads, plays, captions work, and no
      second video format is requested.
- [ ] Repeat the visit and confirm fingerprinted resources are served from
      memory/disk cache or revalidate with zero body transfer.
- [ ] Check English and Hebrew at 360/390/412 px and at 1280/1440 px; confirm
      no horizontal overflow, layout shift, missing glyph, or animation issue.
- [ ] Confirm one AdSense loader, then use AdSense Privacy & Messaging preview
      plus clean sessions in every regulated region to verify consent.
- [ ] Run three production Lighthouse mobile audits and use the median; record
      any Google-controlled unused-JS/cookie warnings without brittle code
      changes.
- [ ] Verify homepage/hashed-asset response headers. Apply the Cloudflare rule
      from `CACHE_DEPLOYMENT_OPTIONS.md` if one-year immutable caching is
      required.
- [ ] Re-run the repository validators and verify canonical URLs, hreflang,
      JSON-LD, sitemap, internal links, and the public Play listing.
