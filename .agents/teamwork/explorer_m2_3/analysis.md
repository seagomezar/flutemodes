# Milestone 2 Investigation Report: App UI, Navigation & Localization Parity (DEF-09)

**Author:** `explorer_m2_3`  
**Date:** 2026-10-11  
**Scope:** Multiplatform Navigation across all 11 modules, Screen Keep-Awake, E2E DEF-09 test requirements, and Localization Parity.

---

## Executive Summary

1. **E2E DEF-09 Failure Diagnosis**:
   - `tests/run_e2e_tests.py` runs 141 tests across Tiers 1–4. Exactly two fail:
     - `test_c14_android_reichert_navigation_routes` (`[DEF-09]` in `tests/test_tier3_combinations.py`)
     - `test_s10_multiplatform_version_consistency_target` (`[DEF-14]`, deferred to M4 version bump).
   - `test_c14` enforces that `MainActivity.kt` contains the signature `onStartReichertPractice = { ex, art, sec ->`. Currently, `MainActivity.kt` defines `onStartReichertPractice = { ex ->`, discarding the chosen articulation and section.
   - In `PracticeScreen.kt`, completing Reichert R1 or R5 incorrectly defaults into `else -> showEJ11CompletionDialog = true`, displaying the Taffanel & Gaubert E.J. 1 completion dialog on Reichert exercises.
   - `PracticeScreen.kt` calls 15 localization keys (`ej4_next_section`, `ej5_milestone_title`, `ej5_milestone_msg`, `ej5_restart_round`, `ej5_ten_arts_completed`, `ej5_go_to_ej10`, `ej5_next_section`, `ej10_milestone_title`, `ej10_milestone_msg`, `ej10_restart_round`, `ej10_ten_arts_completed`, `ej10_go_to_ej11`, `ej10_next_section`, `ej11_ten_arts_completed`, `ej11_next_section`) that do not exist in `LocalizationManager.kt` or `LocalizationManager.swift`.

2. **iOS Navigation & Screen Keep-Awake Verification**:
   - iOS views are structured in `HomeView.swift` and `PracticeView.swift` (with `FluteModesApp.swift` as app entrypoint).
   - Navigation across all 11 modules (`ej1`, `ej2`, `ej4`, `ej5`, `ej10`, `ej11`, `r1`, `r2`, `r4`, `r5`, `modos`) is fully supported in both `HomeView.swift` (exercise selector chips) and `PracticeView.swift` (horizontal switcher pill in `mobileTopBar` and `topBar`).
   - Metronome: Integrated via `MetronomeEngine.swift` (accurate 1400 Hz click, RunLoop `.common` mode `Timer`, BPM +/-2 adjustments, beat dot animations).
   - Screen keep-awake: Integrated via `UIApplication.shared.isIdleTimerDisabled` in `PracticeView.swift` (onAppear, onChange, and onDisappear), toggleable in `HomeView.swift`, and persisted in `UserDefaults` (`FluteModes_keepScreenAwake`), verified by `testKeepScreenAwakeSettingPersistence()` in `FluteModesTests.swift`.
   - Android screen keep-awake: Managed via `LaunchedEffect(store.keepScreenAwake)` setting/clearing `WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON` in `MainActivity.kt`.

3. **Parity Solution**:
   - Provide concrete drop-in code specifications for `MainActivity.kt`, `HomeScreen.kt`, `PracticeScreen.kt`, and synchronized localization updates for `LocalizationManager.kt` and `LocalizationManager.swift` (42 new keys, bringing both dictionaries to 205 keys).
   - Upon applying these specifications, `test_c14_android_reichert_navigation_routes` will pass, reducing E2E defect count for M2 to 0.

---

## Detailed Findings

### 1. Root Cause of DEF-09 Failure

In `tests/test_tier3_combinations.py`, line 157:
```python
def test_c14_android_reichert_navigation_routes(self):
    """
    DEF-09 Verification: MainActivity.kt must pass section and art arguments to Screen.Practice for Reichert.
    Currently onStartReichertPractice accepts only 'ex' and discards section/art.
    """
    main_act = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "java" / "com" / "seagomezar" / "flutemodes" / "MainActivity.kt"
    content = main_act.read_text(encoding="utf-8")
    self.assertRegex(content, r'onStartReichertPractice\s*=\s*\{\s*ex,\s*art,\s*sec\s*->',
                     "DEF-09: MainActivity.kt onStartReichertPractice must receive (ex, art, sec)")
```

