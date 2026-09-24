# Empty Origin — Print Interior Style Guide

**Production update (September 24, 2026):** The author selected **5.5 × 8.5 in**.
The complete 366-page interior and regenerated proofs are documented in
[README.md](README.md). The ring remains traced from `../../layout_sample.jpeg`;
the opener has been recomposed for the smaller trim. The approved September 24
print snapshot supplies the prose and metadata. The Scribus kit is a historical
6 × 9 starter; the Python builder is the current complete editable layout.

**Visual authority:** `layout_sample.jpeg`, supplied for the September 24 ring
correction. Dimensions below govern its adaptation to the selected trim.

## Format
- Trim: **5.5 × 8.5 in** (396 × 612 pt)
- Interior: black-and-white, designed for cream stock
- Fiction body: traditional serif, justified
- Body: **EB Garamond 11.35 pt / 13.55 pt leading**
- Mirrored margins: 0.76 in inside, 0.62 in outside; 0.54 in top, 0.62 in bottom
- Text column: 4.12 in; paragraph indent: 14.5 pt
- First paragraph after a chapter opener or scene break: flush left
- Subsequent paragraphs: first-line indent, no extra paragraph spacing
- Page number: small serif, centered in footer
- No running heads

## Chapter opener
The approved reference is the visual target, not merely inspiration.

1. **Distressed aperture ring**
   - Centered over the text column, **170 pt** overall width including splatter;
     top at **20 pt** from the page edge.
   - Organic broken/inked perimeter with small radial fractures and splatter.
   - Must retain substantially more visual weight than the simplified circle used in the rejected full-book build.
2. **Chapter numeral**
   - Tall, elegant serif numeral centered inside the ring.
   - **Noto Serif 47 pt**, centered; baseline **123 pt** from the top.
3. **Chapter heading**
   - `CHAPTER TWELVE` style, serif capitals with deliberate tracking.
   - Centered.
   - **18 pt EB Garamond**, with up to 7 pt tracking reduced to fit long headings;
     baseline **201 pt** from the top.
4. **Metadata**
   - Two centered lines beneath the heading:
     `[ LOCATION: ROOK ]`
     `[ RUN: WARDER ]`
   - Noto Sans Condensed.
   - **9.15 pt**, 2 pt tracking; baselines **231 pt** and **249 pt** from the top.
   - Metadata is quiet secondary information, not a HUD box.
5. **Sink**
   - Opening paragraph flow begins **264 pt** from the top, retaining the reference’s generous sink.
   - Preserve white space. Do not compress the opener into the top quarter of the page.
6. **Opening paragraph**
   - **31 pt raised initial**, including quoted openings, with ordinary baseline
     spacing below the first line.
   - First paragraph otherwise flush left.

## System typography
- Bracketed System notifications in the manuscript use the same restrained condensed sans family as chapter metadata.
- Centered when presented as standalone System output.
- No gray boxes, borders, icons, shading, or faux game-window chrome.
- Earth-game notifications and world-System notifications remain typographically related but are distinguished by context rather than decorative UI.

## Scene breaks
- Small centered aperture/ring mark.
- Ample but economical white space above and below.
- No asterism or generic ornamental flourish.

## Metadata rules
- `LOCATION` is editorial chapter metadata and must reflect the chapter's actual primary setting.
- `RUN` follows canonical System terminology.
- Before Maya selects a run, use `UNSET`.
- Once Warder is established, use `WARDER`.
- Do not invent a class field or replace canonical `RUN` with `CLASS`.
- When a chapter materially changes locations, use the dominant chapter location rather than listing multiple locations.

## Production rules
- Chapter openers start on a new page.
- Preserve widows/orphans where practical.
- Avoid loose justification and rivers; hyphenation/line-breaking should be tuned in final preflight.
- No content edits are introduced by typesetting.
- The September 24 print snapshot is the textual authority for this layout;
  it must match the active chapters and working draft. The September 20 frozen
  beta/ARC master remains a separate historical release.
- Final PDF must be rendered and visually inspected before release.


## Pagination and narrative-unit rules
These are hard production rules, not optional polish.

- **System/status blocks are indivisible.** Consecutive bracketed System lines must never split across pages.
- Keep a System notification/status block with the **immediate prose reaction** that follows it whenever the combined unit fits on a page.
- Never strand a scene-break ornament at the bottom of a page.
- Keep every scene-break ornament with the **first paragraph of the new scene**.
- Keep the complete chapter-opening stack together: aperture, chapter heading, LOCATION, RUN, and opening paragraph.
- Do not leave a one-line dramatic setup or transition at the foot of a page when its payoff is forced onto the next page.
- Prefer intentional white space at the bottom of a page over splitting a dramatic or System unit.
- A page turn may be used deliberately for suspense, but never as an accidental consequence of line filling.
