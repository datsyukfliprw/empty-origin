# Empty Origin — complete print interior

The current full-book layout is **EMPTY_ORIGIN_6x9_PRINT_INTERIOR.pdf**.
The full manuscript is typeset from the September 20 frozen master: 32 chapters,
96,693 whitespace-counted source words. No manuscript prose has been changed.

## Review files

- `EMPTY_ORIGIN_6x9_PRINT_INTERIOR.pdf`: complete 6×9 interior, 332 physical pages.
- `proofs/EMPTY_ORIGIN_LAYOUT_REVIEW.pdf`: selected opener, body, System, and page-turn proofs.
- `proofs/ART_SPACING_COMPARISON_2026-09-24.pdf`: before/corrected Chapter 1 and 12 spreads.
- `proofs/EMPTY_ORIGIN_CHAPTER_01_LAYOUT_PROOF.pdf`: the complete first chapter, extracted from the full interior.
- `proofs/chapter-01-opener.png`, `chapter-12-opener.png`, `body-page.png`: readable previews.
- `proofs/contact-01.jpg` through `contact-07.jpg`: thumbnails of every physical page.
- `PRINT_VALIDATION.json`: machine-readable preflight results.
- `EMPTY_ORIGIN_6x9_PRINT_INTERIOR.manifest.json`: source/font/art hashes and per-page placement map.

## Design authority

The author's September 24 correction makes `layout_sample.jpeg` the authority
for the ring artwork and opener proportions. The Scribus kit continues to govern
body typography and page margins. The former simplified ring has been replaced.

`assets/aperture_from_reference.svg` traces the actual ink in the supplied image,
including its irregular edges and splatter. The trace excludes the sample's number
12 and paper tone; chapter numbers are typeset separately. It adds no invented
strokes. Source coordinates, hashes, and the method are recorded in the adjacent
JSON file and `trace_reference_ring.py`. The screenshot limits the available ink
detail; vector export does not invent missing high-resolution detail. The same
trace also replaces the Scribus kit's ring and the legacy standalone PNG preview.

- EB Garamond 11.35/13.55 body, 14.5 pt paragraph indent, justified with English hyphenation.
- Noto Sans Condensed System/chat/metadata; Noto Serif numerals and folios.
- Mirrored 0.76 inch inside / 0.62 inch outside margins; 0.54 inch top / 0.62 inch bottom.
- White page, black ink only, no running heads, no bleed or crop marks.
- Reference-derived chapter aperture, 20 pt tracked chapter headings, and a raised
  31 pt initial, including quoted openings. The enlarged initial rises above the
  baseline without adding space below the first line.
- Opener artwork begins 23 pt from the top and spans 190 pt including splatter.
  Chapter title baseline is 225 pt; metadata baselines are 259/279 pt. Opening
  paragraph flow begins at 300 pt, matching the reference's generous sink.
- Flush-left prose after chapter openings and scene ornaments; preserved italic passages.
- Chapter openings begin on the next page, not necessarily a recto.
- Long unprotected paragraphs may continue at a sentence boundary, with at least
  two lines on each page and no indent on the continuation. Sentences never split
  across page turns. The frozen source's paragraph boundaries remain unchanged.
- Consecutive System lines, their immediate reaction, and short multi-stage reveal
  bridges stay together. Scene ornaments stay with the following prose.
- Short setup/payoff and question/answer groups receive bounded keep-together rules,
  limited to avoid large accidental blank areas.
- Consecutive System rows use 10.9 pt leading, with 5 pt space around the group;
  spacing is not added again between each row.
- Chapter 1's Vharos shout ends folio 1. `My eyes open.` ends a page; the alien sky starts the next.

Chapter metadata reflects the current manuscript, not the illustrative text in the
screenshot: Chapter 9 is GREYWARD, Chapter 10 ROAD TO ROOK, Chapters 11–23 ROOK,
Chapters 24–25 EAST RELIEF WORKS, and the remaining chapters ROOK. RUN describes
Maya's state at chapter opening: UNSET through Chapter 10, WARDER from Chapter 11.

The title page is followed by a deliberately blank verso. Publication-specific
copyright/ISBN/dedication/back matter were not supplied and have not been invented.
A final blank verso makes the physical page count even. The existing Scribus SLA
remains a three-page starter; the complete editable layout is the Python source.

## Rebuild

From the repository root, using Python 3.12 or later:

```bash
python -m venv .venv-layout
.venv-layout/bin/pip install -r book1/print/requirements.txt
.venv-layout/bin/python book1/print/build_print_interior.py
.venv-layout/bin/python book1/print/validate_print_interior.py
```

Dependencies are needed only at setup. Subsequent builds need no network, GUI,
image generation, or model calls. Fonts are bundled with their OFL licenses and
source/instance hashes in `assets/fonts/SOURCES.json`. The builder works from any
working directory and produces deterministic PDF bytes in the same environment.
It refuses to build if the active chapters no longer match the frozen master.

The GitHub workflow builds, validates, and uploads artifacts; it no longer commits
PDFs back automatically. The Chapter 1 proof wrapper uses the full-book builder,
so it cannot drift into a different typography or tinted background.

## Validation scope

All pages are rendered. Checks cover exact trim, embedded fonts, black-only ink,
text bounds, block overlap, mirrored margins, chapter bookmarks, source hashes,
ordered text fidelity, scene/System grouping, and the explicit Chapter 1 page turns.
Text comparison normalizes Unicode compatibility forms, whitespace, and hyphens
(to accommodate automatic hyphenation); all other characters are compared in order.
The placement map verifies complete source ranges, including sentence-boundary
continuations, without duplicated or missing text. Checks also cover the raised
initial's baseline spacing, System row spacing, and reference artwork provenance.
Contact sheets and selected full-size pages are used for visual review; automated
preflight is not a line-by-line editorial reread or a physical print proof.

The art/spacing correction reduced the largest unused area on ordinary pages from
212.2 pt to 91.3 pt, and the number of ordinary pages with more than 60 pt unused
from 47 to 28. These measurements exclude chapter openings, endings, and the two
explicit Chapter 1 page turns. Protected reveals and complete sentences can still
leave some bottom whitespace; text is not stretched vertically to hide it.
