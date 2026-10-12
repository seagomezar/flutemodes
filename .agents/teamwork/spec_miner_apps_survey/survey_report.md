# Architectural Survey & Specification Report: FluteModes Ecosystem (iOS, Android, Web)

**Author:** Specification Miner (`spec_miner_apps_survey`)  
**Target:** Architecture, Components, Audio Engines, Navigation, Score Rendering, Visual Cursor Bridge, and Multiplatform Parity  
**Authoritative Reference:** `/Users/sebas/Desktop/partituras/.agents/teamwork/ORIGINAL_REQUEST.md`  
**Date:** 2026-10-11  

---

## Executive Summary

The **FluteModes** ecosystem consists of three software targets designed for flutists practicing modern modes, classical daily exercises (Taffanel & Gaubert), and virtuoso daily studies (M.A. Reichert Op. 5):
1. **Native iOS / iPadOS App** (`FluteModes/`): Built in Swift / SwiftUI, iOS 17.0+ deployment target, target devices iPhone and iPad, utilizing `AVAudioEngine` for low-latency audio synthesis, custom metronome engine, and `WKWebView` evaluating `abcjs` via `score_template.html`.
2. **Native Android App** (`FluteModesAndroid/`): Built in Kotlin / Jetpack Compose, Material 3, compileSdk/targetSdk 36, minSdk 24, utilizing low-level `AudioTrack` PCM streaming for audio synthesis, coroutine-based high-precision metronome, and Android `WebView` evaluating `score_template.html`.
3. **Web Portal** (`docs/`): Hosted on GitHub Pages, built with vanilla HTML5, CSS3, ES6 JavaScript, and CDN-loaded `abcjs` v6.4.4, utilizing Web Audio API (`AudioContext`, OscillatorNode, GainNode ADSR envelopes) for interactive audio playback, modal dialogues, and sheet music rendering.

### Primary Discovered Vulnerabilities & Architectural Gaps
1. **Critical JavaScript Runtime Crash in `score_template.html` (Both iOS & Android)**:
   - In `score_template.html` (lines 922–941), `renderScore(abcString)` contains regex hooks detecting `% R1_SCHOTT_ART`, `% R2_SCHOTT_ART`, `% R4_SCHOTT_ART`, and `% R5_SCHOTT_ART`, which call `renderR1Schott`, `renderR2Schott`, `renderR4Schott`, and `renderR5Schott`.
   - **None of these functions or their section dictionaries are defined in `score_template.html`!** Attempting to render Schott articulations triggers an unhandled `ReferenceError: renderR1Schott is not defined` inside the WebViews.
   - Authoritative reference implementations exist inside `docs/r1.html`, `docs/r2.html`, `docs/r4.html`, and `docs/r5.html`.
2. **Absence of Visual Cursor / Note Highlighting Bridge**:
   - The user specification specifies a visual cursor and synchronized note highlighting during audio playback (`highlightNote`, `clearHighlight`).
   - Neither function exists anywhere in `score_template.html`, nor are any highlight calls emitted by `ScoreAudioPlayer.swift` or `ScoreAudioPlayer.kt`. Audio playback and score rendering are currently completely decoupled.
3. **Android Localization Omissions**:
   - Multiple keys called by `PracticeScreen.kt` via `loc.t(...)` are absent from `LocalizationManager.kt`, resulting in raw key strings displayed to users during milestone popups and section navigation.
   - `MODOS` articulation pattern in `ArticulationPattern.kt` is hardcoded as `"84 Modos"` without an English translation.
4. **Android Reichert Navigation & Completion Dialog Defect**:
   - `MainActivity.kt`'s `Screen.Practice` route does not accept section or articulation parameters for Reichert modules (`R. 1, 2, 4, 5`), discarding user selections from `HomeScreen.kt`.
   - When completing a Reichert exercise round, `PracticeScreen.kt` falls back to `showEJ11CompletionDialog`, erroneously notifying the user that they completed Taffanel & Gaubert E.J. 11.
