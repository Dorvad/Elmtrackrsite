# Elmtrackr Design System

> The **"Aurora"** design language behind Elmtrackr — a shift & hours tracker for hourly
> workers. This system packages the brand's tokens, components, and full-screen UI
> recreations so design agents can build on-brand artifacts and product surfaces.

---

## What is Elmtrackr?

Elmtrackr is a **personal shift & payroll tracker for hourly workers** — clock in/out from
your wrist or phone, and it instantly shows hours, overtime, weekend/holiday premiums, and an
**estimated** gross-pay figure. It is offline-first and syncs to Supabase.

Product surfaces represented here:

- **Mobile app** (the primary product) — a phone-sized PWA / native-Android experience.
  Home (the clock), Shifts list, Reports, and Settings, with a frosted bottom nav.
- **Wear OS watch app** (concept) — punch from the wrist: a glanceable tile, full app,
  watch-face complication, always-on display, and curved history list.

The hero interaction everywhere is the **clock** — a gradient progress ring with a live
count-up timer that punches you in/out in a single tap. The app ships **14 clock face
styles** (classic, bold, minimal, focus, night, retro, aurora, pulse, dial, strand, prism,
sand, blocks, orbit) — a strong signal that *the timepiece is the brand*.

### Sources used to build this system

This design system was reverse-engineered from real Elmtrackr source. Reference these for
deeper, more accurate work:

- **Codebase:** `Elmtrackr-native-android/` — a monorepo. The **active** product is the
  Kotlin + Jetpack Compose Android app under `android/`; the **frozen** Next.js web app under
  `app/` + `components/` is where the Aurora tokens, React components, and all screen layouts
  in this system were lifted from (`app/globals.css`, `components/ui/*`, `components/dashboard/ClockWidget.tsx`).
  See `android/VISUAL_PARITY.md` for the token↔component audit.
- **GitHub:** [`Dorvad/elmtrackr`](https://github.com/Dorvad/elmtrackr) (default branch
  `claude/shift-tracker-app-G91r8`; product also tracks an `elmtrackr-android` branch).
  Explore this repo to build more faithfully against the product.
- **Watch concept:** `uploads/elmtrackr Watch App.pdf` — the Wear OS surfaces.

> If you have access, browse the GitHub repo and the codebase directly — they are richer
> than this snapshot and will help you produce higher-fidelity work.

---

## Content fundamentals — voice & copy

Elmtrackr's voice is **plain, warm, and quietly confident**. It speaks to a worker checking
their wrist between tasks — never corporate, never cute.

- **Person:** Second person ("**your** shift", "**you're** ready"). The app addresses the
  user directly; it rarely says "I" or "we" except in trust moments ("We'll email you a link").
- **Tone:** Calm and encouraging. Short declaratives. *"Tap to start tracking your shift."*
  *"Clock in once. See hours, pay estimate, and overtime instantly."* *"You're ready."*
- **Casing:**
  - **Eyebrow labels** are `UPPERCASE` with wide tracking — `ELAPSED`, `THIS MONTH · ESTIMATED GROSS`, `RECENT SHIFTS`, `DAILY GOAL`. This is the system's signature label treatment.
  - **Titles & buttons** use Title Case or sentence case — "Clock In", "Clock Out", "Save Settings", "Add shift manually".
  - The wordmark **"elmtrackr"** is always lowercase.
- **Numbers lead.** Copy is built around figures — hours, percentages, currency. Timers are
  monospaced/`tabular-nums` so digits don't jitter. Pay is always framed as an **estimate**
  ("Estimated Gross", with a disclaimer note) — never a promise.
- **Microcopy is reassuring, not chatty.** Empty states explain the next action
  ("Complete some shifts to see your report."). Confirmations are two words ("Shift started",
  "Settings saved", "CSV exported").
- **Status language:** "On Shift · Regular", "Not Clocked In", "Live", "Overtime" / "+25%
  night rate". Mid-dot `·` is the preferred separator in labels.
- **Emoji:** Rare and functional. A 🌙 appears in the Night clock; 📋 in an empty state. Treat
  emoji as occasional accents, **not** a system. Prefer the SVG icon set.
- **Vibe:** "Your hours, beautifully accounted for." Premium, glanceable, trustworthy. The
  product makes the mundane act of punching a clock feel a little magical.

---

## Visual foundations

### Palette — "Aurora"
A cool indigo→aqua spine with warm peach and plum accents, floated over a pale lavender page.

- **Page** is never pure white — it's `#ECEEFA` lavender (dark: `#0B1020` near-black navy).
- **Cards** are pure white (`#FFFFFF`) floating on the lavender, with a hairline
  `border: 1px solid rgba(255,255,255,0.8)` and a soft **indigo-tinted** shadow.
- **Indigo `#5B4DF2`** is the primary/brand and represents "regular" hours.
- Semantic hour types each own a hue: **peach `#FF9E7D`** = overtime, **plum `#8B5CF6`** =
  weekend/holiday, **emerald `#10B981`** = live/active. Each has a tinted background chip
  (`--au-overtime-bg`, `--au-weekend-bg`).
- The **signature gradient** `linear-gradient(118deg, #5B4DF2 → #7C5CF6 → #16C8D6)` fills
  primary buttons, active nav pills, the clock ring, and (clipped to text) big money figures.
  A warm variant exists for special moments. The classic clock even shifts gradient stops by
  **time of day** (dawn / day / dusk / night).

