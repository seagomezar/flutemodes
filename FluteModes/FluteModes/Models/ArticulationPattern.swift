import Foundation

public enum ExerciseType: String, CaseIterable, Identifiable, Codable {
    case ej1 = "EJ1"
    case ej2 = "EJ2"
    case ej4 = "EJ4"

    public var id: String { rawValue }

    public var isChromaticExercise: Bool {
        self == .ej1 || self == .ej2
    }

    public var pillLabel: String {
        switch self {
        case .ej1: return "E.J. 1"
        case .ej2: return "E.J. 2"
        case .ej4: return "E.J. 4"
        }
    }

    public var displayTitle: String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .ej1: return isEn ? "E.J. 1 · Major (10 Arts.)" : "E.J. 1 · Mayor (10 Arts.)"
        case .ej2: return isEn ? "E.J. 2 · Minor (10 Arts.)" : "E.J. 2 · Menor (10 Arts.)"
        case .ej4: return isEn ? "E.J. 4 · 84 Parallel Modes" : "E.J. 4 · 84 Modos Paralelos"
        }
    }

    public var shortLabel: String {
        let isEn = LocalizationManager.shared.currentLanguage == .english
        switch self {
        case .ej1: return isEn ? "E.J. 1 (Major)" : "E.J. 1 (Mayor)"
        case .ej2: return isEn ? "E.J. 2 (Minor)" : "E.J. 2 (Menor)"
        case .ej4: return isEn ? "E.J. 4 (84 Modes)" : "E.J. 4 (84 Modos)"
        }
    }

    public var shortName: String { displayTitle }
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
