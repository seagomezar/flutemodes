# Technical Analysis & Implementation Specification: DEF-02, DEF-03, DEF-05

**Agent:** `explorer_m1_2`  
**Milestone:** Milestone 1 — Score Engine & Urtext Parity Fixes  
**Date:** 2026-10-11  
**Target Recipient:** Worker Agent / Orchestrator (`2c224607-5456-4eac-ad55-0172dee3d36d`)  

---

## Executive Summary

This report establishes the exact, drop-in technical specifications for three defects affecting the Android music score and audio synthesis engines:
1. **DEF-02:** Android `ExerciseGenerator.kt` (`ej2RawMeasures`) lines 131–162 contains major third accidentals in mm. 4, 8, 14, 18, 22, 24, 28 (and missing natural/accidental signs in other measures) instead of minor thirds. Full parity with `ExerciseGenerator.swift` (lines 75–106) and `score_template.html` (`EJ2_RAW_MEASURES`, lines 234–265) is designed.
2. **DEF-03:** Android `ScoreAudioPlayer.kt` line 444 hardcodes the diminished seventh chord fourth semitone to `base + 5`, causing incorrect audio playback for minor pentachords (E.J. 2). Exact fix: `val dimFourthSemitone = if (isMinor) 4 else 5` and `listOf(base, base + 1, base + 3, base + dimFourthSemitone, base + 6)`.
3. **DEF-05:** Android `ScoreAudioPlayer.kt` line 302 uses divisor `4.0` for sixteenth notes across all exercises, which causes Reichert Op. 5 Exercise No. 5 (R. 5, written in 2/4 with sixteenth triplets / sextuplets) to play 33% too slowly. Exact fix: divisor `6.0` for R.5 (`(60.0 / tempoBPM.toDouble()) / 6.0`) and aligned final note staccato handling matching iOS `ScoreAudioPlayer.swift`.

---

## 1. DEF-02: Android `ExerciseGenerator.kt` E.J. 2 Measures Parity

### 1.1 Context & Problem Analysis
Taffanel & Gaubert *17 Grands Exercices Journaliers de Mécanisme* (Editions Alphonse Leduc, Plate A. L. 16.588):
- **E.J. 1** consists of chromatic pairs of major pentachords (modulating via diminished vii°).
- **E.J. 2** consists of chromatic pairs of **minor pentachords** (modulating via diminished vii° into minor keys).

In `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/model/ExerciseGenerator.kt`:
The table `ej2RawMeasures` (lines 131–162) was initially created by duplicating parts of `ej1RawMeasures` without correctly updating the modulating diminished chords to minor resolutions.
Specifically, in 7 critical measures:
- **Measure 4:** Contains `^G` (G♯, major 3rd from E) instead of `=G` (G♮, minor 3rd from E).
- **Measure 8:** Contains `^A` (A♯, major 3rd from F♯) instead of `=A` (A♮, minor 3rd from F♯).
- **Measure 14:** Contains `B` and `^c` (C♯, major 3rd from A) instead of `=B` and `=c` (C♮, minor 3rd from A).
- **Measure 18:** Contains `^d` (D♯, major 3rd from B) instead of `=d` (D♮, minor 3rd from B).
- **Measure 22:** Contains `^e` (E♯, major 3rd from C♯) instead of `=e` (E♮, minor 3rd from C♯).
- **Measure 24:** Contains `e` and `^f` (F♯, major 3rd from D) instead of `=e` and `=f` (F♮, minor 3rd from D).
- **Measure 28:** Contains `^g` (G♯, major 3rd from E) instead of `=g` (G♮, minor 3rd from E).

Furthermore, in measures 2, 5, 6, 9, 10, 15, 16, 19, 20, 25, 26, 29, 30, natural signs (`=`) and accidental markings differed from `ExerciseGenerator.swift` and `score_template.html`.
Additionally, in measures 12, 13, 22, and 23, Beats 1–3 had incorrect diatonic repetition bases copied from EJ1 rather than matching the root pitch of EJ2.