5. **Audio Engine Timing Discrepancies**:
   - In Kotlin `ScoreAudioPlayer.kt`, Reichert R.5 sixteenth triplets are computed with quarter-note sixteenth division `(60.0 / tempo) / 4.0` instead of triplet sixteenth division `(60.0 / tempo) / 6.0` (as in Swift `ScoreAudioPlayer.swift`).
   - Kotlin lacks staccato shortening on the final note of Reichert exercises.

---

## Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Modos (Modes) | 84 Modes Rendering | Renders 84 ancient, diatonic, and modern flute modes across all 12 chromatic tonics | Tonic index (0–11), Mode index (0–6) | ABC notation string rendered via `abcjs` | Fallbacks to default mode C Ionian | `ModesData.swift`, `ModesData.kt`, `modes_data.js` |
| 2 | Modos (Modes) | Mode Audio Preview | Synthesizes piano-like scale playback of the active mode | Tempo BPM, Mode notes array | Additive harmonic audio stream (44.1kHz PCM) | Clamped tempo bounds (30–300 BPM) | `ScoreAudioPlayer.swift`, `ScoreAudioPlayer.kt`, `docs/r1.html` |
| 3 | E.J. 1 | 5-Note Exercise Generator | Taffanel & Gaubert E.J. 1 scale patterns across registers | Key/Tonality, Metronome BPM | Dynamic ABC score string | None; bounded range | `EJ1Data.swift`, `EJ1Data.kt`, `docs/ej1.html` |
| 4 | E.J. 2 | Full Compass Register Exercise | Taffanel & Gaubert E.J. 2 across low, medium, and high registers | Key, Articulation | ABC score with slurs/staccatos | None | `EJ2Data.swift`, `EJ2Data.kt`, `docs/ej2.html` |
| 5 | E.J. 4 | 24 Keys Comprehensive Study | 24 tonalities with Schott articulation variations | Key index (0–23), Articulation ID | ABC notation with key signature, notes, slurs | Clamps out-of-range keys | `EJ4Data.swift`, `EJ4Data.kt`, `docs/ej4.html` |
| 6 | E.J. 4 | E.J. 4 Audio Playback | Sequential synthesis of 24 keys study with custom articulations | Tempo BPM, Key, Articulations | Audio playback with note envelope shaping | Audio session interruption pauses playback | `ScoreAudioPlayer.swift`, `ScoreAudioPlayer.kt` |
| 7 | E.J. 5 | Chromatic Studies | Chromatic patterns with 10 standard Schott articulations | Section index, Articulation index | ABC notation string | Clamped indices | `EJ5Data.swift`, `EJ5Data.kt`, `docs/ej5.html` |
| 8 | E.J. 10 | Arpeggio Studies | Arpeggios across major, minor, diminished, and augmented chords | Chord root, Chord quality, Articulation | ABC score string | Clamped indices | `EJ10Data.swift`, `EJ10Data.kt`, `docs/ej10.html` |
| 9 | E.J. 11 | Cadences & Extended Arpeggios | Virtuoso arpeggios covering the full flute compass (C4–D7) | Section index, Articulation | Dynamic ABC score string | Clamped indices | `EJ11Data.swift`, `EJ11Data.kt`, `docs/ej11.html` |
| 10 | R. 1 | Reichert Op. 5 No. 1 | 7 key sections with 10 Schott articulations | Section (1–7), Articulation (A–J) | Injects `% R1_SCHOTT_ART` tag into ABC | **Crashes JS** in WebView (`renderR1Schott` missing) | `ReichertData.swift`, `ReichertData.kt`, `score_template.html` |
| 11 | R. 2 | Reichert Op. 5 No. 2 | 7 sections with Schott articulations | Section (1–7), Articulation (A–J) | Injects `% R2_SCHOTT_ART` tag into ABC | **Crashes JS** in WebView (`renderR2Schott` missing) | `ReichertData.swift`, `ReichertData.kt`, `score_template.html` |
| 12 | R. 4 | Reichert Op. 5 No. 4 | Arpeggiated studies with Schott variations | Section (1–6), Articulation (A–J) | Injects `% R4_SCHOTT_ART` tag into ABC | **Crashes JS** in WebView (`renderR4Schott` missing) | `ReichertData.swift`, `ReichertData.kt`, `score_template.html` |
| 13 | R. 5 | Reichert Op. 5 No. 5 | Sixteenth triplet virtuoso study | Section (1–7), Articulation (A–J) | Injects `% R5_SCHOTT_ART` tag into ABC | **Crashes JS** in WebView (`renderR5Schott` missing) | `ReichertData.swift`, `ReichertData.kt`, `score_template.html` |
| 14 | Audio | Additive Harmonic Synthesis | 6 harmonics + acoustic hammer strike transient for piano tone | MIDI pitch, duration, velocity | Mono 44.1 kHz 32-bit Float / 16-bit Int PCM | Inaudible below 20Hz or above Nyquist | `ScoreAudioPlayer.swift`, `ScoreAudioPlayer.kt` |
| 15 | Metronome | High-Precision Click Generator | Synthesized 1400 Hz click with 50ms decay | Tempo BPM (30–300), Time Signature | Periodic audio clicks on main/sub beats | Timer drifting prevention | `MetronomeEngine.swift`, `MetronomeEngine.kt` |
| 16 | Practice Timer | Practice Duration Countdown | Configurable countdown timer with auto-pause and alarm | Duration minutes (5, 10, 15, 20, 30, 45, 60) | Remaining seconds, progress ring UI | Clamped to positive time | `PracticeViewModel.swift`, `PracticeScreen.kt` |
| 17 | Screen Lock | Keep Screen Awake | Prevents screen dimming/sleeping during flute practice | Enabled boolean toggle | System screen timeout disabled | Restores default timeout on exit | `UIApplication.isIdleTimerDisabled`, `FLAG_KEEP_SCREEN_ON` |
| 18 | Score Zoom | Responsive Pinch/Tap Zoom | Allows flutists to resize score for music stands | Zoom scale multiplier (0.5x – 3.0x) | Re-evaluates ABC render with updated scale | Clamped zoom limits | `ScoreWebView.swift`, `ScoreWebView.kt`, `score_template.html` |
| 19 | Localization | Spanish / English Multi-Language | Dynamic UI localization switching without app restart | Language code (`es` / `en`) | Translated localized strings | Fallback to Spanish / key name | `LocalizationManager.swift`, `LocalizationManager.kt` |
| 20 | Round Tracking | Practice Milestone Progression | Tracks completed keys/sections and awards completion badges | Current index, Articulation index | Completion dialogs, round advancement | Missing translation keys in Android | `PracticeViewModel.swift`, `PracticeScreen.kt` |
| 21 | Visual Cursor | Note Playback Tracking Bridge | Synchronized cursor tracking highlighting note heads | Note index, Bar index, Clef | Visual DOM SVG node highlight (`.highlighted`) | **Missing in WebView** | User request R2, `score_template.html` |
| 22 | Web Portal | Sheet Music & Audio Downloads | Downloadable PDFs, ABC source files, and MP3 collections | User click on download cards | File stream download (PDF, ABC, MP3, APK) | Broken link for Reichert ABC files | `docs/index.html`, `docs/downloads/` |

