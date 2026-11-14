---
description: Run independent design review with two read-only reviewers
subagent: false
---

Load the design-review skill with the skill tool (id: design-review) before proceeding.

Review $ARGUMENTS. If empty, use the profile default_scope. If the profile is missing or incomplete, stop and report the missing keys.

Resolve these absolute paths and pass them to both reviewers:

Profile: !`pwd`/.opencode/design-review/profile.md
Contract: !`pwd`/.opencode/skills/design-review/references/review-output.md

Call the `subagent` tool exactly twice, in foreground:

1. agent `design-review-consistency`
2. agent `design-review-evidence` (only when code or evidence inputs exist; otherwise run consistency only)

Each reviewer prompt must contain the profile path, the contract path, the mode, the exact scope, instruction to read both files first, and instruction to return findings only in contract format.

For drift mode, collect `git diff` and the changed-file list yourself and pass the relevant hunks. Reviewers must not run git.

Present both reviewer sections with attribution. Do not silently dedupe. End with unresolved questions and required human decisions. Do not edit files.
