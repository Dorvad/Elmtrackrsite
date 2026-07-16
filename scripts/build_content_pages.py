#!/usr/bin/env python3
"""Static content-page generator for the Elmtrackr product-information site.

Renders page content from ``content/pages/*.json`` (English) and
``content/pages/he/*.json`` (Hebrew) into route directories using the shared
templates in ``templates/`` and the shared stylesheet
``assets/content-pages.css``.

English pages are written to ``<slug>/index.html`` and Hebrew pages to
``he/<slug>/index.html``. For every slug the two locales are treated as a
translation pair: each page canonicalises to itself and carries reciprocal
``hreflang`` (``en`` / ``he`` / ``x-default``) plus an accessible language
switcher that points at the equivalent page in the other language.

No client-side framework is required to render the output, and only Python's
standard library is used. The Play Store URL and site URL come from
``scripts/seo_manifest.json`` (single source of truth). Output is
deterministic.

Usage:
    python3 scripts/build_content_pages.py            # write pages
    python3 scripts/build_content_pages.py --check     # fail if output is stale
"""
from __future__ import annotations

import html
import json
import os
import re
import sys

from _seo_common import REPO_ROOT, load_manifest

CONTENT_DIR = os.path.join(REPO_ROOT, "content", "pages")
HE_CONTENT_DIR = os.path.join(CONTENT_DIR, "he")
TEMPLATE_DIR = os.path.join(REPO_ROOT, "templates")

DEFAULT_OG = {
    "src": "/assets/render-widgets-tablet.jpg",
    "w": 1400,
    "h": 933,
    "alt": "Elmtrackr home-screen widgets showing hours and estimated pay on an Android tablet.",
}

# Per-locale UI strings and routing. Body content comes from the JSON files;
# these are the chrome strings the builder controls.
LOCALES = {
    "en": {
        "lang": "en", "dir": "ltr", "og_locale": "en", "prefix": "",
        "header": "header.html", "footer": "footer.html",
        "skip": "Skip to main content",
        "reviewed": "Last reviewed",
        "limitations": "Limitations",
        "faq_heading": "Frequently asked questions",
        "related": "Related pages",
        "cta_primary": "Get it on Google Play",
        "cta_back": "Back to the homepage",
        "cta_aria": "Get Elmtrackr on Google Play (opens in a new tab)",
        "breadcrumb_aria": "Breadcrumb",
        "related_aria": "Related pages",
        "switch_label": "עברית",
        "switch_aria": "View this page in Hebrew",
        "home_label": "Home",
    },
    "he": {
        "lang": "he", "dir": "rtl", "og_locale": "he", "prefix": "/he",
        "header": "header.he.html", "footer": "footer.he.html",
        "skip": "דילוג לתוכן הראשי",
        "reviewed": "עודכן לאחרונה",
        "limitations": "מגבלות",
        "faq_heading": "שאלות נפוצות",
        "related": "עמודים קשורים",
        "cta_primary": "הורדה ב־Google Play",
        "cta_back": "חזרה לדף הבית",
        "cta_aria": "הורדת Elmtrackr מ־Google Play (נפתח בלשונית חדשה)",
        "breadcrumb_aria": "פירורי לחם",
        "related_aria": "עמודים קשורים",
        "switch_label": "English",
        "switch_aria": "צפייה בעמוד זה באנגלית",
        "home_label": "בית",
    },
}


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def read_template(name: str) -> str:
    with open(os.path.join(TEMPLATE_DIR, name), encoding="utf-8") as fh:
        return fh.read()


# ── block renderers ─────────────────────────────────────────────────────────

def render_blocks(blocks: list) -> str:
    out = []
    for b in blocks:
        if "p" in b:
            out.append(f'<p class="cp-p">{b["p"]}</p>')
        elif "h3" in b:
            out.append(f'<h3 class="cp-h3">{esc(b["h3"])}</h3>')
        elif "ul" in b:
            items = "".join(f'<li class="cp-li">{it}</li>' for it in b["ul"])
            out.append(f'<ul class="cp-ul">{items}</ul>')
        elif "note" in b:
            n = b["note"]
            out.append(
                '<aside class="cp-note">'
                f'<span class="cp-note-label">{esc(n["label"])}</span>'
                f'<p>{n["html"]}</p></aside>'
            )
        elif "example" in b:
            out.append(render_example(b["example"]))
        elif "img" in b:
            out.append(render_figure(b["img"]))
        else:
            raise ValueError(f"unknown block type: {list(b)}")
    return "\n".join(out)


