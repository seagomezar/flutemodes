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

    internal val strings = mapOf(
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
        "next_art" to Pair("Siguiente Art.", "Next Art."),
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
        "delete" to Pair("Borrar", "Delete"),

        // Settings
        "settings_title" to Pair("Ajustes de Estudio", "Practice Settings"),
        "keep_screen_awake" to Pair("Mantener pantalla activa", "Keep screen awake"),
        "keep_screen_awake_desc" to Pair("Evita que el dispositivo entre en modo reposo", "Prevents device from sleeping during practice"),
        "metronome_title" to Pair("Metrónomo (Blanca)", "Metronome (Half note)"),
        "click_sound" to Pair("Sonido de Clic", "Click Sound"),

        // Articulation Progress Clarity
        "arts_count" to Pair("arts.", "arts."),
        "articulations_title" to Pair("Fórmulas de Articulación", "Articulation Patterns"),
        "arts_completed_badge" to Pair("%d/8 arts. completadas", "%d/8 arts. completed"),
        "next_mode" to Pair("Siguiente Modo", "Next Mode"),
        "mode_done" to Pair("Modo Listo", "Mode Done"),
        "mode_fully_done" to Pair("Modo Completado", "Mode Completed"),
        "legend_completed" to Pair("Completado (8/8 arts.)", "Completed (8/8 arts)"),
        "legend_in_progress" to Pair("En Progreso (1-7/8 arts.)", "In Progress (1-7/8 arts)"),
        "legend_not_started" to Pair("No iniciado (0/8 arts.)", "Not started (0/8 arts)"),
        "completed" to Pair("Completada", "Completed"),
        "in_progress" to Pair("En curso", "Current"),

        // E.J. 1 Taffanel & Gaubert (A. L. 16.588)
        "ej1_title" to Pair(
            "E. J. 1 · Paul Taffanel & Philippe Gaubert (A. L. 16.588)",
            "E. J. 1 · Paul Taffanel & Philippe Gaubert (A. L. 16.588)"
        ),
        "ej1_sub_desc" to Pair(
            "17 Grands Exercices Journaliers de Mécanisme · 31 Compases Cromáticos + 10 Articulaciones",
            "17 Grands Exercices Journaliers de Mécanisme · 31 Chromatic Measures + 10 Articulations"
        ),
        "ej1_header_info" to Pair(
            "15 Pares Cromáticos (Fa4–Sol♭6) · Reprise à l'octave · 8va (Compases 25–31)",
            "15 Chromatic Pairs (F4–G♭6) · Reprise à l'octave · 8va (Measures 25–31)"
        ),
        "ej1_select_art" to Pair(
            "Las 10 Articulaciones Oficiales (A. L. 16.588)",
            "The 10 Official Articulations (A. L. 16.588)"
        ),
        "ej1_start_practice" to Pair("Practicar E. J. 1", "Practice E. J. 1"),
        "ej1_ten_arts_completed" to Pair("10 Articulaciones Completadas", "10 Articulations Completed"),
        "ej1_milestone_title" to Pair("¡E. J. 1 Completado (10/10 Articulaciones)!", "E. J. 1 Completed (10/10 Articulations)!"),
        "ej1_milestone_msg" to Pair(
            "Has completado las 10 articulaciones oficiales del Ejercicio Diario N° 1 de Taffanel & Gaubert.",
            "You have completed all 10 official articulations of Taffanel & Gaubert's Daily Exercise No. 1."
        ),
        "ej1_restart_round" to Pair("🔁 Reiniciar las 10 Articulaciones", "🔁 Restart 10 Articulations"),
        "ej1_go_to_ej2" to Pair("🎵 Ir a E. J. 2 (Pentacordios Menores)", "🎵 Go to E. J. 2 (Minor Pentachords)"),
        "ej1_go_to_ej4" to Pair("🎵 Ir a E. J. 4 (84 Modos Paralelos)", "🎵 Go to E. J. 4 (84 Parallel Modes)"),

        // E.J. 2 Taffanel & Gaubert (A. L. 16.588)
        "ej2_title" to Pair(
            "E. J. 2 · Paul Taffanel & Philippe Gaubert (A. L. 16.588)",
            "E. J. 2 · Paul Taffanel & Philippe Gaubert (A. L. 16.588)"
        ),
        "ej2_sub_desc" to Pair(
            "Pentacordios Menores y 7ª Disminuida · 31 Compases Cromáticos + 10 Articulaciones",
            "Minor Pentachords & Diminished 7th · 31 Chromatic Measures + 10 Articulations"
        ),
        "ej2_header_info" to Pair(
            "15 Pares Cromáticos Menores (Re menor–Mi menor) · 8va (Compases 25–31)",
            "15 Minor Chromatic Pairs (D minor–E minor) · 8va (Measures 25–31)"
        ),
        "ej2_select_art" to Pair(
            "Las 10 Articulaciones Oficiales (A. L. 16.588)",
            "The 10 Official Articulations (A. L. 16.588)"
        ),
        "ej2_start_practice" to Pair("Practicar E. J. 2", "Practice E. J. 2"),
        "ej2_ten_arts_completed" to Pair("10 Articulaciones Completadas", "10 Articulations Completed"),
        "ej2_milestone_title" to Pair("¡E. J. 2 Completado (10/10 Articulaciones)!", "E. J. 2 Completed (10/10 Articulations)!"),
        "ej2_milestone_msg" to Pair(
            "Has completado las 10 articulaciones oficiales del Ejercicio Diario N° 2 de Taffanel & Gaubert.",
            "You have completed all 10 official articulations of Taffanel & Gaubert's Daily Exercise No. 2."
        ),
        "ej2_restart_round" to Pair("🔁 Reiniciar las 10 Articulaciones", "🔁 Restart 10 Articulations"),
        "ej2_go_to_ej4" to Pair("🎵 Ir a E. J. 4 (84 Modos Paralelos)", "🎵 Go to E. J. 4 (84 Parallel Modes)"),

        "ej1_art_0_title" to Pair("0. Edición Original Leduc (4 ligadas + 4 picadas)", "0. Original Leduc Edition (4 slurred + 4 staccato)"),
        "ej1_art_1_title" to Pair("1. Ocho notas ligadas", "1. Eight notes slurred"),
        "ej1_art_2_title" to Pair("2. Cuatro y cuatro ligadas", "2. Four & four slurred"),
        "ej1_art_3_title" to Pair("3. Una picada y tres ligadas", "3. One staccato & three slurred"),
        "ej1_art_4_title" to Pair("4. Tres ligadas y una picada", "4. Three slurred & one staccato"),
        "ej1_art_5_title" to Pair("5. Dos ligadas y dos picadas", "5. Two slurred & two staccato"),
        "ej1_art_6_title" to Pair("6. Dos picadas y dos ligadas", "6. Two staccato & two slurred"),
        "ej1_art_7_title" to Pair("7. Una picada, dos ligadas y una picada", "7. One staccato, two slurred & one staccato"),
        "ej1_art_8_title" to Pair("8. De dos en dos ligadas", "8. Slurred in pairs (2 by 2)"),
        "ej1_art_9_title" to Pair("9. De dos en dos sincopadas", "9. Syncopated pairs"),
        "ej1_art_10_title" to Pair("10. Todo picado (Staccato)", "10. All staccato"),

        "ej1_art_0_short" to Pair("0. Original (4 lig + 4 pic)", "0. Original (4 slur + 4 stacc)"),
        "ej1_art_1_short" to Pair("1. 8 ligadas", "1. 8 slurred"),
        "ej1_art_2_short" to Pair("2. 4 y 4 ligadas", "2. 4 & 4 slurred"),
        "ej1_art_3_short" to Pair("3. 1 pic., 3 lig.", "3. 1 stacc., 3 slur"),
        "ej1_art_4_short" to Pair("4. 3 lig., 1 pic.", "4. 3 slur, 1 stacc."),
        "ej1_art_5_short" to Pair("5. 2 lig., 2 pic.", "5. 2 slur, 2 stacc."),
        "ej1_art_6_short" to Pair("6. 2 pic., 2 lig.", "6. 2 stacc., 2 slur"),
        "ej1_art_7_short" to Pair("7. 1 pic., 2 lig., 1 pic.", "7. 1 stacc., 2 slur, 1 stacc."),
        "ej1_art_8_short" to Pair("8. De 2 en 2 ligadas", "8. Pairs (2 by 2)"),
        "ej1_art_9_short" to Pair("9. De 2 en 2 sincopadas", "9. Syncopated pairs"),
        "ej1_art_10_short" to Pair("10. Todo picado", "10. All staccato")
    )
}
