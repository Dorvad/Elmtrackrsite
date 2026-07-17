#!/usr/bin/env python3
"""Validate Elmtrackr's advertising and optional analytics entry points."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADSENSE_HOST = "pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"
PUBLISHER = "ca-pub-6818267616933452"
AD_PAGES = {Path("index.html"), Path("he/index.html")}


class ScriptParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.scripts: list[dict[str, str]] = []
        self.manual_slots = 0

    def handle_starttag(self, tag, attrs):
        values = {key.lower(): value or "" for key, value in attrs}
        if tag == "script":
            self.scripts.append(values)
        if tag == "ins" and "adsbygoogle" in values.get("class", "").split():
            self.manual_slots += 1


def pages() -> list[Path]:
    found = []
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if rel.parts[0] in {"_site", "templates"}:
            continue
        found.append(rel)
    return sorted(found)


def main() -> int:
    problems: list[str] = []
    adsense_total = 0

    for rel in pages():
        text = (ROOT / rel).read_text(encoding="utf-8")
        parser = ScriptParser()
        parser.feed(text)

        ad_scripts = [
            attrs for attrs in parser.scripts
            if ADSENSE_HOST in attrs.get("src", "")
        ]
        adsense_total += len(ad_scripts)
        expected = 1 if rel in AD_PAGES else 0
        if len(ad_scripts) != expected:
            problems.append(
                f"{rel.as_posix()}: expected {expected} Auto Ads tag(s), "
                f"found {len(ad_scripts)}"
            )
        for attrs in ad_scripts:
            if "async" not in attrs:
                problems.append(f"{rel.as_posix()}: Auto Ads tag is not async")
            if PUBLISHER not in attrs.get("src", ""):
                problems.append(f"{rel.as_posix()}: publisher ID changed or missing")
            if attrs.get("id") != "elmtrackr-adsense":
                problems.append(f"{rel.as_posix()}: Auto Ads script ID is missing")

        if parser.manual_slots:
            problems.append(
                f"{rel.as_posix()}: unexpected manual AdSense slot(s): "
                f"{parser.manual_slots}"
            )
        if "adsbygoogle.push" in text:
            problems.append(f"{rel.as_posix()}: unexpected manual ad initialization")

        loaders = [
            attrs for attrs in parser.scripts
            if attrs.get("src", "").endswith("analytics-loader.js")
        ]
        direct_runtime = [
            attrs for attrs in parser.scripts
            if attrs.get("src", "").endswith("analytics.js")
        ]
        if direct_runtime:
            problems.append(f"{rel.as_posix()}: analytics runtime loads directly")
        if "data-elm-event" in text and len(loaders) != 1:
            problems.append(
                f"{rel.as_posix()}: event-enabled page needs one analytics "
                f"loader, found {len(loaders)}"
            )
        for attrs in loaders:
            if "defer" not in attrs:
                problems.append(f"{rel.as_posix()}: analytics loader is not deferred")
            if not attrs.get("data-analytics-src", "").endswith("analytics.js"):
                problems.append(f"{rel.as_posix()}: analytics runtime source is missing")

    if adsense_total != 2:
        problems.append(f"site: expected two locale Auto Ads tags, found {adsense_total}")

    if problems:
        for problem in problems:
            print(f"FAIL  {problem}")
        return 1

    print(
        "PASS  one async Auto Ads tag on each advertising page; no manual "
        "slots or duplicate initialization"
    )
    print(
        "PASS  optional analytics uses one deferred, provider-gated loader "
        "on every event-enabled page"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
