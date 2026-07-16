/*!
 * Elmtrackr — vendor-neutral analytics layer.
 *
 * Exposes window.trackElmEvent(name, properties). It sends events only to an
 * analytics provider that is ALREADY configured on the page (gtag / GTM
 * dataLayer); otherwise it is a safe no-op. It never throws, never blocks
 * navigation, never sends page copy / emails / other personal data, and
 * respects a consent signal when one exists (window.__elmtrackrConsent).
 *
 * No provider ID is embedded here. To connect a vendor later, see
 * docs/seo/analytics.md.
 */
(function () {
  "use strict";
  var W = window, D = document;

  // ---- consent -------------------------------------------------------------
  // A host page (or a future consent tool) may set window.__elmtrackrConsent
  // to "granted" or "denied". Only "denied" suppresses sending and storage.
  function consentDenied() {
    try { return W.__elmtrackrConsent === "denied"; } catch (e) { return false; }
  }

  // ---- value hygiene -------------------------------------------------------
  function isSafeValue(v) {
    if (v == null) return false;
    var s = String(v);
    if (s.length > 100) return false;              // no long free text / copy
    if (s.indexOf("@") !== -1) return false;        // no emails
    if (/https?:\/\//i.test(s)) return false;       // no full URLs
    return true;
  }
  function cleanToken(s) {
    return String(s || "").toLowerCase().replace(/[^a-z0-9._-]/g, "").slice(0, 64);
  }

  // ---- referrer classification (category only; never the raw URL) ---------
  function classifyReferrer() {
    var ref = "";
    try { ref = D.referrer || ""; } catch (e) {}
    if (!ref) return "direct";
    var host = "";
    try { host = new URL(ref).hostname.toLowerCase(); } catch (e) { return "other_referral"; }
    var self = "";
    try { self = location.hostname.toLowerCase(); } catch (e) {}
    if (host === self) return "internal";
    var rules = [
      [/(^|\.)chatgpt\.com$/, "chatgpt"],
      [/(^|\.)chat\.openai\.com$/, "chatgpt"],
      [/(^|\.)openai\.com$/, "chatgpt"],
      [/(^|\.)copilot\.microsoft\.com$/, "copilot"],
      [/(^|\.)perplexity\.ai$/, "perplexity"],
      [/(^|\.)bing\.com$/, "bing"],
      [/(^|\.)(google)\./, "google"],
      [/(^|\.)(facebook|instagram|twitter|x|linkedin|youtube|youtu|tiktok|reddit|pinterest|t)\.(com|co|be)$/, "social"],
      [/(^|\.)(l\.facebook|lm\.facebook|m\.facebook)\.com$/, "social"],
      [/(^|\.)(whatsapp|wa|chat\.whatsapp)\.(com|me)$/, "social"],
      [/(^|\.)(discord|discordapp)\.(com|gg)$/, "social"]
    ];
    for (var i = 0; i < rules.length; i++) if (rules[i][0].test(host)) return rules[i][1];
    return "other_referral";
  }

  // ---- campaign (UTM) capture, session-scoped, consent-gated --------------
  var CAMPAIGN_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"];
  function storageOK() {
    try { var k = "__elm_t"; sessionStorage.setItem(k, "1"); sessionStorage.removeItem(k); return true; }
    catch (e) { return false; }
  }
  function captureCampaign() {
    var current = {};
    try {
      var p = new URLSearchParams(location.search);
      CAMPAIGN_KEYS.forEach(function (k) { if (p.get(k)) current[k] = cleanToken(p.get(k)); });
    } catch (e) {}
    if (!consentDenied() && storageOK()) {
      try {
        if (Object.keys(current).length) {
          sessionStorage.setItem("elm_campaign", JSON.stringify(current));
        }
      } catch (e) {}
    }
    return current;
  }
  function getCampaign() {
    var cur = captureCampaign();
    if (Object.keys(cur).length) return cur;
    if (consentDenied() || !storageOK()) return {};
    try { return JSON.parse(sessionStorage.getItem("elm_campaign") || "{}"); } catch (e) { return {}; }
  }

  // ---- send ----------------------------------------------------------------
  function deliver(name, payload) {
    try {
      if (typeof W.gtag === "function") { W.gtag("event", name, payload); return; }
      if (W.dataLayer && typeof W.dataLayer.push === "function") {
        var o = { event: name }; for (var k in payload) if (payload.hasOwnProperty(k)) o[k] = payload[k];
        W.dataLayer.push(o); return;
      }
      // no provider configured -> safe no-op
    } catch (e) { /* never throw */ }
  }

  function trackElmEvent(name, properties) {
    try {
      if (!name || consentDenied()) return;
      var payload = {
        page_path: (location.pathname || "/"),
        language: (D.documentElement && D.documentElement.lang) || "",
        referrer_category: classifyReferrer()
      };
      var c = getCampaign();
      if (c.utm_source) payload.campaign_source = c.utm_source;
      if (c.utm_medium) payload.campaign_medium = c.utm_medium;
      if (c.utm_campaign) payload.campaign_name = c.utm_campaign;
      if (c.utm_content) payload.campaign_content = c.utm_content;
      if (properties && typeof properties === "object") {
        for (var k in properties) {
          if (properties.hasOwnProperty(k) && isSafeValue(properties[k])) {
            payload[k] = String(properties[k]);
          }
        }
      }
      deliver(String(name).slice(0, 60), payload);
    } catch (e) { /* never throw */ }
  }
  W.trackElmEvent = trackElmEvent;

  // ---- auto-wiring ---------------------------------------------------------
  function propsFrom(el) {
    var p = {};
    if (el.getAttribute("data-elm-cta")) p.cta_location = cleanToken(el.getAttribute("data-elm-cta"));
    if (el.getAttribute("data-elm-dest")) p.destination_type = cleanToken(el.getAttribute("data-elm-dest"));
    if (el.getAttribute("data-elm-to")) p.to_language = cleanToken(el.getAttribute("data-elm-to"));
    return p;
  }
  function handleActivate(e, isAux) {
    // primary click = button 0; middle click arrives via auxclick (button 1)
    if (isAux && e.button !== 1) return;
    if (!isAux && e.button && e.button !== 0) return;
    var el = e.target && e.target.closest ? e.target.closest("[data-elm-event]") : null;
    if (!el) return;
    trackElmEvent(el.getAttribute("data-elm-event"), propsFrom(el));
  }

  function wireVideo() {
    var v = D.querySelector("[data-elm-video]");
    if (!v) return;
    var fired = { play: false, p25: false, p50: false, done: false };
    v.addEventListener("play", function () {
      if (fired.play) return; fired.play = true; trackElmEvent("video_play", { cta_location: "film" });
    });
    v.addEventListener("timeupdate", function () {
      if (!v.duration) return;
      var pct = v.currentTime / v.duration;
      if (!fired.p25 && pct >= 0.25) { fired.p25 = true; trackElmEvent("video_25_percent", { cta_location: "film" }); }
      if (!fired.p50 && pct >= 0.50) { fired.p50 = true; trackElmEvent("video_50_percent", { cta_location: "film" }); }
    });
    v.addEventListener("ended", function () {
      if (fired.done) return; fired.done = true; trackElmEvent("video_complete", { cta_location: "film" });
    });
  }

  function wireFaq() {
    var list = D.querySelectorAll(".cp-faq-list details, .faq-list details");
    Array.prototype.forEach.call(list, function (d) {
      var fired = false;
      d.addEventListener("toggle", function () {
        if (d.open && !fired) { fired = true; trackElmEvent("faq_expand", { cta_location: "faq" }); }
      });
    });
  }

  function init() {
    try { captureCampaign(); } catch (e) {}
    D.addEventListener("click", function (e) { handleActivate(e, false); }, true);
    D.addEventListener("auxclick", function (e) { handleActivate(e, true); }, true);
    wireVideo();
    wireFaq();
  }
  if (D.readyState === "loading") D.addEventListener("DOMContentLoaded", init);
  else init();
})();
