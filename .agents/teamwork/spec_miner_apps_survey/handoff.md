# Handoff Report: FluteModes Architectural & Features Survey

**Agent**: `spec_miner_apps_survey`  
**Handoff Type**: Hard (Task Complete)  
**Recipient**: Parent Orchestrator (`2c224607-5456-4eac-ad55-0172dee3d36d`)  
**Date**: 2026-10-11  

---

## 1. Observation

### Source Code Paths & Files Inspected
1. **iOS Target (`FluteModes/`)**:
   - `FluteModesApp.swift`, `ContentView.swift`, `PracticeViewModel.swift`, `ScoreWebView.swift`, `AppAudioEngine.swift`, `ScoreAudioPlayer.swift`, `MetronomeEngine.swift`, `LocalizationManager.swift`, `Models/PracticeStore.swift`, `Models/ArticulationPattern.swift`, `FluteModesTests/FluteModesTests.swift`.
   - `score_template.html` at `FluteModes/FluteModes/Resources/score_template.html`.
2. **Android Target (`FluteModesAndroid/`)**:
   - `MainActivity.kt`, `HomeScreen.kt`, `PracticeScreen.kt`, `ScoreWebView.kt`, `ScoreAudioPlayer.kt`, `MetronomeEngine.kt`, `LocalizationManager.kt`, `ArticulationPattern.kt`.
   - `score_template.html` at `app/src/main/assets/score_template.html`.
3. **Web Portal (`docs/`)**:
   - `index.html`, `modes_data.js`, `ej1.html` .. `ej11.html`, `r1.html` .. `r5.html`.
   - Download assets in `docs/downloads/abc/`, `docs/downloads/pdf/`, `docs/downloads/mp3/`.

### Tool Commands & Direct Output Results
1. **Asset Parity**:
   - SHA-256 comparison between `FluteModes/FluteModes/Resources/score_template.html` and `FluteModesAndroid/app/src/main/assets/score_template.html`:
     `748fa33f1c5a70ae4f6b2803b9fb7d27e7f62e84ceb025f12a9e32ffb18db2c2` (100% byte-for-byte identical).
2. **MIDI Note Parity**:
   - Checked all 8 MIDI collections (`ej4`, `ej5`, `ej10`, `ej11`, `r1`, `r2`, `r4`, `r5`) across Swift and Kotlin: 100% identical note counts and MIDI numbers.
3. **Localization Parity**:
   - Both `LocalizationManager.swift` and `LocalizationManager.kt` define 163 base dictionary keys with 0 key discrepancies and 0 empty strings.
   - However, `PracticeScreen.kt` queries 16 keys via `loc.t(...)` that do not exist in `LocalizationManager.kt` (`ej5_milestone_title`, `ej5_milestone_msg`, `ej5_restart_round`, `ej5_go_to_ej10`, `ej10_milestone_title`, `ej10_milestone_msg`, `ej10_restart_round`, `ej10_go_to_ej11`, `ej11_milestone_title`, `ej11_milestone_msg`, `ej11_restart_round`, `ej5_ten_arts_completed`, `ej10_ten_arts_completed`, `ej11_ten_arts_completed`, `ej4_next_section`, `ej5_next_section`).
   - `ArticulationPattern.kt:49` hardcodes `MODOS -> "84 Modos"` without English localization.
4. **JavaScript Runtime Defect in `score_template.html`**:
   - Lines 922–941 in `score_template.html`:
     ```javascript
     if (abcString.includes('% R1_SCHOTT_ART')) { renderR1Schott(cleanAbc); return; }
     if (abcString.includes('% R2_SCHOTT_ART')) { renderR2Schott(cleanAbc); return; }
     if (abcString.includes('% R4_SCHOTT_ART')) { renderR4Schott(cleanAbc); return; }
     if (abcString.includes('% R5_SCHOTT_ART')) { renderR5Schott(cleanAbc); return; }
     ```
     Neither `renderR1Schott`, `renderR2Schott`, `renderR4Schott`, nor `renderR5Schott` is defined in `score_template.html`.
   - The authoritative reference implementations are located in `docs/r1.html`, `docs/r2.html`, `docs/r4.html`, and `docs/r5.html`.
5. **Absence of Visual Cursor Bridge**:
   - Grep search for `highlightNote` across the repository found 0 occurrences in `score_template.html`, iOS, or Android.
6. **Android Navigation & Completion Defect**:
   - `MainActivity.kt`: `Screen.Practice` route ignores `sectionIndex` and `articulationId` for Reichert exercises.
   - `PracticeScreen.kt:2167–2171`: When completing a Reichert exercise round, code sets `showEJ11CompletionDialog = true`.
7. **Audio Timing Discrepancy**:
   - In `ScoreAudioPlayer.kt:118`: R.5 duration is `(60.0 / tempo) / 4.0` (quarter note sixteenths).
   - In `ScoreAudioPlayer.swift:125`: R.5 duration is `(60.0 / tempo) / 6.0` (sixteenth triplets).
8. **Web Portal Link Discrepancy**:
   - `docs/index.html` links to `downloads/abc/reichert_r{1,2,4,5}_completo.abc`, but disk files are `docs/downloads/abc/Reichert_R{1,2,4,5}_Coleccion_Completa.abc`.
9. **Build & Test Executions**:
   - Android `./gradlew testDebugUnitTest`: **Passed** (24/24 unit tests passed, exit code 0).
   - iOS main target build `xcodebuild build -project FluteModes.xcodeproj -scheme FluteModes -destination "id=94204FC1-C90B-4E72-88EE-A197D4B52046"`: **SUCCEEDED** (exit code 0).
   - iOS unit test `xcodebuild test`: **FAILED** (exit code 65) due to outdated API calls in `FluteModesTests.swift` (`sec.shortTitle` vs `shortName`, missing convenience methods on `PracticeStore` for `markR1Completed`, etc.).

