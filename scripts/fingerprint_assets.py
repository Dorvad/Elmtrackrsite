#!/usr/bin/env python3
"""Fingerprint cacheable assets in an assembled static-site directory.

Source files keep readable, stable names for local development. Production
output gets content-derived filenames plus asset-manifest.json so each
deployment can safely use long-lived immutable caching without stale assets.

Assets named in absolute elmtrackr.site URLs (Open Graph, JSON-LD, and similar
public contracts) remain stable. Video, caption, and other media download URLs
also remain stable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
from pathlib import Path

HASH_LENGTH = 12
HASHABLE_EXTENSIONS = {
    ".css", ".js", ".woff2", ".webp", ".jpg", ".jpeg", ".png", ".svg",
}
CODE_EXTENSIONS = {".css", ".js"}
TEXT_EXTENSIONS = {
    ".css", ".html", ".js", ".json", ".txt", ".webmanifest", ".xml",
}
STABLE_MEDIA_EXTENSIONS = {".mp4", ".webm", ".vtt"}
ABSOLUTE_ASSET_RE = re.compile(
    r"https?://(?:www\.)?elmtrackr\.site/assets/"
    r"([A-Za-z0-9_./%+\-]+)"
)
FINGERPRINT_RE = re.compile(r"\.[0-9a-f]{12}\.[^.]+$")


def content_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:HASH_LENGTH]


def text_files(site: Path) -> list[Path]:
    return sorted(
        path for path in site.rglob("*")
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS
    )


def stable_public_assets(site: Path) -> set[str]:
    stable: set[str] = set()
    for path in text_files(site):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in ABSOLUTE_ASSET_RE.finditer(text):
            stable.add(match.group(1).split("?", 1)[0])
    return stable


def candidates(site: Path, extensions: set[str], stable: set[str]) -> list[Path]:
    assets = site / "assets"
    found = []
    for path in assets.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        rel = path.relative_to(assets).as_posix()
        if rel in stable or path.suffix.lower() in STABLE_MEDIA_EXTENSIONS:
            continue
        if FINGERPRINT_RE.search(path.name):
            continue
        found.append(path)
    return sorted(found)


def fingerprint(site: Path, paths: list[Path]) -> dict[str, str]:
    assets = site / "assets"
    fingerprinted = assets / "fp"
    mapping: dict[str, str] = {}
    for source in paths:
        rel = source.relative_to(assets).as_posix()
        hashed_name = f"{source.stem}.{content_hash(source)}{source.suffix.lower()}"
        target = fingerprinted / source.relative_to(assets).parent / hashed_name
        target.parent.mkdir(parents=True, exist_ok=True)
        source.replace(target)
        mapping[f"/assets/{rel}"] = f"/assets/{target.relative_to(assets).as_posix()}"
    return mapping


def rewrite_references(site: Path, mapping: dict[str, str]) -> None:
    if not mapping:
        return
    for path in text_files(site):
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = original
        for old_public, new_public in mapping.items():
            updated = updated.replace(old_public, new_public)
            updated = updated.replace(old_public.lstrip("/"), new_public.lstrip("/"))

            if path.suffix.lower() == ".css":
                css_dir = path.parent.relative_to(site).as_posix()
                old_rel = posixpath.relpath(old_public.lstrip("/"), css_dir)
                updated = updated.replace(old_rel, new_public)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")


def build_manifest(site: Path, mapping: dict[str, str]) -> None:
    manifest = {
        original: mapping[original]
        for original in sorted(mapping)
    }
    (site / "asset-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def verify(site: Path, mapping: dict[str, str]) -> None:
    for old_public, new_public in mapping.items():
        old_path = site / old_public.lstrip("/")
        new_path = site / new_public.lstrip("/")
        if old_path.exists():
            raise RuntimeError(f"unfingerprinted production asset remains: {old_public}")
        if not new_path.is_file():
            raise RuntimeError(f"fingerprinted asset is missing: {new_public}")

    for path in text_files(site):
        if path.name == "asset-manifest.json":
            continue
        text = path.read_text(encoding="utf-8")
        for old_public in mapping:
            if old_public in text or old_public.lstrip("/") in text:
                raise RuntimeError(
                    f"stale asset reference {old_public!r} remains in "
                    f"{path.relative_to(site)}"
                )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", default="_site", help="assembled site directory")
    args = parser.parse_args()
    site = Path(args.site).resolve()
    if not site.is_dir() or not (site / "assets").is_dir():
        parser.error(f"not an assembled site directory: {site}")
    if (site / "assets" / "fp").exists():
        parser.error("site already contains fingerprinted assets; rebuild it cleanly")

    stable = stable_public_assets(site)
    leaf_extensions = HASHABLE_EXTENSIONS - CODE_EXTENSIONS
    mapping = fingerprint(site, candidates(site, leaf_extensions, stable))
    rewrite_references(site, mapping)

    code_mapping = fingerprint(site, candidates(site, CODE_EXTENSIONS, stable))
    rewrite_references(site, code_mapping)
    mapping.update(code_mapping)

    build_manifest(site, mapping)
    verify(site, mapping)
    print(
        f"Fingerprinted {len(mapping)} production asset(s); "
        f"preserved {len(stable)} stable public asset URL(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
