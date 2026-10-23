import Foundation

public enum ExerciseType: String, CaseIterable, Identifiable, Codable {
    case ej1 = "EJ1"
    case ej2 = "EJ2"
    case ej4 = "EJ4"
    case ej5 = "EJ5"
    case ej10 = "EJ10"
    case ej11 = "EJ11"
    case r1 = "R1"
    case r2 = "R2"
    case r4 = "R4"
    case r5 = "R5"
    case modos = "MODOS"

    public var id: String { rawValue }

    public var isChromaticExercise: Bool {
        self == .ej1 || self == .ej2
    }

    public var isReichertExercise: Bool {
        self == .r1 || self == .r2 || self == .r4 || self == .r5
    }

    /// 8-Articulation, 25-Key exercises (T&G E.J. 4, Reichert Nº 2, Reichert Nº 4)
    public var isEJ4Exercise: Bool {
        self == .ej4 || self == .r2 || self == .r4
    }

    /// 10-Articulation sectioned exercises (T&G E.J. 5/10/11, Reichert Nº 1, Reichert Nº 5)
    public var isEJ5TypeExercise: Bool {
        self == .ej5 || self == .ej10 || self == .ej11 || self == .r1 || self == .r5
    }

    public var isSectionedLeducExercise: Bool {
        isEJ4Exercise || isEJ5TypeExercise
    }

    public var isLeducExercise: Bool {
        self != .modos
    }

    public var sectionCount: Int {
        switch self {
        case .ej4, .r1, .r2, .r4, .r5: return 25
        case .ej5, .ej10, .ej11: return 12
        default: return 12
        }
    }

    public var pillLabel: String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .ej1: return "E.J. 1"
        case .ej2: return "E.J. 2"
        case .ej4: return "E.J. 4"
        case .ej5: return "E.J. 5"
        case .ej10: return "E.J. 10"
        case .ej11: return "E.J. 11"
        case .r1: return "R. 1"
        case .r2: return "R. 2"
        case .r4: return "R. 4"
        case .r5: return "R. 5"
        case .modos: return isEn ? "84 Modes" : "84 Modos"
        }
    }

    public var displayTitle: String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .ej1: return isEn ? "E.J. 1 · Major (10 Arts.)" : "E.J. 1 · Mayor (10 Arts.)"
        case .ej2: return isEn ? "E.J. 2 · Minor (10 Arts.)" : "E.J. 2 · Menor (10 Arts.)"
        case .ej4: return isEn ? "E.J. 4 · 24 Keys (8 Arts.)" : "E.J. 4 · 24 Ton. (8 Arts.)"
        case .ej5: return isEn ? "E.J. 5 · Chromatic (10 Arts.)" : "E.J. 5 · Cromáticas (10 Arts.)"
        case .ej10: return isEn ? "E.J. 10 · Arpeggios (10 Arts.)" : "E.J. 10 · Arpegios (10 Arts.)"
        case .ej11: return isEn ? "E.J. 11 · Broken Arp. (10 Arts.)" : "E.J. 11 · Arp. Quebrados (10 Arts.)"
        case .r1: return isEn ? "Reichert 1 · 6/8 (10 Arts.)" : "Reichert 1 · 6/8 (10 Arts.)"
        case .r2: return isEn ? "Reichert 2 · 2/4 (8 Arts.)" : "Reichert 2 · 2/4 (8 Arts.)"
        case .r4: return isEn ? "Reichert 4 · 4/4 (8 Arts.)" : "Reichert 4 · 4/4 (8 Arts.)"
        case .r5: return isEn ? "Reichert 5 · Triplets (10 Arts.)" : "Reichert 5 · Tresillos (10 Arts.)"
        case .modos: return isEn ? "84 Parallel Modes" : "84 Modos Paralelos"
        }
    }

    public var shortLabel: String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .ej1: return isEn ? "E.J. 1 (Major)" : "E.J. 1 (Mayor)"
        case .ej2: return isEn ? "E.J. 2 (Minor)" : "E.J. 2 (Menor)"
        case .ej4: return isEn ? "E.J. 4 (24 Keys)" : "E.J. 4 (24 Ton.)"
        case .ej5: return isEn ? "E.J. 5 (Chromatic)" : "E.J. 5 (Cromáticas)"
        case .ej10: return isEn ? "E.J. 10 (Arpeggios)" : "E.J. 10 (Arpegios)"
        case .ej11: return isEn ? "E.J. 11 (Broken Arp.)" : "E.J. 11 (Arp. Quebr.)"
        case .r1: return isEn ? "Reichert 1 (6/8)" : "Reichert 1 (6/8)"
        case .r2: return isEn ? "Reichert 2 (2/4)" : "Reichert 2 (2/4)"
        case .r4: return isEn ? "Reichert 4 (4/4)" : "Reichert 4 (4/4)"
        case .r5: return isEn ? "Reichert 5 (Triplets)" : "Reichert 5 (Tresillos)"
        case .modos: return isEn ? "84 Modes" : "84 Modos"
        }
    }

    public var shortName: String { displayTitle }
    public var shortBadge: String { pillLabel }

    public var homeButtonTitle: String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .ej1: return "E.J. 1"
        case .ej2: return "E.J. 2"
        case .ej4: return "E.J. 4"
        case .ej5: return "E.J. 5"
        case .ej10: return "E.J. 10"
        case .ej11: return "E.J. 11"
        case .r1: return "Reichert 1"
        case .r2: return "Reichert 2"
        case .r4: return "Reichert 4"
        case .r5: return "Reichert 5"
        case .modos: return isEn ? "84 Parallel Modes (84 × 10)" : "84 Modos Paralelos (84 × 10)"
        }
    }

    public var homeButtonSubtitle: String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .ej1: return isEn ? "Major · 10 Arts." : "Mayor · 10 Arts."
        case .ej2: return isEn ? "Minor · 10 Arts." : "Menor · 10 Arts."
        case .ej4: return isEn ? "24 Keys · 8 Arts." : "24 Ton. · 8 Arts."
        case .ej5: return isEn ? "Chromatic · 10" : "Cromáticas · 10"
        case .ej10: return isEn ? "Arpeggios · 10" : "Arpegios · 10"
        case .ej11: return isEn ? "Broken · 10" : "Quebrados · 10"
        case .r1: return isEn ? "6/8 · 10 Arts." : "6/8 · 10 Arts."
        case .r2: return isEn ? "2/4 · 8 Arts." : "2/4 · 8 Arts."
        case .r4: return isEn ? "4/4 · 8 Arts." : "4/4 · 8 Arts."
        case .r5: return isEn ? "Triplets · 10" : "Tresillos · 10"
        case .modos: return isEn ? "12 Tonics × 7 Modes" : "12 Tónicas × 7 Modos"
        }
    }
}

public enum EJ4Articulation: Int, CaseIterable, Identifiable, Codable {
    case original = 0
    case allSlurred8 = 1
    case slurred4And4 = 2
    case staccato1Slur3 = 3
    case slur2Staccato2 = 4
    case staccato2Slur2 = 5
    case staccato1Slur2Staccato1 = 6
    case pairsSlurred = 7
    case syncopatedPairs = 8

    public var id: Int { rawValue }

    /// The 8 official articulations of Taffanel & Gaubert E.J. 4 (1...8)
    public static var practiceCases: [EJ4Articulation] {
        [
            .allSlurred8,
            .slurred4And4,
            .staccato1Slur3,
            .slur2Staccato2,
            .staccato2Slur2,
            .staccato1Slur2Staccato1,
            .pairsSlurred,
            .syncopatedPairs
        ]
    }

