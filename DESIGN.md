---
name: Plot Armor
description: An evening streaming guide for episode theories and deliberate spoiler reveals.
colors:
  charcoal: "#111311"
  panel: "#1b1e1a"
  divider: "#343831"
  cream: "#f3f0e8"
  muted: "#a7aca0"
  lime: "#d9ff69"
  primary-ink: "#1c2410"
  lime-hover: "#e8ffa2"
  field: "#12160f"
  field-border: "#414839"
  sleeve-green: "#264c43"
  sleeve-purple: "#44434b"
  sleeve-sage: "#c8caaf"
typography:
  display:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "68px"
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "34px"
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: "-0.025em"
  sleeve:
    fontFamily: "Barlow Condensed, sans-serif"
    fontSize: "64px"
    fontWeight: 700
    lineHeight: 0.85
    letterSpacing: "-0.03em"
  body:
    fontFamily: "DM Sans, sans-serif"
    fontSize: "15px"
    lineHeight: 1.6
  button:
    fontFamily: "DM Sans, sans-serif"
    fontSize: "12px"
    fontWeight: 600
rounded:
  panel: "14px"
  button: "8px"
  field: "6px"
  badge: "4px"
spacing:
  phone-gutter: "20px"
  tablet-gutter: "30px"
  desktop-gutter: "56px"
  card-padding: "20px"
  shelf-gap: "23px"
components:
  button-primary:
    backgroundColor: "{colors.lime}"
    textColor: "{colors.primary-ink}"
    typography: "{typography.button}"
    rounded: "{rounded.button}"
    padding: "13px 19px"
  button-primary-hover:
    backgroundColor: "{colors.lime-hover}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.cream}"
    typography: "{typography.button}"
    rounded: "{rounded.button}"
    padding: "13px 19px"
  input:
    backgroundColor: "{colors.field}"
    textColor: "{colors.cream}"
    rounded: "{rounded.field}"
    padding: "12px 13px"
  market-card:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.cream}"
    rounded: "{rounded.panel}"
---

# Design System: Plot Armor

## Overview

**Creative North Star: "Video-rental staff picks, translated into an evening streaming guide"**

Plot Armor feels like a shelf of episode theories: warm charcoal, acid-lime signals, cream typography, and original poster sleeves made from type and geometry. Human curation comes from the third grounded direction, video-rental staff picks (seed 4182635e), translated to honor the user's pinned streaming-guide shelves and show-poster-style cards. Seven grounded candidates were streaming library, festival programme, video-rental staff picks, watch-party ticket, episode recap magazine, television listings, and cinema lobby. Declined catalog challengers contributed metadata discipline and honest time ordering without replacing episode recognition with abstract catalog codes.

The durable thesis is a shelf of theories for the next episode, with receipts behind a deliberate reveal. The visual path is find an episode, freeze a call, inspect its settlement rules, then reveal when ready. This is a code-led world with no approved image comp. Its interface visibly distinguishes historical rehearsals, recorded proof, and live finalized state. Original sleeve artwork must never imply official studio key art.

**Key Characteristics:**
- Condensed sleeve-scale titles paired with quiet sans-serif reading text.
- Flat charcoal panels, fine dividers, and lime actions.
- Streaming shelves with explicit historical and recorded-state labels.
- Spoiler evidence behind a deliberate reveal, with a global shield reset.

## Colors

An evening neutral field carries one functional lime accent; muted sleeve colors identify shows without competing with actions. Frontmatter owns exact token values.

### Primary

Acid Lime (`lime`) marks primary actions, active navigation, shield controls, and selected predictions. `primary-ink` supports readable text on it; `lime-hover` signals hover.

### Secondary

Sleeve Green, Sleeve Purple, and Sleeve Sage belong to original poster art. They are not extra action colors.

### Neutral

Warm Charcoal (`charcoal`) grounds the page; Evening Panel (`panel`) groups cards and forms. Cream (`cream`) carries headings and reading text; Quiet Sage (`muted`) carries supporting metadata. Fine Divider (`divider`) separates shelves and panel edges. `field` and `field-border` distinguish editable surfaces.

**The Signal Rule.** Reserve lime for actions, state, and the established spoiler-explanation panel; avoid spreading it across every card.

## Typography

Barlow Condensed supplies display headings, the wordmark, and sleeve titles. DM Sans supplies prose, questions, controls, and metadata. Both use sans-serif fallbacks.

