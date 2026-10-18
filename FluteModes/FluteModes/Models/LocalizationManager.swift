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
            "Sistema Modal Paralelo · 84 Modos (12 Tónicas × 7 Modos)",
            "Parallel Modal System · 84 Modes (12 Tonics × 7 Modes)"
        ],

        // E.J. 1 General
        "ej1_title": [
            "E. J. 1 · Paul Taffanel & Philippe Gaubert",
            "E. J. 1 · Paul Taffanel & Philippe Gaubert"
        ],
        "ej1_sub_desc": [
            "17 Grands Exercices Journaliers de Mécanisme · Pentacordos cromáticos (31 compases · 10 articulaciones)",
            "17 Daily Mechanism Exercises · Chromatic pentachords (31 measures · 10 articulations)"
        ],
        "ej1_header_info": [
            "Compases 1–10 (plicas ↑) · Compases 11–31 (plicas ↓) · Reprise à l'octave · 8va",
            "Measures 1–10 (stems ↑) · Measures 11–31 (stems ↓) · Reprise à l'octave · 8va"
        ],
        "ej1_select_art": [
            "10 Articulaciones (E. J. 1)",
            "10 Articulations (E. J. 1)"
        ],
        "ej1_start_practice": [
            "Practicar E. J. 1",
            "Practice E. J. 1"
        ],
        "ej1_ten_arts_completed": [
            "10 Articulaciones Completadas",
            "10 Articulations Completed"
        ],
        "ej1_milestone_title": [
            "¡E. J. 1 Completado (10/10 Articulaciones)!",
            "E. J. 1 Completed (10/10 Articulations)!"
        ],
        "ej1_milestone_msg": [
            "Has completado las 10 articulaciones del Ejercicio Diario N.° 1 de Taffanel & Gaubert.",
            "You have completed all 10 articulations of Taffanel & Gaubert Daily Exercise No. 1."
        ],
        "ej1_restart_round": [
            "🔁 Volver a Articulación 1",
            "🔁 Restart from Articulation 1"
        ],
        "ej1_go_to_ej2": [
            "🎵 Ir a E. J. 2 (Pentacordios Menores)",
            "🎵 Switch to E. J. 2 (Minor Pentachords)"
        ],
        "ej1_go_to_ej4": [
            "🎵 Ir a E. J. 4 (Escalas Diatónicas)",
            "🎵 Switch to E. J. 4 (Diatonic Scales)"
        ],

        // E.J. 2 General
        "ej2_title": [
            "E. J. 2 · Paul Taffanel & Philippe Gaubert",
            "E. J. 2 · Paul Taffanel & Philippe Gaubert"
        ],
        "ej2_sub_desc": [
            "17 Grands Exercices Journaliers de Mécanisme · Pentacordios menores y 7ª disminuida (31 compases · 10 articulaciones)",
            "17 Daily Mechanism Exercises · Minor pentachords & diminished 7th (31 measures · 10 articulations)"
        ],
        "ej2_header_info": [
            "Compases 1–10 (plicas ↑) · Compases 11–31 (plicas ↓) · Pentacordios menores · 8va",
            "Measures 1–10 (stems ↑) · Measures 11–31 (stems ↓) · Minor pentachords · 8va"
        ],
        "ej2_select_art": [
            "10 Articulaciones (E. J. 2)",
            "10 Articulations (E. J. 2)"
        ],
        "ej2_start_practice": [
            "Practicar E. J. 2",
            "Practice E. J. 2"
        ],
        "ej2_ten_arts_completed": [
            "10 Articulaciones Completadas",
            "10 Articulations Completed"
        ],
        "ej2_milestone_title": [
            "¡E. J. 2 Completado (10/10 Articulaciones)!",
            "E. J. 2 Completed (10/10 Articulations)!"
        ],
        "ej2_milestone_msg": [
            "Has completado las 10 articulaciones del Ejercicio Diario N.° 2 de Taffanel & Gaubert.",
            "You have completed all 10 articulations of Taffanel & Gaubert Daily Exercise No. 2."
        ],
        "ej2_restart_round": [
            "🔁 Volver a Articulación 1",
            "🔁 Restart from Articulation 1"
        ],
        "ej2_go_to_ej4": [
            "🎵 Ir a E. J. 4 (Escalas Diatónicas)",
            "🎵 Switch to E. J. 4 (Diatonic Scales)"
        ],

        // E.J. 4 General
        "ej4_title": [
            "E. J. 4 · Paul Taffanel & Philippe Gaubert",
            "E. J. 4 · Paul Taffanel & Philippe Gaubert"
        ],
        "ej4_sub_desc": [
            "Escalas Diatónicas en 24 Tonalidades Mayores y Menores Relativas + Coda (194 compases · 8 articulaciones)",
            "Diatonic Scales across 24 Major & Relative Minor Keys + Coda (194 measures · 8 articulations)"
        ],
        "ej4_header_info": [
            "24 Tonalidades (Mayores y Menores: armónica en c. 1 y 7, melódica/natural) · 194 Compases · 8 Articulaciones",
            "24 Keys (Major & Minor: harmonic in m. 1 & 7, melodic/natural) · 194 Measures · 8 Articulations"
        ],
        "ej4_select_section": [
            "25 Secciones Tonales (194 Compases)",
            "25 Tonal Sections (194 Measures)"
        ],
        "ej4_select_art": [
            "8 Articulaciones (E. J. 4)",
            "8 Articulations (E. J. 4)"
        ],
        "ej4_start_practice": [
            "Practicar E. J. 4",
            "Practice E. J. 4"
        ],
        "ej4_eight_arts_completed": [
            "8 Articulaciones Completadas",
            "8 Articulations Completed"
        ],
        "ej4_milestone_title": [
            "¡E. J. 4 Completado (8/8 Articulaciones)!",
            "E. J. 4 Completed (8/8 Articulations)!"
        ],
        "ej4_milestone_msg": [
            "Has completado las 8 articulaciones del Ejercicio Diario N.° 4 de Taffanel & Gaubert (194 compases).",
            "You have completed all 8 articulations of Taffanel & Gaubert Daily Exercise No. 4 (194 measures)."
        ],
        "ej4_restart_round": [
            "🔁 Volver a Articulación 1",
            "🔁 Restart from Articulation 1"
        ],
        "ej4_go_to_modos": [
            "🎵 Ir a 84 Modos Paralelos",
            "🎵 Switch to 84 Parallel Modes"
        ],
        "ej4_next_section": [
            "Siguiente Tonalidad",
            "Next Tonality"
        ],

        // E.J. 5 General
        "ej5_title": [
            "E. J. 5 · Paul Taffanel & Philippe Gaubert",
            "E. J. 5 · Paul Taffanel & Philippe Gaubert"
        ],
        "ej5_sub_desc": [
            "Escalas Cromáticas (Gammes Chromatiques) · 12 Escalas A–L (60 compases · 6/8 & 2/4 · 10 articulaciones)",
            "Chromatic Scales (Gammes Chromatiques) · 12 Scales A–L (60 measures · 6/8 & 2/4 · 10 articulations)"
        ],
        "ej5_header_info": [
            "12 Escalas Cromáticas (Do a Si · 2 Octavas + Reprise à l'octave) · 60 Compases · 10 Articulaciones",
            "12 Chromatic Scales (C to B · 2 Octaves + Reprise à l'octave) · 60 Measures · 10 Articulations"
        ],
        "ej5_select_section": [
            "12 Escalas Cromáticas (A–L · 60 Compases)",
            "12 Chromatic Scales (A–L · 60 Measures)"
        ],
        "ej5_select_art": [
            "10 Articulaciones (E. J. 5)",
            "10 Articulations (E. J. 5)"
        ],
        "ej5_start_practice": [
            "Practicar E. J. 5",
            "Practice E. J. 5"
        ],
        "ej5_ten_arts_completed": [
            "10 Articulaciones Completadas",
            "10 Articulations Completed"
        ],
        "ej5_milestone_title": [
            "¡E. J. 5 Completado (10/10 Articulaciones)!",
            "E. J. 5 Completed (10/10 Articulations)!"
        ],
        "ej5_milestone_msg": [
            "Has completado las 10 articulaciones del Ejercicio Diario N° 5 de Taffanel & Gaubert.",
            "You have completed all 10 articulations of Taffanel & Gaubert's Daily Exercise No. 5."
        ],
        "ej5_restart_round": [
            "🔁 Reiniciar las 10 Articulaciones",
            "🔁 Restart 10 Articulations"
        ],
        "ej5_go_to_ej10": [
            "🎵 Ir a E. J. 10 (Arpegios)",
            "🎵 Go to E. J. 10 (Arpeggios)"
        ],
        "ej5_next_section": [
            "Siguiente Escala (Cromática)",
            "Next Scale (Chromatic)"
        ],

        // E.J. 10 General
        "ej10_title": [
            "E. J. 10 · Paul Taffanel & Philippe Gaubert",
            "E. J. 10 · Paul Taffanel & Philippe Gaubert"
        ],
        "ej10_sub_desc": [
            "Arpegios Progresivos de 2 Octavas (Arpèges) · 12 Series Cromáticas (121 compases · 6/8 & 2/4 · 10 articulaciones)",
            "2-Octave Progressive Arpeggios (Arpèges) · 12 Chromatic Series (121 measures · 6/8 & 2/4 · 10 articulations)"
        ],
        "ej10_header_info": [
            "12 Series Cromáticas (Do a Si · 10 acordes por grado + Coda) · 121 Compases · 10 Articulaciones",
            "12 Chromatic Series (C to B · 10 chords per degree + Coda) · 121 Measures · 10 Articulations"
        ],
        "ej10_select_section": [
            "12 Series de Arpegios (121 Compases)",
            "12 Arpeggio Series (121 Measures)"
        ],
        "ej10_select_art": [
            "10 Articulaciones (E. J. 10)",
            "10 Articulations (E. J. 10)"
        ],
        "ej10_start_practice": [
            "Practicar E. J. 10",
            "Practice E. J. 10"
        ],
        "ej10_ten_arts_completed": [
            "10 Articulaciones Completadas",
            "10 Articulations Completed"
        ],
        "ej10_milestone_title": [
            "¡E. J. 10 Completado (10/10 Articulaciones)!",
            "E. J. 10 Completed (10/10 Articulations)!"
        ],
        "ej10_milestone_msg": [
            "Has completado las 10 articulaciones del Ejercicio Diario N° 10 de Taffanel & Gaubert.",
            "You have completed all 10 articulations of Taffanel & Gaubert's Daily Exercise No. 10."
        ],
        "ej10_restart_round": [
            "🔁 Reiniciar las 10 Articulaciones",
            "🔁 Restart 10 Articulations"
        ],
        "ej10_go_to_ej11": [
            "🎵 Ir a E. J. 11 (Arpegios Quebrados)",
            "🎵 Go to E. J. 11 (Broken Arpeggios)"
        ],
        "ej10_next_section": [
            "Siguiente Serie de Arpegios",
            "Next Arpeggio Series"
        ],

        // E.J. 11 General
        "ej11_title": [
            "E. J. 11 · Paul Taffanel & Philippe Gaubert",
            "E. J. 11 · Paul Taffanel & Philippe Gaubert"
        ],
        "ej11_sub_desc": [
            "Arpegios Quebrados (Arpèges Brisés) · 12 Series Cromáticas (121 compases · 9/8 & 3/4 · 10 articulaciones)",
            "Broken Arpeggios (Arpèges Brisés) · 12 Chromatic Series (121 measures · 9/8 & 3/4 · 10 articulations)"
        ],
        "ej11_header_info": [
            "12 Series Cromáticas en 9/8 y 3/4 (18 semicorcheas por compás + Coda) · 121 Compases · 10 Articulaciones",
            "12 Chromatic Series in 9/8 & 3/4 (18 sixteenths per measure + Coda) · 121 Measures · 10 Articulations"
        ],
        "ej11_select_section": [
            "12 Series de Arpegios Quebrados (121 Compases)",
            "12 Broken Arpeggio Series (121 Measures)"
        ],
        "ej11_select_art": [
            "10 Articulaciones (E. J. 11)",
            "10 Articulations (E. J. 11)"
        ],
        "ej11_start_practice": [
            "Practicar E. J. 11",
            "Practice E. J. 11"
        ],
        "ej11_ten_arts_completed": [
            "10 Articulaciones Completadas",
            "10 Articulations Completed"
        ],
        "ej11_milestone_title": [
            "¡E. J. 11 Completado (10/10 Articulaciones)!",
            "E. J. 11 Completed (10/10 Articulations)!"
        ],
        "ej11_milestone_msg": [
            "Has completado las 10 articulaciones del Ejercicio Diario N° 11 de Taffanel & Gaubert.",
            "You have completed all 10 articulations of Taffanel & Gaubert's Daily Exercise No. 11."
        ],
        "ej11_restart_round": [
            "🔁 Reiniciar las 10 Articulaciones",
            "🔁 Restart 10 Articulations"
        ],
        "ej11_go_to_r1": [
            "🎵 Ir a Reichert 1 (Op. 5)",
            "🎵 Go to Reichert 1 (Op. 5)"
        ],
        "ej11_next_section": [
            "Siguiente Serie de Arpegios Quebrados",
            "Next Broken Arpeggio Series"
        ],

        // Reichert Op. 5, Nº 1 (R1)
        "r1_title": [
            "Reichert Op. 5 Nº 1 · 7 Exercices Journaliers",
            "Reichert Op. 5 No. 1 · 7 Daily Exercises"
        ],
        "r1_sub_desc": [
            "24 Tonalidades Mayores y Menores en 6/8 + D.S. al Fine (100 compases · 10 articulaciones)",
            "24 Major & Minor Keys in 6/8 + D.S. al Fine (100 measures · 10 articulations)"
        ],
        "r1_header_info": [
            "24 Tonalidades en 6/8 (♩. = 80–100 · menor melódica asc. y natural desc.) · 100 Compases · 10 Articulaciones",
            "24 Keys in 6/8 (♩. = 80–100 · melodic minor asc. & natural desc.) · 100 Measures · 10 Articulations"
        ],
        "r1_select_section": [
            "25 Secciones Tonales (100 Compases · 6/8)",
            "25 Tonal Sections (100 Measures · 6/8)"
        ],
        "r1_select_art": [
            "10 Articulaciones (Reichert Nº 1)",
            "10 Articulations (Reichert No. 1)"
        ],
        "r1_start_practice": [
            "Practicar Reichert Nº 1",
            "Practice Reichert No. 1"
        ],

        // Reichert Op. 5, Nº 2 (R2)
        "r2_title": [
            "Reichert Op. 5 Nº 2 · 7 Exercices Journaliers",
            "Reichert Op. 5 No. 2 · 7 Daily Exercises"
        ],
        "r2_sub_desc": [
            "Arpegios modulantes en 24 Tonalidades (2/4 · anacrusa + 200 compases · 8 articulaciones)",
            "Modulating Arpeggios across 24 Keys (2/4 · pickup + 200 measures · 8 articulations)"
        ],
        "r2_header_info": [
            "24 Tonalidades en 2/4 (♩ = 120–152 · 8va en Do M, Re m, Do m, Re♭ M y Do♯ m) · 200 Compases · 8 Articulaciones",
            "24 Keys in 2/4 (♩ = 120–152 · 8va in C, Dm, Cm, D♭ & C♯m) · 200 Measures · 8 Articulations"
        ],
        "r2_select_section": [
            "25 Secciones Tonales (200 Compases · 2/4)",
            "25 Tonal Sections (200 Measures · 2/4)"
        ],
        "r2_select_art": [
            "8 Articulaciones (Reichert Nº 2)",
            "8 Articulations (Reichert No. 2)"
        ],
        "r2_start_practice": [
            "Practicar Reichert Nº 2",
            "Practice Reichert No. 2"
        ],

        // Reichert Op. 5, Nº 4 (R4)
        "r4_title": [
            "Reichert Op. 5 Nº 4 · 7 Exercices Journaliers",
            "Reichert Op. 5 No. 4 · 7 Daily Exercises"
        ],
        "r4_sub_desc": [
            "Mecanismo diatónico y saltos en 24 Tonalidades (4/4 · 100 compases · 8 articulaciones)",
            "Diatonic mechanism & leaps across 24 Keys (4/4 · 100 measures · 8 articulations)"
        ],
        "r4_header_info": [
            "24 Tonalidades en C / 4/4 (♩ = 116–144 · menor armónica con 6ª natural y 7ª sensible) · 100 Compases · 8 Articulaciones",
            "24 Keys in C / 4/4 (♩ = 116–144 · harmonic minor with natural 6th & leading 7th) · 100 Measures · 8 Articulations"
        ],
        "r4_select_section": [
            "25 Secciones Tonales (100 Compases · 4/4)",
            "25 Tonal Sections (100 Measures · 4/4)"
        ],
        "r4_select_art": [
            "8 Articulaciones (Reichert Nº 4)",
            "8 Articulations (Reichert No. 4)"
        ],
        "r4_start_practice": [
            "Practicar Reichert Nº 4",
            "Practice Reichert No. 4"
        ],

        // Reichert Op. 5, Nº 5 (R5)
        "r5_title": [
            "Reichert Op. 5 Nº 5 · 7 Exercices Journaliers",
            "Reichert Op. 5 No. 5 · 7 Daily Exercises"
        ],
        "r5_sub_desc": [
            "Tresillos de semicorchea y bordaduras cromáticas en 24 Tonalidades (2/4 · 200 compases · 10 articulaciones)",
            "Sixteenth-note triplets & chromatic neighbors across 24 Keys (2/4 · 200 measures · 10 articulations)"
        ],
        "r5_header_info": [
            "24 Tonalidades en 2/4 Tresillos (♪ = 144–184 · 8va en Do M, Re m, Do m y Re♭ M) · 200 Compases · 10 Articulaciones",
            "24 Keys in 2/4 Triplets (♪ = 144–184 · 8va in C, Dm, Cm & D♭) · 200 Measures · 10 Articulations"
        ],
        "r5_select_section": [
            "25 Secciones Tonales (200 Compases · Tresillos)",
            "25 Tonal Sections (200 Measures · Triplets)"
        ],
        "r5_select_art": [
            "10 Articulaciones (Reichert Nº 5)",
            "10 Articulations (Reichert No. 5)"
        ],
        "r5_start_practice": [
            "Practicar Reichert Nº 5",
            "Practice Reichert No. 5"
        ],
        // Reichert Completion & Milestones
        "r1_milestone_title": [
            "¡Reichert 1 Completado (10/10 Articulaciones)!",
            "Reichert 1 Completed (10/10 Articulations)!"
        ],
        "r1_milestone_msg": [
            "Has completado las 10 articulaciones de Reichert Nº 1 Op. 5.",
            "You have completed all 10 articulations of Reichert No. 1 Op. 5."
        ],
        "r1_restart_round": [
            "🔁 Reiniciar las 10 Articulaciones",
            "🔁 Restart 10 Articulations"
        ],
        "r1_go_to_r2": [
            "🎵 Ir a Reichert 2 (Op. 5)",
            "🎵 Go to Reichert 2 (Op. 5)"
        ],
        "r1_next_section": [
            "Siguiente Tonalidad (6/8)",
            "Next Key (6/8)"
        ],
        "r1_ten_arts_completed": [
            "10 Articulaciones Completadas",
            "10 Articulations Completed"
        ],

        "r2_milestone_title": [
            "¡Reichert 2 Completado (8/8 Articulaciones)!",
            "Reichert 2 Completed (8/8 Articulations)!"
        ],
        "r2_milestone_msg": [
            "Has completado las 8 articulaciones de Reichert Nº 2 Op. 5.",
            "You have completed all 8 articulations of Reichert No. 2 Op. 5."
        ],
        "r2_restart_round": [
            "🔁 Reiniciar las 8 Articulaciones",
            "🔁 Restart 8 Articulations"
        ],
        "r2_go_to_r4": [
            "🎵 Ir a Reichert 4 (Op. 5)",
            "🎵 Go to Reichert 4 (Op. 5)"
        ],
        "r2_next_section": [
            "Siguiente Tonalidad (2/4)",
            "Next Key (2/4)"
        ],
        "r2_eight_arts_completed": [
            "8 Articulaciones Completadas",
            "8 Articulations Completed"
        ],

        "r4_milestone_title": [
            "¡Reichert 4 Completado (8/8 Articulaciones)!",
            "Reichert 4 Completed (8/8 Articulations)!"
        ],
        "r4_milestone_msg": [
            "Has completado las 8 articulaciones de Reichert Nº 4 Op. 5.",
            "You have completed all 8 articulations of Reichert No. 4 Op. 5."
        ],
        "r4_restart_round": [
            "🔁 Reiniciar las 8 Articulaciones",
            "🔁 Restart 8 Articulations"
        ],
        "r4_go_to_r5": [
            "🎵 Ir a Reichert 5 (Op. 5)",
            "🎵 Go to Reichert 5 (Op. 5)"
        ],
        "r4_next_section": [
            "Siguiente Tonalidad (4/4)",
            "Next Key (4/4)"
        ],
        "r4_eight_arts_completed": [
            "8 Articulaciones Completadas",
            "8 Articulations Completed"
        ],

        "r5_milestone_title": [
            "¡Reichert 5 Completado (10/10 Articulaciones)!",
            "Reichert 5 Completed (10/10 Articulations)!"
        ],
        "r5_milestone_msg": [
            "Has completado las 10 articulaciones de Reichert Nº 5 Op. 5.",
            "You have completed all 10 articulations of Reichert No. 5 Op. 5."
        ],
        "r5_restart_round": [
            "🔁 Reiniciar las 10 Articulaciones",
            "🔁 Restart 10 Articulations"
        ],
        "r5_next_section": [
            "Siguiente Tonalidad (Tresillos)",
            "Next Key (Triplets)"
        ],
        "r5_ten_arts_completed": [
            "10 Articulaciones Completadas",
            "10 Articulations Completed"
        ],

        "r_milestone_title": [
            "¡Hito de Articulaciones Reichert Op. 5!",
            "Reichert Op. 5 Articulation Milestone!"
        ],
        "r_milestone_msg": [
            "Has completado todas las articulaciones de esta sección de Reichert.",
            "You completed all articulations for this Reichert section."
        ],
        "r_restart_round": [
            "🔁 Reiniciar Ronda",
            "🔁 Restart Round"
        ],
        "modos_pill_label": [
            "84 Modos",
            "84 Modes"
        ],

        // E.J. 1 Articulations (0..10)
        "ej1_art_0_title": ["Original", "Original"],
        "ej1_art_1_title": ["A 8 ligadas (Toda ligada)", "All 8 slurred"],
        "ej1_art_2_title": ["A 4 y 4 ligadas", "Slurred 4 & 4"],
        "ej1_art_3_title": ["1 picada y 3 ligadas", "1 staccato, 3 slurred"],
        "ej1_art_4_title": ["3 ligadas y 1 picada", "3 slurred, 1 staccato"],
        "ej1_art_5_title": ["2 ligadas y 2 picadas", "2 slurred, 2 staccato"],
        "ej1_art_6_title": ["2 picadas y 2 ligadas", "2 staccato, 2 slurred"],
        "ej1_art_7_title": ["1 picada, 2 ligadas y 1 picada", "1 stacc., 2 slurred, 1 stacc."],
        "ej1_art_8_title": ["De 2 en 2 ligadas", "Slurred in pairs (2+2+2+2)"],
        "ej1_art_9_title": ["De 2 en 2 sincopadas", "Syncopated pairs"],
        "ej1_art_10_title": ["Todo picado (Staccato)", "All staccato"],

        "ej1_art_0_short": ["Orig.", "Orig."],
        "ej1_art_1_short": ["8 Lig.", "8 Slur"],
        "ej1_art_2_short": ["4+4", "4+4"],
        "ej1_art_3_short": ["1P+3L", "1P+3L"],
        "ej1_art_4_short": ["3L+1P", "3L+1P"],
        "ej1_art_5_short": ["2L+2P", "2L+2P"],
        "ej1_art_6_short": ["2P+2L", "2P+2L"],
        "ej1_art_7_short": ["1P+2L+1P", "1P+2L+1P"],
        "ej1_art_8_short": ["2 en 2", "2+2"],
        "ej1_art_9_short": ["Sinc.", "Sync."],
        "ej1_art_10_short": ["Stacc.", "Stacc."],

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
        "next_art": ["Siguiente Art.", "Next Art."],
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

        // Articulations E.J. 4 (short)
        "art_1_short": ["8 Lig.", "8 Slur"],
        "art_2_short": ["4+4", "4+4"],
        "art_3_short": ["2L+2P", "2L+2P"],
        "art_4_short": ["1P+2L+1P", "1P+2L+1P"],
        "art_5_short": ["2P+2L", "2P+2L"],
        "art_6_short": ["1P+3L", "1P+3L"],
        "art_7_short": ["3L+1P", "3L+1P"],
        "art_8_short": ["Stacc.", "Stacc."],

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
        "mode_done": ["Modo Listo", "Mode Done"],
        "mode_fully_done": ["Modo Completado", "Mode Completed"],
        "legend_completed": ["Completado (8/8 arts.)", "Completed (8/8 arts)"],
        "legend_in_progress": ["En Progreso (1-7/8 arts.)", "In Progress (1-7/8 arts)"],
        "legend_not_started": ["No iniciado (0/8 arts.)", "Not started (0/8 arts)"],
        "completed": ["Completada", "Completed"],
        "in_progress": ["En curso", "Current"],

        // Conservatory Coach & 3-Step Practice Wizard & 3-Level Modes Explorer
        "coach_badge": ["CONSERVATORY COACH · ASISTENTE GUIADO", "CONSERVATORY COACH · GUIDED ASSISTANT"],
        "coach_title": ["Asistente de Estudio: ¿Qué debo practicar hoy?", "Study Assistant: What should I practice today?"],
        "coach_subtitle": [
            "Rutina guiada combinando Taffanel & Gaubert, Reichert Op. 5 y las 840 Variaciones de Modos Paralelos.",
            "Guided daily routine combining Taffanel & Gaubert, Reichert Op. 5, and the 840 Parallel Modal Variations."
        ],
        "coach_open_wizard": ["Practice Wizard (3 Pasos)", "Practice Wizard (3 Steps)"],
        "coach_wizard_title": ["Asistente de Práctica · Conservatory Coach", "Conservatory Practice Wizard"],
        "coach_resume_banner": ["CONTINUAR ÚLTIMA SESIÓN", "CONTINUE LAST SESSION"],
        "coach_resume_action": ["Reanudar", "Resume"],
        "coach_step1_title": ["PASO 1 · TIEMPO DISPONIBLE", "STEP 1 · AVAILABLE TIME"],
        "coach_step2_title": ["PASO 2 · ENFOQUE TÉCNICO PRINCIPAL", "STEP 2 · TECHNICAL FOCUS"],
        "coach_step3_title": ["PASO 3 · TÓNICA, MODO Y RUTINA SUGERIDA", "STEP 3 · TONIC, MODE & GENERATED ROUTINE"],
        "coach_launch_routine": ["🚀 Iniciar Sesión Guiada en el Atril", "🚀 Start Guided Session on Stand"],
        "coach_level1_tonic": ["NIVEL 1 · TÓNICA CROMÁTICA (12)", "LEVEL 1 · CHROMATIC TONIC (12)"],
        "coach_level2_mode": ["NIVEL 2 · MODO PARALELO (7)", "LEVEL 2 · PARALLEL MODE (7)"],
        "coach_level3_scheme": ["NIVEL 3 · ESQUEMA TÉCNICO (10 · 840 VARIACIONES)", "LEVEL 3 · TECHNICAL SCHEME (10 · 840 VARIATIONS)"],
        "coach_level3_subtitle": [
            "Aplica cualquier patrón de Taffanel & Gaubert o Reichert Op. 5 al modo paralelo elegido:",
            "Apply any Taffanel & Gaubert or Reichert Op. 5 pattern to the selected parallel mode:"
        ],
        "coach_taffanel_group": ["Taffanel & Gaubert (6 Esquemas):", "Taffanel & Gaubert (6 Schemes):"],
        "coach_reichert_group": ["M. A. Reichert Op. 5 (4 Esquemas):", "M. A. Reichert Op. 5 (4 Schemes):"]
    ]
}

