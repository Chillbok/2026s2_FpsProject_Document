#!/usr/bin/env python3
"""organize-bookshelf: 노트 타입 속성에 따라 노트를 폴더로 옮긴다.

기본 동작은 계획 출력(dry-run)이다. 실제 이동은 --apply 를 붙인다.
이동은 Obsidian CLI(move)로 수행해 링크와 인덱스를 보존한다.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = SKILL_DIR / "folder-map.json"

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.S)
TYPE_RE = re.compile(r"^노트 타입\s*:\s*(.+?)\s*$", re.M)
WIKILINK_RE = re.compile(r"^\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]$")


def normalize_type(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1].strip()
    match = WIKILINK_RE.match(value)
    if match:
        value = match.group(1).strip()
    return value


def read_note_type(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    type_match = TYPE_RE.search(match.group(1))
    if not type_match:
        return None
    note_type = normalize_type(type_match.group(1))
    return note_type or None


def load_config(path: Path) -> dict:
    if not path.is_file():
        sys.exit(f"설정 파일을 찾을 수 없습니다: {path}")
    with path.open(encoding="utf-8") as handle:
        config = json.load(handle)
    if not isinstance(config.get("folders"), dict) or not config["folders"]:
        sys.exit("설정 파일에 folders 매핑이 없습니다.")
    config.setdefault("excludeDirs", [])
    return config


def iter_notes(root: Path, exclude_dirs: set[str]):
    for path in sorted(root.rglob("*.md")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in exclude_dirs for part in relative.parts[:-1]):
            continue
        if path.name.startswith("."):
            continue
        yield path


def build_plan(root: Path, config: dict) -> dict:
    folders = {note_type: root / folder for note_type, folder in config["folders"].items()}
    exclude_dirs = set(config["excludeDirs"])

    moves: list[dict] = []
    dest_seen: dict[Path, list[Path]] = {}
    already: list[dict] = []
    untyped: list[Path] = []
    unmapped: list[tuple[Path, str]] = []
    conflicts: list[dict] = []

    for path in iter_notes(root, exclude_dirs):
        note_type = read_note_type(path)
        if note_type is None:
            untyped.append(path)
            continue
        if note_type not in folders:
            unmapped.append((path, note_type))
            continue

        target_dir = folders[note_type]
        destination = target_dir / path.name
        record = {
            "source": path,
            "destination": destination,
            "type": note_type,
        }
        if path.parent == target_dir:
            already.append(record)
            continue

        moves.append(record)
        dest_seen.setdefault(destination, []).append(path)

    for record in moves:
        destination = record["destination"]
        reason = None
        if destination.exists() and destination.resolve() != record["source"].resolve():
            reason = "목적지에 같은 이름의 파일이 이미 있음"
        elif len(dest_seen[destination]) > 1:
            reason = "여러 원본이 같은 목적지로 이동하려 함"
        elif (root / destination).is_dir():
            reason = "목적지 경로가 폴더임"
        if reason:
            conflicts.append({**record, "reason": reason})

    return {
        "root": root,
        "moves": moves,
        "already": already,
        "untyped": untyped,
        "unmapped": unmapped,
        "conflicts": conflicts,
    }


def format_rel(root: Path, path: Path) -> str:
    if path.is_absolute():
        return path.relative_to(root).as_posix()
    return path.as_posix()


def print_plan(plan: dict) -> None:
    root = plan["root"]
    print(f"볼트 루트: {root}")
    print(f"이동 대상: {len(plan['moves'])}개")

    by_type: dict[str, list[dict]] = {}
    for record in plan["moves"]:
        by_type.setdefault(record["type"], []).append(record)

    for note_type, records in sorted(by_type.items()):
        print(f"\n[{note_type}] {len(records)}개")
        for record in records:
            marker = "  (충돌)" if record in plan["conflicts"] else ""
            print(f"  {format_rel(root, record['source'])} -> {format_rel(root, record['destination'])}{marker}")

    if plan["conflicts"]:
        print(f"\n충돌: {len(plan['conflicts'])}개 (적용 중단 필요)")
        for record in plan["conflicts"]:
            print(f"  {format_rel(root, record['source'])}: {record['reason']}")

    if plan["already"]:
        print(f"\n이미 올바른 위치: {len(plan['already'])}개")

    if plan["unmapped"]:
        print(f"\n매핑에 없는 노트 타입: {len(plan['unmapped'])}개 (이동하지 않음)")
        for path, note_type in plan["unmapped"]:
            print(f"  [{note_type}] {format_rel(root, path)}")

    if plan["untyped"]:
        print(f"\n노트 타입 없음: {len(plan['untyped'])}개 (이동하지 않음)")
        for path in plan["untyped"]:
            size = path.stat().st_size
            print(f"  {format_rel(root, path)} ({size} bytes)")


def plan_as_json(plan: dict) -> str:
    root = plan["root"]
    payload = {
        "root": str(root),
        "moves": [
            {
                "source": format_rel(root, record["source"]),
                "destination": format_rel(root, record["destination"]),
                "type": record["type"],
            }
            for record in plan["moves"]
        ],
        "conflicts": [
            {
                "source": format_rel(root, record["source"]),
                "destination": format_rel(root, record["destination"]),
                "type": record["type"],
                "reason": record["reason"],
            }
            for record in plan["conflicts"]
        ],
        "unmapped": [
            {"path": format_rel(root, path), "type": note_type}
            for path, note_type in plan["unmapped"]
        ],
        "untyped": [format_rel(root, path) for path in plan["untyped"]],
        "alreadyCount": len(plan["already"]),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def run_command(args: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)


def detect_vault(root: Path, configured: str | None) -> str:
    try:
        result = run_command(["obsidian", "vaults", "verbose"], timeout=30)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                parts = line.split("\t")
                if len(parts) >= 2 and Path(parts[1]).expanduser().resolve() == root:
                    return parts[0]
    except (OSError, subprocess.SubprocessError):
        pass
    if configured:
        return configured
    sys.exit("볼트 이름을 확인할 수 없습니다. folder-map.json의 vault 값을 지정하세요.")


def ensure_obsidian_cli() -> None:
    if shutil.which("obsidian") is None:
        sys.exit("Obsidian CLI를 찾을 수 없습니다. Obsidian 앱과 CLI 설정을 확인하세요.")


def apply_plan(root: Path, config: dict, plan: dict) -> int:
    ensure_obsidian_cli()

    if plan["conflicts"]:
        print("충돌이 있어 이동을 중단했습니다. 계획을 먼저 정리하세요.", file=sys.stderr)
        return 1

    if not plan["moves"]:
        print("이동할 노트가 없습니다.")
        return 0

    vault = detect_vault(root, config.get("vault"))
    print(f"볼트: {vault}")

    target_dirs = sorted({root / record["destination"].parent for record in plan["moves"]})
    for directory in target_dirs:
        directory.mkdir(parents=True, exist_ok=True)

    moved: list[dict] = []
    failures: list[dict] = []
    for record in plan["moves"]:
        source = format_rel(root, record["source"])
        destination = format_rel(root, record["destination"])
        try:
            result = run_command(
                ["obsidian", "move", f"path={source}", f"to={destination}", f"vault={vault}"],
                timeout=120,
            )
        except subprocess.SubprocessError as error:
            failures.append({**record, "error": str(error)})
            break
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            failures.append({**record, "error": detail or f"exit {result.returncode}"})
            break
        moved.append(record)
        print(f"이동: {source} -> {destination}")

    try:
        run_command(["obsidian", "reload", f"vault={vault}"], timeout=60)
    except subprocess.SubprocessError:
        pass

    problems: list[str] = []
    for record in moved:
        destination_abs = root / record["destination"]
        source_abs = root / record["source"]
        if not destination_abs.is_file():
            problems.append(f"목적지 없음: {format_rel(root, destination_abs)}")
        if source_abs.exists():
            problems.append(f"원본 남음: {format_rel(root, source_abs)}")

    removed_dirs: list[Path] = []
    source_parents = sorted(
        {record["source"].parent for record in moved},
        key=lambda item: len(item.parts),
        reverse=True,
    )
    for directory in source_parents:
        if directory == root:
            continue
        if not directory.is_dir():
            continue
        if any(directory.iterdir()):
            continue
        try:
            os.rmdir(directory)
            removed_dirs.append(directory)
        except OSError:
            pass

    print("\n결과")
    print(f"  이동 완료: {len(moved)}개")
    print(f"  실패: {len(failures)}개")
    if failures:
        for record in failures:
            print(f"    {format_rel(root, record['source'])}: {record['error']}")
    if removed_dirs:
        print("  빈 폴더 제거: " + ", ".join(format_rel(root, path) for path in removed_dirs))
    if problems:
        print("  검증 문제:")
        for problem in problems:
            print(f"    {problem}")

    remaining = len(plan["moves"]) - len(moved)
    if remaining > 0:
        print(f"  남은 이동: {remaining}개")
    if failures or problems:
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="노트 타입 속성에 따라 노트를 폴더로 이동합니다.",
    )
    parser.add_argument("--root", default=".", help="볼트 루트 (기본: 현재 디렉터리)")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="folder-map.json 경로")
    parser.add_argument("--plan", action="store_true", help="계획만 출력 (기본 동작)")
    parser.add_argument("--apply", action="store_true", help="계획을 실제로 적용")
    parser.add_argument("--json", action="store_true", help="계획을 JSON으로 출력")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        sys.exit(f"볼트 루트가 아닙니다: {root}")

    config = load_config(Path(args.config).expanduser().resolve())
    plan = build_plan(root, config)

    if args.apply:
        return apply_plan(root, config, plan)
    if args.json:
        print(plan_as_json(plan))
    else:
        print_plan(plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
