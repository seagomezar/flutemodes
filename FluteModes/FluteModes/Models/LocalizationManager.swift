import Foundation
import SwiftUI

public enum AppLanguage: String, CaseIterable, Identifiable {
    case spanish = "es"
    case english = "en"

    public var id: String { rawValue }

    public var displayName: String {
        switch self {
        case .spanish: return "Español"
        case .english: return "English"
        }
    }

    public var flag: String {
        switch self {
        case .spanish: return "🇪🇸"
        case .english: return "🇬🇧"
        }
    }
}

public class LocalizationManager: ObservableObject {
    public static let shared = LocalizationManager()

    @AppStorage("app_language") public var currentLanguageString: String = "es" {
        didSet {
            objectWillChange.send()
        }
    }

    public var currentLanguage: AppLanguage {
        get { AppLanguage(rawValue: currentLanguageString) ?? .spanish }
        set { currentLanguageString = newValue.rawValue }
    }

    public func toggleLanguage() {
        currentLanguage = (currentLanguage == .spanish) ? .english : .spanish
    }

    public func t(_ key: String) -> String {
        let isEn = currentLanguage == .english
        return strings[key]?[isEn ? 1 : 0] ?? key
    }

    // Key: [Spanish, English]
    private let strings: [String: [String]] = [
        // App General
        "app_name": ["FluteModes", "FluteModes"],
        "subtitle": [
            "Estudio Diario N° 4 · Paul Taffanel & Philippe Gaubert",
            "Daily Exercise No. 4 · Paul Taffanel & Philippe Gaubert"
        ],
        "sub_desc": [
            "Sistema paralelo del Maestro León Giraldo · 84 Modos (12 Tónicas × 7 Modos)",
            "Maestro León Giraldo's Parallel System · 84 Modes (12 Tonics × 7 Modes)"
        ],

        // Home View
        "select_tonic": ["Selecciona una Tónica", "Select a Tonic"],
        "major_family": ["Familia Mayor (3 Modos)", "Major Family (3 Modes)"],
        "minor_family": ["Familia Menor (4 Modos)", "Minor Family (4 Modes)"],
        "fixed_key": ["Armadura fija:", "Fixed key signature:"],
        "start_practice": ["Comenzar Práctica", "Start Practicing"],
        "practice_matrix": ["Matriz de Progreso (84 Modos)", "Progress Matrix (84 Modes)"],
        "resuming": ["Reanudando:", "Resuming:"],

        // Practice View
        "back": ["Atrás", "Back"],
        "modes_count": ["modos", "modes"],
        "play_piano": ["Reproducir Piano", "Play Piano"],
        "stop_piano": ["Detener Piano", "Stop Piano"],
        "next_art": ["Siguiente Articulación", "Next Articulation"],
        "complete_and_next": ["Completar y Siguiente Modo", "Complete & Next Mode"],
        "seven_modes_completed": ["7 Modos Completados", "7 Modes Completed"],
        "milestone_title": ["¡7 Modos Completados en %@!", "7 Modes Completed in %@!"],
        "milestone_msg": [
            "Has tocado los 7 modos de %@ (%d/56 articulaciones completadas en esta nota). ¿Qué deseas hacer a continuación?",
            "You have practiced all 7 modes of %@ (%d/56 articulations completed for this note). What would you like to do next?"
        ],
        "next_round": ["🔁 Siguiente Ronda de Articulaciones", "🔁 Next Articulation Round"],
        "advance_tonic": ["🎵 Avanzar a %@ (Siguiente Tónica)", "🎵 Advance to %@ (Next Tonic)"],
        "stay_mode": ["Continuar en este modo", "Stay in this mode"],

        // Modes
        "mode_1_name": ["Jónico (Mayor)", "Ionian (Major)"],
        "mode_2_name": ["Lidio", "Lydian"],
        "mode_3_name": ["Mixolidio", "Mixolydian"],
        "mode_4_name": ["Dórico", "Dorian"],
        "mode_5_name": ["Eólico (Menor Natural)", "Aeolian (Natural Minor)"],
        "mode_6_name": ["Frigio", "Phrygian"],
        "mode_7_name": ["Lócrio", "Locrian"],

        // Accidental Badges
        "acc_ionian": ["Sin alteraciones accidentales", "No accidental alterations"],
        "acc_lydian": ["Cuarta aumentada (♯4) accidental", "Augmented fourth (♯4) accidental"],
        "acc_mixolydian": ["Séptima menor (♭7) accidental", "Minor seventh (♭7) accidental"],
        "acc_dorian": ["Sexta mayor (6) accidental", "Major sixth (6) accidental"],
        "acc_aeolian": ["Menor natural sin alteraciones", "Natural minor without accidentals"],
        "acc_phrygian": ["Segunda menor (♭2) accidental", "Minor second (♭2) accidental"],
        "acc_locrian": ["Segunda menor (♭2) y Quinta disminuida (♭5)", "Minor second (♭2) & Diminished fifth (♭5)"],

        // Articulations (short)
        "art_1_short": ["Toda ligada", "All slurred"],
        "art_2_short": ["Ligado 4 y 4", "Slurred 4 & 4"],
        "art_3_short": ["Lig. 2, pic. 2", "Slur 2, stacc. 2"],
        "art_4_short": ["Pic. 1, lig. 2, pic. 1", "Stacc. 1, slur 2, stacc. 1"],
        "art_5_short": ["Pic. 2, lig. 2", "Stacc. 2, slur 2"],
        "art_6_short": ["Pic. 1, lig. 3", "Stacc. 1, slur 3"],
        "art_7_short": ["Lig. 3, pic. 1", "Slur 3, stacc. 1"],
        "art_8_short": ["Toda picada", "All staccato"],

        // Matrix View
        "matrix_title": ["Matriz de Estudio Modal", "Modal Study Matrix"],
        "matrix_stats": ["Completadas: %d de %d articulaciones (%d%%)", "Completed: %d of %d articulations (%d%%)"],
        "reset_all": ["Resetear Todo", "Reset All"],
        "reset_confirm_title": ["¿Resetear todo el progreso?", "Reset all progress?"],
        "reset_confirm_msg": [
            "Esta acción borrará todas las marcas de estudio registradas y comenzará de cero.",
            "This action will erase all completed practice records and restart from scratch."
        ],
        "cancel": ["Cancelar", "Cancel"],
        "delete": ["Borrar", "Delete"],

        // Settings
        "settings_title": ["Ajustes de Estudio", "Practice Settings"],
        "keep_screen_awake": ["Mantener pantalla activa", "Keep screen awake"],
        "keep_screen_awake_desc": ["Evita que el dispositivo entre en modo reposo", "Prevents device from sleeping during practice"],
        "metronome_title": ["Metrónomo (Blanca)", "Metronome (Half note)"],
        "click_sound": ["Sonido de Clic", "Click Sound"],

        // Articulation Progress Clarity
        "arts_count": ["arts.", "arts."],
        "articulations_title": ["Fórmulas de Articulación", "Articulation Patterns"],
        "arts_completed_badge": ["%d/8 arts. completadas", "%d/8 arts. completed"],
        "next_mode": ["Siguiente Modo", "Next Mode"],
        "mode_fully_done": ["Modo Completado (8/8 arts.)", "Mode Completed (8/8 arts.)"],
        "legend_completed": ["Completado (8/8 arts.)", "Completed (8/8 arts)"],
        "legend_in_progress": ["En Progreso (1-7/8 arts.)", "In Progress (1-7/8 arts)"],
        "legend_not_started": ["No iniciado (0/8 arts.)", "Not started (0/8 arts)"]
    ]
}
