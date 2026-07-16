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

## Delivered 2026-07-16 (5) — Educational guides hub + first guide set (en + he)

A `/guides/` (and `/he/guides/`) hub plus four guide pairs written to answer
the broader questions people ask before they know the brand — grounded in real
Elmtrackr workflows, not thin keyword pages.

- **Hub** (`/guides/`, `/he/guides/`): organizes guides into five themes —
  tracking work hours, estimating pay, overtime & premiums, reviewing work
  records, and using Android/Wear OS tools (the last links to the product
  pages). Two-level breadcrumb (Home / Guides).
- **Four guide pairs** (Article schema, three-level breadcrumb Home / Guides /
  guide, ~800–900 words each): how to track work hours; how to estimate hourly
  pay; overtime vs premium pay; how to review work hours against a payslip.
- **Consistent AI-answer structure** on every guide: direct answer up top, a
  definition section, step-by-step, an illustrative example/table (clearly
  labelled), common mistakes, "How Elmtrackr helps", "What Elmtrackr can't
  determine", a visible FAQ, a Methodology & sources note, and a visible
  reviewed date. Paragraphs are short and self-contained.
- **Builder additions:** `schema_type` (`Article`/`WebPage`), optional
  `parent` (3-level breadcrumb + BreadcrumbList), optional `cta`, and a
  `methodology` block rendered after the FAQ. `FAQPage` is emitted only where a
  visible FAQ exists. No fabricated authors, credentials or citations.
- **Grounded, not name-dropped:** guides reference configurable thresholds,
  visible pay breakdowns, local shift history, tasks, CSV/PDF reports, Wear OS
  and widgets only where they genuinely answer the question, and each is
  explicit about what the app cannot determine (legal correctness, contract
  terms, taxes, whether a payslip is right).
- **Integration:** "Guides"/"מדריכים" added to the content-page headers/footers
  and both homepage navs; guides cross-link to each other and to the product
  pages; 10 routes added to the manifest (sitemap now 28 URLs). `check_locales`,
  `validate_seo`, `check_static_html`, and both `--check` builders pass.

---

## Delivered 2026-07-16 (6) — Media accessibility & performance (film + images)

Made the product film and images understandable to search engines, AI, screen
readers and slow connections. Full inventory in `docs/seo/media-audit.md`.

- **Verified film facts** (MP4 atom parse + ffmpeg probe): H.264, 1080×1920,
  30 fps, AAC stereo, 64.67 s. On-screen content read from decoded frames.
- **Film accessibility (index.html + he/index.html):** descriptive heading and
  an accurate summary; native `controls` (keyboard play/pause/mute/captions/
  fullscreen); `<track kind="captions">` (en + he WebVTT in
  `assets/captions/`); a full visible transcript in each language; renamed
  descriptive poster (`elmtrackr-app-tour-poster.jpg`); `preload="metadata"`;
  **no autoplay** (no sound without user action; reduced-motion respected by
  default); `<source>` + a visible MP4 fallback link; the custom
  autoplay/tap-to-unmute script removed.
- **VideoObject JSON-LD** on both homepages with verified fields only (name,
  description, thumbnailUrl, contentUrl, duration `PT1M5S`, uploadDate=site
  publish date, inLanguage, width, height).
- **Documented gap (not invented):** the clip has an audio track whose content
  can't be verified here, so the transcript/captions describe the meaningful
  **on-screen** content and say so; `uploadDate` uses the site publish date
  because the file embeds none.
- **Images:** classified every asset (screenshot / logo / decorative / poster /
  OG / non-public upload). Renamed the two generic files
  (`app-screenshot`→`elmtrackr-home-screen`, `tour-poster`→…poster). Meaningful
  images have descriptive alt, width/height, `decoding="async"`, lazy below the
  fold and eager for the hero; decorative icons/logos use `alt=""`.
- **Performance:** WebP derivatives for the meaningful raster images
  (~45–80% smaller), served via `<picture>` with JPG fallback (paths never
  break); originals preserved; no upscaling. Content-page figures and the
  homepage hero use `<picture>`.
- **Social images:** homepage, product pages and the guides hub all use a real
  product screenshot (`render-widgets-tablet.jpg`, 1400×933) as the OG image —
  no generic/AI artwork.
- **New checker:** `scripts/check_media.py` verifies broken media URLs, missing
  dimensions/alt, duplicate alt, oversized assets, video controls/captions/
  transcript/fallback, VideoObject consistency, transcript availability in both
  languages, and that non-public `uploads/` are not linked. Passes across 30
  pages.

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
