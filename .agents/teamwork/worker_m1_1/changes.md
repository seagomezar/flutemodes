# Changes Report — Milestone 1: Score Engine & Urtext Parity Fixes

## 1. Overview
This milestone resolves defects DEF-01, DEF-02, DEF-03, DEF-05, DEF-06, DEF-07, and DEF-08 across Web, Android, and iOS platforms. All changes maintain strict parity and byte-for-byte identity between shared templates while adhering to exclusive file ownership boundaries.

---

## 2. Modified Files & Detailed Changes

### 2.1 Web & Score Engine

#### `FluteModes/FluteModes/Resources/score_template.html` & `FluteModesAndroid/app/src/main/assets/score_template.html`
- **SHA-256 Checksum**: `201f313c6e4ab154d16b049495235f148bc8d42b62e8865a15c636fb050c6aa9` (identical on both iOS and Android).
- **DEF-01 (Schott Layout Engine)**:
  - Integrated `renderR1Schott`, `renderR2Schott`, `renderR4Schott`, and `renderR5Schott` rendering pipelines.
  - Added Urtext plate footer `"B. Schott's Söhne · 20623"` and active key badges matching the original edition.
  - Added `const EJ5_SECTIONS_DATA = EJ5_SCALES_DATA;` alias to support section boundary indexing.
- **DEF-08 (Visual Note Cursor Bridge)**:
  - Added `.highlighted-note` CSS styling (`fill: #2563eb !important; stroke: #2563eb !important; font-weight: bold;`).
  - Added `add_classes: true` to all ABCJS render options across EJ1, EJ2, EJ4, EJ5, EJ10, EJ11, Modal exercises, and Reichert R1/R2/R4/R5.
  - Implemented `clearHighlight()` removing `.highlighted-note` class across the document.
  - Implemented `highlightNote(noteIndex)` targeting active focus score containers (`r1-focus-score`, `r2-focus-score`, `r4-focus-score`, `r5-focus-score`, `ej4-focus-score`, `ej5-focus-score`, `ej10-focus-score`, `ej11-focus-score`), measure-by-measure chromatic divs for EJ1/EJ2, and `#paper` fallback with auto-scroll.

#### `build_reichert_outputs.py`
- Updated `ABC_DL_DIR` writes to output both TitleCase (`Reichert_R1_Coleccion_Completa.abc`) and lowercase backwards-compatibility aliases (`reichert_r1_completo.abc`).
- Ensured `add_classes: true` is included in all generated Schott render routines.
- Synchronized template injection to write identical content to both iOS and Android assets.

#### `docs/index.html`
- Updated Reichert download links to use canonical TitleCase filenames.
- Added direct download card and anchor for the complete 84 Modal collection (`00_Coleccion_Completa_84_Modos_EJ4.abc`).

#### `docs/downloads/abc/`
- Added `00_Coleccion_Completa_84_Modos_EJ4.abc`.
- Added lowercase aliases `reichert_r1_completo.abc`, `reichert_r2_completo.abc`, `reichert_r4_completo.abc`, and `reichert_r5_completo.abc`.

---

### 2.2 Android Platform

