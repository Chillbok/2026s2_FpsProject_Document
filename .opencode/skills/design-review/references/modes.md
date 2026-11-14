# Modes

## spec

Purpose: check a design before implementation.
Required inputs: design docs in scope, related decisions, terminology.
Forbidden: guessing implementation details not in the docs.
Output: conflicts across docs, missing decisions, scope risks, acceptance criteria gaps.

## drift

Purpose: check implemented changes against the approved design.
Required inputs: approved design docs, changed-file list, diff hunks, related tests.
The calling session collects the diff. Reviewers read only what is passed.
Forbidden: reviewers running git, build, or test commands.
Output: matched behavior, drifted behavior with both sides cited, missing tests, undecided follow-ups.

## prototype-informed (experimental)

Purpose: check prototype results before folding them into the design.
Required inputs: prototype code paths, evidence cutoff or commit, test notes, related design docs.
Run only when the profile sets `prototype_informed: true` and evidence paths exist.
Forbidden: judging visual quality from screenshots alone, asserting unmeasured claims.
Output: what the prototype proves, what remains untested, design updates needed.

## Mode selection

- Default to `spec` when only docs are given.
- Use `drift` when code changes or a diff is given.
- Use `prototype-informed` only on explicit request.
- Never run all three by default.