---

## Edge Cases

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | Metronome | Tempo = 300 BPM (Maximum) | Period = 200ms; audio buffer underrun avoided by pre-synthesized click sample. |
| 2 | Metronome | Tempo = 30 BPM (Minimum) | Period = 2000ms; coroutine sleep and RunLoop timer handle 2-second interval accurately. |
| 3 | Reichert Schott Render | ABC string containing `% R1_SCHOTT_ART` | JavaScript engine aborts: `ReferenceError: Can't find variable: renderR1Schott`. Score displays blank canvas. |
| 4 | Score Zoom | Scale = 0.4x (Below min 0.5x) | Clamped to 0.5x; score template rejects scales below lower bound. |
| 5 | Audio Engine | MIDI Pitch 36 (C2) or 96 (C7) | Fundamental frequency calculated via $440 \times 2^{(midi - 69)/12}$. Highest harmonics near Nyquist (22.05 kHz) are handled cleanly without aliasing distortion. |
| 6 | Android Milestone Dialog | User completes all 10 articulations of E.J. 5 | `PracticeScreen.kt` queries `loc.t("ej5_milestone_title")` which is missing from `LocalizationManager.kt`. Raw string `"ej5_milestone_title"` appears as title. |
| 7 | Android Reichert Practice | Completing Section 7 of R.1 | Calls `showEJ11CompletionDialog = true`. Dialog reads "¡Felicitaciones! Has completado el Ejercicio Diario Nº 11" instead of Reichert R.1. |
| 8 | Reichert R.5 Audio Playback | Tempo = 120 BPM in Android vs iOS | iOS plays sixteenth triplets at duration $60/(120 \times 6) = 0.0833\text{ s}$ per note; Android plays at $60/(120 \times 4) = 0.125\text{ s}$ per note (33% slower than intended notation). |
| 9 | Rapid Start/Stop Audio | User taps Play and immediately Stop | iOS calls `audioPlayerNode.stop()` and resets buffer indices; Android cancels playback job and calls `audioTrack.stop()` / `audioTrack.flush()`. No memory leak or native crash. |
| 10 | Background / Foreground | App sent to background while practicing | iOS `AVAudioSession` is `.playback` with `.mixWithOthers` so audio and metronome continue; screen wake lock released on pause. |
| 11 | Web Downloads | User clicks Reichert ABC download on `docs/index.html` | HTTP 404 Not Found due to filename casing mismatch (`reichert_r1_completo.abc` vs `Reichert_R1_Coleccion_Completa.abc`). |