In `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/MainActivity.kt`:
- Lines 219–237 define:
  ```kotlin
  onStartReichertPractice = { ex ->
      store.lastExerciseType = ex
      store.saveLastSelection()
      currentScreen = Screen.Practice(
          exerciseType = ex,
          ...
  ```
- Because only `ex` is passed, when a user selects a specific Reichert section (e.g. Section 12) or articulation (e.g. Articulation 4) from `HomeScreen.kt`, those selections are ignored if not already saved to the store, and `Screen.Practice` defaults or reads stale store state.

In `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/ui/HomeScreen.kt`:
- Line 36 defines `onStartReichertPractice: (ExerciseType) -> Unit = {}`.
- In line 492, 497, 586, 815, 820, and 909, `onStartReichertPractice(ex)` is called with only 1 parameter, despite `HomeScreen` having local state variables `selectedR1Art`, `selectedR1Section`, `selectedR2Art`, `selectedR2Section`, etc.

In `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/ui/PracticeScreen.kt`:
- Lines 2165–2173:
  ```kotlin
  if (isEJ5TypeFullyDone) {
      Button(
          onClick = {
              when (currentExercise) {
                  ExerciseType.EJ5 -> showEJ5CompletionDialog = true
                  ExerciseType.EJ10 -> showEJ10CompletionDialog = true
                  else -> showEJ11CompletionDialog = true
              }
          },
  ```
- Lines 2235–2241:
  ```kotlin
  if (store.isEJ5TypeFullyCompleted(currentExercise)) {
      when (currentExercise) {
          ExerciseType.EJ5 -> showEJ5CompletionDialog = true
          ExerciseType.EJ10 -> showEJ10CompletionDialog = true
          else -> showEJ11CompletionDialog = true
      }
  }
  ```
  Both blocks treat Reichert R1 and R5 as fallback `else`, setting `showEJ11CompletionDialog = true`.
- Furthermore, `showEJ11CompletionDialog` displays `loc.t("ej1_milestone_msg")` and restart text `loc.t("ej1_restart_round")`, which is a T&G EJ1 dialog on Reichert.

---

### 2. Localization Coverage Audit

Current status:
- Both `LocalizationManager.kt` and `LocalizationManager.swift` contain exactly 163 keys, but both lack 15 keys actively referenced in `PracticeScreen.kt`:
  1. `ej4_next_section` (line 1930)
  2. `ej5_milestone_title` (line 397)
  3. `ej5_milestone_msg` (line 402)
  4. `ej5_restart_round` (line 418)
  5. `ej5_ten_arts_completed` (line 2191)
  6. `ej5_go_to_ej10` (line 432)
  7. `ej5_next_section` (line 2133)
  8. `ej10_milestone_title` (line 451)
  9. `ej10_milestone_msg` (line 456)
  10. `ej10_restart_round` (line 472)
  11. `ej10_ten_arts_completed` (line 2192)
  12. `ej10_go_to_ej11` (line 486)
  13. `ej10_next_section` (line 2134)
  14. `ej11_ten_arts_completed` (line 2193)
  15. `ej11_next_section` (line 2135)
- In addition, completing Reichert R1, R2, R4, and R5 requires dedicated milestone dialog strings to prevent string fallbacks or mismatched labels.
- Synchronizing 42 missing/expansion keys in both `LocalizationManager.kt` and `LocalizationManager.swift` brings both files to 205 keys with 100% parity across `es` and `en`.

---

### 3. iOS Navigation, Screen Keep-Awake & Metronome Verification

- **Views**:
  - `FluteModes/FluteModes/App/FluteModesApp.swift` initializes `PracticeViewModel` and sets `HomeView` as the root window.
  - `HomeView.swift` contains a horizontal scroll bar iterating over `ExerciseType.allCases`, setting `viewModel.selectExercise(exercise)` and navigating to `PracticeView` via `.navigationDestination(isPresented: $navigateToPractice)`.
  - `PracticeView.swift` contains `mobileTopBar` and `topBar`, both with horizontal scroll pickers iterating over `ExerciseType.allCases`, allowing direct jumps between `EJ1`, `EJ2`, `EJ4`, `EJ5`, `EJ10`, `EJ11`, `R1`, `R2`, `R4`, `R5`, and `MODOS`.
