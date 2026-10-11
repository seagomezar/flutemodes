#!/usr/bin/env python3
"""
Master E2E Test Runner for FluteModes Multiplatform Ecosystem.

Executes all 4 Tiers of opaque-box, requirement-driven tests:
- Tier 1: Feature Coverage (11 modules, >=5 tests/feature)
- Tier 2: Boundary & Corner Cases (11 modules, >=5 tests/feature)
- Tier 3: Cross-Feature Combinations (pairwise interactions, parity, links)
- Tier 4: Real-World Application Scenarios (practice cycles, distribution assets)

Generates human-readable terminal output and a structured JSON report at:
tests/e2e_test_report.json
"""

import sys
import os
import time
import json
import unittest
import argparse
from pathlib import Path

# Ensure workspace root is in sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from tests.test_tier1_features import (
    TestTier1Modos,
    TestTier1EJ1,
    TestTier1EJ2,
    TestTier1EJ4,
    TestTier1EJ5,
    TestTier1EJ10,
    TestTier1EJ11,
    TestTier1ReichertR1,
    TestTier1ReichertR2,
    TestTier1ReichertR4,
    TestTier1ReichertR5
)
from tests.test_tier2_boundaries import (
    TestTier2ModosBoundaries,
    TestTier2EJ1Boundaries,
    TestTier2EJ2Boundaries,
    TestTier2EJ4Boundaries,
    TestTier2EJ5Boundaries,
    TestTier2EJ10Boundaries,
    TestTier2EJ11Boundaries,
    TestTier2ReichertR1Boundaries,
    TestTier2ReichertR2Boundaries,
    TestTier2ReichertR4Boundaries,
    TestTier2ReichertR5Boundaries
)
from tests.test_tier3_combinations import TestTier3Combinations
from tests.test_tier4_scenarios import TestTier4Scenarios


class CustomE2ETestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_records.append({
            "test_id": test.id(),
            "description": test.shortDescription() or test._testMethodName,
            "status": "PASS",
            "message": None
        })

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_records.append({
            "test_id": test.id(),
            "description": test.shortDescription() or test._testMethodName,
            "status": "FAIL",
            "message": str(err[1])
        })

    def addError(self, test, err):
        super().addError(test, err)
        self.test_records.append({
            "test_id": test.id(),
            "description": test.shortDescription() or test._testMethodName,
            "status": "ERROR",
            "message": str(err[1])
        })


def build_suite(tier_filter: str = "all") -> unittest.TestSuite:
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    tier1_classes = [
        TestTier1Modos, TestTier1EJ1, TestTier1EJ2, TestTier1EJ4,
        TestTier1EJ5, TestTier1EJ10, TestTier1EJ11,
        TestTier1ReichertR1, TestTier1ReichertR2, TestTier1ReichertR4, TestTier1ReichertR5
    ]
    tier2_classes = [
        TestTier2ModosBoundaries, TestTier2EJ1Boundaries, TestTier2EJ2Boundaries, TestTier2EJ4Boundaries,
        TestTier2EJ5Boundaries, TestTier2EJ10Boundaries, TestTier2EJ11Boundaries,
        TestTier2ReichertR1Boundaries, TestTier2ReichertR2Boundaries,
        TestTier2ReichertR4Boundaries, TestTier2ReichertR5Boundaries
    ]
    tier3_classes = [TestTier3Combinations]
    tier4_classes = [TestTier4Scenarios]

    if tier_filter in ("all", "1"):
        for cls in tier1_classes:
            suite.addTests(loader.loadTestsFromTestCase(cls))
    if tier_filter in ("all", "2"):
        for cls in tier2_classes:
            suite.addTests(loader.loadTestsFromTestCase(cls))
    if tier_filter in ("all", "3"):
        for cls in tier3_classes:
            suite.addTests(loader.loadTestsFromTestCase(cls))
    if tier_filter in ("all", "4"):
        for cls in tier4_classes:
            suite.addTests(loader.loadTestsFromTestCase(cls))

    return suite


