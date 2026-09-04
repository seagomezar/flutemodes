import XCTest
@testable import FluteModes

final class FluteModesTests: XCTestCase {

    func testAll84ModalExercisesGenerateValidAbc() {
        var count = 0
        for tonic in Tonic.allCases {
            for mode in ModeType.allCases {
                for art in ArticulationPattern.allCases {
                    let abc = ExerciseGenerator.generateABC(
                        tonic: tonic,
                        mode: mode,
                        articulation: art,
                        tempoBPM: 90
                    )

                    XCTAssertFalse(abc.isEmpty)
                    XCTAssertTrue(abc.hasPrefix("X:1"), "ABC should start with X:1 header")
                    XCTAssertTrue(abc.contains("M:4/2"), "ABC should have time signature 4/2")
                    XCTAssertTrue(abc.contains("L:1/8"), "ABC should have unit length 1/8")
                    XCTAssertTrue(abc.contains("Q:1/2=90"), "ABC should have tempo definition")
                    XCTAssertTrue(abc.contains("V:1 clef=treble"), "ABC should define treble clef")
                    XCTAssertTrue(abc.trimmingCharacters(in: .whitespacesAndNewlines).hasSuffix("|]"), "ABC should finish with terminal bar |]")

                    let scoreBody = abc.components(separatedBy: "%%score 1\n").last ?? ""
                    let measures = scoreBody.components(separatedBy: "|").map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }.filter { !$0.isEmpty && $0 != "]" }
                    XCTAssertEqual(measures.count, 8, "Exercise must consist of 8 measures for \(tonic.rawValue) \(mode.rawValue) with \(art.title)")

                    count += 1
                }
            }
        }
        XCTAssertEqual(count, 672, "Should have tested all 12 tonics * 7 modes * 8 articulations = 672 combinations")
    }

    func testFlutePitchRangeSafety() {
        for tonic in Tonic.allCases {
            // Flute lowest note is B3 (59) or C4 (60)
            XCTAssertGreaterThanOrEqual(tonic.rootMidi, 59, "Root MIDI of \(tonic.rawValue) must be >= 59 (B3)")
            XCTAssertLessThanOrEqual(tonic.rootMidi, 71, "Root MIDI of \(tonic.rawValue) must be <= 71 (B4)")

            XCTAssertEqual(tonic.abcNoteSequence.count, 16, "Tonic \(tonic.rawValue) must have 16 base notes in sequence")

            for mode in ModeType.allCases {
                let intervals = mode.intervals
                XCTAssertEqual(intervals.count, 7, "Mode \(mode.rawValue) must define 7 diatonic intervals")

                // Apex note at index 14
                let apexDegree = 14 % 7
                let apexOctave = 14 / 7
                let apexSemitones = intervals[apexDegree] + (apexOctave * 12)
                let apexMidi = tonic.rootMidi + apexSemitones

                XCTAssertLessThanOrEqual(apexMidi, 98, "Peak note of \(tonic.rawValue) \(mode.rawValue) (MIDI \(apexMidi)) must not exceed 98 (D7)")
            }
        }
    }

    func testAll8ArticulationPatternsParenthesesBalanced() {
        let dummyNotes = ["C", "D", "E", "F", "G", "A", "B", "c"]
        for art in ArticulationPattern.allCases {
            let formatted = art.apply(to: dummyNotes)
            let openCount = formatted.filter { $0 == "(" }.count
            let closeCount = formatted.filter { $0 == ")" }.count
            XCTAssertEqual(openCount, closeCount, "Parentheses must balance for articulation \(art.title)")
        }
    }

    func testAccidentalMapDegreesWithinBounds() {
        for tonic in Tonic.allCases {
            for mode in ModeType.allCases {
                let accMap = tonic.accidentalMap(for: mode)
                for degree in accMap.keys {
                    XCTAssertTrue((0...6).contains(degree), "Accidental degree \(degree) must be in range 0..6")
                    let acc = accMap[degree] ?? ""
                    XCTAssertTrue(["^", "^^", "=", "_"].contains(acc), "Accidental must be valid ABC symbol (^, ^^, =, _)")
                }
            }
        }
    }

    func testAudioSynthesisFrequencies() {
        // A4 = 440.0 Hz
        let a4 = ScoreAudioPlayer.midiToFrequency(69.0)
        XCTAssertEqual(a4, 440.0, accuracy: 0.001)

        // A3 = 220.0 Hz
        let a3 = ScoreAudioPlayer.midiToFrequency(57.0)
        XCTAssertEqual(a3, 220.0, accuracy: 0.001)

        // Middle C (C4) = ~261.625 Hz
        let c4 = ScoreAudioPlayer.midiToFrequency(60.0)
        XCTAssertEqual(c4, 261.625, accuracy: 0.05)

        // Low B3 = ~246.94 Hz
        let b3 = ScoreAudioPlayer.midiToFrequency(59.0)
        XCTAssertEqual(b3, 246.94, accuracy: 0.05)

        // High C7 = ~2093.00 Hz
        let c7 = ScoreAudioPlayer.midiToFrequency(96.0)
        XCTAssertEqual(c7, 2093.0, accuracy: 0.1)
    }

    func testLocalizationKeyParity() {
        let loc = LocalizationManager.shared
        // Test switching languages
        loc.currentLanguage = .spanish
        let esTitle = loc.t("settings_title")
        XCTAssertEqual(esTitle, "Ajustes de Estudio")

        loc.currentLanguage = .english
        let enTitle = loc.t("settings_title")
        XCTAssertEqual(enTitle, "Practice Settings")

        // Reset to default
        loc.currentLanguage = .spanish
    }

    func testKeepScreenAwakeSettingPersistence() {
        let vm = PracticeViewModel()
        let initial = vm.keepScreenAwake
        XCTAssertTrue(initial, "keepScreenAwake should default to true")

        vm.keepScreenAwake = false
        XCTAssertFalse(vm.keepScreenAwake)
        XCTAssertEqual(UserDefaults.standard.bool(forKey: "FluteModes_keepScreenAwake"), false)

        vm.keepScreenAwake = true
        XCTAssertTrue(vm.keepScreenAwake)
        XCTAssertEqual(UserDefaults.standard.bool(forKey: "FluteModes_keepScreenAwake"), true)
    }

    func testPracticeStoreCompletionAndToggle() {
        let store = PracticeStore()
        store.resetAll()

        XCTAssertFalse(store.isCompleted(tonic: .doNatural, mode: .ionian, articulation: .allSlurred))
        XCTAssertEqual(store.completedArticulationsCount(tonic: .doNatural, mode: .ionian), 0)

        // Toggle on
        store.toggleCompleted(tonic: .doNatural, mode: .ionian, articulation: .allSlurred)
        XCTAssertTrue(store.isCompleted(tonic: .doNatural, mode: .ionian, articulation: .allSlurred))
        XCTAssertEqual(store.completedArticulationsCount(tonic: .doNatural, mode: .ionian), 1)

        // Toggle off
        store.toggleCompleted(tonic: .doNatural, mode: .ionian, articulation: .allSlurred)
        XCTAssertFalse(store.isCompleted(tonic: .doNatural, mode: .ionian, articulation: .allSlurred))
        XCTAssertEqual(store.completedArticulationsCount(tonic: .doNatural, mode: .ionian), 0)

        // Complete all 8
        for art in ArticulationPattern.allCases {
            store.markCompleted(tonic: .doNatural, mode: .ionian, articulation: art)
        }
        XCTAssertTrue(store.isModeFullyCompleted(tonic: .doNatural, mode: .ionian))
        XCTAssertEqual(store.completedArticulationsCount(tonic: .doNatural, mode: .ionian), 8)
    }

    func testViewModelAdvanceToNextArticulationMarksCompleted() {
        let store = PracticeStore()
        store.resetAll()
        let vm = PracticeViewModel(store: store)
        vm.currentTonic = .doNatural
        vm.currentMode = .ionian
        vm.currentArticulation = .allSlurred

        XCTAssertFalse(store.isCompleted(tonic: .doNatural, mode: .ionian, articulation: .allSlurred))
        vm.advanceToNextArticulation()

        // Should have marked previous (.allSlurred) as completed and advanced to .slurredFourAndFour
        XCTAssertTrue(store.isCompleted(tonic: .doNatural, mode: .ionian, articulation: .allSlurred))
        XCTAssertEqual(vm.currentArticulation, .slurredFourAndFour)
    }
}
