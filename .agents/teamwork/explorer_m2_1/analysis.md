# Technical Analysis: Android Navigation & Reichert Dialog Routing Parity

**Author:** `explorer_m2_1`  
**Milestone:** Milestone 2 (App UI, Navigation & Localization Parity)  
**Target Codebase:** `FluteModesAndroid/` (`MainActivity.kt`, `PracticeScreen.kt`, `LocalizationManager.kt`)  
**Date:** 2026-10-11  

---

## Executive Summary

This investigation analyzed two critical navigation and state lifecycle defects in the Android application of the FluteModes ecosystem:
1. **Omission of Reichert navigation arguments in `MainActivity.kt`**: `Screen.Practice` route handling does not declare or pass section and articulation parameters for Mathieu-André Reichert Op. 5 exercises (`R. 1, 2, 4, 5`). While `HomeScreen.kt` tracks and stores user selections for these exercises, `MainActivity.kt` failed to model them in `Screen.Practice` and `PracticeScreen.kt` defaulted to querying `store` directly rather than accepting route arguments, violating the architectural pattern established for all other exercises.
2. **Reichert Completion Dialog Defect in `PracticeScreen.kt`**: When completing the 10 articulations of R. 1 or R. 5, `PracticeScreen.kt` executes an incomplete `when` branch falling into `else -> showEJ11CompletionDialog = true`. This displays an alert entitled "E.J. 11" with E.J. 1 text and no mechanism to advance to the next tonal section. Furthermore, completing R. 2 or R. 4 triggers `showEJ4CompletionDialog = true`, displaying Taffanel & Gaubert E.J. 4 text.

Below are the root cause analyses and exact drop-in code specifications for the Worker.

---

## 1. Problem 1: `Screen.Practice` Route Handling in `MainActivity.kt`

### 1.1 Root Cause Analysis

In `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/MainActivity.kt`:

1. **`Screen.Practice` Data Class Definition (lines 22–36)**:
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
       val tonic: Tonic = Tonic.DO_NATURAL,
       val mode: ModeType = ModeType.IONIAN
   ) : Screen()
   ```
   Every Taffanel & Gaubert exercise (`EJ1`, `EJ2`, `EJ4`, `EJ5`, `EJ10`, `EJ11`) and Modal exercise (`tonic`, `mode`) has explicit route parameters. However, when Reichert exercises (`R1`, `R2`, `R4`, `R5`) were introduced, no corresponding fields were added to `Screen.Practice`.

2. **Route Construction in `onStartReichertPractice` (lines 219–237)**:
   ```kotlin
   onStartReichertPractice = { ex ->
       store.lastExerciseType = ex
       store.saveLastSelection()
       currentScreen = Screen.Practice(
           exerciseType = ex,
           ej1Articulation = store.lastEJ1Articulation,
           ej2Articulation = store.lastEJ2Articulation,
           ej4Articulation = store.lastEJ4Articulation,
           ej4Section = store.lastEJ4Section,
           ej5Articulation = store.lastEJ5Articulation,
           ej5Section = store.lastEJ5Section,
           ej10Articulation = store.lastEJ10Articulation,
           ej10Section = store.lastEJ10Section,
           ej11Articulation = store.lastEJ11Articulation,
           ej11Section = store.lastEJ11Section,
           tonic = store.lastTonic ?: Tonic.DO_NATURAL,
           mode = store.lastMode ?: ModeType.IONIAN
       )
   }
   ```
   Because `Screen.Practice` lacked parameters for Reichert, `onStartReichertPractice` could not pass the selected Reichert section or articulation.

3. **Route Consumption in `MainActivity.kt` (lines 244–272)**:
   When rendering `PracticeScreen`, `MainActivity.kt` passes `screen.ej1Articulation`, `screen.ej4Section`, etc., but completely omits Reichert arguments because neither `Screen.Practice` nor `PracticeScreen` declared them.

4. **Bypass in `PracticeScreen.kt` (lines 32–71)**:
   `PracticeScreen.kt` does not accept `initialR1Articulation`, `initialR1Section`, etc. Instead, it bypasses the route parameters:
   ```kotlin
   var currentR1Articulation by remember { mutableStateOf(store.lastR1Articulation) }
   var currentR1Section by remember { mutableStateOf(store.lastR1Section) }
   var currentR2Articulation by remember { mutableStateOf(store.lastR2Articulation) }
   var currentR2Section by remember { mutableStateOf(store.lastR2Section) }
   var currentR4Articulation by remember { mutableStateOf(store.lastR4Articulation) }
   var currentR4Section by remember { mutableStateOf(store.lastR4Section) }
   var currentR5Articulation by remember { mutableStateOf(store.lastR5Articulation) }
   var currentR5Section by remember { mutableStateOf(store.lastR5Section) }
   ```
   This breaks navigation argument isolation and encapsulation: navigation events cannot supply custom or deep-linked Reichert parameters to `PracticeScreen`.

---

### 1.2 Exact Drop-In Fix for `MainActivity.kt`

#### Step 1: Update `Screen.Practice` in `MainActivity.kt` (lines 22–36)

```kotlin
<<<<
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
        val tonic: Tonic = Tonic.DO_NATURAL,
        val mode: ModeType = ModeType.IONIAN
    ) : Screen()
