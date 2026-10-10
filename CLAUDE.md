# Joshua Baller — Selected Portfolios (interactive gateway page)

## What this is
A one-page, static HTML version of Joshua Baller's "Selected Portfolios" gateway PDF
(`reference/Joshua_Baller_Selected_Portfolios.pdf`, 1920 x 1080). It introduces Joshua and
sends visitors to three separate portfolios through clickable thumbnails. It is a lightweight
gateway, not a portfolio itself. No frameworks, no build step: `index.html` + `assets/`.

Joshua is a multidisciplinary designer (branding, logo, visual identity, UI) in Metro Manila.
He is a designer, so visual details matter. Keep copy casual-professional, warm, concise.

## Run it
    python3 -m http.server 8000     # then open http://localhost:8000
or just open `index.html` in a browser. Inter loads from Google Fonts (fallback: Helvetica Neue).

## Files
- `index.html`        all markup + CSS (inline, no JS needed)
- `assets/*.jpg`      optimized artwork, about 640 KB total. Only supplied artwork; never generate replacements.
- `assets/case-study/page-01..15.webp`  the 15 campaign case study pages shown in its flipbook (1600 px wide, about 1 MB total)
- `assets/presentation/page-01..09.webp` the 9 Presentation Design portfolio pages shown in its flipbook (about 0.6 MB total)
- `assets/branding/page-01..18.webp`     the 18 branding portfolio pages shown in its flipbook (about 1.3 MB total; source PDF is 1920 x 1080)
- `reference/`        the finished PDF and the Python script that built it (source of truth for layout intent)

## Do not change without asking Joshua
- Copy: headline, intro, the three card titles/descriptions, link labels (`View branding portfolio ↗`,
  `View presentation portfolio ↗`, `View campaign case study ↗`), contact details.
