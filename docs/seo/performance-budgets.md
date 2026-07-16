# Elmtrackr — Performance & Lighthouse budgets

**Config:** `.lighthouserc.json` · **Resource budgets:** `lighthouse-budgets.json`

Lighthouse CI is **optional** — it runs in `.github/workflows/ci.yml` only when the
runner can install it, and never blocks the core audit gate. The core gate
(`make ci`) does not depend on Chrome/Lighthouse being present.

## Representative pages tested

| Page | URL |
|---|---|
| English homepage | `/` |
| Hebrew homepage | `/he/` |
| English product page | `/shift-tracker-android/` |
| Hebrew product page | `/he/shift-tracker-android/` |
| Guide | `/guides/how-to-track-work-hours/` |
| Privacy / security | `/privacy-and-security/` |

## Budgets

| Dimension | Budget | Severity | Notes |
|---|---|---|---|
| Performance | ≥ 0.85 | warn | Warn, not error: the homepage carries a product film and large marketing renders on purpose. We do not want CI to pressure anyone into deleting useful media to chase a number. |
| Accessibility | ≥ 0.95 | error | Hard gate. A11y regressions must fail. |
| SEO | ≥ 0.95 | error | Hard gate. |
| Best practices | ≥ 0.90 | warn | AdSense on the homepage can affect this; kept a warn so a third-party choice doesn't fail the build. |
| Layout shift (CLS) | ≤ 0.10 | error | Every content image ships explicit `width`/`height`; regressions fail. |
| JavaScript errors | 0 | warn | `errors-in-console`. Warn (not error) because Lighthouse in an offline CI runner reports failed loads of external scripts (AdSense) as console errors that are not real defects. |
| Total transfer size | ≤ ~1.2 MB | warn | `resource-summary:total:size`. |
| Largest image / image weight | ≤ ~800 KB total images | warn | `resource-summary:image:size`, plus `image-size-responsive`. WebP `<picture>` derivatives keep individual images small. |
| Script weight | ≤ ~120 KB | warn | First-party JS is tiny (inline enhancer + `analytics.js`). |

## Why the a11y / SEO gates are hard and performance is soft

The instruction was explicit: **do not achieve scores by removing useful
accessibility or media features.** So the two dimensions we never want to
regress — accessibility and SEO — are hard errors, while performance and
best-practices (which a legitimate product film or a business decision to run
AdSense can legitimately lower) are warnings that surface a regression without
forcing a harmful "fix".

## Running locally

```sh
make dist                        # assemble _site/
npx @lhci/cli autorun            # uses .lighthouserc.json
```

Reports are written to `_reports/lighthouse/`.
