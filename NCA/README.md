# NCA Skill Package

This package contains the Nora Compliance Auditor workflow.

## Files
- `SKILL.md` — complete NCA instructions
- `README.md` — invocation help

## Quick invocation
Use phrases such as:
- `Run NCA on this chapter.`
- `NCA this.`
- `Run NCA on the full manuscript until CLEAN.`
- `Use NCA on Chapters 12–16.`
- `Use NCA on the current Nora manuscript in the repo. Repair until GREEN.`

## Core behavior
NCA always uses the same loop:

**audit full range → repair actionable findings → discard prior audit → restart from line one → audit again → repeat until a fresh full pass is CLEAN**
