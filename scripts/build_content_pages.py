#!/usr/bin/env python3
"""Static content-page generator for the Elmtrackr product-information site.

Reads page content from ``content/pages/*.json`` and renders ordinary static
HTML into route directories (``<slug>/index.html``) using the shared templates
in ``templates/`` and the shared stylesheet ``assets/content-pages.css``.

No client-side framework is required to render the output, and only Python's
standard library is used. The Play Store URL and site URL are read from
``scripts/seo_manifest.json`` so there is a single source of truth.

Output is deterministic: pages are processed in sorted order and no clocks or
random values are used (the visible "reviewed" date comes from the content
file). Generated files are committed and served by the existing Pages workflow.

Usage:
    python3 scripts/build_content_pages.py            # write pages
    python3 scripts/build_content_pages.py --check     # fail if output is stale
"""
from __future__ import annotations

import html
import json
import os
import sys

from _seo_common import REPO_ROOT, load_manifest

CONTENT_DIR = os.path.join(REPO_ROOT, "content", "pages")
TEMPLATE_DIR = os.path.join(REPO_ROOT, "templates")

DEFAULT_OG = {
    "src": "/assets/render-widgets-tablet.jpg",
    "w": 1400,
    "h": 933,
    "alt": "Elmtrackr home-screen widgets showing hours and estimated pay on an Android tablet.",
}


def esc(s: str) -> str:
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
    rows = "".join(
        f'<div class="cp-ex-row"><span>{esc(d)}</span><span>{esc(v)}</span></div>'
        for d, v in ex.get("rows", [])
    )
    parts = ['<div class="cp-example">']
    parts.append(f'<p class="cp-ex-title">{esc(ex.get("title", "Example"))}</p>')
    if ex.get("intro"):
        parts.append(f'<p class="cp-ex-intro">{ex["intro"]}</p>')
    parts.append(f'<div class="cp-ex-rows">{rows}</div>')
    if ex.get("total"):
        parts.append('<div class="cp-ex-divider"></div>')
        tl, tv = ex["total"]
        parts.append(f'<div class="cp-ex-total"><span>{esc(tl)}</span><span>{esc(tv)}</span></div>')
    if ex.get("note"):
        parts.append(f'<p class="cp-ex-note">{esc(ex["note"])}</p>')
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


def render_limitations(lim: dict) -> str:
    if not lim:
        return ""
    intro = f'<p class="cp-p">{lim["intro"]}</p>' if lim.get("intro") else ""
    items = "".join(f'<li class="cp-li">{it}</li>' for it in lim.get("items", []))
    return (
        '<section class="cp-limits" aria-labelledby="limitations">'
        '<h2 class="cp-h2" id="limitations">Limitations</h2>'
        f'{intro}<ul class="cp-ul">{items}</ul></section>'
    )


def render_faq(faq: list) -> str:
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
        '<h2 class="cp-h2" id="faq">Frequently asked questions</h2>'
        f'<div class="cp-faq-list">{"".join(items)}</div></section>'
    )


def render_related(related: list) -> str:
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
        '<h2 class="cp-h2" id="related">Related pages</h2>'
        f'<div class="cp-related-grid">{"".join(cards)}</div></section>'
    )


def render_cta(cta: dict, play_url: str) -> str:
    return (
        '<section class="cp-cta">'
        f'<h2>{esc(cta["h2"])}</h2><p>{esc(cta["p"])}</p>'
        '<div class="cp-cta-actions">'
        f'<a class="cp-btn-primary" href="{esc(play_url)}" target="_blank" rel="noopener" '
        'aria-label="Get Elmtrackr on Google Play (opens in a new tab)">Get it on Google Play</a>'
        '<a class="cp-btn-secondary" href="/">Back to the homepage</a>'
        "</div></section>"
    )


def render_breadcrumbs(page: dict) -> str:
    return (
        '<nav class="cp-breadcrumbs" aria-label="Breadcrumb"><ol>'
        '<li><a href="/">Home</a></li>'
        f'<li aria-current="page">{esc(page["breadcrumb"])}</li>'
        "</ol></nav>"
    )


# ── JSON-LD ──────────────────────────────────────────────────────────────────

def build_jsonld(page: dict, canonical: str, site_url: str, og: dict) -> str:
    graph = [
        {
            "@type": "WebPage",
            "@id": canonical + "#webpage",
            "url": canonical,
            "name": page.get("h1") or page["title"],
            "description": page["description"],
            "inLanguage": "en",
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
                {"@type": "ListItem", "position": 1, "name": "Home", "item": site_url + "/"},
                {"@type": "ListItem", "position": 2, "name": page["breadcrumb"], "item": canonical},
            ],
        },
    ]
    if page.get("faq"):
        graph.append({
            "@type": "FAQPage",
            "@id": canonical + "#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": strip_tags(qa["q"]),
                    "acceptedAnswer": {"@type": "Answer", "text": strip_tags(qa["a"])},
                }
                for qa in page["faq"]
            ],
        })
    doc = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(doc, indent=2, ensure_ascii=False)


