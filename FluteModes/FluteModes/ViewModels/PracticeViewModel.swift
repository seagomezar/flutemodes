import Foundation
import Combine
import UIKit

public class PracticeViewModel: ObservableObject {
    @Published public var store: PracticeStore
    @Published public var metronome: MetronomeEngine
    @Published public var scorePlayer: ScoreAudioPlayer

    @Published public var currentTonic: Tonic
    @Published public var currentMode: ModeType
    @Published public var currentArticulation: ArticulationPattern

    @Published public var currentAbcScore: String = ""
    @Published public var showCompletionDialog: Bool = false
    @Published public var keepScreenAwake: Bool {
        didSet {
            UserDefaults.standard.set(keepScreenAwake, forKey: "FluteModes_keepScreenAwake")
            updateScreenAwake()
        }
    }

    private var cancellables = Set<AnyCancellable>()

    public init(
        store: PracticeStore = PracticeStore(),
        metronome: MetronomeEngine = MetronomeEngine(),
        scorePlayer: ScoreAudioPlayer = ScoreAudioPlayer()
    ) {
        self.store = store
        self.metronome = metronome
        self.scorePlayer = scorePlayer

        let savedAwake = UserDefaults.standard.object(forKey: "FluteModes_keepScreenAwake") as? Bool ?? true
        self.keepScreenAwake = savedAwake

        // Restore last session if available, otherwise default to Do Jonico
        if let lastT = store.lastTonic, let lastM = store.lastMode, let lastA = store.lastArticulation {
            self.currentTonic = lastT
            self.currentMode = lastM
            self.currentArticulation = lastA
        } else {
            self.currentTonic = .doNatural
            self.currentMode = .ionian
            self.currentArticulation = .allSlurred
        }

        // Forward child ObservableObject changes to PracticeViewModel
        metronome.objectWillChange
            .receive(on: RunLoop.main)
            .sink { [weak self] _ in
                self?.objectWillChange.send()
            }
            .store(in: &cancellables)

        scorePlayer.objectWillChange
            .receive(on: RunLoop.main)
            .sink { [weak self] _ in
                self?.objectWillChange.send()
            }
            .store(in: &cancellables)

        store.objectWillChange
            .receive(on: RunLoop.main)
            .sink { [weak self] _ in
                self?.objectWillChange.send()
            }
            .store(in: &cancellables)

        updateScore()
    }

    public var practicedModesCountInCurrentTonic: Int {
        store.practicedModesCount(for: currentTonic)
    }

    public var areAllModesInCurrentTonicPracticed: Bool {
        store.areAllSevenModesPracticed(for: currentTonic)
    }

    public var isCurrentTonicMastered: Bool {
        store.isTonicMastered(for: currentTonic)
    }

    public var totalArticulationsInCurrentTonic: Int {
        store.totalArticulationsCompleted(for: currentTonic)
    }

    public var completedArticulationsInCurrentMode: Int {
        store.completedArticulationsCount(tonic: currentTonic, mode: currentMode)
    }

    public func updateScore() {
        self.currentAbcScore = ExerciseGenerator.generateABC(
            tonic: currentTonic,
            mode: currentMode,
            articulation: currentArticulation,
            tempoBPM: metronome.tempoBPM
        )
    }

    public func toggleScorePlayback() {
        scorePlayer.toggle(
            tonic: currentTonic,
            mode: currentMode,
            articulation: currentArticulation,
            tempoBPM: metronome.tempoBPM
        )
    }

    public func selectArticulation(_ articulation: ArticulationPattern, markPreviousCompleted: Bool = true) {
        scorePlayer.stop()
        if markPreviousCompleted && articulation != currentArticulation {
            store.markCompleted(tonic: currentTonic, mode: currentMode, articulation: currentArticulation)
        }
        self.currentArticulation = articulation
        updateScore()
    }

    /// Advances to the next articulation (1 -> 2 -> ... -> 8).
    /// Always marks the current articulation as completed!
    public func advanceToNextArticulation() {
        scorePlayer.stop()
        store.markCompleted(tonic: currentTonic, mode: currentMode, articulation: currentArticulation)

        let all = ArticulationPattern.allCases
        if let idx = all.firstIndex(of: currentArticulation) {
            if idx + 1 < all.count {
                self.currentArticulation = all[idx + 1]
                updateScore()
            } else {
                // Completed all 8 articulations for this mode!
                if store.areAllSevenModesPracticed(for: currentTonic) {
                    self.showCompletionDialog = true
                } else {
                    advanceToNextMode()
                }
            }
        }
    }

    public func selectMode(tonic: Tonic, mode: ModeType) {
        scorePlayer.stop()
        self.currentTonic = tonic
        self.currentMode = mode

        // Suggest the first uncompleted articulation for this mode if any
        let uncompleted = ArticulationPattern.allCases.filter {
            !store.isCompleted(tonic: tonic, mode: mode, articulation: $0)
        }
        self.currentArticulation = uncompleted.first ?? .allSlurred
        updateScore()
    }

    /// Advances to the NEXT MODE within the SAME tonic.
    public func advanceToNextMode() {
        scorePlayer.stop()
        store.markCompleted(tonic: currentTonic, mode: currentMode, articulation: currentArticulation)

        let allPracticed = store.areAllSevenModesPracticed(for: currentTonic)

        let modeOrder: [ModeType] = [.ionian, .lydian, .mixolydian, .dorian, .aeolian, .phrygian, .locrian]
        if let idx = modeOrder.firstIndex(of: currentMode) {
            let nextIdx = (idx + 1) % modeOrder.count
            self.currentMode = modeOrder[nextIdx]
        }

        let uncompleted = ArticulationPattern.allCases.filter {
            !store.isCompleted(tonic: currentTonic, mode: currentMode, articulation: $0)
        }
        self.currentArticulation = uncompleted.first ?? .allSlurred
        updateScore()

        if allPracticed {
            self.showCompletionDialog = true
        }
    }

    /// Legacy alias for backward compatibility
    public func markCurrentCompletedAndAdvanceMode() {
        advanceToNextMode()
    }

    /// Option A: Continue in the same tonic with the next articulation round
    public func startNextArticulationRound() {
        scorePlayer.stop()
        let allArt = ArticulationPattern.allCases
        if let curIdx = allArt.firstIndex(of: currentArticulation) {
            let nextIdx = (curIdx + 1) % allArt.count
            self.currentArticulation = allArt[nextIdx]
        }
        self.currentMode = .ionian
        updateScore()
    }

    /// Option B: Advance to the next chromatic tonic
    public func advanceToNextTonic() {
        scorePlayer.stop()
        self.currentTonic = store.nextTonic(after: currentTonic)
        self.currentMode = .ionian
        updateScore()
    }

    public func suggestNextExercise() {
        scorePlayer.stop()
        // Look first for uncompleted modes in current tonic
        let unpracticedInCurrent = ModeType.allCases.filter {
            store.completedArticulationsCount(tonic: currentTonic, mode: $0) == 0
        }
        if let nextMode = unpracticedInCurrent.first {
            self.currentMode = nextMode
        } else {
            // Find any unpracticed mode in all tonics
            for t in Tonic.allCases {
                let unpracticed = ModeType.allCases.filter {
                    store.completedArticulationsCount(tonic: t, mode: $0) == 0
                }
                if let m = unpracticed.first {
                    self.currentTonic = t
                    self.currentMode = m
                    break
                }
            }
        }
        updateScore()
    }

    public func updateScreenAwake() {
        DispatchQueue.main.async {
            UIApplication.shared.isIdleTimerDisabled = self.keepScreenAwake
        }
    }
}