def render_example(ex: dict) -> str:
    # Row cells are trusted, author-written HTML (they may carry <span class="ltr">
    # around Latin/number runs so they stay left-to-right inside RTL pages).
    rows = "".join(
        f'<div class="cp-ex-row"><span>{d}</span><span>{v}</span></div>'
        for d, v in ex.get("rows", [])
    )
    parts = ['<div class="cp-example">']
    parts.append(f'<p class="cp-ex-title">{ex.get("title", "Example")}</p>')
    if ex.get("intro"):
        parts.append(f'<p class="cp-ex-intro">{ex["intro"]}</p>')
    parts.append(f'<div class="cp-ex-rows">{rows}</div>')
    if ex.get("total"):
        parts.append('<div class="cp-ex-divider"></div>')
        tl, tv = ex["total"]
        parts.append(f'<div class="cp-ex-total"><span>{tl}</span><span>{tv}</span></div>')
    if ex.get("note"):
        parts.append(f'<p class="cp-ex-note">{ex["note"]}</p>')
    parts.append("</div>")
    return "".join(parts)


def render_figure(img: dict) -> str:
    cap = f'<figcaption>{esc(img["caption"])}</figcaption>' if img.get("caption") else ""
    return (
        '<figure class="cp-figure">'
        f'<span class="cp-figimg"><img src="{esc(img["src"])}" alt="{esc(img["alt"])}" '
        f'width="{img["w"]}" height="{img["h"]}" loading="lazy" decoding="async"></span>'
        f"{cap}</figure>"
    )


def render_sections(sections: list) -> str:
    out = []
    for s in sections:
        sid = f' id="{esc(s["id"])}"' if s.get("id") else ""
        out.append(
            f'<section class="cp-section">'
            f'<h2 class="cp-h2"{sid}>{esc(s["h2"])}</h2>'
            f"{render_blocks(s['blocks'])}</section>"
        )
    return "\n".join(out)


def render_limitations(lim: dict, strings: dict) -> str:
    if not lim:
        return ""
    intro = f'<p class="cp-p">{lim["intro"]}</p>' if lim.get("intro") else ""
    items = "".join(f'<li class="cp-li">{it}</li>' for it in lim.get("items", []))
    return (
        '<section class="cp-limits" aria-labelledby="limitations">'
        f'<h2 class="cp-h2" id="limitations">{esc(strings["limitations"])}</h2>'
        f'{intro}<ul class="cp-ul">{items}</ul></section>'
    )


def render_faq(faq: list, strings: dict) -> str:
    if not faq:
        return ""
    items = []
    for qa in faq:
        items.append(
            "<details>"
            f'<summary>{esc(qa["q"])}</summary>'
            f'<p class="cp-faq-a">{qa["a"]}</p>'
            "</details>"
        )
    return (
        '<section class="cp-faq" aria-labelledby="faq">'
        f'<h2 class="cp-h2" id="faq">{esc(strings["faq_heading"])}</h2>'
        f'<div class="cp-faq-list">{"".join(items)}</div></section>'
    )


def render_related(related: list, strings: dict) -> str:
    if not related:
        return ""
    cards = []
    for r in related:
        cards.append(
            f'<a class="cp-related-card" href="{esc(r["href"])}">'
            f'<h3>{esc(r["label"])}</h3><p>{esc(r["desc"])}</p></a>'
        )
    return (
        '<section class="cp-related" aria-labelledby="related">'
        f'<h2 class="cp-h2" id="related">{esc(strings["related"])}</h2>'
        f'<div class="cp-related-grid">{"".join(cards)}</div></section>'
    )


