# Empirical Challenge Report — Milestone 2 (challenger_m2_1)

**Milestone**: Milestone 2 (App UI, Navigation & Localization Parity)  
**Agent**: `challenger_m2_1` (Critic / Empirical Challenger / Specialist)  
**Date**: 2026-10-11T16:32:00Z  
**Parent Agent**: `2c224607-5456-4eac-ad55-0172dee3d36d`

---

## Challenge Summary

**Overall risk assessment**: LOW

Empirical testing confirmed that defect **DEF-09** (Reichert navigation routes and completion dialogs) is thoroughly resolved with genuine, non-facade logic. Cross-platform bilingual localization dictionaries (Spanish and English) exhibit 100% key and content parity (209 keys each, 0 discrepancies, 0 empty values). 

All 1,000 route permutations (25 sections × articulations across R1, R2, R4, R5) construct valid route parameters and bind properly to `score_template.html` renderers. Dedicated completion dialog states in `PracticeScreen.kt` operate with strict cross-exercise isolation and execute genuine round restart, circular key progression (`(sec + 1) % 25`), sequential exercise progression (`R1 -> R2 -> R4 -> R5 -> MODOS`), and dismiss actions.

---

## Challenges & Attack Surface Analysis

### [Low] Challenge 1: Section Index Wrapping at Boundary (Section 24 / Coda)
- **Assumption challenged**: Advancing section from Section 24 (25th key, `C_CODA` / `D.S. al Fine`) cleanly wraps around to Section 0 (`C_MAJOR`) without `IndexOutOfBoundsException` or navigation crash.
- **Attack scenario**: User completes practice round on the final key (Section 24) of Reichert R1, R2, R4, or R5 and taps "Next Key / Siguiente Tonalidad".
- **Blast radius**: Index out of bounds or UI crash on the final exercise section.
- **Mitigation verified**: Formula `val nextSecIdx = (allSecs.indexOf(curSec) + 1) % allSecs.size` was empirically tested across all 25 sections (indices 0..24) in `ReichertNavigationFlowTest.testSectionAdvanceCircularWrapAround` and `verify_navigation_and_dialog_states.py`. For index 24, `(24 + 1) % 25 = 0` resolves to `EJ4Section.C_MAJOR` (Section 0) with zero errors.

### [Low] Challenge 2: Cross-Exercise Dialog Trigger Bleed
- **Assumption challenged**: Completing an 8-articulation round on Reichert R2 or R4, or a 10-articulation round on R1 or R5, never triggers `showEJ11CompletionDialog` or `showEJ4CompletionDialog`.
- **Attack scenario**: User finishes round in R2 or R4; code reuses `showEJ4CompletionDialog` fallback, directing the user inappropriately to E.J. 5 instead of Reichert R4/R5.
- **Blast radius**: User navigation hijacked to incorrect Taffanel & Gaubert exercises.
- **Mitigation verified**: Inspected lines 2076–2144 and 2308–2390 in `PracticeScreen.kt`. Conditionals explicitly branch on `currentExercise.isReichertExercise`:
  - R2/R4 trigger `showReichertCompletionDialog = true`.
  - EJ4 exclusively triggers `showEJ4CompletionDialog = true`.
  - R1/R5 trigger `showReichertCompletionDialog = true`.
  - EJ11 exclusively triggers `showEJ11CompletionDialog = true`.
  Empirically verified by regex and test assertions in `verify_navigation_and_dialog_states.py` and `ReichertNavigationFlowTest.testReichertAndTGStoreIsolation`.

### [Low] Challenge 3: Route Parameter Loss on HomeScreen Tap
- **Assumption challenged**: Clicking an articulation chip or bottom "Start Practice" button for Reichert on `HomeScreen.kt` passes both articulation and section into `Screen.Practice` without discarding user selection.
- **Attack scenario**: User selects Section 14 (`B_MAJOR`) and Articulation 6 (`SLURRED_3_BY_3`), clicks start, but the screen defaults to Section 0 (`C_MAJOR`) and Articulation 0 (`ORIGINAL`).
- **Blast radius**: Degraded user experience where selected section/articulation is discarded upon entering practice mode.
- **Mitigation verified**: `HomeScreen.kt` defines `onStartReichertPractice: (ExerciseType, Any, Any) -> Unit`. Articulation chip taps and bottom CTA buttons explicitly forward `(ex, art, selectedR{1,2,4,5}Section)`. `MainActivity.kt` stores these selections in `PracticeStore` and forwards them into `Screen.Practice` and `PracticeScreen`. Tested across all 1,000 combinations.

