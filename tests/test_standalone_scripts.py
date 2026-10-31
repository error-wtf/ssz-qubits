#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone-Skripte als gesammelte pytest-Fälle (Reparatur 2026-10-31, T3).

`test_paper_consistency.py`, `comprehensive_test.py` und `verify_paper_a_formulas.py`
führen ihre Prüfungen bisher nur beim direkten Ausführen (Modul-Asserts bzw.
eigenes error handling) aus — sie waren damit keine gesammelten pytest-Fälle.
Diese Datei macht jeden Skriptlauf zu einem Testfall MIT wahrem Exitcode
(Auftrag §7.6: End-to-End propagiert Exitcodes).

Die Originalskripte werden NICHT verändert; pytest importiert sie zusätzlich
bei der Sammlung (Modul-Asserts laufen dann ohnehin).
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(script: str, timeout: int = 300):
    return subprocess.run(
        [sys.executable, script],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def test_paper_consistency_script_exit_0():
    r = _run("test_paper_consistency.py")
    assert r.returncode == 0, f"stderr tail: {r.stderr[-1500:]}"


def test_comprehensive_script_exit_0():
    r = _run("comprehensive_test.py")
    assert r.returncode == 0, f"stderr tail: {r.stderr[-1500:]}"
    # Der frühere Claim „REPOSITORY IS 100% CORRECT" ist ersetzt (T5):
    assert "REPOSITORY IS 100% CORRECT" not in r.stdout
    assert "NOT a physics-validity claim" in r.stdout


def test_verify_paper_a_formulas_exit_0():
    r = _run("verify_paper_a_formulas.py")
    assert r.returncode == 0, f"stderr tail: {r.stderr[-1500:]}"


def test_verify_phi_discretization_exit_0():
    """scipy ist seit T4 in requirements.txt → Skript MUSS laufen."""
    r = _run("verify_phi_discretization.py")
    assert r.returncode == 0, f"stderr tail: {r.stderr[-1500:]}"
