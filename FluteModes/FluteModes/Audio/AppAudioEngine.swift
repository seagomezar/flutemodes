import Foundation
import AVFoundation

/// Unified Audio Engine & Session Manager for FluteModes
/// Manages the physical iOS audio pipeline, ensuring audio plays reliably
/// on physical iPhones and iPads even in hardware Silent Mode.
public class AppAudioEngine: NSObject {
    public static let shared = AppAudioEngine()

    public let engine = AVAudioEngine()
    public let metronomePlayer = AVAudioPlayerNode()
    public let pianoPlayer = AVAudioPlayerNode()

    public let standardFormat = AVAudioFormat(standardFormatWithSampleRate: 44100, channels: 1)!

    private var isConfigured = false
    private let lock = NSLock()

    private override init() {
        super.init()
        setupEngine()
        setupNotifications()
    }

    /// Sets up AVAudioSession with .playback category and activates it.
    /// This is strictly required on physical iOS devices to bypass the silent switch
    /// and to ensure audio output is routed properly to speakers / headphones.
    public func configureSession() {
        let session = AVAudioSession.sharedInstance()
        do {
            try session.setCategory(.playback, mode: .default, options: [.mixWithOthers])
            try session.setActive(true, options: [])
        } catch {
            print("[AppAudioEngine] Failed to configure/activate AVAudioSession: \(error)")
        }
    }

    private func setupEngine() {
        lock.lock()
        defer { lock.unlock() }

        guard !isConfigured else { return }

        configureSession()

        engine.attach(metronomePlayer)
        engine.attach(pianoPlayer)

        engine.connect(metronomePlayer, to: engine.mainMixerNode, format: standardFormat)
        engine.connect(pianoPlayer, to: engine.mainMixerNode, format: standardFormat)

        // Set baseline mixer output volume
        engine.mainMixerNode.outputVolume = 1.0

        do {
            try engine.start()
            isConfigured = true
        } catch {
            print("[AppAudioEngine] Engine start error: \(error)")
        }
    }

    /// Ensures both the audio session and the audio engine are active and running.
    public func ensureEngineRunning() {
        configureSession()

        lock.lock()
        defer { lock.unlock() }

        if !engine.isRunning {
            do {
                try engine.start()
            } catch {
                print("[AppAudioEngine] Restarting engine failed: \(error)")
            }
        }
    }

    // MARK: - Notifications & Interruption Recovery
    private func setupNotifications() {
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleInterruption),
            name: AVAudioSession.interruptionNotification,
            object: nil
        )
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleRouteChange),
            name: AVAudioSession.routeChangeNotification,
            object: nil
        )
    }

    @objc private func handleInterruption(notification: Notification) {
        guard let userInfo = notification.userInfo,
              let typeValue = userInfo[AVAudioSessionInterruptionTypeKey] as? UInt,
              let type = AVAudioSession.InterruptionType(rawValue: typeValue) else {
            return
        }

        switch type {
        case .began:
            break
        case .ended:
            if let optionsValue = userInfo[AVAudioSessionInterruptionOptionKey] as? UInt {
                let options = AVAudioSession.InterruptionOptions(rawValue: optionsValue)
                if options.contains(.shouldResume) {
                    ensureEngineRunning()
                }
            }
        @unknown default:
            break
        }
    }

    @objc private func handleRouteChange(notification: Notification) {
        // When headphones/AirPods are plugged or unplugged, restart engine if needed
        ensureEngineRunning()
    }

    deinit {
        NotificationCenter.default.removeObserver(self)
        engine.stop()
    }
}
