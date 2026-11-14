# Review checklist

Apply per mode. A finding needs stated evidence, not style preference.

## Consistency

- Contradictory requirements or decisions across docs.
- Same term with different meanings, or different terms for the same concept.
- Missing decision: behavior required by one doc but undefined elsewhere.
- Scope drift: out-of-scope work implied by examples, diagrams, or edge cases.
- State ownership: two components both claim to own the same state or transition.
- Error handling: undefined failure paths, retries, timeouts, or user-visible errors.
- Configuration and secrets: hardcoded values, undocumented env vars, secrets in docs.
- Naming and contracts: API, event, or schema names that disagree across docs.

A consistency finding requires at least two cited sources, or one source plus an explicit gap.

## Evidence

- Design claim with no supporting code, test, log, or artifact.
- Code behavior that contradicts the approved design.
- Unverified assertion: performance, security, or reliability claim with no measurement.
- Missing test boundary: changed behavior with no test path in the listed evidence.
- Prototype result quoted without commit, date, or artifact reference.

An evidence finding requires both sides cited when claiming a conflict.
If one side is missing, file it under insufficient evidence and state what would resolve it.

## Not findings

- Style nits without a contract or consistency impact.
- Personal preference presented as a defect.
- Guesses about files outside the listed scope.
- Severity inflation: use blocker only when the defect breaks the stated purpose.
- Conflict reports about the review profile's own settings. Report those as configuration notes, not design findings.
- "The design document does not describe module X" when module X is simply outside the requested scope.
