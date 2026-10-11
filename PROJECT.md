# Project: FluteModes Urtext Musicological Audit, Parity & v1.5.1 Release

## Architecture
FluteModes is a multiplatform flute pedagogy ecosystem covering 84 Modal Parallel Exercises, Taffanel & Gaubert (E.J. 1, 2, 4, 5, 10, 11), and Mathieu-André Reichert Op. 5 (R. 1, 2, 4, 5).

- **Core Notation & Rendering Engine:**
  - Shared ABC music notation renderer (`score_template.html` using abcjs) embedded inside iOS `WKWebView` and Android `WebView`.
  - Standalone interactive web portal in `docs/` (`index.html`, `ej*.html`, `r*.html`).
  - Standalone ABC files (`*.abc`, `docs/downloads/abc/`) and printable A4 PDFs (`docs/downloads/pdf/`).
- **Native Applications:**
  - **iOS/iPadOS (`FluteModes/`):** Swift, SwiftUI, `WKWebView`, `AVAudioEngine` PCM synthesizer (`ScoreAudioPlayer.swift`), state persistence (`PracticeStore.swift`), i18n (`LocalizationManager.swift`), unit tests (`FluteModesTests.swift`).
  - **Android (`FluteModesAndroid/`):** Kotlin, Jetpack Compose, Android `WebView`, `AudioTrack` PCM synthesizer (`ScoreAudioPlayer.kt`), state persistence (`PracticeStore.kt`), i18n (`LocalizationManager.kt`), unit tests (`ExerciseGeneratorTest.kt`, `PracticeStoreTest.kt`).
- **Release & Distribution Pipeline:**
  - Android signed APK (`app/flutemodes-release.jks`, `./gradlew assembleRelease` -> `docs/downloads/apk/FluteModes-v1.5.1-release.apk`).
  - iOS TestFlight / App Store Connect archive and upload (`xcodebuild archive` + `xcodebuild -exportArchive -allowProvisioningUpdates`).
  - GitHub repository (`main` branch, tag `v1.5.1`).

---

## Feature Inventory
Every feature identified during the survey phase from the user request and codebase inspection is assigned to a milestone:

| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F01 | 84 Modal Exercises Urtext Parity | 12 tonics × 7 modes × 8 articulations (672 combinations) verification across ABC, web, native | M1 | survey |
| F02 | T&G Urtext Parity | E.J. 1, 2, 4, 5, 10, 11 pitch, meter, accidental, and articulation compliance against Alphonse Leduc Pl. 16.588 | M1 | survey |
| F03 | Reichert Urtext Parity | Op. 5 R. 1, 2, 4, 5 pitch, octave, repeat signs, and articulation compliance against B. Schott Pl. 20623 | M1 | survey |
| F04 | DEF-01: Schott Score Template Engine | Inject missing `renderR1Schott`..`renderR5Schott` and section data into iOS and Android `score_template.html` | M1 | survey |
| F05 | DEF-02: Android EJ2 Accidental Fix | Correct 18 corrupted major-third notes in mm. 4, 8, 14, 18, 22, 24, 28 of `ExerciseGenerator.kt` | M1 | survey |
| F06 | DEF-03: Android Audio EJ2 Diminished Semitone | Align line 444 of `ScoreAudioPlayer.kt` to use `base + (if (isMinor) 4 else 5)` | M1 | survey |
| F07 | DEF-05: Android Audio R.5 Triplet Timing | Correct sixteenth-triplet tempo divisor from 4.0 to 6.0 in `ScoreAudioPlayer.kt` | M1 | survey |
| F08 | DEF-08: Visual Cursor Sync Bridge | Implement `highlightNote` / `clearHighlight` in `score_template.html` and bridge native playback calls | M1 | survey |
| F09 | DEF-09: Android Reichert Routing & Dialogs | Fix `PracticeScreen.kt` Reichert arguments, prevent EJ11 dialog on Reichert, and sync missing keys in `LocalizationManager.kt` | M2 | survey |
| F10 | DEF-06/07: Web Portal Links & ABC Downloads | Fix casing mismatches in `docs/index.html` download links and provide `00_Coleccion_Completa_84_Modos_EJ4.abc` | M1 | survey |
| F11 | DEF-04: iOS Test Compilation Fixes | Fix `sec.shortName` and `PracticeStore` method calls in `FluteModesTests.swift` | M3 | survey |
| F12 | iOS Unit Test Suite Expansion | Add test coverage for E.J. 5, 10, 11 and Reichert R. 1, 2, 4, 5 in `FluteModesTests.swift` | M3 | survey |
| F13 | Android Unit Test Suite Expansion | Add and verify comprehensive tests in `ExerciseGeneratorTest.kt` and `PracticeStoreTest.kt` | M3 | survey |
| F14 | Version Bump v1.5.1 | iOS 1.5.1 (Build 10), Android versionCode 9 (versionName 1.5.1), Web references updated | M4 | survey |
| F15 | Android Signed APK Build & Verification | `./gradlew testDebugUnitTest assembleRelease`, apksigner verify, copy to `docs/downloads/apk/` | M4 | survey |
| F16 | iOS Archive & TestFlight Upload | `xcodebuild archive` + `xcodebuild -exportArchive -allowProvisioningUpdates` Build 10 | M4 | survey |
| F17 | Git Release Tag & Push | Commit all changes, tag `v1.5.1`, push to `origin main --tags` | M4 | survey |

