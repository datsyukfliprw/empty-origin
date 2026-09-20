# The Unheld Warder: applied ARC repairs and verification

> **Historical snapshot:** This report records an earlier manuscript state and has not been rewritten to match the September 20, 2026 synchronized *Empty Origin* manuscript. For current canon, use the chapter files, `WORKING_DRAFT.md`, `PROJECT_NOTES.md`, `STORY_OVERVIEW.md`, and `CHAPTER_LEDGER.md`.

**Revision date:** September 19, 2026, America/Chicago.  
**Reviewed baseline:** `914f2cb1fb3addadcbcf03c60cf6f1fd6ec295f3` (the prior review report commit; manuscript unchanged from `89b176f`).  
**Applied repair commit:** `e91f8f531085fee7eab35afcb2bdb2f553d75439`.  
**Action status:** Applied to canonical chapters, synchronized in active companion files, and rebuilt into `book1/WORKING_DRAFT.md`.  
**Current manuscript:** **100,303 whitespace-counted words across 32 chapters**, up from 99,593. Count includes headings and Markdown scene separators, as in the repository's existing convention.  
**Compiled SHA-256:** `9e202c70ad94ad5ec4b99197e7fbcf3ea1d0a4b577d9a127e6fc6c5be4e6f1c5`.

## Disposition

The seven documented repair chains and eleven local correction items have been addressed. The manuscript is ready for an independent beta/ARC reading round. This is not a claim of zero remaining errors, publication approval, or feedback from human beta readers.

Nineteen chapter files changed. Thirteen remain byte-for-byte identical to the baseline. The net addition is 710 words, primarily the missing physical, communication, and accounting connections. There was no new developmental rewrite, broad voice normalization, or expansion of the romance scenes.

The ending is preserved: Iven returns alive, the drainage remedy works, Sella takes her road, Tolliver's changed conduct supports the relationship, Maya rents a home and chooses the ridge job. No return to Earth, exclusive-couple promise, or settled three-person relationship has been introduced.

## Applied repairs

| Chain | Applied result | Rechecked dependencies |
|---|---|---|
| R01: identity and kinship | Pell retains she/her throughout the affected late scenes. Mara's nephews are no longer called her sons. Speaker and nameplate antecedents are explicit where needed. | Chapters 14–15, 30, 32; family identification and reunion. |
| R02: medical authority | The house mender performs examinations, treatment decisions, loading restrictions, and clearance. Mara remains records keeper, Iven's sister, and an active enforcer of the mender's instructions. Her family reactions and record work are retained. | Chapters 19–23 and 26–32; synopsis, ledger, project notes. |
| R03: Brace | Every repaired use has a physical load path: stopped sweep arm and fixed sill; reachable trolley-bracket stay and sound footing; near anchor shoe and its stone bed. No remote target acquisition or unearned new ability is added. | Teaching in Chapters 10–18, applications in 24–25 and 29, current mechanics notes. |
| R04: communication | Chapters 26–27 use mirror/slate and runner relay. Maya stays at the ground-floor kitchen table under restriction. Chapter 28 establishes and tests audible exchange from the unobstructed lower ledge; galleries and narrowing intervals retain slates. | First contact, restricted recovery, measurement exchange, rescue. |
| R05: action and rules | Light-object floor tests are explicitly provisional. Circled safe plates are not ignored after failure. The party returns along the checked route before taking the upper route. The ankle stop/recheck rule is consistent. Harra reaches the trolley's far landing once, and the final passenger's brake handoff is shown. | Complete East Relief entrance-to-exit chain; prototype and rescue callbacks. |
| R06: wages and dates | Day 18 and expedition Days 19–20 are separately paid. Oral retention begins Day 21. Thirteen retained days, 21–33 inclusive, produce **104 bits / 13 pieces** at the Day 34 settlement. The room costs 28 bits in cash after the unused fare credit. The earlier Day 16 purse count is 62 bits after payment. | Chapters 17–23, 26–27, 30–32; dated wage ledger and active companions. |
| R07: recovery | The pantry-roof memory is on the eighth evening after explicit ladder clearance. The Tolliver encounter remains on the ninth night after Sella leaves. Medical clearance has the same source throughout. | Chapter 30 montage, Chapter 31 clearance, Chapter 32 training. |

### Local corrections and bounded queries

The eleven local items from the earlier review are all applied: the replaced foot wrapping; Ordway's introduction; the carter's attribution; Harra/Sella pronoun clarity; a single staging of the shield payment; Rusk's completed-work tense; removal of the explicit Chapter Seven reference; the Knocker's plate rather than Maya's; removal of the arithmetic-as-canon aside; distinguishing progress from reserve checks; and Sella's bow being slung across her back.

The safe-room farewell signal is now established before its Chapter 30 callback. The office has one door and a fixed-grate ventilation opening, not an unexplained second door. The final departure changes from five days to four, preserving a two-day cart journey and time to see Ordway before the Greyward caravan leaves in six days. Craft-facing commentary about opposition and a sex scene's function has been replaced with in-world thought; Maya's gaming vocabulary and broader humor remain.

