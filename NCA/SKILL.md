# Nora Compliance Auditor (NCA)

## Purpose
Run the Nora Compliance Auditor (NCA) as a repair-until-clean loop for Nora Whitcomb manuscript work.

## Governing principle
NCA is not a one-pass critique. It is an iterative compliance repair system.

## Core loop
1. Read the full relevant manuscript range and all governing Nora authority files required for the task.
2. Audit the entire relevant range for every actionable compliance problem.
3. Repair all actionable issues that can be fixed without violating explicit author decisions, canon, reveal timing, POV, tense, relationship state, continuity, or other locked constraints.
4. Discard the prior audit result.
5. Restart the audit from the beginning of the relevant range.
6. Repeat: audit → repair → restart from zero → audit again.
7. Declare CLEAN / GREEN only when a complete fresh restart pass produces zero unresolved findings.

## Mandatory restart rule
After any material repair, the next audit begins again from line one of the relevant range.
Never resume from the previous stopping point.
Never treat earlier findings as still authoritative after repairs.

## Scope
Audit Nora compliance across all applicable dimensions, including:
- prose and cadence
- POV depth and character-filtered narration
- dialogue and character voice
- internal monologue
- romance and sexual tension
- explicit-scene continuity where applicable
- action clarity
- System integration
- exposition
- continuity and canon
- character knowledge and reveal firewalls
- relationship state
- magic / mechanics
- objects, injuries, geography, and physical state
- setup, callbacks, payoff, and stale dependent references
- Nora anti-patterns and repetitive scaffolding

## Repair behavior
- Fix prose and continuity defects directly when the governing files make the correct repair clear.
- Preserve author decisions and intervening manuscript changes.
- Do not redesign plot, character arcs, reveal timing, or world rules unless explicitly requested.
- Do not opportunistically rewrite unrelated material.
- When a finding depends on a genuine unresolved author choice, isolate it clearly instead of inventing a decision.
- If a repair materially changes a chapter or scene, restart the audit afterward.

## Tools and diagnostics
Searches, scripts, grep, linters, and automated checks are diagnostic aids only.
They do not substitute for a complete manual reread of the affected range.

## Status rules
RED means unresolved actionable findings remain.
GREEN / CLEAN means a complete fresh pass from the beginning found zero unresolved actionable findings.
Do not claim GREEN based on a partial pass.

## Output discipline
Keep intermediate finding lists, pass-by-pass notes, scratch reasoning, and superseded drafts internal unless the user asks for them.

The default user-facing result should be concise:
- what was repaired
- what range was audited
- whether the final fresh pass was CLEAN / GREEN
- any genuine author decision still required

## Invocation
Use this skill whenever the user says things such as:
- "Run NCA"
- "NCA this chapter"
- "Run the Nora Compliance Auditor"
- "Audit and repair this with NCA"
- "NCA the manuscript"
- "Run NCA until clean"

When invoked, apply the loop above to the user-specified manuscript, chapter, repository range, or task.
