# Review output contract

Header (always include):

- Scope and mode
- Baseline (doc date, code commit, evidence cutoff)
- Files read
- Not reviewed

## Sections

### Confirmed facts

Both design and implementation or evidence agree. Include `path:line` and a short quote for each side.

### Conflicts

Design and implementation or two docs disagree. Include both citations.
One-sided claims are not conflicts. Severity: blocker, major, or minor.

### Insufficient evidence

State what is missing and what evidence would resolve it. Do not guess.

### Undecided

Open design questions. Include owner when known and the blast radius.

### Out of scope

Areas excluded by the profile or by the user request.

## Rules

- Every finding has one row: severity, location, observation, evidence, suggested next step.
- Suggestions stop at what to decide or check. No code fixes unless requested.
- Line numbers shift after edits, so keep the quoted text with the citation.
- A finding without a citation goes to insufficient evidence, never to conflicts.
- Keep reviewer attribution when two reviewers report the same area.
