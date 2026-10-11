import Foundation

public struct ExerciseGenerator {

    internal static let ej1RawMeasures: [(num: Int, beats: [[String]], prefix: String, suffix: String)] = [
        (1,  [["D","E","^F","G","A","G","F","E"], ["D","E","F","G","A","G","F","E"], ["D","E","F","G","A","G","F","E"], ["D","E","F","G","A","G","F","E"]], "|:", "|"),
        (2,  [["D","_E","=F","G","_A","G","F","E"], ["D","E","F","G","A","G","F","E"], ["D","E","F","G","A","G","F","E"], ["D","E","F","G","A","F","E","D"]], "", "|"),
        (3,  [["_E","F","G","_A","_B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"]], "", "|"),
        (4,  [["^D","=E","^F","^G","=A","G","F","E"], ["D","E","F","G","A","G","F","E"], ["D","E","F","G","A","G","F","E"], ["D","E","F","G","A","F","E","D"]], "", "|"),
        (5,  [["E","^F","^G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"]], "", "|"),
        (6,  [["E","=F","=G","A","_B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","G","F","E"]], "", "|"),
        (7,  [["F","G","A","_B","c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","B","A","G"]], "", "|"),
        (8,  [["^E","^F","^G","^A","=B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","G","F","E"]], "", "|"),
        (9,  [["^F","^G","^A","B","^c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","B","A","G"]], "", "|"),
        (10, [["^F","=G","=A","B","=c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","A","G","F"]], "", "|"),
        (11, [["G","A","B","c","d","c","B","A"], ["G","A","B","c","d","c","B","A"], ["G","A","B","c","d","c","B","A"], ["G","A","B","c","d","c","B","A"]], "", "|"),
        (12, [["G","_A","_B","c","_d","c","B","A"], ["G","A","B","c","d","c","B","A"], ["G","A","B","c","d","c","B","A"], ["G","A","B","c","d","B","A","G"]], "", "|"),
        (13, [["_A","_B","c","_d","_e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","d","c","B"]], "", "|"),
        (14, [["^G","=A","=B","^c","=d","c","B","A"], ["G","A","B","c","d","c","B","A"], ["G","A","B","c","d","c","B","A"], ["G","A","B","c","d","B","A","G"]], "", "|"),
        (15, [["A","B","^c","d","e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","d","c","B"]], "", "|"),
        (16, [["A","_B","=c","d","_e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","c","B","A"]], "", "|"),
        (17, [["_B","c","d","_e","f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","e","d","c"]], "", "|"),
        (18, [["^A","=B","^c","^d","e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","c","B","A"]], "", "|"),
        (19, [["B","^c","^d","e","^f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","e","d","c"]], "", "|"),
        (20, [["B","=c","=d","e","=f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","d","c","B"]], "", "|"),
        (21, [["c","d","e","f","g","f","e","d"], ["c","d","e","f","g","f","e","d"], ["c","d","e","f","g","f","e","d"], ["c","d","e","f","g","f","e","d"]], "", "|"),
        (22, [["c","_d","_e","f","_g","f","e","d"], ["c","d","e","f","g","f","e","d"], ["c","d","e","f","g","f","e","d"], ["c","d","e","f","g","e","d","c"]], "", "|"),
        (23, [["_d","_e","f","_g","_a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","g","f","e"]], "", "|"),
        (24, [["^c","=d","=e","^f","=g","f","e","d"], ["c","d","e","f","g","f","e","d"], ["c","d","e","f","g","f","e","d"], ["c","d","e","f","g","e","d","c"]], "", ":|"),
        (25, [["d","e","^f","g","a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","g","f","e"]], "", "|"),
        (26, [["d","_e","=f","g","_a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","f","e","d"]], "", "|"),
        (27, [["_e","f","g","_a","_b","a","g","f"], ["e","f","g","a","b","a","g","f"], ["e","f","g","a","b","a","g","f"], ["e","f","g","a","b","a","g","f"]], "", "|"),
        (28, [["^d","=e","^f","^g","=a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","f","e","d"]], "", "|"),
        (29, [["e","^f","^g","a","b","a","g","f"], ["e","f","g","a","b","a","g","f"], ["e","f","g","a","b","a","g","f"], ["e","f","g","a","b","a","g","f"]], "", "|"),
        (30, [["e","=f","=g","a","_b","a","g","f"], ["e","f","g","a","b","a","g","f"], ["e","f","g","a","b","a","g","f"], ["e","f","g","a","b","g","f","e"]], "", "| f4 z4 z8 |]")
    ]