- **Screen Keep-Awake**:
  - `PracticeView.swift`:
    ```swift
    .onAppear {
        viewModel.updateScore()
        if viewModel.keepScreenAwake {
            UIApplication.shared.isIdleTimerDisabled = true
        }
    }
    .onChange(of: viewModel.keepScreenAwake) { isAwake in
        UIApplication.shared.isIdleTimerDisabled = isAwake
    }
    .onDisappear {
        scorePlayer.stop()
        metronome.stop()
        UIApplication.shared.isIdleTimerDisabled = false
    }
    ```
  - `HomeView.swift` lines 417–421 provides a UI toggle for `keepScreenAwake`.
  - `PracticeViewModel.swift` lines 40–60 persists this setting in `UserDefaults` (`FluteModes_keepScreenAwake`).
  - Unit test `testKeepScreenAwakeSettingPersistence()` in `FluteModesTests.swift` confirms persistence.
- **Metronome Engine**:
  - `MetronomeEngine.swift` runs a `Timer` on `RunLoop.common`, generating a 1400 Hz sine wave tone with 50ms exponential decay.
  - `PracticeView.swift` lines 1057–1098 and 1382–1425 provide full controls: play/pause, tempo stepper (-/+ 2 BPM), beat visualizer dots, and direct BPM display.

---

## Drop-in Code Specifications for Worker

### File 1: `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/MainActivity.kt`

#### Step 1.1: Update `Screen.Practice` data class
Add Reichert parameters with defaults:
```kotlin
    data class Practice(
        val exerciseType: ExerciseType = ExerciseType.EJ1,
        val ej1Articulation: EJ1Articulation = EJ1Articulation.ORIGINAL,
        val ej2Articulation: EJ1Articulation = EJ1Articulation.ORIGINAL,
        val ej4Articulation: EJ4Articulation = EJ4Articulation.ORIGINAL,
        val ej4Section: EJ4Section = EJ4Section.C_MAJOR,
        val ej5Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
        val ej5Section: EJ5Section = EJ5Section.C_CHROM,
        val ej10Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
        val ej10Section: EJ10Section = EJ10Section.C_ARP,
        val ej11Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
        val ej11Section: EJ10Section = EJ10Section.C_ARP,
        val r1Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
        val r1Section: EJ4Section = EJ4Section.C_MAJOR,
        val r2Articulation: EJ4Articulation = EJ4Articulation.ORIGINAL,
        val r2Section: EJ4Section = EJ4Section.C_MAJOR,
        val r4Articulation: EJ4Articulation = EJ4Articulation.ORIGINAL,
        val r4Section: EJ4Section = EJ4Section.C_MAJOR,
        val r5Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
        val r5Section: EJ4Section = EJ4Section.C_MAJOR,
        val tonic: Tonic = Tonic.DO_NATURAL,
        val mode: ModeType = ModeType.IONIAN
    ) : Screen()
```

#### Step 1.2: Update `onStartReichertPractice` in `MainActivity.kt`
Match the `test_c14` regex `r'onStartReichertPractice\s*=\s*\{\s*ex,\s*art,\s*sec\s*->'` and update state:
```kotlin
                                onStartReichertPractice = { ex, art, sec ->
                                    store.lastExerciseType = ex
                                    when (ex) {
                                        ExerciseType.R1 -> {
                                            if (art is EJ5Articulation) store.lastR1Articulation = art
                                            if (sec is EJ4Section) store.lastR1Section = sec
                                        }
                                        ExerciseType.R2 -> {
                                            if (art is EJ4Articulation) store.lastR2Articulation = art
                                            if (sec is EJ4Section) store.lastR2Section = sec
                                        }
                                        ExerciseType.R4 -> {
                                            if (art is EJ4Articulation) store.lastR4Articulation = art
                                            if (sec is EJ4Section) store.lastR4Section = sec
                                        }
                                        ExerciseType.R5 -> {
                                            if (art is EJ5Articulation) store.lastR5Articulation = art
                                            if (sec is EJ4Section) store.lastR5Section = sec
                                        }
                                        else -> {}
                                    }
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ex,
                                        ej1Articulation = store.lastEJ1Articulation,
                                        ej2Articulation = store.lastEJ2Articulation,
                                        ej4Articulation = if (ex == ExerciseType.R2 || ex == ExerciseType.R4) (art as? EJ4Articulation ?: store.lastEJ4Articulation) else store.lastEJ4Articulation,
                                        ej4Section = if (ex.isReichertExercise) (sec as? EJ4Section ?: store.lastEJ4Section) else store.lastEJ4Section,
                                        ej5Articulation = if (ex == ExerciseType.R1 || ex == ExerciseType.R5) (art as? EJ5Articulation ?: store.lastEJ5Articulation) else store.lastEJ5Articulation,
                                        ej5Section = store.lastEJ5Section,
                                        ej10Articulation = store.lastEJ10Articulation,
                                        ej10Section = store.lastEJ10Section,
                                        ej11Articulation = store.lastEJ11Articulation,
                                        ej11Section = store.lastEJ11Section,
                                        r1Articulation = store.lastR1Articulation,
                                        r1Section = store.lastR1Section,
                                        r2Articulation = store.lastR2Articulation,
                                        r2Section = store.lastR2Section,
                                        r4Articulation = store.lastR4Articulation,
                                        r4Section = store.lastR4Section,
                                        r5Articulation = store.lastR5Articulation,
                                        r5Section = store.lastR5Section,
                                        tonic = store.lastTonic ?: Tonic.DO_NATURAL,
                                        mode = store.lastMode ?: ModeType.IONIAN
                                    )
                                },
```

