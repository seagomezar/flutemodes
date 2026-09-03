import Foundation
import AVFoundation

public class MetronomeEngine: ObservableObject {
    @Published public var isPlaying: Bool = false
    @Published public var tempoBPM: Int = 90
    @Published public var currentBeat: Int = 0 // 1, 2, 3, 4
    @Published public var isAudioMuted: Bool = false

    private var timer: Timer?
    private var audioEngine: AVAudioEngine?
    private var playerNode: AVAudioPlayerNode?
    private var uniformClickBuffer: AVAudioPCMBuffer?

    public init() {
        setupAudio()
    }

    private func setupAudio() {
        let engine = AVAudioEngine()
        let player = AVAudioPlayerNode()
        engine.attach(player)

        let format = AVAudioFormat(standardFormatWithSampleRate: 44100, channels: 1)!
        engine.connect(player, to: engine.mainMixerNode, format: format)

        // Single uniform click sound for all beats (no distinction between strong and weak)
        uniformClickBuffer = generateClickBuffer(frequency: 1400, duration: 0.025, format: format)

        self.audioEngine = engine
        self.playerNode = player

        do {
            try engine.start()
        } catch {
            print("AudioEngine start failed: \(error)")
        }
    }

    private func generateClickBuffer(frequency: Double, duration: Double, format: AVAudioFormat) -> AVAudioPCMBuffer? {
        let sampleRate = format.sampleRate
        let frameCount = AVAudioFrameCount(sampleRate * duration)
        guard let buffer = AVAudioPCMBuffer(pcmFormat: format, frameCapacity: frameCount) else { return nil }
        buffer.frameLength = frameCount

        let channels = buffer.floatChannelData!
        let channel = channels[0]

        for i in 0..<Int(frameCount) {
            let t = Double(i) / sampleRate
            let envelope = exp(-t * 90.0) // sharp percussive decay
            let sample = sin(2.0 * .pi * frequency * t) * envelope
            channel[i] = Float(sample)
        }
        return buffer
    }

    public func toggle() {
        if isPlaying {
            stop()
        } else {
            start()
        }
    }

    public func start() {
        stop()
        isPlaying = true
        currentBeat = 0

        // In 4/2, metronome tempo is blanca (half note) = tempoBPM
        let interval = 60.0 / Double(tempoBPM)

        timer = Timer.scheduledTimer(withTimeInterval: interval, repeats: true) { [weak self] _ in
            self?.tick()
        }
        RunLoop.current.add(timer!, forMode: .common)
        tick() // Immediate first beat
    }

    public func stop() {
        isPlaying = false
        currentBeat = 0
        timer?.invalidate()
        timer = nil
    }

    public func setTempo(_ newBPM: Int) {
        let clamped = max(40, min(160, newBPM))
        self.tempoBPM = clamped
        if isPlaying {
            start() // Restart timer with new interval
        }
    }

    private func tick() {
        DispatchQueue.main.async { [weak self] in
            guard let self = self, self.isPlaying else { return }
            self.currentBeat = (self.currentBeat % 4) + 1
        }

        // Single uniform click for all beats
        if !isAudioMuted, let player = playerNode, let engine = audioEngine, engine.isRunning {
            if let buf = uniformClickBuffer {
                player.play()
                player.scheduleBuffer(buf, at: nil, options: [], completionHandler: nil)
            }
        }
    }

    deinit {
        stop()
        audioEngine?.stop()
    }
}
