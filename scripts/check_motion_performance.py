#!/usr/bin/env python3
"""Regression checks for the homepage's layout-sensitive motion code."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOMEPAGES = [ROOT / "index.html", ROOT / "he" / "index.html"]
MOTION = ROOT / "assets" / "widget-choreography.js"


def main() -> int:
    problems: list[str] = []

    for page in HOMEPAGES:
        text = page.read_text(encoding="utf-8")
        rel = page.relative_to(ROOT).as_posix()
        if "widget-choreography.js" not in text:
            problems.append(f"{rel}: widget choreography utility is not loaded")
        if "getBoundingClientRect" in text:
            problems.append(f"{rel}: synchronous geometry read remains inline")
        if "requestAnimationFrame(loop)" in text:
            problems.append(f"{rel}: perpetual animation-frame loop remains")
        if "@keyframes floatPhone{0%,100%{margin-top" in text:
            problems.append(f"{rel}: phone float still animates margin-top")
        if "@keyframes floatWatch{0%,100%{margin-top" in text:
            problems.append(f"{rel}: watch float still animates margin-top")

    motion = MOTION.read_text(encoding="utf-8")
    required = {
        "IntersectionObserver activation": "new IntersectionObserver",
        "passive scroll listener": 'window.addEventListener("scroll", onScroll, passive)',
        "scroll listener cleanup": 'window.removeEventListener("scroll", onScroll, passive)',
        "resize invalidation": "geometryValid = false;",
        "frame batching": "window.requestAnimationFrame(flush)",
        "page lifecycle cleanup": 'window.addEventListener("pagehide", destroy',
        "transform-only motion": "translate3d("
    }
    for label, needle in required.items():
        if needle not in motion:
            problems.append(f"widget-choreography.js: missing {label}")

    if motion.count("getBoundingClientRect") != 2:
        # One occurrence is the explanatory header comment and one is the
        # single invalidation-only measurement call.
        problems.append(
            "widget-choreography.js: expected one measurement call outside "
            "the header comment"
        )
    forbidden_writes = ["style.width", "style.height", "style.top", "style.left", "style.margin"]
    for needle in forbidden_writes:
        if needle in motion:
            problems.append(f"widget-choreography.js: layout write remains: {needle}")

    if problems:
        for problem in problems:
            print(f"FAIL  {problem}")
        return 1

    print(
        "PASS  homepage motion is observer-activated, frame-batched, "
        "passive, cached, and transform-only"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