#### Step 1.3: Pass Reichert arguments to `PracticeScreen` in `MainActivity.kt`
In `is Screen.Practice ->`:
```kotlin
                                initialR1Articulation = screen.r1Articulation,
                                initialR1Section = screen.r1Section,
                                initialR2Articulation = screen.r2Articulation,
                                initialR2Section = screen.r2Section,
                                initialR4Articulation = screen.r4Articulation,
                                initialR4Section = screen.r4Section,
                                initialR5Articulation = screen.r5Articulation,
                                initialR5Section = screen.r5Section,
```

---

### File 2: `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/ui/HomeScreen.kt`

#### Step 2.1: Update `HomeScreen` parameter signature
Change line 36:
```kotlin
    onStartReichertPractice: (ExerciseType, Any, Any) -> Unit = { _, _, _ -> },
```

#### Step 2.2: Forward arguments from `HomeScreen`
- Lines 488–498:
  ```kotlin
  ExerciseType.R2 -> {
      selectedR2Art = art
      store.lastR2Articulation = art
      onStartReichertPractice(ex, art, selectedR2Section)
  }
  ExerciseType.R4 -> {
      selectedR4Art = art
      store.lastR4Articulation = art
      onStartReichertPractice(ex, art, selectedR4Section)
  }
  ```
- Lines 584–590:
  ```kotlin
  if (ex.isReichertExercise) {
      onStartReichertPractice(ex, curArt, curSec)
  } else {
      onStartEJ4Practice(selectedEJ4Art, selectedEJ4Section)
  }
  ```
- Lines 812–822:
  ```kotlin
  ExerciseType.R1 -> {
      selectedR1Art = art
      store.lastR1Articulation = art
      onStartReichertPractice(ex, art, selectedR1Section)
  }
  ExerciseType.R5 -> {
      selectedR5Art = art
      store.lastR5Articulation = art
      onStartReichertPractice(ex, art, selectedR5Section)
  }
  ```
- Lines 905–912:
  ```kotlin
  ExerciseType.EJ5 -> onStartEJ5Practice(selectedEJ5Art, selectedEJ5Section)
  ExerciseType.EJ10 -> onStartEJ10Practice(selectedEJ10Art, selectedEJ10Section)
  ExerciseType.EJ11 -> onStartEJ11Practice(selectedEJ11Art, selectedEJ11Section)
  ExerciseType.R1 -> onStartReichertPractice(ex, selectedR1Art, selectedR1Section)
  ExerciseType.R5 -> onStartReichertPractice(ex, selectedR5Art, selectedR5Section)
  ```

---

### File 3: `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/ui/PracticeScreen.kt`

#### Step 3.1: Add constructor parameters & state initialization
```kotlin
    initialR1Articulation: EJ5Articulation = store.lastR1Articulation,
    initialR1Section: EJ4Section = store.lastR1Section,
    initialR2Articulation: EJ4Articulation = store.lastR2Articulation,
    initialR2Section: EJ4Section = store.lastR2Section,
    initialR4Articulation: EJ4Articulation = store.lastR4Articulation,
    initialR4Section: EJ4Section = store.lastR4Section,
    initialR5Articulation: EJ5Articulation = store.lastR5Articulation,
    initialR5Section: EJ4Section = store.lastR5Section,
```
Initialize `currentR1Articulation`..`currentR5Section` from these parameters instead of directly reading `store`.