---

## Architectural Breakdown by Platform

### 1. Native iOS / iPadOS (`FluteModes/`)
- **Structure**:
  - `FluteModesApp.swift`: App entry point, sets up audio session category and global tint.
  - `ContentView.swift`: Navigation split view / tab hierarchy for iPhone and iPad layouts.
  - `PracticeViewModel.swift`: State management for practice session, timers, tempo, audio playback, and score generation.
  - `ScoreWebView.swift`: UIViewRepresentable wrapping `WKWebView`. Interacts with `score_template.html` via `webView.evaluateJavaScript("renderScore(...)")`.
  - `AppAudioEngine.swift`: Central `AVAudioEngine` wrapper configuring `AVAudioSession.sharedInstance().setCategory(.playback, mode: .default, options: [.mixWithOthers])`.
  - `ScoreAudioPlayer.swift`: Additive harmonic tone synthesis using 6 harmonics with amplitude falloff ($1/n$), hammer strike transient, and ADSR envelopes. Generates 44.1 kHz 32-bit float audio buffers scheduled on `AVAudioPlayerNode`.
  - `MetronomeEngine.swift`: Synthesizes 1400 Hz click and schedules clicks via high-priority timer on `RunLoop.main` in `.common` mode.
  - `LocalizationManager.swift`: Multi-language manager providing Spanish (`es`) and English (`en`) strings with 163 base keys.
  - `FluteModesTests/`: Test suite testing modes, exercises, and localization.
  - **iOS Build & Test Status**:
    - Main app build (`xcodebuild build`): **SUCCEEDED** (0 errors).
    - Unit test compilation (`xcodebuild test`): **FAILED** due to API mismatch between `FluteModesTests.swift` and `PracticeStore.swift` / `EJ4Section`:
      - `EJ4Section` has property `shortName`, but `FluteModesTests.swift:230` calls `sec.shortTitle`.
      - `PracticeStore` defines `markEJ5TypeCompleted(art, for: .r1)` and `markEJ4Completed(art, for: .r2)`, but `FluteModesTests.swift` calls missing convenience forwarders `markR1Completed`, `markR2Completed`, `markR4Completed`, `markR5Completed`, `isR2FullyCompleted`, and `isR4FullyCompleted`.


