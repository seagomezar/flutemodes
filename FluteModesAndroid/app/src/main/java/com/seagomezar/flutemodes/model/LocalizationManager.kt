package com.seagomezar.flutemodes.model

import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue

enum class AppLanguage(val code: String, val displayName: String, val flag: String) {
    SPANISH("es", "Español", "🇪🇸"),
    ENGLISH("en", "English", "🇬🇧")
}

class LocalizationManager(context: Context) {
    private val prefs = context.getSharedPreferences("FluteModes_Locale", Context.MODE_PRIVATE)

    var currentLanguage by mutableStateOf(
        if (prefs.getString("lang", "es") == "en") AppLanguage.ENGLISH else AppLanguage.SPANISH
    )
        private set

    fun toggleLanguage() {
        currentLanguage = if (currentLanguage == AppLanguage.SPANISH) AppLanguage.ENGLISH else AppLanguage.SPANISH
        prefs.edit().putString("lang", currentLanguage.code).apply()
    }

    fun t(key: String): String {
        val isEn = currentLanguage == AppLanguage.ENGLISH
        val pair = strings[key] ?: return key
        return if (isEn) pair.second else pair.first
    }

    private val strings = mapOf(
        // App General
        "app_name" to Pair("FluteModes", "FluteModes"),
        "subtitle" to Pair(
            "Estudio Diario N° 4 · Paul Taffanel & Philippe Gaubert",
            "Daily Exercise No. 4 · Paul Taffanel & Philippe Gaubert"
        ),
        "sub_desc" to Pair(
            "Sistema paralelo del Maestro León Giraldo · 84 Modos (12 Tónicas × 7 Modos)",
            "Maestro León Giraldo's Parallel System · 84 Modes (12 Tonics × 7 Modes)"
        ),

        // Home View
        "select_tonic" to Pair("Selecciona una Tónica", "Select a Tonic"),
        "major_family" to Pair("Familia Mayor (3 Modos)", "Major Family (3 Modes)"),
        "minor_family" to Pair("Familia Menor (4 Modos)", "Minor Family (4 Modes)"),
        "fixed_key" to Pair("Armadura fija:", "Fixed key signature:"),
        "start_practice" to Pair("Comenzar Práctica", "Start Practicing"),
        "practice_matrix" to Pair("Matriz de Progreso (84 Modos)", "Progress Matrix (84 Modes)"),
        "resuming" to Pair("Reanudando:", "Resuming:"),

        // Practice View
        "back" to Pair("Atrás", "Back"),
        "modes_count" to Pair("modos", "modes"),
        "play_piano" to Pair("Reproducir Piano", "Play Piano"),
        "stop_piano" to Pair("Detener Piano", "Stop Piano"),
        "next_art" to Pair("Siguiente Articulación", "Next Articulation"),
        "complete_and_next" to Pair("Completar y Siguiente Modo", "Complete & Next Mode"),
        "seven_modes_completed" to Pair("7 Modos Completados", "7 Modes Completed"),
        "milestone_title" to Pair("¡7 Modos Completados en %s!", "7 Modes Completed in %s!"),
        "milestone_msg" to Pair(
            "Has tocado los 7 modos de %s (%d/56 articulaciones completadas en esta nota). ¿Qué deseas hacer a continuación?",
            "You have practiced all 7 modes of %s (%d/56 articulations completed for this note). What would you like to do next?"
        ),
        "next_round" to Pair("🔁 Siguiente Ronda de Articulaciones", "🔁 Next Articulation Round"),
        "advance_tonic" to Pair("🎵 Avanzar a %s (Siguiente Tónica)", "🎵 Advance to %s (Next Tonic)"),
        "stay_mode" to Pair("Continuar en este modo", "Stay in this mode"),

        // Modes
        "mode_1_name" to Pair("Jónico (Mayor)", "Ionian (Major)"),
        "mode_2_name" to Pair("Lidio", "Lydian"),
        "mode_3_name" to Pair("Mixolidio", "Mixolydian"),
        "mode_4_name" to Pair("Dórico", "Dorian"),
        "mode_5_name" to Pair("Eólico (Menor Natural)", "Aeolian (Natural Minor)"),
        "mode_6_name" to Pair("Frigio", "Phrygian"),
        "mode_7_name" to Pair("Lócrio", "Locrian"),

        // Accidental Badges
        "acc_ionian" to Pair("Sin alteraciones accidentales", "No accidental alterations"),
        "acc_lydian" to Pair("Cuarta aumentada (♯4) accidental", "Augmented fourth (♯4) accidental"),
        "acc_mixolydian" to Pair("Séptima menor (♭7) accidental", "Minor seventh (♭7) accidental"),
        "acc_dorian" to Pair("Sexta mayor (6) accidental", "Major sixth (6) accidental"),
        "acc_aeolian" to Pair("Menor natural sin alteraciones", "Natural minor without accidentals"),
        "acc_phrygian" to Pair("Segunda menor (♭2) accidental", "Minor second (♭2) accidental"),
        "acc_locrian" to Pair("Segunda menor (♭2) y Quinta disminuida (♭5)", "Minor second (♭2) & Diminished fifth (♭5)"),

        // Articulations (short)
        "art_1_short" to Pair("Toda ligada", "All slurred"),
        "art_2_short" to Pair("Ligado 4 y 4", "Slurred 4 & 4"),
        "art_3_short" to Pair("Lig. 2, pic. 2", "Slur 2, stacc. 2"),
        "art_4_short" to Pair("Pic. 1, lig. 2, pic. 1", "Stacc. 1, slur 2, stacc. 1"),
        "art_5_short" to Pair("Pic. 2, lig. 2", "Stacc. 2, slur 2"),
        "art_6_short" to Pair("Pic. 1, lig. 3", "Stacc. 1, slur 3"),
        "art_7_short" to Pair("Lig. 3, pic. 1", "Slur 3, stacc. 1"),
        "art_8_short" to Pair("Toda picada", "All staccato"),

        // Matrix View
        "matrix_title" to Pair("Matriz de Estudio Modal", "Modal Study Matrix"),
        "matrix_stats" to Pair("Completadas: %d de %d articulaciones (%d%%)", "Completed: %d of %d articulations (%d%%)"),
        "reset_all" to Pair("Resetear Todo", "Reset All"),
        "reset_confirm_title" to Pair("¿Resetear todo el progreso?", "Reset all progress?"),
        "reset_confirm_msg" to Pair(
            "Esta acción borrará todas las marcas de estudio registradas y comenzará de cero.",
            "This action will erase all completed practice records and restart from scratch."
        ),
        "cancel" to Pair("Cancelar", "Cancel"),
        "delete" to Pair("Borrar", "Delete")
    )
}