#### Step 3.2: Isolate `showEJ11CompletionDialog`
Update `showEJ11CompletionDialog`:
```kotlin
    if (showEJ11CompletionDialog) {
        AlertDialog(
            onDismissRequest = { showEJ11CompletionDialog = false },
            title = {
                Text(
                    text = loc.t("ej11_milestone_title"),
                    fontWeight = FontWeight.Bold
                )
            },
            text = {
                Text(text = loc.t("ej11_milestone_msg"))
            },
            confirmButton = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            store.resetEJ5Type(ExerciseType.EJ11)
                            currentEJ11Articulation = EJ5Articulation.ALL_SLURRED
                            store.lastEJ11Articulation = currentEJ11Articulation
                            store.saveLastSelection()
                            showEJ11CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("ej11_restart_round"))
                    }

                    Button(
                        onClick = {
                            scorePlayer.stop()
                            currentExercise = ExerciseType.R1
                            store.lastExerciseType = ExerciseType.R1
                            store.saveLastSelection()
                            showEJ11CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(loc.t("r1_title"))
                    }

                    TextButton(
                        onClick = { showEJ11CompletionDialog = false },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("stay_mode"))
                    }
                }
            }
        )
    }
```

#### Step 3.3: Add dedicated `showReichertEJ5CompletionDialog` for R1 and R5
```kotlin
    var showReichertEJ5CompletionDialog by remember { mutableStateOf(false) }

    if (showReichertEJ5CompletionDialog) {
        AlertDialog(
            onDismissRequest = { showReichertEJ5CompletionDialog = false },
            title = {
                Text(
                    text = "¡${currentExercise.pillLabel} Completado (10/10 Articulaciones)!",
                    fontWeight = FontWeight.Bold
                )
            },
            text = {
                Text(text = if (currentExercise == ExerciseType.R1) loc.t("r1_milestone_msg") else loc.t("r5_milestone_msg"))
            },
            confirmButton = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            store.resetEJ5Type(currentExercise)
                            when (currentExercise) {
                                ExerciseType.R1 -> {
                                    currentR1Articulation = EJ5Articulation.ALL_SLURRED
                                    store.lastR1Articulation = currentR1Articulation
                                }
                                ExerciseType.R5 -> {
                                    currentR5Articulation = EJ5Articulation.ALL_SLURRED
                                    store.lastR5Articulation = currentR5Articulation
                                }
                                else -> {}
                            }
                            store.saveLastSelection()
                            showReichertEJ5CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t(if (currentExercise == ExerciseType.R1) "r1_restart_round" else "r5_restart_round"))
                    }

                    Button(
                        onClick = {
                            scorePlayer.stop()
                            val nextEx = when (currentExercise) {
                                ExerciseType.R1 -> ExerciseType.R2
                                else -> ExerciseType.MODOS
                            }
                            currentExercise = nextEx
                            store.lastExerciseType = nextEx
                            store.saveLastSelection()
                            showReichertEJ5CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(
                            when (currentExercise) {
                                ExerciseType.R1 -> loc.t("r2_title")
                                else -> loc.t("ej4_go_to_modos")
                            }
                        )
                    }

                    TextButton(
                        onClick = { showReichertEJ5CompletionDialog = false },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("stay_mode"))
                    }
                }
            }
        )
    }
```

#### Step 3.4: Route completion triggers in `PracticeScreen.kt`
Lines 2167–2173:
```kotlin
when (currentExercise) {
    ExerciseType.EJ5 -> showEJ5CompletionDialog = true
    ExerciseType.EJ10 -> showEJ10CompletionDialog = true
    ExerciseType.EJ11 -> showEJ11CompletionDialog = true
    ExerciseType.R1, ExerciseType.R5 -> showReichertEJ5CompletionDialog = true
    else -> {}
}
```
Lines 2235–2241:
```kotlin
if (store.isEJ5TypeFullyCompleted(currentExercise)) {
    when (currentExercise) {
        ExerciseType.EJ5 -> showEJ5CompletionDialog = true
        ExerciseType.EJ10 -> showEJ10CompletionDialog = true
        ExerciseType.EJ11 -> showEJ11CompletionDialog = true
        ExerciseType.R1, ExerciseType.R5 -> showReichertEJ5CompletionDialog = true
        else -> {}
    }
}
```

