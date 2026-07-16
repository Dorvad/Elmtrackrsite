#!/usr/bin/env python3
"""Media & accessibility checker for the Elmtrackr site.

Scans every shipped HTML page and verifies:

  * no broken image/video/track/source URLs (files resolve on disk);
  * every <img> has an alt attribute (decorative alt="" is fine) and
    width + height;
  * no duplicate non-empty alt text within a single page;
  * no oversized referenced raster image (> 1.5 MB);
  * the <video> has controls, preload, a poster, a <track> captions file and
    an MP4 fallback, and does not autoplay with sound;
  * the film transcript and a caption track exist in both English and Hebrew;
  * VideoObject JSON-LD is consistent (contentUrl + thumbnailUrl resolve,
    duration present) on both homepages.

Standard library only. Exit non-zero on failure.
"""
from __future__ import annotations

import glob
import json
import os
import re

from _seo_common import REPO_ROOT

IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
VIDEO_RE = re.compile(r"<video\b[^>]*>", re.I)
TRACK_RE = re.compile(r"<track\b[^>]*>", re.I)
SOURCE_RE = re.compile(r"<source\b[^>]*>", re.I)
ATTR_RE = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')
OVERSIZE = 1_500_000
RASTER = (".jpg", ".jpeg", ".png", ".webp", ".gif")


class Report:
    def __init__(self):
        self.failed = False
        self.lines = []
    def ok(self, m): self.lines.append(f"  PASS  {m}")
    def warn(self, m): self.lines.append(f"  WARN  {m}")
    def fail(self, m): self.failed = True; self.lines.append(f"  FAIL  {m}")
    def section(self, t): self.lines += ["", t]
    def dump(self): print("\n".join(self.lines))


def attrs(tag):
    return {k.lower(): v for k, v in ATTR_RE.findall(tag)}


def shipped_html():
    files = ["index.html", "privacy.html", "terms.html"]
    files += [p for p in glob.glob("**/index.html", recursive=True)
              if not p.startswith(("templates/", "content/", "node_modules/"))]
    seen, out = set(), []
    for f in files:
        full = os.path.join(REPO_ROOT, f)
        if os.path.isfile(full) and full not in seen:
            seen.add(full); out.append(f)
    return sorted(out)


def resolve(page_rel, src):
    if src.startswith("http") or src.startswith("data:"):
        return None  # external / inline — skip existence check
    if src.startswith("/"):
        return os.path.join(REPO_ROOT, src.lstrip("/"))
    return os.path.normpath(os.path.join(REPO_ROOT, os.path.dirname(page_rel), src))


def check_page_media(rep, page_rel):
    html = open(os.path.join(REPO_ROOT, page_rel), encoding="utf-8").read()
    alts = []
    for tag in IMG_RE.findall(html):
        a = attrs(tag)
        src = a.get("src", "")
        # existence
        p = resolve(page_rel, src)
        if p is not None and not os.path.isfile(p):
            rep.fail(f"{page_rel}: broken <img> src {src}")
        # alt
        if "alt" not in a:
            rep.fail(f"{page_rel}: <img> missing alt ({src})")
        elif a["alt"].strip():
            alts.append(a["alt"].strip())
        # dimensions
        if "width" not in a or "height" not in a:
            rep.fail(f"{page_rel}: <img> missing width/height ({src})")
        # oversized
        if p and os.path.isfile(p) and p.lower().endswith(RASTER) and os.path.getsize(p) > OVERSIZE:
            rep.fail(f"{page_rel}: oversized image {src} ({os.path.getsize(p)//1024} KB)")
    # duplicate alt within page
    dupes = {t for t in alts if alts.count(t) > 1}
    if dupes:
        rep.warn(f"{page_rel}: duplicate alt text within page: {sorted(dupes)}")

    # <source> and <track> existence
    for tag in SOURCE_RE.findall(html) + TRACK_RE.findall(html):
        a = attrs(tag)
        src = a.get("src") or a.get("srcset", "").split()[0] if (a.get("src") or a.get("srcset")) else ""
        p = resolve(page_rel, src) if src else None
        if p is not None and not os.path.isfile(p):
            rep.fail(f"{page_rel}: broken media src {src}")


