#!/usr/bin/env python3
"""Locale-pair checker for the Elmtrackr en/he site.

Verifies, from the manifest and the generated HTML, that:

  * every English indexable page has a Hebrew equivalent, and vice versa;
  * reciprocal hreflang is present and correct on both members of a pair
    (en + he + x-default, all pointing at the right URLs);
  * every canonical is self-referencing;
  * no Hebrew page is missing ``dir="rtl"`` (or ``lang="he"``);
  * no page mixes English metadata with Hebrew body content (or vice versa);
  * every language-switch link points at a page that actually exists.

Exit code is non-zero if any check fails. Standard library only.
"""
from __future__ import annotations

import os
import re
import sys

from _seo_common import REPO_ROOT, load_manifest

HEBREW = re.compile(r"[֐-׿]")
ALT_RE = re.compile(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)">', re.I)
HTML_TAG_RE = re.compile(r"<html\b([^>]*)>", re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
CANON_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)">', re.I)
SWITCH_RE = re.compile(r'<a\b[^>]*\bclass="cp-lang-switch"[^>]*\bhref="([^"]+)"', re.I)
# homepage switcher (hand-authored) — an <a> whose visible text is English/עברית
HOME_SWITCH_RE = re.compile(r'<a\s+href="(/he/|/)"[^>]*hreflang="(?:he|en)"[^>]*>', re.I)


class Report:
    def __init__(self):
        self.failed = False
        self.lines = []
    def ok(self, m): self.lines.append(f"  PASS  {m}")
    def fail(self, m): self.failed = True; self.lines.append(f"  FAIL  {m}")
    def section(self, t): self.lines += ["", t]
    def dump(self): print("\n".join(self.lines))


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def url_to_file(manifest, url):
    for r in manifest["routes"]:
        if r["canonical"] == url or r["canonical"].rstrip("/") == url.rstrip("/"):
            return os.path.join(REPO_ROOT, r["file"])
    # fall back to path mapping for bare site urls
    site = manifest["site_url"].rstrip("/")
    path = url[len(site):] if url.startswith(site) else url
    if path in ("/", ""):
        return os.path.join(REPO_ROOT, "index.html")
    if path == "/he/":
        return os.path.join(REPO_ROOT, "he", "index.html")
    return os.path.join(REPO_ROOT, path.strip("/"), "index.html")


def indexable_pairs(manifest):
    """group -> {lang: route} for indexable, existing, non-redirect routes."""
    groups = {}
    for r in manifest["routes"]:
        if not r.get("indexable") or r.get("exists") is False or r.get("redirect"):
            continue
        groups.setdefault(r["hreflang_group"], {})[r["language"]] = r
    return groups


def main():
    manifest = load_manifest()
    site = manifest["site_url"].rstrip("/")
    rep = Report()
    rep.lines.append("Elmtrackr — locale-pair check")
    rep.lines.append("=" * 40)

    groups = indexable_pairs(manifest)

    # 1. every indexable page has both en and he
    rep.section("[pairs] every indexable page has an en + he equivalent")
    for group, langs in sorted(groups.items()):
        if "en" in langs and "he" in langs:
            rep.ok(f"{group}: en + he present")
        elif "en" in langs:
            rep.fail(f"{group}: has English but no Hebrew equivalent")
        else:
            rep.fail(f"{group}: has Hebrew but no English equivalent")

    # 2/3/4/5. per-page checks
    rep.section("[pages] hreflang reciprocity, self-canonical, dir/lang, no mixed-language metadata")
    for group, langs in sorted(groups.items()):
        en = langs.get("en")
        he = langs.get("he")
        expected = {}
        if en:
            expected["en"] = en["canonical"]
            expected["x-default"] = en["canonical"]
        if he:
            expected["he"] = he["canonical"]
        for lang, route in langs.items():
            path = os.path.join(REPO_ROOT, route["file"])
            if not os.path.isfile(path):
                rep.fail(f"{route['path']}: file missing ({route['file']})")
                continue
            html = read(path)

            # hreflang reciprocity
            alts = {k.lower(): v for k, v in ALT_RE.findall(html)}
            if alts == expected:
                rep.ok(f"{route['path']}: hreflang reciprocal ({', '.join(sorted(alts))})")
            else:
                rep.fail(f"{route['path']}: hreflang {alts} != expected {expected}")

            # self-canonical
            cm = CANON_RE.search(html)
            if not cm:
                rep.fail(f"{route['path']}: no canonical")
            elif cm.group(1).rstrip("/") != route["canonical"].rstrip("/"):
                rep.fail(f"{route['path']}: canonical {cm.group(1)} not self ({route['canonical']})")

            # dir/lang + metadata/body language consistency
            attrs = HTML_TAG_RE.search(html)
            attrs = attrs.group(1) if attrs else ""
            title = TITLE_RE.search(html)
            title = title.group(1) if title else ""
            title_he = bool(HEBREW.search(title))
            body = html.split("<body", 1)[-1]
            # sample visible body text: strip tags/scripts/styles
            vis = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S | re.I)
            vis = re.sub(r"<[^>]+>", " ", vis)
            body_he = bool(HEBREW.search(vis))

            if lang == "he":
                if 'dir="rtl"' in attrs:
                    rep.ok(f"{route['path']}: dir=rtl present")
                else:
                    rep.fail(f"{route['path']}: Hebrew page missing dir=\"rtl\"")
                if 'lang="he"' not in attrs:
                    rep.fail(f"{route['path']}: Hebrew page missing lang=\"he\"")
                if not title_he:
                    rep.fail(f"{route['path']}: Hebrew page has non-Hebrew <title> (mixed metadata)")
                if not body_he:
                    rep.fail(f"{route['path']}: Hebrew page body has no Hebrew text (mixed content)")
            else:
                if 'lang="en"' not in attrs:
                    rep.fail(f"{route['path']}: English page missing lang=\"en\"")
                if title_he:
                    rep.fail(f"{route['path']}: English page has Hebrew <title> (mixed metadata)")

    # 6. language-switch links resolve to existing pages
    rep.section("[switch] every language-switch link targets an existing page")
    for group, langs in sorted(groups.items()):
        for lang, route in langs.items():
            path = os.path.join(REPO_ROOT, route["file"])
            if not os.path.isfile(path):
                continue
            html = read(path)
            targets = SWITCH_RE.findall(html)
            if not targets:
                # homepage uses a hand-authored switcher
                targets = [m.group(1) for m in HOME_SWITCH_RE.finditer(html)]
            if not targets:
                rep.fail(f"{route['path']}: no language switcher found")
                continue
            other = "en" if lang == "he" else "he"
            want = langs_other = groups[group].get(other)
            for t in targets:
                turl = t if t.startswith("http") else site + t
                tf = url_to_file(manifest, turl)
                if os.path.isfile(tf):
                    rep.ok(f"{route['path']}: switch -> {t} exists")
                else:
                    rep.fail(f"{route['path']}: switch target missing ({t})")
                if want and turl.rstrip("/") != want["canonical"].rstrip("/"):
                    rep.fail(f"{route['path']}: switch -> {t} is not the {other} equivalent ({want['canonical']})")

    rep.section("=" * 40)
    rep.lines.append("RESULT: " + ("FAIL" if rep.failed else "PASS"))
    rep.dump()
    return 1 if rep.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
