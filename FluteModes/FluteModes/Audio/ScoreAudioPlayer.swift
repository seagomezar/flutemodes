import Foundation
import AVFoundation

public class ScoreAudioPlayer: ObservableObject {
    @Published public var isPlaying: Bool = false

    private var audioEngine: AVAudioEngine?
    private var playerNode: AVAudioPlayerNode?

    public init() {
        setupAudio()
    }

    private func setupAudio() {
        let engine = AVAudioEngine()
        let player = AVAudioPlayerNode()
        engine.attach(player)

        let format = AVAudioFormat(standardFormatWithSampleRate: 44100, channels: 1)!
        engine.connect(player, to: engine.mainMixerNode, format: format)

        self.audioEngine = engine
        self.playerNode = player

        do {
            try engine.start()
        } catch {
            print("ScoreAudioPlayer audioEngine start failed: \(error)")
        }
    }

    public func toggle(tonic: Tonic, mode: ModeType, articulation: ArticulationPattern, tempoBPM: Int) {
        if isPlaying {
            stop()
        } else {
            play(tonic: tonic, mode: mode, articulation: articulation, tempoBPM: tempoBPM)
        }
    }

    public func stop() {
        playerNode?.stop()
        isPlaying = false
    }

    public func play(tonic: Tonic, mode: ModeType, articulation: ArticulationPattern, tempoBPM: Int) {
        stop()

        guard let engine = audioEngine, let player = playerNode else { return }
        if !engine.isRunning {
            try? engine.start()
        }

        let format = AVAudioFormat(standardFormatWithSampleRate: 44100, channels: 1)!
        guard let buffer = generateScoreBuffer(
            tonic: tonic,
            mode: mode,
            articulation: articulation,
            tempoBPM: tempoBPM,
            format: format
        ) else { return }

        isPlaying = true
        player.scheduleBuffer(buffer, at: nil, options: []) { [weak self] in
            DispatchQueue.main.async {
                self?.isPlaying = false
            }
        }
        player.play()
    }