---

### File 4 & 5: Synchronization of `LocalizationManager.kt` and `LocalizationManager.swift`

Add the following 42 entries to the internal string maps:
1. `"ej4_next_section"` -> ES: `"Siguiente Tonalidad"`, EN: `"Next Key"`
2. `"ej5_milestone_title"` -> ES: `"¡E. J. 5 Completado (10/10 Articulaciones)!"`, EN: `"E. J. 5 Completed (10/10 Articulations)!"`
3. `"ej5_milestone_msg"` -> ES: `"Has completado las 10 articulaciones oficiales del Ejercicio Diario N° 5 de Taffanel & Gaubert."`, EN: `"You have completed all 10 official articulations of Taffanel & Gaubert's Daily Exercise No. 5."`
4. `"ej5_restart_round"` -> ES: `"🔁 Reiniciar las 10 Articulaciones"`, EN: `"🔁 Restart 10 Articulations"`
5. `"ej5_ten_arts_completed"` -> ES: `"10 Articulaciones Completadas"`, EN: `"10 Articulations Completed"`
6. `"ej5_go_to_ej10"` -> ES: `"🎵 Ir a E. J. 10 (Arpegios)"`, EN: `"🎵 Go to E. J. 10 (Arpeggios)"`
7. `"ej5_next_section"` -> ES: `"Siguiente Escala (Cromática)"`, EN: `"Next Scale (Chromatic)"`
8. `"ej10_milestone_title"` -> ES: `"¡E. J. 10 Completado (10/10 Articulaciones)!"`, EN: `"E. J. 10 Completed (10/10 Articulations)!"`
9. `"ej10_milestone_msg"` -> ES: `"Has completado las 10 articulaciones oficiales del Ejercicio Diario N° 10 de Taffanel & Gaubert."`, EN: `"You have completed all 10 official articulations of Taffanel & Gaubert's Daily Exercise No. 10."`
10. `"ej10_restart_round"` -> ES: `"🔁 Reiniciar las 10 Articulaciones"`, EN: `"🔁 Restart 10 Articulations"`
11. `"ej10_ten_arts_completed"` -> ES: `"10 Articulaciones Completadas"`, EN: `"10 Articulations Completed"`
12. `"ej10_go_to_ej11"` -> ES: `"🎵 Ir a E. J. 11 (Arpegios Quebrados)"`, EN: `"🎵 Go to E. J. 11 (Broken Arpeggios)"`
13. `"ej10_next_section"` -> ES: `"Siguiente Serie de Arpegios"`, EN: `"Next Arpeggio Series"`
14. `"ej11_milestone_title"` -> ES: `"¡E. J. 11 Completado (10/10 Articulaciones)!"`, EN: `"E. J. 11 Completed (10/10 Articulations)!"`
15. `"ej11_milestone_msg"` -> ES: `"Has completado las 10 articulaciones oficiales del Ejercicio Diario N° 11 de Taffanel & Gaubert."`, EN: `"You have completed all 10 official articulations of Taffanel & Gaubert's Daily Exercise No. 11."`
16. `"ej11_restart_round"` -> ES: `"🔁 Reiniciar las 10 Articulaciones"`, EN: `"🔁 Restart 10 Articulations"`
17. `"ej11_ten_arts_completed"` -> ES: `"10 Articulaciones Completadas"`, EN: `"10 Articulations Completed"`
18. `"ej11_go_to_r1"` -> ES: `"🎵 Ir a Reichert 1 (Op. 5)"`, EN: `"🎵 Go to Reichert 1 (Op. 5)"`
19. `"ej11_next_section"` -> ES: `"Siguiente Serie de Arpegios Quebrados"`, EN: `"Next Broken Arpeggio Series"`
20. `"r1_milestone_title"` -> ES: `"¡Reichert 1 Completado (10/10 Articulaciones)!"`, EN: `"Reichert 1 Completed (10/10 Articulations)!"`
21. `"r1_milestone_msg"` -> ES: `"Has completado las 10 articulaciones de Reichert Nº 1 Op. 5."`, EN: `"You have completed all 10 articulations of Reichert No. 1 Op. 5."`
22. `"r1_restart_round"` -> ES: `"🔁 Reiniciar las 10 Articulaciones"`, EN: `"🔁 Restart 10 Articulations"`
23. `"r1_go_to_r2"` -> ES: `"🎵 Ir a Reichert 2 (Op. 5)"`, EN: `"🎵 Go to Reichert 2 (Op. 5)"`
24. `"r1_next_section"` -> ES: `"Siguiente Tonalidad (6/8)"`, EN: `"Next Key (6/8)"`
25. `"r1_ten_arts_completed"` -> ES: `"10 Articulaciones Completadas"`, EN: `"10 Articulations Completed"`
26. `"r2_milestone_title"` -> ES: `"¡Reichert 2 Completado (8/8 Articulaciones)!"`, EN: `"Reichert 2 Completed (8/8 Articulations)!"`
27. `"r2_milestone_msg"` -> ES: `"Has completado las 8 articulaciones de Reichert Nº 2 Op. 5."`, EN: `"You have completed all 8 articulations of Reichert No. 2 Op. 5."`
28. `"r2_restart_round"` -> ES: `"🔁 Reiniciar las 8 Articulaciones"`, EN: `"🔁 Restart 8 Articulations"`
29. `"r2_go_to_r4"` -> ES: `"🎵 Ir a Reichert 4 (Op. 5)"`, EN: `"🎵 Go to Reichert 4 (Op. 5)"`
30. `"r2_next_section"` -> ES: `"Siguiente Tonalidad (2/4)"`, EN: `"Next Key (2/4)"`
31. `"r2_eight_arts_completed"` -> ES: `"8 Articulaciones Completadas"`, EN: `"8 Articulations Completed"`
32. `"r4_milestone_title"` -> ES: `"¡Reichert 4 Completado (8/8 Articulaciones)!"`, EN: `"Reichert 4 Completed (8/8 Articulations)!"`
33. `"r4_milestone_msg"` -> ES: `"Has completado las 8 articulaciones de Reichert Nº 4 Op. 5."`, EN: `"You have completed all 8 articulations of Reichert No. 4 Op. 5."`
34. `"r4_restart_round"` -> ES: `"🔁 Reiniciar las 8 Articulaciones"`, EN: `"🔁 Restart 8 Articulations"`
35. `"r4_go_to_r5"` -> ES: `"🎵 Ir a Reichert 5 (Op. 5)"`, EN: `"🎵 Go to Reichert 5 (Op. 5)"`
36. `"r4_next_section"` -> ES: `"Siguiente Tonalidad (4/4)"`, EN: `"Next Key (4/4)"`
37. `"r4_eight_arts_completed"` -> ES: `"8 Articulaciones Completadas"`, EN: `"8 Articulations Completed"`
38. `"r5_milestone_title"` -> ES: `"¡Reichert 5 Completado (10/10 Articulaciones)!"`, EN: `"Reichert 5 Completed (10/10 Articulations)!"`
39. `"r5_milestone_msg"` -> ES: `"Has completado las 10 articulaciones de Reichert Nº 5 Op. 5."`, EN: `"You have completed all 10 articulations of Reichert No. 5 Op. 5."`
40. `"r5_restart_round"` -> ES: `"🔁 Reiniciar las 10 Articulaciones"`, EN: `"🔁 Restart 10 Articulations"`
41. `"r5_next_section"` -> ES: `"Siguiente Tonalidad (Tresillos)"`, EN: `"Next Key (Triplets)"`
42. `"r5_ten_arts_completed"` -> ES: `"10 Articulaciones Completadas"`, EN: `"10 Articulations Completed"`

---

## Verification Criteria for Worker Execution

1. **E2E Test Execution**:
   - Run `python3 tests/run_e2e_tests.py --tier 3`
   - Must pass `test_c14_android_reichert_navigation_routes` and `test_c15_android_reichert_completion_dialog_isolation` with 0 failures in Tier 3.
2. **Full E2E Test Suite**:
   - Run `python3 tests/run_e2e_tests.py`
   - Total passed tests should reach 140/141 (99.29%), with 0 defect failures for DEF-09. (The sole remaining failure will be DEF-14 version bump in Tier 4, reserved for M4).
3. **Android Gradle Unit Tests**:
   - Run `./gradlew testDebugUnitTest` in `FluteModesAndroid/`
   - Must exit 0 with all unit tests passing.
4. **Localization Key Parity Script**:
   - Verify that `LocalizationManager.kt` and `LocalizationManager.swift` both have exactly 205 keys with 0 missing or asymmetrical entries.
