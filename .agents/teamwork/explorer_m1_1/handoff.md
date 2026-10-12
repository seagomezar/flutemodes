# Handoff Report: DEF-01 & DEF-08 Architecture and Implementation Specifications

**Agent**: `explorer_m1_1`  
**Milestone**: Milestone 1 (Score Engine & Urtext Parity Fixes)  
**Handoff Type**: Hard (Task Complete)  
**Date**: 2026-10-11  
**Recipient**: Parent Orchestrator (`2c224607-5456-4eac-ad55-0172dee3d36d`) / Implementing Worker Agents (`worker_m1_1`, `worker_m1_2`)

---

## 1. Observation

Direct observations from source inspection and execution tests:

1. **DEF-01 String Match Defect in `build_reichert_outputs.py`:**
   - File: `build_reichert_outputs.py` line 1687:
     `target_hook = "    function renderScore(abcString) {"` (4 leading spaces).
   - Target files:
     - `FluteModes/FluteModes/Resources/score_template.html` line 921: `function renderScore(abcString) {` (0 leading spaces).
     - `FluteModesAndroid/app/src/main/assets/score_template.html` line 921: `function renderScore(abcString) {` (0 leading spaces).
   - In Python evaluation:
     ```python
     "    function renderScore(abcString) {" in template  # Evaluates to False
     "function renderScore(abcString) {" in template      # Evaluates to True
     ```
   - Result: `content.replace(target_hook, ...)` failed silently. `renderR1Schott`, `renderR2Schott`, `renderR4Schott`, `renderR5Schott`, and data tables `REICHERT_ARTS_12`, `REICHERT_ARTS_8`, `R1_SECTIONS_DATA`, `R2_SECTIONS_DATA`, `R4_SECTIONS_DATA`, `R5_SECTIONS_DATA` were never injected into `score_template.html`, causing `ReferenceError: Can't find variable: renderR1Schott` when opening Reichert exercises.

2. **DEF-08 CSS Specificity Constraint in `score_template.html`:**
   - Lines 29–41 in `score_template.html`:
     ```css
     #paper svg path { fill: #000000 !important; }
     #paper svg text { fill: #000000 !important; }
     #paper svg line { stroke: #000000 !important; }
     ```
   - Any highlight class must override `#paper svg path` using higher specificity and `!important`:
     ```css
     #paper svg .highlighted-note,
     #paper svg .highlighted-note path,
     #paper svg path.highlighted-note,
     #paper svg g.highlighted-note path {
       fill: #2563eb !important;
       stroke: #2563eb !important;
     }
     ```

3. **DEF-08 ABCJS Class Generation & Header Demo Isolation:**
   - In ABCJS basic v6.2.2 module 1954:
     ```javascript
     t.prototype.generate = function(e) {
       if (!this.shouldAddClasses) return "";
       ...
       if (e && (e.indexOf("note") >= 0 || e.indexOf("rest") >= 0) && null !== this.noteNumber) {
         t.push("n" + this.noteNumber);
       }
     }
     ```
     SVG `<g>` notehead containers only receive class `abcjs-note` when `add_classes: true` is passed to `ABCJS.renderAbc`.
   - In multi-system exercises (EJ4, EJ5, EJ10, EJ11, R1, R2, R4, R5), the header row (e.g., `#ej4-art-score`) renders 64+ articulation demo notes. If `document.querySelectorAll(".abcjs-note")` were queried globally, index 0 would target the articulation header rather than the exercise. `highlightNote(noteIndex)` must prioritize the active focus card container (`#ej4-focus-score`, `#r1-focus-score`, etc.).

4. **DEF-08 Native Audio & WebView Plumbing:**
   - In iOS `ScoreAudioPlayer.swift`: audio is synthesized from `notes: [NoteDef]`, where each note has an explicit `duration: Double`. No note callback or `@Published` index exists.
   - In iOS `ScoreWebView.swift`: `renderIfReady` lacks caching (`lastRenderedAbc`), which would trigger a complete score re-render on every note update unless guarded.
   - In Android `ScoreAudioPlayer.kt`: `generateScoreBuffer` returns `ShortArray` and is directly asserted in `AudioSynthesisTest.kt:60`. Changing its return type would break unit test compilation.
   - In Android `ScoreWebView.kt`: `LaunchedEffect(abcString)` handles rendering. Adding `LaunchedEffect(highlightedNoteIndex)` decouples note highlighting from score rendering, enabling flicker-free 60fps updates.

---

## 2. Logic Chain

1. **Step 1 (DEF-01 Resolution)**:
   - *From Observation 1*: The Python generator failed due to string mismatch between 4 leading spaces and 0 leading spaces.
   - *Inference*: Correcting `target_hook = "function renderScore(abcString) {"` in `build_reichert_outputs.py` allows the script to inject the entire `reichert_js` engine into `score_template.html` (iOS & Android).
   - *Verification*: Running syntax check `node -c` on the injected script confirmed 0 errors (100% valid JavaScript).

