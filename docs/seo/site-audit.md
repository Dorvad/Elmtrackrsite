# Elmtrackr Marketing Site — SEO & AI-Search Audit

**Date reviewed:** 2026-07-16
**Website repository:** `Dorvad/Elmtrackrsite`
**Branch reviewed (checked out):** `claude/elmtrackr-seo-audit-6riti0`
**Live property:** `https://elmtrackr.site/`

> This document records the *current* state only. It does not implement any change.
> Where the checked-out branch and the deployed site differ, or where branches
> diverge, the difference is recorded rather than reconciled.

---

## 1. Deployment reality (verify before touching anything)

| Item | Finding | Evidence |
|---|---|---|
| Default branch | `claude/github-pages-deploy-i6mtq9` — **there is no `main` branch** | GitHub repo API `default_branch`; `git branch -a` |
| Deploy mechanism | GitHub Actions → Pages, artifact = repo root (`.`) | `.github/workflows/deploy-pages.yml` |
| Branches that trigger a deploy | `main` (absent), `claude/github-pages-deploy-i6mtq9`, `claude/elmtrackr-legal-pages-u9ga8y` | `.github/workflows/deploy-pages.yml` lines 4–5 |
| Concurrency | Single `pages` group, `cancel-in-progress: true` — **last push wins**; three branches publish to one site | workflow lines 13–15 |
| Currently live content | **Byte-identical to the checked-out branch** (`diff` of live `/index.html` vs local = identical) | `curl https://elmtrackr.site/` vs `index.html` |
| Checked-out branch vs `claude/github-pages-deploy-i6mtq9` | Identical (no divergent commits either direction) | `git log` range comparison |

**Conclusion:** the checked-out audit branch reflects what is live today. The live deploy came from the default branch (`claude/github-pages-deploy-i6mtq9`), most recently via the `ads.txt` commit.

### 1a. Undeployed work on another branch (do not overwrite blindly)

The branch `claude/elmtrackr-legal-pages-u9ga8y` (head `6263daa`) contains a **more SEO-complete and internationalised** version of the site that is **not currently live**:

- A `/he/` Hebrew route (`he/index.html`) with `<html dir="rtl" lang="he">`.
- `index.html` (74,852 bytes vs the live 65,588) with `rel="canonical"`, `hreflang` (`en` / `he` / `x-default`), Open Graph tags and `theme-color`.
- A richer `sitemap.xml` listing both `/` and `/he/` with `xhtml:link` hreflang alternates.

Because that branch also triggers the deploy workflow, this content was live at some point but was **overwritten** by a later deploy from the default branch. The live `/he/` route now returns **HTTP 404** (GitHub Pages 404 page).

> **Action rule for later phases:** the Hebrew page, canonical/hreflang tags and expanded sitemap already exist on `claude/elmtrackr-legal-pages-u9ga8y`. Reconcile with that branch first — do not re-author from scratch, and do not assume `/he/` never existed just because it 404s today.

> **Branch consolidation (2026-07-16):** all branches were consolidated into a single `main` branch. `main` matches the live site exactly — none of this SEO/Hebrew work was published. The undeployed work is preserved in `main`'s history (folded in via `-s ours` merges) and under the tags `archive/legal-pages-seo` (commit `6263daa`) and `archive/cursor-dev-env` (commit `43abb03`). To retrieve the Hebrew/SEO source for a later phase: `git show archive/legal-pages-seo:he/index.html`, `git show archive/legal-pages-seo:index.html`, `git show archive/legal-pages-seo:sitemap.xml`.

> **Note on automated fetch tools:** an LLM-based page fetch reported a fully rendered Hebrew page at `/he/` with a "₪10 one-time" price. Direct `curl` shows `/he/` returns **404** on the live site. The fetch output was a hallucination over the 404 body and must not be treated as evidence.

---

## 2. Route inventory (deployed site)

| Route | Type | Indexable? | Notes |
|---|---|---|---|
| `/` (`index.html`) | HTML landing page | **Indexable** — no `noindex`, `robots.txt` allows all | Primary page; single-page site |
| `/privacy.html` | Legal page | **noindex** (`<meta name="robots" content="noindex">`) | Not in sitemap; reachable only via privacy links (none found in `index.html`) |
| `/terms.html` | Legal page | **noindex** | Not in sitemap; no inbound link from `index.html` |
| `/robots.txt` | Directive file | n/a | Allows all, references sitemap |
| `/sitemap.xml` | Sitemap | n/a | Lists only `/` |
| `/ads.txt` | AdSense authorisation | n/a | `google.com, pub-6818267616933452, DIRECT, f08c47fec0942fa0` |
| `/he/` | Hebrew route | **404 live** | Exists only on `claude/elmtrackr-legal-pages-u9ga8y`, not deployed |
| `/assets/*`, `/uploads/*` | Static assets | n/a | Fonts, images, `elmtrackr-tour.mp4` |
| `CNAME` file | — | — | **Not present in repo**; custom domain configured in Pages settings + DNS per `README.md` |