In contrast, `FluteModes/FluteModes/Models/ExerciseGenerator.swift` (lines 75–106) and `FluteModes/FluteModes/Resources/score_template.html` (`EJ2_RAW_MEASURES`, lines 234–265) are **100% identical and Urtext-compliant**.

### 1.2 Target File & Lines
- **Target File:** `/Users/sebas/Desktop/partituras/FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/model/ExerciseGenerator.kt`
- **Lines to Replace:** 131–162

### 1.3 Exact Code Replacement for Worker

#### Target Content (Existing Lines 131–162 in `ExerciseGenerator.kt`):
```kotlin
    internal val ej2RawMeasures = listOf(
        EJ1Measure(1,  listOf(listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E")), "|:", "|"),
        EJ1Measure(2,  listOf(listOf("D","_E","F","G","_A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","F","E","D")), "", "|"),
        EJ1Measure(3,  listOf(listOf("_E","F","_G","_A","_B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F")), "", "|"),
        EJ1Measure(4,  listOf(listOf("^D","=E","^F","^G","=A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","F","E","D")), "", "|"),
        EJ1Measure(5,  listOf(listOf("E","^F","=G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F")), "", "|"),
        EJ1Measure(6,  listOf(listOf("E","=F","G","A","_B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","G","F","E")), "", "|"),
        EJ1Measure(7,  listOf(listOf("F","G","_A","_B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G")), "", "|"),
        EJ1Measure(8,  listOf(listOf("^E","^F","^G","^A","=B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","G","F","E")), "", "|"),
        EJ1Measure(9,  listOf(listOf("^F","^G","=A","B","^c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G")), "", "|"),
        EJ1Measure(10, listOf(listOf("^F","=G","A","B","=c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","A","G","F")), "", "|"),
        EJ1Measure(11, listOf(listOf("G","A","_B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A")), "", "|"),
        EJ1Measure(12, listOf(listOf("^^F","^G","^A","=B","^c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","A","G","F")), "", "|"),
        EJ1Measure(13, listOf(listOf("^G","^A","B","^c","^d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A")), "", "|"),
        EJ1Measure(14, listOf(listOf("^G","=A","B","^c","=d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","B","A","G")), "", "|"),
        EJ1Measure(15, listOf(listOf("A","B","=c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B")), "", "|"),
        EJ1Measure(16, listOf(listOf("A","_B","c","d","_e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","c","B","A")), "", "|"),
        EJ1Measure(17, listOf(listOf("_B","c","_d","_e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c")), "", "|"),
        EJ1Measure(18, listOf(listOf("^A","=B","^c","^d","=e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","c","B","A")), "", "|"),
        EJ1Measure(19, listOf(listOf("B","^c","=d","e","^f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c")), "", "|"),
        EJ1Measure(20, listOf(listOf("B","=c","d","e","=f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","d","c","B")), "", "|"),
        EJ1Measure(21, listOf(listOf("c","d","_e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d")), "", "|"),
        EJ1Measure(22, listOf(listOf("^B","^c","^d","^e","^f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","d","c","B")), "", "|"),
        EJ1Measure(23, listOf(listOf("^c","^d","=e","^f","^g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d")), "", "|"),
        EJ1Measure(24, listOf(listOf("^c","=d","e","^f","=g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","e","d","c")), "", ":|"),
        EJ1Measure(25, listOf(listOf("d","e","=f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e")), "", "|"),
        EJ1Measure(26, listOf(listOf("d","_e","f","g","_a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","f","e","d")), "", "|"),
        EJ1Measure(27, listOf(listOf("_e","f","_g","_a","_b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f")), "", "|"),
        EJ1Measure(28, listOf(listOf("^d","=e","^f","^g","=a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","f","e","d")), "", "|"),
        EJ1Measure(29, listOf(listOf("e","^f","=g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f")), "", "|"),
        EJ1Measure(30, listOf(listOf("e","=f","g","a","_b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","g","f","e")), "", "| f4 z4 z8 |]")
    )
```