    public static func generateEJ1ABC(
        articulation: EJ1Articulation,
        tempoBPM: Int = 80
    ) -> String {
        var lines: [String] = [
            "X:1",
            "T:E. J. 1 — \(articulation.title)",
            "C:Paul Taffanel & Philippe Gaubert (A. L. 16.588)",
            "% EJ1_LEDUC_ART:\(articulation.rawValue)",
            "%%barsperstaff 1",
            "M:4/2",
            "L:1/16",
            "Q:1/4=\(tempoBPM)",
            "K:C",
            "V:1 clef=treble stem=up",
            "%%score 1"
        ]

        var currentStem = "up"
        for m in ej1RawMeasures {
            let targetStem = (m.num <= 10) ? "up" : "down"
            if targetStem != currentStem {
                lines.append("[V:1 stem=\(targetStem)]")
                currentStem = targetStem
            }
            let artBeats = m.beats.map { articulation.apply(to: $0) }.joined(separator: " ")
            let annot = (m.num == 1) ? "\"^Reprise à l'octave\"" : ((m.num == 25) ? "\"^8va\"" : "")
            if !m.prefix.isEmpty {
                lines.append("\(m.prefix) \(annot)\(artBeats) \(m.suffix)")
            } else {
                lines.append("\(annot)\(artBeats) \(m.suffix)")
            }
        }

        return lines.joined(separator: "\n")
    }

    internal static let ej2RawMeasures: [(num: Int, beats: [[String]], prefix: String, suffix: String)] = [
        (1,  [["D","E","F","G","A","G","F","E"], ["D","E","F","G","A","G","F","E"], ["D","E","F","G","A","G","F","E"], ["D","E","F","G","A","G","F","E"]], "|:", "|"),
        (2,  [["D","_E","=F","_G","_A","G","F","E"], ["D","E","F","G","A","G","F","E"], ["D","E","F","G","A","G","F","E"], ["D","E","F","G","A","F","E","D"]], "", "|"),
        (3,  [["_E","F","_G","_A","_B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"]], "", "|"),
        (4,  [["^D","=E","^F","=G","=A","G","F","E"], ["D","E","F","G","A","G","F","E"], ["D","E","F","G","A","G","F","E"], ["D","E","F","G","A","F","E","D"]], "", "|"),
        (5,  [["E","^F","G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"]], "", "|"),
        (6,  [["E","=F","=G","_A","_B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","G","F","E"]], "", "|"),
        (7,  [["F","G","_A","_B","c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","B","A","G"]], "", "|"),
        (8,  [["^E","^F","^G","=A","=B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","A","G","F"], ["E","F","G","A","B","G","F","E"]], "", "|"),
        (9,  [["^F","^G","A","B","^c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","B","A","G"]], "", "|"),
        (10, [["^F","=G","=A","_B","=c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","A","G","F"]], "", "|"),
        (11, [["G","A","_B","c","d","c","B","A"], ["G","A","B","c","d","c","B","A"], ["G","A","B","c","d","c","B","A"], ["G","A","B","c","d","c","B","A"]], "", "|"),
        (12, [["^^F","^G","^A","B","^c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","B","A","G"], ["F","G","A","B","c","A","G","F"]], "", "|"),
        (13, [["^G","^A","B","^c","^d","c","B","A"], ["G","A","B","c","d","c","B","A"], ["G","A","B","c","d","c","B","A"], ["G","A","B","c","d","c","B","A"]], "", "|"),
        (14, [["^G","=A","=B","=c","=d","c","B","A"], ["G","A","B","c","d","c","B","A"], ["G","A","B","c","d","c","B","A"], ["G","A","B","c","d","B","A","G"]], "", "|"),
        (15, [["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","d","c","B"]], "", "|"),
        (16, [["A","_B","=c","_d","_e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","c","B","A"]], "", "|"),
        (17, [["_B","c","_d","_e","f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","e","d","c"]], "", "|"),
        (18, [["^A","=B","^c","=d","=e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","d","c","B"], ["A","B","c","d","e","c","B","A"]], "", "|"),
        (19, [["B","^c","d","e","^f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","e","d","c"]], "", "|"),
        (20, [["B","=c","=d","_e","=f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","d","c","B"]], "", "|"),
        (21, [["c","d","_e","f","g","f","e","d"], ["c","d","e","f","g","f","e","d"], ["c","d","e","f","g","f","e","d"], ["c","d","e","f","g","f","e","d"]], "", "|"),
        (22, [["^B","^c","^d","=e","^f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","e","d","c"], ["B","c","d","e","f","d","c","B"]], "", "|"),
        (23, [["^c","^d","e","^f","^g","f","e","d"], ["c","d","e","f","g","f","e","d"], ["c","d","e","f","g","f","e","d"], ["c","d","e","f","g","f","e","d"]], "", "|"),
        (24, [["^c","=d","=e","=f","=g","f","e","d"], ["c","d","e","f","g","f","e","d"], ["c","d","e","f","g","f","e","d"], ["c","d","e","f","g","e","d","c"]], "", ":|"),
        (25, [["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","g","f","e"]], "", "|"),
        (26, [["d","_e","=f","_g","_a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","f","e","d"]], "", "|"),
        (27, [["_e","f","_g","_a","_b","a","g","f"], ["e","f","g","a","b","a","g","f"], ["e","f","g","a","b","a","g","f"], ["e","f","g","a","b","a","g","f"]], "", "|"),
        (28, [["^d","=e","^f","=g","=a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","g","f","e"], ["d","e","f","g","a","f","e","d"]], "", "|"),
        (29, [["e","^f","g","a","b","a","g","f"], ["e","f","g","a","b","a","g","f"], ["e","f","g","a","b","a","g","f"], ["e","f","g","a","b","a","g","f"]], "", "|"),
        (30, [["e","=f","=g","_a","_b","a","g","f"], ["e","f","g","a","b","a","g","f"], ["e","f","g","a","b","a","g","f"], ["e","f","g","a","b","g","f","e"]], "", "| f4 z4 z8 |]")
    ]