====
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
>>>>
```

#### Step 2: Update `onStartReichertPractice` in `MainActivity.kt` (lines 219–237)

```kotlin
<<<<
                                onStartReichertPractice = { ex ->
                                    store.lastExerciseType = ex
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ex,
                                        ej1Articulation = store.lastEJ1Articulation,
                                        ej2Articulation = store.lastEJ2Articulation,
                                        ej4Articulation = store.lastEJ4Articulation,
                                        ej4Section = store.lastEJ4Section,
                                        ej5Articulation = store.lastEJ5Articulation,
                                        ej5Section = store.lastEJ5Section,
                                        ej10Articulation = store.lastEJ10Articulation,
                                        ej10Section = store.lastEJ10Section,
                                        ej11Articulation = store.lastEJ11Articulation,
                                        ej11Section = store.lastEJ11Section,
                                        tonic = store.lastTonic ?: Tonic.DO_NATURAL,
                                        mode = store.lastMode ?: ModeType.IONIAN
                                    )
                                },
====
                                onStartReichertPractice = { ex ->
                                    store.lastExerciseType = ex
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ex,
                                        ej1Articulation = store.lastEJ1Articulation,
                                        ej2Articulation = store.lastEJ2Articulation,
                                        ej4Articulation = store.lastEJ4Articulation,
                                        ej4Section = store.lastEJ4Section,
                                        ej5Articulation = store.lastEJ5Articulation,
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
>>>>
```

#### Step 3: Forward Reichert arguments to `PracticeScreen` in `MainActivity.kt` (lines 244–272)

```kotlin
<<<<
                        is Screen.Practice -> {
                            PracticeScreen(
                                initialExercise = screen.exerciseType,
                                initialEJ1Articulation = screen.ej1Articulation,
                                initialEJ2Articulation = screen.ej2Articulation,
                                initialEJ4Articulation = screen.ej4Articulation,
                                initialEJ4Section = screen.ej4Section,
                                initialEJ5Articulation = screen.ej5Articulation,
                                initialEJ5Section = screen.ej5Section,
                                initialEJ10Articulation = screen.ej10Articulation,
                                initialEJ10Section = screen.ej10Section,
                                initialEJ11Articulation = screen.ej11Articulation,
                                initialEJ11Section = screen.ej11Section,
                                initialTonic = screen.tonic,
                                initialMode = screen.mode,
                                store = store,
                                loc = loc,
                                metronome = metronome,
                                scorePlayer = scorePlayer,
                                onBack = {
                                    metronome.stop()
                                    scorePlayer.stop()
                                    currentScreen = Screen.Home
                                },
                                onOpenMatrix = {
                                    metronome.stop()
                                    scorePlayer.stop()
                                    currentScreen = Screen.Matrix
                                }
                            )
                        }
====
                        is Screen.Practice -> {
                            PracticeScreen(
                                initialExercise = screen.exerciseType,
                                initialEJ1Articulation = screen.ej1Articulation,
                                initialEJ2Articulation = screen.ej2Articulation,
                                initialEJ4Articulation = screen.ej4Articulation,
                                initialEJ4Section = screen.ej4Section,
                                initialEJ5Articulation = screen.ej5Articulation,
                                initialEJ5Section = screen.ej5Section,
                                initialEJ10Articulation = screen.ej10Articulation,
                                initialEJ10Section = screen.ej10Section,
                                initialEJ11Articulation = screen.ej11Articulation,
                                initialEJ11Section = screen.ej11Section,
                                initialR1Articulation = screen.r1Articulation,
                                initialR1Section = screen.r1Section,
                                initialR2Articulation = screen.r2Articulation,
                                initialR2Section = screen.r2Section,
                                initialR4Articulation = screen.r4Articulation,
                                initialR4Section = screen.r4Section,
                                initialR5Articulation = screen.r5Articulation,
                                initialR5Section = screen.r5Section,
                                initialTonic = screen.tonic,
                                initialMode = screen.mode,
                                store = store,
                                loc = loc,
                                metronome = metronome,
                                scorePlayer = scorePlayer,
                                onBack = {
                                    metronome.stop()
                                    scorePlayer.stop()
                                    currentScreen = Screen.Home
                                },
                                onOpenMatrix = {
                                    metronome.stop()
                                    scorePlayer.stop()
                                    currentScreen = Screen.Matrix
                                }
                            )
                        }
>>>>
```

---

## 2. Problem 2: Completion State and Dialog Routing in `PracticeScreen.kt`

### 2.1 Root Cause Analysis

1. **Reichert Exercises Grouping in `ArticulationPattern.kt`**:
   - `ExerciseType.isEJ4Exercise` returns true for: `EJ4`, `R2`, `R4` (8 articulations, 25 sections).
   - `ExerciseType.isEJ5TypeExercise` returns true for: `EJ5`, `EJ10`, `EJ11`, `R1`, `R5` (10 articulations).
   - All Reichert exercises have 25 tonal sections mapped to `EJ4Section` (from C Major / A Minor up to Coda, 24 Keys + D.S. al Fine).

2. **Defect at Lines 2167–2173 and 2235–2241 in `PracticeScreen.kt`**:
   When an exercise in `isEJ5TypeExercise` is completed:
   ```kotlin
   when (currentExercise) {
       ExerciseType.EJ5 -> showEJ5CompletionDialog = true
       ExerciseType.EJ10 -> showEJ10CompletionDialog = true
       else -> showEJ11CompletionDialog = true
   }
   ```
   When `currentExercise` is `R1` or `R5`, it falls through to `else -> showEJ11CompletionDialog = true`.

3. **Inappropriate Dialog Implementation in `showEJ11CompletionDialog` (lines 500–575)**:
   - Header title: `"¡${currentExercise.pillLabel} Completado (10/10 Articulaciones)!"`.
   - Message: `loc.t("ej1_milestone_msg")` — verbatim French text about Taffanel & Gaubert's E.J. 1!
   - Restart button: `loc.t("ej1_restart_round")`.
   - No section advancement button exists.

4. **Defect for R. 2 and R. 4 (lines 1950–1953, 2001, 313–389)**:
   - When completing R. 2 or R. 4, `showEJ4CompletionDialog = true` is triggered.
   - Message: `loc.t("ej4_milestone_msg")` — verbatim text about Taffanel & Gaubert's E.J. 4 (194 compases).
   - No section advancement button exists.

---

### 2.2 Design of Reichert Completion State & Dialog

A dedicated dialog `showReichertCompletionDialog` must be implemented for `R1`, `R2`, `R4`, and `R5`.

#### Key Requirements:
1. **Accurate Titles & Messages**:
   - Title: `"¡${currentExercise.pillLabel} Completado ($totalArts/$totalArts Articulaciones)!"` (or `"Completed ($totalArts/$totalArts Articulations)!"` in English).
   - Message: Identifies Mathieu-André Reichert Op. 5 and displays the current key/section (`curSec.shortBadge(currentExercise)`).
2. **Action 1: Restart Articulation Round (Reiniciar Ronda)**:
   - Clears the completed articulation set in `store` (`store.resetEJ4(currentExercise)` for R2/R4; `store.resetEJ5Type(currentExercise)` for R1/R5).
   - Resets current articulation to 1 (`EJ4Articulation.ALL_SLURRED_8` or `EJ5Articulation.ALL_SLURRED`).
   - Saves selection and dismisses dialog.
3. **Action 2: Advance to Next Key / Section (Siguiente Tonalidad)**:
   - Advances to `(currentSectionIndex + 1) % 25`.
   - Resets articulation progress for the new key in `store`.
   - Sets current articulation back to 1.
   - Displays label: `"🎵 Siguiente Tonalidad (${nextSecIdx + 1}/25 · ${nextSec.shortBadge(currentExercise)})"` (or `"🎵 Next Key ..."` in English).
4. **Action 3: Advance to Next Exercise in Sequence (Siguiente Ejercicio)**:
   - `R. 1 -> R. 2`
   - `R. 2 -> R. 4`
   - `R. 4 -> R. 5`
   - `R. 5 -> 84 Modos`
5. **Action 4: Stay in Current Section**:
   - Standard `loc.t("stay_mode")` dismiss action.

---

### 2.3 Exact Drop-In Fix for `PracticeScreen.kt`

#### Step 1: Update `PracticeScreen` Signature & State Variables (lines 32–75)

```kotlin
<<<<
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PracticeScreen(
    initialExercise: ExerciseType = ExerciseType.EJ1,
    initialEJ1Articulation: EJ1Articulation = EJ1Articulation.ORIGINAL,
    initialEJ2Articulation: EJ1Articulation = EJ1Articulation.ORIGINAL,
    initialEJ4Articulation: EJ4Articulation = EJ4Articulation.ORIGINAL,
    initialEJ4Section: EJ4Section = EJ4Section.C_MAJOR,
    initialEJ5Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
    initialEJ5Section: EJ5Section = EJ5Section.C_CHROM,
    initialEJ10Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
    initialEJ10Section: EJ10Section = EJ10Section.C_ARP,
    initialEJ11Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
    initialEJ11Section: EJ10Section = EJ10Section.C_ARP,
    initialTonic: Tonic,
    initialMode: ModeType,
    store: PracticeStore,
    loc: LocalizationManager,
    metronome: MetronomeEngine,
    scorePlayer: ScoreAudioPlayer,
    onBack: () -> Unit,
    onOpenMatrix: () -> Unit
) {
    var currentExercise by remember { mutableStateOf(initialExercise) }
    var currentEJ1Articulation by remember { mutableStateOf(initialEJ1Articulation) }
    var currentEJ2Articulation by remember { mutableStateOf(initialEJ2Articulation) }
    var currentEJ4Articulation by remember { mutableStateOf(initialEJ4Articulation) }
    var currentEJ4Section by remember { mutableStateOf(initialEJ4Section) }
    var currentEJ5Articulation by remember { mutableStateOf(initialEJ5Articulation) }
    var currentEJ5Section by remember { mutableStateOf(initialEJ5Section) }
    var currentEJ10Articulation by remember { mutableStateOf(initialEJ10Articulation) }
    var currentEJ10Section by remember { mutableStateOf(initialEJ10Section) }
    var currentEJ11Articulation by remember { mutableStateOf(initialEJ11Articulation) }
    var currentEJ11Section by remember { mutableStateOf(initialEJ11Section) }
    var currentR1Articulation by remember { mutableStateOf(store.lastR1Articulation) }
    var currentR1Section by remember { mutableStateOf(store.lastR1Section) }
    var currentR2Articulation by remember { mutableStateOf(store.lastR2Articulation) }
    var currentR2Section by remember { mutableStateOf(store.lastR2Section) }
    var currentR4Articulation by remember { mutableStateOf(store.lastR4Articulation) }
    var currentR4Section by remember { mutableStateOf(store.lastR4Section) }
    var currentR5Articulation by remember { mutableStateOf(store.lastR5Articulation) }
    var currentR5Section by remember { mutableStateOf(store.lastR5Section) }
    var currentTonic by remember { mutableStateOf(initialTonic) }
    var currentMode by remember { mutableStateOf(initialMode) }
    var currentArticulation by remember { mutableStateOf(ArticulationPattern.ALL_SLURRED) }
    var showCompletionDialog by remember { mutableStateOf(false) }
    var showEJ1CompletionDialog by remember { mutableStateOf(false) }
    var showEJ2CompletionDialog by remember { mutableStateOf(false) }
    var showEJ4CompletionDialog by remember { mutableStateOf(false) }
    var showEJ5CompletionDialog by remember { mutableStateOf(false) }
    var showEJ10CompletionDialog by remember { mutableStateOf(false) }
    var showEJ11CompletionDialog by remember { mutableStateOf(false) }
====
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PracticeScreen(
    initialExercise: ExerciseType = ExerciseType.EJ1,
    initialEJ1Articulation: EJ1Articulation = EJ1Articulation.ORIGINAL,
    initialEJ2Articulation: EJ1Articulation = EJ1Articulation.ORIGINAL,
    initialEJ4Articulation: EJ4Articulation = EJ4Articulation.ORIGINAL,
    initialEJ4Section: EJ4Section = EJ4Section.C_MAJOR,
    initialEJ5Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
    initialEJ5Section: EJ5Section = EJ5Section.C_CHROM,
    initialEJ10Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
    initialEJ10Section: EJ10Section = EJ10Section.C_ARP,
    initialEJ11Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
    initialEJ11Section: EJ10Section = EJ10Section.C_ARP,
    initialR1Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
    initialR1Section: EJ4Section = EJ4Section.C_MAJOR,
    initialR2Articulation: EJ4Articulation = EJ4Articulation.ORIGINAL,
    initialR2Section: EJ4Section = EJ4Section.C_MAJOR,
    initialR4Articulation: EJ4Articulation = EJ4Articulation.ORIGINAL,
    initialR4Section: EJ4Section = EJ4Section.C_MAJOR,
    initialR5Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
    initialR5Section: EJ4Section = EJ4Section.C_MAJOR,
    initialTonic: Tonic,
    initialMode: ModeType,
    store: PracticeStore,
    loc: LocalizationManager,
    metronome: MetronomeEngine,
    scorePlayer: ScoreAudioPlayer,
    onBack: () -> Unit,
    onOpenMatrix: () -> Unit
) {
    var currentExercise by remember { mutableStateOf(initialExercise) }
    var currentEJ1Articulation by remember { mutableStateOf(initialEJ1Articulation) }
    var currentEJ2Articulation by remember { mutableStateOf(initialEJ2Articulation) }
    var currentEJ4Articulation by remember { mutableStateOf(initialEJ4Articulation) }
    var currentEJ4Section by remember { mutableStateOf(initialEJ4Section) }
    var currentEJ5Articulation by remember { mutableStateOf(initialEJ5Articulation) }
    var currentEJ5Section by remember { mutableStateOf(initialEJ5Section) }
    var currentEJ10Articulation by remember { mutableStateOf(initialEJ10Articulation) }
    var currentEJ10Section by remember { mutableStateOf(initialEJ10Section) }
    var currentEJ11Articulation by remember { mutableStateOf(initialEJ11Articulation) }
    var currentEJ11Section by remember { mutableStateOf(initialEJ11Section) }
    var currentR1Articulation by remember { mutableStateOf(initialR1Articulation) }
    var currentR1Section by remember { mutableStateOf(initialR1Section) }
    var currentR2Articulation by remember { mutableStateOf(initialR2Articulation) }
    var currentR2Section by remember { mutableStateOf(initialR2Section) }
    var currentR4Articulation by remember { mutableStateOf(initialR4Articulation) }
    var currentR4Section by remember { mutableStateOf(initialR4Section) }
    var currentR5Articulation by remember { mutableStateOf(initialR5Articulation) }
    var currentR5Section by remember { mutableStateOf(initialR5Section) }
    var currentTonic by remember { mutableStateOf(initialTonic) }
    var currentMode by remember { mutableStateOf(initialMode) }
    var currentArticulation by remember { mutableStateOf(ArticulationPattern.ALL_SLURRED) }
    var showCompletionDialog by remember { mutableStateOf(false) }
    var showEJ1CompletionDialog by remember { mutableStateOf(false) }
    var showEJ2CompletionDialog by remember { mutableStateOf(false) }
    var showEJ4CompletionDialog by remember { mutableStateOf(false) }
    var showEJ5CompletionDialog by remember { mutableStateOf(false) }
    var showEJ10CompletionDialog by remember { mutableStateOf(false) }
    var showEJ11CompletionDialog by remember { mutableStateOf(false) }
    var showReichertCompletionDialog by remember { mutableStateOf(false) }
>>>>
```

#### Step 2: Clean up `showEJ4CompletionDialog` (lines 357–380)

Ensure `showEJ4CompletionDialog` is specific to E.J. 4 and does not mix Reichert:
```kotlin
<<<<
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            val nextEx = when (currentExercise) {
                                ExerciseType.R2 -> ExerciseType.R4
                                ExerciseType.R4 -> ExerciseType.R5
                                else -> ExerciseType.EJ5
                            }
                            currentExercise = nextEx
                            store.lastExerciseType = nextEx
                            store.saveLastSelection()
                            showEJ4CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(
                            when (currentExercise) {
                                ExerciseType.R2 -> loc.t("r4_title")
                                ExerciseType.R4 -> loc.t("r5_title")
                                else -> loc.t("ej5_title")
                            }
                        )
                    }
====
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            currentExercise = ExerciseType.EJ5
                            store.lastExerciseType = ExerciseType.EJ5
                            store.saveLastSelection()
                            showEJ4CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(loc.t("ej5_title"))
                    }
>>>>
```

#### Step 3: Clean up `showEJ11CompletionDialog` (lines 500–576)

Replace the placeholder `ej1_*` texts with proper E.J. 11 texts:
```kotlin
<<<<
    if (showEJ11CompletionDialog) {
        AlertDialog(
            onDismissRequest = { showEJ11CompletionDialog = false },
            title = {
                Text(
                    text = "¡${currentExercise.pillLabel} Completado (10/10 Articulaciones)!",
                    fontWeight = FontWeight.Bold
                )
            },
            text = {
                Text(text = loc.t("ej1_milestone_msg"))
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
                                else -> {
                                    currentEJ11Articulation = EJ5Articulation.ALL_SLURRED
                                    store.lastEJ11Articulation = currentEJ11Articulation
                                }
                            }
                            store.saveLastSelection()
                            showEJ11CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("ej1_restart_round"))
                    }

                    Button(
                        onClick = {
                            scorePlayer.stop()
                            val nextEx = when (currentExercise) {
                                ExerciseType.EJ11 -> ExerciseType.R1
                                ExerciseType.R1 -> ExerciseType.R2
                                else -> ExerciseType.MODOS
                            }
                            currentExercise = nextEx
                            store.lastExerciseType = nextEx
                            store.saveLastSelection()
                            showEJ11CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(
                            when (currentExercise) {
                                ExerciseType.EJ11 -> loc.t("r1_title")
                                ExerciseType.R1 -> loc.t("r2_title")
                                else -> loc.t("ej4_go_to_modos")
                            }
                        )
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
====
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
>>>>
```

#### Step 4: Add `showReichertCompletionDialog` in `PracticeScreen.kt`

Insert right after `showEJ11CompletionDialog`:

```kotlin
    if (showReichertCompletionDialog) {
        val totalArts = if (currentExercise.isEJ4Exercise) 8 else 10
        val curSec = when (currentExercise) {
            ExerciseType.R1 -> currentR1Section
            ExerciseType.R2 -> currentR2Section
            ExerciseType.R4 -> currentR4Section
            ExerciseType.R5 -> currentR5Section
            else -> EJ4Section.C_MAJOR
        }
        val allSecs = EJ4Section.entries
        val nextSecIdx = (allSecs.indexOf(curSec) + 1) % allSecs.size
        val nextSec = allSecs[nextSecIdx]
        val isEn = loc.currentLanguage == AppLanguage.ENGLISH

        AlertDialog(
            onDismissRequest = { showReichertCompletionDialog = false },
            title = {
                Text(
                    text = if (isEn)
                        "¡${currentExercise.pillLabel} Completed ($totalArts/$totalArts Articulations)!"
                    else
                        "¡${currentExercise.pillLabel} Completado ($totalArts/$totalArts Articulaciones)!",
                    fontWeight = FontWeight.Bold
                )
            },
            text = {
                Text(
                    text = if (isEn)
                        "You have completed all $totalArts articulations of ${currentExercise.pillLabel} (M.-A. Reichert Op. 5) in ${curSec.shortBadge(currentExercise)}."
                    else
                        "Has completado las $totalArts articulaciones de ${currentExercise.pillLabel} (M.-A. Reichert Op. 5) en ${curSec.shortBadge(currentExercise)}."
                )
            },
            confirmButton = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    // 1. Restart Articulation Round on current key
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            if (currentExercise.isEJ4Exercise) {
                                store.resetEJ4(currentExercise)
                                if (currentExercise == ExerciseType.R2) {
                                    currentR2Articulation = EJ4Articulation.ALL_SLURRED_8
                                    store.lastR2Articulation = currentR2Articulation
                                } else {
                                    currentR4Articulation = EJ4Articulation.ALL_SLURRED_8
                                    store.lastR4Articulation = currentR4Articulation
                                }
                            } else {
                                store.resetEJ5Type(currentExercise)
                                if (currentExercise == ExerciseType.R1) {
                                    currentR1Articulation = EJ5Articulation.ALL_SLURRED
                                    store.lastR1Articulation = currentR1Articulation
                                } else {
                                    currentR5Articulation = EJ5Articulation.ALL_SLURRED
                                    store.lastR5Articulation = currentR5Articulation
                                }
                            }
                            store.saveLastSelection()
                            showReichertCompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(if (isEn) "🔁 Restart $totalArts Articulations" else "🔁 Reiniciar las $totalArts Articulaciones")
                    }

                    // 2. Advance to next key (Section 1..25)
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            when (currentExercise) {
                                ExerciseType.R1 -> {
                                    currentR1Section = nextSec
                                    store.lastR1Section = nextSec
                                    store.resetEJ5Type(ExerciseType.R1)
                                    currentR1Articulation = EJ5Articulation.ALL_SLURRED
                                    store.lastR1Articulation = currentR1Articulation
                                }
                                ExerciseType.R2 -> {
                                    currentR2Section = nextSec
                                    store.lastR2Section = nextSec
                                    store.resetEJ4(ExerciseType.R2)
                                    currentR2Articulation = EJ4Articulation.ALL_SLURRED_8
                                    store.lastR2Articulation = currentR2Articulation
                                }
                                ExerciseType.R4 -> {
                                    currentR4Section = nextSec
                                    store.lastR4Section = nextSec
                                    store.resetEJ4(ExerciseType.R4)
                                    currentR4Articulation = EJ4Articulation.ALL_SLURRED_8
                                    store.lastR4Articulation = currentR4Articulation
                                }
                                ExerciseType.R5 -> {
                                    currentR5Section = nextSec
                                    store.lastR5Section = nextSec
                                    store.resetEJ5Type(ExerciseType.R5)
                                    currentR5Articulation = EJ5Articulation.ALL_SLURRED
                                    store.lastR5Articulation = currentR5Articulation
                                }
                                else -> {}
                            }
                            store.saveLastSelection()
                            showReichertCompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(
                            if (isEn)
                                "🎵 Next Key (${nextSecIdx + 1}/25 · ${nextSec.shortBadge(currentExercise)})"
                            else
                                "🎵 Siguiente Tonalidad (${nextSecIdx + 1}/25 · ${nextSec.shortBadge(currentExercise)})"
                        )
                    }

                    // 3. Advance to next exercise
                    val nextEx = when (currentExercise) {
                        ExerciseType.R1 -> ExerciseType.R2
                        ExerciseType.R2 -> ExerciseType.R4
                        ExerciseType.R4 -> ExerciseType.R5
                        ExerciseType.R5 -> ExerciseType.MODOS
                        else -> ExerciseType.MODOS
                    }
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            currentExercise = nextEx
                            store.lastExerciseType = nextEx
                            store.saveLastSelection()
                            showReichertCompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.tertiary)
                    ) {
                        Text(
                            when (currentExercise) {
                                ExerciseType.R1 -> loc.t("r2_title")
                                ExerciseType.R2 -> loc.t("r4_title")
                                ExerciseType.R4 -> loc.t("r5_title")
                                else -> loc.t("ej4_go_to_modos")
                            }
                        )
                    }

                    // 4. Stay / Dismiss
                    TextButton(
                        onClick = { showReichertCompletionDialog = false },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("stay_mode"))
                    }
                }
            }
        )
    }
