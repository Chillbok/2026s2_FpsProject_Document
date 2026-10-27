#!/usr/bin/env bash
# 볼트 → Quartz content 디렉터리 준비 스크립트.
# 원본 볼트는 절대 수정하지 않고, 복사본에만 손을 댄다.
#
# 사용법: .publish/prepare.sh <볼트 루트> <content 출력 디렉터리>
set -euo pipefail

VAULT="${1:?볼트 루트 경로를 넘겨주세요}"
DEST="${2:?content 디렉터리 경로를 넘겨주세요}"

mkdir -p "$DEST"

# 1) 문서 복사 (사이트에 불필요한 것만 제외)
rsync -a --delete \
  --exclude '.git/' \
  --exclude '.github/' \
  --exclude '.obsidian/' \
  --exclude '.publish/' \
  --exclude 'templates/' \
  --exclude 'TaskNotes/' \
  --exclude 'bases/배포 스킬 설치 가이드.base' \
  --exclude '.DS_Store' \
  "$VAULT"/ "$DEST"/

# 2) 홈페이지 생성: Home.md → index.md (루트 URL에서 열리도록)
python3 - "$DEST" <<'PY'
import pathlib
import re
import sys

dest = pathlib.Path(sys.argv[1])
home = dest / "notes" / "Home.md"
if not home.exists():
    sys.exit(0)

text = home.read_text(encoding="utf-8")
body = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
(dest / "index.md").write_text(
    "---\ntitle: 홈\naliases:\n  - Home\n---\n" + body.lstrip("\n"),
    encoding="utf-8",
)
home.unlink()
PY

echo "content 준비 완료: $(find "$DEST" -type f | wc -l | tr -d ' ')개 파일"
