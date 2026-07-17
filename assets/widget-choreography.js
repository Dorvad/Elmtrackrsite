/*
 * Scroll-linked widget choreography for the homepage sticky section.
 *
 * The old implementation measured getBoundingClientRect() in a perpetual
 * requestAnimationFrame loop. This version activates only near the section,
 * caches stable geometry, and schedules at most one read-then-write pass for
 * each scroll/resize frame.
 */
(function () {
  "use strict";

  var stage = document.getElementById("widgets");
  if (!stage) return;

  var widgets = [0, 1, 2, 3].map(function (index) {
    return document.querySelector('[data-w="' + index + '"]');
  });
  if (!widgets[0]) return;

  var reduceMotion = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var specs = [
    [widgets[0], -420, 160, -22, 0.05],
    [widgets[1], 460, -180, 14, 0.22],
    [widgets[2], 380, 300, 10, 0.42],
    [widgets[3], -360, 260, -12, 0.62]
  ];

  function ease(value) {
    return 1 - Math.pow(1 - value, 3);
  }

  function render(progress) {
    for (var index = 0; index < specs.length; index++) {
      var spec = specs[index];
      var element = spec[0];
      if (!element) continue;
      var local = Math.max(0, Math.min(1, (progress - spec[4]) / 0.26));
      var amount = ease(local);
      var inverse = 1 - amount;
      element.style.opacity = amount;
      element.style.transform =
        "translate3d(" + (spec[1] * inverse).toFixed(1) + "px," +
        (spec[2] * inverse).toFixed(1) + "px,0) rotate(" +
        (spec[3] * inverse).toFixed(2) + "deg) scale(" +
        (0.72 + 0.28 * amount).toFixed(3) + ")";
    }
  }

  if (reduceMotion) {
    render(1);
    return;
  }

  // Establish the pre-scroll state without forcing a geometry read.
  render(0);

  var active = false;
  var geometryValid = false;
  var stageTop = 0;
  var stageHeight = 0;
  var viewportHeight = 0;
  var frameId = 0;
  var terminalProgress = null;
  var observer = null;
  var passive = { passive: true };

  function scrollTop() {
    return window.scrollY || window.pageYOffset || 0;
  }

  function cacheObserverGeometry(entry) {
    stageTop = scrollTop() + entry.boundingClientRect.top;
    stageHeight = entry.boundingClientRect.height;
    viewportHeight = window.innerHeight;
    geometryValid = true;
  }

  function readInvalidatedGeometry() {
    // This is the only synchronous layout read. It runs after resize/font/load
    // invalidation, never on the ordinary scroll path.
    var rect = stage.getBoundingClientRect();
    stageTop = scrollTop() + rect.top;
    stageHeight = rect.height;
    viewportHeight = window.innerHeight;
    geometryValid = true;
  }

  function flush() {
    frameId = 0;
    if (!active) {
      if (terminalProgress !== null) {
        render(terminalProgress);
        terminalProgress = null;
      }
      return;
    }

    // Batch the optional geometry read before all style writes in render().
    if (!geometryValid) readInvalidatedGeometry();
    var distance = Math.max(stageHeight - viewportHeight, 1);
    var progress = Math.max(0, Math.min(1, (scrollTop() - stageTop) / distance));
    render(progress);
  }

  function schedule() {
    if (!frameId) frameId = window.requestAnimationFrame(flush);
  }

  function onScroll() {
    schedule();
  }

  function onResize() {
    geometryValid = false;
    schedule();
  }

  function activate(entry) {
    terminalProgress = null;
    cacheObserverGeometry(entry);
    if (!active) {
      active = true;
      window.addEventListener("scroll", onScroll, passive);
      window.addEventListener("resize", onResize);
    }
    schedule();
  }

  function deactivate(entry) {
    if (active) {
      active = false;
      window.removeEventListener("scroll", onScroll, passive);
      window.removeEventListener("resize", onResize);
    }
    geometryValid = false;
    terminalProgress = entry.boundingClientRect.bottom < 0 ? 1 : 0;
    schedule();
  }

  if ("IntersectionObserver" in window) {
    observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) activate(entry);
        else deactivate(entry);
      });
    }, { rootMargin: "100% 0px", threshold: 0 });
    observer.observe(stage);
  } else {
    // Legacy fallback remains event-driven; modern browsers use the observer.
    active = true;
    window.addEventListener("scroll", onScroll, passive);
    window.addEventListener("resize", onResize);
    schedule();
  }

  function invalidateIfActive() {
    if (!active) return;
    geometryValid = false;
    schedule();
  }

  window.addEventListener("load", invalidateIfActive, { once: true });
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(invalidateIfActive);
  }

  function destroy() {
    active = false;
    window.removeEventListener("scroll", onScroll, passive);
    window.removeEventListener("resize", onResize);
    if (observer) observer.disconnect();
    if (frameId) window.cancelAnimationFrame(frameId);
    frameId = 0;
    terminalProgress = null;
  }

  window.addEventListener("pagehide", destroy, { once: true });
})();