    public func title(for exercise: ExerciseType = .ej4) -> String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .original:                return isEn ? "Original (As written)" : "Original (Como está escrito)"
        case .allSlurred8:             return isEn ? "8 slurred: (CDEFGABc)" : "8 ligadas: (CDEFGABc)"
        case .slurred4And4:            return isEn ? "4 and 4 slurred: (CDEF)(GABc)" : "4 y 4 ligadas: (CDEF)(GABc)"
        case .staccato1Slur3:          return isEn ? "1 staccato, 3 slurred: .C(DEF) .G(ABc)" : "1 picada y 3 ligadas: .C(DEF) .G(ABc)"
        case .slur2Staccato2:          return isEn ? "2 slurred, 2 staccato: (CD).E.F (GA).B.c" : "2 ligadas y 2 picadas: (CD).E.F (GA).B.c"
        case .staccato2Slur2:          return isEn ? "2 staccato, 2 slurred: .C.D(EF) .G.A(Bc)" : "2 picadas y 2 ligadas: .C.D(EF) .G.A(Bc)"
        case .staccato1Slur2Staccato1: return isEn ? "1 stacc., 2 slurred, 1 stacc.: .C(DE).F .G(AB).c" : "1 picada, 2 ligadas y 1 picada: .C(DE).F .G(AB).c"
        case .pairsSlurred:            return isEn ? "Slurred in pairs: (CD)(EF)(GA)(Bc)" : "De 2 en 2 ligadas: (CD)(EF)(GA)(Bc)"
        case .syncopatedPairs:         return isEn ? "Syncopated pairs: .C(DE)(FG)(AB).c" : "De 2 en 2 sincopadas: .C(DE)(FG)(AB).c"
        }
    }

    public var title: String { title(for: .ej4) }

    public var shortTitle: String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .original:                return "Orig."
        case .allSlurred8:             return isEn ? "8 Slur" : "8 Lig."
        case .slurred4And4:            return "4+4"
        case .staccato1Slur3:          return "1P+3L"
        case .slur2Staccato2:          return "2L+2P"
        case .staccato2Slur2:          return "2P+2L"
        case .staccato1Slur2Staccato1: return "1P+2L+1P"
        case .pairsSlurred:            return isEn ? "2+2" : "2 en 2"
        case .syncopatedPairs:         return isEn ? "Sync." : "Sinc."
        }
    }

    public func formulaBadge(for exercise: ExerciseType = .ej4) -> String {
        switch self {
        case .original:                return "Original"
        case .allSlurred8:             return "(8)"
        case .slurred4And4:            return "(4)+(4)"
        case .staccato1Slur3:          return "·(3) ·(3)"
        case .slur2Staccato2:          return "(2)·· (2)··"
        case .staccato2Slur2:          return "··(2) ··(2)"
        case .staccato1Slur2Staccato1: return "·(2)· ·(2)·"
        case .pairsSlurred:            return "(2)(2)(2)(2)"
        case .syncopatedPairs:         return "·(2)(2)(2)·"
        }
    }

    public var formulaBadge: String { formulaBadge(for: .ej4) }
}

public enum EJ5Articulation: Int, CaseIterable, Identifiable, Codable {
    case original = 0
    case allSlurred = 1
    case slurredSixBySix = 2
    case slur4Stacc2 = 3
    case stacc2Slur4 = 4
    case slur2Stacc4 = 5
    case slurredThreeByThree = 6
    case slur3Stacc3 = 7
    case pairsSlurred = 8
    case syncopatedPairs = 9
    case allStaccato = 10

    public var id: Int { rawValue }

    /// The 10 official articulations of Taffanel & Gaubert E.J. 5, E.J. 10, E.J. 11 (1...10)
    public static var practiceCases: [EJ5Articulation] {
        [
            .allSlurred,
            .slurredSixBySix,
            .slur4Stacc2,
            .stacc2Slur4,
            .slur2Stacc4,
            .slurredThreeByThree,
            .slur3Stacc3,
            .pairsSlurred,
            .syncopatedPairs,
            .allStaccato
        ]
    }

    public func title(for exercise: ExerciseType = .ej5) -> String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        let is98 = (exercise == .ej11)
        switch self {
        case .original:
            return isEn ? "Original (As written)" : "Original (Como está escrito)"
        case .allSlurred:
            return is98
                ? (isEn ? "18 slurred (full measure)" : "18 ligadas (compás completo)")
                : (isEn ? "12 slurred (full measure)" : "12 ligadas (compás completo)")
        case .slurredSixBySix:
            return is98
                ? (isEn ? "6+6+6 slurred (by beats)" : "6+6+6 ligadas (por tiempos)")
                : (isEn ? "6 and 6 slurred (by beats)" : "6 y 6 ligadas (por tiempos)")
        case .slur4Stacc2:
            return isEn ? "4 slurred and 2 staccato" : "4 ligadas y 2 picadas"
        case .stacc2Slur4:
            return isEn ? "2 staccato and 4 slurred" : "2 picadas y 4 ligadas"
        case .slur2Stacc4:
            return isEn ? "2 slurred and 4 staccato" : "2 ligadas y 4 picadas"
        case .slurredThreeByThree:
            return is98
                ? (isEn ? "Slurred in 3s (3/4)" : "De 3 en 3 ligadas (3/4)")
                : (isEn ? "Slurred in 3s (2/4)" : "De 3 en 3 ligadas (2/4)")
        case .slur3Stacc3:
            return is98
                ? (isEn ? "3 slurred, 3 staccato (3/4)" : "3 ligadas y 3 picadas (3/4)")
                : (isEn ? "3 slurred, 3 staccato (2/4)" : "3 ligadas y 3 picadas (2/4)")
        case .pairsSlurred:
            return isEn ? "Slurred in pairs" : "De 2 en 2 ligadas"
        case .syncopatedPairs:
            return isEn ? "Syncopated pairs" : "De 2 en 2 sincopadas"
        case .allStaccato:
            return isEn ? "All staccato" : "Todas picadas (Staccato)"
        }
    }

    public var title: String { title(for: .ej5) }

    public func shortTitle(for exercise: ExerciseType = .ej5) -> String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        let is98 = (exercise == .ej11)
        switch self {
        case .original:            return "Orig."
        case .allSlurred:          return is98 ? (isEn ? "18 Slur" : "18 Lig.") : (isEn ? "12 Slur" : "12 Lig.")
        case .slurredSixBySix:     return is98 ? "6+6+6" : "6+6"
        case .slur4Stacc2:         return "4L+2P"
        case .stacc2Slur4:         return "2P+4L"
        case .slur2Stacc4:         return "2L+4P"
        case .slurredThreeByThree: return isEn ? "3 by 3" : "3 en 3"
        case .slur3Stacc3:         return "3L+3P"
        case .pairsSlurred:        return isEn ? "2 by 2" : "2 en 2"
        case .syncopatedPairs:     return isEn ? "Sync." : "Sinc."
        case .allStaccato:         return "Stacc."
        }
    }

    public var shortTitle: String { shortTitle(for: .ej5) }

    public func formulaBadge(for exercise: ExerciseType = .ej5) -> String {
        let is98 = (exercise == .ej11)
        switch self {
        case .original:
            if exercise == .r1 { return "6/8" }
            if exercise == .r5 { return "2/4" }
            return is98 ? "9/8 · 3/4" : "6/8 · 2/4"
        case .allSlurred:          return is98 ? "(18)" : "(12)"
        case .slurredSixBySix:     return is98 ? "(6)+(6)+(6)" : "(6)+(6)"
        case .slur4Stacc2:         return "(4)·· (4)··"
        case .stacc2Slur4:         return "··(4) ··(4)"
        case .slur2Stacc4:         return "(2)····"
        case .slurredThreeByThree: return is98 ? "(3)×6 [3/4]" : "(3)(3)(3)(3)"
        case .slur3Stacc3:         return "(3)···"
        case .pairsSlurred:        return "(2)(2)(2)"
        case .syncopatedPairs:     return "·(2)(2)·"
        case .allStaccato:         return "······"
        }
    }

    public var formulaBadge: String { formulaBadge(for: .ej5) }
}

