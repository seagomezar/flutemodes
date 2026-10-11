import Foundation

public enum ExerciseType: String, CaseIterable, Identifiable, Codable {
    case ej1 = "EJ1"
    case ej2 = "EJ2"
    case ej4 = "EJ4"
    case ej5 = "EJ5"
    case ej10 = "EJ10"
    case ej11 = "EJ11"
    case modos = "MODOS"

    public var id: String { rawValue }

    public var isChromaticExercise: Bool {
        self == .ej1 || self == .ej2
    }

    public var isEJ4Exercise: Bool {
        self == .ej4
    }

    public var isEJ5TypeExercise: Bool {
        self == .ej5 || self == .ej10 || self == .ej11
    }

    public var isSectionedLeducExercise: Bool {
        self == .ej4 || self == .ej5 || self == .ej10 || self == .ej11
    }

    public var isLeducExercise: Bool {
        self != .modos
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
        case .modos: return isEn ? "84 Modes" : "84 Modos"
        }
    }

    public var shortName: String { displayTitle }
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

    public var title: String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .original:                return isEn ? "Original (As written — A. L. 16.588)" : "Original (Como está escrito — A. L. 16.588)"
        case .allSlurred8:             return isEn ? "1. 8 slurred: (CDEFGABc)" : "1. 8 ligadas: (CDEFGABc)"
        case .slurred4And4:            return isEn ? "2. 4 and 4 slurred: (CDEF)(GABc)" : "2. 4 y 4 ligadas: (CDEF)(GABc)"
        case .staccato1Slur3:          return isEn ? "3. 1 staccato, 3 slurred: .C(DEF) .G(ABc)" : "3. 1 picada y 3 ligadas: .C(DEF) .G(ABc)"
        case .slur2Staccato2:          return isEn ? "4. 2 slurred, 2 staccato: (CD).E.F (GA).B.c" : "4. 2 ligadas y 2 picadas: (CD).E.F (GA).B.c"
        case .staccato2Slur2:          return isEn ? "5. 2 staccato, 2 slurred: .C.D(EF) .G.A(Bc)" : "5. 2 picadas y 2 ligadas: .C.D(EF) .G.A(Bc)"
        case .staccato1Slur2Staccato1: return isEn ? "6. 1 stacc., 2 slurred, 1 stacc.: .C(DE).F .G(AB).c" : "6. 1 picada, 2 ligadas y 1 picada: .C(DE).F .G(AB).c"
        case .pairsSlurred:            return isEn ? "7. Slurred in pairs: (CD)(EF)(GA)(Bc)" : "7. De 2 en 2 ligadas: (CD)(EF)(GA)(Bc)"
        case .syncopatedPairs:         return isEn ? "8. Syncopated pairs: .C(DE)(FG)(AB).c" : "8. De 2 en 2 sincopadas: .C(DE)(FG)(AB).c"
        }
    }

    public var shortTitle: String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .original:                return "Orig."
        case .allSlurred8:             return isEn ? "1: 8 Slur" : "1: 8 Lig."
        case .slurred4And4:            return isEn ? "2: 4+4" : "2: 4+4"
        case .staccato1Slur3:          return isEn ? "3: 1P+3L" : "3: 1P+3L"
        case .slur2Staccato2:          return isEn ? "4: 2L+2P" : "4: 2L+2P"
        case .staccato2Slur2:          return isEn ? "5: 2P+2L" : "5: 2P+2L"
        case .staccato1Slur2Staccato1: return isEn ? "6: 1P+2L+1P" : "6: 1P+2L+1P"
        case .pairsSlurred:            return isEn ? "7: 2+2" : "7: 2 en 2"
        case .syncopatedPairs:         return isEn ? "8: Sync." : "8: Sinc."
        }
    }

    public var formulaBadge: String {
        switch self {
        case .original:                return "A.L. 16.588"
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
            return isEn ? "0. Original (As written — A. L. 16.588)" : "0. Original (Como está escrito — A. L. 16.588)"
        case .allSlurred:
            return is98
                ? (isEn ? "1. 18 slurred (full measure)" : "1. 18 ligadas (compás completo)")
                : (isEn ? "1. 12 slurred (full measure)" : "1. 12 ligadas (compás completo)")
        case .slurredSixBySix:
            return is98
                ? (isEn ? "2. 6+6+6 slurred (by beats)" : "2. 6+6+6 ligadas (por tiempos)")
                : (isEn ? "2. 6 and 6 slurred (by beats)" : "2. 6 y 6 ligadas (por tiempos)")
        case .slur4Stacc2:
            return isEn ? "3. 4 slurred and 2 staccato" : "3. 4 ligadas y 2 picadas"
        case .stacc2Slur4:
            return isEn ? "4. 2 staccato and 4 slurred" : "4. 2 picadas y 4 ligadas"
        case .slur2Stacc4:
            return isEn ? "5. 2 slurred and 4 staccato" : "5. 2 ligadas y 4 picadas"
        case .slurredThreeByThree:
            return is98
                ? (isEn ? "6. Slurred in 3s (3/4)" : "6. De 3 en 3 ligadas (3/4)")
                : (isEn ? "6. Slurred in 3s (2/4)" : "6. De 3 en 3 ligadas (2/4)")
        case .slur3Stacc3:
            return is98
                ? (isEn ? "7. 3 slurred, 3 staccato (3/4)" : "7. 3 ligadas y 3 picadas (3/4)")
                : (isEn ? "7. 3 slurred, 3 staccato (2/4)" : "7. 3 ligadas y 3 picadas (2/4)")
        case .pairsSlurred:
            return isEn ? "8. Slurred in pairs" : "8. De 2 en 2 ligadas"
        case .syncopatedPairs:
            return isEn ? "9. Syncopated pairs" : "9. De 2 en 2 sincopadas"
        case .allStaccato:
            return isEn ? "10. All staccato" : "10. Todas picadas (Staccato)"
        }
    }

    public var title: String { title(for: .ej5) }

    public func shortTitle(for exercise: ExerciseType = .ej5) -> String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        let is98 = (exercise == .ej11)
        switch self {
        case .original:            return "Orig."
        case .allSlurred:          return is98 ? (isEn ? "1: 18 Slur" : "1: 18 Lig.") : (isEn ? "1: 12 Slur" : "1: 12 Lig.")
        case .slurredSixBySix:     return is98 ? "2: 6+6+6" : "2: 6+6"
        case .slur4Stacc2:         return "3: 4L+2P"
        case .stacc2Slur4:         return "4: 2P+4L"
        case .slur2Stacc4:         return "5: 2L+4P"
        case .slurredThreeByThree: return isEn ? "6: 3 by 3" : "6: 3 en 3"
        case .slur3Stacc3:         return "7: 3L+3P"
        case .pairsSlurred:        return isEn ? "8: 2 by 2" : "8: 2 en 2"
        case .syncopatedPairs:     return isEn ? "9: Sync." : "9: Sinc."
        case .allStaccato:         return "10: Stacc."
        }
    }

    public var shortTitle: String { shortTitle(for: .ej5) }

    public func formulaBadge(for exercise: ExerciseType = .ej5) -> String {
        let is98 = (exercise == .ej11)
        switch self {
        case .original:            return is98 ? "9/8 · 3/4" : "6/8 · 2/4"
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
        case .original:                return "A.L. 16.588"
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
        case .allSlurred: return "1. Toda ligada"
        case .slurredFourAndFour: return "2. Ligado 4 y 4"
        case .slurTwoStaccatoTwo: return "3. Ligado 2, picado 2"
        case .staccatoSlurTwoStaccato: return "4. Picado 1, ligado 2, picado 1"
        case .staccatoTwoSlurTwo: return "5. Picado 2, ligado 2"
        case .staccatoOneSlurThree: return "6. Picado 1, ligado 3"
        case .slurThreeStaccatoOne: return "7. Ligado 3, picado 1"
        case .allStaccato: return "8. Toda picada (Staccato)"
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
}
