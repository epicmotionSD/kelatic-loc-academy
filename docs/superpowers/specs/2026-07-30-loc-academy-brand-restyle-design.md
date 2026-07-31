# Loc Academy Brand Restyle — Design

**Date:** 2026-07-30
**Repo:** `C:\Users\shawn\dev\kelatic-loc-academy` (static HTML, no build step, deployed on Vercel)

## Problem

`index.html` is the only page still on the old purple/pink theme. `links.html`,
`chapter-one.html`, and `blueprint-thanks.html` already share the brass-and-ink
KELATIC brand system. A visitor who lands on `/links` and taps through to the
academy page sees two unrelated brands.

Separately, the 10-Week Master Semester still advertises a March 30 start that
has already passed, and the new Kelatic Vitality House site is not linked from
anywhere.

## Goals

1. Restyle `index.html` to the brass/ink brand system used by the other pages.
2. Move the class start date to August 31, 2026.
3. Link Kelatic Vitality House from the `/links` hub and from the academy page.

## Non-Goals

- No change to course content, pricing, deposits, or Stripe checkout URLs.
- No change to `chapter-one.html` or `blueprint-thanks.html`.
- `qr-poster.html` is a print asset and stays on its current design.
- No shared stylesheet extraction. Five static pages, no build step; the churn
  across three working pages is not justified by this change.

## Approach

Replace the `<style>` block inside `index.html` while leaving the DOM structure
and all JavaScript untouched. The Stripe enroll buttons, syllabus modals, FAQ
accordion, and payment chooser are the revenue path — rebuilding the markup to
get a visual result would risk them for no gain.

Markup edits are limited to: copy changes, emoji removal, the theme-toggle
removal, and the new Vitality House links.

## Design System

Tokens copied verbatim from `links.html` so the pages are the same brand, not a
close match:

| Token | Value | Use |
|---|---|---|
| `--ink` | `#26221E` | page background |
| `--ink2` | `#2E2925` | raised surfaces |
| `--silk` | `#F8F4EC` | body text on ink; card background |
| `--ivory` | `#EFE9DD` | secondary surfaces |
| `--brass` | `#A6884E` | borders, rules |
| `--brass-hi` | `#C9A961` | headings on ink, hover |
| `--brass-soft` | `rgba(166,136,78,.45)` | inset card hairline |
| `--cream-dim` | `rgba(239,233,221,.72)` | muted text on ink |

Typography, matching `links.html`:

- **Playfair Display** 500 — headings
- **EB Garamond** — body copy, italic for taglines
- **Jost** 300/400 — eyebrows, buttons, labels, addresses; uppercase with
  `.22em`–`.4em` tracking and matching `padding-left` to offset the trailing gap

Card treatment: `--silk` background, ink text, 4px radius, and the
`.card:before` inset hairline at `inset:7px` with a `--brass-soft` border.

Removed: gradient text fills, purple glow shadows, and the `[data-theme]` light
palette.

## Section-by-Section

**Top banner** — replace the virtual-consultations line with `CLASSES START
AUGUST 31` in Jost uppercase, brass on ink, with a hairline bottom border in
place of the gradient background.

**Header** — `K` monogram, `KELATIC` wordmark at `.14em` tracking, `LOC ACADEMY`
Jost eyebrow. Phone link and "View Classes" button restyled as brass-outlined
Jost. Gains a Vitality House nav link.

**Hero** — copy unchanged. The 👑 placeholder and the emoji feature checks
become brass `◆` marks. Phone CTA becomes a brass-outlined block.

**Course cards** — titles, prices, deposits, feature lists, syllabus buttons,
and all four Stripe URLs unchanged. Silk card treatment with the inset hairline.
The featured card is distinguished by a full `--brass` border rather than a
gradient header. Spot-scarcity badges stay but render as brass Jost text rather
than a 🔥 pill.

The 10-Week Master Semester duration line becomes:

```
August 31 – November 4, 2026 • Mon–Wed, 9 AM – 4 PM • 8 Students Max
```

August 31, 2026 is a Monday; ten Mon–Wed weeks put the final Wednesday on
November 4, 2026.

**Learn / instructor / FAQ / CTA** — restyled only. Emoji icons become `◆`
marks; section badges become Jost eyebrows; FAQ `+` / `−` icons render in brass.

**Footer** — brass-on-ink, Jost address. Address corrected to `9430 Richmond
Ave, Unit D · Houston, TX 77063` to agree with `links.html`, which carries the
unit number. Gains a Vitality House link. Copyright year updated to 2026.

**Ornament** — the `◆ ◆ ◆` divider from `links.html` separates major sections.

## Vitality House Links

`links.html` gains a fourth link card, placed after "Shop Loc Care":

- Title: `Kelatic Vitality House`
- Subtitle: `Plant-based teas, sea moss & smoothies — Houston, TX`
- Href: `https://kelaticvitalityhouse.com`

`index.html` gains the same destination in the header nav (label: `Vitality
House`) and in the footer link row.

Existing `kelatichairlounge.com` destinations on `links.html` are unchanged.

## Removals

- **Theme toggle** — the button, its CSS, and the `toggleTheme()` /
  `localStorage` restore block. The brand system is dark-only; a light mode
  would fight it. This drops the `theme` localStorage key, which nothing else
  reads.
- **Decorative emoji** — ☀️ 🌙 💬 ✨ 👑 📞 🎓 🔥 💳 💡 🧴 🔄 📚 ❓ and any
  others in the modals, replaced by `◆` marks or Jost labels. The floating SMS
  button keeps its behavior and `sms:` href; only its 💬 glyph is replaced.

## Verification

Static site, no test suite. Verify by:

1. Serving the directory locally and loading `/` and `/links` side by side —
   the header, palette, and type should read as one brand.
2. Confirming all four Stripe URLs in `index.html` are byte-identical to their
   pre-change values (`git diff` should show no change on those lines).
3. Opening both syllabus modals, the payment chooser, and the FAQ accordion.
4. Checking the page at a 375px viewport.
5. Confirming no `[data-theme]` selector or `toggleTheme` reference remains.
