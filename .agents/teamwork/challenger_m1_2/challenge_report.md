# Empirical Challenge Report — Milestone 1 (Score Engine & Urtext Parity Fixes)

**Agent**: `challenger_m1_2` (Empirical Challenger)  
**Date**: 2026-10-11T15:38:00Z  
**Scope**: Taffanel & Gaubert E.J. 2 Urtext Accidental Corrections, Web Download Integrity, Score Template Parity, and Full E2E Test Suite.

---

## 1. Executive Summary

- **Overall Risk Assessment**: **LOW**
- **Verdict**: **APPROVE**
- **Empirical Validation Summary**:
  - Android `ExerciseGenerator.kt` `ej2RawMeasures` was compared note-for-note, beat-for-beat, and measure-for-measure against iOS `ExerciseGenerator.swift` and the Urtext edition (Alphonse Leduc, Paris, Plate A. L. 16.588, pages 8–9).
  - Exact 100% byte-for-byte and note-for-note parity is confirmed across all 30 measures (960 notes total).
  - All corrupted major-third notes in transition measures mm. 4, 8, 14, 18, 22, 24, 28 have been genuinely corrected to their Urtext minor-third naturals (`=G`, `=A`, `=c`, `=d`, `=e`, `=f`, `=g`), restoring harmonic fidelity without any accidental leakage across barlines.
  - All 49 download links in `docs/index.html` (and all 106 local links across all 13 HTML files in `docs/`) resolve to existing, valid, non-empty, and readable files on disk.
  - Byte-level SHA-256 parity between iOS (`FluteModes/FluteModes/Resources/score_template.html`) and Android (`FluteModesAndroid/app/src/main/assets/score_template.html`) is 100% identical (`201f313c6e4ab154d16b049495235f148bc8d42b62e8865a15c636fb050c6aa9`, 723,634 bytes).
  - `python3 tests/run_e2e_tests.py` ran 141 tests: 139 passed (98.58%), 0 errors, and exactly 0 failures across all Milestone 1 defects (DEF-01, DEF-02, DEF-03, DEF-05, DEF-06, DEF-07, DEF-08). The only 2 failing tests belong strictly to subsequent milestones (DEF-09 in M2, DEF-14 in M4).
  - Android unit tests (`./gradlew testDebugUnitTest`) pass 100% (24 tasks executed).
  - iOS target compilation (`xcodebuild build -project FluteModes/FluteModes.xcodeproj -scheme FluteModes`) succeeded with zero errors (`** BUILD SUCCEEDED **`).

---

## 2. Adversarial Challenges & Empirical Verifications

### Challenge 1: Urtext Note-for-Note Parity in E.J. 2 (Alphonse Leduc Plate 16.588)
- **Assumption Challenged**: That Android `ExerciseGenerator.kt` accurately reproduces the minor pentachord modulations of Taffanel & Gaubert E.J. 2 without retaining major-third corruptions or introducing accidental leaks.
- **Adversarial Test**:
  1. Parsed all 30 measures (4 beats per measure, 8 notes per beat = 32 notes/measure) from `FluteModesAndroid/.../ExerciseGenerator.kt` and `FluteModes/.../ExerciseGenerator.swift`.
  2. Compared each measure note-for-note against git commit `c56db36` (v1.5.0 baseline) and against `docs/downloads/abc/00_Taffanel_EJ2_Original_AL16588.abc`.
  3. Verified every pitch, stem directive, 8va mark, and measure delimiter.