---

## 2. Logic Chain

1. **Step 1: Multiplatform Codebase Audit**
   - By examining `FluteModes/`, `FluteModesAndroid/`, and `docs/`, we verified that all 11 modules (Modos, E.J. 1, 2, 4, 5, 10, 11, R. 1, 2, 4, 5) share identical musical data (notes, scales, keys).
2. **Step 2: Score Template Verification**
   - Both mobile apps load an identical `score_template.html`.
   - When any Reichert exercise (R. 1, 2, 4, 5) is requested with Schott articulations, the generator injects `% R{N}_SCHOTT_ART`.
   - Because `renderR{N}Schott` is referenced but undefined in `score_template.html`, the browser engine throws `ReferenceError`, completely preventing score display.
   - The authoritative reference implementation is in `docs/r{1,2,4,5}.html`, making porting direct and unambiguous.
3. **Step 3: Visual Cursor & Highlight Bridge**
   - Feature R2 of the specification requires synchronized note-head highlighting during audio playback.
   - Neither the web template nor the native audio engines have any tracking hooks.
   - Implementing this requires:
     - Adding `highlightNote(index)` and `clearHighlight()` in `score_template.html`.
     - Firing callbacks during audio playback in `ScoreAudioPlayer.swift` and `ScoreAudioPlayer.kt`.
4. **Step 4: Android Defect Root Cause**
   - In `PracticeScreen.kt`, multiple UI dialogs and navigation buttons reference keys that were never added to `LocalizationManager.kt`.
   - For Reichert completion, the code author copy-pasted `showEJ11CompletionDialog = true`, causing an incorrect dialog to be shown.
   - R.5 is written in 2/4 with sextuplets (sixteenth triplets); Android's divisor of 4.0 makes playback 33% too slow, whereas iOS's divisor of 6.0 is mathematically correct.
5. **Step 5: iOS Test Suite Breakage**
   - The iOS application builds cleanly, but tests fail to compile due to missing convenience methods on `PracticeStore` and a renamed property on `EJ4Section` (`shortName` vs `shortTitle`).

---

## 3. Caveats

- **No Source Code Modified**: As required by the Specification Miner role, no production or test code in `FluteModes/`, `FluteModesAndroid/`, or `docs/` was modified during this survey. All findings and code proposals are documented in `survey_report.md`.
- **WebView Evaluation in Headless CI**: In headless test environments without a display or simulator, JavaScript evaluation inside `WKWebView` and Android `WebView` requires an active window context to verify visual SVG note-head bounding boxes.

---

## 4. Conclusion

The FluteModes architecture across iOS, Android, and Web is solid, well-structured, and has high musical data parity across all 11 modules. However, several high-priority defects must be resolved:
1. **Port the Schott articulation rendering engine from `docs/r{1,2,4,5}.html` into `score_template.html`** (deployed to both iOS and Android assets) to prevent JavaScript runtime crashes.
2. **Build the bidirectional Visual Cursor bridge** (`highlightNote`/`clearHighlight`) in `score_template.html` and wire it to `ScoreAudioPlayer` in both iOS and Android.
3. **Add the 16 missing localization keys in `LocalizationManager.kt`** and localize `"84 Modos"` in `ArticulationPattern.kt`.
4. **Correct Android Reichert practice route handling and completion dialog** in `MainActivity.kt` and `PracticeScreen.kt`.
5. **Align Android audio timing for R.5** by changing the tempo divisor from 4.0 to 6.0, and add final note staccato handling.
6. **Fix download links in `docs/index.html`** to match existing file casing.
7. **Add convenience forwarding methods to `PracticeStore.swift` and `EJ4Section`** so `FluteModesTests` compiles and runs cleanly.

---

## 5. Verification Method

To independently verify all observations in this report:

1. **Verify `score_template.html` missing Schott functions**:
   ```bash
   grep -n "renderR1Schott" FluteModes/FluteModes/Resources/score_template.html
   grep -n "function renderR1Schott" FluteModes/FluteModes/Resources/score_template.html
   # Expected: Line 924 calls renderR1Schott, but 0 function definitions exist.
   ```

2. **Verify Android missing localization keys**:
   ```bash
   python3 -c "
   import re
   kt = open('FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/data/LocalizationManager.kt').read()
   ps = open('FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/ui/screens/PracticeScreen.kt').read()
   used = set(re.findall(r'loc\.t\(\"([^\"]+)\"\)', ps))
   defined = set(re.findall(r'\"([^\"]+)\"\s*to', kt))
   missing = used - defined
   print('Missing keys in Android:', missing)
   "
   ```

3. **Verify Android unit tests**:
   ```bash
   cd FluteModesAndroid && ./gradlew testDebugUnitTest
   ```

4. **Verify iOS target build and test compilation failures**:
   ```bash
   cd FluteModes && xcodebuild build -project FluteModes.xcodeproj -scheme FluteModes -destination "id=94204FC1-C90B-4E72-88EE-A197D4B52046"
   cd FluteModes && xcodebuild test -project FluteModes.xcodeproj -scheme FluteModes -destination "id=94204FC1-C90B-4E72-88EE-A197D4B52046"
   ```

5. **Inspect the comprehensive survey report**:
   View `/Users/sebas/Desktop/partituras/.agents/teamwork/spec_miner_apps_survey/survey_report.md`.
