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

Forms use a main form and explanatory aside on desktop, stacking on phones. Detail content uses a poster beside the question and prediction controls, with rules and claim panels below; these stack on phones. Proof contracts use four columns, then two at the intermediate breakpoint, then one on phones. Long hashes wrap. In populated phone prediction cards, the question occupies a full row and actions sit below; desktop rows retain their horizontal layout.

The live first viewport is a compact header followed by an episode-led feature and shelf, without a marketing hero. The current recorded release contains two live War markets and four historical rehearsals. Discover conditionally features the first live market with bold outcome actions, then separates the live and historical shelves. Only when no live market exists does a compact factual no-live notice replace the feature; the live shelf is then omitted. Search and show filters use contextual no-match messages rather than promoting historical records into live forecasts.

## Elevation & Depth

Depth comes from tonal layering and fine one-pixel borders, without a card-shadow vocabulary. Poster art clips inside cards; concealed-result decoration uses a blurred abstract placeholder behind an explicit shield action. This decoration must not carry concealed evidence into visible content. Focus uses a lime outline (2px) with an offset (5px).

Motion is small and functional: buttons transition background, color, and position over (.16s); an enabled press moves down (1px), and poster hover scales to (1.015) over (.3s). Reduced-motion preference disables transitions, animation, and smooth scrolling.

## Shapes

Panels use `panel` rounding; buttons, inputs, and badges step down through the corresponding rounded tokens. Original sleeves use large typography with rotated lines, planes, or concentric rings rather than photographic studio imagery. Thin borders and restrained corners preserve the streaming-guide atmosphere.

## Components

- **Buttons:** Lime primary actions and outlined secondary actions share compact bold DM Sans text and a default minimum height of (44px). Disabled controls lower opacity and show an unavailable cursor. Preserve visible keyboard focus.
- **Fields:** Dark inset surfaces, fine borders, explicit labels, and cream values; placeholders supplement labels. Textareas resize vertically.
- **Navigation:** Muted links become cream when active, with a lime bottom rule. Phone navigation stays visible on its own row.
- **Episode sleeves and cards:** Original geometric artwork anchors recognition. Concise shelf questions and detail H1s remove broadcast ISO strings and repeated option lists. The raw immutable question remains in the collapsed native “Exact submitted question” disclosure inside “How this settles”; formatted broadcast dates and bold option controls remain separately visible. Show/season/episode metadata and historical badges stay explicit.
- **Spoiler shield:** Results, quotes, historical definitions/propositions, and revision links stay behind deliberate reveal. The global header action derives its visible state and accessible name from exposed results, scores, standings, or claims, then clears those exposed views. A shared request epoch prevents pending reveal responses from restoring concealed content after reset. The phone icon preserves that action. Supplied frontend interaction records cover reveal/hide, refresh, and reset behavior; older revealed captures document behavior only and are not final visual authority.
- **Standings:** A labeled Overall/season selector scopes the theory table. Changing scope clears the old rows; standings remain an explicit reveal action and the global shield clears them.
- **Notices and empty states:** Phase-appropriate no-live, no-match, no-wallet, no-predictions, and no-activity states describe what is missing and offer a relevant next action. Never promote historical rehearsals into live forecasts to fill a layout.
- **Receipts:** Contract panels, wrapping hashes, transaction rows, and expandable read-back preserve evidence hierarchy. Read-back explicitly warns that it may contain spoilers. The Proof page presents the submitted pool’s 2 GEN PAID demonstration, with canonical pool, claim-parent and credited-native-child links. Its market page labels this as a recorded release-wallet payout, distinct from the connected viewer’s claim. The old 11 wei payout remains previous-deployment history in the manifest and release report.

Documentation evidence is `components/app.tsx`, `app/globals.css`, `lib/domain.ts`, and all fourteen current JPEG captures under `.impeccable/review/`: `desktop.jpg` / `mobile.jpg` for Discover, plus desktop/mobile pairs for Propose, Predictions, Activity, Proof, live market detail, and historical market detail. `flow-checks.json` records actual (1440 x 960) and (390 x 844) viewports with no horizontal overflow across those routes after the detail minimum-width correction. `final-reviewer.md` reviewed the complete current capture set and requested one detail-heading hierarchy fix; `final-verdict.md` scored that fix resolved and returned **ship at that fix scope only**. The four detail captures were refreshed after the concise-heading correction; older reviewer/verdict files are previous-release evidence. The supplied one-time detector result was `[]`; no second detector ran. This code-led review has no approved image comp or comparative quality-bar image. Wallet signing completion, populated personal pages, browser-submitted transaction reload, backend consensus, and whole-release readiness are outside this visual verdict. Separate browser evidence now records owner-selected MetaMask connection and signing of the zero-value YES prediction for market-2: Activity showed ACCEPTED with an appeal deadline, preserved the hash after reload, then showed FINALIZED SUCCESS. The targeted independent verifier confirmed the correct PlotSeasons contract, zero value, actual personal prediction, and real Explorer API record (transaction 0xcb36e99d7a9c893fa3821b042cf79c009fc7bc83709d03655c5cae1f9072bd4e; `docs/browser-verifier-output.txt`: PASS). A subsequent owner-account reconnect and Refresh my predictions displayed the actual War episode 5 question, “Your call YES,” View market & claims, and Sync finalized score without an error. Personal scores initially remained shielded behind Reveal my scores; the owner then revealed 0 points, current/best streak 0, and a PENDING 0-point row, and Restore spoiler shield hid them again. Activity displayed FINALIZED SUCCESS and a Finalized state read-back disclosure containing market-2, option 0, War season 1, SHIELDED status, and 0 points; the disclosure remained available after reload without a new transaction or signature. This verifies the pending owner-prediction and score reveal/reset flow; terminal winner claims and settled personal outcomes remain untested because the future market is pending. The Activity read-back cancellation correction has its own eleventh application regression test. Separate populated Activity/Predictions checks at (1440 x 960) and (390 x 844) report no overflow in `.impeccable/review/wallet-flow-checks.json`; the viewed `artifacts/mobile-wallet-predictions.jpg` confirms the phone prediction question uses a full (308px) row with actions below. These four populated-state checks do not expand the original fix-only visual review. This targeted browser/transaction evidence and application-test results are separate from the fix-only design verdict.

## Do's and Don'ts

- Do keep original typographic sleeves, streaming shelves, and explicit historical labels.
- Do show concise shelf and detail headings and preserve the immutable question in its labeled disclosure.
- Do keep result evidence behind explicit reveal and provide the global shield reset on phones.
- Do feature actual live markets and use the compact factual notice only when none exists.
- Don't add ornamental pre-heading eyebrows.
- Don't present original sleeves as official studio artwork.
- Don't use historical rehearsals as live competitive forecasts.
- Don't treat the detail-heading fix verdict as proof of wallet signing or whole-release readiness.
