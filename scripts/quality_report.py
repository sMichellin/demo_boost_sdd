#!/usr/bin/env python3
"""Quality report for a PR: three metrics that matter, plus two that do not.

Reads PIT, JaCoCo and surefire reports from target/, scenarios from openspec/specs
and escaped defects from metrics/escaped_defects.csv. Prints Markdown to stdout.
Missing inputs are reported as n/a, so the report can run even after a failed gate.
"""
from __future__ import annotations

import argparse
import csv
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import req_coverage

ROOT = Path(__file__).resolve().parent.parent


def show(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def pct(part: int, total: int) -> str:
    return f"{100.0 * part / total:.0f}% ({part}/{total})" if total else "n/a"


def mutation_score(path: Path) -> str:
    if not path.exists():
        return f"n/a (нет {show(path)})"
    mutations = ET.parse(path).getroot().findall("mutation")
    detected = sum(m.get("detected") == "true" for m in mutations)
    return pct(detected, len(mutations))


def requirement_coverage() -> tuple[str, list[str]]:
    scenarios, _ = req_coverage.compute()
    covered = sum(s.covered for s in scenarios)
    missing = [s.id or s.title for s in scenarios if not s.covered]
    return pct(covered, len(scenarios)) + " сценариев", missing


def escape_rate(path: Path) -> str:
    if not path.exists():
        return f"n/a (нет {show(path)})"
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    prod = sum(r["found_at"].strip() == "prod" for r in rows)
    dates = sorted(r["date"] for r in rows if r.get("date"))
    period = f", {dates[0]} … {dates[-1]}" if dates else ""
    return pct(prod, len(rows)) + period


def line_coverage(path: Path) -> str:
    if not path.exists():
        return f"n/a (нет {show(path)})"
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    covered = sum(int(r["LINE_COVERED"]) for r in rows)
    missed = sum(int(r["LINE_MISSED"]) for r in rows)
    return pct(covered, covered + missed)


def test_count(reports_dir: Path) -> str:
    suites = [ET.parse(p).getroot() for p in sorted(reports_dir.glob("TEST-*.xml"))]
    if not suites:
        return f"n/a (нет {show(reports_dir)})"
    total = sum(int(s.get("tests", 0)) for s in suites)
    failed = sum(int(s.get("failures", 0)) + int(s.get("errors", 0)) for s in suites)
    skipped = sum(int(s.get("skipped", 0)) for s in suites)
    return f"{total - failed - skipped} passed, {failed} failed, {skipped} skipped"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pit", type=Path, default=ROOT / "target/pit-reports/mutations.xml")
    parser.add_argument("--jacoco", type=Path, default=ROOT / "target/site/jacoco/jacoco.csv")
    parser.add_argument("--surefire", type=Path, default=ROOT / "target/surefire-reports")
    parser.add_argument("--escaped", type=Path, default=ROOT / "metrics/escaped_defects.csv")
    args = parser.parse_args()

    req, missing = requirement_coverage()
    print("## Отчёт о качестве\n")
    print("| Метрика | Значение | Источник |")
    print("|---|---|---|")
    print(f"| **Mutation score** | {mutation_score(args.pit)} | PIT, тесты из спеки |")
    print(f"| **Покрытие требований** | {req} | `openspec/specs` + `@Tag` |")
    print(f"| **Defect escape rate** | {escape_rate(args.escaped)} | `metrics/escaped_defects.csv` |")
    if missing:
        print(f"\nСценарии без теста: {', '.join(missing)}")

    print("\n### Для контраста: не является аргументом\n")
    print("| Метрика | Значение | Источник |")
    print("|---|---|---|")
    print(f"| Line coverage | {line_coverage(args.jacoco)} | JaCoCo |")
    print(f"| Число тестов | {test_count(args.surefire)} | surefire |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