public struct EJ4Section: Identifiable, Equatable {
    public let id: Int
    public let shortName: String
    public let fullName: String
    public let measureRange: String
    public let isMinor: Bool

    public static let all: [EJ4Section] = [
        EJ4Section(id: 0,  shortName: "1. Do M",   fullName: "1. Do Mayor (C Major)",           measureRange: "c. 1–8",     isMinor: false),
        EJ4Section(id: 1,  shortName: "2. La m",   fullName: "2. La menor (Relatif Mineur)",    measureRange: "c. 9–16",    isMinor: true),
        EJ4Section(id: 2,  shortName: "3. Fa M",   fullName: "3. Fa Mayor (F Major)",           measureRange: "c. 17–24",   isMinor: false),
        EJ4Section(id: 3,  shortName: "4. Re m",   fullName: "4. Re menor (Mineur)",            measureRange: "c. 25–32",   isMinor: true),
        EJ4Section(id: 4,  shortName: "5. Si♭ M",  fullName: "5. Si♭ Mayor (B♭ Major)",         measureRange: "c. 33–40",   isMinor: false),
        EJ4Section(id: 5,  shortName: "6. Sol m",  fullName: "6. Sol menor (Mineur)",           measureRange: "c. 41–48",   isMinor: true),
        EJ4Section(id: 6,  shortName: "7. Mi♭ M",  fullName: "7. Mi♭ Mayor (E♭ Major)",         measureRange: "c. 49–56",   isMinor: false),
        EJ4Section(id: 7,  shortName: "8. Do m",   fullName: "8. Do menor (Mineur)",            measureRange: "c. 57–64",   isMinor: true),
        EJ4Section(id: 8,  shortName: "9. La♭ M",  fullName: "9. La♭ Mayor (A♭ Major)",         measureRange: "c. 65–72",   isMinor: false),
        EJ4Section(id: 9,  shortName: "10. Fa m",  fullName: "10. Fa menor (Mineur)",           measureRange: "c. 73–80",   isMinor: true),
        EJ4Section(id: 10, shortName: "11. Re♭ M", fullName: "11. Re♭ Mayor (D♭ Major)",        measureRange: "c. 81–88",   isMinor: false),
        EJ4Section(id: 11, shortName: "12. Si♭ m", fullName: "12. Si♭ menor (Mineur)",          measureRange: "c. 89–96",   isMinor: true),
        EJ4Section(id: 12, shortName: "13. Sol♭ M",fullName: "13. Sol♭ Mayor (G♭ Major)",       measureRange: "c. 97–104",  isMinor: false),
        EJ4Section(id: 13, shortName: "14. Mi♭ m", fullName: "14. Mi♭ menor (Mineur)",          measureRange: "c. 105–112", isMinor: true),
        EJ4Section(id: 14, shortName: "15. Si M",  fullName: "15. Si Mayor (B Major)",          measureRange: "c. 113–120", isMinor: false),
        EJ4Section(id: 15, shortName: "16. Sol♯ m",fullName: "16. Sol♯ menor (Mineur)",         measureRange: "c. 121–128", isMinor: true),
        EJ4Section(id: 16, shortName: "17. Mi M",  fullName: "17. Mi Mayor (E Major)",          measureRange: "c. 129–136", isMinor: false),
        EJ4Section(id: 17, shortName: "18. Do♯ m", fullName: "18. Do♯ menor (Mineur)",          measureRange: "c. 137–144", isMinor: true),
        EJ4Section(id: 18, shortName: "19. La M",  fullName: "19. La Mayor (A Major)",          measureRange: "c. 145–152", isMinor: false),
        EJ4Section(id: 19, shortName: "20. Fa♯ m", fullName: "20. Fa♯ menor (Mineur)",          measureRange: "c. 153–160", isMinor: true),
        EJ4Section(id: 20, shortName: "21. Re M",  fullName: "21. Re Mayor (D Major)",          measureRange: "c. 161–168", isMinor: false),
        EJ4Section(id: 21, shortName: "22. Si m",  fullName: "22. Si menor (Mineur)",           measureRange: "c. 169–176", isMinor: true),
        EJ4Section(id: 22, shortName: "23. Sol M", fullName: "23. Sol Mayor (G Major)",         measureRange: "c. 177–184", isMinor: false),
        EJ4Section(id: 23, shortName: "24. Mi m",  fullName: "24. Mi menor (Mineur)",           measureRange: "c. 185–192", isMinor: true),
        EJ4Section(id: 24, shortName: "25. Coda",  fullName: "25. Do Mayor (Coda Final)",       measureRange: "c. 193–194", isMinor: false)
    ]

    public func shortName(for exercise: ExerciseType) -> String {
        if id == 24 && exercise.isReichertExercise {
            return "25. D.S."
        }
        return shortName
    }

    public func fullName(for exercise: ExerciseType) -> String {
        if id == 24 && exercise.isReichertExercise {
            return "25. Do Mayor (D.S. al Fine)"
        }
        return fullName
    }

    public func measureRange(for exercise: ExerciseType) -> String {
        switch exercise {
        case .r1, .r4:
            return id < 24 ? "c. \(id * 4 + 1)–\(id * 4 + 4)" : "c. 97–100 (D.S.)"
        case .r2, .r5:
            return id < 24 ? "c. \(id * 8 + 1)–\(id * 8 + 8)" : "c. 193–200 (D.S.)"
        default:
            return measureRange
        }
    }
}

public struct EJ5Section: Identifiable, Equatable {
    public let id: Int
    public let shortName: String
    public let fullName: String
    public let measureRange: String