#### `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/model/ExerciseGenerator.kt`
- **DEF-02**: Replaced truncated/corrupted `ej2RawMeasures` with the complete 30-measure Urtext pentachord table matching Alphonse Leduc Pl. 16.588 and iOS `ExerciseGenerator.swift`. Corrected accidentals across all minor chromatic shifts including measure 12 (F# - A - C# - D# - F# - D# - C# - A).

#### `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/audio/ScoreAudioPlayer.kt`
- **DEF-03**: Corrected diminished fourth semitone in `generateChromaticPentachordBuffer`:
  `val dimFourthSemitone = if (isMinor) 4 else 5`
  `val dim = listOf(base, base + 1, base + 3, base + (if (isMinor) 4 else 5), base + 6)`
- **DEF-05**: Corrected R.5 sixteenth-triplet audio divisor:
  `val sixteenthDuration = when (exercise) { ExerciseType.R5 -> (60.0 / tempoBPM.toDouble()) / 6.0; else -> (60.0 / tempoBPM.toDouble()) / 4.0 }`
  Added R.1/R.5 staccato eighth note final duration (`sixteenthDuration * 2.0`, `isStaccato = true`).
  Added R.2/R.4 final staccato eighth note duration (`eighthDuration * 2.0`, `isStaccato = true`) and R.2 pickup sub-index alignment.
- **DEF-08**: Added `var currentNoteIndex by mutableStateOf<Int?>(null)`, tracked `lastNoteDurations = notes.map { it.duration }` in `renderNotesToPcm`, and launched highlight coroutine in `playPcmBuffer` updating `currentNoteIndex` synchronously with note playback.

#### `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/ui/ScoreWebView.kt`
- Added `highlightedNoteIndex: Int? = null` parameter.
- Added `lastRenderedAbc` caching to prevent full score re-renders during note highlighting.
- Added `LaunchedEffect(highlightedNoteIndex, isLoaded)` evaluating `highlightNote($highlightedNoteIndex);` and `clearHighlight();`.

#### `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/ui/PracticeScreen.kt`
- Updated `ScoreWebView` invocation at line 1155 to pass `highlightedNoteIndex = scorePlayer.currentNoteIndex`.

---

### 2.3 iOS Platform

#### `FluteModes/FluteModes/Audio/ScoreAudioPlayer.swift`
- **DEF-08**: Added `@Published public var currentNoteIndex: Int? = nil`.
- Implemented `scheduleHighlightUpdates(durations:)` and `cancelHighlightUpdates()` using `DispatchWorkItem` scheduled on `DispatchQueue.main.asyncAfter`.
- Captured `lastGeneratedDurations` during `synthesizePianoNotes`.
- Integrated `scheduleHighlightUpdates` into `play`, `playEJ1`, `playEJ2`, `playEJ4`, `playEJ5Type`, and `cancelHighlightUpdates()` into `stop()`.

#### `FluteModes/FluteModes/Views/ScoreWebView.swift`
- Added `public var highlightedNoteIndex: Int? = nil` parameter with default argument preserving backward compatibility.
- In `Coordinator`, added `lastRenderedAbc` and `lastHighlightedIndex` caching to avoid score redraws.
- Added `updateHighlight(_:noteIndex:)` evaluating `highlightNote(...)` and `clearHighlight()` via `evaluateJavaScript`.
- Wired `updateHighlight` inside `updateUIView`.

#### `FluteModes/FluteModes/Views/PracticeView.swift`
- Updated `ScoreWebView` call at line 39 to pass `highlightedNoteIndex: scorePlayer.currentNoteIndex`.

---

## 3. Verification & Results

1. **SHA-256 Parity**:
   `shasum -a 256 FluteModes/FluteModes/Resources/score_template.html FluteModesAndroid/app/src/main/assets/score_template.html`
   Output: `201f313c6e4ab154d16b049495235f148bc8d42b62e8865a15c636fb050c6aa9` for both.

2. **E2E Test Suite**:
   `python3 tests/run_e2e_tests.py`
   Output:
   - Total Tests Executed: 141
   - Passed: 139 (98.58%)
   - Failures: 2 (DEF-09 in M2, DEF-14 in M4)
   - Zero failures remaining for Milestone 1 (DEF-01, DEF-02, DEF-03, DEF-05, DEF-06, DEF-07, DEF-08 are all 100% verified passing).

3. **Android Unit Tests**:
   `./gradlew testDebugUnitTest` in `FluteModesAndroid/`
   Output: `BUILD SUCCESSFUL in 13s` (all 24 tasks passed).

4. **iOS App Build**:
   `xcodebuild build -project FluteModes.xcodeproj -scheme FluteModes -destination 'generic/platform=iOS' CODE_SIGNING_ALLOWED=NO`
   Output: `** BUILD SUCCEEDED **`.