Display is large and compact; body text stays calm. Page titles use the display token on desktop and reduce to (47px) on phones. General section headings use the headline token; shelf headings use (31px) on desktop and (28px) on phones. Sleeve titles use the sleeve token, becoming (72px) in the phone shelf. Card questions use DM Sans (17px desktop, 18px phone); body becomes (14px) on phones. Metadata uses compact (8-12px) sizes according to hierarchy and remains secondary.

**The Useful Label Rule.** Show, season, episode, status, and historical labels convey information. Do not add ornamental eyebrow copy above page headings.

## Layout

The main container has a maximum width of (1440px), desktop side gutters from `desktop-gutter`, and a three-column shelf using `shelf-gap`. At (1100px) and below gutters switch to `tablet-gutter`; at (740px) and below they use `phone-gutter`, shelves become one column, filters wrap above search, and navigation moves to a second header row. The global shield action remains available on phones as an icon with an accessible name.

Forms use a main form and explanatory aside on desktop, stacking on phones. Detail content uses a poster beside the question and prediction controls, with rules and claim panels below; these stack on phones. Proof contracts use four columns, then two at the intermediate breakpoint, then one on phones. Long hashes wrap.

The intended live first viewport is a compact header followed by an episode-led feature and shelf, without a marketing hero. The current release has no finalized upcoming market because validator Wikipedia fetching has failed. Built truth therefore uses a compact factual no-live notice and proceeds directly to historical sleeves; it does not reserve a tall empty feature or duplicate empty shelf. A populated live feature remains conditional and is not demonstrated by the current captures.

## Elevation & Depth

Depth comes from tonal layering and fine one-pixel borders, without a card-shadow vocabulary. Poster art clips inside cards; concealed-result decoration uses a blurred abstract placeholder behind an explicit shield action. This decoration must not carry concealed evidence into visible content. Focus uses a lime outline (2px) with an offset (5px).

Motion is small and functional: buttons transition background, color, and position over (.16s); an enabled press moves down (1px), and poster hover scales to (1.015) over (.3s). Reduced-motion preference disables transitions, animation, and smooth scrolling.

## Shapes

Panels use `panel` rounding; buttons, inputs, and badges step down through the corresponding rounded tokens. Original sleeves use large typography with rotated lines, planes, or concentric rings rather than photographic studio imagery. Thin borders and restrained corners preserve the streaming-guide atmosphere.

## Components

- **Buttons:** Lime primary actions and outlined secondary actions share compact bold DM Sans text and a default minimum height of (44px). Disabled controls lower opacity and show an unavailable cursor. Preserve visible keyboard focus.
- **Fields:** Dark inset surfaces, fine borders, explicit labels, and cream values; placeholders supplement labels. Textareas resize vertically.
- **Navigation:** Muted links become cream when active, with a lime bottom rule. Phone navigation stays visible on its own row.
- **Episode sleeves and cards:** Original geometric artwork anchors recognition. Concise shelf questions remove broadcast ISO strings and repeated option lists; the detail H1 preserves the full submitted question. Show/season/episode metadata and historical badges remain explicit.
- **Spoiler shield:** Results and evidence appear only after the reveal action. The global header action derives its visible state and accessible name from revealed results or scores, and resets both. The phone icon preserves that action. The source-and-capture review does not certify interactive revealed-state behavior.
- **Notices and empty states:** Compact factual no-live notice on Discover; contextual wallet and activity empty states offer a next action. Never promote historical rehearsals into live forecasts to fill a layout.
- **Receipts:** Contract panels, wrapping hashes, transaction rows, and expandable read-back preserve evidence hierarchy. Read-back explicitly warns that it may contain spoilers.

Documentation evidence is `components/app.tsx`, `app/globals.css`, and the ten final JPEG captures under `.impeccable/review/`: desktop/mobile Discover, Propose, Predictions, Activity, and Proof. Captures used actual (1280 x 720) and (390 x 844) viewports and include full-page content. `reviewer.md` requested four fixes; `verdict.md` scored all four resolved and returned **ship at that four-fix scope only**. The supplied one-time detector result was `[]`. Exact (1440 x 960) rendering, market-detail captures, wallet-populated states, extension signing, backend correctness, and release readiness were not verified by that verdict.

## Do's and Don'ts

- Do keep original typographic sleeves, streaming shelves, and explicit historical labels.
- Do show concise shelf questions and preserve the full submitted question in detail.
- Do keep result evidence behind explicit reveal and provide the global shield reset on phones.
- Do represent unavailable live content with the compact factual notice.
- Don't add ornamental pre-heading eyebrows.
- Don't present original sleeves as official studio artwork.
- Don't use historical rehearsals as live competitive forecasts.
- Don't treat the four-fix visual verdict as proof of wallet signing or whole-release readiness.