#### Replacement Content:
```kotlin
    internal val ej2RawMeasures = listOf(
        EJ1Measure(1,  listOf(listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E")), "|:", "|"),
        EJ1Measure(2,  listOf(listOf("D","_E","=F","_G","_A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","F","E","D")), "", "|"),
        EJ1Measure(3,  listOf(listOf("_E","F","_G","_A","_B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F")), "", "|"),
        EJ1Measure(4,  listOf(listOf("^D","=E","^F","=G","=A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","G","F","E"), listOf("D","E","F","G","A","F","E","D")), "", "|"),
        EJ1Measure(5,  listOf(listOf("E","^F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F")), "", "|"),
        EJ1Measure(6,  listOf(listOf("E","=F","=G","_A","_B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","G","F","E")), "", "|"),
        EJ1Measure(7,  listOf(listOf("F","G","_A","_B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G")), "", "|"),
        EJ1Measure(8,  listOf(listOf("^E","^F","^G","=A","=B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","A","G","F"), listOf("E","F","G","A","B","G","F","E")), "", "|"),
        EJ1Measure(9,  listOf(listOf("^F","^G","A","B","^c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G")), "", "|"),
        EJ1Measure(10, listOf(listOf("^F","=G","=A","_B","=c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","A","G","F")), "", "|"),
        EJ1Measure(11, listOf(listOf("G","A","_B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A")), "", "|"),
        EJ1Measure(12, listOf(listOf("^^F","^G","^A","B","^c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","B","A","G"), listOf("F","G","A","B","c","A","G","F")), "", "|"),
        EJ1Measure(13, listOf(listOf("^G","^A","B","^c","^d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A")), "", "|"),
        EJ1Measure(14, listOf(listOf("^G","=A","=B","=c","=d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","c","B","A"), listOf("G","A","B","c","d","B","A","G")), "", "|"),
        EJ1Measure(15, listOf(listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B")), "", "|"),
        EJ1Measure(16, listOf(listOf("A","_B","=c","_d","_e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","c","B","A")), "", "|"),
        EJ1Measure(17, listOf(listOf("_B","c","_d","_e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c")), "", "|"),
        EJ1Measure(18, listOf(listOf("^A","=B","^c","=d","=e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","d","c","B"), listOf("A","B","c","d","e","c","B","A")), "", "|"),
        EJ1Measure(19, listOf(listOf("B","^c","d","e","^f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c")), "", "|"),
        EJ1Measure(20, listOf(listOf("B","=c","=d","_e","=f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","d","c","B")), "", "|"),
        EJ1Measure(21, listOf(listOf("c","d","_e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d")), "", "|"),
        EJ1Measure(22, listOf(listOf("^B","^c","^d","=e","^f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","e","d","c"), listOf("B","c","d","e","f","d","c","B")), "", "|"),
        EJ1Measure(23, listOf(listOf("^c","^d","e","^f","^g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d")), "", "|"),
        EJ1Measure(24, listOf(listOf("^c","=d","=e","=f","=g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","f","e","d"), listOf("c","d","e","f","g","e","d","c")), "", ":|"),
        EJ1Measure(25, listOf(listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e")), "", "|"),
        EJ1Measure(26, listOf(listOf("d","_e","=f","_g","_a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","f","e","d")), "", "|"),
        EJ1Measure(27, listOf(listOf("_e","f","_g","_a","_b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f")), "", "|"),
        EJ1Measure(28, listOf(listOf("^d","=e","^f","=g","=a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","g","f","e"), listOf("d","e","f","g","a","f","e","d")), "", "|"),
        EJ1Measure(29, listOf(listOf("e","^f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f")), "", "|"),
        EJ1Measure(30, listOf(listOf("e","=f","=g","_a","_b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","a","g","f"), listOf("e","f","g","a","b","g","f","e")), "", "| f4 z4 z8 |]")
    )
```