---

## 3. Head metadata, titles, canonical, language

| Element | `/` (live) | `/privacy.html` | `/terms.html` |
|---|---|---|---|
| `<html lang>` | **Missing** (`<html><head>`) | `en` | `en` |
| `<title>` | `Elmtrackr — Every shift, measured` | `Privacy Policy — Elmtrackr` | `Terms & Conditions — Elmtrackr` |
| `<meta name="description">` | Present (mentions "$3 once, no subscription") | Absent | Absent |
| `rel="canonical"` | **Absent** | Absent | Absent |
| `hreflang` | **Absent** | Absent | Absent |
| Open Graph / Twitter Card | **Absent** | Absent | Absent |
| `theme-color` | Absent | Absent | Absent |
| Favicon / apple-touch-icon | Present (`assets/icon-192.png`) | Present | Present |

**Issues:**
- The home page has **no `lang` attribute**, no canonical, no social metadata and no structured data.
- The description tag advertises a price ("$3 once") — see the price conflict in §12.

---

## 4. Heading hierarchy (`/`)

- **One `<h1>`:** "Every shift, measured." — good (single H1).
- **`<h2>` per section:** "One tap. The record starts." / "Premiums classify themselves." / "The math is never hidden." / "Night shift, from the wrist." / "Punch in from the home screen." / "Three steps. That's it." / "One minute. A month, measured." / "$3. Once."
- **`<h3>`:** the three "Method" step cards ("Set your rates once", "Punch, phone or wrist", "Check your payslip").

Hierarchy is clean (H1 → H2 → H3, no skips). Minor: two sections carry the label `06` in `data-screen-label` ("06 Method" and "06 Price"); this is a cosmetic label, not a heading, but should be renumbered for consistency.

---

## 5. Rendering model & content-without-JavaScript

- The page markup lives inside custom elements `<x-dc>` / `<helmet>` / `<sc-if>` and is rendered at runtime by `support.js`.
- `support.js` is a **generated bundle** (`// GENERATED from dc-runtime/src/*.ts — do not edit. Rebuild with cd dc-runtime && bun run build`). The `dc-runtime/` source is **not present in this repository**, so the bundle cannot be regenerated here and must be treated as read-only.
- `support.js` loads **React 18.3.1, ReactDOM 18.3.1 and Babel standalone 7.29.0 from `unpkg.com`** at runtime and compiles the in-page component in the browser.
- The visible marketing copy *is* present in the static HTML source, but the hero/live widgets contain **raw template placeholders** that only resolve once JavaScript runs.

**Raw template placeholders visible to non-JS crawlers** (in `index.html`): `{{ clockHM }}`, `{{ clockS }}`, `{{ paySoFar }}`, `{{ ringProgress }}`, `{{ goalPct }}`, `{{ goalHM }}`, `{{ showWatch }}`, `{{ playState }}`, plus `ref="{{ ... }}"` bindings. A crawler or AI agent that does not execute JS (and does not run the unpkg-hosted Babel step) sees literal `{{ clockHM }}` etc. in the hero clock and widgets.

**Risk:** content and interactivity depend on a third-party CDN (`unpkg.com`) and on client-side Babel compilation. If unpkg is unreachable or JS is disabled, the page degrades to static copy with unresolved `{{ }}` tokens.

---

## 6. Internal-link structure

- Nav / footer anchors are all **in-page fragments**: `#method`, `#widgets`, `#watch`, `#film`, `#price`, `#get`.
- **No internal link to `/privacy.html` or `/terms.html`** from `index.html` (they are orphan pages, reachable only by direct URL).
- External links: Google Play (see §7), WhatsApp community (real invite `chat.whatsapp.com/BWUCyX16z7c596iiYO9Vbv...`), Discord (`https://discord.com` — generic, not an invite).

---

## 7. Play Store link destinations

- **All "Get it on Google Play" buttons point to `https://play.google.com`** (the Play Store home page), not to the Elmtrackr app listing. Two occurrences in `index.html` (hero + price CTA).
- This is a functional and SEO problem: the primary conversion CTA does not reach the product. The correct listing URL depends on the verified package ID (see `product-facts.md`).

---

## 8. Image & video metadata

- Decorative images use empty `alt=""` correctly (logos, icons, device chrome).
- The hero screenshot has a descriptive alt: *"Elmtrackr home screen — hours distribution, gross pay and recent shifts."*
- **Video** (`assets/elmtrackr-tour.mp4`): `preload="metadata"`, poster `assets/tour-poster.jpg`, autoplays muted in view, unmutes on tap. **No captions/subtitles `<track>`** — accessibility and video-SEO gap. No `VideoObject` structured data.
- No width/height on some inline device images could cause layout shift, though most decorative elements are CSS-sized.

---

## 9. Structured data

