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

## Delivered 2026-07-16 (2) — Homepage relevance & on-page content

Content pass on `index.html`, still sourced only from `product-facts.md`.
The editorial Aurora design, typography, animations and section numbering
are preserved; no walls of text were added.

- **Hero `h1`:** now leads with a visible, search-oriented line ("Hourly pay
  and shift tracking for Android and Wear OS") above the oversized brand
  statement "Every shift, measured." The supporting paragraph explains
  clocking in from phone or watch, tracking hours, applying configured
  overtime/premium rules, and the live estimated gross — stated explicitly as
  an estimate, not an official payslip. ("Breaks" was intentionally **not**
  claimed: it is not verified in the registry.)
- **New concise sections:** an *Overview* band (what Elmtrackr is / who it's
  for), an *Explore — focused guides* band, and a visible *FAQ*. Combined with
  the existing numbered sections, the page now answers all ten target
  questions (what/who/clock-in/estimate/overtime/Wear OS/reports/privacy/
  offline/pricing).
- **Visible FAQ:** eight native, keyboard-accessible `<details>` items; every
  answer is present in the HTML even when collapsed; each answer traces to a
  verified registry row.
- **Compensation disclaimer:** a concise visible block in the estimate section
  — rules are user-configured, presets are starting points, compare with the
  employer's official records/payslip, and Elmtrackr is not legal, payroll or
  tax advice.
- **Pricing:** unverified price copy ("$3. Once." / "no subscription") was
  **neutralized** (owner decision) — the price H2 slot keeps its visual
  treatment with "Know the number." and the copy points to the live Google
  Play listing for current pricing. No price is stated until verified.
- **Contextual internal links** (descriptive, not "Learn more"): to
  `/hourly-pay-tracker/`, `/android-shift-tracker/`, `/overtime-tracker/`,
  `/wear-os/`, `/reports/`, `/tasks/`, `/receipts-reimbursements/` and the
  existing `/privacy.html`.
- **Planned focused pages:** the seven new destinations are registered in
  `scripts/seo_manifest.json` as `exists:false` — excluded from the sitemap
  and skipped by the validator until authored. **These links 404 until the
  pages are built;** the next task should author each page, set `exists:true`
  with a `lastmod`, and re-run `scripts/build_sitemap.py`.
- **Verification:** static-HTML, SEO and sitemap checks pass; mobile (390px)
  and desktop (1280px) layouts rendered and reviewed for the new sections
  (overview grid, disclaimer, explore cards and FAQ all stack correctly).

---

## Delivered 2026-07-16 (3) — Static product-information page system

Turned the one-page site into a small crawlable product site **without a
client-side framework and without migrating the homepage**. All claims trace
to `product-facts.md`.

- **Build system (stdlib only):** `scripts/build_content_pages.py` renders
  `content/pages/*.json` through `templates/` (`page.html`, `header.html`,
  `footer.html`) into route directories (`<slug>/index.html`), using the
  shared `assets/content-pages.css` (Aurora type + palette). Output is
  deterministic; `--check` mode fails if the committed HTML is stale. Shared
  header/footer, breadcrumbs, metadata, canonical + hreflang, visible
  reviewed date, CTA, FAQ (`<details>`), and JSON-LD are all produced by the
  templates.
- **Eight English pages** (each: unique title/description, one `h1`, a short
  direct answer, sections, a concrete example where useful, a Limitations
  section, a visible FAQ, related-page links, homepage + Play CTA, breadcrumb,
  canonical, and `WebPage` + `BreadcrumbList` + `FAQPage` structured data):
  `/shift-tracker-android/`, `/hourly-pay-tracker/`, `/overtime-pay-tracker/`,
  `/wear-os-shift-tracker/`, `/receipt-expense-tracker/`,
  `/work-hours-reports/`, `/task-time-tracking/`, `/privacy-and-security/`.
- **Real screenshots only:** the Android, hourly-pay and Wear OS pages reuse
  existing product renders with descriptive alt text; pages without a relevant
  asset carry no image (no stock or AI imagery).
- **Verification-driven omissions:** requested items not backed by
  `product-facts.md` were left out rather than invented — notably break
  tracking / paid-vs-unpaid breaks, automatic receipt field extraction
  (amount/merchant/currency/date), task icons/colours, and explicit
  recent-task ordering. Presets are described as starting points, never as
  legal compliance; pay is always an estimate; nothing claims automatic
  payslip verification or claim submission to an employer.
- **Internal linking:** homepage links to all eight pages (old placeholder
  slugs repointed to the canonical ones); every page links home and to 2–4
  related pages; the required cross-links (overtime→hourly+reports,
  Wear OS→Android+privacy, receipts→reports+privacy, tasks→reports+shift) are
  present. No broken internal links; no duplicated paragraphs across pages.
- **SEO plumbing:** the eight routes are registered in `seo_manifest.json`
  (`exists:true`), so `build_sitemap.py` now emits nine URLs and
  `validate_seo.py` checks every page. The deploy workflow strips
  `content/`, `templates/` and `scripts/` from the published artifact.

---

## Delivered 2026-07-16 (4) — Hebrew (RTL) equivalents for the whole site

Full Hebrew counterparts for the homepage and all eight product pages, under
stable ASCII `/he/…` routes. Existing Hebrew work (the undeployed
`6263daa:he/index.html`) was reviewed and its terminology reused rather than
discarded.

- **Locale-aware build:** `scripts/build_content_pages.py` now generates both
  `en` (`content/pages/*.json`) and `he` (`content/pages/he/*.json`) into
  `<slug>/` and `he/<slug>/`. Hebrew chrome comes from `templates/header.he.html`
  and `templates/footer.he.html`; `templates/page.html` carries
  `lang`/`dir`/locale tokens. 16 pages total.
- **Hebrew homepage:** `he/index.html` (`<html lang="he" dir="rtl">`) mirrors
  the current English homepage — hero, all numbered sections, overview,
  explore cards, visible FAQ, video summary, CTA and footer localized. The
  descriptive H1 is `מעקב שעות עבודה וחישוב שכר משוער בזמן אמת`; the brand line
  `כל משמרת, נמדדת.` is preserved.
- **Translation, not transliteration:** natural Israeli Hebrew using the app's
  own terminology (`משמרת`, `החתמת כניסה/יציאה`, `שעות נוספות`, `תוספות`,
  `פרופילי תגמול`, `דוחות`, `החזרים`, `נעילת אפליקציה`, `סנכרון`, `תלוש`).
  Latin/number runs (Elmtrackr, Wear OS, CSV/PDF, ₪42, ×1.25, 22:00–06:00) are
  wrapped in bidi-isolated `.ltr` spans for stable display.
- **Typeface:** no Heebo. No Hebrew webfont is bundled, so Hebrew uses a safe
  self-contained system stack (`system-ui, 'Segoe UI', 'Arial Hebrew',
  'Noto Sans Hebrew', …`) with Archivo still serving Latin. No font files were
  downloaded or committed.
- **Hreflang & switcher:** every en/he pair carries reciprocal
  `hreflang="en"`/`"he"`/`"x-default"`; each page canonicalises to itself. An
  accessible language switcher links to the equivalent page (not the homepage),
  visible on mobile too.
- **Structured data:** localized names, descriptions, FAQ Q&A, breadcrumb
  labels and `inLanguage`, with product identity, URLs and verified facts kept
  consistent across languages.
- **New checker:** `scripts/check_locales.py` verifies en↔he coverage,
  hreflang reciprocity, self-canonicals, `dir="rtl"` on Hebrew pages, no
  mixed-language metadata/body, and that every language-switch target exists.
  Passes, along with `validate_seo` (18 sitemap URLs), `check_static_html`,
  `build_content_pages --check` and `build_sitemap --check`.
- **Responsive/RTL note:** content and typography verified in-browser at
  phone/desktop widths. The pre-installed headless Chromium cannot *screenshot*
  a page whose root element is `dir="rtl"` (it captures blank; the identical
  page renders the moment `dir="rtl"` is removed) — a capture quirk, not a page
  defect. RTL correctness is enforced via direction-aware CSS
  (`text-align:start`, flex ordering, right-side bullets, `.ltr` isolation).

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