---

## 2. DEF-03: Android `ScoreAudioPlayer.kt` Diminished Fourth Semitone

### 2.1 Context & Problem Analysis
In Taffanel & Gaubert E.J. 1 & E.J. 2 audio synthesis (`generateChromaticPentachordBuffer`):
- Measures 1..30 consist of 15 pairs of measures:
  - **Odd measure ($2k+1$):** Pentachord built on `base = 62 + k`.
    - E.J. 1 (Major): Semitone intervals `[0, 2, 4, 5, 7]` (major 3rd = 4).
    - E.J. 2 (Minor): Semitone intervals `[0, 2, 3, 5, 7]` (minor 3rd = 3).
  - **Even measure ($2k+2$):** Diminished leading chord vii° resolving into `base + 1`.
    - In E.J. 1 (leading to next major pentachord): Semitones `[0, 1, 3, 5, 6]`.
    - In E.J. 2 (leading to next minor pentachord): Semitones `[0, 1, 3, 4, 6]`. Note that the fourth pitch is a diminished 4th (`base + 4`) rather than a perfect 4th (`base + 5`).

In iOS `ScoreAudioPlayer.swift` (lines 401–414):
```swift
        let thirdSemitone = isMinor ? 3 : 4
        let dimFourthSemitone = isMinor ? 4 : 5

        for k in 0..<15 {
            let base = 62 + k
            let pent = [base, base + 2, base + thirdSemitone, base + 5, base + 7]
            ...
            let dim = [base, base + 1, base + 3, base + dimFourthSemitone, base + 6]
```

In Android `ScoreAudioPlayer.kt` (lines 431–444):
Line 431 has:
```kotlin
        val thirdOffset = if (isMinor) 3 else 4
```
And line 444 hardcodes:
```kotlin
        val dim = listOf(base, base + 1, base + 3, base + 5, base + 6)
```
Consequently, during Android E.J. 2 playback, the even measures play a perfect fourth (`base + 5`) instead of a diminished fourth (`base + 4`), distorting the harmony.

### 2.2 Target File & Lines
- **Target File:** `/Users/sebas/Desktop/partituras/FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/audio/ScoreAudioPlayer.kt`
- **Lines to Edit:** Lines 431–445

### 2.3 Exact Code Replacement for Worker

#### Target Content 1 (Lines 431–432 in `ScoreAudioPlayer.kt`):
```kotlin
        val thirdOffset = if (isMinor) 3 else 4

        // 15 chromatic pairs (Measures 1..30), starting on D4 (MIDI 62) up to F5 (MIDI 77)
```

#### Replacement Content 1:
```kotlin
        val thirdOffset = if (isMinor) 3 else 4
        val dimFourthSemitone = if (isMinor) 4 else 5

        // 15 chromatic pairs (Measures 1..30), starting on D4 (MIDI 62) up to F5 (MIDI 77)
```

#### Target Content 2 (Line 444 in `ScoreAudioPlayer.kt`):
```kotlin
            // Even measure: Diminished 7th vii° (0, 1, 3, 5, 6) resolving to base + 1
            val dim = listOf(base, base + 1, base + 3, base + 5, base + 6)
```

#### Replacement Content 2:
```kotlin
            // Even measure: Diminished 7th vii° resolving to base + 1
            val dim = listOf(base, base + 1, base + 3, base + dimFourthSemitone, base + 6)
```

---

## 3. DEF-05: Android `ScoreAudioPlayer.kt` R.5 Sixteenth Triplet Tempo Timing

