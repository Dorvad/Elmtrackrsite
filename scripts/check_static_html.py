#!/usr/bin/env python3
"""Static-source validator for the Elmtrackr marketing site.

Fails (exit code 1) when a page's *initial* HTML — what a crawler or a
JavaScript-less browser sees — is incomplete or invalid. Specifically it
flags, per page:

  * visible HTML containing ``{{`` (unrendered template interpolation)
  * visible HTML containing unresolved custom template values
    (``<x-dc>``, ``<helmet>``, ``<sc-*>`` elements, or ``style-hover``/
    ``ref="{{`` attributes left over from the runtime)
  * a missing ``lang`` attribute on ``<html>``
  * not exactly one ``<h1>``
  * a missing ``<main>``
  * an internal anchor (``href="#id"``) whose target ``id`` is absent
  * an ``<img>`` with no ``alt`` attribute
  * a link with an empty ``href`` (``href=""`` or ``href="#"``)

Only Python's standard library is used.

Usage:
    python3 scripts/check_static_html.py [file ...]

With no arguments it checks the site's shipped HTML pages
(``index.html``, ``privacy.html``, ``terms.html`` and ``he/index.html`` if
present). Script and style contents and HTML comments are stripped before
the template-token checks, so documented examples inside ``<script>`` blocks
do not cause false positives.
"""
from __future__ import annotations

import os
import re
import sys
from html.parser import HTMLParser

# Custom runtime tokens that must never reach shipped, visible HTML.
CUSTOM_ELEMENT_RE = re.compile(r"<\s*(x-dc|helmet|sc-[a-z0-9-]+)\b", re.I)
CUSTOM_ATTR_RE = re.compile(r'\bstyle-hover\s*=|\bref\s*=\s*"\{\{', re.I)
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b.*?</\1\s*>", re.I | re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang: str | None = None
        self.saw_html = False
        self.h1_count = 0
        self.main_count = 0
        self.ids: set[str] = set()
        self.anchor_hrefs: list[str] = []
        self.imgs_without_alt = 0
        self.img_total = 0

    def handle_starttag(self, tag, attrs):
        d = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "html" and not self.saw_html:
            self.saw_html = True
            self.html_lang = d.get("lang")
        if tag == "h1":
            self.h1_count += 1
        if tag == "main":
            self.main_count += 1
        if "id" in d and d["id"]:
            self.ids.add(d["id"])
        if tag == "a":
            # href present but empty, or absent entirely on an anchor, is only
            # flagged when the attribute exists and is empty (per spec).
            if "href" in d:
                self.anchor_hrefs.append(d["href"])
        if tag == "img":
            self.img_total += 1
            if "alt" not in d:
                self.imgs_without_alt += 1

    # treat self-closing tags identically
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def visible_markup(html: str) -> str:
    """Markup as a crawler renders it: script/style bodies and comments gone,
    element tags retained."""
    html = SCRIPT_STYLE_RE.sub("", html)
    html = COMMENT_RE.sub("", html)
    return html


def check_file(path: str) -> list[str]:
    with open(path, encoding="utf-8") as fh:
        html = fh.read()

    problems: list[str] = []
    visible = visible_markup(html)

    if "{{" in visible:
        problems.append("visible HTML contains '{{' (unrendered template interpolation)")
    m = CUSTOM_ELEMENT_RE.search(visible)
    if m:
        problems.append(f"visible HTML contains custom template element '<{m.group(1)}>'")
    m = CUSTOM_ATTR_RE.search(visible)
    if m:
        problems.append("visible HTML contains a custom template attribute (style-hover / ref=\"{{)")

    p = PageParser()
    p.feed(html)

    if not p.saw_html or not (p.html_lang and p.html_lang.strip()):
        problems.append("<html> is missing a non-empty lang attribute")
    if p.h1_count != 1:
        problems.append(f"expected exactly one <h1>, found {p.h1_count}")
    if p.main_count < 1:
        problems.append("page has no <main> element")
    if p.imgs_without_alt:
        problems.append(f"{p.imgs_without_alt} <img> element(s) missing an alt attribute")

    for href in p.anchor_hrefs:
        h = href.strip()
        if h == "" or h == "#":
            problems.append("a link has an empty href")
        elif h.startswith("#"):
            target = h[1:]
            if target not in p.ids:
                problems.append(f"internal anchor target missing: '{href}'")

    return problems


def default_targets() -> list[str]:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = ["index.html", "privacy.html", "terms.html", "he/index.html"]
    return [os.path.join(root, c) for c in candidates
            if os.path.isfile(os.path.join(root, c))]


def main(argv: list[str]) -> int:
    targets = argv[1:] or default_targets()
    if not targets:
        print("check_static_html: no HTML files to check", file=sys.stderr)
        return 1

    failed = False
    for path in targets:
        rel = os.path.relpath(path)
        try:
            problems = check_file(path)
        except FileNotFoundError:
            print(f"FAIL  {rel}\n        - file not found")
            failed = True
            continue
        if problems:
            failed = True
            print(f"FAIL  {rel}")
            for pr in problems:
                print(f"        - {pr}")
        else:
            print(f"PASS  {rel}")

    print()
    print("RESULT:", "FAIL" if failed else "PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
