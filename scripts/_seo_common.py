#!/usr/bin/env python3
"""Shared helpers for the Elmtrackr SEO tooling.

Both ``build_sitemap.py`` and ``validate_seo.py`` read the same route
manifest (``seo_manifest.json``) so that canonical URLs, hreflang pairings
and sitemap entries can never drift apart. Only Python's standard library
is used.
"""
from __future__ import annotations

import datetime
import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seo_manifest.json")


def load_manifest() -> dict:
    """Load and lightly validate the route manifest."""
    with open(MANIFEST_PATH, encoding="utf-8") as fh:
        data = json.load(fh)
    if not data.get("site_url"):
        raise ValueError("manifest: missing 'site_url'")
    if not isinstance(data.get("routes"), list) or not data["routes"]:
        raise ValueError("manifest: 'routes' must be a non-empty list")
    return data


def is_iso_date(value: str) -> bool:
    try:
        datetime.date.fromisoformat(value)
        return True
    except (ValueError, TypeError):
        return False


def sitemap_routes(manifest: dict) -> list[dict]:
    """Routes that belong in the sitemap: canonical, indexable, present,
    non-redirect pages. Excludes noindex pages, redirects and any page that
    does not yet exist (e.g. a Hebrew route that has not shipped)."""
    routes = []
    seen = set()
    for r in manifest["routes"]:
        if not r.get("indexable"):
            continue
        if r.get("redirect"):
            continue
        if r.get("exists") is False:
            continue
        canonical = r.get("canonical")
        if not canonical or canonical in seen:
            continue
        seen.add(canonical)
        routes.append(r)
    return routes


def hreflang_alternates(manifest: dict, group: str) -> list[dict]:
    """Existing, indexable, non-redirect routes sharing an hreflang group.

    A Hebrew alternate is emitted only once ``he/index.html`` actually
    exists (``exists`` is true) — never before.
    """
    alts = []
    for r in manifest["routes"]:
        if r.get("hreflang_group") != group:
            continue
        if not r.get("indexable") or r.get("redirect") or r.get("exists") is False:
            continue
        alts.append(r)
    return alts
