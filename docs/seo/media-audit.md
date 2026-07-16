# Elmtrackr — Media Audit (images & product film)

**Date reviewed:** 2026-07-16
**Scope:** every image and the product film shipped from `assets/`.

Verified media facts and per-asset classification. Validated by
`scripts/check_media.py`.

## Product film — `assets/elmtrackr-tour.mp4`

| Fact | Value | How verified |
|---|---|---|
| Container / video codec | MP4 / H.264 (Constrained Baseline) | MP4 atom parse + ffmpeg probe |
| Audio | AAC-LC, 44.1 kHz, stereo (present) | ffmpeg probe |
| Resolution | 1080 × 1920 (portrait 9:16) | ffmpeg probe |
| Frame rate | 30 fps | ffmpeg probe |
| Duration | 64.67 s (≈ 1:05, `PT1M5S`) | `mvhd` timescale/duration |
| Embedded creation date | none (0) | `mvhd` |

**Content (from decoded frames):** a silent-by-default screen recording that
walks through the app — intro calendar, a taxi receipt, a "last week" teaser,
the home dashboard, the shift list (active shift, breaks, overtime/weekend
tags), receipt capture, the reports screen with CSV/PDF export and travel
refunds, a clock-out timer, a monthly gross summary, and the closing logo. All
on-screen figures are in-app sample values.

**Accessibility implemented:** descriptive heading + summary; native
`controls` (keyboard-accessible play/pause/mute/captions/fullscreen); `<track
kind="captions">` in English (`/he/` in Hebrew); a full visible transcript in
each language; `preload="metadata"`; **no autoplay** (so no sound without a
user action and reduced-motion is respected by default); poster
`elmtrackr-app-tour-poster.jpg`; `<source>` + a visible MP4 fallback link;
`VideoObject` JSON-LD on both homepages (name, description, thumbnailUrl,
contentUrl, duration `PT1M5S`, uploadDate, inLanguage, width, height).

**Documented gap (not invented):** the file carries an audio track, but its
audio content cannot be verified here (no narration is visible and audio can't
be listened to in this environment). The transcript and captions therefore
describe the **on-screen** content — the meaningful information in this
screencast — and explicitly note the background audio is not transcribed. The
embedded upload date is absent, so `uploadDate` uses the site publication date
(2026-07-16).

## Images

| File | Class | Dims | Public use | Alt / handling |
|---|---|---|---|---|
| `elmtrackr-home-screen.jpg` (+`.webp`) | Product screenshot | 720×1600 | Homepage hero; hourly-pay & shift-tracker guides/pages | Descriptive alt; `width/height`; hero is eager, figures lazy; `decoding=async`; WebP via `<picture>` |
| `render-widgets-tablet.jpg` (+`.webp`) | Product screenshot | 1400×933 | Shift-tracker page figure; default OG image | Descriptive alt; dims; lazy; WebP |
| `render-watch-live.jpg` (+`.webp`) | Product screenshot | 1100×1100 | Wear OS page figure | Descriptive alt; dims; lazy; WebP |
| `render-watch-glance.jpg` (+`.webp`) | Product screenshot | 1100×1100 | (available; not currently placed) | Descriptive alt when used |
| `elmtrackr-app-tour-poster.jpg` (+`.webp`) | Video poster | 720×1280 | Film `poster=` | Poster (no `alt`); video has `aria-label`/described-by; descriptive filename |
| `icon-192.png` | Logo / favicon / OG logo | 192×192 | Favicon, apple-touch, Organization logo | n/a (icon) |
| `logo-mark.svg` | Logo (decorative in headers) | 26/20 px | Header/footer brand mark | `alt=""` (wordmark text carries the name) |
| `google-play.svg` | Decorative icon | 18–20 px | Inside "Get it on Google Play" buttons | `alt=""` (link text carries the label) |
| `discord.svg` | Decorative icon | 13–17 px | Discord link | `alt=""` (link text carries the label) |
| `uploads/*.png`, `uploads/IMG-*.jpg` | Source uploads, **not used publicly** | various | none (not referenced by any shipped page) | Left as-is; excluded from the published set is not required as nothing links them, but they should not be linked publicly |

### Social (Open Graph) images

- **Homepage (en/he):** `render-widgets-tablet.jpg` (1400×933) with width/height/alt.
- **Product pages & guides hub:** the same product screenshot as the default OG
  (`render-widgets-tablet.jpg`) via the content-page builder — a real product
  asset, landscape, with dimensions and alt. No generic/AI artwork is used.

### Performance

- Modern **WebP** derivatives generated for the meaningful raster images
  (roughly 45–80% smaller) and served via `<picture>` with the JPG as
  fallback, so GitHub Pages paths never break. Originals preserved.
- Hero screenshot is eagerly available (no `loading=lazy`); below-the-fold
  figures are `loading="lazy"` with `decoding="async"`.
- No image is upscaled; display sizes are at or below native dimensions.
- Largest shipped raster is ~150 KB; the 11 MB MP4 uses `preload="metadata"`
  and never autoplays.