    public static let all: [EJ5Section] = [
        EJ5Section(id: 0,  shortName: "A. Do",    fullName: "A. Escala cromática desde Do (C4–C6)",       measureRange: "c. 1–5"),
        EJ5Section(id: 1,  shortName: "B. Re♭",   fullName: "B. Escala cromática desde Re♭ (D♭4–D♭6)",    measureRange: "c. 6–10"),
        EJ5Section(id: 2,  shortName: "C. Re",    fullName: "C. Escala cromática desde Re (D4–D6)",       measureRange: "c. 11–15"),
        EJ5Section(id: 3,  shortName: "D. Mi♭",   fullName: "D. Escala cromática desde Mi♭ (E♭4–E♭6)",    measureRange: "c. 16–20"),
        EJ5Section(id: 4,  shortName: "E. Mi",    fullName: "E. Escala cromática desde Mi (E4–E6)",       measureRange: "c. 21–25"),
        EJ5Section(id: 5,  shortName: "F. Fa",    fullName: "F. Escala cromática desde Fa (F4–F6)",       measureRange: "c. 26–30"),
        EJ5Section(id: 6,  shortName: "G. Sol♭",  fullName: "G. Escala cromática desde Sol♭ (G♭4–G♭6)",   measureRange: "c. 31–35"),
        EJ5Section(id: 7,  shortName: "H. Sol",   fullName: "H. Escala cromática desde Sol (G4–G6)",      measureRange: "c. 36–40"),
        EJ5Section(id: 8,  shortName: "I. La♭",   fullName: "I. Escala cromática desde La♭ (A♭4–A♭6)",    measureRange: "c. 41–45"),
        EJ5Section(id: 9,  shortName: "J. La",    fullName: "J. Escala cromática desde La (A4–A6)",       measureRange: "c. 46–50"),
        EJ5Section(id: 10, shortName: "K. Si♭",   fullName: "K. Escala cromática desde Si♭ (B♭4–B♭6)",    measureRange: "c. 51–55"),
        EJ5Section(id: 11, shortName: "L. Si",    fullName: "L. Escala cromática desde Si (B4–B6)",       measureRange: "c. 56–60")
    ]
}

public struct EJ10Section: Identifiable, Equatable {
    public let id: Int
    public let shortName: String
    public let fullName: String
    public let measureRange: String

    public static let all: [EJ10Section] = [
        EJ10Section(id: 0,  shortName: "1. Do",        fullName: "1. Serie sobre Do (C)",               measureRange: "c. 1–10"),
        EJ10Section(id: 1,  shortName: "2. Do♯/Re♭",   fullName: "2. Serie sobre Do♯ / Re♭ (C♯ / D♭)",  measureRange: "c. 11–20"),
        EJ10Section(id: 2,  shortName: "3. Re",        fullName: "3. Serie sobre Re (D)",               measureRange: "c. 21–30"),
        EJ10Section(id: 3,  shortName: "4. Re♯/Mi♭",   fullName: "4. Serie sobre Re♯ / Mi♭ (D♯ / E♭)",  measureRange: "c. 31–40"),
        EJ10Section(id: 4,  shortName: "5. Mi",        fullName: "5. Serie sobre Mi (E)",               measureRange: "c. 41–50"),
        EJ10Section(id: 5,  shortName: "6. Fa",        fullName: "6. Serie sobre Fa (F)",               measureRange: "c. 51–60"),
        EJ10Section(id: 6,  shortName: "7. Fa♯/Sol♭",  fullName: "7. Serie sobre Fa♯ / Sol♭ (F♯ / G♭)", measureRange: "c. 61–70"),
        EJ10Section(id: 7,  shortName: "8. Sol",       fullName: "8. Serie sobre Sol (G)",              measureRange: "c. 71–80"),
        EJ10Section(id: 8,  shortName: "9. Sol♯/La♭",  fullName: "9. Serie sobre Sol♯ / La♭ (G♯ / A♭)", measureRange: "c. 81–90"),
        EJ10Section(id: 9,  shortName: "10. La",       fullName: "10. Serie sobre La (A)",              measureRange: "c. 91–100"),
        EJ10Section(id: 10, shortName: "11. La♯/Si♭",  fullName: "11. Serie sobre La♯ / Si♭ (A♯ / B♭)", measureRange: "c. 101–110"),
        EJ10Section(id: 11, shortName: "12. Si",       fullName: "12. Serie sobre Si + Coda (B)",       measureRange: "c. 111–121")
    ]
}

public enum EJ1Articulation: Int, CaseIterable, Identifiable, Codable {
    case original = 0
    case allSlurred8 = 1
    case slurred4And4 = 2
    case staccato1Slur3 = 3
    case slur3Staccato1 = 4
    case slur2Staccato2 = 5
    case staccato2Slur2 = 6
    case staccato1Slur2Staccato1 = 7
    case pairsSlurred = 8
    case syncopatedPairs = 9
    case allStaccato = 10

    public var id: Int { rawValue }

    /// The 10 official articulations of Taffanel & Gaubert E.J. 1 (1...10)
    public static var practiceCases: [EJ1Articulation] {
        [
            .allSlurred8,
            .slurred4And4,
            .staccato1Slur3,
            .slur3Staccato1,
            .slur2Staccato2,
            .staccato2Slur2,
            .staccato1Slur2Staccato1,
            .pairsSlurred,
            .syncopatedPairs,
            .allStaccato
        ]
    }

    public var title: String {
        LocalizationManager.shared.t("ej1_art_\(rawValue)_title")
    }

    public var shortTitle: String {
        LocalizationManager.shared.t("ej1_art_\(rawValue)_short")
    }

    public var formulaBadge: String {
        switch self {
        case .original:                return "Original"
        case .allSlurred8:             return "(8)"
        case .slurred4And4:            return "(4)+(4)"
        case .staccato1Slur3:          return "·(3) ·(3)"
        case .slur3Staccato1:          return "(3)· (3)·"
        case .slur2Staccato2:          return "(2)·· (2)··"
        case .staccato2Slur2:          return "··(2) ··(2)"
        case .staccato1Slur2Staccato1: return "·(2)· ·(2)·"
        case .pairsSlurred:            return "(2)(2)(2)(2)"
        case .syncopatedPairs:         return "·(2)(2)(2)·"
        case .allStaccato:             return "········"
        }
    }

    /// Applies this E.J. 1 articulation to an 8-sixteenth-note group
    public func apply(to notes: [String]) -> String {
        guard notes.count == 8 else { return notes.joined() }
        let n = notes
        switch self {
        case .original:
            return n.joined()
        case .allSlurred8:
            return "(\(n[0])\(n[1])\(n[2])\(n[3])\(n[4])\(n[5])\(n[6])\(n[7]))"
        case .slurred4And4:
            return "(\(n[0])\(n[1])\(n[2])\(n[3]))(\(n[4])\(n[5])\(n[6])\(n[7]))"
        case .staccato1Slur3:
            return ".\(n[0])(\(n[1])\(n[2])\(n[3])).\(n[4])(\(n[5])\(n[6])\(n[7]))"
        case .slur3Staccato1:
            return "(\(n[0])\(n[1])\(n[2])).\(n[3])(\(n[4])\(n[5])\(n[6])).\(n[7])"
        case .slur2Staccato2:
            return "(\(n[0])\(n[1])).\(n[2]).\(n[3])(\(n[4])\(n[5])).\(n[6]).\(n[7])"
        case .staccato2Slur2:
            return ".\(n[0]).\(n[1])(\(n[2])\(n[3])).\(n[4]).\(n[5])(\(n[6])\(n[7]))"
        case .staccato1Slur2Staccato1:
            return ".\(n[0])(\(n[1])\(n[2])).\(n[3]).\(n[4])(\(n[5])\(n[6])).\(n[7])"
        case .pairsSlurred:
            return "(\(n[0])\(n[1]))(\(n[2])\(n[3]))(\(n[4])\(n[5]))(\(n[6])\(n[7]))"
        case .syncopatedPairs:
            return ".\(n[0])(\(n[1])\(n[2]))(\(n[3])\(n[4]))(\(n[5])\(n[6])).\(n[7])"
        case .allStaccato:
            return ".\(n[0]).\(n[1]).\(n[2]).\(n[3]).\(n[4]).\(n[5]).\(n[6]).\(n[7])"
        }
    }
}

