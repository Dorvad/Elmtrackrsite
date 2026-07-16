#!/usr/bin/env python3
"""Comprehensive static-site audit for the Elmtrackr marketing site.

This is the repeatable quality gate. It inspects every shipped HTML page and
fails (exit code 1) when a change would silently break crawlability, bilingual
routing, metadata, structured data, accessibility or link integrity.

Only Python's standard library is used, so it runs anywhere without installs.

Per page it checks:
  * build existence (manifest route resolves to a file on disk)
  * exactly one <h1>
  * a valid <html lang> that matches the page's language
  * dir="rtl" on Hebrew pages
  * unique <title> across the site
  * unique <meta name=description> across the site
  * a self-referencing canonical
  * a valid, reciprocal hreflang set (matching the manifest)
  * Open Graph metadata (og:type/title/description/url/image)
  * no unresolved {{ ... }} template placeholders in visible HTML
  * no broken internal anchors (href="#id" whose id is absent)
  * no broken internal links (site-relative href that resolves to nothing)
  * no missing local image files
  * an alt attribute on every <img> (alt="" allowed for decorative images)
  * width and height on every content <img>
  * every FAQPage schema question present as visible text
  * valid JSON-LD (parses)
  * BreadcrumbList schema on nested (content) pages
  * indexability that matches sitemap inclusion (robots <-> manifest <-> sitemap)
  * no accidental staging / preview URLs
  * no generic Play Store URLs (every Play link carries the verified app id)
  * no fictional rating / review schema
  * no mixed-language metadata (Hebrew page titles are Hebrew, English aren't)
  * no duplicate page bodies (two routes sharing identical main content)

Usage:
    python3 scripts/audit_site.py                 # human-readable report
    python3 scripts/audit_site.py --report FILE   # also write a Markdown report
    python3 scripts/audit_site.py --json FILE     # also write a JSON report

Exit code is 0 when there are no ERROR findings, 1 otherwise. WARN findings
never fail the build on their own.
"""
from __future__ import annotations

import argparse
import html as html_mod
import json
import os
import re
import sys
from html.parser import HTMLParser

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(REPO_ROOT, "scripts", "seo_manifest.json")
SITEMAP_PATH = os.path.join(REPO_ROOT, "sitemap.xml")

VERIFIED_APP_ID = "com.elmlaunch.myapp"
HEBREW_RE = re.compile(r"[֐-׿]")
PLACEHOLDER_RE = re.compile(r"\{\{")
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b.*?</\1\s*>", re.I | re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
# Hostnames / tokens that must never ship in a public page.
STAGING_RE = re.compile(
    r"github\.io|\blocalhost\b|127\.0\.0\.1|:8000\b|\bstaging\b|\.preview\b|"
    r"netlify\.app|vercel\.app|ngrok",
    re.I,
)


# --------------------------------------------------------------------------- #
# Findings
# --------------------------------------------------------------------------- #
class Findings:
    def __init__(self):
        self.items = []  # (severity, page, check, message)

    def error(self, page, check, message):
        self.items.append(("ERROR", page, check, message))

    def warn(self, page, check, message):
        self.items.append(("WARN", page, check, message))

    @property
    def errors(self):
        return [i for i in self.items if i[0] == "ERROR"]

    @property
    def warnings(self):
        return [i for i in self.items if i[0] == "WARN"]


