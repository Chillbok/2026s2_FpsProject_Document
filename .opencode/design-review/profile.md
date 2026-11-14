---
profile_version: 1
kit_version: 0.1.0
status: complete
updated_at: 2026-11-12
modes:
  - spec
---

# Design review profile

Project-root-relative paths only. No absolute paths. No secrets.
This file is user-owned. Kit updates never overwrite it.

## Paths

- docs:
  - 돌격 소총 프로토타입 기획.md
  - 프로토타입 플레이어용 무기에 필요한 것들.md
  - 무기의 스테이터스.md
- code: []
- evidence:
  - notes/총기 구현 현황 기록 문서.md
- exclude:
  - ".obsidian/**"
  - ".publish/**"
  - ".opencode/**"
  - "assets/**"
  - "**/.git/**"

## Scope

- default_scope: 돌격 소총 프로토타입 기획.md
- max_files: 10

## Baselines

- design_doc_updated_at: 2026-11-10
- prototype_commit: n-a
- evidence_cutoff: 2026-11-12

## Modes enabled

- spec: true
- drift: false
- prototype_informed: false

## Notes

- output_language: ko
- Fill every placeholder before running `/design-review`.
- Literal paths must exist. Glob patterns may match zero files; report the empty match instead of guessing.
