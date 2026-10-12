# Handoff Report: Technical Specifications for DEF-02, DEF-03, and DEF-05

**Agent:** `explorer_m1_2`  
**Milestone:** Milestone 1 (Score Engine & Urtext Parity Fixes)  
**Target Recipient:** Orchestrator (`2c224607-5456-4eac-ad55-0172dee3d36d`) / Implementing Worker Agent  
**Date:** 2026-10-11  
**Handoff Type:** Hard (Task Complete)  

---

## 1. Observation

### Source Code Paths & Line Numbers Examined

1. **Android Exercise Generator:**
   - Path: `/Users/sebas/Desktop/partituras/FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/model/ExerciseGenerator.kt`
   - Lines 131–162: Definition of `internal val ej2RawMeasures = listOf(...)`.
   - Line 135: `EJ1Measure(4, listOf(listOf("^D","=E","^F","^G","=A","G","F","E"), ...` contains `^G` (G♯) instead of `=G`.
   - Line 139: `EJ1Measure(8, listOf(listOf("^E","^F","^G","^A","=B","A","G","F"), ...` contains `^A` (A♯) instead of `=A`.
   - Line 145: `EJ1Measure(14, listOf(listOf("^G","=A","B","^c","=d","c","B","A"), ...` contains `^c` (C♯) instead of `=c`, and `B` instead of `=B`.
   - Line 149: `EJ1Measure(18, listOf(listOf("^A","=B","^c","^d","=e","d","c","B"), ...` contains `^d` (D♯) instead of `=d`.
   - Line 153: `EJ1Measure(22, listOf(listOf("^B","^c","^d","^e","^f","e","d","c"), ...` contains `^e` (E♯) instead of `=e`.
   - Line 155: `EJ1Measure(24, listOf(listOf("^c","=d","e","^f","=g","f","e","d"), ...` contains `^f` (F♯) instead of `=f`, and `e` instead of `=e`.
   - Line 159: `EJ1Measure(28, listOf(listOf("^d","=e","^f","^g","=a","g","f","e"), ...` contains `^g` (G♯) instead of `=g`.
   - Furthermore, measures 12, 13, 22, 23 contain diatonic repetitions in Beats 1–3 copied from EJ1 rather than matching EJ2 root pitches.

2. **iOS Exercise Generator & Score Template (Ground Truth):**
   - Path: `/Users/sebas/Desktop/partituras/FluteModes/FluteModes/Models/ExerciseGenerator.swift`
   - Lines 75–106: `internal static let ej2RawMeasures: [(num: Int, beats: [[String]], prefix: String, suffix: String)] = [...]`.
   - Path: `/Users/sebas/Desktop/partituras/FluteModes/FluteModes/Resources/score_template.html`
   - Lines 234–265: `const EJ2_RAW_MEASURES = [...]`.
   - Automated comparison confirmed 100% agreement across all 30 measures between `ExerciseGenerator.swift` and `score_template.html`.