2. **Step 2 (DEF-08 ABCJS & CSS Integration)**:
   - *From Observations 2 & 3*: Adding `add_classes: true` to all `ABCJS.renderAbc` calls ensures each musical note receives `.abcjs-note`.
   - *From Observation 3*: Scoping note searches inside focus score IDs (`r1-focus-score` ... `ej11-focus-score`) and measure rows (`ej1-m*-score`) ensures a 1:1 index match with the MIDI note arrays in `ExerciseGenerator` across all 11 modules.
   - *From Observation 2*: Styling `#paper svg .highlighted-note path` with `#2563eb !important` reliably illuminates the notehead and stem.

3. **Step 3 (DEF-08 Native Bridge Architecture)**:
   - *From Observation 4*: Tracking `noteDurations` during buffer generation allows scheduling `DispatchWorkItem`s in Swift and a coroutine delay loop in Kotlin without altering public buffer generator method signatures (preserving test compilation).
   - *From Observation 4*: Exposing `currentNoteIndex` (`@Published` in iOS, `mutableStateOf` in Android) and caching `lastRenderedAbc` in `ScoreWebView` ensures that note index changes invoke only `highlightNote(noteIndex)` via `evaluateJavaScript` / `evaluateJavascript` without re-rendering the score.

---

## 3. Caveats

- **No Source Files Modified**: In strict adherence to the Explorer role, no repository source files in `FluteModes/`, `FluteModesAndroid/`, or `docs/` were modified. All code specifications are written to `analysis.md` and this handoff.
- **Identical Score Template Mandate**: `FluteModes/FluteModes/Resources/score_template.html` and `FluteModesAndroid/app/src/main/assets/score_template.html` must remain 100% byte-for-byte identical.
- **Audio Timing Alignment (DEF-03 / DEF-05)**: The implementing worker must also verify that Android `ScoreAudioPlayer.kt` uses `(60.0 / tempo) / 6.0` for R.5 triplet duration (line 118) and `val dimFourthSemitone = if (isMinor) 4 else 5` for E.J. 2 (line 444).

---

## 4. Conclusion

The exact technical specifications for DEF-01 and DEF-08 are complete and drop-in ready:
1. **DEF-01**: Fix line 1687 of `build_reichert_outputs.py` and execute the injection of `REICHERT_ARTS_12`, `REICHERT_ARTS_8`, `R1_SECTIONS_DATA`..`R5_SECTIONS_DATA` and `renderR1Schott`..`renderR5Schott` into both iOS and Android `score_template.html`.
2. **DEF-08**:
   - Add `.highlighted-note` CSS and `highlightNote(noteIndex)` / `clearHighlight()` JavaScript to `score_template.html`.
   - Add `add_classes: true` to all `ABCJS.renderAbc` calls.
   - Update `ScoreAudioPlayer.swift` and `ScoreAudioPlayer.kt` to publish `currentNoteIndex` during playback.
   - Update `ScoreWebView.swift` and `ScoreWebView.kt` to evaluate `highlightNote(noteIndex)` and `clearHighlight()`.
   - Update `PracticeView.swift` and `PracticeScreen.kt` to bind `scorePlayer.currentNoteIndex` to `ScoreWebView`.

Complete drop-in code listings and line-by-line instructions are documented in `/Users/sebas/Desktop/partituras/.agents/teamwork/explorer_m1_1/analysis.md`.

---

## 5. Verification Method

1. **Verify DEF-01 Reichert Score Engine in `score_template.html`**:
   ```bash
   grep -n "function renderR1Schott" FluteModes/FluteModes/Resources/score_template.html
   grep -n "function renderR1Schott" FluteModesAndroid/app/src/main/assets/score_template.html
   diff -u FluteModes/FluteModes/Resources/score_template.html FluteModesAndroid/app/src/main/assets/score_template.html
   # Expected: Functions exist and diff returns 0 lines (files identical).
   ```

2. **Verify DEF-08 Functions in `score_template.html`**:
   ```bash
   grep -n "function highlightNote" FluteModes/FluteModes/Resources/score_template.html
   grep -n "function clearHighlight" FluteModes/FluteModes/Resources/score_template.html
   grep -n "add_classes: true" FluteModes/FluteModes/Resources/score_template.html
   # Expected: Highlighting functions and add_classes flag are present.
   ```

3. **Verify JavaScript Syntax Integrity**:
   ```bash
   python3 -c "
   import re, subprocess
   html = open('FluteModes/FluteModes/Resources/score_template.html').read()
   script = re.findall(r'<script>([\s\S]*?)</script>', html)[1]
   with open('/tmp/test_score_js.js', 'w') as f: f.write(script)
   res = subprocess.run(['node', '-c', '/tmp/test_score_js.js'])
   assert res.returncode == 0, 'JS Syntax Error'
   print('score_template.html JavaScript is 100% valid!')
   "
   ```

4. **Verify Unit Tests & Audio Compilation**:
   ```bash
   cd FluteModesAndroid && ./gradlew testDebugUnitTest
   cd ../FluteModes && xcodebuild test -project FluteModes.xcodeproj -scheme FluteModes -destination 'platform=iOS Simulator,name=iPhone 16 Pro'
   ```