public enum ArticulationPattern: Int, CaseIterable, Identifiable, Codable {
    case allSlurred = 1
    case slurredFourAndFour = 2
    case slurTwoStaccatoTwo = 3
    case staccatoSlurTwoStaccato = 4
    case staccatoTwoSlurTwo = 5
    case staccatoOneSlurThree = 6
    case slurThreeStaccatoOne = 7
    case allStaccato = 8

    public var id: Int { rawValue }

    public var title: String {
        switch self {
        case .allSlurred: return "Toda ligada"
        case .slurredFourAndFour: return "Ligado 4 y 4"
        case .slurTwoStaccatoTwo: return "Ligado 2, picado 2"
        case .staccatoSlurTwoStaccato: return "Picado 1, ligado 2, picado 1"
        case .staccatoTwoSlurTwo: return "Picado 2, ligado 2"
        case .staccatoOneSlurThree: return "Picado 1, ligado 3"
        case .slurThreeStaccatoOne: return "Ligado 3, picado 1"
        case .allStaccato: return "Toda picada (Staccato)"
        }
    }

    public var shortTitle: String {
        LocalizationManager.shared.t("art_\(rawValue)_short")
    }

    public var iconName: String {
        switch self {
        case .allSlurred: return "waveform.path"
        case .slurredFourAndFour: return "waveform.path.badge.plus"
        case .slurTwoStaccatoTwo: return "ellipsis"
        case .staccatoSlurTwoStaccato: return "circle.dotted"
        case .staccatoTwoSlurTwo: return "circle.grid.2x1"
        case .staccatoOneSlurThree: return "circle.grid.3x1"
        case .slurThreeStaccatoOne: return "circle.grid.3x1.fill"
        case .allStaccato: return "circle.fill"
        }
    }

    /// Applies this articulation to an 8-note sequence: [n0, n1, n2, n3, n4, n5, n6, n7]
    public func apply(to notes: [String]) -> String {
        guard notes.count == 8 else { return notes.joined() }
        let n = notes
        switch self {
        case .allSlurred:
            return "(\(n[0])\(n[1])\(n[2])\(n[3]) \(n[4])\(n[5])\(n[6])\(n[7]))"
        case .slurredFourAndFour:
            return "(\(n[0])\(n[1])\(n[2])\(n[3])) (\(n[4])\(n[5])\(n[6])\(n[7]))"
        case .slurTwoStaccatoTwo:
            return "(\(n[0])\(n[1])).\(n[2]).\(n[3]) (\(n[4])\(n[5])).\(n[6]).\(n[7])"
        case .staccatoSlurTwoStaccato:
            return ".\(n[0])(\(n[1])\(n[2])).\(n[3]) .\(n[4])(\(n[5])\(n[6])).\(n[7])"
        case .staccatoTwoSlurTwo:
            return ".\(n[0]).\(n[1])(\(n[2])\(n[3])) .\(n[4]).\(n[5])(\(n[6])\(n[7]))"
        case .staccatoOneSlurThree:
            return ".\(n[0])(\(n[1])\(n[2])\(n[3])) .\(n[4])(\(n[5])\(n[6])\(n[7]))"
        case .slurThreeStaccatoOne:
            return "(\(n[0])\(n[1])\(n[2])).\(n[3]) (\(n[4])\(n[5])\(n[6])).\(n[7])"
        case .allStaccato:
            return ".\(n[0]).\(n[1]).\(n[2]).\(n[3]) .\(n[4]).\(n[5]).\(n[6]).\(n[7])"
        }
    }

    /// Formats an 8-sixteenth-note group (E.J. 1 / E.J. 2 modal schemes)
    public func apply16ths8(to notes: [String]) -> String {
        guard notes.count == 8 else { return notes.joined() }
        let n = notes
        switch self {
        case .allSlurred:
            return "(\(n[0])\(n[1])\(n[2])\(n[3])\(n[4])\(n[5])\(n[6])\(n[7]))"
        case .slurredFourAndFour:
            return "(\(n[0])\(n[1])\(n[2])\(n[3]))(\(n[4])\(n[5])\(n[6])\(n[7]))"
        case .slurTwoStaccatoTwo:
            return "(\(n[0])\(n[1])).\(n[2]).\(n[3])(\(n[4])\(n[5])).\(n[6]).\(n[7])"
        case .staccatoSlurTwoStaccato:
            return ".\(n[0])(\(n[1])\(n[2])).\(n[3]).\(n[4])(\(n[5])\(n[6])).\(n[7])"
        case .staccatoTwoSlurTwo:
            return ".\(n[0]).\(n[1])(\(n[2])\(n[3])).\(n[4]).\(n[5])(\(n[6])\(n[7]))"
        case .staccatoOneSlurThree:
            return ".\(n[0])(\(n[1])\(n[2])\(n[3])).\(n[4])(\(n[5])\(n[6])\(n[7]))"
        case .slurThreeStaccatoOne:
            return "(\(n[0])\(n[1])\(n[2])).\(n[3])(\(n[4])\(n[5])\(n[6])).\(n[7])"
        case .allStaccato:
            return ".\(n[0]).\(n[1]).\(n[2]).\(n[3]).\(n[4]).\(n[5]).\(n[6]).\(n[7])"
        }
    }

    /// Formats a 4-sixteenth-note group (R. 2 pickup / R. 4 tail)
    public func apply16ths4(to notes: [String]) -> String {
        guard notes.count == 4 else { return notes.joined() }
        let n = notes
        switch self {
        case .allSlurred, .slurredFourAndFour:
            return "(\(n[0])\(n[1])\(n[2])\(n[3]))"
        case .slurTwoStaccatoTwo:
            return "(\(n[0])\(n[1])).\(n[2]).\(n[3])"
        case .staccatoSlurTwoStaccato:
            return ".\(n[0])(\(n[1])\(n[2])).\(n[3])"
        case .staccatoTwoSlurTwo:
            return ".\(n[0]).\(n[1])(\(n[2])\(n[3]))"
        case .staccatoOneSlurThree:
            return ".\(n[0])(\(n[1])\(n[2])\(n[3]))"
        case .slurThreeStaccatoOne:
            return "(\(n[0])\(n[1])\(n[2])).\(n[3])"
        case .allStaccato:
            return ".\(n[0]).\(n[1]).\(n[2]).\(n[3])"
        }
    }

    /// Formats a 6-sixteenth-note group (E.J. 5, E.J. 10, E.J. 11, R. 1 modal schemes)
    public func apply16ths6(to notes: [String]) -> String {
        guard notes.count == 6 else { return notes.joined() }
        let n = notes
        switch self {
        case .allSlurred:
            return "(\(n[0])\(n[1])\(n[2])\(n[3])\(n[4])\(n[5]))"
        case .slurredFourAndFour:
            return "(\(n[0])\(n[1])\(n[2]))(\(n[3])\(n[4])\(n[5]))"
        case .slurTwoStaccatoTwo:
            return "(\(n[0])\(n[1])\(n[2])\(n[3])).\(n[4]).\(n[5])"
        case .staccatoSlurTwoStaccato:
            return ".\(n[0])(\(n[1])\(n[2])).\(n[3])(\(n[4])\(n[5]))"
        case .staccatoTwoSlurTwo:
            return ".\(n[0]).\(n[1])(\(n[2])\(n[3])\(n[4])\(n[5]))"
        case .staccatoOneSlurThree:
            return "(\(n[0])\(n[1])).\(n[2])(\(n[3])\(n[4])).\(n[5])"
        case .slurThreeStaccatoOne:
            return "(\(n[0])\(n[1])\(n[2])).\(n[3]).\(n[4]).\(n[5])"
        case .allStaccato:
            return ".\(n[0]).\(n[1]).\(n[2]).\(n[3]).\(n[4]).\(n[5])"
        }
    }