### 2. Native Android (`FluteModesAndroid/`)
- **Structure**:
  - `MainActivity.kt`: Single-activity Compose architecture. Manages system bars, navigation stack, and keep-screen-on window flags.
  - `HomeScreen.kt`: Module selection cards for Modos, E.J. 1–11, and R. 1–5.
  - `PracticeScreen.kt`: Practice interface with score display, playback controls, metronome overlay, zoom controls, and timer.
  - `ScoreWebView.kt`: Android `WebView` wrapping `score_template.html`. Injects ABC notation via `evaluateJavascript("renderScore(...)")`.
  - `ScoreAudioPlayer.kt`: Low-level additive synthesis writing 16-bit PCM samples into an `AudioTrack` operating in `MODE_STATIC` or `MODE_STREAM`.
  - `MetronomeEngine.kt`: Coroutine-based click loop using `System.nanoTime()` for drift-free timing, triggering static `AudioTrack` playback.
  - `LocalizationManager.kt`: Multi-language singleton containing 163 dictionary keys.
  - `app/src/test/`: Automated test suite (24 unit tests passing).

### 3. Web Portal (`docs/`)
- **Structure**:
  - `index.html`: Main landing page featuring flute curriculum overview, module index, download links for PDFs/ABC/MP3/APK, and documentation.
  - `modes_data.js`: Complete 84-mode database with note arrays, Greek names, and characteristic intervals.
  - `ej1.html` through `ej11.html`: Standalone web practice pages for Taffanel & Gaubert exercises.
  - `r1.html`, `r2.html`, `r4.html`, `r5.html`: Standalone web practice pages for Reichert studies, containing the **authoritative Schott articulation definitions** (`renderR1Schott`, `renderR2Schott`, etc.).
  - Web Audio: Native `AudioContext` with exponential gain ramps for synthesis.

---

## Detailed Analysis of `score_template.html` & Missing Schott Definitions

Both iOS and Android bundle an identical `score_template.html` file (SHA-256: `748fa33f1c5a70ae4f6b2803b9fb7d27e7f62e84ceb025f12a9e32ffb18db2c2`).

### The Schott Articulation Defect
Lines 922–941 of `score_template.html`:
```javascript
if (abcString.includes('% R1_SCHOTT_ART')) {
    renderR1Schott(cleanAbc);
    return;
}
if (abcString.includes('% R2_SCHOTT_ART')) {
    renderR2Schott(cleanAbc);
    return;
}
if (abcString.includes('% R4_SCHOTT_ART')) {
    renderR4Schott(cleanAbc);
    return;
}
if (abcString.includes('% R5_SCHOTT_ART')) {
    renderR5Schott(cleanAbc);
    return;
}
```
**Problem:** The functions `renderR1Schott`, `renderR2Schott`, `renderR4Schott`, and `renderR5Schott` are never declared in `score_template.html`. When Reichert exercises are loaded in either the iOS or Android app with Schott articulations selected:
1. The app injects the comment header `% R1_SCHOTT_ART ...` into the ABC string.
2. The WebView executes `renderScore(abcString)`.
3. The branch evaluates to true and attempts to call `renderR1Schott(...)`.
4. The JavaScript engine throws: `Uncaught ReferenceError: renderR1Schott is not defined`.
5. Score rendering halts, leaving the canvas blank or showing a web error.

### Authoritative Solution in `docs/r1.html` .. `r5.html`
In `docs/r1.html`, `docs/r2.html`, `docs/r4.html`, and `docs/r5.html`, these functions are fully defined. They:
1. Parse the section number and articulation letter from the comment header.
2. Look up the specific measure grouping and slur rules for that articulation.
3. Transform the raw note sequence into ABC notation with slurs `(...)`, staccato dots `.`, and tenutos.
4. Call `abcjs.renderAbc("score-container", transformedAbc, visualOptions)`.