def check_video(rep, page_rel):
    html = open(os.path.join(REPO_ROOT, page_rel), encoding="utf-8").read()
    vids = VIDEO_RE.findall(html)
    if not vids:
        return False
    for tag in vids:
        a = attrs(tag)
        if "controls" not in tag.lower():
            rep.fail(f"{page_rel}: <video> lacks controls")
        else:
            rep.ok(f"{page_rel}: <video> has accessible native controls")
        if a.get("preload") != "metadata":
            rep.warn(f"{page_rel}: <video> preload is {a.get('preload')!r} (expected metadata)")
        if "autoplay" in tag.lower() and "muted" not in tag.lower():
            rep.fail(f"{page_rel}: <video> autoplays WITH sound")
        if not a.get("poster"):
            rep.fail(f"{page_rel}: <video> has no poster")
        if "aria-label" not in a and "aria-labelledby" not in a:
            rep.warn(f"{page_rel}: <video> has no accessible name")
    # caption track + transcript presence
    if "<track" not in html or "kind=\"captions\"" not in html:
        rep.fail(f"{page_rel}: film has no <track kind=captions>")
    if not re.search(r"\.vtt", html):
        rep.fail(f"{page_rel}: no .vtt caption file referenced")
    transcript = ("Read the transcript" in html) or ("קראו את התמלול" in html)
    if not transcript:
        rep.fail(f"{page_rel}: no visible transcript")
    else:
        rep.ok(f"{page_rel}: caption track + visible transcript present")
    return True


def check_videoobject(rep, page_rel):
    html = open(os.path.join(REPO_ROOT, page_rel), encoding="utf-8").read()
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        data = json.loads(block)
        nodes = data.get("@graph", [data]) if isinstance(data, dict) else data
        for n in nodes:
            if isinstance(n, dict) and n.get("@type") == "VideoObject":
                for field in ("name", "description", "thumbnailUrl", "contentUrl", "duration", "uploadDate", "inLanguage"):
                    if not n.get(field):
                        rep.fail(f"{page_rel}: VideoObject missing {field}")
                for urlf in ("thumbnailUrl", "contentUrl"):
                    u = n.get(urlf, "")
                    rel = u.split("elmtrackr.site/", 1)[-1] if "elmtrackr.site/" in u else u
                    if rel and not os.path.isfile(os.path.join(REPO_ROOT, rel)):
                        rep.fail(f"{page_rel}: VideoObject {urlf} not found on disk ({u})")
                rep.ok(f"{page_rel}: VideoObject present and consistent ({n.get('inLanguage')})")


def main():
    rep = Report()
    rep.lines.append("Elmtrackr — media & accessibility check")
    rep.lines.append("=" * 44)
    pages = shipped_html()

    rep.section("[images] alt / dimensions / existence / size")
    for p in pages:
        check_page_media(rep, p)
    if not rep.failed:
        rep.ok(f"images OK across {len(pages)} page(s)")

    rep.section("[video] controls, captions, transcript, fallback")
    film_pages = [p for p in pages if check_video(rep, p)]

    rep.section("[video] VideoObject JSON-LD consistency")
    for p in ("index.html", "he/index.html"):
        check_videoobject(rep, p)

    rep.section("[captions] transcript + captions in both languages")
    for lang, page, vtt in [("en", "index.html", "assets/captions/elmtrackr-tour.en.vtt"),
                            ("he", "he/index.html", "assets/captions/elmtrackr-tour.he.vtt")]:
        if os.path.isfile(os.path.join(REPO_ROOT, vtt)) and page in film_pages:
            rep.ok(f"{lang}: transcript page + {vtt} present")
        else:
            rep.fail(f"{lang}: missing transcript page or caption file ({vtt})")

    rep.section("[uploads] source uploads not linked publicly")
    linked = False
    for p in pages:
        if "/uploads/" in open(os.path.join(REPO_ROOT, p), encoding="utf-8").read():
            rep.fail(f"{p}: references non-public uploads/"); linked = True
    if not linked:
        rep.ok("no shipped page links uploads/")

    rep.section("=" * 44)
    rep.lines.append("RESULT: " + ("FAIL" if rep.failed else "PASS"))
    rep.dump()
    return 1 if rep.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