def render_cta(cta: dict, play_url: str, strings: dict) -> str:
    return (
        '<section class="cp-cta">'
        f'<h2>{esc(cta["h2"])}</h2><p>{esc(cta["p"])}</p>'
        '<div class="cp-cta-actions">'
        f'<a class="cp-btn-primary" href="{esc(play_url)}" target="_blank" rel="noopener" '
        f'aria-label="{esc(strings["cta_aria"])}">{esc(strings["cta_primary"])}</a>'
        f'<a class="cp-btn-secondary" href="{strings["home_href"]}">{esc(strings["cta_back"])}</a>'
        "</div></section>"
    )


def render_breadcrumbs(page: dict, strings: dict) -> str:
    return (
        f'<nav class="cp-breadcrumbs" aria-label="{esc(strings["breadcrumb_aria"])}"><ol>'
        f'<li><a href="{strings["home_href"]}">{esc(strings["home_label"])}</a></li>'
        f'<li aria-current="page">{esc(page["breadcrumb"])}</li>'
        "</ol></nav>"
    )


# ── JSON-LD ──────────────────────────────────────────────────────────────────

def build_jsonld(page, canonical, site_url, og, loc, strings) -> str:
    home_url = site_url + ("/he/" if loc == "he" else "/")
    graph = [
        {
            "@type": "WebPage",
            "@id": canonical + "#webpage",
            "url": canonical,
            "name": page.get("h1") or page["title"],
            "description": page["description"],
            "inLanguage": loc,
            "isPartOf": {"@id": site_url + "/#website"},
            "publisher": {"@id": site_url + "/#organization"},
            "datePublished": page["reviewed"],
            "dateModified": page["reviewed"],
            "primaryImageOfPage": {
                "@type": "ImageObject",
                "url": site_url + og["src"] if og["src"].startswith("/") else og["src"],
                "width": og["w"],
                "height": og["h"],
            },
            "breadcrumb": {"@id": canonical + "#breadcrumb"},
        },
        {
            "@type": "BreadcrumbList",
            "@id": canonical + "#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": strings["home_label"], "item": home_url},
                {"@type": "ListItem", "position": 2, "name": page["breadcrumb"], "item": canonical},
            ],
        },
    ]
    if page.get("faq"):
        graph.append({
            "@type": "FAQPage",
            "@id": canonical + "#faq",
            "inLanguage": loc,
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": strip_tags(qa["q"]),
                    "acceptedAnswer": {"@type": "Answer", "text": strip_tags(qa["a"])},
                }
                for qa in page["faq"]
            ],
        })
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    return s.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#39;", "'").strip()


# ── page assembly ─────────────────────────────────────────────────────────────

def build_article(page, play_url, og, strings) -> str:
    parts = []
    if page.get("hero_eyebrow"):
        parts.append(f'<p class="cp-eyebrow">{esc(page["hero_eyebrow"])}</p>')
    parts.append(f'<h1 class="cp-h1">{esc(page["h1"])}</h1>')
    parts.append(f'<p class="cp-lead">{page["lead"]}</p>')
    parts.append(
        f'<p class="cp-reviewed">{esc(strings["reviewed"])}: '
        f'<span class="ltr">{esc(page["reviewed"])}</span></p>'
    )
    if page.get("image"):
        parts.append(render_figure(page["image"]))
    parts.append(render_sections(page["sections"]))
    parts.append(render_limitations(page.get("limitations"), strings))
    parts.append(render_faq(page.get("faq"), strings))
    parts.append(render_related(page.get("related"), strings))
    parts.append(render_cta(page["cta"], play_url, strings))
    return "\n".join(p for p in parts if p)


def hreflang_block(en_url, he_url) -> str:
    return (
        f'<link rel="alternate" hreflang="en" href="{en_url}">\n'
        f'<link rel="alternate" hreflang="he" href="{he_url}">\n'
        f'<link rel="alternate" hreflang="x-default" href="{en_url}">'
    )


def lang_switch_anchor(target_url, loc) -> str:
    # anchor pointing at the equivalent page in the other language
    other = "en" if loc == "he" else "he"
    strings = LOCALES[loc]
    return (
        f'<a class="cp-lang-switch" href="{target_url}" hreflang="{other}" lang="{other}" '
        f'aria-label="{esc(strings["switch_aria"])}">{esc(strings["switch_label"])}</a>'
    )


