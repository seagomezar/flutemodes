package com.seagomezar.flutemodes.model

import android.content.Context
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue

class PracticeStore(context: Context) {
    private val prefs = context.getSharedPreferences("FluteModes_Progress_v1", Context.MODE_PRIVATE)

    // Key: "Tonic_Mode" -> Set of completed articulation IDs (1..8)
    val completedMap = mutableStateMapOf<String, Set<Int>>()

    // Completed E.J. 1 articulation IDs (1..10)
    var ej1CompletedSet by mutableStateOf<Set<Int>>(emptySet())
        private set

    // Completed E.J. 2 articulation IDs (1..10)
    var ej2CompletedSet by mutableStateOf<Set<Int>>(emptySet())
        private set

    var lastExerciseType by mutableStateOf(ExerciseType.EJ1)
    var lastEJ1Articulation by mutableStateOf(EJ1Articulation.ORIGINAL)
    var lastEJ2Articulation by mutableStateOf(EJ1Articulation.ORIGINAL)

    var lastTonic by mutableStateOf<Tonic?>(null)
    var lastMode by mutableStateOf<ModeType?>(null)
    var lastArticulation by mutableStateOf<ArticulationPattern?>(null)

    var keepScreenAwake by mutableStateOf(prefs.getBoolean("keep_screen_awake", true))
        private set

    fun setKeepScreenAwakeState(enabled: Boolean) {
        keepScreenAwake = enabled
        prefs.edit().putBoolean("keep_screen_awake", enabled).apply()
    }

    init {
        loadProgress()
    }

    // --- E.J. 1 Progress ---
    fun isEJ1Completed(articulation: EJ1Articulation): Boolean {
        if (articulation == EJ1Articulation.ORIGINAL) return false
        return ej1CompletedSet.contains(articulation.id)
    }

    val ej1CompletedCount: Int
        get() = ej1CompletedSet.size

    val isEJ1FullyCompleted: Boolean
        get() = ej1CompletedSet.size == 10

    fun markEJ1Completed(articulation: EJ1Articulation) {
        if (articulation != EJ1Articulation.ORIGINAL) {
            ej1CompletedSet = ej1CompletedSet + articulation.id
        }
        lastExerciseType = ExerciseType.EJ1
        lastEJ1Articulation = articulation
        saveProgress()
    }

    fun unmarkEJ1Completed(articulation: EJ1Articulation) {
        ej1CompletedSet = ej1CompletedSet - articulation.id
        saveProgress()
    }

    fun toggleEJ1Completed(articulation: EJ1Articulation) {
        if (articulation == EJ1Articulation.ORIGINAL) return
        if (isEJ1Completed(articulation)) {
            unmarkEJ1Completed(articulation)
        } else {
            markEJ1Completed(articulation)
        }
    }

    fun resetEJ1() {
        ej1CompletedSet = emptySet()
        saveProgress()
    }

    // --- E.J. 2 Progress ---
    fun isEJ2Completed(articulation: EJ1Articulation): Boolean {
        if (articulation == EJ1Articulation.ORIGINAL) return false
        return ej2CompletedSet.contains(articulation.id)
    }

    val ej2CompletedCount: Int
        get() = ej2CompletedSet.size

    val isEJ2FullyCompleted: Boolean
        get() = ej2CompletedSet.size == 10

    fun markEJ2Completed(articulation: EJ1Articulation) {
        if (articulation != EJ1Articulation.ORIGINAL) {
            ej2CompletedSet = ej2CompletedSet + articulation.id
        }
        lastExerciseType = ExerciseType.EJ2
        lastEJ2Articulation = articulation
        saveProgress()
    }

    fun unmarkEJ2Completed(articulation: EJ1Articulation) {
        ej2CompletedSet = ej2CompletedSet - articulation.id
        saveProgress()
    }

