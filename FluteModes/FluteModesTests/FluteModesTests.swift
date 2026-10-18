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

    func testEJ1AndEJ2AllArticulationsGenerateValidAbc() {
        XCTAssertEqual(ExerciseGenerator.ej1RawMeasures.count, 30, "E. J. 1 must have 30 chromatic lines (+ M.31 suffix)")
        XCTAssertEqual(ExerciseGenerator.ej2RawMeasures.count, 30, "E. J. 2 must have 30 chromatic lines (+ M.31 suffix)")

        for art in EJ1Articulation.allCases {
            let ej1Abc = ExerciseGenerator.generateEJ1ABC(articulation: art, tempoBPM: 120)
            XCTAssertTrue(ej1Abc.contains("% EJ1_LEDUC_ART:\(art.rawValue)"), "E. J. 1 ABC must include EJ1_LEDUC_ART header")
            XCTAssertTrue(ej1Abc.contains("Q:1/4=120"), "E. J. 1 ABC must include tempo Q:1/4=120")

            let ej2Abc = ExerciseGenerator.generateEJ2ABC(articulation: art, tempoBPM: 120)
            XCTAssertTrue(ej2Abc.contains("% EJ2_LEDUC_ART:\(art.rawValue)"), "E. J. 2 ABC must include EJ2_LEDUC_ART header")
            XCTAssertTrue(ej2Abc.contains("Q:1/4=120"), "E. J. 2 ABC must include tempo Q:1/4=120")
            XCTAssertTrue(ej2Abc.contains("^^F"), "E. J. 2 ABC must preserve double sharp ^^F in measure 12")
            XCTAssertTrue(ej2Abc.contains("^B"), "E. J. 2 ABC must preserve enharmonic ^B in measure 22")
        }
    }

    func testEJ1AndEJ2PracticeStoreTracking() {
        let store = PracticeStore()
        store.resetAll()

        XCTAssertEqual(store.ej1CompletedCount, 0)
        XCTAssertEqual(store.ej2CompletedCount, 0)
        XCTAssertFalse(store.isEJ1FullyCompleted)
        XCTAssertFalse(store.isEJ2FullyCompleted)

        for art in EJ1Articulation.practiceCases {
            store.markEJ1Completed(art)
            store.markEJ2Completed(art)
        }

        XCTAssertEqual(store.ej1CompletedCount, 10)
        XCTAssertEqual(store.ej2CompletedCount, 10)
        XCTAssertTrue(store.isEJ1FullyCompleted)
        XCTAssertTrue(store.isEJ2FullyCompleted)
    }

    func testEJ4AllSectionsAndArticulationsGenerateValidAbc() {
        XCTAssertEqual(EJ4Section.all.count, 25, "E. J. 4 must have 25 sections (24 keys + Coda)")
        XCTAssertEqual(ExerciseGenerator.ej4SectionMidiNotes.count, 25, "E. J. 4 must have 25 MIDI note arrays")
        // Verify A Minor (section 1) has harmonic minor descent (80 = G#5, 77 = F5) in measure 1 (indices 10, 11) and measure 7 (indices 106, 107)
        let aMinorNotes = ExerciseGenerator.ej4SectionMidiNotes[1]
        XCTAssertEqual(aMinorNotes[10], 80, "A minor m.1 descent must have G#5 (MIDI 80)")
        XCTAssertEqual(aMinorNotes[11], 77, "A minor m.1 descent must have F5 (MIDI 77)")
        XCTAssertEqual(aMinorNotes[106], 80, "A minor m.7 descent must have G#5 (MIDI 80)")
        XCTAssertEqual(aMinorNotes[107], 77, "A minor m.7 descent must have F5 (MIDI 77)")

        for sec in EJ4Section.all {
            for art in EJ4Articulation.allCases {
                let ej4Abc = ExerciseGenerator.generateEJ4ABC(sectionIndex: sec.id, articulation: art, tempoBPM: 120)
                XCTAssertTrue(ej4Abc.contains("% EJ4_LEDUC_ART:\(art.rawValue):SEC:\(sec.id)"), "E. J. 4 ABC must include EJ4_LEDUC_ART:SEC header")
                XCTAssertTrue(ej4Abc.contains("Q:1/4=120"), "E. J. 4 ABC must include tempo Q:1/4=120")
            }
            let midiNotes = ExerciseGenerator.ej4SectionMidiNotes[sec.id]
            let expectedNotes = sec.id < 24 ? 128 : 29
            XCTAssertEqual(midiNotes.count, expectedNotes, "Section \(sec.shortName) should generate \(expectedNotes) MIDI notes")
        }
    }

    func testEJ4PracticeStoreTracking() {
        let store = PracticeStore()
        store.resetAll()

        XCTAssertEqual(store.ej4CompletedCount, 0)
        XCTAssertFalse(store.isEJ4FullyCompleted)

        for art in EJ4Articulation.practiceCases {
            store.markEJ4Completed(art)
        }

        XCTAssertEqual(store.ej4CompletedCount, 8)
        XCTAssertTrue(store.isEJ4FullyCompleted)
    }

    func testReichertR1ToR5AllSectionsAndArticulationsGenerateValidAbc() {
        XCTAssertEqual(ExerciseGenerator.r1SectionMidiNotes.count, 25, "R1 must have 25 MIDI note arrays")
        XCTAssertEqual(ExerciseGenerator.r2SectionMidiNotes.count, 25, "R2 must have 25 MIDI note arrays")
        XCTAssertEqual(ExerciseGenerator.r4SectionMidiNotes.count, 25, "R4 must have 25 MIDI note arrays")
        XCTAssertEqual(ExerciseGenerator.r5SectionMidiNotes.count, 25, "R5 must have 25 MIDI note arrays")

        for sec in EJ4Section.all {
            let r1Notes = ExerciseGenerator.r1SectionMidiNotes[sec.id]
            XCTAssertEqual(r1Notes.count, 43, "R1 section \(sec.id) must have 43 notes")
            for art in EJ5Articulation.allCases {
                let r1Abc = ExerciseGenerator.generateR1ABC(sectionIndex: sec.id, articulation: art, tempoBPM: 92)
                XCTAssertTrue(r1Abc.contains("% R1_SCHOTT_ART:\(art.rawValue):SEC:\(sec.id)"))
            }

            let r2Notes = ExerciseGenerator.r2SectionMidiNotes[sec.id]
            XCTAssertEqual(r2Notes.count, 61, "R2 section \(sec.id) must have 61 notes")
            for art in EJ4Articulation.allCases {
                let r2Abc = ExerciseGenerator.generateR2ABC(sectionIndex: sec.id, articulation: art, tempoBPM: 128)
                XCTAssertTrue(r2Abc.contains("% R2_SCHOTT_ART:\(art.rawValue):SEC:\(sec.id)"))
            }

            let r4Notes = ExerciseGenerator.r4SectionMidiNotes[sec.id]
            XCTAssertEqual(r4Notes.count, 61, "R4 section \(sec.id) must have 61 notes")
            for art in EJ4Articulation.allCases {
                let r4Abc = ExerciseGenerator.generateR4ABC(sectionIndex: sec.id, articulation: art, tempoBPM: 120)
                XCTAssertTrue(r4Abc.contains("% R4_SCHOTT_ART:\(art.rawValue):SEC:\(sec.id)"))
            }

            let r5Notes = ExerciseGenerator.r5SectionMidiNotes[sec.id]
            XCTAssertEqual(r5Notes.count, 91, "R5 section \(sec.id) must have 91 notes")
            for art in EJ5Articulation.allCases {
                let r5Abc = ExerciseGenerator.generateR5ABC(sectionIndex: sec.id, articulation: art, tempoBPM: 80)
                XCTAssertTrue(r5Abc.contains("% R5_SCHOTT_ART:\(art.rawValue):SEC:\(sec.id)"))
            }
        }
    }

    func testReichertR1ToR5PracticeStoreTracking() {
        let store = PracticeStore()
        store.resetAll()

        XCTAssertEqual(store.r1CompletedCount, 0)
        XCTAssertEqual(store.r2CompletedCount, 0)
        XCTAssertEqual(store.r4CompletedCount, 0)
        XCTAssertEqual(store.r5CompletedCount, 0)

        for art in EJ5Articulation.practiceCases {
            store.markEJ5TypeCompleted(art, for: .r1)
            store.markEJ5TypeCompleted(art, for: .r5)
        }
        for art in EJ4Articulation.practiceCases {
            store.markEJ4Completed(art, for: .r2)
            store.markEJ4Completed(art, for: .r4)
        }

        XCTAssertEqual(store.r1CompletedCount, 10)
        XCTAssertEqual(store.r2CompletedCount, 8)
        XCTAssertEqual(store.r4CompletedCount, 8)
        XCTAssertEqual(store.r5CompletedCount, 10)
        XCTAssertTrue(store.isR1FullyCompleted)
        XCTAssertTrue(store.isEJ4TypeFullyCompleted(for: .r2))
        XCTAssertTrue(store.isEJ4TypeFullyCompleted(for: .r4))
        XCTAssertTrue(store.isR5FullyCompleted)
    }

    func testEJ5AllSectionsAndArticulationsGenerateValidAbcAndMidi() {
        XCTAssertEqual(EJ5Section.all.count, 12, "E. J. 5 must have 12 chromatic sections")
        XCTAssertEqual(ExerciseGenerator.ej5SectionMidiNotes.count, 12, "E. J. 5 must have 12 MIDI note arrays")

        for sec in EJ5Section.all {
            let notes = ExerciseGenerator.ej5SectionMidiNotes[sec.id]
            XCTAssertEqual(notes.count, 49, "E. J. 5 section \(sec.shortName) must have 49 notes")

            // Flute pitch range safety
            for midi in notes {
                XCTAssertGreaterThanOrEqual(midi, 59, "MIDI \(midi) in E.J. 5 \(sec.shortName) must be >= 59 (B3)")
                XCTAssertLessThanOrEqual(midi, 98, "MIDI \(midi) in E.J. 5 \(sec.shortName) must be <= 98 (D7)")
            }

            // Root pitch check: section starts on root, reaches apex at index 24, returns to root
            XCTAssertEqual(notes.first, 60 + sec.id, "E. J. 5 section \(sec.shortName) must start on root")
            XCTAssertEqual(notes[24], 84 + sec.id, "E. J. 5 section \(sec.shortName) apex note at index 24")
            XCTAssertEqual(notes.last, 60 + sec.id, "E. J. 5 section \(sec.shortName) must return to root")

            for art in EJ5Articulation.allCases {
                let ej5Abc = ExerciseGenerator.generateEJ5ABC(sectionIndex: sec.id, articulation: art, tempoBPM: 96)
                XCTAssertTrue(ej5Abc.contains("% EJ5_LEDUC_ART:\(art.rawValue):SEC:\(sec.id)"), "ABC must contain EJ5_LEDUC_ART header")
                XCTAssertTrue(ej5Abc.contains("M:6/8"), "E. J. 5 must have 6/8 meter")
                XCTAssertTrue(ej5Abc.contains("L:1/16"), "E. J. 5 must have 1/16 unit note length")
                XCTAssertTrue(ej5Abc.contains("Q:1/4=96"), "E. J. 5 must have tempo Q:1/4=96")
                XCTAssertTrue(ej5Abc.contains("K:C"), "E. J. 5 must have key K:C")
            }
        }
    }

    func testEJ5PracticeStoreTracking() {
        let store = PracticeStore()
        store.resetAll()

        XCTAssertEqual(store.ej5CompletedCount, 0)
        XCTAssertEqual(store.ej5TypeCompletedCount(for: .ej5), 0)
        XCTAssertFalse(store.isEJ5FullyCompleted)
        XCTAssertFalse(store.isEJ5TypeFullyCompleted(for: .ej5))

        for art in EJ5Articulation.practiceCases {
            XCTAssertFalse(store.isEJ5TypeCompleted(art, for: .ej5))
            store.markEJ5TypeCompleted(art, for: .ej5)
            XCTAssertTrue(store.isEJ5TypeCompleted(art, for: .ej5))
        }

        XCTAssertEqual(store.ej5CompletedCount, 10)
        XCTAssertEqual(store.ej5TypeCompletedCount(for: .ej5), 10)
        XCTAssertTrue(store.isEJ5FullyCompleted)
        XCTAssertTrue(store.isEJ5TypeFullyCompleted(for: .ej5))

        // Toggle test
        store.toggleEJ5TypeCompleted(.allSlurred, for: .ej5)
        XCTAssertFalse(store.isEJ5TypeCompleted(.allSlurred, for: .ej5))
        XCTAssertEqual(store.ej5CompletedCount, 9)
        XCTAssertFalse(store.isEJ5FullyCompleted)

        store.toggleEJ5TypeCompleted(.allSlurred, for: .ej5)
        XCTAssertTrue(store.isEJ5TypeCompleted(.allSlurred, for: .ej5))
        XCTAssertEqual(store.ej5CompletedCount, 10)
        XCTAssertTrue(store.isEJ5FullyCompleted)
    }

    func testEJ10AllSectionsAndArticulationsGenerateValidAbcAndMidi() {
        XCTAssertEqual(EJ10Section.all.count, 12, "E. J. 10 must have 12 series sections")
        XCTAssertEqual(ExerciseGenerator.ej10SectionMidiNotes.count, 12, "E. J. 10 must have 12 MIDI note arrays")

        for sec in EJ10Section.all {
            let notes = ExerciseGenerator.ej10SectionMidiNotes[sec.id]
            let expectedNotes = (sec.id < 11) ? 120 : 121
            XCTAssertEqual(notes.count, expectedNotes, "E. J. 10 section \(sec.shortName) must have \(expectedNotes) notes")

            // Flute pitch range safety
            for midi in notes {
                XCTAssertGreaterThanOrEqual(midi, 59, "MIDI \(midi) in E.J. 10 \(sec.shortName) must be >= 59 (B3)")
                XCTAssertLessThanOrEqual(midi, 98, "MIDI \(midi) in E.J. 10 \(sec.shortName) must be <= 98 (D7)")
            }

            for art in EJ5Articulation.allCases {
                let ej10Abc = ExerciseGenerator.generateEJ10ABC(sectionIndex: sec.id, articulation: art, tempoBPM: 96)
                XCTAssertTrue(ej10Abc.contains("% EJ10_LEDUC_ART:\(art.rawValue):SEC:\(sec.id)"), "ABC must contain EJ10_LEDUC_ART header")
                XCTAssertTrue(ej10Abc.contains("M:6/8"), "E. J. 10 must have 6/8 meter")
                XCTAssertTrue(ej10Abc.contains("L:1/16"), "E. J. 10 must have 1/16 unit note length")
                XCTAssertTrue(ej10Abc.contains("Q:1/4=96"), "E. J. 10 must have tempo Q:1/4=96")
                XCTAssertTrue(ej10Abc.contains("K:C"), "E. J. 10 must have key K:C")
            }
        }
    }

    func testEJ10PracticeStoreTracking() {
        let store = PracticeStore()
        store.resetAll()

        XCTAssertEqual(store.ej10CompletedCount, 0)
        XCTAssertEqual(store.ej5TypeCompletedCount(for: .ej10), 0)
        XCTAssertFalse(store.isEJ10FullyCompleted)
        XCTAssertFalse(store.isEJ5TypeFullyCompleted(for: .ej10))

        for art in EJ5Articulation.practiceCases {
            XCTAssertFalse(store.isEJ5TypeCompleted(art, for: .ej10))
            store.markEJ5TypeCompleted(art, for: .ej10)
            XCTAssertTrue(store.isEJ5TypeCompleted(art, for: .ej10))
        }

        XCTAssertEqual(store.ej10CompletedCount, 10)
        XCTAssertEqual(store.ej5TypeCompletedCount(for: .ej10), 10)
        XCTAssertTrue(store.isEJ10FullyCompleted)
        XCTAssertTrue(store.isEJ5TypeFullyCompleted(for: .ej10))

        // Toggle test
        store.toggleEJ5TypeCompleted(.allStaccato, for: .ej10)
        XCTAssertFalse(store.isEJ5TypeCompleted(.allStaccato, for: .ej10))
        XCTAssertEqual(store.ej10CompletedCount, 9)
        XCTAssertFalse(store.isEJ10FullyCompleted)

        store.toggleEJ5TypeCompleted(.allStaccato, for: .ej10)
        XCTAssertTrue(store.isEJ5TypeCompleted(.allStaccato, for: .ej10))
        XCTAssertEqual(store.ej10CompletedCount, 10)
        XCTAssertTrue(store.isEJ10FullyCompleted)
    }

    func testEJ11AllSectionsAndArticulationsGenerateValidAbcAndMidi() {
        XCTAssertEqual(EJ10Section.all.count, 12, "E. J. 11 must have 12 series sections")
        XCTAssertEqual(ExerciseGenerator.ej11SectionMidiNotes.count, 12, "E. J. 11 must have 12 MIDI note arrays")

        for sec in EJ10Section.all {
            let notes = ExerciseGenerator.ej11SectionMidiNotes[sec.id]
            let expectedNotes = (sec.id < 11) ? 180 : 181
            XCTAssertEqual(notes.count, expectedNotes, "E. J. 11 section \(sec.shortName) must have \(expectedNotes) notes")

            // Flute pitch range safety
            for midi in notes {
                XCTAssertGreaterThanOrEqual(midi, 59, "MIDI \(midi) in E.J. 11 \(sec.shortName) must be >= 59 (B3)")
                XCTAssertLessThanOrEqual(midi, 98, "MIDI \(midi) in E.J. 11 \(sec.shortName) must be <= 98 (D7)")
            }

            for art in EJ5Articulation.allCases {
                let ej11Abc = ExerciseGenerator.generateEJ11ABC(sectionIndex: sec.id, articulation: art, tempoBPM: 96)
                XCTAssertTrue(ej11Abc.contains("% EJ11_LEDUC_ART:\(art.rawValue):SEC:\(sec.id)"), "ABC must contain EJ11_LEDUC_ART header")
                XCTAssertTrue(ej11Abc.contains("M:9/8"), "E. J. 11 must have 9/8 meter")
                XCTAssertTrue(ej11Abc.contains("L:1/16"), "E. J. 11 must have 1/16 unit note length")
                XCTAssertTrue(ej11Abc.contains("Q:1/4=96"), "E. J. 11 must have tempo Q:1/4=96")
                XCTAssertTrue(ej11Abc.contains("K:C"), "E. J. 11 must have key K:C")
            }
        }
    }

    func testEJ11PracticeStoreTracking() {
        let store = PracticeStore()
        store.resetAll()

        XCTAssertEqual(store.ej11CompletedCount, 0)
        XCTAssertEqual(store.ej5TypeCompletedCount(for: .ej11), 0)
        XCTAssertFalse(store.isEJ11FullyCompleted)
        XCTAssertFalse(store.isEJ5TypeFullyCompleted(for: .ej11))

        for art in EJ5Articulation.practiceCases {
            XCTAssertFalse(store.isEJ5TypeCompleted(art, for: .ej11))
            store.markEJ5TypeCompleted(art, for: .ej11)
            XCTAssertTrue(store.isEJ5TypeCompleted(art, for: .ej11))
        }

        XCTAssertEqual(store.ej11CompletedCount, 10)
        XCTAssertEqual(store.ej5TypeCompletedCount(for: .ej11), 10)
        XCTAssertTrue(store.isEJ11FullyCompleted)
        XCTAssertTrue(store.isEJ5TypeFullyCompleted(for: .ej11))

        // Toggle test
        store.toggleEJ5TypeCompleted(.pairsSlurred, for: .ej11)
        XCTAssertFalse(store.isEJ5TypeCompleted(.pairsSlurred, for: .ej11))
        XCTAssertEqual(store.ej11CompletedCount, 9)
        XCTAssertFalse(store.isEJ11FullyCompleted)

        store.toggleEJ5TypeCompleted(.pairsSlurred, for: .ej11)
        XCTAssertTrue(store.isEJ5TypeCompleted(.pairsSlurred, for: .ej11))
        XCTAssertEqual(store.ej11CompletedCount, 10)
        XCTAssertTrue(store.isEJ11FullyCompleted)
    }

    func testAll11ModulesPitchRangeAndSafety() {
        // 1. Modos (tested across all 84 in testFlutePitchRangeSafety)
        // 2 & 3. E.J. 1 & 2 (MIDI range confirmed in measures)
        // 4. E.J. 4 (25 sections)
        for sec in EJ4Section.all {
            for midi in ExerciseGenerator.ej4SectionMidiNotes[sec.id] {
                XCTAssertTrue((59...98).contains(midi), "EJ4 sec \(sec.id) pitch \(midi) out of flute bounds")
            }
        }
        // 5. E.J. 5 (12 sections)
        for sec in EJ5Section.all {
            for midi in ExerciseGenerator.ej5SectionMidiNotes[sec.id] {
                XCTAssertTrue((59...98).contains(midi), "EJ5 sec \(sec.id) pitch \(midi) out of flute bounds")
            }
        }
        // 6. E.J. 10 (12 sections)
        for sec in EJ10Section.all {
            for midi in ExerciseGenerator.ej10SectionMidiNotes[sec.id] {
                XCTAssertTrue((59...98).contains(midi), "EJ10 sec \(sec.id) pitch \(midi) out of flute bounds")
            }
        }
        // 7. E.J. 11 (12 sections)
        for sec in EJ10Section.all {
            for midi in ExerciseGenerator.ej11SectionMidiNotes[sec.id] {
                XCTAssertTrue((59...98).contains(midi), "EJ11 sec \(sec.id) pitch \(midi) out of flute bounds")
            }
        }
        // 8. R. 1 (25 sections)
        for sec in EJ4Section.all {
            for midi in ExerciseGenerator.r1SectionMidiNotes[sec.id] {
                XCTAssertTrue((59...98).contains(midi), "R1 sec \(sec.id) pitch \(midi) out of flute bounds")
            }
        }
        // 9. R. 2 (25 sections)
        for sec in EJ4Section.all {
            for midi in ExerciseGenerator.r2SectionMidiNotes[sec.id] {
                XCTAssertTrue((59...98).contains(midi), "R2 sec \(sec.id) pitch \(midi) out of flute bounds")
            }
        }
        // 10. R. 4 (25 sections)
        for sec in EJ4Section.all {
            for midi in ExerciseGenerator.r4SectionMidiNotes[sec.id] {
                XCTAssertTrue((59...98).contains(midi), "R4 sec \(sec.id) pitch \(midi) out of flute bounds")
            }
        }
        // 11. R. 5 (25 sections)
        for sec in EJ4Section.all {
            for midi in ExerciseGenerator.r5SectionMidiNotes[sec.id] {
                XCTAssertTrue((59...98).contains(midi), "R5 sec \(sec.id) pitch \(midi) out of flute bounds")
            }
        }
    }

    func testAll840ModalSchemesGenerateValidAbcAndMidi() {
        XCTAssertEqual(ModalScheme.allCases.count, 10, "There must be 10 technical schemes in Modos Paralelos")
        let expectedNoteCounts: [ModalScheme: Int] = [
            .ej1: 257,
            .ej2: 257,
            .ej4: 127,
            .ej5: 49,
            .ej10: 97,
            .ej11: 145,
            .r1: 43,
            .r2: 61,
            .r4: 61,
            .r5: 91
        ]

        var totalCombinations = 0
        for tonic in Tonic.allCases {
            for mode in ModeType.allCases {
                for scheme in ModalScheme.allCases {
                    totalCombinations += 1
                    let midiNotes = ExerciseGenerator.generateModalSchemeMidiNotes(tonic: tonic, mode: mode, scheme: scheme)
                    XCTAssertEqual(
                        midiNotes.count,
                        expectedNoteCounts[scheme],
                        "Scheme \(scheme.rawValue) for \(tonic.rawValue) \(mode.name) must have \(expectedNoteCounts[scheme]!) MIDI notes"
                    )
                    for midi in midiNotes {
                        XCTAssertTrue((58...98).contains(midi), "MIDI \(midi) out of flute range in \(tonic.rawValue) \(mode.name) \(scheme.rawValue)")
                    }

                    let abc = ExerciseGenerator.generateABC(
                        tonic: tonic,
                        mode: mode,
                        articulation: .allSlurred,
                        tempoBPM: 92,
                        scheme: scheme
                    )
                    let expectedTitle = "T:Modo \(mode.rawValue): \(tonic.rawValue) \(mode.shortName) (\(scheme.pillLabel))"
                    XCTAssertTrue(abc.contains(expectedTitle), "ABC must contain concise title '\(expectedTitle)'")
                    XCTAssertLessThanOrEqual(expectedTitle.dropFirst(2).count, 32, "Visible ABC title '\(expectedTitle.dropFirst(2))' must be <= 32 chars to prevent mobile SVG clipping")
                    XCTAssertFalse(expectedTitle.contains("(Mayor)") || expectedTitle.contains("(Menor"), "ABC T: title must use shortName without parentheticals")
                    XCTAssertTrue(abc.contains("M:\(scheme.meter)"), "ABC for \(scheme.rawValue) must contain M:\(scheme.meter)")
                    XCTAssertTrue(abc.contains("L:\(scheme.unitLen)"), "ABC for \(scheme.rawValue) must contain L:\(scheme.unitLen)")
                    XCTAssertTrue(abc.contains("K:\(mode.keySignature(for: tonic))"), "ABC must contain parallel key signature K:\(mode.keySignature(for: tonic))")

                    if tonic == .miBemol && mode == .locrian {
                        XCTAssertTrue(abc.contains("__B") || abc.contains("__b"), "Eb Locrian in \(scheme.rawValue) must contain double flat Bbb (__B)")
                    }
                    if tonic == .laBemol && (mode == .phrygian || mode == .locrian) {
                        XCTAssertTrue(abc.contains("__B") || abc.contains("__b") || abc.contains("__E") || abc.contains("__e"), "Ab \(mode.name) in \(scheme.rawValue) must contain double flat (__B or __E)")
                    }
                }
            }
        }
        XCTAssertEqual(totalCombinations, 840, "Must test all 840 modal combinations (12 tonics x 7 modes x 10 schemes)")
    }

    func testConservatoryCoachPracticeWizardRoutines() {
        for duration in PracticeWizardDuration.allCases {
            for focus in PracticeWizardFocus.allCases {
                let blocks = PracticeRoutineBlock.generateRoutine(
                    duration: duration,
                    focus: focus,
                    tonic: .doNatural,
                    mode: .dorian
                )
                XCTAssertEqual(blocks.count, 3, "Conservatory Coach routine must have 3 structured blocks")
                let sumMinutes = blocks.reduce(0) { $0 + $1.minutes }
                XCTAssertEqual(sumMinutes, duration.rawValue, "Sum of block minutes (\(sumMinutes)) must equal preset duration (\(duration.rawValue))")
            }
        }

        // Verify barsPerStaff matches the 2-bars-per-line ABC layout for ej10 and ej11
        XCTAssertEqual(ModalScheme.ej1.barsPerStaff, 1)
        XCTAssertEqual(ModalScheme.ej2.barsPerStaff, 1)
        XCTAssertEqual(ModalScheme.ej4.barsPerStaff, 2)
        XCTAssertEqual(ModalScheme.ej5.barsPerStaff, 2)
        XCTAssertEqual(ModalScheme.ej10.barsPerStaff, 2)
        XCTAssertEqual(ModalScheme.ej11.barsPerStaff, 2)
        XCTAssertEqual(ModalScheme.r1.barsPerStaff, 2)
        XCTAssertEqual(ModalScheme.r4.barsPerStaff, 2)
        XCTAssertEqual(ModalScheme.r2.barsPerStaff, 4)
        XCTAssertEqual(ModalScheme.r5.barsPerStaff, 4)

        // Verify LocalizationManager Coach/Wizard keys resolve properly (not returning raw key) and omit internal "OPCIÓN 1"
        let loc = LocalizationManager.shared
        XCTAssertNotEqual(CoachStrings.coachTitle(loc), "coach_title")
        XCTAssertNotEqual(CoachStrings.openWizardBtn(loc), "coach_open_wizard")
        XCTAssertNotEqual(CoachStrings.level3SchemeLabel(loc), "coach_level3_scheme")
        XCTAssertFalse(CoachStrings.coachBadge(loc).contains("OPCIÓN 1"))
        XCTAssertFalse(CoachStrings.coachBadge(loc).contains("OPTION 1"))
        XCTAssertTrue(
            CoachStrings.coachBadge(loc) == "CONSERVATORY COACH · ASISTENTE GUIADO" ||
            CoachStrings.coachBadge(loc) == "CONSERVATORY COACH · GUIDED ASSISTANT"
        )
    }
}





