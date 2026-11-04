---
aliases:
작성 날짜: 2026-11-03T01:36
작성자:
  - "[[인공지능 에이전트]]"
관여 주체:
  - "[[플레이어 캐릭터]]"
categories:
  - "[[구현 기록]]"
노트 타입: "[[기획 문서]]"
---

# 상호작용 포인트 및 UI 구현 방식 기록

## 구현 개요

상호작용 대상 오브젝트에 `InteractionPointController`를 두고, 인스펙터에서 탭·홀드 동작을 각각 UnityEvent로 연결한다. 플레이어의 `InteractionDetector`가 후보 중 하나를 선택하고 `InteractionUIController`가 대상 안내와 입력 진행을 화면에 표시한다.

## 대상 선택

- 플레이어 몸통 중심을 기준으로 `OverlapSphereNonAlloc`을 수행한다(기본 반경 1m). 할당을 줄이기 위해 64개짜리 콜라이더 버퍼를 재사용한다.
- 후보는 `Interactable` 레이어(레이어가 없으면 전체 레이어)에서 찾고, 포인트의 실제 위치가 반경 안인지 다시 검사한다.
- 카메라 전방과 포인트 방향의 각도(기본 허용 30도)를 비교하고, 허용각 안에서 카메라 전방과 가장 가까운 후보를 선택한다.
- 트리거 콜라이더도 감지 대상으로 포함한다. 포인트에 탭 또는 홀드 이벤트가 실제로 연결되어 있지 않으면 상호작용 대상으로 취급하지 않는다.

## 입력과 UI 연결

- `PlayerTapHoldInput`의 Press/Tap/Hold/Cancelled 이벤트를 감지기가 받아 UI에 전달한다. 실제 동작은 포인트의 UnityEvent를 실행한다.
- UI는 대상의 탭·홀드 메시지와 지원 동작에 맞춰 표시 요소를 켜고 끈다. 홀드 진행 게이지에는 탭/홀드 경계를 넘긴 뒤의 진행률을 전달한다.
- 대상 위치를 카메라의 `WorldToScreenPoint`로 변환해 UI를 포인트에 붙인다. 카메라 이동이 끝난 `LateUpdate`에서 위치를 갱신한다.
- 탭만 있는 대상은 Press 시 실행하고, Press와 Tap에서 중복 실행되지 않도록 현재 누름의 실행 여부를 기억한다.

## 범위 및 제약

- 이 포인트 기반 시스템은 `PlayerInteractor`/`IInteractable`로 구현된 문·작업대 상호작용과 별도 경로다. 두 방식은 프로젝트 안에 공존한다.
- 탐지 버퍼가 64개로 고정되어 있어 한 번의 쿼리 결과가 이를 초과할 경우 모든 콜라이더를 담지 못할 수 있다.

## 참조

- `Assets/_Project/Scripts/Interaction/InteractionDetector.cs`
- `Assets/_Project/Scripts/InteractionObject/InteractionPointController.cs`
- `Assets/_Project/Scripts/UI/InteractionUIController.cs`
- `Assets/_Project/Scripts/UI/MiddlePointLineConnector.cs`
- `Assets/_Project/Scripts/UI/SingleLineAutoSizeText.cs`
