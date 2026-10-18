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

    // Completed E.J. 4, R. 2, R. 4 articulation IDs (1..8)
    var ej4CompletedSet by mutableStateOf<Set<Int>>(emptySet())
        private set
    var r2CompletedSet by mutableStateOf<Set<Int>>(emptySet())
        private set
    var r4CompletedSet by mutableStateOf<Set<Int>>(emptySet())
        private set

    // Completed E.J. 5, E.J. 10, E.J. 11, R. 1, R. 5 articulation IDs (1..10)
    var ej5CompletedSet by mutableStateOf<Set<Int>>(emptySet())
        private set
    var ej10CompletedSet by mutableStateOf<Set<Int>>(emptySet())
        private set
    var ej11CompletedSet by mutableStateOf<Set<Int>>(emptySet())
        private set
    var r1CompletedSet by mutableStateOf<Set<Int>>(emptySet())
        private set
    var r5CompletedSet by mutableStateOf<Set<Int>>(emptySet())
        private set

    var lastExerciseType by mutableStateOf(ExerciseType.EJ1)
    var lastEJ1Articulation by mutableStateOf(EJ1Articulation.ORIGINAL)
    var lastEJ2Articulation by mutableStateOf(EJ1Articulation.ORIGINAL)
    var lastEJ4Articulation by mutableStateOf(EJ4Articulation.ORIGINAL)
    var lastEJ4Section by mutableStateOf(EJ4Section.C_MAJOR)
    var lastEJ5Articulation by mutableStateOf(EJ5Articulation.ORIGINAL)
    var lastEJ5Section by mutableStateOf(EJ5Section.C_CHROM)
    var lastEJ10Articulation by mutableStateOf(EJ5Articulation.ORIGINAL)
    var lastEJ10Section by mutableStateOf(EJ10Section.C_ARP)
    var lastEJ11Articulation by mutableStateOf(EJ5Articulation.ORIGINAL)
    var lastEJ11Section by mutableStateOf(EJ10Section.C_ARP)
    var lastR1Articulation by mutableStateOf(EJ5Articulation.ORIGINAL)
    var lastR1Section by mutableStateOf(EJ4Section.C_MAJOR)
    var lastR2Articulation by mutableStateOf(EJ4Articulation.ORIGINAL)
    var lastR2Section by mutableStateOf(EJ4Section.C_MAJOR)
    var lastR4Articulation by mutableStateOf(EJ4Articulation.ORIGINAL)
    var lastR4Section by mutableStateOf(EJ4Section.C_MAJOR)
    var lastR5Articulation by mutableStateOf(EJ5Articulation.ORIGINAL)
    var lastR5Section by mutableStateOf(EJ4Section.C_MAJOR)

    var lastTonic by mutableStateOf<Tonic?>(null)
    var lastMode by mutableStateOf<ModeType?>(null)
    var lastArticulation by mutableStateOf<ArticulationPattern?>(null)
    var lastModalScheme by mutableStateOf(ModalScheme.EJ4)

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

    // --- E.J. 4, R. 2, R. 4 (8-Articulation) Progress ---
    fun isEJ4Completed(articulation: EJ4Articulation, exercise: ExerciseType = ExerciseType.EJ4): Boolean {
        if (articulation == EJ4Articulation.ORIGINAL) return false
        return when (exercise) {
            ExerciseType.R2 -> r2CompletedSet.contains(articulation.id)
            ExerciseType.R4 -> r4CompletedSet.contains(articulation.id)
            else -> ej4CompletedSet.contains(articulation.id)
        }
    }

    val ej4CompletedCount: Int
        get() = ej4CompletedSet.size

    val isEJ4FullyCompleted: Boolean
        get() = ej4CompletedSet.size == 8

    fun ej4TypeCompletedCount(exercise: ExerciseType): Int = when (exercise) {
        ExerciseType.R2 -> r2CompletedSet.size
        ExerciseType.R4 -> r4CompletedSet.size
        else -> ej4CompletedSet.size
    }

    fun isEJ4TypeFullyCompleted(exercise: ExerciseType): Boolean =
        ej4TypeCompletedCount(exercise) == 8

    fun ej4CompletedCount(exercise: ExerciseType): Int = ej4TypeCompletedCount(exercise)

    fun isEJ4FullyCompleted(exercise: ExerciseType): Boolean = isEJ4TypeFullyCompleted(exercise)

    fun markEJ4Completed(articulation: EJ4Articulation, exercise: ExerciseType = ExerciseType.EJ4) {
        if (articulation != EJ4Articulation.ORIGINAL) {
            when (exercise) {
                ExerciseType.R2 -> {
                    r2CompletedSet = r2CompletedSet + articulation.id
                    lastR2Articulation = articulation
                }
                ExerciseType.R4 -> {
                    r4CompletedSet = r4CompletedSet + articulation.id
                    lastR4Articulation = articulation
                }
                else -> {
                    ej4CompletedSet = ej4CompletedSet + articulation.id
                    lastEJ4Articulation = articulation
                }
            }
        }
        lastExerciseType = exercise
        saveProgress()
    }

    fun unmarkEJ4Completed(articulation: EJ4Articulation, exercise: ExerciseType = ExerciseType.EJ4) {
        when (exercise) {
            ExerciseType.R2 -> r2CompletedSet = r2CompletedSet - articulation.id
            ExerciseType.R4 -> r4CompletedSet = r4CompletedSet - articulation.id
            else -> ej4CompletedSet = ej4CompletedSet - articulation.id
        }
        saveProgress()
    }

    fun toggleEJ4Completed(articulation: EJ4Articulation, exercise: ExerciseType = ExerciseType.EJ4) {
        if (articulation == EJ4Articulation.ORIGINAL) return
        if (isEJ4Completed(articulation, exercise)) {
            unmarkEJ4Completed(articulation, exercise)
        } else {
            markEJ4Completed(articulation, exercise)
        }
    }

    fun resetEJ4(exercise: ExerciseType = ExerciseType.EJ4) {
        when (exercise) {
            ExerciseType.R2 -> r2CompletedSet = emptySet()
            ExerciseType.R4 -> r4CompletedSet = emptySet()
            else -> ej4CompletedSet = emptySet()
        }
        saveProgress()
    }

    // --- E.J. 5, E.J. 10, E.J. 11, R. 1, R. 5 (10-Articulation) Progress ---
    val ej5CompletedCount: Int get() = ej5CompletedSet.size
    val isEJ5FullyCompleted: Boolean get() = ej5CompletedSet.size == 10

    val ej10CompletedCount: Int get() = ej10CompletedSet.size
    val isEJ10FullyCompleted: Boolean get() = ej10CompletedSet.size == 10

    val ej11CompletedCount: Int get() = ej11CompletedSet.size
    val isEJ11FullyCompleted: Boolean get() = ej11CompletedSet.size == 10

    val r1CompletedCount: Int get() = r1CompletedSet.size
    val isR1FullyCompleted: Boolean get() = r1CompletedSet.size == 10

    val r5CompletedCount: Int get() = r5CompletedSet.size
    val isR5FullyCompleted: Boolean get() = r5CompletedSet.size == 10

    fun isEJ5TypeCompleted(articulation: EJ5Articulation, exercise: ExerciseType): Boolean {
        if (articulation == EJ5Articulation.ORIGINAL) return false
        return when (exercise) {
            ExerciseType.EJ5 -> ej5CompletedSet.contains(articulation.id)
            ExerciseType.EJ10 -> ej10CompletedSet.contains(articulation.id)
            ExerciseType.EJ11 -> ej11CompletedSet.contains(articulation.id)
            ExerciseType.R1 -> r1CompletedSet.contains(articulation.id)
            ExerciseType.R5 -> r5CompletedSet.contains(articulation.id)
            else -> false
        }
    }

    fun ej5TypeCompletedCount(exercise: ExerciseType): Int = when (exercise) {
        ExerciseType.EJ5 -> ej5CompletedCount
        ExerciseType.EJ10 -> ej10CompletedCount
        ExerciseType.EJ11 -> ej11CompletedCount
        ExerciseType.R1 -> r1CompletedCount
        ExerciseType.R5 -> r5CompletedCount
        else -> 0
    }

    fun isEJ5TypeFullyCompleted(exercise: ExerciseType): Boolean =
        ej5TypeCompletedCount(exercise) == 10

    fun markEJ5TypeCompleted(articulation: EJ5Articulation, exercise: ExerciseType) {
        if (articulation != EJ5Articulation.ORIGINAL) {
            when (exercise) {
                ExerciseType.EJ5 -> {
                    ej5CompletedSet = ej5CompletedSet + articulation.id
                    lastEJ5Articulation = articulation
                }
                ExerciseType.EJ10 -> {
                    ej10CompletedSet = ej10CompletedSet + articulation.id
                    lastEJ10Articulation = articulation
                }
                ExerciseType.EJ11 -> {
                    ej11CompletedSet = ej11CompletedSet + articulation.id
                    lastEJ11Articulation = articulation
                }
                ExerciseType.R1 -> {
                    r1CompletedSet = r1CompletedSet + articulation.id
                    lastR1Articulation = articulation
                }
                ExerciseType.R5 -> {
                    r5CompletedSet = r5CompletedSet + articulation.id
                    lastR5Articulation = articulation
                }
                else -> {}
            }
        }
        lastExerciseType = exercise
        saveProgress()
    }

    fun unmarkEJ5TypeCompleted(articulation: EJ5Articulation, exercise: ExerciseType) {
        when (exercise) {
            ExerciseType.EJ5 -> ej5CompletedSet = ej5CompletedSet - articulation.id
            ExerciseType.EJ10 -> ej10CompletedSet = ej10CompletedSet - articulation.id
            ExerciseType.EJ11 -> ej11CompletedSet = ej11CompletedSet - articulation.id
            ExerciseType.R1 -> r1CompletedSet = r1CompletedSet - articulation.id
            ExerciseType.R5 -> r5CompletedSet = r5CompletedSet - articulation.id
            else -> {}
        }
        saveProgress()
    }

    fun toggleEJ5TypeCompleted(articulation: EJ5Articulation, exercise: ExerciseType) {
        if (articulation == EJ5Articulation.ORIGINAL) return
        if (isEJ5TypeCompleted(articulation, exercise)) {
            unmarkEJ5TypeCompleted(articulation, exercise)
        } else {
            markEJ5TypeCompleted(articulation, exercise)
        }
    }

    fun resetEJ5Type(exercise: ExerciseType) {
        when (exercise) {
            ExerciseType.EJ5 -> ej5CompletedSet = emptySet()
            ExerciseType.EJ10 -> ej10CompletedSet = emptySet()
            ExerciseType.EJ11 -> ej11CompletedSet = emptySet()
            ExerciseType.R1 -> r1CompletedSet = emptySet()
            ExerciseType.R5 -> r5CompletedSet = emptySet()
            else -> {}
        }
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

    // --- 84 Modos Progress ---
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

        lastExerciseType = ExerciseType.MODOS
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
        ej4CompletedSet = emptySet()
        ej5CompletedSet = emptySet()
        ej10CompletedSet = emptySet()
        ej11CompletedSet = emptySet()
        r1CompletedSet = emptySet()
        r2CompletedSet = emptySet()
        r4CompletedSet = emptySet()
        r5CompletedSet = emptySet()
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
        editor.putString("ej4_completed", ej4CompletedSet.joinToString(","))
        editor.putString("ej5_completed", ej5CompletedSet.joinToString(","))
        editor.putString("ej10_completed", ej10CompletedSet.joinToString(","))
        editor.putString("ej11_completed", ej11CompletedSet.joinToString(","))
        editor.putString("r1_completed", r1CompletedSet.joinToString(","))
        editor.putString("r2_completed", r2CompletedSet.joinToString(","))
        editor.putString("r4_completed", r4CompletedSet.joinToString(","))
        editor.putString("r5_completed", r5CompletedSet.joinToString(","))
        editor.putString("last_exercise_type", lastExerciseType.name)
        editor.putString("last_ej1_articulation", lastEJ1Articulation.name)
        editor.putString("last_ej2_articulation", lastEJ2Articulation.name)
        editor.putString("last_ej4_articulation", lastEJ4Articulation.name)
        editor.putString("last_ej4_section", lastEJ4Section.name)
        editor.putString("last_ej5_articulation", lastEJ5Articulation.name)
        editor.putString("last_ej5_section", lastEJ5Section.name)
        editor.putString("last_ej10_articulation", lastEJ10Articulation.name)
        editor.putString("last_ej10_section", lastEJ10Section.name)
        editor.putString("last_ej11_articulation", lastEJ11Articulation.name)
        editor.putString("last_ej11_section", lastEJ11Section.name)
        editor.putString("last_r1_articulation", lastR1Articulation.name)
        editor.putString("last_r1_section", lastR1Section.name)
        editor.putString("last_r2_articulation", lastR2Articulation.name)
        editor.putString("last_r2_section", lastR2Section.name)
        editor.putString("last_r4_articulation", lastR4Articulation.name)
        editor.putString("last_r4_section", lastR4Section.name)
        editor.putString("last_r5_articulation", lastR5Articulation.name)
        editor.putString("last_r5_section", lastR5Section.name)
        lastTonic?.let { editor.putString("last_tonic", it.name) }
        lastMode?.let { editor.putString("last_mode", it.name) }
        lastArticulation?.let { editor.putString("last_articulation", it.name) }
        editor.putString("last_modal_scheme", lastModalScheme.name)
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
        val ej4Str = prefs.getString("ej4_completed", null)
        if (!ej4Str.isNullOrBlank()) {
            ej4CompletedSet = ej4Str.split(",")
                .mapNotNull { it.trim().toIntOrNull() }
                .filter { it in 1..8 }
                .toSet()
        }
        val r2Str = prefs.getString("r2_completed", null)
        if (!r2Str.isNullOrBlank()) {
            r2CompletedSet = r2Str.split(",")
                .mapNotNull { it.trim().toIntOrNull() }
                .filter { it in 1..8 }
                .toSet()
        }
        val r4Str = prefs.getString("r4_completed", null)
        if (!r4Str.isNullOrBlank()) {
            r4CompletedSet = r4Str.split(",")
                .mapNotNull { it.trim().toIntOrNull() }
                .filter { it in 1..8 }
                .toSet()
        }
        val ej5Str = prefs.getString("ej5_completed", null)
        if (!ej5Str.isNullOrBlank()) {
            ej5CompletedSet = ej5Str.split(",")
                .mapNotNull { it.trim().toIntOrNull() }
                .filter { it in 1..10 }
                .toSet()
        }
        val ej10Str = prefs.getString("ej10_completed", null)
        if (!ej10Str.isNullOrBlank()) {
            ej10CompletedSet = ej10Str.split(",")
                .mapNotNull { it.trim().toIntOrNull() }
                .filter { it in 1..10 }
                .toSet()
        }
        val ej11Str = prefs.getString("ej11_completed", null)
        if (!ej11Str.isNullOrBlank()) {
            ej11CompletedSet = ej11Str.split(",")
                .mapNotNull { it.trim().toIntOrNull() }
                .filter { it in 1..10 }
                .toSet()
        }
        val r1Str = prefs.getString("r1_completed", null)
        if (!r1Str.isNullOrBlank()) {
            r1CompletedSet = r1Str.split(",")
                .mapNotNull { it.trim().toIntOrNull() }
                .filter { it in 1..10 }
                .toSet()
        }
        val r5Str = prefs.getString("r5_completed", null)
        if (!r5Str.isNullOrBlank()) {
            r5CompletedSet = r5Str.split(",")
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
        val ej4ArtStr = prefs.getString("last_ej4_articulation", null)
        if (ej4ArtStr != null) {
            lastEJ4Articulation = runCatching { EJ4Articulation.valueOf(ej4ArtStr) }.getOrDefault(EJ4Articulation.ORIGINAL)
        }
        val ej4SecStr = prefs.getString("last_ej4_section", null)
        if (ej4SecStr != null) {
            lastEJ4Section = runCatching { EJ4Section.valueOf(ej4SecStr) }.getOrDefault(EJ4Section.C_MAJOR)
        }
        val ej5ArtStr = prefs.getString("last_ej5_articulation", null)
        if (ej5ArtStr != null) {
            lastEJ5Articulation = runCatching { EJ5Articulation.valueOf(ej5ArtStr) }.getOrDefault(EJ5Articulation.ORIGINAL)
        }
        val ej5SecStr = prefs.getString("last_ej5_section", null)
        if (ej5SecStr != null) {
            lastEJ5Section = runCatching { EJ5Section.valueOf(ej5SecStr) }.getOrDefault(EJ5Section.C_CHROM)
        }
        val ej10ArtStr = prefs.getString("last_ej10_articulation", null)
        if (ej10ArtStr != null) {
            lastEJ10Articulation = runCatching { EJ5Articulation.valueOf(ej10ArtStr) }.getOrDefault(EJ5Articulation.ORIGINAL)
        }
        val ej10SecStr = prefs.getString("last_ej10_section", null)
        if (ej10SecStr != null) {
            lastEJ10Section = runCatching { EJ10Section.valueOf(ej10SecStr) }.getOrDefault(EJ10Section.C_ARP)
        }
        val ej11ArtStr = prefs.getString("last_ej11_articulation", null)
        if (ej11ArtStr != null) {
            lastEJ11Articulation = runCatching { EJ5Articulation.valueOf(ej11ArtStr) }.getOrDefault(EJ5Articulation.ORIGINAL)
        }
        val ej11SecStr = prefs.getString("last_ej11_section", null)
        if (ej11SecStr != null) {
            lastEJ11Section = runCatching { EJ10Section.valueOf(ej11SecStr) }.getOrDefault(EJ10Section.C_ARP)
        }
        val r1ArtStr = prefs.getString("last_r1_articulation", null)
        if (r1ArtStr != null) {
            lastR1Articulation = runCatching { EJ5Articulation.valueOf(r1ArtStr) }.getOrDefault(EJ5Articulation.ORIGINAL)
        }
        val r1SecStr = prefs.getString("last_r1_section", null)
        if (r1SecStr != null) {
            lastR1Section = runCatching { EJ4Section.valueOf(r1SecStr) }.getOrDefault(EJ4Section.C_MAJOR)
        }
        val r2ArtStr = prefs.getString("last_r2_articulation", null)
        if (r2ArtStr != null) {
            lastR2Articulation = runCatching { EJ4Articulation.valueOf(r2ArtStr) }.getOrDefault(EJ4Articulation.ORIGINAL)
        }
        val r2SecStr = prefs.getString("last_r2_section", null)
        if (r2SecStr != null) {
            lastR2Section = runCatching { EJ4Section.valueOf(r2SecStr) }.getOrDefault(EJ4Section.C_MAJOR)
        }
        val r4ArtStr = prefs.getString("last_r4_articulation", null)
        if (r4ArtStr != null) {
            lastR4Articulation = runCatching { EJ4Articulation.valueOf(r4ArtStr) }.getOrDefault(EJ4Articulation.ORIGINAL)
        }
        val r4SecStr = prefs.getString("last_r4_section", null)
        if (r4SecStr != null) {
            lastR4Section = runCatching { EJ4Section.valueOf(r4SecStr) }.getOrDefault(EJ4Section.C_MAJOR)
        }
        val r5ArtStr = prefs.getString("last_r5_articulation", null)
        if (r5ArtStr != null) {
            lastR5Articulation = runCatching { EJ5Articulation.valueOf(r5ArtStr) }.getOrDefault(EJ5Articulation.ORIGINAL)
        }
        val r5SecStr = prefs.getString("last_r5_section", null)
        if (r5SecStr != null) {
            lastR5Section = runCatching { EJ4Section.valueOf(r5SecStr) }.getOrDefault(EJ4Section.C_MAJOR)
        }
        val tStr = prefs.getString("last_tonic", null)
        val mStr = prefs.getString("last_mode", null)
        val aStr = prefs.getString("last_articulation", null)
        val msStr = prefs.getString("last_modal_scheme", null)

        if (tStr != null) lastTonic = runCatching { Tonic.valueOf(tStr) }.getOrNull()
        if (mStr != null) lastMode = runCatching { ModeType.valueOf(mStr) }.getOrNull()
        if (aStr != null) lastArticulation = runCatching { ArticulationPattern.valueOf(aStr) }.getOrNull()
        if (msStr != null) lastModalScheme = runCatching { ModalScheme.valueOf(msStr) }.getOrDefault(ModalScheme.EJ4)
    }
}
