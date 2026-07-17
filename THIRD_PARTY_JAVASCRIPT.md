# Third-party JavaScript baseline

Reviewed: 2026-07-17

## Shipped integration

The English and Hebrew homepages are the only advertising pages. Each contains
one asynchronous Google Auto Ads loader with the existing publisher ID. There
are no authored `<ins class="adsbygoogle">` slots and no `adsbygoogle.push()`
calls. Other pages contain no advertising tag.

Google injects DoubleClick, `show_ads_impl`, `lidar`, traffic-quality code and,
when the visitor's region and account configuration require it, Privacy &
Messaging / Funding Choices. Those resources are not separate repository
integrations and cannot be removed or individually deferred here.

The Auto Ads loader deliberately remains asynchronous in the document head.
Deferring it to an idle or viewport event could also delay Google's conditional
consent interface. That consent and monetization tradeoff is not safe to change
without the publisher's AdSense account configuration and regional testing.

The first-party `assets/analytics.js` runtime is optional and provider-neutral.
No analytics provider is currently configured, so fetching and evaluating it
was pure overhead. `assets/analytics-loader.js` now waits for `window.load`,
then an idle callback (bounded by a timeout), and fetches the runtime only if
`gtag` or `dataLayer` already exists and consent is not explicitly denied. The
loader is not a CMP and does not run before or replace Funding Choices.

## Baseline and measured result

The preserved 2026-07-16 mobile Lighthouse trace reports:

- `assets/analytics.js`: 52.7 ms total main-thread work, including 45.6 ms of
  scripting.
- Total main-thread work: 10.46 s. Most of that total is first-party continuous
  animation/rendering work, not analytics; this task does not alter visuals.
- Earlier AdSense-connected measurements attributed about 155 KiB of unused
  JavaScript to Google's `show_ads_impl` and loader code. That code is
  Google-controlled and remains an expected Lighthouse warning while Auto Ads
  is enabled.

The final 2026-07-17 mobile Lighthouse run and browser checks show:

- One `adsbygoogle.js` request and one Google-injected `show_ads_impl` request.
  Lighthouse also recorded two DoubleClick requests and no Funding Choices
  request in the current local region/session.
- One 1,573-byte fingerprinted analytics loader request and no request for the
  7,910-byte analytics runtime. The runtime no longer appears in Lighthouse's
  bootup table, removing its previous 45.6 ms of scripting from the current
  provider-free configuration.
- Total main-thread work was 5.11 s after versus 10.46 s in the preserved trace.
  Script evaluation was 1.082 s after versus 0.972 s before because the final
  run successfully loaded Google's advertising code while the earlier local
  trace did not. These whole-page figures are run-sensitive because the page
  has continuous animation; the reliable task-specific comparison is the
  disappearance of the 52.7 ms analytics runtime entry.
- The remaining unused-JavaScript estimate is 155 KiB: 127,988 bytes in
  Google-controlled `show_ads_impl` and 30,972 bytes in Google's global loader.
- CLS was 0.0008. On localhost Google created one unfilled, zero-size Auto Ads
  placeholder; there are still no authored manual ad containers.
- English and Hebrew homepages produced no advertising or consent console
  warnings/errors. A non-ad guide page loaded no AdSense script.

## Consent and verification boundary

Funding Choices is conditional on geography, prior consent state and settings
inside the publisher's AdSense account. A local static build cannot force or
fully certify that regional flow. Repository verification can establish that
the single early Auto Ads entry point is unchanged and that nothing in the new
analytics loader runs a provider ahead of it. The owner should also use the
Privacy & Messaging preview in AdSense and a clean browser session in every
regulated region served before deployment.

## Optional future manual-placement strategy

Do not combine this with the current Auto Ads strategy silently. If the owner
chooses manual placements later:

1. Decide and configure the monetization change in AdSense first.
2. Add explicit, policy-compliant ad units with fixed or responsive reserved
   dimensions so requested ads are never hidden and do not shift content.
3. Observe only below-the-fold containers with one `IntersectionObserver`
   using a 300–500 px root margin, and make a single request per slot as it
   approaches the viewport.
4. Keep the global AdSense library single-loaded and asynchronous; do not
   refresh slots automatically or manipulate visibility, clicks or views.

Auto Ads chooses and inserts its own containers, so repository CSS cannot
reserve dimensions for those placements without switching strategies. No fake
empty ad area was added in this change.

## Maintainer references

- [Google: About Auto ads](https://support.google.com/adsense/answer/9261805)
- [Google: About European regulations messages](https://support.google.com/adsense/answer/10961068)
- [Google: Modifications of AdSense ad code](https://support.google.com/adsense/answer/1354736)
- [MDN: `requestIdleCallback`](https://developer.mozilla.org/docs/Web/API/Window/requestIdleCallback)