---

## Stress Test Results

| Scenario | Expected Behavior | Actual Behavior | Result |
|---|---|---|---|
| R1 Route Construction (11 arts × 25 secs) | 275 valid routes & `% R1_SCHOTT_ART:art:SEC:sec` hooks | 275 valid routes generated and parsed | PASS |
| R2 Route Construction (9 arts × 25 secs) | 225 valid routes & `% R2_SCHOTT_ART:art:SEC:sec` hooks | 225 valid routes generated and parsed | PASS |
| R4 Route Construction (9 arts × 25 secs) | 225 valid routes & `% R4_SCHOTT_ART:art:SEC:sec` hooks | 225 valid routes generated and parsed | PASS |
| R5 Route Construction (11 arts × 25 secs) | 275 valid routes & `% R5_SCHOTT_ART:art:SEC:sec` hooks | 275 valid routes generated and parsed | PASS |
| `score_template.html` hook binding | Regex matches all 4 Reichert hook patterns in Android & iOS | Regex captures exact artId and secId for all 1,000 permutations | PASS |
| Dialog isolation: R2/R4 completion | `showReichertCompletionDialog = true`, `showEJ4 = false` | Exclusively triggers `showReichertCompletionDialog` | PASS |
| Dialog isolation: R1/R5 completion | `showReichertCompletionDialog = true`, `showEJ11 = false` | Exclusively triggers `showReichertCompletionDialog` | PASS |
| Dialog isolation: EJ11 completion | `showEJ11CompletionDialog = true`, advances to R1 | Exclusively triggers `showEJ11`, advance goes to R1 | PASS |
| Dialog isolation: EJ4 completion | `showEJ4CompletionDialog = true`, advances to EJ5 | Exclusively triggers `showEJ4`, advance goes to EJ5 | PASS |
| Action 1: Restart Round | Resets store progress & resets art to index 0 | `resetEJ4`/`resetEJ5Type` called, art set to ALL_SLURRED | PASS |
| Action 2: Advance Section (all 25 keys) | Advances `(sec + 1) % 25`, circular wrap from 24 to 0 | Accurate progression across all 25 keys; wraps 24 -> 0 | PASS |
| Action 3: Advance Exercise | `R1 -> R2 -> R4 -> R5 -> MODOS` | Exact 4-step sequence executed and persisted to store | PASS |
| Action 4: Dismiss / Stay | Closes dialog without modifying exercise/state | `showReichertCompletionDialog = false` | PASS |
| Dictionary Key Parity | 209 keys in Kotlin == 209 keys in Swift | 209 keys in Kotlin == 209 keys in Swift (diff = `set()`) | PASS |
| Dictionary Content Completeness | Zero empty strings in Spanish or English | 0 empty strings found across all 209 keys | PASS |
| Android Unit Test Suite | `./gradlew testDebugUnitTest` runs with 0 errors | 31 unit tests executed across 5 test classes, 0 failures | PASS |
| iOS Release Build | `xcodebuild build` succeeds with 0 errors | `** BUILD SUCCEEDED **` | PASS |
| Master E2E Test Suite | 140/141 passing tests (only DEF-14 failing) | 140/141 passing (99.29% pass rate, 0 DEF-09 failures) | PASS |

---

## Unchallenged Areas

- **DEF-14 Version Bump (v1.5.1 target)**: Intentionally scoped to Milestone 4. Scenarios testing target version 1.5.1 fail as expected at this stage.
- **WAV PCM Synthesis Sample Rate / Pitch Accuracy**: Scoped and thoroughly validated in Milestone 1 challenge report (`tests/verify_audio_synthesis_math.py`).