The manuscript's 97 displayed System lines and 158 scene breaks are unchanged in number and source content. Level costs, reserve expenditure, progression endpoints, two active abilities, and the distinction between recognized technique and activated ability are preserved. No level-up heals an injury or refills reserve.

## Wage decision requiring an actual correction

The previous review correctly declined to guess a replacement final total before reconciling the calendar. That reconciliation is now complete. The two paid expedition days end on Day 20. Three full recovery days follow, 21–23. Rescue and Sella's departure occur on Day 24. Their ninth night apart is Day 33, and Chapter 32 is the following morning, Day 34.

Retained service therefore runs from Day 21 through Day 33, thirteen days, not twelve. The already-paid Day 18 and expedition days are excluded. The new manuscript specifies that Day 34 is settlement and release, with no new assignment. Food and lodging through settlement use the existing unused-return provision. It does not manufacture an exact final personal purse or a value for the unused fare.

See `ARC_WAGE_CHRONOLOGY_2026-09-19.md` for the earned/paid distinction and the earlier coin chain.

## Reread scope and preservation

The earlier pass read all 32 chapters in order. This repair pass reread the changed passages in context and their dependencies, with particular attention to the complete Chapters 23–29 action/mechanics chain and Chapters 29–32 emotional, recovery, and settlement sequence. Mechanical scans supported that reading; they did not replace it.

The ending, reunion, Sella's independence, the nine-night separation, chosen surrender, revocable consent, and nonexclusive relationship discussion were preserved. No broad compression was applied merely because the earlier review identified possible attention fatigue. Those pacing observations remain useful questions for independent readers, not automatic reasons to reopen the manuscript.

Changed chapters: **5, 6, 10, 14, 15, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32**.

Unchanged chapters: **1, 2, 3, 4, 7, 8, 9, 11, 12, 13, 16, 17, 19**.

Updated companions: README, project notes, chapter ledger, cumulative story overview, and rescue mechanics. Earlier review documents remain historical records, not rewritten claims of current state. `ARC_REPAIR_PATCH_2026-09-19.diff` supplies exact source changes.

## Reading editions and verification

### EPUB

The EPUB 3 edition has a title page, 32 linked chapter entries, an ordered reading spine, legacy NCX navigation, preserved emphasis and System displays, and responsive paragraph styling. The package is deterministic for the same source. No author name, ISBN, copyright declaration, or cover artwork has been invented.

Verified: XML parsing; manifest resources; reading order; all navigation targets; exact chapter paragraph text compared with the canonical source; and 64 Chromium layout checks across all 32 chapters at widths of 320 and 768 pixels, with zero horizontal-overflow failures. Extracted XHTML was rendered with its packaged stylesheet. Representative chapter openings and System displays were visually inspected at phone and tablet widths.

These checks are **not an EPUBCheck run or a test in Kindle, Apple Books, or another physical reading device**. They do not certify every reading application's pagination or accessibility behavior.

### PDF

The 6-by-9-inch reading PDF has **433 pages**: two front-matter pages and 431 numbered manuscript pages. It has 32 chapter bookmarks, chapter starts on new pages, running heads, preserved italics and bold, explicit scene dividers, and System text in an arrow-capable font.

All chapter text extracted from the finished PDF matches the canonical source after whitespace normalization and removal of page furniture. Every page was checked programmatically for text extending beyond page bounds. All chapter openings, front matter, the final page, and selected body/System pages were visually inspected. This is not a claim of a second human page-by-page copyedit of all 433 rendered pages or a press-ready print interior.

The export check initially exposed missing arrow glyphs and malformed scene-break rendering. Both were corrected, the editions rebuilt, and the text and layout checks rerun successfully.

### Recorded evidence

- `arc/ARC_BUILD_MANIFEST.json`: source/chapter hashes and EPUB build identity.
- `arc/ARC_VALIDATION.json`: source, EPUB, and PDF structural/text checks performed locally.
- `arc/EPUB_BROWSER_CHECK.json`: responsive browser-check results.
- `arc/ARC_LOCAL_PDF_MANIFEST.json`: local PDF fingerprint and chapter-start pages.
- `tools/build_arc.py`: repeatable EPUB builder; optional PDF build requires the documented local fonts and ReportLab.

A downloaded GitHub build was compared against the local proof: all 32 chapters, the compilation, changed companion files, build scripts, and EPUB match byte for byte.

The PDF is distributed with the conversation's ARC bundle; the repository stores its fingerprint rather than a redundant binary. The EPUB and compiled Markdown are also in the repository.

## Remaining external checks

Independent beta-reader feedback and a final pass inside the actual target reading applications remain separate from this completed repair. Publication cover, author/imprint metadata, front/back matter, retailer packaging, and any final print production proof are not part of this manuscript repair. No further plot rewrite is prescribed by this report.
