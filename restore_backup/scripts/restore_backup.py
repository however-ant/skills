#!/usr/bin/env python3
"""Preview or restore files from common backup filename patterns."""

from __future__ import annotations

import argparse
import dataclasses
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


TIMESTAMP_RE = r"(?:19|20)\d{6}(?:[_-]?\d{6})?"
BACKUP_PATTERNS = [
    re.compile(rf"^(?P<base>.+)\.bak(?:[._-]?{TIMESTAMP_RE})?$", re.IGNORECASE),
    re.compile(rf"^(?P<base>.+)\.backup(?:[._-]?{TIMESTAMP_RE})?$", re.IGNORECASE),
    re.compile(rf"^(?P<base>.+?)(?:[._-]bak)[._-]?{TIMESTAMP_RE}$", re.IGNORECASE),
    re.compile(rf"^(?P<base>.+?)[._-]{TIMESTAMP_RE}$", re.IGNORECASE),
]


@dataclasses.dataclass(frozen=True)
class RestorePlan:
    backup_path: Path
    target_path: Path
    existing_target: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview or restore files from common backup filename patterns."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Directory to scan. Defaults to current directory.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually restore files. Without this flag, only prints a dry-run preview.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacing existing target files.",
    )
    parser.add_argument(
        "--keep-current",
        action="store_true",
        help="When overwriting, move the existing target to *.before_restore_<timestamp> first.",
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Only scan the root directory, not child directories.",
    )
    args = parser.parse_args()
    if args.keep_current and not args.overwrite:
        parser.error("--keep-current requires --overwrite")
    return args


def target_name_for(name: str) -> str | None:
    if ".before_restore_" in name:
        return None

    for pattern in BACKUP_PATTERNS:
        match = pattern.match(name)
        if match:
            base = match.group("base")
            if base and base != name:
                return base
    return None


def find_candidates(root: Path, recursive: bool) -> list[Path]:
    entries = root.rglob("*") if recursive else root.glob("*")
    return sorted(path for path in entries if path.is_file())


def build_plans(root: Path, recursive: bool) -> list[RestorePlan]:
    grouped: dict[Path, list[Path]] = {}

    for path in find_candidates(root, recursive):
        target_name = target_name_for(path.name)
        if not target_name:
            continue

        target_path = path.with_name(target_name)
        if target_path == path:
            continue
        grouped.setdefault(target_path, []).append(path)

    plans: list[RestorePlan] = []
    for target_path, backup_paths in grouped.items():
        backup_path = newest_backup(backup_paths)
        plans.append(
            RestorePlan(
                backup_path=backup_path,
                target_path=target_path,
                existing_target=target_path.exists(),
            )
        )

    return sorted(plans, key=lambda plan: str(plan.target_path).lower())


def newest_backup(paths: list[Path]) -> Path:
    return max(paths, key=lambda path: (timestamp_key(path.name), path.stat().st_mtime, path.name))


def timestamp_key(name: str) -> str:
    match = re.search(TIMESTAMP_RE, name)
    return match.group(0).replace("_", "").replace("-", "") if match else ""


def print_plans(plans: list[RestorePlan], root: Path) -> None:
    if not plans:
        print("No backup files matched.")
        return

    for plan in plans:
        status = "overwrite" if plan.existing_target else "create"
        print(f"[{status}] {relative(plan.backup_path, root)} -> {relative(plan.target_path, root)}")


def relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def apply_plans(plans: list[RestorePlan], overwrite: bool, keep_current: bool) -> int:
    failures = 0
    for plan in plans:
        try:
            if plan.target_path.exists():
                if not overwrite:
                    print(f"skip existing target: {plan.target_path}", file=sys.stderr)
                    continue

                if keep_current:
                    preserved = preserved_name(plan.target_path)
                    shutil.move(str(plan.target_path), str(preserved))
                    print(f"preserved: {plan.target_path} -> {preserved}")
                else:
                    plan.target_path.unlink()

            shutil.move(str(plan.backup_path), str(plan.target_path))
            print(f"restored: {plan.backup_path} -> {plan.target_path}")
        except OSError as exc:
            failures += 1
            print(f"failed: {plan.backup_path} -> {plan.target_path}: {exc}", file=sys.stderr)

    return failures


def preserved_name(path: Path) -> Path:
    suffix = f".before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    candidate = path.with_name(f"{path.name}{suffix}")
    index = 1
    while candidate.exists():
        candidate = path.with_name(f"{path.name}{suffix}_{index}")
        index += 1
    return candidate


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    plans = build_plans(root=root, recursive=not args.no_recursive)
    print_plans(plans, root)

    if not args.apply:
        print("\nDry run only. Add --apply to restore files.")
        return 0

    failures = apply_plans(plans, overwrite=args.overwrite, keep_current=args.keep_current)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