def strip_tags(s: str) -> str:
    """Plain text for JSON-LD answer bodies (visible HTML may contain links)."""
    import re
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&nbsp;", " ").strip()


# ── page assembly ─────────────────────────────────────────────────────────────

def build_article(page: dict, play_url: str, og: dict) -> str:
    parts = []
    if page.get("hero_eyebrow"):
        parts.append(f'<p class="cp-eyebrow">{esc(page["hero_eyebrow"])}</p>')
    parts.append(f'<h1 class="cp-h1">{esc(page["h1"])}</h1>')
    parts.append(f'<p class="cp-lead">{page["lead"]}</p>')
    parts.append(f'<p class="cp-reviewed">Last reviewed: {esc(page["reviewed"])}</p>')
    if page.get("image"):
        parts.append(render_figure(page["image"]))
    parts.append(render_sections(page["sections"]))
    parts.append(render_limitations(page.get("limitations")))
    parts.append(render_faq(page.get("faq")))
    parts.append(render_related(page.get("related")))
    parts.append(render_cta(page["cta"], play_url))
    return "\n".join(p for p in parts if p)


def render_page(page: dict, manifest: dict, page_tpl: str, header: str, footer: str) -> str:
    site_url = manifest["site_url"].rstrip("/")
    play_url = manifest["play_store"]["url"]
    slug = page["slug"]
    canonical = f"{site_url}/{slug}/"

    og = dict(DEFAULT_OG)
    if page.get("og_image"):
        og.update(page["og_image"])
    og_abs = site_url + og["src"] if og["src"].startswith("/") else og["src"]

    article = build_article(page, play_url, og)
    jsonld = build_jsonld(page, canonical, site_url, og)

    subs = {
        "{{TITLE}}": esc(page["title"]),
        "{{DESCRIPTION}}": esc(page["description"]),
        "{{CANONICAL}}": canonical,
        "{{OG_TITLE}}": esc(page.get("og_title") or page["title"]),
        "{{OG_IMAGE}}": og_abs,
        "{{OG_IMAGE_W}}": str(og["w"]),
        "{{OG_IMAGE_H}}": str(og["h"]),
        "{{OG_IMAGE_ALT}}": esc(og["alt"]),
        "{{JSONLD}}": jsonld,
        "{{HEADER}}": header,
        "{{FOOTER}}": footer,
        "{{BREADCRUMBS}}": render_breadcrumbs(page),
        "{{ARTICLE}}": article,
    }
    out = page_tpl
    for k, v in subs.items():
        out = out.replace(k, v)
    if "{{" in out:
        leftover = out[out.index("{{"): out.index("{{") + 40]
        raise ValueError(f"{slug}: unreplaced template token near {leftover!r}")
    return out


def load_pages() -> list:
    pages = []
    for fn in sorted(os.listdir(CONTENT_DIR)):
        if fn.endswith(".json"):
            with open(os.path.join(CONTENT_DIR, fn), encoding="utf-8") as fh:
                pages.append(json.load(fh))
    return pages


def main(argv: list[str]) -> int:
    check_only = "--check" in argv[1:]
    manifest = load_manifest()
    page_tpl = read_template("page.html")
    header = read_template("header.html").replace("{{PLAY_URL}}", manifest["play_store"]["url"])
    footer = read_template("footer.html")

    pages = load_pages()
    stale = []
    for page in pages:
        rendered = render_page(page, manifest, page_tpl, header, footer)
        # validate embedded JSON-LD parses
        raw = rendered.split('<script type="application/ld+json">', 1)[1].split("</script>", 1)[0]
        json.loads(raw)

        out_dir = os.path.join(REPO_ROOT, page["slug"])
        out_path = os.path.join(out_dir, "index.html")
        if check_only:
            current = ""
            if os.path.isfile(out_path):
                with open(out_path, encoding="utf-8") as fh:
                    current = fh.read()
            if current != rendered:
                stale.append(page["slug"])
        else:
            os.makedirs(out_dir, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as fh:
                fh.write(rendered)
            print(f"  wrote {page['slug']}/index.html")

    if check_only:
        if stale:
            print("FAIL  stale content pages: " + ", ".join(stale))
            print("      run: python3 scripts/build_content_pages.py")
            return 1
        print(f"PASS  {len(pages)} content page(s) up to date")
        return 0

    print(f"Built {len(pages)} content page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
