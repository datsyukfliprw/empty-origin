---
name: nora-story-ledger
description: After a Nora chapter is finalized, append an accurate flowing chapter synopsis and a compact continuity ledger so the book accumulates a readable whole-story overview chapter by chapter. Run after continuity fixes are accepted and before Zippy packages the session.
---

# Nora Story Ledger

## Purpose

Maintain a cumulative, trustworthy record of the novel as it is actually written.

This skill runs **after the chapter has been written, continuity-audited, and any accepted fixes have been made**. It runs **before Zippy**.

It does not plan the next chapter, rewrite prose, edit canon, or repair the manuscript. Its job is to record the finished chapter in two complementary forms:

1. a **flowing cumulative story overview** that can eventually be read from Chapter 1 through the current chapter as a coherent long synopsis;
2. a **compact chapter ledger** that preserves the concrete facts future sessions need to remember.

The long-term goal is that after Chapter 53, the author can open one file and read the story from the beginning through Chapter 53 without reconstructing it from dozens of chats.

## Normal invocation

Use with Nora project authority:

`$nora $nora-story-ledger`

Normal workflow:

`Compass -> chapter skeleton -> Nora prose -> continuity audit/fixes -> story ledger -> Zippy`

## Project authority

Work from the active Nora Whitcomb book project and its actual finalized manuscript files.

For the current project, the author root is normally:

`/home/jay/Projects/books/novels/nora-whitcomb/`

Use the book-level routing/canon files to locate the manuscript and current chapter when needed. Treat the finalized manuscript as the authority for what actually happened on page.

Do not turn character beliefs, rumors, guesses, lies, theories, or reader implications into objective facts. Preserve uncertainty as uncertainty.

## Files this skill maintains

Create these if they do not yet exist:

### `book1/STORY_OVERVIEW.md`

A cumulative chronological synopsis of the novel in natural, flowing prose.

Each finalized chapter gets its own section:

`## Chapter 06`

followed by the chapter's synopsis.

The sections should read smoothly in sequence. A reader should be able to start at Chapter 1 and continue downward as if reading a detailed narrative summary of the entire book.

### `book1/CHAPTER_LEDGER.md`

A compact factual record for each finalized chapter. This is not the pretty synopsis. It is the memory layer for future agents and sessions.

## Process

### 1. Identify the finalized chapter

Determine which chapter has just been finalized.

Confirm that it is the next expected chapter relative to the existing ledger. Do not silently skip a missing chapter.

If the current chapter already has an entry, **update that chapter's existing sections instead of appending a duplicate**. The skill must be safe to rerun.

If more than one unsummarized chapter is present, do not guess which one the user intends. Report the gap or ambiguity.

### 2. Read the previous endpoint

Read the previous chapter's final story-overview section and ledger entry before summarizing the new chapter.

The new synopsis should begin from the state in which the previous chapter actually left the story. Do not restate the entire previous chapter, but make the transition intelligible.

For Chapter 1, simply begin with the opening state of the novel.

### 3. Read the complete finalized chapter

Read the entire finalized chapter, not excerpts.

Track the chapter's causal movement rather than merely listing scenes. Capture:

- what the viewpoint character wants or is trying to do;
- what changes or obstructs that goal;
- important decisions and their causes;
- discoveries, reveals, misunderstandings, and withheld information;
- relationship movement;
- emotional movement and consequences;
- System/LitRPG mechanics and progression that materially matter;
- meaningful worldbuilding learned through the chapter;
- injuries, resources, possessions, money, abilities, locations, promises, obligations, or other continuity-bearing details;
- setups, callbacks, mysteries, threats, and unresolved hooks that remain live;
- the state in which the chapter leaves the story.

Do not record every decorative detail. Preserve what matters to understanding how the story evolved.

### 4. Append or refresh the flowing synopsis

Write one substantial prose synopsis for the chapter in `book1/STORY_OVERVIEW.md`.

Target roughly **350-700 words per ordinary chapter**, with freedom to go shorter or longer when chapter complexity warrants it. Do not pad to hit a number.

Write in clear chronological prose, normally past tense and third person. The tone should be readable and human, closer to a detailed book synopsis than meeting notes.

Preserve causality:

`because this happened -> the character chose this -> which caused this -> which changed this`

Do not flatten the chapter into a sequence of disconnected events.

Preserve emotional and relationship changes when they affect the story. A kiss, argument, humiliation, betrayal, moment of trust, sexual encounter, death, victory, or refusal matters because of what it changes, not merely because it occurred.

Do not imitate Nora's novel prose. This is a lucid story record, not a second version of the chapter.

### 5. Append or refresh the factual ledger

Add a corresponding chapter section to `book1/CHAPTER_LEDGER.md` using this shape:

```markdown
## Chapter 06

**Opening state:**
- ...

**Major movement:**
- ...

**Character / relationship changes:**
- ...

**System / progression / resources:**
- ...

**Reveals and established facts:**
- ...

**Open threads / setups / uncertainties:**
- ...

**Ending state:**
- ...
```

Keep this section compact. Usually 1-4 bullets per heading is enough. Omit a heading's bullets when genuinely irrelevant rather than inventing content to fill the template.

Facts must be epistemically precise. Examples:

- `Maya suspects X` is not the same as `X is true`.
- `Tolliver tells Maya X` is not the same as `X is established fact`.
- `The System displays X` may establish what the System displayed without establishing Maya's interpretation of it.

### 6. Check the cumulative handoff

Before finishing, reread:

- the ending of the previous overview section;
- the beginning and ending of the new overview section;
- the new ledger entry.

Check that:

- the chronology connects;
- names and relationships are consistent;
- the summary does not contradict the chapter;
- important consequences were not lost;
- unresolved matters remain unresolved;
- the ending state is sufficient for the next session to understand where the story now stands.

### 7. Report, do not repair, contradictions

If summarizing exposes a possible canon or continuity contradiction, do **not** modify the manuscript, canon, or prior chapter summaries to make it disappear.

Finish the ledger work where possible, then report the issue separately as:

`Possible continuity issue: ...`

Distinguish a genuine contradiction from an intentional mystery or character misunderstanding.

## Compression rules

The story overview should become long over the course of the novel. That is intentional.

Do not progressively shorten later chapter summaries merely because the overview file is getting large.

Do not periodically replace earlier detailed chapter sections with a shorter global summary unless the user explicitly requests a separate compressed synopsis.

Do not rewrite all earlier chapter summaries every time a new chapter is added. This is an incremental record.

If a later chapter definitively recontextualizes an earlier event, preserve the earlier chapter's historical perspective and record the new truth in the later chapter. Do not retroactively pretend the reader or characters knew it earlier.

## Hard boundaries

This skill must not:

- write or rewrite the novel chapter;
- change Nora's prose specification;
- change chapter architecture;
- decide what happens next;
- alter canon;
- silently reconcile contradictions;
- turn implications into facts;
- summarize an unfinished draft as if it were final;
- duplicate an already-recorded chapter;
- replace Zippy.

Zippy runs after this skill and packages the newly updated story-state files for the next session.

## Completion report

Keep the user-facing completion report brief. State:

- which chapter was recorded;
- whether `STORY_OVERVIEW.md` was updated;
- whether `CHAPTER_LEDGER.md` was updated;
- any possible continuity issue discovered while summarizing.

Do not paste the entire synopsis into the completion report unless asked.
