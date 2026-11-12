---
name: organize-bookshelf
description: 2026s2 FPS 기획 볼트 전용 관리 스킬. 노트 frontmatter의 노트 타입 속성에 따라 문서를 notes/기획 문서, notes/데이터베이스, notes/회의록으로 옮겨 정리한다. "문서 정리", "폴더 정리", "노트 타입에 따라 옮겨", "organize-bookshelf" 요청 시 사용한다.
metadata:
  author: 이준호
  version: 0.1.0
---

# organize-bookshelf

이 볼트의 문서를 `노트 타입` 속성에 따라 정해진 폴더로 옮긴다. 파일 내용은 수정하지 않고 위치만 바꾼다.

## 기준 데이터

- 매핑: `scripts/folder-map.json`
- 실행 스크립트: `scripts/organize.py` (Python 3 표준 라이브러리만 사용)

현재 매핑:

| 노트 타입 | 이동 위치 |
|---|---|
| `기획 문서` | `notes/기획 문서/` |
| `데이터베이스` | `notes/데이터베이스/` |
| `회의록` | `notes/회의록/` |

`templates/`, `bases/`, `assets/`, `.obsidian/`, `.publish/`, `.opencode/`는 스캔에서 제외한다.

## 절차

1. 볼트 루트(이 저장소 루트)에서 계획을 출력한다.

   ```bash
   python3 .opencode/skills/organize-bookshelf/scripts/organize.py --plan
   ```

2. 사용자에게 요약을 보여준다.
   - 이동 대상 수와 유형별 파일 목록
   - 충돌, 매핑 없는 타입, 타입 없는 파일
   - 삭제 예정인 빈 폴더
3. 사용자의 명시적 승인을 받은 뒤에만 적용한다.

   ```bash
   python3 .opencode/skills/organize-bookshelf/scripts/organize.py --apply
   ```

4. 결과를 확인해 보고한다.
   - 이동 완료 수, 실패 수
   - 제거된 빈 폴더
   - 검증 문제(원본 잔존, 목적지 누락)

## 안전 규칙

- 계획 없이 바로 적용하지 않는다. 항상 계획을 먼저 보여주고 승인을 받는다.
- 목적지에 같은 이름의 파일이 있으면 덮어쓰지 않고 중단한다.
- `노트 타입`이 없거나 매핑에 없는 문서는 이동하지 않고 보고만 한다. 타입을 임의로 바꾸지 않는다.
- 이동은 Obsidian CLI(`obsidian move`)로만 수행한다. `mv`로 대체하지 않는다.
- Obsidian 앱이 실행 중이 아니거나 CLI가 없으면 이동하지 않고 안내한다.
- 모든 이동이 끝난 뒤에만 빈 원본 폴더를 제거한다.
- git 커밋은 하지 않는다. 변경 사항 검토와 커밋은 사용자에게 맡긴다.

## 참고

- 이동 후 Obsidian 인덱스 반영을 위해 `obsidian reload`를 실행한다.
- 파일명이 중복되면 위키링크가 모호해질 수 있으므로, 계획 단계에서 중복 목적지를 충돌로 처리한다.
- `.publish` 사이트는 폴더 구조를 그대로 반영하므로 이동 시 문서 URL이 바뀔 수 있다.