    fun toggleEJ2Completed(articulation: EJ1Articulation) {
        if (articulation == EJ1Articulation.ORIGINAL) return
        if (isEJ2Completed(articulation)) {
            unmarkEJ2Completed(articulation)
        } else {
            markEJ2Completed(articulation)
        }
    }

    fun resetEJ2() {
        ej2CompletedSet = emptySet()
        saveProgress()
    }

    // --- Unified Chromatic Helpers ---
    fun isChromaticCompleted(articulation: EJ1Articulation, exercise: ExerciseType): Boolean {
        return if (exercise == ExerciseType.EJ2) isEJ2Completed(articulation) else isEJ1Completed(articulation)
    }

    fun chromaticCompletedCount(exercise: ExerciseType): Int {
        return if (exercise == ExerciseType.EJ2) ej2CompletedCount else ej1CompletedCount
    }

    fun isChromaticFullyCompleted(exercise: ExerciseType): Boolean {
        return if (exercise == ExerciseType.EJ2) isEJ2FullyCompleted else isEJ1FullyCompleted
    }

    fun toggleChromaticCompleted(articulation: EJ1Articulation, exercise: ExerciseType) {
        if (exercise == ExerciseType.EJ2) {
            toggleEJ2Completed(articulation)
        } else {
            toggleEJ1Completed(articulation)
        }
    }

    fun markChromaticCompleted(articulation: EJ1Articulation, exercise: ExerciseType) {
        if (exercise == ExerciseType.EJ2) {
            markEJ2Completed(articulation)
        } else {
            markEJ1Completed(articulation)
        }
    }

    // --- E.J. 4 Progress ---
    fun isCompleted(tonic: Tonic, mode: ModeType, articulation: ArticulationPattern): Boolean {
        val key = "${tonic.name}_${mode.name}"
        return completedMap[key]?.contains(articulation.id) ?: false
    }

    fun completedArticulationsCount(tonic: Tonic, mode: ModeType): Int {
        val key = "${tonic.name}_${mode.name}"
        return completedMap[key]?.size ?: 0
    }

    fun isModeFullyCompleted(tonic: Tonic, mode: ModeType): Boolean {
        return completedArticulationsCount(tonic, mode) == 8
    }

    fun practicedModesCount(tonic: Tonic): Int {
        return ModeType.entries.count { mode ->
            completedArticulationsCount(tonic, mode) > 0
        }
    }

    fun areAllSevenModesPracticed(tonic: Tonic): Boolean {
        return practicedModesCount(tonic) == 7
    }

    fun isTonicMastered(tonic: Tonic): Boolean {
        return ModeType.entries.all { mode ->
            isModeFullyCompleted(tonic, mode)
        }
    }

    fun totalArticulationsCompleted(tonic: Tonic): Int {
        return ModeType.entries.sumOf { mode ->
            completedArticulationsCount(tonic, mode)
        }
    }

    fun markCompleted(tonic: Tonic, mode: ModeType, articulation: ArticulationPattern) {
        val key = "${tonic.name}_${mode.name}"
        val current = (completedMap[key] ?: emptySet()).toMutableSet()
        current.add(articulation.id)
        completedMap[key] = current

        lastExerciseType = ExerciseType.EJ4
        lastTonic = tonic
        lastMode = mode
        lastArticulation = articulation

        saveProgress()
    }

    fun unmarkCompleted(tonic: Tonic, mode: ModeType, articulation: ArticulationPattern) {
        val key = "${tonic.name}_${mode.name}"
        val current = (completedMap[key] ?: emptySet()).toMutableSet()
        current.remove(articulation.id)
        completedMap[key] = current
        saveProgress()
    }

    fun toggleCompleted(tonic: Tonic, mode: ModeType, articulation: ArticulationPattern) {
        if (isCompleted(tonic, mode, articulation)) {
            unmarkCompleted(tonic, mode, articulation)
        } else {
            markCompleted(tonic, mode, articulation)
        }
    }

