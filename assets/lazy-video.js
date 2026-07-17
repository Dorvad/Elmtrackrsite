(function () {
  "use strict";

  var videos = document.querySelectorAll("video[data-lazy-video]");
  if (!videos.length) return;

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  videos.forEach(function (video) {
    var loaded = false;

    function attachSources() {
      if (loaded) return;
      loaded = true;

      video.querySelectorAll("source[data-src]").forEach(function (source) {
        source.src = source.dataset.src;
        source.removeAttribute("data-src");
      });
      video.load();
    }

    function playWhenVisible() {
      attachSources();
      video.play().catch(function () {});
    }

    video.addEventListener("pointerdown", attachSources, { once: true, passive: true });
    video.addEventListener("keydown", attachSources, { once: true });
    video.addEventListener("focus", attachSources, { once: true });

    if (!("IntersectionObserver" in window)) return;

    var preloadObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        attachSources();
        preloadObserver.unobserve(video);
      });
    }, { rootMargin: "400px 0px", threshold: 0 });

    preloadObserver.observe(video);

    if (reduceMotion || !video.hasAttribute("data-autoplay")) return;

    var playbackObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && entry.intersectionRatio >= 0.35) playWhenVisible();
        else video.pause();
      });
    }, { threshold: [0, 0.35] });

    playbackObserver.observe(video);
  });
})();