- Links (all open in a new tab):
  - Branding: opens the in-page flipbook (see below). The label uses `href="#branding"`; there is no Drive link on them.
    (Old Drive URL, now unused: https://drive.google.com/file/d/1nbz-2EZG-4Goj-G-L_njkj0Jlnt62MLH/view?usp=sharing)
  - Presentations: opens the in-page flipbook (see below). The label uses `href="#presentations"`; there is no Drive link on them.
    (Old Drive URL, now unused: https://drive.google.com/file/d/1yVroiQ2rTMrIW6OhgdXgeHQ7R5eB4bjh/view?usp=sharing)
  - Social campaign: opens the in-page flipbook (see below). The label uses `href="#case-study"`; there is no Drive link on them.
    Visiting `index.html#case-study` opens the flipbook on load. (Old Drive URL, now unused:
    https://drive.google.com/file/d/1niZ-RM92YBTyM1elVjxVlBRXOak-WtKt/view?usp=sharing)
  - Email: mailto:hello@joshuaballer.com  ·  Site: https://joshuaballer.com
- Palette: bg #F5F5F2, ink #202020, secondary #70706C, rules #DDDDD7. Inter / Helvetica Neue.
  Neutral editorial look: no gradients, decorative shapes, device mockups, heavy shadows or card chrome.
  The artwork supplies the colour.
- No unsupported claims (achievements, metrics, credentials). Presentation and campaign work are
  self-initiated concepts, not commissioned client work. Do not imply otherwise.
- Do not add the resume as a thumbnail.

## Design rules that already hold
- Thumbnail frame aspect is 558.67:317.7 (about 16:9). The frames are display-only `<div class="thumb">` elements: they keep the hover
  animation (tile zoom + project caption) but are NOT clickable and not focusable. The "View ... ↗" label link below each frame is the
  only way into a flipbook (and the only keyboard target).
- Branding: Crosby dominant, Renumerate + Revin supporting (cropped, `object-fit: cover`).
- Presentations: 2 x 2 of the four deck covers (Relay, Signal, Briefly, Forma), each 16:9.
- Campaign: launch post stays exactly 4:5 (grid column 45.49%), promo 16:9, storyboard frame 1:1 seated on
  its own cream (#F4F0E7). Nothing is cropped (`object-fit: contain`). Do not crop headlines or the speaker's face.
- Interaction is deliberately small: tile zoom + project caption on hover, arrow nudge on the card link, visible
  focus rings, `prefers-reduced-motion` respected. One brief staggered load reveal (about 1s, `settle` keyframes, delays via `--d`), skipped under reduced motion.
- Type and spacing are fluid (`clamp()` against vw) and match the 1920 PDF at 1920px wide. Single column at <= 900px.
- Fits 1920 x 1080 with no scroll. Re-check after any spacing change.

## Flipbooks (branding, presentation, campaign case study)
All three cards open a full-screen `<dialog id="flipbook">` instead of an external link. The trigger (the "View ... ↗" label only;
thumbnails are display-only) carries `data-flipbook="branding" | "presentation" | "case-study"`; the script at the bottom of `index.html` holds a `BOOKS`
object with each document's title, pages (`src`, `title`, `links`) and a `HASHES` map for deep links.
- `branding`: `Joshua_Baller_Senior_Brand_and_Web_UI_Designer_-_Design_Portfolio_Aug2026.pdf`, 18 pages (cover, index, about,
  14 projects, contact), deep link `#branding`. Hotspots: 15 external links (each project's site on pages 4 to 17, LinkedIn on 18)
  plus about 268 internal jump links (the Index page and the sidebar menu on each page) that move inside the flipbook.
- The source PDF has no link for Psychecare anywhere except its own page: the "04 Psychecare" tile on the Index page and the
  "Psychecare" sidebar entry on every other page were unlinked. Those 16 jump hotspots are added in `BOOKS.branding` (hand-added,
  not from `get_links()`), so rebuilding pages from the PDF must re-add them. Sidebar audit: 256 entries, all correctly linked.
- `presentation`: `Presentation_Design_Portfolio.pdf`, 9 pages (overview + Relay, Signal, Briefly, Forma, two pages each),
  deep link `#presentations`. 4 "View full presentation" links kept as hotspots on pages 3, 5, 7, 9.
- `case-study`: `Brand_Momentum_Week___Portfolio_Case_Study.pdf`, 15 pages, deep link `#case-study`.
  8 PDF links kept as hotspots (Figma Config and UX+ on page 4, six full-resolution asset links on pages 7 to 12).
- Single-page flipbook with a page-turn (leaf rotates about its left edge, Web Animations API; end frames are cancelled
  after each turn so no shading lingers). Controls: prev/next, page bar, arrow keys / PageUp / PageDown / Home / End,
  swipe, mouse wheel / trackpad scroll, Esc or Close. Focus returns to the link that opened it.
- Scroll navigation: wheel or two-finger scroll down/right = next page, up/left = previous (listener on the dialog, `passive: false`,
  Ctrl+wheel left to the browser for pinch-zoom). One page per scroll gesture: deltas are summed (threshold 40), then further events are
  ignored until scrolling pauses for 160 ms, which absorbs trackpad inertia. A brief "Scroll or use the arrow keys" hint shows on the first
  open for mouse users only. Verified: single notches, trackpad bursts and decaying tails, ends of the book, reduced motion.
- Hotspot types in `links`: external (`href`, opens a new tab, keyboard-focusable) and internal (`page`, 1-based; jumps inside the book,
  `tabindex=-1` and `aria-hidden` because the page bar gives keyboard users the same jumps). Coordinates are percentages of the page.
- Respects `prefers-reduced-motion` (pages swap instantly). Portrait phones show a "rotate your phone" hint.
  The stage is fixed at 16:9; every source PDF is 16:9. A different page shape would need a per-book aspect ratio.
- To change a document: re-render its pages and rebuild its `pages` array. With PyMuPDF:
  `page.get_pixmap(matrix=pymupdf.Matrix(1600/page_width, 1600/page_width))` for images, `page.get_links()` for hotspots
  (external: `uri`; internal: `kind == pymupdf.LINK_GOTO`, `page`), dividing rect values by the page size for percentages.
- Keep each document's own disclosures intact (fictional companies, self-initiated concepts, AI-assisted process notes, no results reported).

## Verify after edits
- No horizontal scroll at 1920, 1440, 820, 390 px wide.
- All 8 link targets correct (3 thumbnails, 3 labels, email, site). All three open flipbooks.
- Flipbooks (all three): open from the "View ..." label (thumbnails are not clickable), turn forward and back (buttons, keys, swipe, scroll wheel), page-bar jump works, Esc closes, PDF hotspots open in a new tab, deep links work.
- Images sharp, undistorted, no clipping on the campaign tiles.
- Page weight stays small (artwork about 640 KB, flipbook pages about 2.9 MB in total, loaded as a viewer opens).

## Reasonable next steps (ask before doing)
- Self-host Inter (woff2) instead of Google Fonts.
- Add a social/OG preview image and meta tags.
- Deploy (e.g. Netlify, Vercel, GitHub Pages) and update joshuaballer.com.
- Replace Drive links with permanent project URLs if Joshua publishes the portfolios on his own site.
- Drive links need sharing set to "Anyone with the link"; remind Joshua to test in a private window.