---

## Milestones

| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Score Engine & Urtext Parity Fixes | F01, F02, F03, F04, F05, F06, F07, F08, F10: Repair `score_template.html` (iOS & Android) with Schott renderers, fix Android E.J. 2 accidentals in `ExerciseGenerator.kt`, fix audio synth semitone and triplet timing, wire visual cursor hooks, fix web download links. | none | DONE |
| M2 | App UI, Navigation & Localization Parity | F09: Fix Android Reichert route args, Reichert completion dialog in `PracticeScreen.kt`, and audit all localization keys in `LocalizationManager.kt` and `LocalizationManager.swift`. | M1 | DONE |
| M3 | Unit Test Expansion & Verification | F11, F12, F13: Fix `FluteModesTests.swift` compilation and add E.J. 5/10/11 + Reichert test cases; expand Android test cases; verify 100% pass on both platforms. | M1, M2 | PLANNED |
| M-E2E | E2E Testing Track | Independent opaque-box test suite covering Tiers 1-4 across all 11 modules and multiplatform requirements; publish `TEST_READY.md`. | none | DONE |
| M-Final | Final Milestone: E2E Test Pass & Hardening | Pass 100% of E2E test suite (Tiers 1-4) + Tier 5 adversarial hardening across all modules. | M1, M2, M3, M-E2E | PLANNED |
| M4 | Version Bump & Release Deployment | F14, F15, F16, F17: Update versions to v1.5.1 (Build 10, versionCode 9), build & sign release APK, archive & upload iOS Build 10 to TestFlight, git commit/tag/push. | M-Final | PLANNED |

---

## Interface Contracts

### Score Template ↔ Native WebViews
- **Function:** `renderScore(abcString)`: Detects `% EJ...` and `% R..._SCHOTT_ART:artIndex:SEC:secIndex` comment hooks and renders correct score via abcjs.
- **Function:** `highlightNote(noteIndex)`: Adds CSS highlight class `.highlighted-note` to the note element at index `noteIndex`.
- **Function:** `clearHighlight()`: Removes all highlighted note classes.
- **Contract:** Identical file in:
  - `FluteModes/FluteModes/Resources/score_template.html`
  - `FluteModesAndroid/app/src/main/assets/score_template.html`

### Exercise Generator ↔ Audio Player
- **MIDI Sequence:** Array of integers representing standard MIDI pitches (59 to 98 for standard flute range C4/B3 to D7).
- **Pitch Frequency Formula:** `f = 440.0 * 2^((midi - 69) / 12.0)`.

### Practice Store
- **EJ4 / Reichert 2 & 4 Progress:**
  - `markEJ4Completed(artIndex, for: .r2 / .r4)`
  - `isEJ4TypeFullyCompleted(for: .r2 / .r4)`
- **EJ5 / Reichert 1 & 5 Progress:**
  - `markEJ5TypeCompleted(artIndex, for: .r1 / .r5)`
  - `isEJ5TypeFullyCompleted(for: .r1 / .r5)`

---

## Code Layout
- **iOS Application:**
  - `FluteModes/FluteModes/Resources/score_template.html`
  - `FluteModes/FluteModes/Models/ExerciseGenerator.swift`
  - `FluteModes/FluteModes/Models/PracticeStore.swift`
  - `FluteModes/FluteModes/Models/LocalizationManager.swift`
  - `FluteModes/FluteModes/Audio/ScoreAudioPlayer.swift`
  - `FluteModes/FluteModes/Views/`
  - `FluteModes/FluteModesTests/FluteModesTests.swift`
  - `FluteModes/project.yml`
  - `FluteModes/FluteModes.xcodeproj/project.pbxproj`
- **Android Application:**
  - `FluteModesAndroid/app/src/main/assets/score_template.html`
  - `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/ExerciseGenerator.kt`
  - `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/PracticeStore.kt`
  - `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/LocalizationManager.kt`
  - `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/ScoreAudioPlayer.kt`
  - `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/MainActivity.kt`
  - `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/PracticeScreen.kt`
  - `FluteModesAndroid/app/src/test/java/com/seagomezar/flutemodes/`
  - `FluteModesAndroid/app/build.gradle.kts`
- **Web Portal & Documentation:**
  - `docs/index.html`
  - `docs/ej*.html`
  - `docs/r*.html`
  - `docs/downloads/apk/`
  - `docs/downloads/abc/`
  - `docs/downloads/pdf/`
