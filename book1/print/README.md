# Empty Origin — complete print interior

**Editorial-version notice:** The active manuscript was subsequently revised to 97,048 words on September 24. These print files represent earlier snapshots and do not include the changes recorded in [the revision record](../REVISION_2026-09-24.md). A new source snapshot and print build are needed after the pending alternate-beginning reviews are addressed.


The current full-book layout is **EMPTY_ORIGIN_5.5x8.5_PRINT_INTERIOR.pdf**.
The full manuscript is typeset from the September 24 print snapshot: 32 chapters,
96,691 whitespace-counted source words, including the accepted Chapter One revision.
The snapshot matches the active chapters and working draft. Typesetting changes no prose.
The completed interior has **366 physical pages**: two front-matter pages and
364 numbered story pages. The September 20 frozen beta/ARC master is retained.
For the original comparison with 6 × 9 inches and smaller trims, see
[TRIM_SIZE_RECOMMENDATION.md](TRIM_SIZE_RECOMMENDATION.md).

## Review files

- `EMPTY_ORIGIN_5.5x8.5_PRINT_INTERIOR.pdf`: complete 5.5 × 8.5 interior, 366 physical pages.
- `proofs/EMPTY_ORIGIN_LAYOUT_REVIEW.pdf`: selected opener, body, System, and page-turn proofs.
- `proofs/ART_SPACING_COMPARISON_2026-09-24.pdf`: historical 6 × 9 art correction comparison.
- `proofs/EMPTY_ORIGIN_CHAPTER_01_LAYOUT_PROOF.pdf`: the complete first chapter, extracted from the full interior.
- `proofs/chapter-01-opener.png`, `chapter-12-opener.png`, `body-page.png`: readable previews.
- `proofs/contact-01.jpg` through `contact-08.jpg`: thumbnails of every physical page.
- `PRINT_VALIDATION.json`: machine-readable preflight results.
- `EMPTY_ORIGIN_5.5x8.5_PRINT_INTERIOR.manifest.json`: source/font/art hashes and per-page placement map.
- `sources/EMPTY_ORIGIN_PRINT_MASTER_2026-09-24.md`: reproducible source snapshot.
- `EMPTY_ORIGIN_6x9_PRINT_INTERIOR.pdf` and its manifest: retained 332-page prior edition;
  its original preflight is archived as `EMPTY_ORIGIN_6x9_PRINT_VALIDATION.json`.

## Design authority

The author's September 24 correction makes `layout_sample.jpeg` the authority
for the ring artwork and opener proportions. The 5.5 × 8.5 layout retains the
kit’s body typography and margins, and recomposes the opener to fit the selected trim. The former simplified ring has been replaced.

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
- Reference-derived chapter aperture, 18 pt tracked chapter headings, and a raised
  31 pt initial, including quoted openings. The enlarged initial rises above the
  baseline without adding space below the first line.
- Opener artwork begins 20 pt from the top and spans 170 pt including splatter.
  Numerals are 47 pt on a baseline 123 pt from the top. Chapter title baseline
  is 201 pt; metadata baselines are 231/249 pt. Opening paragraph flow begins
  at 264 pt, retaining the reference’s generous sink on the smaller page.
- Text column is 296.64 pt (4.12 inches) wide. Body type remains 11.35 pt;
  this is a fresh composition at the selected trim, not a scaled PDF.
- Flush-left prose after chapter openings and scene ornaments; preserved italic passages.
- Chapter openings begin on the next page, not necessarily a recto.
- Long unprotected paragraphs may continue at a sentence boundary, with at least
  two lines on each page and no indent on the continuation. Sentences never split
  across page turns. The print source's paragraph boundaries remain unchanged.
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
The book ends on a verso; the builder adds a final blank only when needed for an
even physical page count. The existing Scribus SLA remains a historical 6 × 9
three-page starter; the complete editable 5.5 × 8.5 layout is the Python source.

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
It refuses to build if the active chapters or working draft no longer match the
September 24 print snapshot. Later accepted text revisions need an explicit new snapshot.

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

The 5.5 × 8.5 layout has 21.12 pt average unused space on ordinary pages,
95.98 pt maximum, and 18 ordinary pages with more than 60 pt unused. These
measurements exclude chapter openings, endings, and the two explicit Chapter One
page turns. Protected reveals and complete sentences can leave bottom whitespace;
text is not stretched vertically to hide it.

Visual review covered all eight contact sheets plus full-size title, opening, body,
long-heading, dense-System, and short-ending pages. The actual 366-page result
supersedes the recommendation’s rough 390–410-page estimate. Print physical proofs
at 100% / actual size to assess type comfort and gutter space before publication.