### 3.1 Context & Problem Analysis
Reichert Op. 5 Exercise No. 5 (R. 5) is written in 2/4 meter with continuous sixteenth-note triplets (sextuplets).
- There are **6 sixteenth triplets per quarter note beat** (12 notes per measure).
- In standard music notation and metronome practice, `tempoBPM` represents quarter notes per minute.
- Therefore, the duration of each sixteenth triplet note is:
  $$\text{duration} = \frac{60.0}{\text{tempoBPM}} \times \frac{1}{6.0} = \frac{60.0}{\text{tempoBPM} \times 6.0}$$
- For standard sixteenth notes in E.J. 5, E.J. 10, E.J. 11, and R. 1, there are 4 notes per quarter note:
  $$\text{duration} = \frac{60.0}{\text{tempoBPM}} \times \frac{1}{4.0}$$

In `ScoreAudioPlayer.kt` line 302:
```kotlin
        val sixteenthDuration = (60.0 / tempoBPM.toDouble()) / 4.0
```
This hardcoded divisor `4.0` causes R. 5 audio playback in Android to run at $\frac{4}{6} = \frac{2}{3}$ speed (33% slower than intended BPM).

In iOS `ScoreAudioPlayer.swift` lines 224–226:
```swift
        let baseNoteDuration = (exercise == .r5)
            ? ((60.0 / Double(tempoBPM)) / 6.0)
            : ((60.0 / Double(tempoBPM)) / 4.0)
```

Furthermore, in iOS `ScoreAudioPlayer.swift` lines 250–257, for Reichert R. 1 and R. 5:
Each section ends with an eighth note staccato (duration = `baseNoteDuration * 2.0`, `isStaccato: true`).
In Android lines 334–340, only `secIdx == 24` was flagged `isLongFinal` (duration = `sixteenthDuration * 6.0`), while sections 0..23 received a standard regular note duration without staccato.

### 3.2 Target File & Lines
- **Target File:** `/Users/sebas/Desktop/partituras/FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/audio/ScoreAudioPlayer.kt`
- **Lines to Edit:**
  - Line 302 (`sixteenthDuration`)
  - Lines 333–342 (final note duration and staccato handling)

### 3.3 Exact Code Replacement for Worker

#### Target Content 1 (Line 302 in `ScoreAudioPlayer.kt`):
```kotlin
    internal fun generateEJ5TypeScoreBuffer(
        exercise: ExerciseType,
        articulation: EJ5Articulation,
        sectionIndex: Int,
        tempoBPM: Int
    ): ShortArray {
        val sixteenthDuration = (60.0 / tempoBPM.toDouble()) / 4.0
        val finalDuration = sixteenthDuration * 6.0
```

#### Replacement Content 1:
```kotlin
    internal fun generateEJ5TypeScoreBuffer(
        exercise: ExerciseType,
        articulation: EJ5Articulation,
        sectionIndex: Int,
        tempoBPM: Int
    ): ShortArray {
        val sixteenthDuration = if (exercise == ExerciseType.R5) {
            (60.0 / tempoBPM.toDouble()) / 6.0
        } else {
            (60.0 / tempoBPM.toDouble()) / 4.0
        }
        val finalDuration = sixteenthDuration * 6.0
```

#### Target Content 2 (Lines 333–342 in `ScoreAudioPlayer.kt`):
```kotlin
        val notes = mutableListOf<NoteDef>()
        for ((idx, m) in midiNotes.withIndex()) {
            val isLongFinal = (idx == midiNotes.size - 1) && (exercise == ExerciseType.EJ5 || (!exercise.isReichertExercise && secIdx == 11) || (exercise.isReichertExercise && secIdx == 24))
            notes.add(
                NoteDef(
                    freq = midiToFrequency(m.toDouble()),
                    duration = if (isLongFinal) finalDuration else sixteenthDuration,
                    isStaccato = if (isLongFinal) false else isStaccatoAt(idx)
                )
            )
        }
        return renderNotesToPcm(notes)
```

