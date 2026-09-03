import Foundation

public struct ExerciseGenerator {

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