    /// Formats a 6-note triplet pair (R. 5 modal scheme)
    public func applyTripletPair(to notes: [String]) -> String {
        guard notes.count == 6 else { return notes.joined() }
        let n = notes
        switch self {
        case .allSlurred:
            return "((3\(n[0])\(n[1])\(n[2])(3\(n[3])\(n[4])\(n[5]))"
        case .slurredFourAndFour:
            return "((3\(n[0])\(n[1])\(n[2])) ((3\(n[3])\(n[4])\(n[5]))"
        case .slurTwoStaccatoTwo:
            return "((3\(n[0])\(n[1])\(n[2])(3\(n[3])).\(n[4]).\(n[5])"
        case .staccatoSlurTwoStaccato:
            return "(3.\(n[0])(\(n[1])\(n[2])) (3.\(n[3])(\(n[4])\(n[5]))"
        case .staccatoTwoSlurTwo:
            return "(3.\(n[0]).\(n[1])(\(n[2])(3\(n[3])\(n[4])\(n[5]))"
        case .staccatoOneSlurThree:
            return "(3(\(n[0])\(n[1])).\(n[2]) (3(\(n[3])\(n[4])).\(n[5])"
        case .slurThreeStaccatoOne:
            return "((3\(n[0])\(n[1])\(n[2])) (3.\(n[3]).\(n[4]).\(n[5])"
        case .allStaccato:
            return "(3.\(n[0]).\(n[1]).\(n[2]) (3.\(n[3]).\(n[4]).\(n[5])"
        }
    }
}

/// 10 Technical Schemes for the 84 Parallel Modes (84 × 10 = 840 Modal Variations)
public enum ModalScheme: String, CaseIterable, Identifiable, Codable {
    case ej1  = "ej1"
    case ej2  = "ej2"
    case ej4  = "ej4"
    case ej5  = "ej5"
    case ej10 = "ej10"
    case ej11 = "ej11"
    case r1   = "r1"
    case r2   = "r2"
    case r4   = "r4"
    case r5   = "r5"

    public var id: String { rawValue }

    public var code: String {
        switch self {
        case .ej1:  return "EJ1"
        case .ej2:  return "EJ2"
        case .ej4:  return "EJ4"
        case .ej5:  return "EJ5"
        case .ej10: return "EJ10"
        case .ej11: return "EJ11"
        case .r1:   return "R1"
        case .r2:   return "R2"
        case .r4:   return "R4"
        case .r5:   return "R5"
        }
    }

    public var shortName: String {
        switch self {
        case .ej1:  return "E.J. 1"
        case .ej2:  return "E.J. 2"
        case .ej4:  return "E.J. 4"
        case .ej5:  return "E.J. 5"
        case .ej10: return "E.J. 10"
        case .ej11: return "E.J. 11"
        case .r1:   return "R. 1"
        case .r2:   return "R. 2"
        case .r4:   return "R. 4"
        case .r5:   return "R. 5"
        }
    }

    public var pillLabel: String { shortName }

    public var isReichert: Bool {
        switch self {
        case .r1, .r2, .r4, .r5: return true
        default: return false
        }
    }

    public var meter: String {
        switch self {
        case .ej1, .ej2, .ej4: return "4/2"
        case .ej5, .ej10, .r1: return "6/8"
        case .ej11:            return "9/8"
        case .r2, .r5:         return "2/4"
        case .r4:              return "C"
        }
    }

    public var unitLen: String {
        self == .ej4 ? "1/8" : "1/16"
    }

    public var barsPerStaff: Int {
        switch self {
        case .ej1, .ej2:                         return 1
        case .ej4, .ej5, .ej10, .ej11, .r1, .r4: return 2
        case .r2, .r5:                           return 4
        }
    }

    public var totalNotes: Int {
        switch self {
        case .ej1, .ej2: return 257
        case .ej4:       return 127
        case .ej5:       return 49
        case .ej10:      return 97
        case .ej11:      return 145
        case .r1:        return 43
        case .r2, .r4:   return 61
        case .r5:        return 91
        }
    }

    public var measuresCount: Int {
        switch self {
        case .ej1, .ej2, .ej10, .ej11: return 9
        case .ej4, .r2, .r5:           return 8
        case .ej5:                     return 5
        case .r1, .r4:                 return 4
        }
    }

    public var sourceRef: String {
        isReichert ? "M.-A. Reichert Op. 5" : "Taffanel & Gaubert"
    }

    public func title(_ loc: LocalizationManager = .shared) -> String {
        let isEn = loc.currentLanguage == .english
        switch self {
        case .ej1:  return isEn ? "E.J. 1 · Modal Pentachords by Degree" : "E.J. 1 · Pentacordios Modales por Grados"
        case .ej2:  return isEn ? "E.J. 2 · Harmonic Modal Pentachords" : "E.J. 2 · Pentacordios Modales en Progresión"
        case .ej4:  return isEn ? "E.J. 4 · Canonical 2-Octave Modal Scale" : "E.J. 4 · Escala Modal Canónica en 2 Octavas"
        case .ej5:  return isEn ? "E.J. 5 · Continuous 6/8 Modal Scale" : "E.J. 5 · Escala Modal Continua en 6/8"
        case .ej10: return isEn ? "E.J. 10 · 2-Octave Modal Arpeggios" : "E.J. 10 · Arpegios Modales de 2 Octavas"
        case .ej11: return isEn ? "E.J. 11 · Broken Modal Arpeggios (9/8)" : "E.J. 11 · Arpegios Modales Quebrados (9/8)"
        case .r1:   return isEn ? "R. 1 · Reichert Op. 5 No. 1 Gruppetti (6/8)" : "R. 1 · Grupetos Modales Reichert Nº 1 (6/8)"
        case .r2:   return isEn ? "R. 2 · Reichert Op. 5 No. 2 Arpeggios (2/4)" : "R. 2 · Arpegios con Anacrusa Reichert Nº 2 (2/4)"
        case .r4:   return isEn ? "R. 4 · Reichert Op. 5 No. 4 Diatonic Leaps" : "R. 4 · Saltos Diatónicos Reichert Nº 4 (4/4)"
        case .r5:   return isEn ? "R. 5 · Reichert Op. 5 No. 5 Triplets (2/4)" : "R. 5 · Tresillos Modales Reichert Nº 5 (2/4)"
        }
    }

