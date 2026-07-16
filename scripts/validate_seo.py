#!/usr/bin/env python3
"""Technical-SEO validator for the Elmtrackr marketing site.

Checks the shipped, hand-authored HTML and the generated ``sitemap.xml``
against the single source of truth in ``scripts/seo_manifest.json`` and the
verified product facts. It reports, per check, PASS / WARN / FAIL and exits
non-zero if any FAIL is found.

Checks performed:
  * titles present and non-empty (length advisory)
  * meta descriptions present and non-empty (length advisory)
  * self-referencing canonical URL matches the manifest
  * Open Graph url/title/description present; og:url == canonical
  * every inline JSON-LD block is syntactically valid JSON
  * required schema properties on Organization / WebSite / SoftwareApplication
  * no invented rating/review fields (and no unverified price/offers) in JSON-LD
  * sitemap ↔ canonical consistency (both directions)
  * hreflang reciprocity, driven by the manifest (no Hebrew alternate until /he/ exists)
  * route uniqueness (manifest paths, canonicals, sitemap locs)

Only Python's standard library is used.

Usage:
    python3 scripts/validate_seo.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from html.parser import HTMLParser
from xml.etree import ElementTree as ET

from _seo_common import (
    REPO_ROOT,
    hreflang_alternates,
    load_manifest,
    sitemap_routes,
)

SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
JSONLD_RE = re.compile(
    r'<script[^>]*type\s*=\s*["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
# Fields that must never appear in our JSON-LD (unverifiable / prohibited).
FORBIDDEN_JSONLD_KEYS = {
    "aggregaterating",
    "ratingvalue",
    "ratingcount",
    "reviewcount",
    "bestrating",
    "worstrating",
    "review",
    "reviews",
    "offers",
    "price",
    "pricecurrency",
    "lowprice",
    "highprice",
}
RECOMMENDED_TITLE_MAX = 70
DESC_MIN, DESC_MAX = 50, 160


class Report:
    def __init__(self) -> None:
        self.failed = False
        self.lines: list[str] = []

    def ok(self, msg: str) -> None:
        self.lines.append(f"  PASS  {msg}")

    def warn(self, msg: str) -> None:
        self.lines.append(f"  WARN  {msg}")

    def fail(self, msg: str) -> None:
        self.failed = True
        self.lines.append(f"  FAIL  {msg}")

    def section(self, title: str) -> None:
        self.lines.append("")
        self.lines.append(title)

    def dump(self) -> None:
        print("\n".join(self.lines))


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._in_title = False
        self.title = ""
        self.metas: list[dict] = []
        self.links: list[dict] = []

    def handle_starttag(self, tag, attrs):
        d = {k.lower(): (v or "") for k, v in attrs}
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            self.metas.append(d)
        elif tag == "link":
            self.links.append(d)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def parse_head(path: str) -> HeadParser:
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    p = HeadParser()
    p.feed(html)
    return p, html


def meta_content(head: HeadParser, *, name: str | None = None, prop: str | None = None) -> str | None:
    for m in head.metas:
        if name and m.get("name", "").lower() == name.lower():
            return m.get("content")
        if prop and m.get("property", "").lower() == prop.lower():
            return m.get("content")
    return None


def link_href(head: HeadParser, rel: str) -> str | None:
    for l in head.links:
        if l.get("rel", "").lower() == rel.lower():
            return l.get("href")
    return None


def hreflang_map(head: HeadParser) -> dict[str, str]:
    out: dict[str, str] = {}
    for l in head.links:
        if l.get("rel", "").lower() == "alternate" and l.get("hreflang"):
            out[l["hreflang"].lower()] = l.get("href", "")
    return out


def walk_keys(obj):
    """Yield every (lowercased-key, value) pair recursively through a JSON-LD tree."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k.lower(), v
            yield from walk_keys(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk_keys(item)


def graph_nodes(data) -> list[dict]:
    nodes: list[dict] = []
    blocks = data if isinstance(data, list) else [data]
    for block in blocks:
        if isinstance(block, dict) and "@graph" in block:
            nodes.extend(n for n in block["@graph"] if isinstance(n, dict))
        elif isinstance(block, dict):
            nodes.append(block)
    return nodes


def node_types(node: dict) -> set[str]:
    t = node.get("@type")
    if isinstance(t, list):
        return set(t)
    return {t} if t else set()


def check_page(rep: Report, manifest: dict, route: dict) -> None:
    path = os.path.join(REPO_ROOT, route["file"])
    rep.section(f"[page] {route['path']}  ({route['file']})")
    if not os.path.isfile(path):
        rep.fail(f"file not found: {route['file']}")
        return

    head, html = parse_head(path)
    canonical = route["canonical"]

    # --- title ---
    title = head.title.strip()
    if not title:
        rep.fail("missing/empty <title>")
    else:
        rep.ok(f"title present: {title!r}")
        if len(title) > RECOMMENDED_TITLE_MAX:
            rep.warn(f"title is {len(title)} chars (> {RECOMMENDED_TITLE_MAX} recommended)")

    # --- description ---
    desc = meta_content(head, name="description")
    if not desc or not desc.strip():
        rep.fail("missing/empty meta description")
    else:
        rep.ok("meta description present")
        if not (DESC_MIN <= len(desc) <= DESC_MAX):
            rep.warn(f"meta description is {len(desc)} chars (recommend {DESC_MIN}-{DESC_MAX})")

    # --- canonical ---
    html_canonical = link_href(head, "canonical")
    if not html_canonical:
        rep.fail("missing <link rel=canonical>")
    elif html_canonical != canonical:
        rep.fail(f"canonical {html_canonical!r} != manifest canonical {canonical!r}")
    else:
        rep.ok(f"self-referencing canonical matches manifest: {canonical}")

    # --- Open Graph ---
    og_url = meta_content(head, prop="og:url")
    og_title = meta_content(head, prop="og:title")
    og_desc = meta_content(head, prop="og:description")
    for label, val in (("og:title", og_title), ("og:description", og_desc), ("og:url", og_url)):
        if not val or not val.strip():
            rep.fail(f"missing {label}")
        else:
            rep.ok(f"{label} present")
    if og_url and og_url != canonical:
        rep.fail(f"og:url {og_url!r} != canonical {canonical!r}")
    elif og_url:
        rep.ok("og:url == canonical")

    # --- JSON-LD ---
    blocks = JSONLD_RE.findall(html)
    if not blocks:
        if node_types_expected(route):
            rep.fail("no JSON-LD found on a page that requires structured data")
    for i, raw in enumerate(blocks, 1):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            rep.fail(f"JSON-LD block #{i} is invalid JSON: {e}")
            continue
        rep.ok(f"JSON-LD block #{i} is valid JSON")

        # forbidden (unverifiable/prohibited) fields
        hits = sorted({k for k, _ in walk_keys(data) if k in FORBIDDEN_JSONLD_KEYS})
        if hits:
            rep.fail(f"JSON-LD block #{i} contains forbidden field(s): {', '.join(hits)}")
        else:
            rep.ok(f"JSON-LD block #{i} has no rating/review/price fields")

        # required schema properties
        check_schema_requirements(rep, data, block_no=i)


def node_types_expected(route: dict) -> bool:
    """The homepage is the only page currently required to carry JSON-LD."""
    return route["path"] == "/"


REQUIRED_PROPS = {
    "Organization": ["name", "url", "logo"],
    "WebSite": ["name", "url"],
    "SoftwareApplication": ["name", "applicationCategory", "operatingSystem", "url"],
}


def check_schema_requirements(rep: Report, data, block_no: int) -> None:
    nodes = graph_nodes(data)
    found_types = set()
    for node in nodes:
        for t in node_types(node):
            found_types.add(t)
            if t in REQUIRED_PROPS:
                missing = [p for p in REQUIRED_PROPS[t] if p not in node]
                if missing:
                    rep.fail(f"JSON-LD {t}: missing required propert(y/ies): {', '.join(missing)}")
                else:
                    rep.ok(f"JSON-LD {t}: required properties present")


def check_sitemap(rep: Report, manifest: dict) -> None:
    rep.section("[sitemap] sitemap.xml ↔ canonicals")
    sm_path = os.path.join(REPO_ROOT, "sitemap.xml")
    if not os.path.isfile(sm_path):
        rep.fail("sitemap.xml not found")
        return
    try:
        tree = ET.parse(sm_path)
    except ET.ParseError as e:
        rep.fail(f"sitemap.xml is not valid XML: {e}")
        return
    rep.ok("sitemap.xml is valid XML")

    locs = [el.text.strip() for el in tree.getroot().iter(f"{{{SM_NS}}}loc") if el.text]
    if len(locs) != len(set(locs)):
        rep.fail("sitemap contains duplicate <loc> URLs")
    else:
        rep.ok("sitemap <loc> URLs are unique")

    expected = {r["canonical"] for r in sitemap_routes(manifest)}
    got = set(locs)
    if got != expected:
        missing = expected - got
        extra = got - expected
        if missing:
            rep.fail(f"sitemap missing indexable canonical(s): {', '.join(sorted(missing))}")
        if extra:
            rep.fail(f"sitemap contains non-canonical/non-indexable URL(s): {', '.join(sorted(extra))}")
    else:
        rep.ok(f"sitemap matches indexable canonicals ({len(expected)} URL(s))")

    # noindex / non-existent routes must not appear
    for r in manifest["routes"]:
        if (not r.get("indexable") or r.get("exists") is False or r.get("redirect")) and r["canonical"] in got:
            rep.fail(f"sitemap wrongly includes {r['canonical']} (noindex/redirect/absent)")


def check_hreflang(rep: Report, manifest: dict) -> None:
    rep.section("[hreflang] reciprocity (manifest-driven)")
    for route in manifest["routes"]:
        if not route.get("indexable") or route.get("exists") is False or route.get("redirect"):
            continue
        path = os.path.join(REPO_ROOT, route["file"])
        if not os.path.isfile(path):
            continue
        head, _ = parse_head(path)
        declared = hreflang_map(head)

        alts = hreflang_alternates(manifest, route.get("hreflang_group"))
        expected = {a["language"].lower(): a["canonical"] for a in alts}
        if expected:
            default = next((a for a in alts if a["language"] == "en"), alts[0])
            expected["x-default"] = default["canonical"]

        if declared == expected:
            rep.ok(f"{route['path']}: hreflang set matches manifest ({', '.join(sorted(expected)) or 'none'})")
        else:
            rep.fail(f"{route['path']}: hreflang mismatch — declared {declared} vs expected {expected}")

        # No Hebrew alternate may be emitted before /he/ exists.
        he_exists = any(a["language"] == "he" for a in alts)
        if "he" in declared and not he_exists:
            rep.fail(f"{route['path']}: emits hreflang='he' but no Hebrew page exists yet")


def check_route_uniqueness(rep: Report, manifest: dict) -> None:
    rep.section("[routes] uniqueness")
    paths = [r["path"] for r in manifest["routes"]]
    canons = [r["canonical"] for r in manifest["routes"]]
    if len(paths) != len(set(paths)):
        rep.fail("manifest has duplicate route paths")
    else:
        rep.ok("manifest route paths are unique")
    if len(canons) != len(set(canons)):
        rep.fail("manifest has duplicate canonical URLs")
    else:
        rep.ok("manifest canonical URLs are unique")


def check_play_link_consistency(rep: Report, manifest: dict) -> None:
    rep.section("[links] Play Store URL is centralized")
    play = manifest.get("play_store", {})
    canonical_url = play.get("url", "")
    app_id = play.get("application_id", "")
    idx = os.path.join(REPO_ROOT, "index.html")
    with open(idx, encoding="utf-8") as fh:
        html = fh.read()

    # Every Play link must reach the verified package listing and carry the
    # constant campaign source/medium. utm_campaign / utm_content are allowed
    # to differ per CTA (see docs/seo/analytics.md) — the destination listing
    # is unchanged, so this stays a single canonical destination.
    play_links = re.findall(r'href="([^"]*play\.google\.com[^"]*)"', html)
    if not play_links:
        rep.warn("no Play Store links found on index.html")
    generic = [u for u in play_links if "/store/apps/details" not in u]
    if generic:
        rep.fail(f"generic play.google.com destination still present: {generic}")
    else:
        rep.ok("no generic play.google.com home-page links remain")

    def ok_params(u):
        return (app_id in u
                and "utm_source%3Delmtrackr.site" in u
                and "utm_medium%3Dwebsite" in u)
    bad = [u for u in play_links if not ok_params(u)]
    if bad:
        rep.fail(f"Play link(s) missing verified id / utm_source / utm_medium: {bad}")
    else:
        rep.ok(f"all {len(play_links)} Play link(s) reach the verified listing with consistent source/medium")

    if app_id and app_id not in canonical_url:
        rep.fail("manifest play_store.url does not contain the verified application_id")
    elif app_id:
        rep.ok(f"canonical Play URL uses verified application id ({app_id})")
    if play.get("listing_public") is not True:
        rep.warn("play_store.listing_public is not true — listing availability UNVERIFIED "
                 "(see docs/seo/play-listing.md)")


def main(argv: list[str]) -> int:
    manifest = load_manifest()
    rep = Report()
    rep.lines.append("Elmtrackr — Technical SEO validation report")
    rep.lines.append("=" * 46)

    for route in manifest["routes"]:
        if route.get("indexable") and route.get("exists") is not False:
            check_page(rep, manifest, route)

    check_sitemap(rep, manifest)
    check_hreflang(rep, manifest)
    check_route_uniqueness(rep, manifest)
    check_play_link_consistency(rep, manifest)

    rep.section("=" * 46)
    rep.lines.append("RESULT: " + ("FAIL" if rep.failed else "PASS"))
    rep.dump()
    return 1 if rep.failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