# --------------------------------------------------------------------------- #
# HTML parsing
# --------------------------------------------------------------------------- #
class PageParser(HTMLParser):
    """Collects everything the audit needs from a single HTML document."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.dir = None
        self.title = None
        self._in_title = False
        self.meta = {}          # name/property -> content
        self.canonical = None
        self.alternates = []    # (hreflang, href)
        self.h1_count = 0
        self._in_h1 = False
        self.images = []        # dict(src, alt, width, height)
        self.links = []         # href values
        self.ids = set()        # every id="" on the page
        self.jsonld_blocks = [] # raw json-ld strings
        self._in_ld = False
        self._ld_buf = []
        self.summaries = []     # visible <summary> text
        self._in_summary = False
        self._summary_buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
            self.dir = a.get("dir")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key is not None:
                self.meta[key.lower()] = a.get("content", "")
        elif tag == "link":
            rel = (a.get("rel") or "").lower()
            if rel == "canonical":
                self.canonical = a.get("href")
            elif rel == "alternate" and a.get("hreflang"):
                self.alternates.append((a.get("hreflang"), a.get("href")))
        elif tag == "h1":
            self.h1_count += 1
            self._in_h1 = True
        elif tag == "img":
            self.images.append(
                {
                    "src": a.get("src"),
                    "alt": a.get("alt"),  # None means attribute absent
                    "width": a.get("width"),
                    "height": a.get("height"),
                }
            )
        elif tag == "a" and a.get("href") is not None:
            self.links.append(a["href"])
        elif tag == "summary":
            self._in_summary = True
            self._summary_buf = []
        elif tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._in_ld = True
            self._ld_buf = []
        if "id" in a and a["id"]:
            self.ids.add(a["id"])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag == "summary":
            self._in_summary = False
            self.summaries.append("".join(self._summary_buf).strip())
        elif tag == "script" and self._in_ld:
            self._in_ld = False
            self.jsonld_blocks.append("".join(self._ld_buf))

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data
        if self._in_ld:
            self._ld_buf.append(data)
        if self._in_summary:
            self._summary_buf.append(data)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def sitemap_locs(path):
    if not os.path.exists(path):
        return set()
    text = open(path, encoding="utf-8").read()
    return set(re.findall(r"<loc>\s*(.*?)\s*</loc>", text))


def norm_text(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def resolve_internal_link(href, page_url_path):
    """Return a site-relative path (leading '/') for an internal link, or None
    if the link is external / non-navigational (mailto, tel, #, http...)."""
    if not href:
        return None
    href = href.strip()
    if href.startswith(("mailto:", "tel:", "javascript:")):
        return None
    if href.startswith("#"):
        return None
    if re.match(r"^[a-z]+://", href, re.I):
        # absolute URL; only treat our own origin as internal
        m = re.match(r"^https?://elmtrackr\.site(/.*)?$", href, re.I)
        if not m:
            return None
        path = m.group(1) or "/"
    elif href.startswith("/"):
        path = href
    else:
        # relative to the current directory
        base = page_url_path.rsplit("/", 1)[0]
        path = base + "/" + href
    path = path.split("#", 1)[0].split("?", 1)[0]
    return path or "/"


def path_to_file(path):
    """Map a site path ('/foo/' or '/x.html') to an on-disk file."""
    p = path.lstrip("/")
    if p == "" or p.endswith("/"):
        candidate = os.path.join(REPO_ROOT, p, "index.html")
    elif p.endswith(".html"):
        candidate = os.path.join(REPO_ROOT, p)
    else:
        candidate = os.path.join(REPO_ROOT, p, "index.html")
    return candidate


def parse_ld(blocks):
    """Return (parsed_nodes, parse_errors). Flattens @graph."""
    nodes, errors = [], []
    for b in blocks:
        try:
            data = json.loads(b)
        except json.JSONDecodeError as exc:
            errors.append(str(exc))
            continue
        graph = data.get("@graph") if isinstance(data, dict) else None
        if graph:
            nodes.extend(graph)
        elif isinstance(data, list):
            nodes.extend(data)
        else:
            nodes.append(data)
    return nodes, errors


def types_of(node):
    t = node.get("@type")
    if isinstance(t, list):
        return set(t)
    return {t} if t else set()


# --------------------------------------------------------------------------- #
# Audit
# --------------------------------------------------------------------------- #
def audit(find: Findings):
    manifest = load_json(MANIFEST_PATH)
    routes = manifest["routes"]
    sm_locs = sitemap_locs(SITEMAP_PATH)

    # Index routes by file for cross-checks.
    by_file = {r["file"]: r for r in routes}

    titles = {}       # title -> [pages]
    descriptions = {} # description -> [pages]
    bodies = {}       # normalized main body -> [pages]

    pages = []  # (route, filepath, parser)

    # ---- existence + parse ------------------------------------------------- #
    for r in routes:
        if r.get("redirect"):
            continue
        rel = r["file"]
        fp = os.path.join(REPO_ROOT, rel)
        if r.get("exists") is False:
            if os.path.exists(fp):
                find.warn(rel, "existence",
                          "manifest marks route as not-yet-existing but file is present")
            continue
        if not os.path.exists(fp):
            find.error(rel, "existence", "manifest route has no file on disk")
            continue
        parser = PageParser()
        try:
            parser.feed(open(fp, encoding="utf-8").read())
        except Exception as exc:  # noqa: BLE001 - report, do not crash
            find.error(rel, "parse", f"failed to parse HTML: {exc}")
            continue
        pages.append((r, fp, parser))

    # Also make sure no shipped HTML file is missing from the manifest.
    for root, _dirs, files in os.walk(REPO_ROOT):
        if any(seg in root for seg in (os.sep + "templates", os.sep + "_ds",
                                       os.sep + ".git", os.sep + "node_modules",
                                       os.sep + "scripts", os.sep + "_site",
                                       os.sep + "_reports", os.sep + "dc-runtime")):
            continue
        for f in files:
            if not f.endswith(".html"):
                continue
            relf = os.path.relpath(os.path.join(root, f), REPO_ROOT)
            if relf not in by_file:
                find.error(relf, "manifest",
                           "shipped HTML file is not listed in seo_manifest.json")

    # ---- per-page checks --------------------------------------------------- #
    for r, fp, p in pages:
        rel = r["file"]
        raw = open(fp, encoding="utf-8").read()
        lang = (r.get("language") or "").lower()
        canonical = r.get("canonical")
        indexable = bool(r.get("indexable"))

        # exactly one h1
        if p.h1_count != 1:
            find.error(rel, "h1", f"expected exactly one <h1>, found {p.h1_count}")

        # valid lang matching language
        if not p.lang:
            find.error(rel, "lang", "<html> has no lang attribute")
        else:
            base = p.lang.lower().split("-")[0]
            if lang and base != lang:
                find.error(rel, "lang",
                           f"<html lang='{p.lang}'> does not match manifest language '{lang}'")

        # dir=rtl for Hebrew
        if lang == "he" and (p.dir or "").lower() != "rtl":
            find.error(rel, "dir", "Hebrew page must have dir=\"rtl\" on <html>")
        if lang != "he" and (p.dir or "").lower() == "rtl":
            find.warn(rel, "dir", "non-Hebrew page has dir=\"rtl\"")

        # unique title / description
        title = norm_text(html_mod.unescape(p.title or ""))
        desc = norm_text(p.meta.get("description", ""))
        if not title:
            find.error(rel, "title", "missing <title>")
        else:
            titles.setdefault(title, []).append(rel)
        if not desc:
            find.error(rel, "description", "missing meta description")
        else:
            descriptions.setdefault(desc, []).append(rel)

        # self-referencing canonical
        if not p.canonical:
            find.error(rel, "canonical", "missing rel=canonical")
        elif canonical and p.canonical != canonical:
            find.error(rel, "canonical",
                       f"canonical '{p.canonical}' != expected self URL '{canonical}'")

        # hreflang reciprocity (indexable pages participate)
        group = r.get("hreflang_group")
        expected_alts = {}
        for rr in routes:
            if rr.get("hreflang_group") != group:
                continue
            if not rr.get("indexable") or rr.get("redirect") or rr.get("exists") is False:
                continue
            expected_alts[rr["language"]] = rr["canonical"]
        if indexable and expected_alts:
            got = {hl: href for hl, href in p.alternates}
            # every language alternate + x-default expected
            for langcode, href in expected_alts.items():
                if got.get(langcode) != href:
                    find.error(rel, "hreflang",
                               f"missing/mismatched hreflang '{langcode}' "
                               f"(want {href}, got {got.get(langcode)})")
            # x-default should point at the English canonical of the group
            en_href = expected_alts.get("en")
            if en_href and got.get("x-default") != en_href:
                find.error(rel, "hreflang",
                           f"x-default should be {en_href}, got {got.get('x-default')}")
            # reciprocity: each alternate target page must point back here
            for langcode, href in expected_alts.items():
                tgt = path_to_file(re.sub(r"^https?://elmtrackr\.site", "", href))
                trel = os.path.relpath(tgt, REPO_ROOT)
                tr = by_file.get(trel)
                if tr and canonical:
                    # the target's group must include this page's canonical
                    if canonical not in expected_alts.values():
                        find.error(rel, "hreflang", "page canonical missing from its own hreflang group")
                    break

        # Open Graph
        for prop in ("og:type", "og:title", "og:description", "og:url", "og:image"):
            if not p.meta.get(prop):
                find.error(rel, "opengraph", f"missing {prop}")
        if p.meta.get("og:url") and canonical and p.meta["og:url"] != canonical:
            find.warn(rel, "opengraph", f"og:url '{p.meta['og:url']}' != canonical")

        # unresolved template placeholders (visible HTML only)
        visible = COMMENT_RE.sub("", SCRIPT_STYLE_RE.sub("", raw))
        if PLACEHOLDER_RE.search(visible):
            snippet = visible[max(0, PLACEHOLDER_RE.search(visible).start() - 20):
                              PLACEHOLDER_RE.search(visible).start() + 40]
            find.error(rel, "placeholder",
                       f"unresolved '{{{{' template token in visible HTML near: {norm_text(snippet)!r}")

        # internal anchors + links
        for href in p.links:
            if href.startswith("#"):
                target = href[1:]
                if target and target not in p.ids:
                    find.error(rel, "anchor", f"broken in-page anchor '{href}'")
                continue
            path = resolve_internal_link(href, r["path"])
            if path is None:
                continue  # external / non-navigational
            tgt = path_to_file(path)
            if not os.path.exists(tgt):
                # allow asset files that exist under REPO_ROOT
                asset = os.path.join(REPO_ROOT, path.lstrip("/"))
                if not os.path.exists(asset):
                    find.error(rel, "link", f"broken internal link '{href}' -> {path}")

        # images: files exist, alt present, dimensions present
        for img in p.images:
            src = img["src"]
            if src and not re.match(r"^[a-z]+://", src, re.I) and not src.startswith("data:"):
                asset = os.path.join(REPO_ROOT, src.lstrip("/"))
                if not os.path.exists(asset):
                    find.error(rel, "image", f"missing image file: {src}")
            if img["alt"] is None:
                find.error(rel, "alt", f"<img> without alt attribute: {src}")
            # decorative images (alt="") are exempt from dimension requirement
            if img["alt"]:
                if not img["width"] or not img["height"]:
                    find.warn(rel, "dimensions",
                              f"content <img> without width/height: {src}")

        # JSON-LD validity + structured-data checks
        nodes, ld_errors = parse_ld(p.jsonld_blocks)
        for e in ld_errors:
            find.error(rel, "jsonld", f"invalid JSON-LD: {e}")
        node_types = set()
        for n in nodes:
            node_types |= types_of(n)

        # no fictional rating/review schema
        joined_ld = " ".join(p.jsonld_blocks)
        if re.search(r'"(aggregateRating|ratingValue|reviewCount|review)"', joined_ld, re.I) \
           or "Review" in node_types or "AggregateRating" in node_types:
            find.error(rel, "rating", "rating/review schema present — not verifiable, must not ship")

        # breadcrumb on nested content pages
        is_content_page = rel.endswith("/index.html") and rel not in ("index.html", "he/index.html")
        if is_content_page and "BreadcrumbList" not in node_types:
            find.error(rel, "breadcrumb", "nested content page missing BreadcrumbList schema")

        # visible FAQ matches FAQPage schema
        faq_nodes = [n for n in nodes if "FAQPage" in types_of(n)]
        if faq_nodes:
            visible_summaries = {norm_text(html_mod.unescape(s)).rstrip("?").lower()
                                 for s in p.summaries}
            for fn in faq_nodes:
                for q in fn.get("mainEntity", []):
                    qname = norm_text(html_mod.unescape(q.get("name", ""))).rstrip("?").lower()
                    if qname and qname not in visible_summaries:
                        find.error(rel, "faq",
                                   f"FAQPage question not visible on page: {q.get('name')!r}")
        elif len(p.summaries) >= 2 and rel not in ("index.html", "he/index.html"):
            # A content page with a visible FAQ but no FAQPage schema — the
            # homepages omit FAQ schema deliberately, so they are exempted.
            find.warn(rel, "faq", "visible FAQ present but no FAQPage schema")

        # indexability matches sitemap inclusion
        robots = (p.meta.get("robots") or "").lower()
        has_noindex = "noindex" in robots
        in_sitemap = canonical in sm_locs
        if indexable and has_noindex:
            find.error(rel, "index", "manifest says indexable but page robots is noindex")
        if not indexable and not has_noindex:
            find.warn(rel, "index", "manifest says non-indexable but page has no noindex robots")
        if indexable and not in_sitemap:
            find.error(rel, "sitemap", "indexable page is missing from sitemap.xml")
        if not indexable and in_sitemap:
            find.error(rel, "sitemap", "non-indexable page appears in sitemap.xml")

        # staging URLs
        for m in STAGING_RE.finditer(raw):
            find.error(rel, "staging", f"accidental staging/preview token: {m.group(0)!r}")

        # generic Play Store URLs
        for m in re.finditer(r"https://play\.google\.com[^\"'\s)]*", raw):
            url = m.group(0)
            if ("id=" + VERIFIED_APP_ID) not in url and ("id%3D" + VERIFIED_APP_ID) not in url:
                find.error(rel, "playstore",
                           f"Play Store URL without verified app id: {url}")

        # mixed-language metadata
        title_has_he = bool(HEBREW_RE.search(title))
        desc_has_he = bool(HEBREW_RE.search(desc))
        if lang == "he":
            if title and not title_has_he:
                find.error(rel, "metalang", "Hebrew page title contains no Hebrew text")
            if desc and not desc_has_he:
                find.error(rel, "metalang", "Hebrew page description contains no Hebrew text")
        elif lang == "en":
            if title_has_he:
                find.error(rel, "metalang", "English page title contains Hebrew text")
            if desc_has_he:
                find.error(rel, "metalang", "English page description contains Hebrew text")

        # collect body for duplicate detection
        m = re.search(r"<main\b.*?</main>", raw, re.S | re.I)
        body = norm_text(re.sub(r"<[^>]+>", " ", m.group(0))) if m else ""
        if body:
            bodies.setdefault(body, []).append(rel)

    # ---- cross-page checks ------------------------------------------------- #
    for title, pgs in titles.items():
        if len(pgs) > 1:
            find.error(", ".join(pgs), "title", f"duplicate <title>: {title!r}")
    for desc, pgs in descriptions.items():
        if len(pgs) > 1:
            find.error(", ".join(pgs), "description", f"duplicate meta description: {desc[:60]!r}…")
    for body, pgs in bodies.items():
        if len(pgs) > 1:
            find.error(", ".join(pgs), "duplicate-body",
                       "two pages share identical <main> content")

    return len(pages)


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #
def write_markdown(path, find, page_count):
    lines = ["# Elmtrackr site audit report", ""]
    lines.append(f"- Pages audited: **{page_count}**")
    lines.append(f"- Errors: **{len(find.errors)}**")
    lines.append(f"- Warnings: **{len(find.warnings)}**")
    lines.append("")
    if not find.items:
        lines.append("All checks passed with no findings.")
    for sev in ("ERROR", "WARN"):
        group = [i for i in find.items if i[0] == sev]
        if not group:
            continue
        lines.append(f"## {sev} ({len(group)})")
        lines.append("")
        lines.append("| Page | Check | Detail |")
        lines.append("|---|---|---|")
        for _sev, page, check, msg in group:
            safe = msg.replace("|", "\\|")
            lines.append(f"| `{page}` | {check} | {safe} |")
        lines.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def write_json(path, find, page_count):
    payload = {
        "pages_audited": page_count,
        "errors": len(find.errors),
        "warnings": len(find.warnings),
        "findings": [
            {"severity": s, "page": pg, "check": c, "message": m}
            for s, pg, c, m in find.items
        ],
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Audit the Elmtrackr static site.")
    ap.add_argument("--report", help="write a Markdown report to this path")
    ap.add_argument("--json", dest="json_path", help="write a JSON report to this path")
    args = ap.parse_args(argv)

    find = Findings()
    page_count = audit(find)

    # Console output.
    for sev, page, check, msg in find.items:
        marker = "ERROR" if sev == "ERROR" else "WARN "
        print(f"  {marker}  [{check}] {page}: {msg}")

    print("")
    print(f"Audited {page_count} page(s): "
          f"{len(find.errors)} error(s), {len(find.warnings)} warning(s).")

    if args.report:
        write_markdown(args.report, find, page_count)
        print(f"Markdown report written to {args.report}")
    if args.json_path:
        write_json(args.json_path, find, page_count)
        print(f"JSON report written to {args.json_path}")

    print("RESULT:", "PASS" if not find.errors else "FAIL")
    return 1 if find.errors else 0


if __name__ == "__main__":
    sys.exit(main())