- **Empirical Findings**:
  - **Swift vs Android Parity**: 0 differences across all 30 measures.
  - **Correction of Corrupted Notes in Target Measures**:
    - **Measure 4** (vii° -> E minor): Beat 1 Note 4 corrected from `^G` (G# = major 3rd) to `=G` (G natural = minor 3rd).
    - **Measure 8** (vii° -> F# minor): Beat 1 Note 4 corrected from `^A` (A# = major 3rd) to `=A` (A natural = minor 3rd).
    - **Measure 14** (vii° -> A minor): Beat 1 Note 3 corrected from `B` to `=B`; Note 4 corrected from `^c` (C# = major 3rd) to `=c` (C natural = minor 3rd).
    - **Measure 18** (vii° -> B minor): Beat 1 Note 4 corrected from `^d` (D# = major 3rd) to `=d` (D natural = minor 3rd).
    - **Measure 22** (vii° -> C# minor): Beat 1 Note 4 corrected from `^e` (E# = major 3rd) to `=e` (E natural = minor 3rd); Note 1 preserves enharmonic `^B` (B# = C natural sounding).
    - **Measure 24** (vii° -> D minor): Beat 1 Note 3 corrected from `e` to `=e`; Note 4 corrected from `^f` (F# = major 3rd) to `=f` (F natural = minor 3rd).
    - **Measure 28** (vii° -> E minor 8va): Beat 1 Note 4 corrected from `^g` (G# = major 3rd) to `=g` (G natural = minor 3rd).
  - **Accidental Leak & Scoping Check**:
    - All 15 chromatic pairs maintain strict barlines (`|` / `:|`).
    - Every chromatic shift is explicitly prefixed with its accidental in Beat 1.
    - Beats 2–4 repeat the pitch class without accidental restatement, conforming to standard ABC and Urtext conventions.
    - No accidental leaks occur across barlines or into adjacent measures.
- **Status**: **PASS** (100% compliant with Alphonse Leduc Pl. 16.588).

---

### Challenge 2: Web Download Integrity and Link Resolution
- **Assumption Challenged**: That all download URLs in `docs/index.html` point to physical files that exist, are readable, non-empty, and match canonical naming.
- **Adversarial Test**:
  1. Extracted all 90 `href` attributes and 3 `src` attributes from `docs/index.html`.
  2. Identified all 49 download URLs (`downloads/...`).
  3. Resolved every relative URL against `docs/` and verified file existence, file type, file size > 0, and read access.
  4. Expanded the audit to all 13 HTML files in `docs/` (checking 106 local links).
- **Empirical Findings**:
  - Download links checked: **49 of 49 OK**.
  - General page links checked: **33 of 33 OK**.
  - Local scripts/assets checked: **3 of 3 OK**.
  - Broken links found: **0**.
  - Full collection ABC download `docs/downloads/abc/00_Coleccion_Completa_84_Modos_EJ4.abc` exists (32,013 bytes) and contains all 84 modal exercises.
  - Both TitleCase and lowercase aliases exist for Reichert R1, R2, R4, R5 ABC downloads.
- **Status**: **PASS**.

---

### Challenge 3: Score Template SHA-256 Parity (iOS vs Android)
- **Assumption Challenged**: That `score_template.html` in iOS and Android are identical byte-for-byte, ensuring uniform notation and visual playback across both mobile platforms.
- **Adversarial Test**:
  1. Computed SHA-256 hashes of:
     - `FluteModes/FluteModes/Resources/score_template.html`
     - `FluteModesAndroid/app/src/main/assets/score_template.html`
  2. Byte-by-byte direct comparison: `ios_bytes == android_bytes`.
- **Empirical Findings**:
  - iOS SHA-256: `201f313c6e4ab154d16b049495235f148bc8d42b62e8865a15c636fb050c6aa9` (723,634 bytes)
  - Android SHA-256: `201f313c6e4ab154d16b049495235f148bc8d42b62e8865a15c636fb050c6aa9` (723,634 bytes)
  - Exact match: `True`.
  - Both templates include:
    - Schott rendering routines (`renderR1Schott`, `renderR2Schott`, `renderR4Schott`, `renderR5Schott`).
    - Schott plate notice `"B. Schott's Söhne · 20623"`.
    - Note highlighting functions `highlightNote(noteIndex)` and `clearHighlight()`.
    - CSS `.highlighted-note` definition.
    - `add_classes: true` in all 32 `ABCJS.renderAbc` configurations.
- **Status**: **PASS**.

---

### Challenge 4: Audio Synthesizer Parity (DEF-03 & DEF-05)
- **Assumption Challenged**: That diminished pentachord semitones and Reichert R.5 sixteenth-triplet tempos are correctly synthesized on Android and iOS.
- **Adversarial Test**:
  - Inspected `ScoreAudioPlayer.kt` and `ScoreAudioPlayer.swift`.
  - Verified diminished fourth semitone formula: `val dimFourthSemitone = if (isMinor) 4 else 5`.
  - Verified R.5 tempo divisor: `sixteenthDuration = (60.0 / tempoBPM.toDouble()) / 6.0` (sixteenth triplet) vs `4.0` (standard sixteenth).
  - Verified final staccato notes on R.1, R.2, R.4, R.5.
- **Empirical Findings**:
  - Android `ScoreAudioPlayer.kt` line 444 properly uses `base + (if (isMinor) 4 else 5)` matching Swift `let dimFourthSemitone = isMinor ? 4 : 5`.
  - Android `ScoreAudioPlayer.kt` lines 270–273 use divisor `6.0` for `ExerciseType.R5`, matching Swift `(60.0 / Double(tempoBPM)) / 6.0`.
  - Both platforms accurately double the final staccato eighth duration (`duration * 2.0`, `isStaccato = true`).
- **Status**: **PASS**.

---

### Challenge 5: Full E2E Test Suite Execution
- **Command Executed**: `python3 tests/run_e2e_tests.py`
- **Output Metrics**:
  - Total Tests: 141
  - Passed: 139 (98.58%)
  - Failed: 2
  - Errors: 0
  - Execution Time: 0.27s
- **Defect Breakdown Analysis**:
  - DEF-01 (Schott Score Engine): **0 failing** (All tests pass)
  - DEF-02 (Android EJ2 Accidentals): **0 failing** (All tests pass)
  - DEF-03 (Android Audio Diminished Semitone): **0 failing** (All tests pass)
  - DEF-05 (Android Audio R5 Triplet Divisor): **0 failing** (All tests pass)
  - DEF-06 (Web Portal Links): **0 failing** (All tests pass)
  - DEF-07 (Colección Completa 84 Modos ABC): **0 failing** (All tests pass)
  - DEF-08 (Visual Note Cursor Bridge): **0 failing** (All tests pass)
  - Out of Scope Failures:
    - `test_c14_android_reichert_navigation_routes` -> DEF-09 (Assigned to Milestone 2).
    - `test_s10_multiplatform_version_consistency_target` -> DEF-14 (Assigned to Milestone 4).
- **Status**: **PASS**.

---

## 3. Stress Test Results Summary

| # | Test Scenario | Expected Behavior | Actual Behavior | Result |
|---|---------------|-------------------|-----------------|--------|
| 1 | Android vs iOS EJ2 note comparison | 0 differences across 30 measures | 0 differences (30/30 identical) | **PASS** |
| 2 | EJ2 m.4, 8, 14, 18, 22, 24, 28 accidental fix | Minor-third naturals (`=G`, `=A`, `=c`, `=d`, `=e`, `=f`, `=g`) | All 7 measures use Urtext minor-third naturals | **PASS** |
| 3 | EJ2 accidental leakage test | No accidental carryover across barlines | Every measure has explicit accidentals in Beat 1; 0 leaks | **PASS** |
| 4 | Web downloads existence | All 49 download links in `docs/index.html` resolve | 49 of 49 files exist, non-empty, and readable | **PASS** |
| 5 | Cross-HTML docs links | All 106 local links across 13 HTML files resolve | 106 of 106 links resolve | **PASS** |
| 6 | `score_template.html` SHA-256 parity | Exact byte match between iOS and Android | Byte parity match `True`, SHA-256 `201f313c...` | **PASS** |
| 7 | Android audio diminished semitone | `base + (if (isMinor) 4 else 5)` | Present in `ScoreAudioPlayer.kt:444` | **PASS** |
| 8 | Android audio R.5 tempo divisor | `60.0 / tempoBPM / 6.0` | Present in `ScoreAudioPlayer.kt:272` | **PASS** |
| 9 | E2E suite (`run_e2e_tests.py`) | 0 failures in M1 scope | 139 passed, 0 failures in M1 defects | **PASS** |
| 10 | Android unit tests | Gradle build and test pass | `BUILD SUCCESSFUL in 15s` (24/24 tasks) | **PASS** |
| 11 | iOS project build | Xcode build succeeds | `** BUILD SUCCEEDED **` | **PASS** |

---

## 4. Unchallenged Areas

- **DEF-09 (Android Reichert Route Navigation & Dialogs)**: Out of scope for Milestone 1; planned for Milestone 2.
- **DEF-14 (Version Bump to v1.5.1)**: Out of scope for Milestone 1; planned for Milestone 4.

---

## 5. Final Recommendation

All Milestone 1 criteria have been empirically challenged, independently reproduced, and fully verified. The work product demonstrates robust Urtext fidelity and multiplatform parity. Milestone 1 is **APPROVED**.
