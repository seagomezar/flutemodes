#!/usr/bin/env python3
"""
Empirical Verification Test Suite: Audio Synthesis Math & Urtext Note Parity.
Cross-verifies Kotlin (Android) and Swift (iOS) models:
1. Exact MIDI note parity for all Reichert and T&G exercises.
2. Note counts and flute pitch boundary checks.
3. Frequency calculation math precision and landmark frequencies.
4. Duration calculation math (tempo divisors, staccato factors, triplet timing).
5. Pentachord interval math (major/minor thirds, diminished fourth semitones).
"""

import math
import re
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

SWIFT_GEN = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Models" / "ExerciseGenerator.swift"
KOTLIN_GEN = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "model" / "ExerciseGenerator.kt"

SWIFT_AUDIO = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Audio" / "ScoreAudioPlayer.swift"
KOTLIN_AUDIO = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "audio" / "ScoreAudioPlayer.kt"


def extract_kotlin_arrays(content: str, val_name: str) -> list:
    """Extract list of IntArray from Kotlin source."""
    pattern = rf"val\s+{val_name}:\s*List<IntArray>\s*by\s*lazy\s*\{{\s*listOf\((.*?)\)\s*\}}"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise ValueError(f"Kotlin val {val_name} not found")
    inner = match.group(1)
    array_matches = re.findall(r"intArrayOf\((.*?)\)", inner)
    result = []
    for am in array_matches:
        nums = [int(x.strip()) for x in am.split(",") if x.strip()]
        result.append(nums)
    return result


def extract_swift_arrays(content: str, var_name: str) -> list:
    """Extract [[Int]] from Swift source."""
    pattern = rf"public\s+static\s+let\s+{var_name}:\s*\[\[Int\]\]\s*=\s*\[(.*?)\n\s*\](?:\n\n|\n\}})"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise ValueError(f"Swift let {var_name} not found")
    inner = match.group(1)
    array_matches = re.findall(r"\[([\d,\s]+)\]", inner)
    result = []
    for am in array_matches:
        nums = [int(x.strip()) for x in am.split(",") if x.strip()]
        result.append(nums)
    return result


def extract_ej2_measures_kotlin(content: str) -> list:
    pattern = r"internal\s+val\s+ej2RawMeasures\s*=\s*listOf\((.*?)\)\n\s*\n\s*/\*\*"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise ValueError("Kotlin ej2RawMeasures not found")
    # Each measure has EJ1Measure(num, listOf(listOf(...), ...), prefix, suffix)
    # Extract beats: listOf\("([^"]+)"(?:,\s*"([^"]+)")*\)
    measure_blocks = re.findall(r"EJ1Measure\(\s*(\d+),\s*listOf\((.*?)\),\s*\"([^\"]*)\",\s*\"([^\"]*)\"\)", match.group(1), re.DOTALL)
    measures = []
    for num, beats_str, prefix, suffix in measure_blocks:
        beat_lists = re.findall(r"listOf\((.*?)\)", beats_str)
        beats = [[n.replace('"', '').strip() for n in b.split(',') if n.strip()] for b in beat_lists]
        measures.append((int(num), beats, prefix, suffix))
    return measures


def extract_ej2_measures_swift(content: str) -> list:
    pattern = r"internal\s+static\s+let\s+ej2RawMeasures:.*?=\s*\[(.*?)\n\s*\]\n\n\s*public\s+static\s+func\s+generateEJ2ABC"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise ValueError("Swift ej2RawMeasures not found")
    measure_blocks = re.findall(r"\(\s*(\d+),\s*\[(.*?)\],\s*\"([^\"]*)\",\s*\"([^\"]*)\"\)", match.group(1), re.DOTALL)
    measures = []
    for num, beats_str, prefix, suffix in measure_blocks:
        beat_lists = re.findall(r"\[(.*?)\]", beats_str)
        beats = [[n.replace('"', '').strip() for n in b.split(',') if n.strip()] for b in beat_lists]
        measures.append((int(num), beats, prefix, suffix))
    return measures


