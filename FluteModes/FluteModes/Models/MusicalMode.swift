import Foundation

public enum ModeFamily: String, CaseIterable, Identifiable, Codable {
    case major = "Familia Mayor"
    case minor = "Familia Menor"

    public var id: String { rawValue }
}

public enum ModeType: Int, CaseIterable, Identifiable, Codable {
    case ionian = 1
    case lydian = 2
    case mixolydian = 3
    case dorian = 4
    case aeolian = 5
    case phrygian = 6
    case locrian = 7

    public var id: Int { rawValue }

    public var family: ModeFamily {
        switch self {
        case .ionian, .lydian, .mixolydian:
            return .major
        case .dorian, .aeolian, .phrygian, .locrian:
            return .minor
        }
    }

    public var intervals: [Int] {
        switch self {
        case .ionian:     return [0, 2, 4, 5, 7, 9, 11]
        case .lydian:     return [0, 2, 4, 6, 7, 9, 11]
        case .mixolydian: return [0, 2, 4, 5, 7, 9, 10]
        case .dorian:     return [0, 2, 3, 5, 7, 9, 10]
        case .aeolian:    return [0, 2, 3, 5, 7, 8, 10]
        case .phrygian:   return [0, 1, 3, 5, 7, 8, 10]
        case .locrian:    return [0, 1, 3, 5, 6, 8, 10]
        }
    }

    public var name: String {
        switch self {
        case .ionian: return LocalizationManager.shared.t("mode_1_name")
        case .lydian: return LocalizationManager.shared.t("mode_2_name")
        case .mixolydian: return LocalizationManager.shared.t("mode_3_name")
        case .dorian: return LocalizationManager.shared.t("mode_4_name")
        case .aeolian: return LocalizationManager.shared.t("mode_5_name")
        case .phrygian: return LocalizationManager.shared.t("mode_6_name")
        case .locrian: return LocalizationManager.shared.t("mode_7_name")
        }
    }

    public var character: String {
        switch self {
        case .ionian: return "Brillante y luminoso"
        case .lydian: return "Etéreo y soñador"
        case .mixolydian: return "Festivo y folclórico"
        case .dorian: return "Melancólico y noble"
        case .aeolian: return "Triste e introspectivo"
        case .phrygian: return "Oscuro y exótico"
        case .locrian: return "Inestable y tenso"
        }
    }

    public var formula: String {
        switch self {
        case .ionian: return "1 - 2 - 3 - 4 - 5 - 6 - 7"
        case .lydian: return "1 - 2 - 3 - ♯4 - 5 - 6 - 7"
        case .mixolydian: return "1 - 2 - 3 - 4 - 5 - 6 - ♭7"
        case .dorian: return "1 - 2 - ♭3 - 4 - 5 - 6 - ♭7"
        case .aeolian: return "1 - 2 - ♭3 - 4 - 5 - ♭6 - ♭7"
        case .phrygian: return "1 - ♭2 - ♭3 - 4 - 5 - ♭6 - ♭7"
        case .locrian: return "1 - ♭2 - ♭3 - 4 - ♭5 - ♭6 - ♭7"
        }
    }

    public func accidentalBadge(for tonic: Tonic) -> String {
        switch self {
        case .ionian:
            return LocalizationManager.shared.t("acc_ionian")
        case .lydian:
            return LocalizationManager.shared.t("acc_lydian")
        case .mixolydian:
            return LocalizationManager.shared.t("acc_mixolydian")
        case .dorian:
            return LocalizationManager.shared.t("acc_dorian")
        case .aeolian:
            return LocalizationManager.shared.t("acc_aeolian")
        case .phrygian:
            return LocalizationManager.shared.t("acc_phrygian")
        case .locrian:
            return LocalizationManager.shared.t("acc_locrian")
        }
    }

    public func keySignature(for tonic: Tonic) -> String {
        switch family {
        case .major:
            return tonic.majorKey
        case .minor:
            return tonic.minorKey
        }
    }

    public func keyDescription(for tonic: Tonic) -> String {
        switch family {
        case .major:
            return "Armadura fija: \(tonic.majorKey) Mayor (\(tonic.majorDesc))"
        case .minor:
            return "Armadura fija: \(tonic.minorKey) Menor (\(tonic.minorDesc))"
        }
    }
}
