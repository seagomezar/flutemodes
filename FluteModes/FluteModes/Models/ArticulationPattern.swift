import Foundation

public enum ExerciseType: String, CaseIterable, Identifiable, Codable {
    case ej1 = "EJ1"
    case ej2 = "EJ2"
    case ej4 = "EJ4"
    case modos = "MODOS"

    public var id: String { rawValue }

    public var isChromaticExercise: Bool {
        self == .ej1 || self == .ej2
    }

    public var isLeducExercise: Bool {
        self == .ej1 || self == .ej2 || self == .ej4
    }

    public var pillLabel: String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .ej1: return "E.J. 1"
        case .ej2: return "E.J. 2"
        case .ej4: return "E.J. 4"
        case .modos: return isEn ? "84 Modes" : "84 Modos"
        }
    }

    public var displayTitle: String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .ej1: return isEn ? "E.J. 1 · Major (10 Arts.)" : "E.J. 1 · Mayor (10 Arts.)"
        case .ej2: return isEn ? "E.J. 2 · Minor (10 Arts.)" : "E.J. 2 · Menor (10 Arts.)"
        case .ej4: return isEn ? "E.J. 4 · 24 Keys (8 Arts.)" : "E.J. 4 · 24 Ton. (8 Arts.)"
        case .modos: return isEn ? "84 Parallel Modes" : "84 Modos Paralelos"
        }
    }

    public var shortLabel: String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .ej1: return isEn ? "E.J. 1 (Major)" : "E.J. 1 (Mayor)"
        case .ej2: return isEn ? "E.J. 2 (Minor)" : "E.J. 2 (Menor)"
        case .ej4: return isEn ? "E.J. 4 (24 Keys)" : "E.J. 4 (24 Ton.)"
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