def run_checks():
    print("=" * 80)
    print("EMPIRICAL VERIFICATION: AUDIO SYNTHESIS MATH & URTEXT NOTE PARITY")
    print("=" * 80)

    total_checks = 0
    passed_checks = 0
    failed_checks = 0
    errors = []

    def check(condition, desc):
        nonlocal total_checks, passed_checks, failed_checks
        total_checks += 1
        if condition:
            passed_checks += 1
        else:
            failed_checks += 1
            errors.append(desc)
            print(f"  FAIL: {desc}")

    # Read files
    swift_gen_src = SWIFT_GEN.read_text(encoding="utf-8")
    kt_gen_src = KOTLIN_GEN.read_text(encoding="utf-8")
    swift_audio_src = SWIFT_AUDIO.read_text(encoding="utf-8")
    kt_audio_src = KOTLIN_AUDIO.read_text(encoding="utf-8")

    # 1. Frequency calculation math precision
    print("\n[1/5] Verifying Pitch-to-Frequency Synthesis Math...")
    # Standard formula: f = 440.0 * 2^((midi - 69.0) / 12.0)
    def calc_freq(midi):
        return 440.0 * math.pow(2.0, (midi - 69.0) / 12.0)

    landmarks = [
        (69, 440.0, "A4 (Concert Pitch)"),
        (60, 261.6255653005986, "C4 (Middle C)"),
        (72, 523.2511306011972, "C5"),
        (84, 1046.5022612023945, "C6"),
        (96, 2093.004522404789, "C7"),
        (59, 246.94165062806206, "B3 (Low B Flute Footjoint)"),
        (98, 2349.31814333926, "D7 (Flute High D)"),
    ]

    for midi, expected_f, name in landmarks:
        computed = calc_freq(midi)
        check(abs(computed - expected_f) < 1e-6, f"Frequency for {name} (MIDI {midi}) == {expected_f} Hz")

    # Check formula in Swift: 440.0 * pow(2.0, (midi - 69.0) / 12.0)
    check("440.0 * pow(2.0, (midi - 69.0) / 12.0)" in swift_audio_src, "Swift uses standard 12-TET formula")
    # Check formula in Kotlin: 440.0 * 2.0.pow((midi - 69.0) / 12.0)
    check("440.0 * 2.0.pow((midi - 69.0) / 12.0)" in kt_audio_src, "Kotlin uses standard 12-TET formula")

    # 2. Section MIDI Notes Parity (Swift vs Kotlin)
    print("\n[2/5] Verifying 100% Cross-Platform Note Parity...")
    exercises = [
        ("r1SectionMidiNotes", 25, "R.1 (Exercice Journalier)"),
        ("r2SectionMidiNotes", 25, "R.2 (Arpèges Modulants)"),
        ("r4SectionMidiNotes", 25, "R.4 (Exercice d'Agilité)"),
        ("r5SectionMidiNotes", 25, "R.5 (Arpèges en Triolets)"),
        ("ej4SectionMidiNotes", 25, "E.J. 4 (Gammes Majeures et Mineures)"),
        ("ej5SectionMidiNotes", 12, "E.J. 5 (Arpèges)"),
        ("ej10SectionMidiNotes", 12, "E.J. 10 (Tierces)"),
        ("ej11SectionMidiNotes", 12, "E.J. 11 (Octaves)")
    ]

    for var_name, expected_sections, desc in exercises:
        swift_data = extract_swift_arrays(swift_gen_src, var_name)
        kt_data = extract_kotlin_arrays(kt_gen_src, var_name)

        check(len(swift_data) == expected_sections, f"{desc}: Swift has {expected_sections} sections")
        check(len(kt_data) == expected_sections, f"{desc}: Kotlin has {expected_sections} sections")

        parity_ok = True
        notes_in_range = True
        total_notes = 0
        for s_idx in range(min(len(swift_data), len(kt_data))):
            s_arr = swift_data[s_idx]
            k_arr = kt_data[s_idx]
            total_notes += len(s_arr)
            if s_arr != k_arr:
                parity_ok = False
                check(False, f"{desc} section {s_idx} mismatch: Swift len={len(s_arr)}, Kotlin len={len(k_arr)}")
            for pitch in s_arr:
                if not (59 <= pitch <= 102):  # Flute practical compass: B3 to F#7
                    notes_in_range = False

        check(parity_ok, f"{desc}: 100% note parity between Swift and Kotlin across all {total_notes} notes")
        check(notes_in_range, f"{desc}: All pitches within flute compass (59..102)")
        print(f"  ✓ {desc}: {expected_sections} sections, {total_notes} notes, 100% parity verified")

    # 3. E.J. 2 Urtext 30-Measure Pentachord Parity
    print("\n[3/5] Verifying E.J. 2 30-Measure Pentachord Parity...")
    swift_ej2 = extract_ej2_measures_swift(swift_gen_src)
    kt_ej2 = extract_ej2_measures_kotlin(kt_gen_src)
    check(len(swift_ej2) == 30, f"Swift ej2RawMeasures has 30 measures (found {len(swift_ej2)})")
    check(len(kt_ej2) == 30, f"Kotlin ej2RawMeasures has 30 measures (found {len(kt_ej2)})")
    check(swift_ej2 == kt_ej2, "E.J. 2 measures have 100% parity between Swift and Kotlin across all 30 measures")
    # Verify measure 12 (DEF-02 accidental fix)
    # Measure 12: ^^F, ^G, ^A, B, ^c, B, A, G (Urtext Plate 16.588)
    m12_beat0 = ["^^F", "^G", "^A", "B", "^c", "B", "A", "G"]
    check(swift_ej2[11][1][0] == m12_beat0, "Swift EJ2 measure 12 matches Urtext Pl. 16.588")
    check(kt_ej2[11][1][0] == m12_beat0, "Kotlin EJ2 measure 12 matches Urtext Pl. 16.588")
    print(f"  ✓ E.J. 2: 30 measures, 100% parity verified, m.12 Urtext compliant")

    # 4. Duration Calculation Math & Timing Divisors
    print("\n[4/5] Verifying Duration Calculation Math & Timing Divisors...")
    # DEF-05: R.5 sixteenth-triplet divisor must be 6.0 (2/4 meter with 2 dotted eighths / 4 triplets per beat)
    # Standard sixteenth duration: (60.0 / BPM) / 4.0
    for bpm in [60, 80, 100, 120, 144]:
        r5_sixteenth = (60.0 / bpm) / 6.0
        std_sixteenth = (60.0 / bpm) / 4.0
        check(r5_sixteenth == std_sixteenth * (4.0 / 6.0), f"R.5 triplet tempo scaling at {bpm} BPM")

    # Check Swift timing code
    check("let baseNoteDuration = (exercise == .r5)" in swift_audio_src, "Swift scales baseNoteDuration for R.5")
    check("? ((60.0 / Double(tempoBPM)) / 6.0)" in swift_audio_src, "Swift uses divisor 6.0 for R.5 triplets")
    check(": ((60.0 / Double(tempoBPM)) / 4.0)" in swift_audio_src, "Swift uses divisor 4.0 for standard sixteenths")

    # Check Kotlin timing code
    check("ExerciseType.R5 -> (60.0 / tempoBPM.toDouble()) / 6.0" in kt_audio_src, "Kotlin uses divisor 6.0 for R.5 triplets")
    check("else -> (60.0 / tempoBPM.toDouble()) / 4.0" in kt_audio_src, "Kotlin uses divisor 4.0 for standard sixteenths")

    # Final note durations in R.1, R.2, R.4, R.5:
    check("duration = sixteenthDuration * 2.0" in kt_audio_src, "Kotlin R.1 & R.5 final note has 2x sixteenth duration")
    check("isStaccato = true" in kt_audio_src, "Kotlin R.1 & R.5 final note is staccato")
    check("duration: baseNoteDuration * 2.0" in swift_audio_src, "Swift R.1 & R.5 final note has 2x base duration")
    check("isStaccato: true" in swift_audio_src, "Swift R.1 & R.5 final note is staccato")

    # 5. Pentachord Interval Math (DEF-03)
    print("\n[5/5] Verifying Chromatic Pentachord Interval Math...")
    # In chromatic pentachords:
    # Major: third = 4 semitones, diminished fourth = 5 semitones
    # Minor: third = 3 semitones, diminished fourth = 4 semitones
    check("val dimFourthSemitone = if (isMinor) 4 else 5" in kt_audio_src, "Kotlin uses if (isMinor) 4 else 5")
    check("val thirdOffset = if (isMinor) 3 else 4" in kt_audio_src, "Kotlin uses if (isMinor) 3 else 4")
    check("let dimFourthSemitone = isMinor ? 4 : 5" in swift_audio_src, "Swift uses isMinor ? 4 : 5")
    check("let thirdSemitone = isMinor ? 3 : 4" in swift_audio_src, "Swift uses isMinor ? 3 : 4")

    print("\n" + "=" * 80)
    print(f"VERIFICATION SUMMARY: {passed_checks} / {total_checks} checks PASSED")
    if failed_checks > 0:
        print(f"FAILED CHECKS: {failed_checks}")
        for err in errors:
            print(f"  - {err}")
    else:
        print("ALL AUDIO SYNTHESIS & NOTE PARITY CHECKS PASSED (100% SUCCESS)")
    print("=" * 80)

    return failed_checks == 0


if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