    public func pedagogy(_ loc: LocalizationManager = .shared) -> String {
        let isEn = loc.currentLanguage == .english
        switch self {
        case .ej1:  return isEn ? "5-note modal cells ascending step-by-step I–VIII (257 notes · 4/2)" : "Células de 5 notas sobre los 8 grados del modo I–VIII (257 notas · 4/2)"
        case .ej2:  return isEn ? "Modal pentachords over degrees I–III–V–I8–IV8–VI–IV–II–I (257 notes)" : "Pentacordios modales sobre grados I–III–V–I8–IV8–VI–IV–II–I (257 notas)"
        case .ej4:  return isEn ? "Taffanel E.J. 4 overlapping 8-note waves across 2 octaves (127 notes)" : "Olas progresivas de 8 corcheas de Taffanel E.J. 4 en 2 octavas (127 notas)"
        case .ej5:  return isEn ? "Uninterrupted 2-octave modal velocity stream in 6/8 (49 notes)" : "Flujo modal ininterrumpido de 2 octavas en 6/8 (49 notas)"
        case .ej10: return isEn ? "7th chords built on every degree of the parallel mode (97 notes · 6/8)" : "Acordes de 7ª sobre los 7 grados del modo paralelo (97 notas · 6/8)"
        case .ej11: return isEn ? "Broken thirds & fourths across all 7 modal chords (145 notes · 9/8)" : "Arpegios quebrados sobre los 7 acordes del modo (145 notas · 9/8)"
        case .r1:   return isEn ? "Turn figures & register leaps culminating in a 2-octave tonic arpeggio" : "Giros melódicos en 6/8 culminando en gran arpegio modal de 2 octavas"
        case .r2:   return isEn ? "Pickup arpeggio waves alternating I and VII across 2 octaves (61 notes)" : "Arpegios con anacrusa de 4 semicorcheas en 2/4 (61 notas)"
        case .r4:   return isEn ? "Arpeggio ascents with upper neighbor turns & cascade resolution (61 notes)" : "Ascenso arpegiado con bordadura superior y cascada final (61 notas)"
        case .r5:   return isEn ? "Wide-interval sixteenth triplets testing embouchure flexibility (91 notes)" : "Tresillos de semicorchea con grandes intervalos de embocadura (91 notas)"
        }
    }

    public static var taffanelSchemes: [ModalScheme] {
        [.ej1, .ej2, .ej4, .ej5, .ej10, .ej11]
    }

    public static var reichertSchemes: [ModalScheme] {
        [.r1, .r2, .r4, .r5]
    }
}

/// Step 1 of the Conservatory Coach 3-Step Practice Wizard
public enum PracticeWizardDuration: Int, CaseIterable, Identifiable {
    case min15 = 15
    case min30 = 30
    case min45 = 45

    public var id: Int { rawValue }

    public var warmupMinutes: Int {
        switch self {
        case .min15: return 4
        case .min30: return 8
        case .min45: return 12
        }
    }

    public var coreMinutes: Int {
        switch self {
        case .min15: return 7
        case .min30: return 14
        case .min45: return 20
        }
    }

    public var agilityMinutes: Int {
        switch self {
        case .min15: return 4
        case .min30: return 8
        case .min45: return 13
        }
    }

    public func label(_ loc: LocalizationManager = .shared) -> String {
        "\(rawValue) min"
    }

    public func presetTitle(_ loc: LocalizationManager = .shared) -> String {
        "\(rawValue) min"
    }

    public func subtitle(_ loc: LocalizationManager = .shared) -> String {
        let isEn = loc.currentLanguage == .english
        switch self {
        case .min15: return isEn ? "Warmup + Direct Modal Core" : "Activación + Núcleo Modal directo"
        case .min30: return isEn ? "Standard Taffanel + Reichert + Mode" : "Estándar Taffanel + Reichert + Modo"
        case .min45: return isEn ? "Full Cycle + 10 Articulations" : "Ciclo completo + 10 Articulaciones"
        }
    }
}

/// Step 2 of the Conservatory Coach 3-Step Practice Wizard
public enum PracticeWizardFocus: String, CaseIterable, Identifiable {
    case scales    = "scales"
    case arpeggios = "arpeggios"
    case reichert  = "reichert"
    case modes     = "modes"

    public var id: String { rawValue }

    public var badgeCode: String {
        switch self {
        case .scales:    return "E.J. 1 · 2 · 4 · 5"
        case .arpeggios: return "E.J. 10 · 11 · R. 2 · 4"
        case .reichert:  return "R. 1 · 2 · 4 · 5"
        case .modes:     return "84 Modos"
        }
    }

    public var iconName: String {
        switch self {
        case .scales:    return "waveform.path.ecg"
        case .arpeggios: return "tuningfork"
        case .reichert:  return "bolt.fill"
        case .modes:     return "sparkles"
        }
    }

    public func title(_ loc: LocalizationManager = .shared) -> String {
        let isEn = loc.currentLanguage == .english
        switch self {
        case .scales:    return isEn ? "Scales & Finger Equality" : "Escalas / Igualdad Digital"
        case .arpeggios: return isEn ? "Arpeggios & Flexibility" : "Arpegios & Flexibilidad"
        case .reichert:  return isEn ? "Reichert Op. 5 Agility" : "Agilidad Reichert Op. 5"
        case .modes:     return isEn ? "Parallel Modes (84)" : "Modos Paralelos (84)"
        }
    }

    public func subtitle(_ loc: LocalizationManager = .shared) -> String {
        let isEn = loc.currentLanguage == .english
        switch self {
        case .scales:    return isEn ? "Pentachords, Diatonic & Chromatic" : "Pentacordios, Diatónicas y Cromáticas"
        case .arpeggios: return isEn ? "Progressive & Broken Arpeggios" : "Arpegios Progresivos y Quebrados"
        case .reichert:  return isEn ? "6/8 Gruppetti, 2/4, 4/4 & Triplets" : "Grupetos 6/8, Anacrusa, 4/4 y Tresillos"
        case .modes:     return isEn ? "12 Tonics × 7 Parallel Modes" : "12 Tónicas × 7 Modos Paralelos"
        }
    }
}

/// Generated Practice Block from Step 3 of the Conservatory Coach Wizard
public struct PracticeRoutineBlock: Identifiable, Equatable {
    public let id: Int
    public let phaseTitle: String
    public let minutes: Int
    public let exerciseTitle: String
    public let detailSubtitle: String
    public let exerciseType: ExerciseType
    public let modalScheme: ModalScheme
    public let tonic: Tonic
    public let mode: ModeType

