# AdSense Rendering & Layout Impact — Audit and Optimization

Internal engineering note. Excluded from the published site (see `Makefile` →
`INTERNAL`). Companion to `LCP_DIAGNOSIS.md` and `CRP_OPTIMIZATION.md`.

## Scope

Reduce the initial rendering/layout impact of Google AdSense, specifically the
~76 ms forced reflow Lighthouse attributes to Google's
`show_ads_impl_fy2021.js`, without violating Google policy or consent
requirements.

## Audit results

The home pages (`index.html`, `he/index.html`) are the only pages that carry any
advertising code. Findings, point by point:

1. **Is Auto Ads enabled?** Yes. The page contains only the AdSense loader tag
   with the publisher client ID and **no** ad slots — the canonical modern
   Auto Ads pattern. Page-level ad enablement is controlled in the AdSense
   dashboard (server side), not in page code. There is no legacy
   `enable_page_level_ads` push (not required since 2019).
2. **Are manual ad slots used?** No. There are zero `<ins class="adsbygoogle">`
   elements and zero `data-ad-slot` / `data-ad-format` attributes in any page
   (source or built `_site/`).
3. **Is the loader included more than once?** No. Exactly one
   `pagead/js/adsbygoogle.js` tag per page, and only on the two home pages.
   Verified in source and in the built output; a headless load requested
   `adsbygoogle.js` exactly **once**.
4. **Does Funding Choices load separately or repeatedly?** No. Google Privacy &
   Messaging / Funding Choices is delivered through the same single
   `adsbygoogle.js` chain. There is no separate `fundingchoices.google.com`
   script and no duplicate consent bootstrap. (The "not a consent manager"
   comments elsewhere belong to the unrelated first-party analytics loader.)
5. **Are ads initialized before meaningful content renders?** No. The loader is
   `async` in `<head>`, so it is fetched early but does not block HTML parsing or
   rendering. The hero is complete static HTML and paints independently of the ad
   script. Auto Ads only measures/injects after its script executes.
6. **Is any ad in or near the initial viewport?** No manual ad is placed in the
   hero. Auto Ads placement is decided by Google at runtime; it may serve a
   fixed-position anchor ad (no layout shift) or in-content ads further down the
   page. Page code does not position any ad.
7. **Do ad containers have reserved dimensions?** There are no first-party ad
   containers to reserve. Auto Ads injects and sizes its own containers; anchor
   ads are `position: fixed` (no CLS); in-content insertions are Google-managed.
8. **Are ad scripts responsible for the delayed FCP?** Not directly. The loader
   is `async` and non-render-blocking, so it does not gate FCP in the critical
   request graph. Its main-thread execution — including the ~76 ms forced reflow
   in `show_ads_impl_fy2021.js` — is additional main-thread work that can affect
   FCP and Speed Index on real devices/networks. That work is inside Google's
   code.

## What was changed

**No page code was changed, because the implementation already satisfies every
safe optimization in the brief:**

| Safe optimization | Status |
| --- | --- |
| Global AdSense script loads only once | Already true (one tag/page) |
| Keep it asynchronous | Already `async` |
| Do not block hero / initial HTML on AdSense | Already non-blocking (`async`, static hero) |
| Advertising init after critical content *when allowed* | See note below — not safely applicable to Auto Ads |
| Per-slot IntersectionObserver init for manual below-the-fold slots | N/A — there are no manual slots |
| IntersectionObserver with root margin | N/A — no manual slots |
| Reserve stable ad dimensions / min-heights | N/A — no first-party ad containers |
| No scroll polling | Already true |
| Do not initialize slots that don't exist | Already true — no slot init at all |
| Prevent duplicate `adsbygoogle.push()` | N/A — no `push()` calls exist |
| Keep consent ahead of nonessential ad behavior | Preserved (single chain, consent first) |
| No new dependencies | None added |

