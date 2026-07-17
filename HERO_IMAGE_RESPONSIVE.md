# Hero Image — Responsive Delivery

Internal engineering note. Excluded from the published site (see `Makefile` →
`INTERNAL`).

## Layout measurement (the basis for `sizes`)

The hero phone image (`img[alt*="home screen"]`) sits inside a **fixed-size**
phone mockup: `width: 296px` with `padding: 11px` (`box-sizing: border-box`), so
the screen content box — and therefore the image's CSS layout width — is
`296 − 22 = 274px`. This mockup is **not** scaled by any media query; measured
across viewports from 320px to 1920px the image's layout width is constant.
(`getBoundingClientRect()` reports ~307px because the phone is rotated in 3-D via
`transform`, but the browser uses the untransformed 274px layout width for
`srcset` selection — confirmed: at DPR 1.75 it selects the 480w candidate, i.e.
274 × 1.75 = 480.)

Because the rendered width is a single constant, the correct, CSS-derived value is:

```
sizes="274px"
```

This is intentionally not a generic `100vw`-style value; it is the real rendered
width at every breakpoint.

## Variants generated

Regenerated as a uniform WebP ladder (Pillow, quality 82, downscaled from the
720×1600 source with Lanczos), plus the existing JPEG fallback:

| File | Dimensions | Size |
| --- | --- | --- |
| `elmtrackr-home-screen-300.webp` | 300 × 667 | 12.8 KB |
| `elmtrackr-home-screen-360.webp` | 360 × 800 | 16.4 KB |
| `elmtrackr-home-screen-480.webp` | 480 × 1067 | 22.5 KB |
| `elmtrackr-home-screen-560.webp` | 560 × 1244 | 26.4 KB |
| `elmtrackr-home-screen.webp` (720) | 720 × 1600 | 35.3 KB |
| `elmtrackr-home-screen.jpg` (fallback) | 720 × 1600 | 62.5 KB |

`-300` and `-560` are new; they close the two real gaps in the ladder:
- **DPR 1** needs 274px → previously picked 360w (oversized); now picks **300w**.
- **DPR 2** needs 548px → previously picked 720w (oversized); now picks **560w**.

The build fingerprints all of them automatically (`assets/fp/…`) and rewrites the
`srcset`; `check_media.py` confirms every candidate exists with valid dimensions.

### AVIF — evaluated, not adopted
Pillow can encode AVIF, but for this flat-UI screenshot the saving over WebP is
only ~9–14% (e.g. 480w: 22.5 KB WebP vs 18.3 KB AVIF ≈ 2.8 KB), and the build
pipeline (`fingerprint_assets.py`, `check_media.py`) does not natively recognise
`.avif`. Per the requirement ("add AVIF only if the build supports it reliably
**and** it produces a meaningful saving"), AVIF was **not** added. It remains an
optional future enhancement if the build is extended to fingerprint `.avif`.

## Markup (both `index.html` and `he/index.html`)

```html
<picture>
  <source type="image/webp" srcset="
    …-300.webp 300w, …-360.webp 360w, …-480.webp 480w,
    …-560.webp 560w, …home-screen.webp 720w" sizes="274px">
  <img src="…home-screen.jpg" width="720" height="1600"
       decoding="async" fetchpriority="high" alt="…"
       style="…object-fit:cover;object-position:center;…">
</picture>
```

Preserved unchanged: WebP, the JPEG fallback `src`, `fetchpriority="high"`,
`decoding="async"`, the alt text, the intrinsic `width`/`height` (720×1600, which
matches the fallback file), and the `object-fit`/`object-position` composition.
No `loading="lazy"`. No `<link rel=preload>` exists for this image, so there is no
preload/`srcset` mismatch.

## Selected candidate per tested viewport (headless Network capture)

| Viewport | DPR | Need (274×DPR) | Selected | Requests |
| --- | --- | --- | --- | --- |
| narrow mobile 360×780 | 2 | 548 | **560w** | 1 |
| narrow mobile 360×780 | 3 | 822 | **720w** | 1 |
| Lighthouse mobile 412×823 | 1.75 | 480 | **480w** | 1 |
| large mobile 430×932 | 3 | 822 | **720w** | 1 |
| tablet 768×1024 | 2 | 548 | **560w** | 1 |
| desktop 1440×900 | 1 | 274 | **300w** | 1 |
| desktop 1440×900 | 2 | 548 | **560w** | 1 |

Exactly **one** home-screen candidate is downloaded in every case — no duplicate
request, and never both a WebP and the JPEG.

## Reported items

1. **Variants + sizes:** see the table above (5 WebP widths + JPEG fallback).
2. **Selected candidate per viewport:** see the table above.
3. **Does Lighthouse still report image-delivery savings?** No — in local mobile
   runs the `uses-responsive-images` and `uses-optimized-images` audits report no
   items. The original ~15 KB figure reflected the caller's environment (the
   savings depend on how that run accounted for device-pixel-ratio); the ladder
   now serves a right-sized candidate at DPR 1, 1.75, 2 and 3.
4. **Is the image still a valid LCP element?** Yes. On desktop / side-by-side
   layouts the phone image is the measured LCP (≈204,474 px²), served by the
   correct candidate (300w at DPR 1, 560w at DPR 2). On the narrow, stacked
   mobile layout the hero **paragraph** is the largest in-viewport element and is
   the LCP there; the image remains a valid candidate (opaque, `fetchpriority`
   high, present in the initial HTML). LCP timing is unchanged (2.1–2.2 s under
   mobile simulation).
5. **Duplicate image request?** None — one candidate per load in all viewports.

Lighthouse mobile ×3 after the change: FCP 1.2 s, LCP 2.1–2.2 s, TBT 0 ms,
Speed Index 1.2 s, CLS 0.