To resolve this issue across iOS and Android, the Schott articulation dictionary and helper functions must be extracted from `docs/r{1,2,4,5}.html` and integrated into `score_template.html`.

---

## Visual Cursor & Audio Bridge Specification

In `ORIGINAL_REQUEST.md` (R2) and the dispatch assignment, a synchronized visual cursor / note-head highlight is required.

### Current Implementation Gap
1. **In `score_template.html`**:
   - There are no listener callbacks or exported functions for `highlightNote(noteIndex)` or `clearHighlight()`.
   - `abcjs` provides `visualOptions.add_classes = true` which outputs CSS classes for every note head (`abcjs-n0`, `abcjs-n1`, etc.) or SVG element attributes.
2. **In Audio Players (`ScoreAudioPlayer.swift` / `ScoreAudioPlayer.kt`)**:
   - Notes are synthesized in a loop or scheduled via audio buffers, but no callback is invoked to inform the UI of the currently playing note index.
3. **Bridge Architecture Required**:
   - In `score_template.html`: Add:
     ```javascript
     function highlightNote(noteIndex) {
         clearHighlight();
         var el = document.querySelector('.abcjs-n' + noteIndex);
         if (el) {
             el.classList.add('highlighted-note');
             el.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
         }
     }
     function clearHighlight() {
         document.querySelectorAll('.highlighted-note').forEach(function(el) {
             el.classList.remove('highlighted-note');
         });
     }
     ```
   - In iOS: Add a timer/progress callback in `ScoreAudioPlayer.swift` that dispatches `webView.evaluateJavaScript("highlightNote(\(currentIndex))")`.
   - In Android: In `ScoreAudioPlayer.kt`, invoke a callback lambda `onNoteProgress: (Int) -> Unit` after each note duration, calling `webView.evaluateJavascript("highlightNote($currentIndex)", null)`.

---

## Android Localization Defect Analysis

A comparative audit of `LocalizationManager.swift` vs `LocalizationManager.kt` revealed that while both share 163 identical base keys, `PracticeScreen.kt` references 16 keys that are absent from `LocalizationManager.kt`:

1. `ej5_milestone_title`: `"¡Hito de Articulaciones E.J. 5!"` / `"E.J. 5 Articulation Milestone!"`
2. `ej5_milestone_msg`: `"Has completado las 10 articulaciones de esta sección."` / `"You completed all 10 articulations for this section."`
3. `ej5_restart_round`: `"Reiniciar Ronda"` / `"Restart Round"`
4. `ej5_go_to_ej10`: `"Ir a E.J. 10"` / `"Go to E.J. 10"`
5. `ej10_milestone_title`: `"¡Hito de Articulaciones E.J. 10!"` / `"E.J. 10 Articulation Milestone!"`
6. `ej10_milestone_msg`: `"Has completado las 10 articulaciones de este arpegio."` / `"You completed all 10 articulations for this arpeggio."`
7. `ej10_restart_round`: `"Reiniciar Ronda"` / `"Restart Round"`
8. `ej10_go_to_ej11`: `"Ir a E.J. 11"` / `"Go to E.J. 11"`
9. `ej11_milestone_title`: `"¡Hito de Articulaciones E.J. 11!"` / `"E.J. 11 Articulation Milestone!"`
10. `ej11_milestone_msg`: `"Has completado las 10 articulaciones de esta cadencia."` / `"You completed all 10 articulations for this cadence."`
11. `ej11_restart_round`: `"Reiniciar Ronda"` / `"Restart Round"`
12. `ej5_ten_arts_completed`: `"10 articulaciones completadas"` / `"10 articulations completed"`
13. `ej10_ten_arts_completed`: `"10 articulaciones completadas"` / `"10 articulations completed"`
14. `ej11_ten_arts_completed`: `"10 articulaciones completadas"` / `"10 articulations completed"`
15. `ej4_next_section`: `"Siguiente Tonalidad"` / `"Next Tonality"`
16. `ej5_next_section`: `"Siguiente Sección"` / `"Next Section"`

