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
            "Sistema Modal Paralelo · 84 Modos (12 Tónicas × 7 Modos)",
            "Parallel Modal System · 84 Modes (12 Tonics × 7 Modes)"
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
        "art_1_short" to Pair("8 Lig.", "8 Slur"),
        "art_2_short" to Pair("4+4", "4+4"),
        "art_3_short" to Pair("2L+2P", "2S+2P"),
        "art_4_short" to Pair("1P+2L+1P", "1P+2S+1P"),
        "art_5_short" to Pair("2P+2L", "2P+2S"),
        "art_6_short" to Pair("1P+3L", "1P+3S"),
        "art_7_short" to Pair("3L+1P", "3S+1P"),
        "art_8_short" to Pair("Stacc.", "Stacc."),

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

        // E.J. 1 Taffanel & Gaubert
        "ej1_title" to Pair(
            "E. J. 1 · Paul Taffanel & Philippe Gaubert",
            "E. J. 1 · Paul Taffanel & Philippe Gaubert"
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
            "Las 10 Articulaciones Oficiales (E. J. 1)",
            "The 10 Official Articulations (E. J. 1)"
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
        "ej1_go_to_ej4" to Pair("🎵 Ir a E. J. 4 (Escalas Diatónicas)", "🎵 Go to E. J. 4 (Diatonic Scales)"),

        // E.J. 2 Taffanel & Gaubert
        "ej2_title" to Pair(
            "E. J. 2 · Paul Taffanel & Philippe Gaubert",
            "E. J. 2 · Paul Taffanel & Philippe Gaubert"
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
            "Las 10 Articulaciones Oficiales (E. J. 2)",
            "The 10 Official Articulations (E. J. 2)"
        ),
        "ej2_start_practice" to Pair("Practicar E. J. 2", "Practice E. J. 2"),
        "ej2_ten_arts_completed" to Pair("10 Articulaciones Completadas", "10 Articulations Completed"),
        "ej2_milestone_title" to Pair("¡E. J. 2 Completado (10/10 Articulaciones)!", "E. J. 2 Completed (10/10 Articulations)!"),
        "ej2_milestone_msg" to Pair(
            "Has completado las 10 articulaciones oficiales del Ejercicio Diario N° 2 de Taffanel & Gaubert.",
            "You have completed all 10 official articulations of Taffanel & Gaubert's Daily Exercise No. 2."
        ),
        "ej2_restart_round" to Pair("🔁 Reiniciar las 10 Articulaciones", "🔁 Restart 10 Articulations"),
        "ej2_go_to_ej4" to Pair("🎵 Ir a E. J. 4 (Escalas Diatónicas)", "🎵 Go to E. J. 4 (Diatonic Scales)"),

        // E.J. 4 Taffanel & Gaubert
        "ej4_title" to Pair(
            "E. J. 4 · Paul Taffanel & Philippe Gaubert",
            "E. J. 4 · Paul Taffanel & Philippe Gaubert"
        ),
        "ej4_sub_desc" to Pair(
            "Escalas Diatónicas en 24 Tonalidades Mayores y Menores Relativas + Coda (194 compases · 8 articulaciones oficiales)",
            "Diatonic Scales across 24 Major & Relative Minor Keys + Coda (194 measures · 8 official articulations)"
        ),
        "ej4_header_info" to Pair(
            "24 Tonalidades (Mayores y Menores: armónica en c. 1 y 7, melódica/natural) · 194 Compases · 8 Articulaciones",
            "24 Keys (Major & Minor: harmonic in m. 1 & 7, melodic/natural) · 194 Measures · 8 Articulations"
        ),
        "ej4_select_section" to Pair(
            "25 Secciones Tonales (194 Compases)",
            "25 Tonal Sections (194 Measures)"
        ),
        "ej4_select_art" to Pair(
            "Las 8 Articulaciones Oficiales (E. J. 4)",
            "The 8 Official Articulations (E. J. 4)"
        ),
        "ej4_start_practice" to Pair("Practicar E. J. 4", "Practice E. J. 4"),
        "ej4_eight_arts_completed" to Pair("8 Articulaciones Completadas", "8 Articulations Completed"),
        "ej4_milestone_title" to Pair("¡E. J. 4 Completado (8/8 Articulaciones)!", "E. J. 4 Completed (8/8 Articulations)!"),
        "ej4_milestone_msg" to Pair(
            "Has completado las 8 articulaciones oficiales del Ejercicio Diario N° 4 de Taffanel & Gaubert (194 compases).",
            "You have completed all 8 official articulations of Taffanel & Gaubert's Daily Exercise No. 4 (194 measures)."
        ),
        "ej4_restart_round" to Pair("🔁 Reiniciar las 8 Articulaciones", "🔁 Restart 8 Articulations"),
        "ej4_go_to_modos" to Pair("🎵 Ir a 84 Modos Paralelos", "🎵 Go to 84 Parallel Modes"),
        "ej4_next_section" to Pair("Siguiente Tonalidad", "Next Tonality"),

        // E.J. 5 Taffanel & Gaubert
        "ej5_title" to Pair(
            "E. J. 5 · Paul Taffanel & Philippe Gaubert",
            "E. J. 5 · Paul Taffanel & Philippe Gaubert"
        ),
        "ej5_sub_desc" to Pair(
            "Escalas Cromáticas (Gammes Chromatiques) · 12 Escalas A–L (60 compases · 6/8 & 2/4 · 10 articulaciones oficiales)",
            "Chromatic Scales (Gammes Chromatiques) · 12 Scales A–L (60 measures · 6/8 & 2/4 · 10 official articulations)"
        ),
        "ej5_header_info" to Pair(
            "12 Escalas Cromáticas (Do a Si · 2 Octavas + Reprise à l'octave) · 60 Compases · 10 Articulaciones",
            "12 Chromatic Scales (C to B · 2 Octaves + Reprise à l'octave) · 60 Measures · 10 Articulations"
        ),
        "ej5_select_section" to Pair(
            "12 Escalas Cromáticas (A–L · 60 Compases)",
            "12 Chromatic Scales (A–L · 60 Measures)"
        ),
        "ej5_select_art" to Pair(
            "Las 10 Articulaciones Oficiales (E. J. 5)",
            "The 10 Official Articulations (E. J. 5)"
        ),
        "ej5_start_practice" to Pair("Practicar E. J. 5", "Practice E. J. 5"),
        "ej5_ten_arts_completed" to Pair("10 Articulaciones Completadas", "10 Articulations Completed"),
        "ej5_milestone_title" to Pair("¡E. J. 5 Completado (10/10 Articulaciones)!", "E. J. 5 Completed (10/10 Articulations)!"),
        "ej5_milestone_msg" to Pair(
            "Has completado las 10 articulaciones oficiales del Ejercicio Diario N° 5 de Taffanel & Gaubert.",
            "You have completed all 10 official articulations of Taffanel & Gaubert's Daily Exercise No. 5."
        ),
        "ej5_restart_round" to Pair("🔁 Reiniciar las 10 Articulaciones", "🔁 Restart 10 Articulations"),
        "ej5_go_to_ej10" to Pair("🎵 Ir a E. J. 10 (Arpegios)", "🎵 Go to E. J. 10 (Arpeggios)"),
        "ej5_next_section" to Pair("Siguiente Escala (Cromática)", "Next Scale (Chromatic)"),

        // E.J. 10 Taffanel & Gaubert
        "ej10_title" to Pair(
            "E. J. 10 · Paul Taffanel & Philippe Gaubert",
            "E. J. 10 · Paul Taffanel & Philippe Gaubert"
        ),
        "ej10_sub_desc" to Pair(
            "Arpegios Progresivos de 2 Octavas (Arpèges) · 12 Series Cromáticas (121 compases · 6/8 & 2/4 · 10 articulaciones)",
            "2-Octave Progressive Arpeggios (Arpèges) · 12 Chromatic Series (121 measures · 6/8 & 2/4 · 10 articulations)"
        ),
        "ej10_header_info" to Pair(
            "12 Series Cromáticas (Do a Si · 10 acordes por grado + Coda) · 121 Compases · 10 Articulaciones",
            "12 Chromatic Series (C to B · 10 chords per degree + Coda) · 121 Measures · 10 Articulations"
        ),
        "ej10_select_section" to Pair(
            "12 Series de Arpegios (121 Compases)",
            "12 Arpeggio Series (121 Measures)"
        ),
        "ej10_select_art" to Pair(
            "Las 10 Articulaciones Oficiales (E. J. 10)",
            "The 10 Official Articulations (E. J. 10)"
        ),
        "ej10_start_practice" to Pair("Practicar E. J. 10", "Practice E. J. 10"),
        "ej10_ten_arts_completed" to Pair("10 Articulaciones Completadas", "10 Articulations Completed"),
        "ej10_milestone_title" to Pair("¡E. J. 10 Completado (10/10 Articulaciones)!", "E. J. 10 Completed (10/10 Articulations)!"),
        "ej10_milestone_msg" to Pair(
            "Has completado las 10 articulaciones oficiales del Ejercicio Diario N° 10 de Taffanel & Gaubert.",
            "You have completed all 10 official articulations of Taffanel & Gaubert's Daily Exercise No. 10."
        ),
        "ej10_restart_round" to Pair("🔁 Reiniciar las 10 Articulaciones", "🔁 Restart 10 Articulations"),
        "ej10_go_to_ej11" to Pair("🎵 Ir a E. J. 11 (Arpegios Quebrados)", "🎵 Go to E. J. 11 (Broken Arpeggios)"),
        "ej10_next_section" to Pair("Siguiente Serie de Arpegios", "Next Arpeggio Series"),

        // E.J. 11 Taffanel & Gaubert
        "ej11_title" to Pair(
            "E. J. 11 · Paul Taffanel & Philippe Gaubert",
            "E. J. 11 · Paul Taffanel & Philippe Gaubert"
        ),
        "ej11_sub_desc" to Pair(
            "Arpegios Quebrados (Arpèges Brisés) · 12 Series Cromáticas (121 compases · 9/8 & 3/4 · 10 articulaciones)",
            "Broken Arpeggios (Arpèges Brisés) · 12 Chromatic Series (121 measures · 9/8 & 3/4 · 10 articulations)"
        ),
        "ej11_header_info" to Pair(
            "12 Series Cromáticas en 9/8 y 3/4 (18 semicorcheas por compás + Coda) · 121 Compases · 10 Articulaciones",
            "12 Chromatic Series in 9/8 & 3/4 (18 sixteenths per measure + Coda) · 121 Measures · 10 Articulations"
        ),
        "ej11_select_section" to Pair(
            "12 Series de Arpegios Quebrados (121 Compases)",
            "12 Broken Arpeggio Series (121 Measures)"
        ),
        "ej11_select_art" to Pair(
            "Las 10 Articulaciones Oficiales (E. J. 11)",
            "The 10 Official Articulations (E. J. 11)"
        ),
        "ej11_start_practice" to Pair("Practicar E. J. 11", "Practice E. J. 11"),
        "ej11_ten_arts_completed" to Pair("10 Articulaciones Completadas", "10 Articulations Completed"),
        "ej11_milestone_title" to Pair("¡E. J. 11 Completado (10/10 Articulaciones)!", "E. J. 11 Completed (10/10 Articulations)!"),
        "ej11_milestone_msg" to Pair(
            "Has completado las 10 articulaciones oficiales del Ejercicio Diario N° 11 de Taffanel & Gaubert.",
            "You have completed all 10 official articulations of Taffanel & Gaubert's Daily Exercise No. 11."
        ),
        "ej11_restart_round" to Pair("🔁 Reiniciar las 10 Articulaciones", "🔁 Restart 10 Articulations"),
        "ej11_go_to_r1" to Pair("🎵 Ir a Reichert 1 (Op. 5)", "🎵 Go to Reichert 1 (Op. 5)"),
        "ej11_next_section" to Pair("Siguiente Serie de Arpegios Quebrados", "Next Broken Arpeggio Series"),

        // Reichert 7 Exercices Journaliers Op. 5
        "r1_title" to Pair(
            "R. 1 · Mathieu-André Reichert (Op. 5 Nº 1, págs. 2–3)",
            "R. 1 · Mathieu-André Reichert (Op. 5 No. 1, pp. 2–3)"
        ),
        "r1_sub_desc" to Pair(
            "7 Exercices Journaliers pour la Flûte · 24 Tonalidades + D.S. al Fine (100 compases · 6/8 & 2/4 · 10 articulaciones)",
            "7 Exercices Journaliers pour la Flûte · 24 Keys + D.S. al Fine (100 measures · 6/8 & 2/4 · 10 articulations)"
        ),
        "r1_header_info" to Pair(
            "24 Tonalidades (4 compases por tonalidad + D.S. al Fine) · 100 Compases · 10 Articulaciones",
            "24 Keys (4 measures per key + D.S. al Fine) · 100 Measures · 10 Articulations"
        ),
        "r1_select_section" to Pair("25 Secciones Tonales (100 Compases · R. 1)", "25 Tonal Sections (100 Measures · R. 1)"),
        "r1_select_art" to Pair("Las 10 Articulaciones de Práctica (R. 1)", "The 10 Practice Articulations (R. 1)"),
        "r1_start_practice" to Pair("Practicar R. 1 (Reichert Op. 5)", "Practice R. 1 (Reichert Op. 5)"),

        "r2_title" to Pair(
            "R. 2 · Mathieu-André Reichert (Op. 5 Nº 2, págs. 4–5)",
            "R. 2 · Mathieu-André Reichert (Op. 5 No. 2, pp. 4–5)"
        ),
        "r2_sub_desc" to Pair(
            "7 Exercices Journaliers pour la Flûte · 24 Tonalidades + D.S. al Fine (200 compases · 2/4 · 8 articulaciones)",
            "7 Exercices Journaliers pour la Flûte · 24 Keys + D.S. al Fine (200 measures · 2/4 · 8 articulations)"
        ),
        "r2_header_info" to Pair(
            "24 Tonalidades con Anacrusa (8 compases por tonalidad + D.S. al Fine) · 200 Compases · 8 Articulaciones",
            "24 Keys with Pickup (8 measures per key + D.S. al Fine) · 200 Measures · 8 Articulations"
        ),
        "r2_select_section" to Pair("25 Secciones Tonales (200 Compases · R. 2)", "25 Tonal Sections (200 Measures · R. 2)"),
        "r2_select_art" to Pair("Las 8 Articulaciones de Práctica (R. 2)", "The 8 Practice Articulations (R. 2)"),
        "r2_start_practice" to Pair("Practicar R. 2 (Reichert Op. 5)", "Practice R. 2 (Reichert Op. 5)"),

        "r4_title" to Pair(
            "R. 4 · Mathieu-André Reichert (Op. 5 Nº 4, págs. 8–9)",
            "R. 4 · Mathieu-André Reichert (Op. 5 No. 4, pp. 8–9)"
        ),
        "r4_sub_desc" to Pair(
            "7 Exercices Journaliers pour la Flûte · 24 Tonalidades + D.S. al Fine (100 compases · 4/4 · 8 articulaciones)",
            "7 Exercices Journaliers pour la Flûte · 24 Keys + D.S. al Fine (100 measures · 4/4 · 8 articulations)"
        ),
        "r4_header_info" to Pair(
            "24 Tonalidades en 4/4 (4 compases por tonalidad + D.S. al Fine) · 100 Compases · 8 Articulaciones",
            "24 Keys in 4/4 (4 measures per key + D.S. al Fine) · 100 Measures · 8 Articulations"
        ),
        "r4_select_section" to Pair("25 Secciones Tonales (100 Compases · R. 4)", "25 Tonal Sections (100 Measures · R. 4)"),
        "r4_select_art" to Pair("Las 8 Articulaciones de Práctica (R. 4)", "The 8 Practice Articulations (R. 4)"),
        "r4_start_practice" to Pair("Practicar R. 4 (Reichert Op. 5)", "Practice R. 4 (Reichert Op. 5)"),

        "r5_title" to Pair(
            "R. 5 · Mathieu-André Reichert (Op. 5 Nº 5, págs. 10–13)",
            "R. 5 · Mathieu-André Reichert (Op. 5 No. 5, pp. 10–13)"
        ),
        "r5_sub_desc" to Pair(
            "7 Exercices Journaliers pour la Flûte · 24 Tonalidades + D.S. al Fine (200 compases · Tresillos en 2/4 · 10 articulaciones)",
            "7 Exercices Journaliers pour la Flûte · 24 Keys + D.S. al Fine (200 measures · 2/4 Triplets · 10 articulations)"
        ),
        "r5_header_info" to Pair(
            "24 Tonalidades en Tresillos (8 compases por tonalidad + D.S. al Fine) · 200 Compases · 10 Articulaciones",
            "24 Keys in Triplets (8 measures per key + D.S. al Fine) · 200 Measures · 10 Articulations"
        ),
        "r5_select_section" to Pair("25 Secciones Tonales (200 Compases · R. 5)", "25 Tonal Sections (200 Measures · R. 5)"),
        "r5_select_art" to Pair("Las 10 Articulaciones de Práctica (R. 5)", "The 10 Practice Articulations (R. 5)"),
        "r5_start_practice" to Pair("Practicar R. 5 (Reichert Op. 5)", "Practice R. 5 (Reichert Op. 5)"),
        // Reichert Completion & Milestones
        "r1_milestone_title" to Pair("¡Reichert 1 Completado (10/10 Articulaciones)!", "Reichert 1 Completed (10/10 Articulations)!"),
        "r1_milestone_msg" to Pair(
            "Has completado las 10 articulaciones de Reichert Nº 1 Op. 5.",
            "You have completed all 10 articulations of Reichert No. 1 Op. 5."
        ),
        "r1_restart_round" to Pair("🔁 Reiniciar las 10 Articulaciones", "🔁 Restart 10 Articulations"),
        "r1_go_to_r2" to Pair("🎵 Ir a Reichert 2 (Op. 5)", "🎵 Go to Reichert 2 (Op. 5)"),
        "r1_next_section" to Pair("Siguiente Tonalidad (6/8)", "Next Key (6/8)"),
        "r1_ten_arts_completed" to Pair("10 Articulaciones Completadas", "10 Articulations Completed"),

        "r2_milestone_title" to Pair("¡Reichert 2 Completado (8/8 Articulaciones)!", "Reichert 2 Completed (8/8 Articulations)!"),
        "r2_milestone_msg" to Pair(
            "Has completado las 8 articulaciones de Reichert Nº 2 Op. 5.",
            "You have completed all 8 articulations of Reichert No. 2 Op. 5."
        ),
        "r2_restart_round" to Pair("🔁 Reiniciar las 8 Articulaciones", "🔁 Restart 8 Articulations"),
        "r2_go_to_r4" to Pair("🎵 Ir a Reichert 4 (Op. 5)", "🎵 Go to Reichert 4 (Op. 5)"),
        "r2_next_section" to Pair("Siguiente Tonalidad (2/4)", "Next Key (2/4)"),
        "r2_eight_arts_completed" to Pair("8 Articulaciones Completadas", "8 Articulations Completed"),

        "r4_milestone_title" to Pair("¡Reichert 4 Completado (8/8 Articulaciones)!", "Reichert 4 Completed (8/8 Articulations)!"),
        "r4_milestone_msg" to Pair(
            "Has completado las 8 articulaciones de Reichert Nº 4 Op. 5.",
            "You have completed all 8 articulations of Reichert No. 4 Op. 5."
        ),
        "r4_restart_round" to Pair("🔁 Reiniciar las 8 Articulaciones", "🔁 Restart 8 Articulations"),
        "r4_go_to_r5" to Pair("🎵 Ir a Reichert 5 (Op. 5)", "🎵 Go to Reichert 5 (Op. 5)"),
        "r4_next_section" to Pair("Siguiente Tonalidad (4/4)", "Next Key (4/4)"),
        "r4_eight_arts_completed" to Pair("8 Articulaciones Completadas", "8 Articulations Completed"),

        "r5_milestone_title" to Pair("¡Reichert 5 Completado (10/10 Articulaciones)!", "Reichert 5 Completed (10/10 Articulations)!"),
        "r5_milestone_msg" to Pair(
            "Has completado las 10 articulaciones de Reichert Nº 5 Op. 5.",
            "You have completed all 10 articulations of Reichert No. 5 Op. 5."
        ),
        "r5_restart_round" to Pair("🔁 Reiniciar las 10 Articulaciones", "🔁 Restart 10 Articulations"),
        "r5_next_section" to Pair("Siguiente Tonalidad (Tresillos)", "Next Key (Triplets)"),
        "r5_ten_arts_completed" to Pair("10 Articulaciones Completadas", "10 Articulations Completed"),

        "r_milestone_title" to Pair("¡Hito de Articulaciones Reichert Op. 5!", "Reichert Op. 5 Articulation Milestone!"),
        "r_milestone_msg" to Pair(
            "Has completado todas las articulaciones de esta sección de Reichert.",
            "You completed all articulations for this Reichert section."
        ),
        "r_restart_round" to Pair("🔁 Reiniciar Ronda", "🔁 Restart Round"),
        "modos_pill_label" to Pair("84 Modos", "84 Modes"),

        "ej1_art_0_title" to Pair("Original (4 ligadas + 4 picadas)", "Original (4 slurred + 4 staccato)"),
        "ej1_art_1_title" to Pair("Ocho notas ligadas", "Eight notes slurred"),
        "ej1_art_2_title" to Pair("Cuatro y cuatro ligadas", "Four & four slurred"),
        "ej1_art_3_title" to Pair("Una picada y tres ligadas", "One staccato & three slurred"),
        "ej1_art_4_title" to Pair("Tres ligadas y una picada", "Three slurred & one staccato"),
        "ej1_art_5_title" to Pair("Dos ligadas y dos picadas", "Two slurred & two staccato"),
        "ej1_art_6_title" to Pair("Dos picadas y dos ligadas", "Two staccato & two slurred"),
        "ej1_art_7_title" to Pair("Una picada, dos ligadas y una picada", "One staccato, two slurred & one staccato"),
        "ej1_art_8_title" to Pair("De dos en dos ligadas", "Slurred in pairs (2 by 2)"),
        "ej1_art_9_title" to Pair("De dos en dos sincopadas", "Syncopated pairs"),
        "ej1_art_10_title" to Pair("Todo picado (Staccato)", "All staccato"),

        "ej1_art_0_short" to Pair("Orig.", "Orig."),
        "ej1_art_1_short" to Pair("8 Lig.", "8 Slur"),
        "ej1_art_2_short" to Pair("4+4", "4+4"),
        "ej1_art_3_short" to Pair("1P+3L", "1P+3S"),
        "ej1_art_4_short" to Pair("3L+1P", "3S+1P"),
        "ej1_art_5_short" to Pair("2L+2P", "2S+2P"),
        "ej1_art_6_short" to Pair("2P+2L", "2P+2S"),
        "ej1_art_7_short" to Pair("1P+2L+1P", "1P+2S+1P"),
        "ej1_art_8_short" to Pair("2 en 2", "Pairs"),
        "ej1_art_9_short" to Pair("Sinc.", "Sync."),
        "ej1_art_10_short" to Pair("Stacc.", "Stacc."),

        // Conservatory Coach & 3-Step Practice Wizard (Opción 1 UX)
        "coach_badge" to Pair("CONSERVATORY COACH · ASISTENTE GUIADO", "CONSERVATORY COACH · GUIDED ASSISTANT"),
        "coach_title" to Pair("¿Qué debo practicar hoy?", "What should I practice today?"),
        "coach_subtitle" to Pair(
            "Continúa tu última sesión en 1 toque o diseña tu rutina de conservatorio.",
            "Continue your last session in 1 tap or build a tailored conservatory routine."
        ),
        "coach_open_wizard" to Pair("✨ Practice Wizard (3 Pasos)", "✨ Practice Wizard (3 Steps)"),
        "coach_wizard_title" to Pair("Asistente de Práctica · Conservatory Coach", "Conservatory Practice Wizard"),
        "coach_resume_banner" to Pair("Continuar última sesión", "Continue Last Session"),
        "coach_resume_action" to Pair("Abrir en Atril", "Open in Stand"),
        "coach_step1_title" to Pair("PASO 1 · TIEMPO DISPONIBLE", "STEP 1 · AVAILABLE TIME"),
        "coach_step2_title" to Pair("PASO 2 · ENFOQUE TÉCNICO", "STEP 2 · TECHNICAL FOCUS"),
        "coach_step3_title" to Pair("PASO 3 · TÓNICA, MODO Y RUTINA SUGERIDA", "STEP 3 · TONIC, MODE & GENERATED ROUTINE"),
        "coach_launch_routine" to Pair("Iniciar Rutina en el Atril", "Launch Routine in Stand"),
        "coach_level1_tonic" to Pair("NIVEL 1 · TÓNICA CROMÁTICA (12)", "LEVEL 1 · CHROMATIC TONIC (12)"),
        "coach_level2_mode" to Pair("NIVEL 2 · MODO PARALELO (7)", "LEVEL 2 · PARALLEL MODE (7)"),
        "coach_level3_scheme" to Pair("NIVEL 3 · ESQUEMA TÉCNICO (10 · 840 VARIACIONES)", "LEVEL 3 · TECHNICAL SCHEME (10 · 840 VARIATIONS)"),
        "coach_level3_subtitle" to Pair(
            "Aplica cualquier patrón de Taffanel & Gaubert o Reichert Op. 5 al modo paralelo elegido:",
            "Apply any Taffanel & Gaubert or Reichert Op. 5 pattern to the selected parallel mode:"
        ),
        "coach_taffanel_group" to Pair("Taffanel & Gaubert (6)", "Taffanel & Gaubert (6)"),
        "coach_reichert_group" to Pair("Reichert Op. 5 (4)", "Reichert Op. 5 (4)")
    )
}

