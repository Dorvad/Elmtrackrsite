# Elmtrackr — Crawler Policy

**Date reviewed:** 2026-07-16
**Applies to:** `robots.txt` at `https://elmtrackr.site/robots.txt`

This note documents the site's crawler policy and, in particular, the
distinction between AI-search crawling and model-training crawling. It is a
reference for the current `robots.txt`; the file itself remains the source of
truth for what is actually served.

## Current policy (as shipped)

| User-agent | Rule | Meaning |
|---|---|---|
| `*` (all crawlers) | `Allow: /` | Normal indexing. Nothing is disallowed, so CSS, JavaScript, images, video and inline JSON-LD are all reachable and pages can be fully rendered. |
| `OAI-SearchBot` | `Allow: /` | Explicitly permitted (see below). |
| `GPTBot` | *(no dedicated rule — inherits `*`)* | Intentionally left on the wildcard policy. **Do not add a dedicated rule without a product decision.** |

The sitemap is declared: `Sitemap: https://elmtrackr.site/sitemap.xml`.

## ChatGPT search crawling vs. model-training crawling

OpenAI operates separate crawlers for separate purposes, and they can be
governed independently in `robots.txt`:

- **`OAI-SearchBot`** — used to fetch and surface pages in **ChatGPT search
  results**. Allowing it helps the site appear when users search inside
  ChatGPT. It is *not* used to train models. We allow it explicitly.
- **`GPTBot`** — OpenAI's crawler associated with **collecting data that may
  be used to train models**. Allowing or blocking `GPTBot` is a separate
  choice from search visibility: blocking `GPTBot` does not remove the site
  from ChatGPT search, and allowing `OAI-SearchBot` does not opt the site
  into training.

> The exact behaviour of each crawler is defined by OpenAI and can change.
> These are the operator names as OpenAI documents them; verify against
> OpenAI's current crawler documentation before making a policy change. This
> note does not assert anything beyond how our own `robots.txt` is
> configured.

### Optional distinction to decide later (owner decision)

If the project wants to **allow ChatGPT search but opt out of
model-training**, the change would be to add a dedicated `GPTBot` block while
keeping `OAI-SearchBot` allowed, e.g.:

```
User-agent: GPTBot
Disallow: /
```

This is deliberately **not** shipped today, because "do not change the
`GPTBot` policy without an explicit product decision" is a standing
constraint. Record the decision here and update `robots.txt` in the same
change if/when it is made.

Analogous separate-purpose crawlers exist for other assistants (for example,
Google-Extended for Gemini training, and various vendor-specific search vs.
training agents). Any per-vendor allow/deny should be decided and documented
the same way, and should preserve normal search-engine indexing.
