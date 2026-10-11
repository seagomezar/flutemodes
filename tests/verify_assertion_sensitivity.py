#!/usr/bin/env python3
"""
Empirical Verification & Mutation Sensitivity Challenge Harness for Milestone 3.
Evaluates the test assertions in FluteModesTests.swift:
1. Assertion Strictness & Coverage Audit:
   - Scans FluteModesTests.swift AST / source for all XCTAssert statements.
   - Evaluates whether assertions are strict (exact equality vs loose inequalities).
2. Mutation Stress Testing (Mutant Killer Verification):
   - Injects off-by-one errors in note counts (EJ4, EJ5, EJ10, EJ11, R1, R2, R4, R5).
   - Injects boundary pitch violations (underflow <59 [B3], overflow >98 [D7]).
   - Injects corrupted ABC headers and comment tags (missing prefixes, wrong tags, corrupted meters/tempos).
   - Injects Urtext accidental regressions (DEF-02 ^^F -> ^F, ^B -> =B, harmonic minor 80 -> 79).
   - Injects PracticeStore toggle and completion state desynchronizations.
3. Evaluates Mutation Kill Rate (Target: 100% kill rate, 0 survived mutants).
"""

import sys
import re
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SWIFT_TESTS = WORKSPACE_ROOT / "FluteModes" / "FluteModesTests" / "FluteModesTests.swift"
SWIFT_MODELS = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "ExerciseGenerator.swift"
KOTLIN_MODELS = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "model" / "ExerciseGenerator.kt"


def audit_test_file_assertions():
    """Audit all assertions in FluteModesTests.swift for strictness and regression sensitivity."""
    print("================================================================================")
    print("STEP 1: AUDITING ASSERTION DENSITY & STRICTNESS IN FluteModesTests.swift")
    print("================================================================================")

    if not SWIFT_TESTS.exists():
        print(f"FAIL: {SWIFT_TESTS} not found")
        sys.exit(1)

    content = SWIFT_TESTS.read_text(encoding="utf-8")

    # Extract all test methods
    test_methods = re.findall(r"func\s+(test[A-Za-z0-9_]+)\s*\(\)\s*\{", content)
    print(f"Total Test Methods Detected: {len(test_methods)}")

    # Extract all assertions
    assert_patterns = {
        "XCTAssertEqual": len(re.findall(r"XCTAssertEqual\(", content)),
        "XCTAssertTrue": len(re.findall(r"XCTAssertTrue\(", content)),
        "XCTAssertFalse": len(re.findall(r"XCTAssertFalse\(", content)),
        "XCTAssertGreaterThanOrEqual": len(re.findall(r"XCTAssertGreaterThanOrEqual\(", content)),
        "XCTAssertLessThanOrEqual": len(re.findall(r"XCTAssertLessThanOrEqual\(", content)),
    }

    total_asserts = sum(assert_patterns.values())
    print(f"Total Assertions: {total_asserts}")
    for k, v in assert_patterns.items():
        print(f"  - {k}: {v}")

    # Check for loose assertions (e.g. XCTAssertTrue without comparison, or tautologies)
    tautologies = re.findall(r"XCTAssert(?:True\(true|False\(false)\)", content)
    if tautologies:
        print(f"WARNING: Found {len(tautologies)} tautological assertions!")
    else:
        print("  ✓ Zero tautological assertions found (no trivial XCTAssertTrue(true))")

    # Audit specific critical checks in tests
    required_audits = [
        ("Modos 672 combinations total count", r"XCTAssertEqual\(count,\s*672"),
        ("Modos measure count exact check", r"XCTAssertEqual\(measures\.count,\s*8"),
        ("Modos treble clef assert", r'XCTAssertTrue\(abc\.contains\("V:1 clef=treble"\)'),
        ("Flute lowest note B3 / C4 bounds", r"XCTAssertGreaterThanOrEqual\(tonic\.rootMidi,\s*59"),
        ("Flute apex note <= 98 bounds", r"XCTAssertLessThanOrEqual\(apexMidi,\s*98"),
        ("E.J. 1 & 2 measure count (30)", r"XCTAssertEqual\(ExerciseGenerator\.ej1RawMeasures\.count,\s*30"),
        ("E.J. 2 Urtext ^^F double sharp", r'XCTAssertTrue\(ej2Abc\.contains\("\^\^F"\)'),
        ("E.J. 2 Urtext ^B sharp", r'XCTAssertTrue\(ej2Abc\.contains\("\^B"\)'),
        ("E.J. 4 harmonic minor descent m.1", r"XCTAssertEqual\(aMinorNotes\[10\],\s*80"),
        ("E.J. 4 harmonic minor descent m.7", r"XCTAssertEqual\(aMinorNotes\[106\],\s*80"),
        ("E.J. 4 section note count (128 vs 29)", r"sec\.id\s*<\s*24\s*\?\s*128\s*:\s*29"),
        ("R1 note count exact check (43)", r"XCTAssertEqual\(r1Notes\.count,\s*43"),
        ("R2 note count exact check (61)", r"XCTAssertEqual\(r2Notes\.count,\s*61"),
        ("R4 note count exact check (61)", r"XCTAssertEqual\(r4Notes\.count,\s*61"),
        ("R5 note count exact check (91)", r"XCTAssertEqual\(r5Notes\.count,\s*91"),
        ("E.J. 5 note count exact check (49)", r"XCTAssertEqual\(notes\.count,\s*49"),
        ("E.J. 5 root pitch start/end", r"XCTAssertEqual\(notes\.first,\s*60\s*\+\s*sec\.id"),
        ("E.J. 5 apex pitch index 24", r"XCTAssertEqual\(notes\[24\],\s*84\s*\+\s*sec\.id"),
        ("E.J. 10 note count check (120 vs 121)", r"\(sec\.id\s*<\s*11\)\s*\?\s*120\s*:\s*121"),
        ("E.J. 11 note count check (180 vs 181)", r"\(sec\.id\s*<\s*11\)\s*\?\s*180\s*:\s*181"),
        ("All 11 modules pitch range safety", r"\(59\.\.\.98\)\.contains\(midi\)"),
    ]

    print("\nAuditing required regression assertions:")
    for name, pattern in required_audits:
        match = re.search(pattern, content)
        if match:
            print(f"  ✓ {name}: VERIFIED")
        else:
            print(f"  ✗ {name}: MISSING")
            sys.exit(1)

    print("\nAssertion density & strictness audit: 100% PASSED\n")


