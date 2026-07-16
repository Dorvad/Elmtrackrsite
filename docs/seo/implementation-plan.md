# Elmtrackr SEO & AI-Search Overhaul — Phased Implementation Plan

**Date:** 2026-07-16
**Scope:** marketing-site repository (`Dorvad/Elmtrackrsite`) only.
**Source of truth for product claims:** `docs/seo/product-facts.md` (this repo) →
derived from the Android repository `Dorvad/elmtrackr`, branch `Main` (read-only).

> This is a plan, not an implementation. Nothing here changes public copy until the
> corresponding phase is explicitly approved. Every claim published in any phase must
> trace to a `verified: implemented` row in `product-facts.md`. Never invent legal,
> payroll or product claims. Pay results are estimates, never official payroll.

---

## Guiding constraints

- **Deploy topology first.** Three branches (`main` — absent, `claude/github-pages-deploy-i6mtq9`, `claude/elmtrackr-legal-pages-u9ga8y`) publish to one Pages site with `cancel-in-progress`, so "last push wins." Any SEO work can be silently rolled back by a deploy from another branch. Consolidation is a prerequisite, not an afterthought.
- **Undeployed work exists.** The Hebrew route, canonical/hreflang/OG tags and the expanded sitemap already live on `claude/elmtrackr-legal-pages-u9ga8y`. Reconcile with that branch; do not re-author from scratch.
- **`support.js` is generated and unbuildable here.** Its source (`dc-runtime/`) is absent, and it is marked "do not edit." Treat as read-only. All SEO markup must go into hand-authored HTML (`index.html`, legal pages, new files), not the bundle.
- **Facts before copy.** Phase 0 (this deliverable) gates everything else.

---

## Delivered 2026-07-16 — Technical SEO foundation (Phases 2, 3-partial, 4, 7)

Implemented on branch `claude/technical-seo-foundation-fzqrk0`, using
`docs/seo/product-facts.md` as the only source for product claims. No rating,
price, review or compatibility claim was fabricated.

- **Homepage metadata (`index.html`):** descriptive title, meta description
  (price removed), self-referencing canonical, `robots` directive,
  Open Graph (title/description/url/type/image + dimensions/alt/locale),
  Twitter `summary_large_image`, light/dark `theme-color`, SVG + PNG favicons
  and `apple-touch-icon`.
- **Structured data:** one JSON-LD `@graph` — `Organization`, `WebSite`,
  `SoftwareApplication`. Verified facts only; `offers`/price omitted (price
  unverified), no `aggregateRating`/reviews, no "free"/payroll/"fully offline"
  claims.
