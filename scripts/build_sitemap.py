#!/usr/bin/env python3
"""Reproducible sitemap generator for the Elmtrackr marketing site.

Replaces the hand-maintained ``sitemap.xml`` with output derived entirely
from ``scripts/seo_manifest.json``. It:

  * includes every canonical, indexable, existing English (and, once it
    ships, Hebrew) page;
  * excludes redirects, duplicate URLs and ``noindex`` pages;
  * uses the ``lastmod`` recorded per route (validated as an ISO date);
  * emits reciprocal ``hreflang`` alternates (``en`` / ``he`` /
    ``x-default``) only for languages that actually exist in a group;
  * omits ``priority`` and ``changefreq`` (they carry no reliable signal);
  * validates the generated XML by re-parsing it before writing;
  * leaves ``ads.txt`` untouched and confirms it is still present.

Only Python's standard library is used.

Usage:
    python3 scripts/build_sitemap.py            # write sitemap.xml
    python3 scripts/build_sitemap.py --check     # verify sitemap.xml is up to date (no write)
"""
from __future__ import annotations

import os
import sys
from xml.dom import minidom
from xml.etree import ElementTree as ET

from _seo_common import (
    REPO_ROOT,
    hreflang_alternates,
    is_iso_date,
    load_manifest,
    sitemap_routes,
)

SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
XHTML_NS = "http://www.w3.org/1999/xhtml"
SITEMAP_PATH = os.path.join(REPO_ROOT, "sitemap.xml")
ADS_TXT_PATH = os.path.join(REPO_ROOT, "ads.txt")


def build_xml(manifest: dict) -> str:
    routes = sitemap_routes(manifest)
    if not routes:
        raise ValueError("no indexable routes to emit — refusing to write an empty sitemap")

    ET.register_namespace("", SM_NS)
    ET.register_namespace("xhtml", XHTML_NS)
    urlset = ET.Element(f"{{{SM_NS}}}urlset")

    for route in routes:
        lastmod = route.get("lastmod")
        if not is_iso_date(lastmod):
            raise ValueError(f"route {route['path']}: 'lastmod' is not a valid ISO date: {lastmod!r}")

        url_el = ET.SubElement(urlset, f"{{{SM_NS}}}url")
        loc = ET.SubElement(url_el, f"{{{SM_NS}}}loc")
        loc.text = route["canonical"]
        lm = ET.SubElement(url_el, f"{{{SM_NS}}}lastmod")
        lm.text = lastmod

        # Reciprocal hreflang alternates — only for languages that exist.
        group = route.get("hreflang_group")
        alts = hreflang_alternates(manifest, group) if group else []
        if len(alts) > 1:
            for alt in alts:
                link = ET.SubElement(url_el, f"{{{XHTML_NS}}}link")
                link.set("rel", "alternate")
                link.set("hreflang", alt["language"])
                link.set("href", alt["canonical"])
            # x-default → the English page in the group, else the first alt.
            default = next((a for a in alts if a["language"] == "en"), alts[0])
            xdef = ET.SubElement(url_el, f"{{{XHTML_NS}}}link")
            xdef.set("rel", "alternate")
            xdef.set("hreflang", "x-default")
            xdef.set("href", default["canonical"])

    raw = ET.tostring(urlset, encoding="utf-8")
    # Validate by re-parsing before we pretty-print or write anything.
    ET.fromstring(raw)
    pretty = minidom.parseString(raw).toprettyxml(indent="  ", encoding="UTF-8")
    return pretty.decode("utf-8").strip() + "\n"


def main(argv: list[str]) -> int:
    check_only = "--check" in argv[1:]
    manifest = load_manifest()
    xml = build_xml(manifest)

    if check_only:
        current = ""
        if os.path.isfile(SITEMAP_PATH):
            with open(SITEMAP_PATH, encoding="utf-8") as fh:
                current = fh.read()
        if current != xml:
            print("FAIL  sitemap.xml is out of date — run: python3 scripts/build_sitemap.py")
            return 1
        print("PASS  sitemap.xml is up to date")
        return 0

    with open(SITEMAP_PATH, "w", encoding="utf-8") as fh:
        fh.write(xml)

    url_count = xml.count("<loc>")
    print(f"Wrote {os.path.relpath(SITEMAP_PATH, REPO_ROOT)} with {url_count} URL(s).")

    # Preserve ads.txt — never touched here, but confirm it survived.
    if os.path.isfile(ADS_TXT_PATH):
        print("OK    ads.txt present (untouched).")
    else:
        print("WARN  ads.txt is missing — it must be preserved.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