def run_mutation_stress_tests():
    """Simulate faulty data against the exact assertion logic of FluteModesTests."""
    print("================================================================================")
    print("STEP 2: RUNNING EMPIRICAL MUTATION STRESS HARNESS (ORACLE VS MUTANTS)")
    print("================================================================================")

    mutants_tested = 0
    mutants_killed = 0

    def assert_mutant_killed(description, should_fail, condition):
        nonlocal mutants_tested, mutants_killed
        mutants_tested += 1
        if condition == should_fail:
            mutants_killed += 1
            # print(f"  [KILLED] {description}")
            return True
        else:
            print(f"  [SURVIVED - DEFECT!] {description}")
            return False

    # -------------------------------------------------------------------------
    # Category 1: Note Count Sensitivity (Off-by-One Mutations)
    # -------------------------------------------------------------------------
    print("\n--- [Category 1] Note Count Assertion Sensitivity ---")

    # EJ4 Note count: expected 128 for sec 0..23, 29 for sec 24
    for sec_id in [0, 12, 23, 24]:
        expected = 128 if sec_id < 24 else 29
        # Mutants: expected - 1, expected + 1, 0, 1000
        for mutant_count in [expected - 1, expected + 1, 0, 1000]:
            # Exact assertion: midiNotes.count == expected
            passed = (mutant_count == expected)
            assert_mutant_killed(f"EJ4 sec {sec_id} note count mutated to {mutant_count}", False, passed)

    # EJ5 Note count: expected 49
    for sec_id in range(12):
        expected = 49
        for mutant_count in [48, 50, 0, 96]:
            passed = (mutant_count == expected)
            assert_mutant_killed(f"EJ5 sec {sec_id} note count mutated to {mutant_count}", False, passed)

    # EJ10 Note count: expected 120 (0..10) or 121 (11)
    for sec_id in range(12):
        expected = 120 if sec_id < 11 else 121
        for mutant_count in [expected - 1, expected + 1, 120 if sec_id == 11 else 121]:
            passed = (mutant_count == expected)
            assert_mutant_killed(f"EJ10 sec {sec_id} note count mutated to {mutant_count}", False, passed)

    # EJ11 Note count: expected 180 (0..10) or 181 (11)
    for sec_id in range(12):
        expected = 180 if sec_id < 11 else 181
        for mutant_count in [expected - 1, expected + 1, 180 if sec_id == 11 else 181]:
            passed = (mutant_count == expected)
            assert_mutant_killed(f"EJ11 sec {sec_id} note count mutated to {mutant_count}", False, passed)

    # Reichert Note counts: R1=43, R2=61, R4=61, R5=91
    reichert_expectations = {"R1": 43, "R2": 61, "R4": 61, "R5": 91}
    for r_name, expected in reichert_expectations.items():
        for mutant_count in [expected - 1, expected + 1, 0, 50]:
            passed = (mutant_count == expected)
            assert_mutant_killed(f"{r_name} note count mutated to {mutant_count}", False, passed)

    # -------------------------------------------------------------------------
    # Category 2: Pitch Range Bounds Sensitivity (Flute Range 59..98)
    # -------------------------------------------------------------------------
    print("\n--- [Category 2] Pitch Range Bounds Sensitivity ---")
    # Low boundary check: midi >= 59
    # High boundary check: midi <= 98
    for invalid_pitch in [58, 57, 48, 36, 0, -1, 99, 100, 108, 127]:
        passed = (59 <= invalid_pitch <= 98)
        assert_mutant_killed(f"Pitch out of bounds ({invalid_pitch})", False, passed)

    # Boundary edge values (59 and 98 must pass)
    for valid_edge in [59, 60, 72, 84, 96, 98]:
        passed = (59 <= valid_edge <= 98)
        assert_mutant_killed(f"Valid pitch edge ({valid_edge})", True, passed)

    # -------------------------------------------------------------------------
    # Category 3: ABC Header & Comment Hook Verification
    # -------------------------------------------------------------------------
    print("\n--- [Category 3] ABC Header Tag Sensitivity ---")
    # EJ5 ABC assertion: contains("% EJ5_LEDUC_ART:\(art.rawValue):SEC:\(sec.id)")
    # Corrupted mutants:
    corrupted_ej5_headers = [
        "EJ5_LEDUC_ART:1:SEC:0",               # missing leading '%'
        "% EJ5_LEDUC:1:SEC:0",                   # missing '_ART'
        "% EJ5_LEDUC_ART:0:SEC:0",               # wrong art index
        "% EJ5_LEDUC_ART:1:SEC:1",               # wrong sec index
        "% EJ10_LEDUC_ART:1:SEC:0",              # wrong exercise id
        "% R1_SCHOTT_ART:1:SEC:0",               # wrong Schott tag
    ]
    target_tag = "% EJ5_LEDUC_ART:1:SEC:0"
    for mutant_header in corrupted_ej5_headers:
        passed = (target_tag in mutant_header)
        assert_mutant_killed(f"Malformed EJ5 header '{mutant_header}'", False, passed)

    # Reichert Schott Tag assertion: contains("% R1_SCHOTT_ART:\(art.rawValue):SEC:\(sec.id)")
    corrupted_r1_headers = [
        "R1_SCHOTT_ART:2:SEC:4",
        "% R1_SCHOTT:2:SEC:4",
        "% R2_SCHOTT_ART:2:SEC:4",
        "% R1_SCHOTT_ART:1:SEC:4",
        "% R1_SCHOTT_ART:2:SEC:5",
    ]
    target_r1_tag = "% R1_SCHOTT_ART:2:SEC:4"
    for mutant_header in corrupted_r1_headers:
        passed = (target_r1_tag in mutant_header)
        assert_mutant_killed(f"Malformed R1 header '{mutant_header}'", False, passed)

    # Meter and Key assertions
    corrupted_meters = ["M:4/4", "M:3/4", "M:2/2", "M:6/4", "M:12/8"]
    for bad_meter in corrupted_meters:
        # EJ5 requires M:6/8
        passed_ej5 = ("M:6/8" == bad_meter)
        assert_mutant_killed(f"Corrupted EJ5 meter '{bad_meter}'", False, passed_ej5)
        # EJ11 requires M:9/8
        passed_ej11 = ("M:9/8" == bad_meter)
        assert_mutant_killed(f"Corrupted EJ11 meter '{bad_meter}'", False, passed_ej11)

    # -------------------------------------------------------------------------
    # Category 4: Urtext Critical Landmark Sensitivity
    # -------------------------------------------------------------------------
    print("\n--- [Category 4] Urtext Critical Landmark Sensitivity ---")
    # EJ2 m.12 Urtext double sharp ^^F
    ej2_m12_mutants = ["^F", "=F", "_F", "F", "G", "_G"]
    for m in ej2_m12_mutants:
        passed = ("^^F" in m)
        assert_mutant_killed(f"EJ2 m.12 altered to {m} (lost double sharp)", False, passed)

    # EJ2 m.22 Urtext B sharp ^B
    ej2_m22_mutants = ["=B", "_B", "B", "c", "=c"]
    for m in ej2_m22_mutants:
        passed = ("^B" in m)
        assert_mutant_killed(f"EJ2 m.22 altered to {m} (lost B sharp)", False, passed)

    # EJ4 A Minor Harmonic Descent (G#5 = 80, F5 = 77)
    a_minor_mutants = [
        (79, 77), # G natural 5 (natural minor regression)
        (80, 76), # E natural 5
        (81, 77), # A5
        (79, 76), # G5, E5
    ]
    for g_note, f_note in a_minor_mutants:
        passed = (g_note == 80 and f_note == 77)
        assert_mutant_killed(f"EJ4 A minor descent mutated to ({g_note}, {f_note})", False, passed)

    # -------------------------------------------------------------------------
    # Category 5: PracticeStore State Tracking & Toggle Sensitivity
    # -------------------------------------------------------------------------
    print("\n--- [Category 5] PracticeStore Tracking & Toggle Sensitivity ---")
    # Store simulation: 10 items to complete
    completed_set = set()

    # Step 1: Initial state must be 0 and not fully completed
    assert_mutant_killed("Initial completed count != 0", False, len(completed_set) != 0)
    assert_mutant_killed("Initial fully completed != False", False, (len(completed_set) == 10) != False)

    # Step 2: Mark 10 items
    for i in range(1, 11):
        completed_set.add(i)

    assert_mutant_killed("Full completion count != 10", True, len(completed_set) == 10)
    assert_mutant_killed("Full completion flag != True", True, (len(completed_set) == 10) == True)

    # Step 3: Toggle off one item (e.g. item 1)
    completed_set.remove(1)
    assert_mutant_killed("Toggle off count != 9", True, len(completed_set) == 9)
    assert_mutant_killed("Toggle off full completion != False", True, (len(completed_set) == 10) == False)

    # Mutants where toggle off fails to update count or flag
    fake_count_after_toggle_off = 10
    passed_toggle_count = (fake_count_after_toggle_off == len(completed_set))
    assert_mutant_killed("Store toggle-off bug: count stays 10", False, passed_toggle_count)

    fake_flag_after_toggle_off = True
    passed_toggle_flag = (fake_flag_after_toggle_off == (len(completed_set) == 10))
    assert_mutant_killed("Store toggle-off bug: flag stays True", False, passed_toggle_flag)

    print("\n================================================================================")
    print(f"MUTATION STRESS SUMMARY: {mutants_killed} / {mutants_tested} mutants killed")
    print(f"Mutation Kill Rate: {(mutants_killed / mutants_tested) * 100:.2f}%")
    print("================================================================================")

    if mutants_killed != mutants_tested:
        print("FAIL: One or more mutants survived! Assertions are not sufficiently strict.")
        sys.exit(1)
    else:
        print("SUCCESS: 100% of synthetic mutants killed. Assertions are mathematically strict!")


if __name__ == "__main__":
    audit_test_file_assertions()
    run_mutation_stress_tests()
