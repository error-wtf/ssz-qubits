#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ-Qubits Test Runner

Runs all tests and generates comprehensive output with physical interpretations.

© 2025 Carmen Wrede, Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# UTF-8 for Windows
os.environ['PYTHONIOENCODING'] = 'utf-8:replace'

# Project root
PROJECT_ROOT = Path(__file__).parent.absolute()
TESTS_DIR = PROJECT_ROOT / "tests"
REPORTS_DIR = PROJECT_ROOT / "reports"


def ensure_reports_dir():
    """Create reports directory if it doesn't exist."""
    REPORTS_DIR.mkdir(exist_ok=True)


def run_test_file(test_file: Path) -> dict:
    """Run a single test file and capture output."""
    print(f"\n{'='*70}")
    print(f"RUNNING: {test_file.name}")
    print(f"{'='*70}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300
        )
        
        elapsed = time.time() - start_time
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        success = result.returncode == 0
        
        return {
            'file': test_file.name,
            'success': success,
            'returncode': result.returncode,
            'elapsed': elapsed,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT: {test_file.name} exceeded 300 seconds")
        return {
            'file': test_file.name,
            'success': False,
            'returncode': -1,
            'elapsed': 300,
            'stdout': '',
            'stderr': 'TIMEOUT'
        }
    except Exception as e:
        print(f"ERROR: {e}")
        return {
            'file': test_file.name,
            'success': False,
            'returncode': -1,
            'elapsed': 0,
            'stdout': '',
            'stderr': str(e)
        }


def run_demo():
    """Run the main module demo."""
    print(f"\n{'='*70}")
    print("RUNNING: ssz_qubits.py (Demo)")
    print(f"{'='*70}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "ssz_qubits.py")],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        return {
            'file': 'ssz_qubits.py (Demo)',
            'success': result.returncode == 0,
            'returncode': result.returncode,
            'elapsed': elapsed,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
    except Exception as e:
        return {
            'file': 'ssz_qubits.py (Demo)',
            'success': False,
            'returncode': -1,
            'elapsed': 0,
            'stdout': '',
            'stderr': str(e)
        }


def count_tests_in_output(stdout: str) -> tuple:
    """Count passed/failed tests from pytest output."""
    passed = 0
    failed = 0
    
    # Look for pytest summary line
    for line in stdout.split('\n'):
        if 'passed' in line.lower():
            # Try to extract number
            parts = line.split()
            for i, part in enumerate(parts):
                if part == 'passed' and i > 0:
                    try:
                        passed = int(parts[i-1])
                    except ValueError:
                        pass
        if 'failed' in line.lower():
            parts = line.split()
            for i, part in enumerate(parts):
                if part == 'failed' and i > 0:
                    try:
                        failed = int(parts[i-1])
                    except ValueError:
                        pass
    
    return passed, failed


def generate_summary(results: list) -> str:
    """Generate summary report."""
    total_passed = 0
    total_failed = 0
    total_time = 0
    
    summary_lines = []
    summary_lines.append("=" * 70)
    summary_lines.append("SSZ-QUBITS TEST SUMMARY")
    summary_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary_lines.append("=" * 70)
    summary_lines.append("")
    
    summary_lines.append(f"{'Test File':<40} | {'Status':<10} | {'Time':<10}")
    summary_lines.append("-" * 65)
    
    for r in results:
        status = "PASS" if r['success'] else "FAIL"
        time_str = f"{r['elapsed']:.2f}s"
        summary_lines.append(f"{r['file']:<40} | {status:<10} | {time_str:<10}")
        
        if r['success']:
            passed, failed = count_tests_in_output(r['stdout'])
            total_passed += max(passed, 1)  # At least 1 if success
        else:
            total_failed += 1
        
        total_time += r['elapsed']
    
    summary_lines.append("-" * 65)
    summary_lines.append("")
    
    all_success = all(r['success'] for r in results)
    
    summary_lines.append("RESULTS:")
    summary_lines.append(f"  Total test files: {len(results)}")
    summary_lines.append(f"  Passed: {sum(1 for r in results if r['success'])}")
    summary_lines.append(f"  Failed: {sum(1 for r in results if not r['success'])}")
    summary_lines.append(f"  Total time: {total_time:.2f}s")
    summary_lines.append("")
    
    if all_success:
        summary_lines.append("STATUS: ALL TESTS PASSED")
    else:
        summary_lines.append("STATUS: SOME TESTS FAILED")
        summary_lines.append("")
        summary_lines.append("Failed tests:")
        for r in results:
            if not r['success']:
                summary_lines.append(f"  - {r['file']}")
    
    summary_lines.append("")
    summary_lines.append("=" * 70)
    
    return "\n".join(summary_lines)


def main():
    """Main test runner."""
    print("\n" + "=" * 70)
    print("SSZ-QUBITS COMPLETE TEST SUITE")
    print("Segmented Spacetime Framework for Quantum Computing")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    ensure_reports_dir()
    
    results = []
    all_output = []
    
    # 1. Run demo first
    print("\n[PHASE 1] Running Core Module Demo")
    demo_result = run_demo()
    results.append(demo_result)
    all_output.append(f"=== {demo_result['file']} ===\n{demo_result['stdout']}")
    
    # 2. Run all test files
    print("\n[PHASE 2] Running Test Suite")
    
    test_files = sorted(TESTS_DIR.glob("test_*.py"))
    
    for test_file in test_files:
        result = run_test_file(test_file)
        results.append(result)
        all_output.append(f"=== {result['file']} ===\n{result['stdout']}")
    
    # 3. Generate summary
    print("\n[PHASE 3] Generating Summary")
    summary = generate_summary(results)
    print(summary)
    
    # 4. Save reports
    summary_file = REPORTS_DIR / "RUN_SUMMARY.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"# SSZ-Qubits Test Summary\n\n")
        f.write(f"```\n{summary}\n```\n")
    print(f"\nSummary saved to: {summary_file}")
    
    full_output_file = REPORTS_DIR / "full-output.md"
    with open(full_output_file, 'w', encoding='utf-8') as f:
        f.write(f"# SSZ-Qubits Full Test Output\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for output in all_output:
            f.write(f"```\n{output}\n```\n\n")
    print(f"Full output saved to: {full_output_file}")
    
    # Return exit code
    all_success = all(r['success'] for r in results)
    
    # License notice
    print()
    print("=" * 70)
    print("SSZ-Qubits - Segmented Spacetime Framework for Quantum Computing")
    print("Copyright (c) 2025 Carmen Wrede and Lino Casu")
    print("Licensed under the Anti-Capitalist Software License v1.4")
    print("https://github.com/error-wtf/ssz-qubits")
    print("=" * 70)
    
    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())
