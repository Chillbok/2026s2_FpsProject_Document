---
aliases:
작성 날짜: 2026-11-06
작성자:
  - "[[인공지능 에이전트]]"
관여 주체:
  - "[[플레이어 캐릭터]]"
  - "[[씬]]"
categories:
  - "[[이현종 게임잼 프로토타입 구현 기록]]"
노트 타입: "[[기획 문서]]"
---

# 타이틀·게임 UI 및 레벨 제작 도구 구현 기록

## 구현 개요

타이틀 화면, 설정, 상호작용 안내, 미션 HUD, 일시정지·결과 화면은 주로 Unity UI 오브젝트를 코드에서 생성한다. 플레이 레벨의 임무·적·스폰·출구 설정은 Unity 에디터 전용 빌더가 씬에 배치한다. 따라서 화면과 레벨 기능은 씬 파일뿐 아니라 `Assets/Scripts/UI`와 `Assets/Scripts/Editor`의 코드에 의해 구성된다.

## 타이틀과 브리핑

- `TitleScreen.Start`는 시간 배율과 커서를 초기화하고 `UIKit`으로 타이틀 Canvas, 배경, 메뉴, 설정, 조작법, 브리핑 패널을 만든다. 조작법·브리핑 화면은 같은 루트의 패널 활성화 상태를 바꿔 표시한다 (`Assets/Scripts/UI/TitleScreen.cs:33-56`, `:103-109`).
- 메뉴는 작전 시작, 설정, 조작법, 종료 항목을 제공한다. 작전 시작은 브리핑 화면을 열고, Enter 또는 숫자 키패드 Enter 입력 시 `GameProgress.StartRun`을 한 번 호출해 새 런을 시작한다 (`TitleScreen.cs:58-73`, `:138-148`).
- 타이틀과 브리핑은 텍스트·버튼·패널을 코드로 생성한다. 제목 글자 크기는 현재 화면 폭을 기준으로 조정한다 (`TitleScreen.cs:75-87`, `:111-176`).

## UI 생성 방식과 표시

- `UIKit`은 Canvas, RectTransform, 레이블, 버튼, 레이아웃 등 반복되는 UI 생성을 모으는 헬퍼다. 개별 화면은 이를 이용해 런타임 오브젝트를 만든다. 상호작용 프롬프트는 OS 폰트 목록을 이용하고, 둥근 배경 스프라이트도 픽셀 텍스처로 생성한다 (`Assets/Scripts/UI/InteractionPrompt.cs:29-43`, `:80-100`, `:161-190`).
- `InteractionPrompt`는 플레이어 주변 상호작용 안내를 화면 중앙 아래에 표시한다. 문에 대해서는 열기와 내시경 선택지를 모두 보여주고 현재 선택을 강조한다 (`InteractionPrompt.cs:45-70`).
- `MissionHUD`는 목표를 좌측 상단에 표시하고, 완료 문구용 중앙 배너를 가진다. `Mission`이 아이템 진행에 맞춰 목표를 갱신한다 (`Assets/Scripts/UI/MissionHUD.cs:14-36`, `Assets/Scripts/World/Mission.cs:28-58`).
- `PauseMenu`는 플레이 씬마다 `SceneFlow`가 생성한다. Esc로 시간과 오디오를 정지하고 플레이어 입력을 비활성화하며, 재개 시 이를 복구한다. 사망·완료 화면 위에서는 정지를 시작하지 않는다 (`Assets/Scripts/UI/PauseMenu.cs:20-45`, `:55-97`).
- `EndScreen`은 사망과 임무 완료 문구를 같은 결과 화면으로 표현하고, 실시간 기준 페이드·대기 후 전달된 콜백을 실행한다. 사망 콜백은 체크포인트 재시작, 성공 콜백은 타이틀 복귀다 (`Assets/Scripts/UI/EndScreen.cs:18-32`, `:55-78`).
- `ScreenFade`는 `DontDestroyOnLoad` 오브젝트로 씬 전환 후에도 검은 화면을 유지한다. 씬 로드가 시작될 때 가리고 새 씬이 동작하면 0.5초 동안 다시 드러낸다 (`Assets/Scripts/UI/ScreenFade.cs:6-23`, `:25-47`, `:58-63`).

## 설정 저장

