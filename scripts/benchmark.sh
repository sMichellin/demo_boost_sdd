#!/usr/bin/env bash
# Benchmark on our own defects (scenario F, slides 15 and 19).
#
# For every patch in benchmark/defects/: check out HEAD into a temporary git worktree,
# apply the patch (the defect comes back), run one test suite and count the defect
# as caught if a test that passes on clean HEAD now fails.
#
# Usage: scripts/benchmark.sh [--suite from-spec|from-code]
# Env:   MVN  Maven command (default: mvn)
set -euo pipefail

SUITE=from-spec
while [[ $# -gt 0 ]]; do
  case "$1" in
    --suite) SUITE="$2"; shift 2 ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

case "$SUITE" in
  from-spec)
    # Every scenario ID from the current specs, as a JUnit 5 tag expression
    TAGS="$(grep -rhoE '^#### Scenario: [A-Z][A-Z0-9-]*-[0-9]+' openspec/specs | awk '{print $3}' | sort -u | paste -sd '|' -)"
    MVN_ARGS=(-Dgroups="$TAGS") ;;
  from-code)
    MVN_ARGS=(-Pdemo-from-code) ;;
  *) echo "unknown suite: $SUITE (expected from-spec or from-code)" >&2; exit 2 ;;
esac

MVN="${MVN:-mvn}"
RESULTS="$ROOT/benchmark/results.csv"
WORK="$(mktemp -d)"
cleanup() {
  for wt in "$WORK"/wt-*; do
    [[ -d "$wt" ]] && git worktree remove --force "$wt" >/dev/null 2>&1
  done
  git worktree prune
  rm -rf "$WORK"
}
trap cleanup EXIT

# Print "Class#method" for every failed or errored test in surefire XML reports
failing_tests() {
  local reports="$1"
  compgen -G "$reports/TEST-*.xml" >/dev/null || return 0
  awk '
    /<testcase / {
      match($0, / name="[^"]*"/);      name = substr($0, RSTART + 7, RLENGTH - 8)
      match($0, / classname="[^"]*"/); cls  = substr($0, RSTART + 12, RLENGTH - 13)
    }
    /<(failure|error)[ >\/]/ { print cls "#" name }
  ' "$reports"/TEST-*.xml | sort -u
}

# run_suite <name> [patch]: fresh worktree of HEAD, optional patch, failing tests to stdout
run_suite() {
  local name="$1" patch="${2:-}" wt="$WORK/wt-$1"
  git worktree add --quiet --detach "$wt" HEAD
  if [[ -n "$patch" ]]; then
    git -C "$wt" apply "$patch"
  fi
  if (cd "$wt" && "$MVN" -q -B test -Dmaven.test.failure.ignore=true "${MVN_ARGS[@]}" >"$WORK/$name.log" 2>&1); then
    failing_tests "$wt/target/surefire-reports"
  else
    echo "BUILD-ERROR"
  fi
  git worktree remove --force "$wt"
}

echo "Suite: $SUITE"
echo "Baseline (clean HEAD)..."
run_suite baseline >"$WORK/baseline.txt"
if grep -q BUILD-ERROR "$WORK/baseline.txt"; then
  echo "Baseline build failed, see log:" >&2
  cat "$WORK/baseline.log" >&2
  exit 1
fi

# Keep rows of the other suite, rewrite rows of this one
TMP_RESULTS="$WORK/results.csv"
echo "suite,defect_id,caught,failing_tests" >"$TMP_RESULTS"
if [[ -f "$RESULTS" ]]; then
  tail -n +2 "$RESULTS" | grep -v "^$SUITE," >>"$TMP_RESULTS" || true
fi

total=0
caught=0
for patch in "$ROOT"/benchmark/defects/*.patch; do
  id="$(basename "$patch" .patch)"
  total=$((total + 1))
  run_suite "$id" "$patch" >"$WORK/$id.txt"
  # New failures = failing now, but not on clean HEAD
  new_failures="$(comm -13 "$WORK/baseline.txt" "$WORK/$id.txt" | paste -sd ';' -)"
  if [[ -n "$new_failures" ]]; then
    caught=$((caught + 1))
    printf '  %-34s caught  %s\n' "$id" "$new_failures"
    echo "$SUITE,$id,yes,$new_failures" >>"$TMP_RESULTS"
  else
    printf '  %-34s MISSED\n' "$id"
    echo "$SUITE,$id,no," >>"$TMP_RESULTS"
  fi
done

cp "$TMP_RESULTS" "$RESULTS"
echo "$SUITE: caught $caught of $total"
