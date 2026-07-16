# Elmtrackr — Manual QA matrix

**Date reviewed:** 2026-07-16

The automated gate (`make ci`) covers metadata, structured data, links, images,
locales and accessibility *structure*. This matrix covers what a machine can't
fully judge: real rendering, input modalities and human-perceived behavior. Run
it against the assembled site (`make dist && make serve`, then browse
`http://localhost:8000/`) before a release, and after any change to layout, the
video, the header/footer, or the language switch.

Mark each cell **Pass / Fail / N/A** and attach a note on any Fail.

## 1. Viewports & rendering

Representative pages to check at each width: English home `/`, Hebrew home
`/he/`, a product page `/shift-tracker-android/`, a guide
`/guides/how-to-track-work-hours/`, and the privacy/security page.

| Check | 320 px | 375 px | Tablet portrait | Tablet landscape | Desktop |
|---|---|---|---|---|---|
| No horizontal scroll / overflow | | | | | |
| Header + language switch usable | | | | | |
| Hero / H1 readable, not clipped | | | | | |
| Images scale, no layout shift on load | | | | | |
| Video block fits, controls reachable | | | | | |
| Footer nav wraps cleanly | | | | | |
| Hebrew pages mirror correctly (RTL) | | | | | |

## 2. System preferences

| Check | Light | Dark |
|---|---|---|
| Colours/contrast acceptable, no invisible text | | |
| `theme-color` matches (light `#FBFAFE`, dark `#0E0C1F`) | | |
| 404 page respects the preference | | |

- **Reduced motion** (`prefers-reduced-motion: reduce`): the homepage's ticking
  clock, pay counter, ring animations and film auto-behaviour must not induce
  motion; nothing should autoplay aggressively. Verify the page is fully usable
  and readable with motion reduced.

## 3. Input modalities

| Check | Result |
|---|---|
| **Keyboard only:** Tab reaches every link/CTA/FAQ/video control in a sensible order | |
| Visible focus ring on every focusable element | |
| Skip link ("skip to content") appears on first Tab and works | |
| `Enter`/`Space` activate CTAs and open FAQ items | |
| FAQ `<details>` toggle open/close via keyboard | |
| Video controls operable via keyboard | |
| **Screen reader:** heading order is logical (one H1, then H2/H3) | |
| Screen-reader link list is meaningful (no "click here"/empty links) | |
| Images have sensible alt text; decorative images are silent (`alt=""`) | |
| Language of Hebrew pages announced as Hebrew (`lang="he"`) | |
| Data-flow figure on privacy/security page has a text equivalent | |

## 4. Progressive enhancement / resilience

| Check | Result |
|---|---|
| **JavaScript disabled:** every page still renders complete, readable content | |
| With JS off, all links/CTAs still navigate; FAQ still readable | |
| With JS off, video shows native controls (no blank box) | |
| **External CDN unavailable / AdSense blocked:** page still renders fully (only the homepage ad slot is affected; fonts are self-hosted, so text is unaffected) | |
| No uncaught JS errors in console on any page (analytics helper no-ops when no provider) | |

## 5. Bilingual routing & language switch

Language-switch controls carry `data-elm-event="language_switch"`.

| From | Switch goes to | Back-link returns to | Result |
|---|---|---|---|
| `/` | `/he/` | `/` | |
| `/shift-tracker-android/` | `/he/shift-tracker-android/` | `/shift-tracker-android/` | |
| `/hourly-pay-tracker/` | `/he/hourly-pay-tracker/` | … | |
| `/overtime-pay-tracker/` | `/he/overtime-pay-tracker/` | … | |
| `/wear-os-shift-tracker/` | `/he/wear-os-shift-tracker/` | … | |
| `/receipt-expense-tracker/` | `/he/receipt-expense-tracker/` | … | |
| `/work-hours-reports/` | `/he/work-hours-reports/` | … | |
| `/task-time-tracking/` | `/he/task-time-tracking/` | … | |
| `/privacy-and-security/` | `/he/privacy-and-security/` | … | |
| `/delete-account/` | `/he/delete-account/` | … | |
| `/guides/` | `/he/guides/` | … | |
| each of the 4 guides | its `/he/guides/…` pair | … | |

(`check_locales.py` proves the pairs exist and are reciprocal; this row set is
to confirm the on-page switch actually lands on the right page in the browser.)

## 6. Call-to-action inventory

| CTA | Where | Expected behavior |
|---|---|---|
| "Get it on Google Play" — hero | home hero | opens the verified Play listing (`id=com.elmlaunch.myapp`), `utm_content=hero` |
| "Get it on Google Play" — price | home price block | same listing, `utm_content=price` |
| "Get the app" — header | every content page header | same listing, `utm_content=header` |
| Article CTA | each product / guide page body | same listing, `utm_content=article` |
| WhatsApp link | home | opens WhatsApp (external) |
| Discord link | home | opens Discord (external) |
| Language switch | header / home | swaps locale (section 5) |
| Footer legal links | all footers | Privacy, Terms, Privacy & security, Delete account resolve |

For each: **left-click navigates**, **middle-click opens a new tab**, and
**keyboard `Enter` navigates** — and none is blocked by the analytics layer.

## 7. Media

| Check | Result |
|---|---|
| Homepage film: play/pause/seek/volume/fullscreen all work | |
| Captions track selectable; captions display | |
| Visible transcript present and matches | |
| Poster image shows before play; no CLS when video loads | |
| Hebrew homepage film behaves identically | |

## 8. FAQ controls

| Check | Result |
|---|---|
| Every product/guide page FAQ opens/closes on click and keyboard | |
| Only one open at a time is **not** required — independent toggles OK | |
| Visible questions match the FAQ rich-result schema (also enforced by audit) | |

## 9. Error page

| Check | Result |
|---|---|
| Visiting a non-existent path (e.g. `/does-not-exist/`) serves `/404.html` | |
| 404 page has working links back to Home, Guides, product, privacy | |
| 404 page is `noindex` and not in the sitemap | |

## 10. Cross-browser spot check

Repeat sections 1, 3 and 7 on at least: latest Chrome, latest Firefox, latest
Safari (desktop + iOS), and Chrome on Android.

---

### Notes on scope

- This matrix is **manual** by design — it verifies perceived behavior, not code.
  The deterministic checks live in `make ci`.
- Do not "fix" a Lighthouse performance number by removing captions, transcripts,
  alt text, the film, or focus styles. Accessibility and media are features.