Auto Ads is a single Google-managed script. The only lever page code has over it
is *when the one tag loads*. Wrapping that in a custom deferral/IntersectionObserver
mechanism would be exactly the "brittle custom loader" the brief warns against,
and it would move consent timing as a side effect. Per the brief's fallback
clause ("If Auto Ads makes fine-grained deferral unsafe or unsupported: keep the
supported Auto Ads implementation; do not create a brittle custom loader"), the
supported implementation was kept as-is.

## What remains controlled by Google

- The ~76 ms forced reflow inside `show_ads_impl_fy2021.js` (Auto Ads page
  measurement).
- All ad placement decisions and the number/type of ads.
- Any layout shift from dynamically injected in-content Auto Ads.
- Rendering and timing of the Funding Choices consent UI within the chain.

These cannot be modified without editing Google's third-party code (prohibited)
or changing the ad product.

## Does the 76 ms forced reflow remain?

**Yes.** It originates entirely within Google's `show_ads_impl_fy2021.js` and is
intrinsic to how Auto Ads scans and measures the page to choose placements. It
cannot be removed while Auto Ads is in use without editing Google's code. It is
therefore documented here as an **unavoidable third-party cost of Auto Ads**, not
a first-party defect. (The previously reported first-party forced reflow is gone
and did not return.)

## Optional monetization tradeoffs (NOT implemented)

Both options below change monetization and/or consent timing, so per the brief
they are recommendations only and were **not** applied silently.

### Option A — Defer the single Auto Ads tag until after critical content
Load `adsbygoogle.js` after first paint (e.g. on the `load` event or first user
interaction) instead of in `<head>`. This moves the reflow and ad main-thread
work out of the FCP/Speed-Index window.
- **Benefit:** measurable FCP/Speed Index/TBT improvement on real devices.
- **Cost:** the consent prompt and ads appear later; Auto Ads coverage/revenue
  may drop; contradicts Google's recommended `<head>` placement.
- **Compliance:** consent still precedes ad serving (chain order preserved), so
  it does not start tracking before consent — but it *delays* the consent UI,
  which the in-repo note explicitly says to review first. Requires a product
  decision.

### Option B — Move from Auto Ads to manual below-the-fold slots
Replace Auto Ads with explicit `<ins class="adsbygoogle">` slots placed below the
fold, each initialized by `adsbygoogle.push({})` only when its container nears the
viewport via IntersectionObserver (root margin ~200–400 px), with reserved
`min-height` to prevent CLS, and a guard to prevent duplicate pushes.
- **Benefit:** full control of placement/timing; removes the Auto Ads page-scan
  reflow; deterministic CLS reservation.
- **Cost:** loses Auto Ads' automatic optimization; requires ongoing slot
  management; typically different revenue characteristics.
- This is a monetization change and must be an explicit decision.

If Option B is chosen, the safe pattern is: keep the single async loader; do
**not** call `push()` for slots that are not on the page; observe each slot once;
`unobserve` after the first push; never refresh or re-push; keep consent ahead of
any push.

## Testing performed and limitations

**Environment limitation (important):** in this build/sandbox the Google ad
domain `pagead2.googlesyndication.com` is blocked by the outbound proxy
(`ERR_CONNECTION_RESET`). Live ad rendering, the Funding Choices consent matrix
(fresh cookies, existing consent, accepted, rejected), ad-blocker behavior, and
the real 76 ms reflow **cannot be exercised here** and must be validated on the
deployed origin (or any network where the ad domain is reachable).

Verified in this environment:
- The AdSense loader is requested exactly **once** (headless network capture).
- The loader carries `async` and `crossorigin="anonymous"` (Google's snippet).
- The hero renders as static HTML without waiting for ads; the LCP element still
  fires (PerformanceObserver ~0.1 s; ~2.1–2.2 s under simulated mobile
  throttling).
- No first-party console errors (only the sandbox's ad-domain block).
- CLS from first-party code is 0 (mobile simulation).
- Publisher/slot IDs unchanged; no `push()` added; no auto-refresh; no
  impression fabrication; no request-then-hide.

To validate on a reachable network, test the matrix from the brief (fresh
cookies / existing consent / accepted / rejected / ad-blocker off / slow mobile /
mobile + desktop) and confirm: ads appear, loader requested once, consent valid,
no new CLS, no console errors, hero renders before ads.