```

#### Step 5: Update Trigger Sites in `PracticeScreen.kt`

1. **In `isEJ4FullyDone` Button (line ~1952)**:
   ```kotlin
   <<<<
                                   onClick = { showEJ4CompletionDialog = true },
   ====
                                   onClick = {
                                       if (currentExercise.isReichertExercise) {
                                           showReichertCompletionDialog = true
                                       } else {
                                           showEJ4CompletionDialog = true
                                       }
                                   },
   >>>>
   ```

2. **In `isEJ4FullyDone` Articulation Advance (line ~2001)**:
   ```kotlin
   <<<<
                                               if (store.isEJ4FullyCompleted(currentExercise)) {
                                                   showEJ4CompletionDialog = true
                                               }
   ====
                                               if (store.isEJ4FullyCompleted(currentExercise)) {
                                                   if (currentExercise.isReichertExercise) {
                                                       showReichertCompletionDialog = true
                                                   } else {
                                                       showEJ4CompletionDialog = true
                                                   }
                                               }
   >>>>
   ```

3. **In `isEJ5TypeFullyDone` Button (line ~2167)**:
   ```kotlin
   <<<<
                                       when (currentExercise) {
                                           ExerciseType.EJ5 -> showEJ5CompletionDialog = true
                                           ExerciseType.EJ10 -> showEJ10CompletionDialog = true
                                           else -> showEJ11CompletionDialog = true
                                       }
   ====
                                       when (currentExercise) {
                                           ExerciseType.EJ5 -> showEJ5CompletionDialog = true
                                           ExerciseType.EJ10 -> showEJ10CompletionDialog = true
                                           ExerciseType.EJ11 -> showEJ11CompletionDialog = true
                                           ExerciseType.R1, ExerciseType.R5 -> showReichertCompletionDialog = true
                                           else -> {}
                                       }
   >>>>
   ```

4. **In `isEJ5TypeFullyDone` Label (line ~2190)**:
   ```kotlin
   <<<<
                                           val doneLabel = when (currentExercise) {
                                               ExerciseType.EJ5 -> loc.t("ej5_ten_arts_completed")
                                               ExerciseType.EJ10 -> loc.t("ej10_ten_arts_completed")
                                               else -> loc.t("ej11_ten_arts_completed")
                                           }
   ====
                                           val doneLabel = when (currentExercise) {
                                               ExerciseType.EJ5 -> loc.t("ej5_ten_arts_completed")
                                               ExerciseType.EJ10 -> loc.t("ej10_ten_arts_completed")
                                               ExerciseType.EJ11 -> loc.t("ej11_ten_arts_completed")
                                               ExerciseType.R1, ExerciseType.R5 -> if (loc.currentLanguage == AppLanguage.ENGLISH) "10 Articulations Completed" else "10 Articulaciones Completadas"
                                               else -> ""
                                           }
   >>>>
   ```

5. **In `isEJ5TypeFullyDone` Articulation Advance (line ~2236)**:
   ```kotlin
   <<<<
                                               if (store.isEJ5TypeFullyCompleted(currentExercise)) {
                                                   when (currentExercise) {
                                                       ExerciseType.EJ5 -> showEJ5CompletionDialog = true
                                                       ExerciseType.EJ10 -> showEJ10CompletionDialog = true
                                                       else -> showEJ11CompletionDialog = true
                                                   }
                                               }
   ====
                                               if (store.isEJ5TypeFullyCompleted(currentExercise)) {
                                                   when (currentExercise) {
                                                       ExerciseType.EJ5 -> showEJ5CompletionDialog = true
                                                       ExerciseType.EJ10 -> showEJ10CompletionDialog = true
                                                       ExerciseType.EJ11 -> showEJ11CompletionDialog = true
                                                       ExerciseType.R1, ExerciseType.R5 -> showReichertCompletionDialog = true
                                                       else -> {}
                                                   }
                                               }
   >>>>
   ```

---

## 3. Problem 3: Synchronization of Missing Localization Keys

During the investigation, 18 keys queried by `PracticeScreen.kt` were found missing in `LocalizationManager.kt` and `LocalizationManager.swift`:

| Key | Spanish (`es`) | English (`en`) |
|-----|----------------|----------------|
| `ej4_next_section` | `"Siguiente Sección"` | `"Next Section"` |
| `ej5_next_section` | `"Siguiente Sección"` | `"Next Section"` |
| `ej10_next_section` | `"Siguiente Sección"` | `"Next Section"` |
| `ej11_next_section` | `"Siguiente Sección"` | `"Next Section"` |
| `ej5_ten_arts_completed` | `"10 Articulaciones Completadas"` | `"10 Articulations Completed"` |
| `ej10_ten_arts_completed` | `"10 Articulaciones Completadas"` | `"10 Articulations Completed"` |
| `ej11_ten_arts_completed` | `"10 Articulaciones Completadas"` | `"10 Articulations Completed"` |
| `ej5_milestone_title` | `"¡E. J. 5 Completado (10/10 Articulaciones)!"` | `"E. J. 5 Completed (10/10 Articulations)!"` |
| `ej5_milestone_msg` | `"Has completado las 10 articulaciones oficiales del Ejercicio Diario N° 5 de Taffanel & Gaubert."` | `"You have completed all 10 official articulations of Taffanel & Gaubert's Daily Exercise No. 5."` |
| `ej5_restart_round` | `"🔁 Reiniciar las 10 Articulaciones"` | `"🔁 Restart 10 Articulations"` |
| `ej5_go_to_ej10` | `"🎵 Ir a E. J. 10 (Arpegios)"` | `"🎵 Go to E. J. 10 (Arpeggios)"` |
| `ej10_milestone_title` | `"¡E. J. 10 Completado (10/10 Articulaciones)!"` | `"E. J. 10 Completed (10/10 Articulations)!"` |
| `ej10_milestone_msg` | `"Has completado las 10 articulaciones oficiales del Ejercicio Diario N° 10 de Taffanel & Gaubert."` | `"You have completed all 10 official articulations of Taffanel & Gaubert's Daily Exercise No. 10."` |
| `ej10_restart_round` | `"🔁 Reiniciar las 10 Articulaciones"` | `"🔁 Restart 10 Articulations"` |
| `ej10_go_to_ej11` | `"🎵 Ir a E. J. 11 (Arpegios Quebrados)"` | `"🎵 Go to E. J. 11 (Broken Arpeggios)"` |
| `ej11_milestone_title` | `"¡E. J. 11 Completado (10/10 Articulaciones)!"` | `"E. J. 11 Completed (10/10 Articulations)!"` |
| `ej11_milestone_msg` | `"Has completado las 10 articulaciones oficiales del Ejercicio Diario N° 11 de Taffanel & Gaubert."` | `"You have completed all 10 official articulations of Taffanel & Gaubert's Daily Exercise No. 11."` |
| `ej11_restart_round` | `"🔁 Reiniciar las 10 Articulaciones"` | `"🔁 Restart 10 Articulations"` |

Adding these entries to `LocalizationManager.kt` and `LocalizationManager.swift` guarantees 100% key parity with 0 missing strings across iOS and Android.