    public static func generateRoutine(
        duration: PracticeWizardDuration,
        focus: PracticeWizardFocus,
        tonic: Tonic,
        mode: ModeType,
        loc: LocalizationManager = .shared
    ) -> [PracticeRoutineBlock] {
        let isEn = loc.currentLanguage == .english
        let tonicName = tonic.displayName
        let modeName = mode.localizedName

        let phase1 = isEn ? "1. Warmup & Sound" : "1. Calentamiento y Sonido"
        let phase2 = isEn ? "2. Technical Core" : "2. Núcleo Técnico"
        let phase3 = isEn ? "3. Agility & Closure" : "3. Agilidad y Cierre"

        switch focus {
        case .scales:
            return [
                PracticeRoutineBlock(
                    id: 1,
                    phaseTitle: phase1,
                    minutes: duration.warmupMinutes,
                    exerciseTitle: isEn ? "Taffanel E.J. 1 (Major Pentachords)" : "Taffanel E.J. 1 (Pentacordios Mayores)",
                    detailSubtitle: isEn ? "Art. 1 (All slurred) · ♩ = 72 BPM" : "Art. 1 (Toda ligada) · ♩ = 72 BPM",
                    exerciseType: .ej1,
                    modalScheme: .ej4,
                    tonic: tonic,
                    mode: mode
                ),
                PracticeRoutineBlock(
                    id: 2,
                    phaseTitle: phase2,
                    minutes: duration.coreMinutes,
                    exerciseTitle: isEn ? "Taffanel E.J. 4 (Diatonic Scales)" : "Taffanel E.J. 4 (Escalas Diatónicas)",
                    detailSubtitle: isEn ? "24 Major & Minor Keys · ♩ = 88 BPM" : "24 Tonalidades Mayores y Menores · ♩ = 88 BPM",
                    exerciseType: .ej4,
                    modalScheme: .ej4,
                    tonic: tonic,
                    mode: mode
                ),
                PracticeRoutineBlock(
                    id: 3,
                    phaseTitle: phase3,
                    minutes: duration.agilityMinutes,
                    exerciseTitle: isEn ? "Taffanel E.J. 5 (Chromatic Scales)" : "Taffanel E.J. 5 (Escalas Cromáticas)",
                    detailSubtitle: isEn ? "12 Chromatic Scales in 6/8 · ♩. = 84 BPM" : "12 Escalas Cromáticas en 6/8 · ♩. = 84 BPM",
                    exerciseType: .ej5,
                    modalScheme: .ej4,
                    tonic: tonic,
                    mode: mode
                )
            ]
        case .arpeggios:
            return [
                PracticeRoutineBlock(
                    id: 1,
                    phaseTitle: phase1,
                    minutes: duration.warmupMinutes,
                    exerciseTitle: isEn ? "Taffanel E.J. 2 (Minor Pentachords)" : "Taffanel E.J. 2 (Pentacordios Menores)",
                    detailSubtitle: isEn ? "Chromatic Minor Pentachords · ♩ = 76 BPM" : "Pentacordios Menores Cromáticos · ♩ = 76 BPM",
                    exerciseType: .ej2,
                    modalScheme: .ej4,
                    tonic: tonic,
                    mode: mode
                ),
                PracticeRoutineBlock(
                    id: 2,
                    phaseTitle: phase2,
                    minutes: duration.coreMinutes,
                    exerciseTitle: isEn ? "Taffanel E.J. 10 (Progressive Arpeggios)" : "Taffanel E.J. 10 (Arpegios Progresivos)",
                    detailSubtitle: isEn ? "120 Arpeggios in 6/8 · ♩. = 76 BPM" : "120 Arpegios en 6/8 · ♩. = 76 BPM",
                    exerciseType: .ej10,
                    modalScheme: .ej4,
                    tonic: tonic,
                    mode: mode
                ),
                PracticeRoutineBlock(
                    id: 3,
                    phaseTitle: phase3,
                    minutes: duration.agilityMinutes,
                    exerciseTitle: isEn ? "Taffanel E.J. 11 (Broken Arpeggios)" : "Taffanel E.J. 11 (Arpegios Quebrados)",
                    detailSubtitle: isEn ? "120 Broken Arpeggios in 9/8 · ♩. = 72 BPM" : "120 Arpegios Quebrados en 9/8 · ♩. = 72 BPM",
                    exerciseType: .ej11,
                    modalScheme: .ej4,
                    tonic: tonic,
                    mode: mode
                )
            ]
        case .reichert:
            return [
                PracticeRoutineBlock(
                    id: 1,
                    phaseTitle: phase1,
                    minutes: duration.warmupMinutes,
                    exerciseTitle: "Reichert Op. 5, Nº 1 (6/8)",
                    detailSubtitle: isEn ? "Melodic Gruppetti in 24 Keys · ♩. = 84 BPM" : "Grupetos Melódicos en 24 Tonalidades · ♩. = 84 BPM",
                    exerciseType: .r1,
                    modalScheme: .ej4,
                    tonic: tonic,
                    mode: mode
                ),
                PracticeRoutineBlock(
                    id: 2,
                    phaseTitle: phase2,
                    minutes: duration.coreMinutes,
                    exerciseTitle: "Reichert Op. 5, Nº 2 & Nº 4",
                    detailSubtitle: isEn ? "Modulating Arpeggios & Diatonic Leaps · ♩ = 112 BPM" : "Arpegios Modulantes y Saltos Diatónicos · ♩ = 112 BPM",
                    exerciseType: .r2,
                    modalScheme: .ej4,
                    tonic: tonic,
                    mode: mode
                ),
                PracticeRoutineBlock(
                    id: 3,
                    phaseTitle: phase3,
                    minutes: duration.agilityMinutes,
                    exerciseTitle: "Reichert Op. 5, Nº 5 (2/4)",
                    detailSubtitle: isEn ? "Sixteenth-Note Triplets in 24 Keys · ♩ = 88 BPM" : "Tresillos de Semicorchea en 24 Tonalidades · ♩ = 88 BPM",
                    exerciseType: .r5,
                    modalScheme: .ej4,
                    tonic: tonic,
                    mode: mode
                )
            ]
        case .modes:
            return [
                PracticeRoutineBlock(
                    id: 1,
                    phaseTitle: phase1,
                    minutes: duration.warmupMinutes,
                    exerciseTitle: isEn ? "Taffanel E.J. 1 (Warmup)" : "Taffanel E.J. 1 (Calentamiento)",
                    detailSubtitle: isEn ? "Chromatic Pentachords · ♩ = 80 BPM" : "Pentacordios Cromáticos · ♩ = 80 BPM",
                    exerciseType: .ej1,
                    modalScheme: .ej4,
                    tonic: tonic,
                    mode: mode
                ),
                PracticeRoutineBlock(
                    id: 2,
                    phaseTitle: phase2,
                    minutes: duration.coreMinutes,
                    exerciseTitle: "\(tonicName) \(modeName)",
                    detailSubtitle: isEn ? "2-Octave Parallel Modal Scale (84 Modes) · ♩ = 90 BPM" : "Escala Modal Paralela en 2 Octavas (84 Modos) · ♩ = 90 BPM",
                    exerciseType: .modos,
                    modalScheme: .ej4,
                    tonic: tonic,
                    mode: mode
                ),
                PracticeRoutineBlock(
                    id: 3,
                    phaseTitle: phase3,
                    minutes: duration.agilityMinutes,
                    exerciseTitle: "Reichert Op. 5, Nº 1 (6/8)",
                    detailSubtitle: isEn ? "24 Major & Minor Keys · ♩. = 88 BPM" : "24 Tonalidades Mayores y Menores · ♩. = 88 BPM",
                    exerciseType: .r1,
                    modalScheme: .ej4,
                    tonic: tonic,
                    mode: mode
                )
            ]
        }
    }
}

/// Bilingual strings for Opción 1 (Conservatory Coach), 3-Step Practice Wizard & 3-Level Modes Explorer
public enum CoachStrings {
    public static func coachBadge(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_badge")
    }
    public static func coachTitle(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_title")
    }
    public static func coachSubtitle(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_subtitle")
    }
    public static func openWizardBtn(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_open_wizard")
    }
    public static func resumeBannerTitle(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_resume_banner")
    }
    public static func resumeAction(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_resume_action")
    }
    public static func step1Title(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_step1_title")
    }
    public static func step2Title(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_step2_title")
    }
    public static func step3Title(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_step3_title")
    }
    public static func launchRoutineBtn(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_launch_routine")
    }
    public static func level1TonicLabel(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_level1_tonic")
    }
    public static func level2ModeLabel(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_level2_mode")
    }
    public static func level3SchemeLabel(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_level3_scheme")
    }
    public static func taffanelGroupLabel(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_taffanel_group")
    }
    public static func reichertGroupLabel(_ loc: LocalizationManager = .shared) -> String {
        loc.t("coach_reichert_group")
    }
}