def render_page(page, manifest, page_tpl, header_raw, footer, loc):
    site_url = manifest["site_url"].rstrip("/")
    play_url = manifest["play_store"]["url"]
    slug = page["slug"]
    strings = dict(LOCALES[loc])

    en_canonical = f"{site_url}/{slug}/"
    he_canonical = f"{site_url}/he/{slug}/"
    canonical = he_canonical if loc == "he" else en_canonical
    counterpart = en_canonical if loc == "he" else he_canonical
    strings["home_href"] = "/he/" if loc == "he" else "/"

    og = dict(DEFAULT_OG)
    if page.get("og_image"):
        og.update(page["og_image"])
    og_abs = site_url + og["src"] if og["src"].startswith("/") else og["src"]

    article = build_article(page, play_url, og, strings)
    jsonld = build_jsonld(page, canonical, site_url, og, loc, strings)
    header = header_raw.replace("{{PLAY_URL}}", play_url).replace(
        "{{LANG_SWITCH}}", lang_switch_anchor(counterpart, loc))

    subs = {
        "{{LANG}}": strings["lang"],
        "{{DIR}}": strings["dir"],
        "{{OG_LOCALE}}": strings["og_locale"],
        "{{SKIP}}": esc(strings["skip"]),
        "{{TITLE}}": esc(page["title"]),
        "{{DESCRIPTION}}": esc(page["description"]),
        "{{CANONICAL}}": canonical,
        "{{OG_TITLE}}": esc(page.get("og_title") or page["title"]),
        "{{OG_IMAGE}}": og_abs,
        "{{OG_IMAGE_W}}": str(og["w"]),
        "{{OG_IMAGE_H}}": str(og["h"]),
        "{{OG_IMAGE_ALT}}": esc(og["alt"]),
        "{{HREFLANG}}": hreflang_block(en_canonical, he_canonical),
        "{{JSONLD}}": jsonld,
        "{{HEADER}}": header,
        "{{FOOTER}}": footer,
        "{{BREADCRUMBS}}": render_breadcrumbs(page, strings),
        "{{ARTICLE}}": article,
    }
    out = page_tpl
    for k, v in subs.items():
        out = out.replace(k, v)
    if "{{" in out:
        leftover = out[out.index("{{"): out.index("{{") + 40]
        raise ValueError(f"{loc}/{slug}: unreplaced template token near {leftover!r}")
    return out


def load_pages(directory):
    pages = []
    for fn in sorted(os.listdir(directory)):
        if fn.endswith(".json"):
            with open(os.path.join(directory, fn), encoding="utf-8") as fh:
                pages.append(json.load(fh))
    return pages


def main(argv):
    check_only = "--check" in argv[1:]
    manifest = load_manifest()
    page_tpl = read_template("page.html")

    jobs = []  # (loc, page, out_path)
    for loc in ("en", "he"):
        directory = CONTENT_DIR if loc == "en" else HE_CONTENT_DIR
        header_raw = read_template(LOCALES[loc]["header"])
        footer = read_template(LOCALES[loc]["footer"])
        for page in load_pages(directory):
            rendered = render_page(page, manifest, page_tpl, header_raw, footer, loc)
            raw = rendered.split('<script type="application/ld+json">', 1)[1].split("</script>", 1)[0]
            json.loads(raw)  # validate embedded JSON-LD
            sub = "" if loc == "en" else "he/"
            out_path = os.path.join(REPO_ROOT, f"{sub}{page['slug']}", "index.html")
            jobs.append((f"{sub}{page['slug']}", out_path, rendered))

    stale = []
    for name, out_path, rendered in jobs:
        if check_only:
            current = ""
            if os.path.isfile(out_path):
                with open(out_path, encoding="utf-8") as fh:
                    current = fh.read()
            if current != rendered:
                stale.append(name)
        else:
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as fh:
                fh.write(rendered)
            print(f"  wrote {name}/index.html")

    if check_only:
        if stale:
            print("FAIL  stale content pages: " + ", ".join(stale))
            print("      run: python3 scripts/build_content_pages.py")
            return 1
        print(f"PASS  {len(jobs)} content page(s) up to date")
        return 0

    print(f"Built {len(jobs)} content page(s) across en + he.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