    // MARK: - Acoustic Grand Piano Synthesis Buffer Generation
    private func generateScoreBuffer(
        tonic: Tonic,
        mode: ModeType,
        articulation: ArticulationPattern,
        tempoBPM: Int,
        format: AVAudioFormat
    ) -> AVAudioPCMBuffer? {
        let sampleRate = format.sampleRate

        // Root MIDI note
        let rootMidi: Int
        switch tonic {
        case .si: rootMidi = 59 // B3
        case .doNatural: rootMidi = 60
        case .doSostenido: rootMidi = 61
        case .re: rootMidi = 62
        case .miBemol: rootMidi = 63
        case .mi: rootMidi = 64
        case .fa: rootMidi = 65
        case .faSostenido: rootMidi = 66
        case .sol: rootMidi = 67
        case .laBemol: rootMidi = 68
        case .la: rootMidi = 69
        case .siBemol: rootMidi = 70
        }

        // Mode intervals from root (semitones)
        let intervals: [Int]
        switch mode {
        case .ionian:     intervals = [0, 2, 4, 5, 7, 9, 11]
        case .lydian:     intervals = [0, 2, 4, 6, 7, 9, 11]
        case .mixolydian: intervals = [0, 2, 4, 5, 7, 9, 10]
        case .dorian:     intervals = [0, 2, 3, 5, 7, 9, 10]
        case .aeolian:    intervals = [0, 2, 3, 5, 7, 8, 10]
        case .phrygian:   intervals = [0, 1, 3, 5, 7, 8, 10]
        case .locrian:    intervals = [0, 1, 3, 5, 6, 8, 10]
        }

        func freqForIndex(_ idx: Int) -> Double {
            let octave = idx / 7
            let degree = idx % 7
            let semitones = intervals[degree] + (octave * 12)
            let midi = Double(rootMidi + semitones)
            return 440.0 * pow(2.0, (midi - 69.0) / 12.0)
        }

        // Eighth note (corchea) duration in seconds
        let eighthDuration = (60.0 / Double(tempoBPM)) / 4.0
        let halfDuration = eighthDuration * 4.0

        struct NoteDef {
            let freq: Double
            let duration: Double
            let isStaccato: Bool
        }

        func isStaccatoAt(beatSubIndex: Int) -> Bool {
            let i = beatSubIndex % 4
            switch articulation {
            case .allSlurred, .slurredFourAndFour: return false
            case .slurTwoStaccatoTwo: return (i >= 2)
            case .staccatoSlurTwoStaccato: return (i == 0 || i == 3)
            case .staccatoTwoSlurTwo: return (i < 2)
            case .staccatoOneSlurThree: return (i == 0)
            case .slurThreeStaccatoOne: return (i == 3)
            case .allStaccato: return true
            }
        }

        var notes: [NoteDef] = []

        func addNotes(_ indices: [Int]) {
            for (subIdx, idx) in indices.enumerated() {
                notes.append(NoteDef(
                    freq: freqForIndex(idx),
                    duration: eighthDuration,
                    isStaccato: isStaccatoAt(beatSubIndex: subIdx)
                ))
            }
        }

        // Measure 1
        addNotes([0, 1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2, 1])
        // Measure 2
        addNotes([2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3])
        // Measure 3
        addNotes([4, 5, 6, 7, 8, 9, 10, 11, 12, 11, 10, 9, 8, 7, 6, 5])
        // Measure 4 (Peak)
        addNotes([6, 7, 8, 9, 10, 11, 12, 13, 14, 13, 12, 11, 10, 9, 8, 7])
        // Measure 5
        addNotes([6, 7, 8, 9, 10, 11, 12, 13, 12, 11, 10, 9, 8, 7, 6, 5])
        // Measure 6
        addNotes([4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3])
        // Measure 7
        addNotes([2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1])
        // Measure 8
        addNotes([0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1])
        // Final tonic half note
        notes.append(NoteDef(freq: freqForIndex(0), duration: halfDuration, isStaccato: false))

        let totalDuration = notes.reduce(0.0) { $0 + $1.duration }
        let totalFrames = AVAudioFrameCount(sampleRate * totalDuration)

        guard let buffer = AVAudioPCMBuffer(pcmFormat: format, frameCapacity: totalFrames) else { return nil }
        buffer.frameLength = totalFrames

        let channelData = buffer.floatChannelData![0]
        var currentFrame = 0

        // Acoustic Piano Harmonics (overtone multiplier, relative amplitude, decay scale)
        let pianoHarmonics: [(Double, Double, Double)] = [
            (1.0, 1.00, 1.00),
            (2.0, 0.55, 0.72),
            (3.0, 0.35, 0.52),
            (4.0, 0.20, 0.38),
            (5.0, 0.12, 0.28),
            (6.0, 0.06, 0.18)
        ]

        // Piano unison detuning for acoustic warmth (chorus effect)
        let unisons: [Double] = [-0.35, 0.0, 0.35]

        for note in notes {
            let noteFrames = Int(note.duration * sampleRate)
            let soundGate = note.isStaccato ? 0.45 : 0.96
            let soundFrames = Int(Double(noteFrames) * soundGate)

            // Fast hammer strike attack (~3ms)
            let attackFrames = max(1, Int(0.003 * sampleRate))
            let damperReleaseFrames = Int(0.020 * sampleRate)

            // Frequency-dependent acoustic piano decay
            let decayBase = max(0.40, 0.85 - (note.freq / 2000.0) * 0.35)

            for i in 0..<noteFrames {
                let frameIndex = currentFrame + i
                if frameIndex >= Int(totalFrames) { break }

                if i < soundFrames {
                    let t = Double(i) / sampleRate

                    // Hammer attack
                    let attackEnv = (i < attackFrames) ? Double(i) / Double(attackFrames) : 1.0

                    // Damper release
                    let releaseEnv: Double
                    if i > soundFrames - damperReleaseFrames {
                        releaseEnv = Double(soundFrames - i) / Double(damperReleaseFrames)
                    } else {
                        releaseEnv = 1.0
                    }

                    // Multi-harmonic synthesis with unisons
                    var noteSample = 0.0
                    for (fMult, amp, dScale) in pianoHarmonics {
                        let hDecay = exp(-t / (decayBase * dScale))
                        let hFreq = note.freq * fMult
                        for u in unisons {
                            noteSample += amp * (1.0 / 3.0) * sin(2.0 * .pi * (hFreq + u) * t) * hDecay
                        }
                    }

                    // Subtle hammer strike transient in the initial 8ms
                    if t < 0.008 {
                        let hammerNoise = sin(2.0 * .pi * 820.0 * t) * exp(-t / 0.002)
                        noteSample += hammerNoise * 0.10
                    }

                    let sample = noteSample * attackEnv * releaseEnv * 0.26
                    channelData[frameIndex] = Float(sample)
                } else {
                    channelData[frameIndex] = 0.0
                }
            }
            currentFrame += noteFrames
        }

        return buffer
    }

    deinit {
        stop()
        audioEngine?.stop()
    }
}
