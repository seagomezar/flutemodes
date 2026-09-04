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
        lastTonic = null
        lastMode = null
        lastArticulation = null
        prefs.edit().clear().apply()
    }

    private fun saveProgress() {
        val editor = prefs.edit()
        for ((k, v) in completedMap) {
            editor.putString("cell_$k", v.joinToString(","))
        }
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
        val tStr = prefs.getString("last_tonic", null)
        val mStr = prefs.getString("last_mode", null)
        val aStr = prefs.getString("last_articulation", null)

        if (tStr != null) lastTonic = runCatching { Tonic.valueOf(tStr) }.getOrNull()
        if (mStr != null) lastMode = runCatching { ModeType.valueOf(mStr) }.getOrNull()
        if (aStr != null) lastArticulation = runCatching { ArticulationPattern.valueOf(aStr) }.getOrNull()
    }
}