- **None.** No JSON-LD, Microdata or RDFa anywhere (`/`, `/privacy.html`, `/terms.html`).
- For an app marketing site, the absence of `SoftwareApplication`/`MobileApplication`, `Organization`, `BreadcrumbList`, `FAQPage` and `VideoObject` schema is a significant AI-search and rich-result gap. Any `SoftwareApplication` price/rating fields must only be populated from verified facts (see `product-facts.md`).

---

## 10. Robots directives & sitemap

- **`robots.txt`** (live): `User-agent: *` / `Allow: /` / `Sitemap: https://elmtrackr.site/sitemap.xml`. No disallows.
- **`sitemap.xml`** (live): a single URL, `https://elmtrackr.site/`, `lastmod 2026-07-13`, `changefreq monthly`, `priority 1.0`. No hreflang alternates, no legal pages (legal pages are intentionally `noindex`).
- The AdSense loader is present site-wide even on legal pages served with `noindex`.
- The richer sitemap with hreflang alternates exists only on the undeployed `legal-pages` branch (§1a).

---

## 11. Social metadata

- **Absent on all pages.** No `og:title`, `og:description`, `og:image`, `og:url`, `og:type`, no Twitter Card tags. Link previews on social platforms and in chat apps will fall back to bare URL/title.
- Open Graph tags exist only on the undeployed `legal-pages` branch.

---

## 12. Privacy & advertising inconsistencies (conflicts — recorded, not resolved)

1. **AdSense vs privacy policy.** `index.html` loads Google AdSense (`pagead2.googlesyndication.com/.../adsbygoogle.js?client=ca-pub-6818267616933452`) and `ads.txt` authorises `pub-6818267616933452`. **`privacy.html` states: "We do not use third-party advertising or analytics SDKs."** The live site therefore runs third-party advertising that the privacy policy says it does not. This is a direct contradiction and a compliance risk.
2. **"No ads" product claim vs ad-serving site.** The price section states "No subscription, no ads". That refers to the app, but the marketing site itself serves ads — worth aligning messaging and disclosure.
3. **Price conflict.** English copy says **"$3. Once."** / meta description "$3 once". The Hebrew page on the `legal-pages` branch says **"10 ₪ פעם אחת"** (₪10 once). `$3` and `₪10` are stated as different nominal prices. Neither is verifiable from the Android source or from a live Play listing — treat price as **unverified** (see `product-facts.md`).
4. **Brand capitalisation is inconsistent** across the site: wordmark/nav/footer render `elmtrackr` (lowercase); `<title>`/meta and legal pages use `Elmtrackr`; widget mockups and privacy/terms body use `ElmTrackr`. Canonical capitalisation must be pinned in `product-facts.md`.

---

## 13. Accessibility issues affecting search

- Missing `<html lang>` on the home page (screen-reader language + hreflang signals).
- Video has no captions `<track>`.
- Live-updating clock/pay values (`aria-live` not set) — minor.
- Colour-on-gradient text in device mockups is decorative; primary copy contrast appears adequate but was not measured.
- Raw `{{ }}` placeholders (§5) are read literally by assistive tech when JS is unavailable.

---

## 14. Performance risks

- Runtime dependency on **`unpkg.com`** for React + ReactDOM + **Babel standalone** (in-browser compilation) — render-blocking on the critical path, third-party origin, and a single point of failure.
- Client-side Babel compilation of the page component adds main-thread cost on load.
- `index.html` is ~64 KB of inline HTML/CSS; self-hosted fonts are good (no Google Fonts request), but multiple large `@font-face` subsets load.
- `elmtrackr-tour.mp4` autoplays when in view; `preload="metadata"` limits initial cost, acceptable.
- AdSense script is `async` but still a third-party request on every page.

---

## 15. Differences between checked-out branch and deployed site

- **Home page, robots, sitemap, ads.txt, legal pages:** checked-out branch == live (verified identical).
- **Missing from live but present in repo (on `claude/elmtrackr-legal-pages-u9ga8y`):** `/he/` Hebrew route, canonical + hreflang + Open Graph tags on the English page, and the expanded hreflang sitemap. These are undeployed, not absent — see §1a.
- No CNAME file is tracked in any branch reviewed; the custom domain is managed in GitHub Pages settings/DNS.

---

## 16. Summary of highest-impact gaps (for the implementation plan)

1. Fix the primary CTA: Play Store links go to the generic store home, not the app listing.
2. Resolve the AdSense-vs-privacy-policy contradiction (compliance).
3. Add `<html lang>`, canonical, Open Graph/Twitter, and `SoftwareApplication` JSON-LD — reconciled with the `legal-pages` branch, using only verified facts.
4. Decide the fate of the Hebrew route and hreflang (undeployed work exists; do not duplicate).
5. Address the JS-dependent rendering / raw `{{ }}` placeholders for crawlers and AI agents.
6. Pin canonical brand capitalisation and a single, verified price statement.
7. Consolidate deploy branches so "last push wins" cannot silently roll back live SEO work.