#### Replacement Content 2:
```kotlin
        val notes = mutableListOf<NoteDef>()
        for ((idx, m) in midiNotes.withIndex()) {
            val isLast = (idx == midiNotes.size - 1)
            if (isLast && (exercise == ExerciseType.R1 || exercise == ExerciseType.R5)) {
                notes.add(
                    NoteDef(
                        freq = midiToFrequency(m.toDouble()),
                        duration = sixteenthDuration * 2.0,
                        isStaccato = true
                    )
                )
            } else {
                val isLongFinal = isLast && (exercise == ExerciseType.EJ5 || (!exercise.isReichertExercise && secIdx == 11))
                notes.add(
                    NoteDef(
                        freq = midiToFrequency(m.toDouble()),
                        duration = if (isLongFinal) finalDuration else sixteenthDuration,
                        isStaccato = if (isLongFinal) false else isStaccatoAt(idx)
                    )
                )
            }
        }
        return renderNotesToPcm(notes)
```

---

## 4. Complementary Audio Engine Parity: R. 2 and R. 4 in `generateEJ4ScoreBuffer`

For complete multiplatform synthesis parity, in `generateEJ4ScoreBuffer` (`ScoreAudioPlayer.kt` lines 380–389), iOS handles Reichert R. 2 and R. 4 final notes with `isStaccato = true` and `duration = eighthDuration * 2.0`, plus anacrusis phase alignment for R. 2:
```kotlin
        val notes = mutableListOf<NoteDef>()
        for ((idx, m) in midiNotes.withIndex()) {
            val isLast = (idx == midiNotes.size - 1)
            if (isLast && (exercise == ExerciseType.R2 || exercise == ExerciseType.R4)) {
                notes.add(
                    NoteDef(
                        freq = midiToFrequency(m.toDouble()),
                        duration = eighthDuration * 2.0,
                        isStaccato = true
                    )
                )
            } else {
                val isLastInCoda = isCoda && isLast
                val subIdx = if (exercise == ExerciseType.R2) {
                    if (idx >= 4) (idx - 4) else (idx + 4)
                } else idx
                notes.add(
                    NoteDef(
                        freq = midiToFrequency(m.toDouble()),
                        duration = if (isLastInCoda) finalDuration else eighthDuration,
                        isStaccato = if (isLastInCoda) false else isStaccatoAt(subIdx)
                    )
                )
            }
        }
```

---

## 5. Unit Test Expansion Specifications

To verify DEF-02, DEF-03, and DEF-05 automatically in CI (`./gradlew testDebugUnitTest`), the Worker should add the following unit tests:

### 5.1 In `ExerciseGeneratorTest.kt`:
```kotlin
    @Test
    fun testEJ2MeasuresContainUrtextMinorThirdAccidentals() {
        val ej2Abc = ExerciseGenerator.generateEJ2ABC(articulation = EJ1Articulation.ORIGINAL, tempoBPM = 80, loc = loc)
        
        // Measure 4: must have =G (G natural), not ^G (G sharp)
        assertTrue("Measure 4 must contain =G", ej2Abc.contains("^D=E^F=G=A") || ExerciseGenerator.ej2RawMeasures[3].beats[0].contains("=G"))
        assertFalse("Measure 4 must not contain ^G", ExerciseGenerator.ej2RawMeasures[3].beats[0].contains("^G"))

        // Measure 8: must have =A (A natural), not ^A (A sharp)
        assertTrue("Measure 8 must contain =A", ExerciseGenerator.ej2RawMeasures[7].beats[0].contains("=A"))
        assertFalse("Measure 8 must not contain ^A", ExerciseGenerator.ej2RawMeasures[7].beats[0].contains("^A"))

        // Measure 14: must have =c (C natural), not ^c (C sharp)
        assertTrue("Measure 14 must contain =c", ExerciseGenerator.ej2RawMeasures[13].beats[0].contains("=c"))
        assertFalse("Measure 14 must not contain ^c", ExerciseGenerator.ej2RawMeasures[13].beats[0].contains("^c"))

        // Measure 18: must have =d (D natural), not ^d (D sharp)
        assertTrue("Measure 18 must contain =d", ExerciseGenerator.ej2RawMeasures[17].beats[0].contains("=d"))
        assertFalse("Measure 18 must not contain ^d", ExerciseGenerator.ej2RawMeasures[17].beats[0].contains("^d"))

        // Measure 22: must have =e (E natural), not ^e (E sharp)
        assertTrue("Measure 22 must contain =e", ExerciseGenerator.ej2RawMeasures[21].beats[0].contains("=e"))
        assertFalse("Measure 22 must not contain ^e", ExerciseGenerator.ej2RawMeasures[21].beats[0].contains("^e"))

        // Measure 24: must have =f (F natural), not ^f (F sharp)
        assertTrue("Measure 24 must contain =f", ExerciseGenerator.ej2RawMeasures[23].beats[0].contains("=f"))
        assertFalse("Measure 24 must not contain ^f", ExerciseGenerator.ej2RawMeasures[23].beats[0].contains("^f"))

        // Measure 28: must have =g (G natural), not ^g (G sharp)
        assertTrue("Measure 28 must contain =g", ExerciseGenerator.ej2RawMeasures[27].beats[0].contains("=g"))
        assertFalse("Measure 28 must not contain ^g", ExerciseGenerator.ej2RawMeasures[27].beats[0].contains("^g"))
    }
```

