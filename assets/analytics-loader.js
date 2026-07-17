/*
 * Load Elmtrackr's optional analytics wiring only after the critical page load.
 *
 * This is deliberately not a consent manager. Google Privacy & Messaging /
 * Funding Choices remains part of the single Auto Ads tag in the document
 * head. If an analytics provider is added later, its consent defaults and the
 * window.__elmtrackrConsent signal must be configured before this loader.
 */
(function (W, D) {
  "use strict";

  var bootstrap = D.currentScript;
  var runtimeSrc = bootstrap && bootstrap.getAttribute("data-analytics-src");
  if (!runtimeSrc) return;

  function providerReady() {
    return typeof W.gtag === "function" ||
      Boolean(W.dataLayer && typeof W.dataLayer.push === "function");
  }

  function loadRuntime() {
    // The runtime is a no-op without an existing provider, so do not spend a
    // request or main-thread time on it in the site's current configuration.
    if (W.__elmtrackrConsent === "denied" || !providerReady()) return;
    if (D.querySelector("script[data-elm-analytics-runtime]")) return;

    var script = D.createElement("script");
    script.src = runtimeSrc;
    script.async = true;
    script.setAttribute("data-elm-analytics-runtime", "");
    D.head.appendChild(script);
  }

  function schedule() {
    if (typeof W.requestIdleCallback === "function") {
      W.requestIdleCallback(loadRuntime, { timeout: 2500 });
    } else {
      W.setTimeout(loadRuntime, 1500);
    }
  }

  if (D.readyState === "complete") schedule();
  else W.addEventListener("load", schedule, { once: true });
})(window, document);
