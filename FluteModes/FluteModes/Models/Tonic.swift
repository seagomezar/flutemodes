import Foundation

public enum Tonic: String, CaseIterable, Identifiable, Codable {
    case si = "Si"
    case doNatural = "Do"
    case doSostenido = "Do♯"
    case re = "Re"
    case miBemol = "Mi♭"
    case mi = "Mi"
    case fa = "Fa"
    case faSostenido = "Fa♯"
    case sol = "Sol"
    case laBemol = "La♭"
    case la = "La"
    case siBemol = "Si♭"

    public var id: String { rawValue }

    public var fullName: String {
        switch self {
        case .si: return "Si (B3 - Pata de Si)"
        case .doNatural: return "Do"
        case .doSostenido: return "Do sostenido (Do♯)"
        case .re: return "Re"
        case .miBemol: return "Mi bemol (Mi♭)"
        case .mi: return "Mi"
        case .fa: return "Fa"
        case .faSostenido: return "Fa sostenido (Fa♯)"
        case .sol: return "Sol"
        case .laBemol: return "La bemol (La♭)"
        case .la: return "La"
        case .siBemol: return "Si bemol (Si♭)"
        }
    }

    public var majorKey: String {
        switch self {
        case .si: return "B"
        case .doNatural: return "C"
        case .doSostenido: return "C#"
        case .re: return "D"
        case .miBemol: return "Eb"
        case .mi: return "E"
        case .fa: return "F"
        case .faSostenido: return "F#"
        case .sol: return "G"
        case .laBemol: return "Ab"
        case .la: return "A"
        case .siBemol: return "Bb"
        }
    }

    public var minorKey: String {
        switch self {
        case .si: return "Bm"
        case .doNatural: return "Cm"
        case .doSostenido: return "C#m"
        case .re: return "Dm"
        case .miBemol: return "Ebm"
        case .mi: return "Em"
        case .fa: return "Fm"
        case .faSostenido: return "F#m"
        case .sol: return "Gm"
        case .laBemol: return "Abm"
        case .la: return "Am"
        case .siBemol: return "Bbm"
        }
    }

    public var majorDesc: String {
        switch self {
        case .si: return "5 sostenidos (Fa♯, Do♯, Sol♯, Re♯, La♯)"
        case .doNatural: return "Sin alteraciones"
        case .doSostenido: return "7 sostenidos"
        case .re: return "2 sostenidos (Fa♯, Do♯)"
        case .miBemol: return "3 bemoles (Si♭, Mi♭, La♭)"
        case .mi: return "4 sostenidos (Fa♯, Do♯, Sol♯, Re♯)"
        case .fa: return "1 bemol (Si♭)"
        case .faSostenido: return "6 sostenidos"
        case .sol: return "1 sostenido (Fa♯)"
        case .laBemol: return "4 bemoles (Si♭, Mi♭, La♭, Re♭)"
        case .la: return "3 sostenidos (Fa♯, Do♯, Sol♯)"
        case .siBemol: return "2 bemoles (Si♭, Mi♭)"
        }
    }

    public var minorDesc: String {
        switch self {
        case .si: return "2 sostenidos (Fa♯, Do♯)"
        case .doNatural: return "3 bemoles (Si♭, Mi♭, La♭)"
        case .doSostenido: return "4 sostenidos (Fa♯, Do♯, Sol♯, Re♯)"
        case .re: return "1 bemol (Si♭)"
        case .miBemol: return "6 bemoles"
        case .mi: return "1 sostenido (Fa♯)"
        case .fa: return "4 bemoles (Si♭, Mi♭, La♭, Re♭)"
        case .faSostenido: return "3 sostenidos (Fa♯, Do♯, Sol♯)"
        case .sol: return "2 bemoles (Si♭, Mi♭)"
        case .laBemol: return "7 bemoles"
        case .la: return "Sin alteraciones"
        case .siBemol: return "5 bemoles"
        }
    }

    public var abcNoteSequence: [String] {
        switch self {
        case .si:
            return ["B,", "C", "D", "E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'"]
        case .doNatural, .doSostenido:
            return ["C", "D", "E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'"]
        case .re:
            return ["D", "E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'"]
        case .miBemol, .mi:
            return ["E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'"]
        case .fa, .faSostenido:
            return ["F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'"]
        case .sol:
            return ["G", "A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'"]
        case .laBemol, .la:
            return ["A", "B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'", "b'"]
        case .siBemol:
            return ["B", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"]
        }
    }

    public func accidentalMap(for mode: ModeType) -> [Int: String] {
        switch mode {
        case .ionian, .aeolian:
            return [:]
        case .lydian:
            switch self {
            case .doNatural, .re, .mi, .faSostenido, .sol, .la, .si: return [3: "^"]
            case .doSostenido: return [3: "^^"]
            case .miBemol, .fa, .laBemol, .siBemol: return [3: "="]
            }
        case .mixolydian:
            switch self {
            case .si, .doSostenido, .re, .mi, .faSostenido, .sol, .la: return [6: "="]
            case .doNatural, .miBemol, .fa, .laBemol, .siBemol: return [6: "_"]
            }
        case .dorian:
            switch self {
            case .si, .doSostenido, .mi, .faSostenido, .la: return [5: "^"]
            case .doNatural, .re, .miBemol, .fa, .sol, .laBemol, .siBemol: return [5: "="]
            }
        case .phrygian:
            switch self {
            case .si, .doSostenido, .mi, .faSostenido, .la: return [1: "="]
            case .doNatural, .re, .miBemol, .fa, .sol, .laBemol, .siBemol: return [1: "_"]
            }
        case .locrian:
            switch self {
            case .si, .doSostenido, .faSostenido: return [1: "=", 4: "="]
            case .mi: return [1: "=", 4: "_"]
            case .la: return [1: "^", 4: "_"]
            default: return [1: "_", 4: "_"]
            }
        }
    }
}
