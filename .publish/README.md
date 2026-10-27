# 사이트 퍼블리시 설정

이 폴더는 [Quartz 5](https://quartz.jzhao.xyz/)로 기획 문서 사이트를 빌드하기 위한 설정입니다.
볼트 본문은 건드리지 않고, CI에서 복사본에만 손을 댑니다.

- 사이트 주소: https://chillbok.github.io/2026s2_FpsProject_Document/
- 배포: `.github/workflows/publish-site.yml` (main 브랜치 push 시 자동)

## 파일

| 파일 | 역할 |
|---|---|
| `quartz.config.yaml` | 사이트 제목·언어(ko-KR)·baseUrl·플러그인 설정 |
| `custom.scss` | 커스텀 CSS (mermaid 색상 파싱 문제 우회) |
| `prepare.sh` | 볼트 → Quartz `content/` 복사, 홈페이지(`index.md`) 생성 |

## Mermaid가 코드블록으로 보일 때

증상: 다이어그램 자리에 ```mermaid 코드가 그대로 보인다.
브라우저 콘솔에 `Unsupported color format: "hsl(calc(...), ...)"`가 찍힌다면
테마가 `calc()` 기반 색을 만들고 mermaid의 색 파서가 이를 이해하지 못한 것이다.

`custom.scss`가 `--color-accent-1/2`를 미리 계산한 정적 hsl 값으로 덮어써서 회피한다.
테마를 바꾸거나 `@quartz-themes/*`를 업데이트했다면 이 값도 다시 맞춰야 한다.

## 사이트에서 제외되는 것

`prepare.sh`의 rsync 제외 목록:

- `.git/`, `.github/`, `.obsidian/`, `.publish/`
- `templates/` — `{{title}}` 플레이스홀더가 깨진 임베드로 노출됨
- `TaskNotes/` — TaskNotes 전용 뷰(`tasknotesKanban` 등)와 formula는 Quartz가 렌더하지 못함
- `bases/배포 스킬 설치 가이드.base` — 필터가 없어 전체 문서를 나열함

제외를 바꾸려면 `prepare.sh`의 `--exclude` 줄을 수정합니다.

## 홈페이지

볼트의 `notes/Home.md`는 사이트 루트(`/`)에서 열리도록 `index.md`로 변환됩니다
(`title: 홈`, `aliases: [Home]` 자동 추가). 원본 `notes/Home.md`는 그대로 둡니다.

## 검색엔진 노출

워크플로 마지막의 `Add noindex` 단계가 모든 HTML에
`<meta name="robots" content="noindex">`를 삽입합니다. 링크를 아는 사람은 접속할 수 있지만
검색 결과에는 뜨지 않습니다. 노출을 원하면 그 단계를 삭제하세요.

## Quartz 버전

`publish-site.yml`의 `QUARTZ_REF` 커밋에 고정되어 있습니다. 올릴 때는 값을 바꾸고
로컬에서 한 번 빌드해 확인한 뒤 push하세요.
`v5.0.0` 태그는 플러그인을 git에서 받아와야 해서 CI에 부적합합니다.

## 로컬 미리보기

```bash
git clone --depth 1 --branch v5 https://github.com/jackyzha0/quartz.git /tmp/quartz
cd /tmp/quartz && npm ci
npx quartz create -t obsidian -X new -b "chillbok.github.io/2026s2_FpsProject_Document" -l shortest
cp <볼트>/.publish/quartz.config.yaml quartz.config.yaml
bash <볼트>/.publish/prepare.sh <볼트> content
npx quartz build --serve
```