    public static func generateEJ2ABC(
        articulation: EJ1Articulation,
        tempoBPM: Int = 80
    ) -> String {
        var lines: [String] = [
            "X:1",
            "T:E. J. 2 — \(articulation.title)",
            "C:Paul Taffanel & Philippe Gaubert (A. L. 16.588)",
            "% EJ2_LEDUC_ART:\(articulation.rawValue)",
            "%%barsperstaff 1",
            "M:4/2",
            "L:1/16",
            "Q:1/4=\(tempoBPM)",
            "K:C",
            "V:1 clef=treble stem=up",
            "%%score 1"
        ]

        var currentStem = "up"
        for m in ej2RawMeasures {
            let targetStem = (m.num <= 10) ? "up" : "down"
            if targetStem != currentStem {
                lines.append("[V:1 stem=\(targetStem)]")
                currentStem = targetStem
            }
            let artBeats = m.beats.map { articulation.apply(to: $0) }.joined(separator: " ")
            let annot = (m.num == 25) ? "\"^8va\"" : ""
            if !m.prefix.isEmpty {
                lines.append("\(m.prefix) \(annot)\(artBeats) \(m.suffix)")
            } else {
                lines.append("\(annot)\(artBeats) \(m.suffix)")
            }
        }

        return lines.joined(separator: "\n")
    }

    public static func generateABC(
        tonic: Tonic,
        mode: ModeType,
        articulation: ArticulationPattern,
        tempoBPM: Int = 90
    ) -> String {
        let keySig = mode.keySignature(for: tonic)
        let accMap = tonic.accidentalMap(for: mode)
        let baseNotes = tonic.abcNoteSequence

        // Apply accidentals to each degree (0..6)
        var s: [String] = []
        for (idx, note) in baseNotes.enumerated() {
            let degree = idx % 7
            if let acc = accMap[degree] {
                s.append("\(acc)\(note)")
            } else {
                s.append(note)
            }
        }

        func art(_ notes: [String]) -> String {
            return articulation.apply(to: notes)
        }

        // Compas 1
        let c1_asc = Array(s[0..<8])
        let c1_desc = [s[8], s[7], s[6], s[5], s[4], s[3], s[2], s[1]]
        let c1 = "\(art(c1_asc)) \(art(c1_desc))"

        // Compas 2
        let c2_asc = Array(s[2..<10])
        let c2_desc = [s[10], s[9], s[8], s[7], s[6], s[5], s[4], s[3]]
        let c2 = "\(art(c2_asc)) \(art(c2_desc))"

        // Compas 3
        let c3_asc = Array(s[4..<12])
        let c3_desc = [s[12], s[11], s[10], s[9], s[8], s[7], s[6], s[5]]
        let c3 = "\(art(c3_asc)) \(art(c3_desc))"

        // Compas 4 (Peak)
        let c4_asc = Array(s[6..<14])
        let c4_desc = [s[14], s[13], s[12], s[11], s[10], s[9], s[8], s[7]]
        let c4 = "\(art(c4_asc)) \(art(c4_desc))"

        // Compas 5
        let c5_asc = Array(s[6..<14])
        let c5_desc = [s[12], s[11], s[10], s[9], s[8], s[7], s[6], s[5]]
        let c5 = "\(art(c5_asc)) \(art(c5_desc))"

        // Compas 6
        let c6_asc = Array(s[4..<12])
        let c6_desc = [s[10], s[9], s[8], s[7], s[6], s[5], s[4], s[3]]
        let c6 = "\(art(c6_asc)) \(art(c6_desc))"

        // Compas 7
        let c7_asc = Array(s[2..<10])
        let c7_desc = [s[8], s[7], s[6], s[5], s[4], s[3], s[2], s[1]]
        let c7 = "\(art(c7_asc)) \(art(c7_desc))"

        // Compas 8
        let c8_asc = Array(s[0..<8])
        let c8_desc_notes = [s[6], s[5], s[4], s[3], s[2], s[1]]
        let finalTonic = "\(s[0])2"
        let c8_desc_str = "(\(c8_desc_notes.joined()) \(finalTonic))"
        let c8 = "\(art(c8_asc)) \(c8_desc_str)"

        let abc = """
        X:1
        T:Modo \(mode.rawValue): \(tonic.rawValue) \(mode.name)
        % \(mode.family.rawValue) | \(mode.accidentalBadge(for: tonic)) | Fórmula: \(mode.formula)
        %%barsperstaff 2
        M:4/2
        L:1/8
        Q:1/2=\(tempoBPM)
        K:\(keySig)
        V:1 clef=treble
        %%score 1
        \(c1) | \(c2) |
        \(c3) | \(c4) |
        \(c5) | \(c6) |
        \(c7) | \(c8) |]
        """

        return abc
    }
}