- **Play Store links:** both CTAs now use the one canonical package-specific
  URL derived from the verified application id `com.elmlaunch.myapp`, with
  website-acquisition campaign params (via Play's `referrer`), `target=_blank`,
  `rel="noopener"` and an `aria-label`. The generic `play.google.com`
  home-page links are gone. **Listing public availability remains UNVERIFIED**
  — status centralized in `scripts/seo_manifest.json` and documented in
  `docs/seo/play-listing.md` (owner to confirm and flip `listing_public`).
- **`robots.txt`:** upgraded, not replaced — normal indexing preserved,
  `OAI-SearchBot` explicitly allowed, sitemap declared, nothing content-blocked.
  `GPTBot` policy left unchanged (inherits `*`); the ChatGPT-search vs
  model-training distinction is documented in `docs/seo/crawler-policy.md`.
- **Sitemap:** hand-maintained file replaced by a reproducible generator
  (`scripts/build_sitemap.py`) driven by a route manifest
  (`scripts/seo_manifest.json`). Emits only canonical/indexable/existing
  pages, accurate `lastmod`, no priority/changefreq, validates its XML, and
  leaves `ads.txt` untouched.
- **Canonicals & hreflang:** manifest-driven mechanism. Homepage carries
  self-referencing `hreflang="en"` + `x-default`. **No Hebrew alternate is
  emitted** because `/he/` does not exist yet (Phase 5).
- **Validation:** `scripts/validate_seo.py` checks titles, descriptions,
  canonicals, OG URLs, JSON-LD syntax + required schema properties,
  sitemap/canonical consistency, absence of invented rating/price fields,
  hreflang reciprocity, route uniqueness and Play-link centralization. Passes.

**Still open (owner decisions, out of this phase's scope):** the visible
marketing price ("$3. Once." / "$3 once, no subscription") and the
"no ads" copy vs. the AdSense loader (Phase 8), brand capitalization
(`Elmtrackr` visible vs verified `ElmTrackr` — used as JSON-LD `name` with
`Elmtrackr` as `alternateName`), and the Hebrew route (Phase 5).

---

## Phase 0 — Verified product-facts registry & audit *(this deliverable — documentation only)*

- **Deliverables:** `docs/seo/product-facts.md`, `docs/seo/site-audit.md`, `docs/seo/implementation-plan.md`.
- **Files changed:** `docs/seo/*` only.
- **Risks:** none (docs only). Unverified facts are flagged, not published.
- **Dependencies:** read-only review of the Android `Main` branch.
- **Rollback:** delete the docs; no runtime impact.
- **Exit criteria:** every required fact has a status and evidence path; conflicts recorded.

---

## Phase 1 — Deploy-topology consolidation & guardrails — **DONE (2026-07-16)**

- **Goal:** one predictable deploy source so later SEO work cannot be rolled back.
- **Completed:**
  - Consolidated all branches into a single `main`. `main` matches the live site exactly (deployed files byte-identical); no SEO/Hebrew work was published.
  - The undeployed work from `claude/elmtrackr-legal-pages-u9ga8y` (`6263daa`) and `cursor/setup-dev-environment-1a3e` (`43abb03`) is preserved in `main`'s history (`-s ours` merges) — the commits stay reachable from `origin/main` after the branches are deleted, retrievable with `git show 6263daa:<path>`. Nothing lost.
  - Narrowed `.github/workflows/deploy-pages.yml` `on.push.branches` to `[main]`, and added a step that strips internal files (`docs/`, `AGENTS.md`) from the published artifact so they are not served publicly.
- **Still pending (requires repo admin — the agent lacks admin rights):**
  - Set `main` as the repository's **default branch** in GitHub → Settings → Branches.
  - After that, delete the old default `claude/github-pages-deploy-i6mtq9`.
  - Optional: add a `CNAME` file if the project wants the custom domain pinned in-repo (currently only in Pages settings).
- **Rollback:** revert the workflow change; the archived branches/tags allow full recovery of any prior state.

---

## Phase 2 — Technical SEO foundation (English home + legal pages)

- **Goal:** the crawlable essentials, reconciled with the `legal-pages` branch.
- **Work:**
  - Add `<html lang="en">` to `index.html`.
  - Add `rel="canonical"` (`https://elmtrackr.site/`).
  - Add Open Graph + Twitter Card tags (title, description, `og:image`, `og:url`, `og:type`, `theme-color`), using an existing asset for `og:image`.
  - Add internal links to `/privacy.html` and `/terms.html` from the footer (they are currently orphaned).
  - Keep legal pages `noindex` (intentional) but ensure they are linked.
- **Files likely to change:** `index.html`, `privacy.html`, `terms.html`.
- **Risks:** duplicating tags already on the `legal-pages` branch → conflicting canonicals; must merge, not stack.
- **Dependencies:** Phase 1 (so tags survive), `product-facts.md` for the description wording.
- **Rollback:** remove the added `<head>` tags; purely additive, low risk.

---

## Phase 3 — Conversion & link correctness

- **Goal:** the CTA reaches the product; external links resolve.
- **Work:**
  - Replace `https://play.google.com` with the verified app-listing URL derived from the confirmed package ID (`product-facts.md`). **Blocked until the package ID and listing availability are verified.**
  - Replace the generic `https://discord.com` link with a real invite or remove it.
  - Confirm the WhatsApp invite is current.
- **Files likely to change:** `index.html` (hero + price CTA + footer).
- **Risks:** linking to a listing that is not yet public would send users to a dead page — verify listing availability first.
- **Dependencies:** verified package ID / listing status (currently **unknown** — see `product-facts.md`).
- **Rollback:** restore prior hrefs.

---

## Phase 4 — Structured data (JSON-LD)

- **Goal:** rich results + AI-search comprehension, strictly from verified facts.
- **Work:**
  - `SoftwareApplication` / `MobileApplication`: name, `operatingSystem`, `applicationCategory`, `offers` (price) — **only** if price is verified; otherwise omit `offers` rather than guess.
  - `Organization` (brand, logo, contact).
  - `VideoObject` for the tour film.
  - Optional `FAQPage` if FAQ copy is added.
  - **Do not** include `aggregateRating`/`ratingValue`/`reviewCount` — not verifiable from an authoritative source (see rules).
- **Files likely to change:** `index.html` (new `<script type="application/ld+json">`).
- **Risks:** Google structured-data penalties for unverifiable `offers`/`aggregateRating`; keep to confirmed fields.
- **Dependencies:** `product-facts.md` (name, price, platform), Phase 3 (listing URL).
- **Rollback:** remove the JSON-LD block.

---

## Phase 5 — Hebrew route & internationalisation

- **Goal:** restore and correctly signal the `/he/` route.
- **Work:**
  - Bring back `he/index.html` from `claude/elmtrackr-legal-pages-u9ga8y` (do not rewrite).
  - Add `hreflang` (`en` / `he` / `x-default`) to both pages and to `sitemap.xml`.
  - Reconcile the **price conflict** ($3 vs ₪10) into a single verified statement or a clearly localised equivalent — do not ship two contradictory prices.
  - Verify RTL (`dir="rtl"`) and Hebrew string accuracy against the Android Hebrew resources.
- **Files likely to change:** `he/index.html`, `index.html`, `sitemap.xml`.
- **Risks:** conflicting/duplicate hreflang; shipping an unverified price; RTL layout regressions.
- **Dependencies:** Phase 1 (merge), price resolution in `product-facts.md`, Android Hebrew strings.
- **Rollback:** remove `/he/` and its hreflang refs; revert sitemap.

---

## Phase 6 — Crawlability of JS-rendered content

- **Goal:** non-JS crawlers and AI agents do not see raw `{{ }}` placeholders.
- **Work (options, to be chosen with the owner):**
  - Provide a static, meaningful fallback for the hero/live values (e.g. sample values in the source instead of `{{ clockHM }}`), so the pre-JS DOM reads sensibly.
  - Consider self-hosting React/Babel or pre-rendering to remove the `unpkg.com` runtime dependency (also a performance win).
  - Because `support.js` is generated/unbuildable here, changes must be confined to hand-authored HTML or a documented regeneration of `dc-runtime` (source not currently in repo).
- **Files likely to change:** `index.html` (placeholder fallbacks); possibly build tooling if `dc-runtime` is added.
- **Risks:** editing generated output by hand is prohibited; must not hand-patch `support.js`.
- **Dependencies:** access to `dc-runtime` source if the render pipeline is to change.
- **Rollback:** revert placeholder fallbacks.

---

## Phase 7 — Sitemap, robots & metadata hygiene

- **Goal:** accurate discovery signals.
- **Work:** finalise `sitemap.xml` (home + `/he/` with hreflang, correct `lastmod`), keep legal pages out (they are `noindex`), confirm `robots.txt` and `ads.txt` remain consistent with the advertising decision from Phase 8.
- **Files likely to change:** `sitemap.xml`, `robots.txt`.
- **Risks:** listing `noindex` pages in the sitemap sends mixed signals.
- **Dependencies:** Phase 5, Phase 8.
- **Rollback:** restore previous sitemap/robots.

---

## Phase 8 — Privacy / advertising compliance alignment

- **Goal:** remove the contradiction between running AdSense and a privacy policy that says "no third-party advertising or analytics SDKs."
- **Work (owner decision required):** either (a) remove AdSense + `ads.txt` to match the stated policy and the "no ads" positioning, or (b) update `privacy.html` to disclose AdSense accurately and keep the loader. **This is a legal/compliance decision, not an SEO one** — surface it, do not decide unilaterally.
- **Files likely to change:** `index.html`, `ads.txt`, `privacy.html`.
- **Risks:** compliance exposure if left contradictory; revenue/consent implications.
- **Dependencies:** explicit owner instruction.
- **Rollback:** revert whichever direction was taken.

---

## Phase 9 — Accessibility & performance

- **Goal:** search-affecting a11y + Core Web Vitals.
- **Work:** video captions `<track>`; `aria-live` on live counters; reduce/remove third-party CDN reliance (ties to Phase 6); verify contrast; explicit media dimensions to limit CLS.
- **Files likely to change:** `index.html`, assets (caption file).
- **Risks:** motion/perf regressions; test `prefers-reduced-motion` paths.
- **Rollback:** per-change revert.

---

## Cross-phase dependency summary

| Phase | Hard blockers |
|---|---|
| 1 Deploy consolidation | Owner decision on canonical branch |
| 2 Technical SEO | Phase 1; verified description wording |
| 3 CTA/links | **Verified package ID + listing availability (currently unknown)** |
| 4 Structured data | Verified name/price/platform; Phase 3 URL |
| 5 Hebrew/i18n | Phase 1 merge; resolved price; Hebrew strings |
| 6 Crawlability | Access to `dc-runtime` source for any render change |
| 7 Sitemap/robots | Phases 5 & 8 |
| 8 Ads/privacy | **Owner legal/compliance decision** |
| 9 A11y/perf | Ties to Phase 6 |

## Global rollback note

All changes are static-file edits deployed via GitHub Pages. Every phase is revertible by
`git revert` of its commit; Pages redeploys the prior state on the next push to the canonical
branch. Keep each phase in its own commit/PR to preserve granular rollback.
