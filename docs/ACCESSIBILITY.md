# Accessibility — WCAG 2.2 AA

Target: WCAG 2.2 level AA on every page, designed from a 320 px phone upward.

## What is built in

| Area | Implementation |
|---|---|
| Structure | One `<h1>` per page, no skipped heading levels (`tools/seo-check.py` warns on skips), landmarks `header` / `nav` / `main#main` / `footer`, skip link first in every page |
| Keyboard | Every control is a real link or button. Dropdown triggers are buttons with `aria-expanded` + `aria-controls`; Escape closes menu, dropdowns and the search dialog; focus returns to the opener |
| Focus | 3 px indigo ring (13.7:1 on cream) and a gold ring on dark surfaces (8.8:1). Sticky headers use `scroll-margin-top` so a focused element is never hidden under them (2.4.11) |
| Search | Native `<dialog>` (focus trap, Esc, inert page). Arrow keys move through real links; results are announced in a live region |
| Menu | Closed menu is `visibility:hidden`, so it is out of the tab order and the accessibility tree |
| Touch targets | Primary controls 44 × 44 px; outbound source links padded to 44 px; nothing below the WCAG 2.5.8 24 px minimum |
| Colour | All text pairings computed (`tools/qa/contrast.py`), every one ≥ 4.5:1. Status is never colour-only: each badge carries a glyph and a word |
| Motion | `prefers-reduced-motion` disables transitions and reveal animations; no autoplaying motion |
| Tables | Wrapped in a focusable, labelled `role="region"` scroller so a wide table scrolls inside itself (1.4.10 reflow) |
| Forms | Visible labels (the home search label is visible, not placeholder-only); search is `role="search"` |
| Images | Descriptive `alt` where the image carries meaning, empty `alt` where a card's heading already names it; width/height on every content image |
| Disclosure | FAQs use native `<details>/<summary>` |
| Language | `lang="en"` on every page |

## Honest status

* **Accessibility of places is not claimed.** `/accessible-nashik/` marks every place *accessibility unknown* until it is verified (see `data/accessibility.json`).
* The legacy guides were hand-written; their heading hierarchy, table scrolling, contrast and image attributes were corrected in this phase, but they have **not** had a screen-reader pass.
* **Video:** the site publishes none. If video is added, captions and a transcript are required before publishing.

## How it is tested

```bash
python3 tools/qa/contrast.py                                  # computed contrast of every colour pairing
npm install --no-save axe-core
node tools/qa/a11y.js --widths 360,1280 --open-search        # axe, WCAG 2.0–2.2 A/AA + best practice, incl. open dialog and menu
node tools/qa/interactions.js                                 # keyboard, dialog focus return, menu, skip link
node tools/qa/viewports.js                                    # overflow, tap targets, CLS at 320–1920 px
node tools/qa/no-javascript.js                                # content and links without JavaScript
```

## Last full run (4 Oct 2026, headless Chromium 1.56 against a production-like server)

| Check | Result |
|---|---|
| axe-core 4.13, WCAG 2.0–2.2 A/AA + best practice, 46 pages × 360 and 1280 px, each with the page, the open search dialog and the open mobile menu | 0 violations (54 colour-contrast findings on legacy guides were fixed first) |
| Interaction suite (search dialog, menu, filters, expiry, Kumbh phases via a mocked clock, weather success and failure, keyboard) | 59 passed, 0 failed, 0 page errors |
| Layout sweep, 46 pages × 10 widths (320, 360, 375, 390, 414, 768, 1024, 1280, 1440, 1920) | 460 combinations, 0 horizontal overflow, 0 load failures, 0 images without dimensions |
| Layout shift / paint | worst CLS 0.0066; worst LCP 516 ms on localhost (not a field measurement) |
| Targets under 44 px | Gallery dots on one guide (24 × 24 px, which meets WCAG 2.2 AA 2.5.8) and one 41 px inline link; both are below the stricter 44 px guideline |
| Search relevance | 13 of 13 brief queries return the expected page first |
| No-JavaScript | content and links present; only phase-gated blocks (live band, post-Kumbh section) are hidden, by design |
| Unit tests / SEO audit | 38 tests pass; 0 errors, 39 title/description-length warnings |

The only console errors were blocked third-party requests from the sandbox's TLS proxy.

## Manual checks still to do (automation finds about a third of problems)

1. Tab through the home, a destination page, the Kumbh hub, `/search/` and `/updates/` at 320 px and 1280 px; confirm order matches reading order.
2. With VoiceOver (iOS/macOS) and TalkBack/NVDA: open the menu, the search dialog, an FAQ, a status badge, a table region.
3. Zoom to 200 % and 400 % (1.4.4, 1.4.10): no loss of content or horizontal page scroll.
4. Windows High Contrast / forced-colors: badges and focus rings remain visible.
5. Review any new hand-written HTML against this list before publishing.