    fun nextTonic(after: Tonic): Tonic {
        val all = Tonic.entries
        val idx = all.indexOf(after)
        return if (idx >= 0) all[(idx + 1) % all.size] else all[0]
    }

    val totalModesCount: Int = Tonic.entries.size * ModeType.entries.size // 84

    val completedModesCount: Int
        get() = Tonic.entries.sumOf { t ->
            ModeType.entries.count { m -> isModeFullyCompleted(t, m) }
        }

    val totalPracticedArticulationsCount: Int
        get() = completedMap.values.sumOf { it.size }

    fun resetAll() {
        completedMap.clear()
        ej1CompletedSet = emptySet()
        ej2CompletedSet = emptySet()
        lastTonic = null
        lastMode = null
        lastArticulation = null
        prefs.edit().clear().apply()
    }

    fun saveLastSelection() {
        saveProgress()
    }

    private fun saveProgress() {
        val editor = prefs.edit()
        for ((k, v) in completedMap) {
            editor.putString("cell_$k", v.joinToString(","))
        }
        editor.putString("ej1_completed", ej1CompletedSet.joinToString(","))
        editor.putString("ej2_completed", ej2CompletedSet.joinToString(","))
        editor.putString("last_exercise_type", lastExerciseType.name)
        editor.putString("last_ej1_articulation", lastEJ1Articulation.name)
        editor.putString("last_ej2_articulation", lastEJ2Articulation.name)
        lastTonic?.let { editor.putString("last_tonic", it.name) }
        lastMode?.let { editor.putString("last_mode", it.name) }
        lastArticulation?.let { editor.putString("last_articulation", it.name) }
        editor.apply()
    }

    private fun loadProgress() {
        val allKeys = prefs.all
        for ((k, v) in allKeys) {
            if (k.startsWith("cell_") && v is String) {
                val cellKey = k.removePrefix("cell_")
                val set = v.split(",")
                    .mapNotNull { it.trim().toIntOrNull() }
                    .toSet()
                completedMap[cellKey] = set
            }
        }
        val ej1Str = prefs.getString("ej1_completed", null)
        if (!ej1Str.isNullOrBlank()) {
            ej1CompletedSet = ej1Str.split(",")
                .mapNotNull { it.trim().toIntOrNull() }
                .filter { it in 1..10 }
                .toSet()
        }
        val ej2Str = prefs.getString("ej2_completed", null)
        if (!ej2Str.isNullOrBlank()) {
            ej2CompletedSet = ej2Str.split(",")
                .mapNotNull { it.trim().toIntOrNull() }
                .filter { it in 1..10 }
                .toSet()
        }
        val exStr = prefs.getString("last_exercise_type", null)
        if (exStr != null) {
            lastExerciseType = runCatching { ExerciseType.valueOf(exStr) }.getOrDefault(ExerciseType.EJ1)
        }
        val ej1ArtStr = prefs.getString("last_ej1_articulation", null)
        if (ej1ArtStr != null) {
            lastEJ1Articulation = runCatching { EJ1Articulation.valueOf(ej1ArtStr) }.getOrDefault(EJ1Articulation.ORIGINAL)
        }
        val ej2ArtStr = prefs.getString("last_ej2_articulation", null)
        if (ej2ArtStr != null) {
            lastEJ2Articulation = runCatching { EJ1Articulation.valueOf(ej2ArtStr) }.getOrDefault(EJ1Articulation.ORIGINAL)
        }
        val tStr = prefs.getString("last_tonic", null)
        val mStr = prefs.getString("last_mode", null)
        val aStr = prefs.getString("last_articulation", null)

        if (tStr != null) lastTonic = runCatching { Tonic.valueOf(tStr) }.getOrNull()
        if (mStr != null) lastMode = runCatching { ModeType.valueOf(mStr) }.getOrNull()
        if (aStr != null) lastArticulation = runCatching { ArticulationPattern.valueOf(aStr) }.getOrNull()
    }
}