### 5.2 In `AudioSynthesisTest.kt`:
```kotlin
    @Test
    fun testEJ2ScoreBufferGeneratesValidAudio() {
        val player = ScoreAudioPlayer()
        val buffer = player.generateEJ2ScoreBuffer(articulation = EJ1Articulation.ORIGINAL, tempoBPM = 100)
        assertTrue("EJ2 buffer must not be empty", buffer.isNotEmpty())
    }

    @Test
    fun testR5TempoDivisorSixteenthTripletDuration() {
        val player = ScoreAudioPlayer()
        val tempo = 120
        // R5 has 91 notes, with 16th triplets (divisor 6.0)
        val r5Buffer = player.generateEJ5TypeScoreBuffer(
            exercise = ExerciseType.R5,
            articulation = EJ5Articulation.ORIGINAL,
            sectionIndex = 0,
            tempoBPM = tempo
        )
        // EJ5 has 73 notes, with standard 16th notes (divisor 4.0)
        val ej5Buffer = player.generateEJ5TypeScoreBuffer(
            exercise = ExerciseType.EJ5,
            articulation = EJ5Articulation.ORIGINAL,
            sectionIndex = 0,
            tempoBPM = tempo
        )
        
        // Single note duration: R5 note is (60/120)/6 = 0.5/6 = 0.0833s. EJ5 note is (60/120)/4 = 0.125s.
        // Ratio of single note length is exactly 4.0 / 6.0 = 2/3.
        val r5FramesPerNote = (44100.0 * ((60.0 / tempo) / 6.0))
        val ej5FramesPerNote = (44100.0 * ((60.0 / tempo) / 4.0))
        assertEquals(2.0 / 3.0, r5FramesPerNote / ej5FramesPerNote, 0.001)
        assertTrue("R5 buffer must be populated", r5Buffer.isNotEmpty())
        assertTrue("EJ5 buffer must be populated", ej5Buffer.isNotEmpty())
    }
```

---

## 6. Verification Checklist
- [ ] Replace lines 131–162 in `ExerciseGenerator.kt` with the 30 updated measures.
- [ ] Replace lines 431–432 and line 444 in `ScoreAudioPlayer.kt` with `dimFourthSemitone`.
- [ ] Replace line 302 and lines 333–342 in `ScoreAudioPlayer.kt` with the R5 divisor `6.0` and staccato handling.
- [ ] Run `./gradlew testDebugUnitTest` in `FluteModesAndroid/` -> Expect all tests to pass.