3. **Android Audio Synth Player:**
   - Path: `/Users/sebas/Desktop/partituras/FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/audio/ScoreAudioPlayer.kt`
   - Line 302:
     ```kotlin
     val sixteenthDuration = (60.0 / tempoBPM.toDouble()) / 4.0
     ```
   - Lines 333–342:
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
     ```
   - Lines 431–444:
     ```kotlin
     val thirdOffset = if (isMinor) 3 else 4
     // 15 chromatic pairs (Measures 1..30), starting on D4 (MIDI 62) up to F5 (MIDI 77)
     for (k in 0 until 15) {
         val base = 62 + k
         val pent = listOf(base, base + 2, base + thirdOffset, base + 5, base + 7)
         ...
         // Even measure: Diminished 7th vii° (0, 1, 3, 5, 6) resolving to base + 1
         val dim = listOf(base, base + 1, base + 3, base + 5, base + 6)
     ```

4. **iOS Audio Synth Player (Ground Truth):**
   - Path: `/Users/sebas/Desktop/partituras/FluteModes/FluteModes/Audio/ScoreAudioPlayer.swift`
   - Lines 224–226:
     ```swift
     let baseNoteDuration = (exercise == .r5)
         ? ((60.0 / Double(tempoBPM)) / 6.0)
         : ((60.0 / Double(tempoBPM)) / 4.0)
     ```
   - Lines 250–257:
     ```swift
     let isLast = (idx == midiNotes.count - 1)
     if isLast && (exercise == .r1 || exercise == .r5) {
         notes.append(NoteDef(
             freq: Self.midiToFrequency(Double(m)),
             duration: baseNoteDuration * 2.0,
             isStaccato: true
         ))
     } else {
         let isLongFinal = isLast && (exercise == .ej5 || clampedSec == 11)
         notes.append(NoteDef(
             freq: Self.midiToFrequency(Double(m)),
             duration: isLongFinal ? baseNoteDuration * 6.0 : baseNoteDuration,
             isStaccato: isLongFinal ? false : isStaccatoAt(idx)
         ))
     }
     ```
   - Lines 401–414:
     ```swift
     let thirdSemitone = isMinor ? 3 : 4
     let dimFourthSemitone = isMinor ? 4 : 5
     ...
     let dim = [base, base + 1, base + 3, base + dimFourthSemitone, base + 6]
     ```

---

## 2. Logic Chain

1. **DEF-02 (Android E.J. 2 Measures Parity):**
   - *Premise:* Taffanel & Gaubert E.J. 2 (Plate A. L. 16.588) exercises minor pentachords.
   - *Observation:* Kotlin's `ej2RawMeasures` contains major thirds in mm. 4, 8, 14, 18, 22, 24, 28 (e.g. `^G` in m.4 instead of `=G`, `^A` in m.8 instead of `=A`), alongside missing natural signs and diatonic baseline discrepancies in mm. 12, 13, 22, 23.
   - *Observation:* `ExerciseGenerator.swift` lines 75–106 and `score_template.html` lines 234–265 have identical, musicologically verified representations.
   - *Inference:* Dropping in the 30 measures converted from `ExerciseGenerator.swift` directly into lines 131–162 of `ExerciseGenerator.kt` guarantees 100% parity across platforms and restores Urtext compliance.

2. **DEF-03 (Android Audio Diminished Fourth Semitone):**
   - *Premise:* In E.J. 2 (minor), the diminished chord in even measures modulating to the minor tonic requires semitones `(0, 1, 3, 4, 6)` above `base`.
   - *Observation:* Line 444 of `ScoreAudioPlayer.kt` hardcodes `listOf(base, base + 1, base + 3, base + 5, base + 6)`.
   - *Inference:* Defining `val dimFourthSemitone = if (isMinor) 4 else 5` and substituting it into `dim` brings audio synthesis in sync with iOS and music theory.

3. **DEF-05 (Android Audio R.5 Triplet Timing):**
   - *Premise:* Reichert Op. 5 Exercise No. 5 is written in 2/4 meter with continuous sixteenth sextuplets (triplets: 6 notes per quarter-note beat).
   - *Observation:* Android `ScoreAudioPlayer.kt` line 302 divides `(60.0 / tempoBPM)` by `4.0` for all exercises, causing R.5 to play 33% too slowly.
   - *Observation:* iOS `ScoreAudioPlayer.swift` sets divisor to `6.0` when `exercise == .r5` and handles final staccato eighth notes.
   - *Inference:* Using `if (exercise == ExerciseType.R5) (60.0 / tempoBPM.toDouble()) / 6.0 else (60.0 / tempoBPM.toDouble()) / 4.0` and matching iOS's final note staccato logic eliminates the tempo defect.

---

## 3. Caveats

- **Read-Only Explorer Scope:** As an explorer agent, no project source code files were directly modified in this phase. The worker agent will apply the modifications.
- **Related R2/R4 Audio Engine Logic:** While DEF-05 targets R.5, R.2 and R.4 have anacrusis / pickup phrasing in `generateEJ4ScoreBuffer`. Specifications for this enhancement were provided in Section 4 of `analysis.md` for complete symmetry.
- **Audio Verification in Headless CI:** PCM buffer math and durations can be verified via JUnit unit tests (`AudioSynthesisTest.kt`) without requiring an active audio device.

---

## 4. Conclusion

The technical solution for DEF-02, DEF-03, and DEF-05 is completely specified with exact line-by-line drop-in replacements ready for immediate application by the Worker:

1. **DEF-02:** Replace lines 131–162 of `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/model/ExerciseGenerator.kt` with the 30 Urtext measures specified in `analysis.md` Section 1.3.
2. **DEF-03:** Add `val dimFourthSemitone = if (isMinor) 4 else 5` at line 432 and update line 444 in `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/audio/ScoreAudioPlayer.kt` as specified in `analysis.md` Section 2.3.
3. **DEF-05:** Update line 302 and lines 333–342 in `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/audio/ScoreAudioPlayer.kt` to use tempo divisor 6.0 for R.5 and staccato note handling as specified in `analysis.md` Section 3.3.
4. **Unit Tests:** Add test cases in `ExerciseGeneratorTest.kt` and `AudioSynthesisTest.kt` as specified in `analysis.md` Section 5.

Full technical details and drop-in code snippets are located at:
`/Users/sebas/Desktop/partituras/.agents/teamwork/explorer_m1_2/analysis.md`

---

## 5. Verification Method

To independently verify the fixes once applied by the Worker:

1. **Verify E.J. 2 Measures in `ExerciseGenerator.kt`:**
   ```bash
   python3 -c "
   kt = open('FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/model/ExerciseGenerator.kt').read()
   for bad in ['listOf(\"^D\",\"=E\",\"^F\",\"^G\"', 'listOf(\"^E\",\"^F\",\"^G\",\"^A\"', 'listOf(\"^G\",\"=A\",\"B\",\"^c\"']:
       assert bad not in kt, f'Found uncorrected accidental: {bad}'
   print('DEF-02 verification: PASSED')
   "
   ```

2. **Verify Diminished Fourth Semitone in `ScoreAudioPlayer.kt`:**
   ```bash
   grep -n "dimFourthSemitone" FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/audio/ScoreAudioPlayer.kt
   # Expected: val dimFourthSemitone = if (isMinor) 4 else 5
   # And: listOf(base, base + 1, base + 3, base + dimFourthSemitone, base + 6)
   ```

3. **Verify R.5 Tempo Divisor in `ScoreAudioPlayer.kt`:**
   ```bash
   grep -n "ExerciseType.R5" FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/audio/ScoreAudioPlayer.kt
   # Expected: Check dividing by 6.0 when exercise == ExerciseType.R5
   ```

4. **Run Android Unit Test Suite:**
   ```bash
   cd FluteModesAndroid && ./gradlew testDebugUnitTest
   # Expected: BUILD SUCCESSFUL with 0 failures
   ```
