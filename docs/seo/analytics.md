# Elmtrackr — Analytics layer

**Date reviewed:** 2026-07-16
**Module:** `assets/analytics.js` · **API:** `window.trackElmEvent(name, properties)`

A vendor-neutral event layer for measuring SEO and AI-search acquisition
**without** silently adding an analytics provider or collecting personal data.

## How it behaves

- It sends events **only to a provider that is already configured** on the
  page — `window.gtag` (GA) or a `window.dataLayer` (GTM). If neither exists it
  is a safe **no-op**.
- It never throws, never calls `preventDefault`, and never blocks navigation.
- It never sends page copy, email addresses, or full URLs. Values longer than
  100 chars, or containing `@` or `http(s)://`, are dropped.
- It respects consent: if `window.__elmtrackrConsent === "denied"`, nothing is
  sent and no UTM values are stored.
- **No property ID is embedded.** Do not hard-code a GA ID here.

## Connecting a vendor later

1. Decide on a provider and (for regulated regions) a consent mechanism first
   — see the review list in `docs/seo/privacy-data-inventory.md`.
2. Add that provider's snippet to the pages (e.g. GA4 `gtag.js` with your
   Measurement ID, or a GTM container that defines `window.dataLayer`).
3. Nothing else changes: `trackElmEvent` detects `gtag`/`dataLayer` and starts
   forwarding the same events. Update `privacy.html` to name the provider.
4. If you use a consent tool, set `window.__elmtrackrConsent` to
   `"granted"`/`"denied"` from it.

## Event dictionary

| Event | Fires when | Placed on |
|---|---|---|
| `play_store_click` | a Google Play link is activated | homepage hero/price, header “Get the app” |
| `product_page_cta_click` | the article CTA button on a product page | product pages |
| `guide_cta_click` | the article CTA button on a guide | guide pages |
| `video_play` | the tour video starts | homepage film |
| `video_25_percent` | playback passes 25% | homepage film |
| `video_50_percent` | playback passes 50% | homepage film |
| `video_complete` | playback ends | homepage film |
| `language_switch` | the en↔he switcher is used | header / homepage nav |
| `whatsapp_click` | a WhatsApp link is activated | homepage |
| `discord_click` | a Discord link is activated | homepage |
| `faq_expand` | a visible FAQ item is opened | any page with an FAQ |

Each event fires **once per activation**; video milestones fire once per load;
`faq_expand` fires once per item. Left-click, keyboard activation and
middle-click (`auxclick`) are all captured without duplication.

## Property definitions

| Property | Meaning | Example |
|---|---|---|
| `page_path` | pathname only, no query string | `/guides/how-to-track-work-hours/` |
| `language` | `<html lang>` of the page | `en`, `he` |
| `cta_location` | where the control sits | `hero`, `price`, `header`, `article`, `film`, `faq` |
| `destination_type` | where an outbound link goes | `play_store`, `whatsapp`, `discord` |
| `to_language` | target of a language switch | `he`, `en` |
| `referrer_category` | classified inbound source (see below) | `google`, `chatgpt` |
| `campaign_source` / `campaign_medium` / `campaign_name` / `campaign_content` | inbound UTM values captured for the session | `google` / `cpc` / `seo` / `hero` |

## Privacy considerations

- Only the property allow-list above is forwarded; unknown or unsafe values are
  dropped by `isSafeValue`.
- The **raw referrer URL is never sent** — only a category string. This avoids
  leaking query data a referrer URL may contain.
- Inbound UTM parameters are captured to `sessionStorage` **only** when consent
  is not denied and storage is available; they live for the session only.
- No cookies are set by this layer. Any cookies come from Google AdSense (see
  the privacy policy).

## Referral source classification

`referrer_category` is derived from `document.referrer`'s hostname (never the
full URL):

| Category | Matches (hostname) |
|---|---|
| `chatgpt` | `chatgpt.com`, `chat.openai.com`, `openai.com` |
| `copilot` | `copilot.microsoft.com` |
| `perplexity` | `perplexity.ai` |
| `bing` | `bing.com` |
| `google` | `google.*` |
| `social` | facebook/instagram/twitter/x/linkedin/youtube/tiktok/reddit/pinterest, whatsapp, discord |
| `internal` | same host as the site |
| `direct` | no referrer |
| `other_referral` | any other host |

**Identifying `chatgpt.com` traffic:** events carry
`referrer_category = "chatgpt"`. In GA/GTM, build a segment where that property
equals `chatgpt`, or (without this layer) filter sessions whose referrer host
contains `chatgpt.com` / `chat.openai.com`. Note that AI assistants often strip
the referrer, so ChatGPT-sourced visits can also arrive as `direct` — watch a
combination of `chatgpt` + a rise in `direct` alongside AI-crawler hits in
server logs, and tag any links you control with UTM `utm_source=chatgpt`.

## Play Store campaign parameters

Every “Get it on Google Play” link reaches the same verified listing
(`com.elmlaunch.myapp`) and carries campaign values in Google Play’s install
`referrer`:

| Parameter | Value |
|---|---|
| `utm_source` | `elmtrackr.site` (constant) |
| `utm_medium` | `website` (constant) |
| `utm_campaign` | page category: `homepage` \| `product` \| `guide` |
| `utm_content` | CTA location: `hero` \| `price` \| `header` \| `article` |

The destination listing is unchanged — only attribution differs, so this is
still a single canonical destination (see `validate_seo.py`).

**On footer CTAs:** the scheme reserves `utm_content=footer` and
`cta_location=footer` for a footer app CTA. The site footers currently hold
only legal/navigation links and a contact email — there is **no** "Get the app"
button in the footer today, so no `footer` value is emitted. If a footer Play
CTA is added later, give its link `data-elm-cta="footer"` and
`utm_content=footer` and it will be attributed distinctly with no other change.

## Reports to create (GA4 or equivalent)

1. **Acquisition by AI/search source** — sessions and Play clicks by
   `referrer_category`, to see Google vs Bing vs ChatGPT vs Perplexity vs
   Copilot vs social vs direct.
2. **Play Store clicks by page and language** — `play_store_click` +
   `product_page_cta_click` + `guide_cta_click`, grouped by `page_path`,
   `language` and `cta_location`. Cross-check with Play Console’s UTM
   (`utm_content`) attribution.
3. **Video funnel** — `video_play → video_25_percent → video_50_percent →
   video_complete` drop-off.
4. **Language behaviour** — `language_switch` counts and direction
   (`to_language`).
5. **Content engagement** — `faq_expand`, and guide vs product CTA rates.

### Comparing Play Store clicks by page and language

Filter to the three Play-click events, then pivot by `page_path` (which page)
and `language` (`en`/`he`), optionally splitting by `cta_location`. In Google
Play Console, the differentiated `utm_campaign`/`utm_content` values let you see
installs attributed to homepage vs product vs guide, and to header vs in-body
CTAs.