Additionally, `ArticulationPattern.kt` line 49 contains:
```kotlin
MODOS -> "84 Modos"
```
which should be localized via `LocalizationManager` (`"84 Modos"` in Spanish, `"84 Modes"` in English).

---

## Audio Engine Timing & Notation Parity

1. **Reichert R.5 Triplet Division**:
   - In Swift `ScoreAudioPlayer.swift` line 125:
     ```swift
     let noteDuration = (60.0 / tempo) / 6.0 // sixteenth triplets
     ```
   - In Kotlin `ScoreAudioPlayer.kt` line 118:
     ```kotlin
     val noteDuration = (60.0 / tempo) / 4.0 // sixteenth notes (INCORRECT for triplets)
     ```
   - *Fix needed*: Change Android's divisor to `6.0` to match the triplet metric.

2. **Reichert Final Note Duration & Staccato**:
   - In Swift, the final note of R.1, R.2, R.4, and R.5 is lengthened by $2\times$ and flagged `isStaccato: true`, giving it a clean, musical resolution.
   - In Android, the final note is played at standard duration without staccato shaping.

3. **E.J. 4 Tempo Specification**:
   - Swift uses `Q:1/4=\(tempoBPM)` in the ABC header.
   - Android uses `Q:1/2=$tempoBPM` (half note / blanca).
   - Both should align with the authoritative tempo marking in Taffanel & Gaubert.

---

## Web Portal Broken Link Audit

In `docs/index.html`:
- Link: `downloads/abc/reichert_r1_completo.abc` $\rightarrow$ Actual file: `docs/downloads/abc/Reichert_R1_Coleccion_Completa.abc`
- Link: `downloads/abc/reichert_r2_completo.abc` $\rightarrow$ Actual file: `docs/downloads/abc/Reichert_R2_Coleccion_Completa.abc`
- Link: `downloads/abc/reichert_r4_completo.abc` $\rightarrow$ Actual file: `docs/downloads/abc/Reichert_R4_Coleccion_Completa.abc`
- Link: `downloads/abc/reichert_r5_completo.abc` $\rightarrow$ Actual file: `docs/downloads/abc/Reichert_R5_Coleccion_Completa.abc`
- Link: `downloads/apk/FluteModes-v1.5.0-release.apk` $\rightarrow$ Matches existing artifact, but should be updated to `FluteModes-v1.5.1-release.apk` when the new release is built.

---

## Recommendations & Next Implementation Actions

1. **Update `score_template.html` (Both iOS and Android)**:
   - Port `renderR1Schott`, `renderR2Schott`, `renderR4Schott`, and `renderR5Schott` from `docs/r{1,2,4,5}.html` into `score_template.html`.
   - Add `highlightNote(noteIndex)` and `clearHighlight()` functions with smooth scrolling and `.highlighted-note` CSS styling.
2. **Implement Audio-to-WebView Cursor Sync**:
   - In `ScoreAudioPlayer.swift`, add an asynchronous progress callback that runs on the main thread and invokes `highlightNote(index)`.
   - In `ScoreAudioPlayer.kt`, pass a `onNoteProgress: (Int) -> Unit` lambda that calls `webView.evaluateJavascript("highlightNote($index)", null)`.
3. **Fix Android Localization & Navigation**:
   - Add the 16 missing keys to `LocalizationManager.kt`.
   - Update `MainActivity.kt` `Screen.Practice` to accept Reichert section and articulation arguments.
   - Fix `PracticeScreen.kt` Reichert completion handler so it does not invoke `showEJ11CompletionDialog`.
4. **Fix Android Audio Engine**:
   - Update R.5 tempo duration to `(60.0 / tempo) / 6.0`.
   - Add final note duration doubling and staccato articulation.
5. **Fix Web Portal Links**:
   - Correct the file paths in `docs/index.html` to point to the actual filenames in `docs/downloads/abc/`.
