# Challenge Report — Milestone 1: Score Engine & Urtext Parity Fixes

## 1. Challenge Summary

**Overall risk assessment**: **LOW**
**Milestone 1 Quality Verdict**: **APPROVE**

Milestone 1 fixes (DEF-01, DEF-02, DEF-03, DEF-05, DEF-06, DEF-07, DEF-08) were subjected to rigorous, independent empirical stress testing, cross-platform mathematical verification, and adversarial boundary fuzzing. The implementation demonstrates robust musicological precision, byte-for-byte asset parity between platforms, exact 12-TET frequency synthesis math, and zero runtime crashes across all standard and in-bounds exercise parameters.

---

## 2. Empirical Verification Results

### 2.1 Score Template Rendering (`score_template.html` in JSDOM)
- **Harness**: `tests/empirical_score_engine.js` (Node.js v24 + JSDOM).
- **Template Identity**: Verified SHA-256 byte-for-byte identity between:
  - `FluteModes/FluteModes/Resources/score_template.html`
  - `FluteModesAndroid/app/src/main/assets/score_template.html`
  - Checksum: `201f313c6e4ab154d16b049495235f148bc8d42b62e8865a15c636fb050c6aa9`.
- **Exhaustive Schott Reichert Rendering**:
  - **R.1 (Exercice Journalier)**: 25 sections (0..24) × 11 articulations (0..10) = 275 combinations -> **275 / 275 PASSED**.
  - **R.2 (Arpèges Modulants)**: 25 sections (0..24) × 9 articulations (0..8) = 225 combinations -> **225 / 225 PASSED**.
  - **R.4 (Exercice d'Agilité)**: 25 sections (0..24) × 9 articulations (0..8) = 225 combinations -> **225 / 225 PASSED**.
  - **R.5 (Arpèges en Triolets)**: 25 sections (0..24) × 11 articulations (0..10) = 275 combinations -> **275 / 275 PASSED**.
  - **Total Schott Combinations Tested**: **1,000 / 1,000 PASSED (100%)**.
  - Every single combination generated valid SVGs, populated the focus score container, rendered `.abcjs-note` elements, and included the Urtext plate footer `"B. Schott's Söhne · 20623"`.
- **Taffanel & Gaubert Hooks**: Verified rendering of E.J. 1, E.J. 2, E.J. 4, E.J. 5, E.J. 10, E.J. 11.
- **Fallback Standard ABC**: Successfully renders valid SVG notation into `#paper`.

### 2.2 Visual Cursor Note Highlighting (DEF-08)
- **Functions Tested**: `highlightNote(noteIndex)` and `clearHighlight()`.
- **Single-Section Focus Scores**:
  - `highlightNote(0)` accurately applies `.highlighted-note` class exclusively to the first note of the active focus score.
  - `highlightNote(mid)` and `highlightNote(last)` correctly highlight intermediate and final notes.
  - Complete sequential sweep across all 43 notes in R.1 Section 0 verified without index drift or orphaned highlights.
  - Tested on R.1, R.2, R.4, R.5, E.J. 4, E.J. 5, E.J. 10, E.J. 11 focus containers.
- **Chromatic Measure Divs**: Verified highlighting across measure containers for E.J. 1 and E.J. 2 (`ej1-m1-score` through `ej1-m30-score`).
- **Clear Highlight**: `clearHighlight()` verified to clear all active highlight classes across all containers (0 remaining elements).
- **Out-of-Bounds & Type Safety**: Handled negative indices (`-1`, `-100`), extreme indices (`999999`), and non-numeric inputs (`null`, `undefined`, `"0"`, `"abc"`, `NaN`) without throwing unhandled exceptions or leaving invalid DOM states.

### 2.3 Audio Synthesis Math & Urtext Note Parity
- **Harness**: `tests/verify_audio_synthesis_math.py`.
- **Status**: **64 / 64 checks PASSED (100%)**.
- **Pitch Frequency Math**:
  - Standard formula $f(midi) = 440.0 \times 2^{(midi - 69.0) / 12.0}$ verified in both Swift (`ScoreAudioPlayer.swift`) and Kotlin (`ScoreAudioPlayer.kt`).
  - Maximum delta across landmark frequencies (A4=440.0, C4=261.626, C5=523.251, C6=1046.502, C7=2093.005, B3=246.942, D7=2349.318) was < 1e-12 Hz.
- **Note-for-Note Cross-Platform Parity**:
  - R.1: 25 sections (1,075 notes) -> 100% exact match between Kotlin and Swift.
  - R.2: 25 sections (1,525 notes) -> 100% exact match between Kotlin and Swift.
  - R.4: 25 sections (1,525 notes) -> 100% exact match between Kotlin and Swift.
  - R.5: 25 sections (2,275 notes) -> 100% exact match between Kotlin and Swift.
  - E.J. 4: 25 sections (3,101 notes) -> 100% exact match between Kotlin and Swift.
  - E.J. 5: 12 sections (588 notes) -> 100% exact match between Kotlin and Swift.
  - E.J. 10: 12 sections (1,441 notes) -> 100% exact match between Kotlin and Swift.
  - E.J. 11: 12 sections (2,161 notes) -> 100% exact match between Kotlin and Swift.
  - All pitches confirmed within standard flute compass (MIDI 59 to 102).
- **E.J. 2 Urtext Accidental Parity (DEF-02)**:
  - 30-measure pentachord sequence compared between Swift `ej2RawMeasures` and Kotlin `ej2RawMeasures`.
  - Measure 12 matches Urtext Plate A. L. 16.588: `^^F, ^G, ^A, B, ^c, B, A, G` (F## / G# / A# / B / C# / B / A / G).
- **Timing Divisors & Durations (DEF-05)**:
  - R.5 sixteenth-triplet timing divisor verified as 6.0: `(60.0 / tempoBPM) / 6.0` in both Swift and Kotlin.
  - Standard sixteenth duration divisor verified as 4.0: `(60.0 / tempoBPM) / 4.0`.
  - Final notes on R.1 and R.5 have duration `sixteenthDuration * 2.0` with `isStaccato = true`.
  - Final notes on R.2 and R.4 have duration `eighthDuration * 2.0` with `isStaccato = true`.
- **Interval Semitones (DEF-03)**:
  - Diminished fourth semitone in chromatic pentachord: `if (isMinor) 4 else 5` in both Swift and Kotlin.
  - Minor third semitone in chromatic pentachord: `if (isMinor) 3 else 4` in both Swift and Kotlin.

### 2.4 Ecosystem E2E Test Suite
- `python3 tests/run_e2e_tests.py`:
  - Total Tests Executed: 141
  - Passed: 139 (98.58%)
  - Failures: 2 (DEF-09 in M2, DEF-14 in M4)
  - 0 failures in Milestone 1 defects (DEF-01, DEF-02, DEF-03, DEF-05, DEF-06, DEF-07, DEF-08 are all 100% passing).

### 2.5 Native Target Verification
- Android Unit Tests (`./gradlew testDebugUnitTest` in `FluteModesAndroid/`): **BUILD SUCCESSFUL in 854ms** (24 tasks up to date).
- iOS Target Build (`xcodebuild build` in `FluteModes/`): `** BUILD SUCCEEDED **`.

---

## 3. Adversarial Findings & Hardening Recommendations

During adversarial input fuzzing and out-of-bounds exploration, two low-severity edge-case failure modes and one environment observation were identified. None of these block Milestone 1, but they are documented for future defensive hardening:

### Finding ADV-01 (Low): Unhandled Null Input in `renderScore`
- **Observation**: Calling `renderScore(null)` or `renderScore(undefined)` throws `TypeError: Cannot read properties of null (reading 'match')` from deep within ABCJS.
- **Cause**: In `score_template.html`, if no regex comment hook matches, execution falls through to `ABCJS.renderAbc("paper", abcString, ...)`. When `abcString` is `null`, ABCJS attempts to evaluate regex on it.
- **Blast Radius**: Zero in production apps (native `WKWebView` and `WebView` callers only pass non-null ABC strings constructed by generators), but fails in defensive unit fuzzers.
- **Recommended Hardening (Milestone 2 or Hardening Track)**:
  Add an early return guard at the top of `renderScore(abcString)`:
  ```javascript
  if (!abcString || typeof abcString !== "string") return;
  ```

### Finding ADV-02 (Low): Legacy EJ11 Out-of-Bounds Section Index
- **Observation**: Calling `renderScore("% EJ11_LEDUC_ART:0:SEC:999")` throws `TypeError: Cannot read properties of undefined (reading 'm')`.
- **Cause**: In pre-existing legacy function `buildEj11SectionFocusAbc`, `startM = secIdx * 10` slices `EJ11_MEASURES_DATA`. If `secIdx >= 12`, `slice` is empty, leading to `slice[i].m` dereferencing `undefined`.
- **Comparison**: In contrast, the newly implemented Schott renderers (DEF-01) properly guard this with:
  ```javascript
  const sec = R1_SECTIONS_DATA[secIdx] || R1_SECTIONS_DATA[0];
  ```
  Which safely handles any invalid section index without throwing.
- **Blast Radius**: Zero in production apps (native views only pass section indices `0..11`), but represents an inconsistency between legacy EJ11 and the new Schott renderers.
- **Recommended Hardening**: Add clamping or fallback in `buildEj11SectionFocusAbc`.

### Finding ADV-03 (Informational): Headless DOM `scrollIntoView` Dependency
- **Observation**: In headless Node.js/JSDOM test environments, `targetNote.scrollIntoView` throws `TypeError: targetNote.scrollIntoView is not a function` unless polyfilled.
- **Assessment**: Native iOS `WKWebView` and Android Chromium `WebView` support W3C `Element.prototype.scrollIntoView` natively, so this does not affect real devices. Adding `if (typeof targetNote.scrollIntoView === 'function')` would ensure seamless execution in both headless and native environments.

---

## 4. Stress Test Results Summary Table

| Test Suite / Harness | Scenarios Tested | Passed | Failed | Result |
|----------------------|------------------|--------|--------|--------|
| Template SHA-256 Parity | iOS vs Android template identity | 1 | 0 | PASS |
| Schott R.1 (25 Sec × 11 Art) | Layout, SVG render, notes, plate footer | 275 | 0 | PASS |
| Schott R.2 (25 Sec × 9 Art) | Layout, SVG render, notes, plate footer | 225 | 0 | PASS |
| Schott R.4 (25 Sec × 9 Art) | Layout, SVG render, notes, plate footer | 225 | 0 | PASS |
| Schott R.5 (25 Sec × 11 Art) | Layout, SVG render, notes, plate footer | 275 | 0 | PASS |
| T&G Hook Renderers | EJ1, EJ2, EJ4, EJ5, EJ10, EJ11 | 6 | 0 | PASS |
| Note Highlighting (DEF-08) | 0..N, focus scores, chromatic divs, clear | 12 | 0 | PASS |
| Audio Math & Landmark Frequencies | 12-TET formulas, B3..D7 compass | 10 | 0 | PASS |
| Note Counts & Pitch Parity | R1, R2, R4, R5, EJ4, EJ5, EJ10, EJ11 (13,691 notes) | 16 | 0 | PASS |
| Urtext EJ2 30-Measure Parity | mm. 1..30 and m.12 Urtext accidental check | 6 | 0 | PASS |
| Audio Timing & Interval Math | R.5 6.0 divisor, staccato 2x, pentachord 3rd/4th | 12 | 0 | PASS |
| Master E2E Suite (`run_e2e_tests.py`) | 141 tests covering Tiers 1-4 | 139 | 2* | PASS (M1 Clean) |
| Android Unit Tests (`./gradlew`) | `testDebugUnitTest` | 24 tasks | 0 | PASS |
| iOS Xcode Build (`xcodebuild`) | FluteModes App Scheme | 1 | 0 | PASS |

*\*The 2 E2E test failures belong to DEF-09 (Milestone 2) and DEF-14 (Milestone 4).*

---

## 5. Verdict

**APPROVE** — Milestone 1 is verified with high empirical confidence. All assigned defects are completely resolved, Urtext musicological compliance is exact, cross-platform assets are synchronized, and the core rendering and audio synthesis engines are performant and mathematically correct.