- 공통 설정 패널은 마우스 감도와 전체 음량 슬라이더를 제공한다 (`Assets/Scripts/UI/SettingsPanel.cs:7-33`).
- `GameSettings`는 PlayerPrefs에 감도와 음량을 저장한다. 감도는 0.2~3 범위로 제한하고, 음량은 0~1 범위로 제한해 `AudioListener.volume`에 반영한다. 씬 전 시작 초기화 시 저장 값을 읽는다 (`Assets/Scripts/World/GameSettings.cs:5-43`, `:45-59`).
- UI의 저장 버튼은 `GameSettings.Save()`를 호출한다. 개별 설정 값 대입 시 PlayerPrefs에도 기록하고, Save에서 디스크 저장을 요청한다.

## 병원 레벨 에디터 도구

- `AsylumEnemyPlacer`의 메뉴 항목 `Tools/Game Jam/Build Asylum Level (Enemies + Mission)`은 병원 씬에서 기존 적 루트를 지우고 Guard·Patrol과 경로점을 생성한다. 빈 바닥 위치 탐색, 방 렌더러 바운즈, NavMesh 경로, 시야 방향 계산 등 배치 보조 함수가 같은 도구에 있다 (`Assets/Scripts/Editor/AsylumEnemyPlacer.cs:130-225`, `:309-397`).
- 같은 도구가 랜덤 위치 열쇠카드, 소음 설정이 있는 장부, 열쇠카드 잠금 문, 병원 출구 스폰과 단계별 미션을 생성한다 (`AsylumEnemyPlacer.cs:227-288`).
- 맵에 놓는 위치·순찰 경로·적 종류는 에디터 코드의 고정 스펙으로 관리된다. 재생 중에 동적으로 레벨을 절차 생성하는 도구가 아니라, 편집 중 씬 오브젝트를 재구성하는 메뉴 도구다.

## 마을 레벨 에디터 도구

- `VillageLevelBuilder` 메뉴는 `Bridge_Village` 씬에서 맵 루트, 차량, 플레이어를 확인한 뒤 기존 `Village Gameplay` 루트를 교체한다. 차량 메시에서 바운즈를 구해 BoxCollider를 맞추고 운전석 옆 기본 스폰, 병원 입구 스폰, 병원 출구, 차량 탈출 목표를 만든다 (`Assets/Scripts/Editor/VillageLevelBuilder.cs:59-110`, `:125-163`).
- 마을의 두 Guard와 두 Patrol은 스크립트의 고정 위치·회전·경로 스펙에서 생성한다. 시야 거리는 안개 시야에 맞춰 45m로 설정한다 (`VillageLevelBuilder.cs:22-57`, `:165-221`).
- 생성 전 NavMesh를 굽고, 플레이어 컴포넌트와 마을 임무를 설정하며 씬을 dirty 상태로 표시한다 (`VillageLevelBuilder.cs:102-120`).
- 공통 `LevelBuildTools`는 플레이어 필수 구성요소, SpawnPoint, SceneExit 생성과 플레이어 위치 설정을 제공한다 (`Assets/Scripts/Editor/LevelBuildUtility.cs:9-67`).

## 성능·사운드 보조 기능

- `AudioPreloader`는 씬의 MonoBehaviour 필드와 일부 ScriptableObject 참조를 제한된 깊이로 순회해 AudioClip을 찾아 미리 로드한다. `SceneFlow`는 씬 로드 후 한 프레임을 기다려 플레이어 무기 생성 이후 프리로드를 호출한다 (`Assets/Scripts/World/AudioPreloader.cs:8-24`, `:27-66`, `Assets/Scripts/World/SceneFlow.cs:38-45`).
- `PerfProbe`는 문, 적 업데이트·재경로·인식·이동·발사, 소음 전달 등 프로파일러 표식을 제공한다. 런타임 기능이 아니라 Unity Profiler 측정 지점을 위한 진단 코드다 (`Assets/Scripts/Diagnostics/PerfProbe.cs`).

## 관련 문서

- 캠페인과 커밋 이력은 [[이현종 게임잼 프로토타입 구현 개요 및 브랜치 이력]]을 참고한다.
- 상호작용과 씬 이동은 [[상호작용·임무 진행 및 씬 전환 구현 기록]]을 참고한다.