### Type
- **Bricolage Grotesque** — display. Used for titles, the wordmark, stat values, and timers,
  always with tight tracking (`-0.02em` to `-0.05em`) and bold/extrabold weight.
- **Hanken Grotesk** — body & UI. Clean grotesque for everything else.
- Timers/numbers use `tabular-nums` so digits hold position as they tick.
- Eyebrows: `text-xs`, `font-bold`, `uppercase`, `tracking-widest`, in `--au-faint`.

### Shape, depth & texture
- **Radii are generous:** cards `24px` (rounded-3xl), buttons `18px`, inputs/tiles `12–15px`,
  pills fully round. Nothing is sharp.
- **Shadows are soft, large, and tinted indigo** — never neutral grey. The card shadow uses a
  big negative spread (`0 16px 40px -26px rgba(80,64,210,0.34)`) for a lifted, glassy feel.
  A `-glow` variant deepens it on hover.
- **Glass:** the bottom nav and some sheets use `backdrop-filter: blur(22px)` over a
  translucent surface.
- **Aurora mesh + grain:** the clock card layers a slowly-drifting blurred radial-gradient
  "mesh" plus a ~4.5% SVG film grain, giving panels a living, textured glow. The mesh is the
  brand's signature ambient background — not flat color, not photography.

### Motion
- Entrances **fade-up** (`translateY(10px)` → 0) on `cubic-bezier(0.16,1,0.3,1)`, often
  staggered (`stagger-1…5`).
- Progress rings sweep over `1s` on `cubic-bezier(0.3,0.8,0.3,1)`; numbers "count-settle".
- Clock-in fires a one-shot **bloom** ring + haptic. Idle states **breathe** softly.
- **Hover:** subtle — lift to the `-glow` shadow, or background → `--au-surface-sub`, or
  opacity drop (~0.7–0.8). **Press:** scale down `active:scale-[0.98]` (`0.95–0.97` on the
  big clock button). No bounces.
- All decorative loops respect `prefers-reduced-motion`.

### Layout
- **Phone-first.** Content lives in a centered column, `max-width: 28rem` (448px), with
  `~16–20px` gutters and a `pt-12` top safe-area.
- A **fixed frosted bottom nav** (Home / Shifts / Reports / Settings) with a gradient pill
  behind the active icon. Page bottom padding `pb-28` clears it.
- Vertical rhythm is a `gap-4` (16px) stack of cards. Section eyebrows sit above each group.

### Dark mode
First-class. `<html class="dark">` swaps the page to deep navy `#0B1020`, cards to `#151D2E`,
text to near-white, and softens shadows to black. The accent gradient and hue system carry
over unchanged. A pre-hydration script applies the saved theme to avoid a flash.

---

## Iconography

See [ICONOGRAPHY.md](./ICONOGRAPHY.md) — the app uses hand-rolled 2px-stroke line icons
(Feather/Lucide style); **Lucide** is the recommended CDN substitution.

---

## Index — what's in this system

**Foundations**
- `styles.css` — the single entry point consumers link (an `@import` manifest only).
- `tokens/` — `fonts.css`, `colors.css` (light + `.dark`), `typography.css`, `spacing.css`,
  `effects.css` (shadows/glass/grain helpers + `au-*` utility classes), `animation.css`
  (keyframes + entrance utilities).
- `guidelines/` — foundation specimen cards (Colors, Type, Spacing, Brand groups).
- `assets/` — `icon-512.png`, `icon-192.png` (app icon), `logo-mark.svg` (bolt lockup mark).

**Components** — `const { X } = window.ElmtrackrDesignSystem_2c2e11`
- `components/core/` — **Button**, **Card**, **Badge**, **Eyebrow**
- `components/forms/` — **Input**, **Segmented**
- `components/data/` — **StatCard**, **SegmentedBar**, **ProgressRing**
- `components/navigation/` — **BottomNav**
- `components/feedback/` — **Toast**, **EmptyState**

Each component directory holds `Name.jsx` + `Name.d.ts` + `Name.prompt.md` and one
`@dsCard` HTML showing its states.

**UI kits** — `ui_kits/`
- `mobile-app/` — interactive phone recreation: Home (live clock), Shifts, Reports, Settings,
  with light/dark theme switching. Composes the components above.
- `watch-app/` — Wear OS concept board: tile, full app, complication, always-on, history.

**Meta**
- `ICONOGRAPHY.md`, `SKILL.md` (Agent-Skill front matter), this `README.md`.
- `_ds_bundle.js`, `_ds_manifest.json`, `_adherence.oxlintrc.json` are **generated** — never edit.

### Quick start for a new artifact
```html
<link rel="stylesheet" href="styles.css">
<script src="_ds_bundle.js"></script>
<script>
  const { Button, Card, ProgressRing } = window.ElmtrackrDesignSystem_2c2e11;
</script>
```
Pull real assets from `assets/`, follow the voice in *Content fundamentals*, and lean on the
Aurora gradient + indigo-tinted shadows. For deeper fidelity, read the source in
`Elmtrackr-native-android/` or [`Dorvad/elmtrackr`](https://github.com/Dorvad/elmtrackr).
