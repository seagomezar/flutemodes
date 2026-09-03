import Foundation

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
