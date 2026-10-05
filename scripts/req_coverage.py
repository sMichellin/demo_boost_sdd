#!/usr/bin/env python3
"""Requirement coverage: share of spec scenarios that have a test tagged with their ID.

Scenarios come from openspec/specs/**/spec.md ("#### Scenario: <ID> <title>"),
tests from @Tag("<ID>") in src/test/java/demo/fromspec.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = ROOT / "openspec" / "specs"
TESTS_DIR = ROOT / "src" / "test" / "java" / "demo" / "fromspec"

SCENARIO_RE = re.compile(r"^####\s+Scenario:\s+(.+?)\s*$", re.MULTILINE)
SCENARIO_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+$")
TAG_RE = re.compile(r'@Tag\(\s*"([^"]+)"\s*\)')


@dataclass
class Scenario:
    id: str | None
    title: str
    spec: str
    covered: bool = False


def collect_scenarios(specs_dir: Path = SPECS_DIR) -> list[Scenario]:
    scenarios = []
    for spec in sorted(specs_dir.glob("**/spec.md")):
        for match in SCENARIO_RE.finditer(spec.read_text(encoding="utf-8")):
            header = match.group(1)
            first, _, rest = header.partition(" ")
            scenario_id = first if SCENARIO_ID_RE.match(first) else None
            title = rest if scenario_id else header
            scenarios.append(Scenario(scenario_id, title, str(spec.relative_to(ROOT))))
    return scenarios


def collect_tags(tests_dir: Path = TESTS_DIR) -> set[str]:
    tags = set()
    for test in tests_dir.glob("**/*.java"):
        tags.update(TAG_RE.findall(test.read_text(encoding="utf-8")))
    return tags


def compute() -> tuple[list[Scenario], float]:
    """Return scenarios with coverage flags and the covered percentage."""
    scenarios = collect_scenarios()
    tags = collect_tags()
    for scenario in scenarios:
        scenario.covered = scenario.id is not None and scenario.id in tags
    if not scenarios:
        return scenarios, 100.0
    covered = sum(s.covered for s in scenarios)
    return scenarios, 100.0 * covered / len(scenarios)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--min", type=float, default=0.0,
                        help="fail (exit 1) if coverage is below this percentage")
    args = parser.parse_args()

    scenarios, percent = compute()
    print("| Scenario | Spec | Test |")
    print("|---|---|---|")
    for s in scenarios:
        name = s.id or f"(no ID) {s.title}"
        print(f"| {name} | {s.spec} | {'yes' if s.covered else 'NO'} |")
    covered = sum(s.covered for s in scenarios)
    print(f"\nRequirement coverage: {percent:.0f}% ({covered}/{len(scenarios)} scenarios)")

    if percent < args.min:
        missing = ", ".join(s.id or s.title for s in scenarios if not s.covered)
        print(f"FAIL: below --min {args.min:.0f}%. Scenarios without a test: {missing}",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