def categorize_defects(records):
    """Categorize failures by known project defect identifiers."""
    defects = {
        "DEF-01": {"name": "Missing Schott Renderers in score_template.html", "count": 0, "tests": []},
        "DEF-02": {"name": "Android EJ2 Accidental Fix mm. 4, 8, 14, 18, 22, 24, 28", "count": 0, "tests": []},
        "DEF-03": {"name": "Android Audio EJ2 Diminished Semitone", "count": 0, "tests": []},
        "DEF-05": {"name": "Android Audio R.5 Triplet Timing Divisor 6.0", "count": 0, "tests": []},
        "DEF-06": {"name": "Web Portal Reichert ABC Download Links Casing", "count": 0, "tests": []},
        "DEF-07": {"name": "Missing 00_Coleccion_Completa_84_Modos_EJ4.abc in downloads", "count": 0, "tests": []},
        "DEF-08": {"name": "Missing highlightNote/clearHighlight in score_template.html", "count": 0, "tests": []},
        "DEF-09": {"name": "Android Reichert Route Navigation & Dialog", "count": 0, "tests": []},
        "DEF-14": {"name": "Multiplatform Version Bump to v1.5.1 Target", "count": 0, "tests": []},
        "OTHER": {"name": "Uncategorized Defect / Expectation Mismatch", "count": 0, "tests": []}
    }

    for r in records:
        if r["status"] in ("FAIL", "ERROR"):
            msg = (r["message"] or "") + " " + r["test_id"]
            matched = False
            for code in ["DEF-01", "DEF-02", "DEF-03", "DEF-05", "DEF-06", "DEF-07", "DEF-08", "DEF-09"]:
                if code in msg:
                    defects[code]["count"] += 1
                    defects[code]["tests"].append(r["test_id"])
                    matched = True
                    break
            if not matched:
                if "version" in msg.lower():
                    defects["DEF-14"]["count"] += 1
                    defects["DEF-14"]["tests"].append(r["test_id"])
                else:
                    defects["OTHER"]["count"] += 1
                    defects["OTHER"]["tests"].append(r["test_id"])

    return defects


def main():
    parser = argparse.ArgumentParser(description="FluteModes E2E Test Suite Runner")
    parser.add_argument("--tier", choices=["all", "1", "2", "3", "4"], default="all",
                        help="Filter execution by test tier (default: all)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose test execution output")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON summary report to stdout")
    args = parser.parse_args()

    print("=" * 80)
    print("FLUTEMODES MULTIPLATFORM ECOSYSTEM — E2E TEST RUNNER")
    print(f"Target: Tier {args.tier.upper()} | Workspace: {WORKSPACE_ROOT}")
    print("=" * 80)

    suite = build_suite(args.tier)
    start_time = time.time()

    runner = unittest.TextTestRunner(
        resultclass=CustomE2ETestResult,
        verbosity=2 if args.verbose else 1
    )
    result = runner.run(suite)
    elapsed = time.time() - start_time

    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors

    defects = categorize_defects(result.test_records)

    report_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tier": args.tier,
        "total_tests": total_tests,
        "passed": passed,
        "failed": failures,
        "errors": errors,
        "pass_rate_percent": round((passed / total_tests * 100), 2) if total_tests > 0 else 0,
        "duration_seconds": round(elapsed, 3),
        "defects_summary": defects,
        "test_results": result.test_records
    }

    report_path = WORKSPACE_ROOT / "tests" / "e2e_test_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    print("\n" + "=" * 80)
    print("E2E TEST EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Total Tests Executed : {total_tests}")
    print(f"Passed               : {passed} ({report_data['pass_rate_percent']}%)")
    print(f"Failed               : {failures}")
    print(f"Errors               : {errors}")
    print(f"Execution Time       : {elapsed:.2f} seconds")
    print(f"Detailed JSON Report : {report_path}")
    print("-" * 80)

    print("DEFECTS & BASELINE GAP BREAKDOWN:")
    for code, info in defects.items():
        if info["count"] > 0:
            print(f"  [{code}] {info['name']}: {info['count']} failing tests")
            for t in info["tests"]:
                print(f"      - {t}")
    print("=" * 80)

    if args.json:
        print(json.dumps(report_data, indent=2))

    # Exit code: 0 if all pass, 1 if failures exist
    sys.exit(0 if (failures == 0 and errors == 0) else 1)


if __name__ == "__main__":
    main()
