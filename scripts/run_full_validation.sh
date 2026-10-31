#!/usr/bin/env bash
# =============================================================================
# run_full_validation.sh — reproduzierbare Validierungsmatrix für ssz-qubits
# Teil des Reparatur-/Audit-Auftrags 2026-10-31 (Branch audit/ssz-qubits-repair-8to6-20261031)
#
# Regeln (Auftrag §0.5):
#  - set -Eeuo pipefail, Zeitstempel, Exitcodes, JUnit-XML, stdout/stderr-Logs
#  - Fehler werden NICHT weggefiltert; || true nur für ausdrücklich erwartete
#    Negativläufe (hier: verify_phi_discretization.py ohne SciPy).
#
# Nutzung:
#   PYTHON=/pfad/zu/python scripts/run_full_validation.sh <label>
#   PYTHON muß die Project-Abhängigkeiten haben (numpy, matplotlib, pytest;
#   scipy optional — der φ-Lauf wird in beiden Fällen mit wahrem Exitcode
#   protokolliert und als EXPECTED_FAIL bzw. PASS klassifiziert).
# =============================================================================
set -Eeuo pipefail

LABEL="${1:?Usage: run_full_validation.sh <label> z.B. baseline|post-repair}"
PYTHON="${PYTHON:-python3}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAMP="$(date +%Y-%m-%dT%H:%M:%S%z)"
OUT_DIR="$REPO_ROOT/reports/repair_validation/${LABEL}-${STAMP}"
mkdir -p "$OUT_DIR"

STATUS_FILE="$OUT_DIR/status.tsv"
: > "$STATUS_FILE"
echo -e "run\texitcode\tclassification\tlog" > "$STATUS_FILE"

log_env() {
    {
        echo "timestamp: $STAMP"
        echo "label:     $LABEL"
        echo "host:      $(uname -srmo)"
        echo "repo_root: $REPO_ROOT"
        echo "git_head:  $(git -C "$REPO_ROOT" rev-parse HEAD 2>/dev/null || echo 'n/a')"
        echo "git_branch: $(git -C "$REPO_ROOT" branch --show-current 2>/dev/null || echo 'n/a')"
        echo "python:    $($PYTHON --version 2>&1)"
        echo "scipy:     $($PYTHON -c 'import scipy; print(scipy.__version__)' 2>/dev/null || echo 'NICHT INSTALLIERT')"
        echo "pip_freeze:"
        $PYTHON -m pip freeze 2>/dev/null | sed 's/^/  /'
    } > "$OUT_DIR/environment.txt"
}

# run <name> <expected: pass|fail-ok> <cmd...>
run() {
    local name="$1"; shift
    local expected="$1"; shift
    local rc=0
    echo "[$(date +%H:%M:%S)] RUN  $name" | tee -a "$OUT_DIR/progress.log"
    "$PYTHON" "$@" > "$OUT_DIR/${name}.log" 2>&1 || rc=$?
    local cls
    if [ "$rc" -eq 0 ]; then cls="PASS";
    elif [ "$expected" = "fail-ok" ]; then cls="EXPECTED_FAIL";
    else cls="FAIL"; fi
    printf '%s\t%s\t%s\t%s\n' "$name" "$rc" "$cls" "${name}.log" >> "$STATUS_FILE"
    echo "[$(date +%H:%M:%S)] EXIT $name rc=$rc ($cls)" | tee -a "$OUT_DIR/progress.log"
    return 0   # einzelne FAILs brechen die Matrix NICHT ab; Gesamtkennzahl unten
}

log_env

# --- 1. volle pytest-Suite (echter pytest-Exitstatus, kein Runner-Filter) ----
echo "[$(date +%H:%M:%S)] RUN  pytest-full" | tee -a "$OUT_DIR/progress.log"
prc=0
$PYTHON -m pytest -v --tb=long -p no:cacheprovider \
    --junitxml="$OUT_DIR/pytest-results.xml" \
    > "$OUT_DIR/pytest-full.log" 2>&1 || prc=$?
printf 'pytest-full\t%s\t%s\tpytest-full.log\n' "$prc" "$([ "$prc" -eq 0 ] && echo PASS || echo FAIL)" >> "$STATUS_FILE"

# --- 2. dokumentierte Einstiegspunkte (Auftrag §0.6) -------------------------
# SciPy-Verfügbarkeit für φ-Lauf-Klassifikation bestimmen:
if $PYTHON -c 'import scipy' 2>/dev/null; then PHI_EXPECT=pass; else PHI_EXPECT=fail-ok; fi

run run_tests             pass  run_tests.py
run verify_phi_discret    "$PHI_EXPECT"  verify_phi_discretization.py
run verify_paper_a_form   pass  verify_paper_a_formulas.py
run comprehensive_test    pass  comprehensive_test.py
run test_corrections      pass  test_corrections.py
run test_paper_consist    pass  test_paper_consistency.py
run demo                  pass  demo.py

# --- 3. Discovery-Zahl (maschinenlesbar) -------------------------------------
$PYTHON -m pytest --collect-only -q -p no:cacheprovider > "$OUT_DIR/collect-only.txt" 2>&1 || true

# --- 4. Gesamturteil (maschinenlesbar + menschenlesbar) ----------------------
$PYTHON - "$STATUS_FILE" > "$OUT_DIR/summary.json" <<'PYEOF'
import json, sys
rows = []
with open(sys.argv[1]) as f:
    header = next(f)
    for line in f:
        run, rc, cls, log = line.rstrip("\n").split("\t")
        rows.append({"run": run, "exitcode": int(rc), "classification": cls, "log": log})
fails  = [r for r in rows if r["classification"] == "FAIL"]
expf   = [r for r in rows if r["classification"] == "EXPECTED_FAIL"]
summary = {
    "total_runs": len(rows),
    "passed": len(rows) - len(fails) - len(expf),
    "expected_fail": len(expf),
    "failed": len(fails),
    "overall": "PASS" if not fails else "FAIL",
    "runs": rows,
}
print(json.dumps(summary, indent=2))
sys.exit(0 if not fails else 1)
PYEOF
SUMMARY_RC=$? || true

echo
echo "=== VALIDIERUNG $LABEL — $(grep -c PASS "$STATUS_FILE" || true) PASS, $(grep -c FAIL "$STATUS_FILE" || true) FAIL-zeilen ==="
cat "$STATUS_FILE"
echo "Log-Verzeichnis: $OUT_DIR"
exit "$SUMMARY_RC"
