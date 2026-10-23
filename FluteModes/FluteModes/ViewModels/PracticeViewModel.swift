import Foundation
import Combine
import UIKit

public class PracticeViewModel: ObservableObject {
    @Published public var store: PracticeStore
    @Published public var metronome: MetronomeEngine
    @Published public var scorePlayer: ScoreAudioPlayer

    @Published public var currentExercise: ExerciseType
    @Published public var currentEJ1Articulation: EJ1Articulation
    @Published public var currentEJ2Articulation: EJ1Articulation
    @Published public var currentEJ4Articulation: EJ4Articulation
    @Published public var currentEJ4Section: Int
    @Published public var currentR2Articulation: EJ4Articulation
    @Published public var currentR2Section: Int
    @Published public var currentR4Articulation: EJ4Articulation
    @Published public var currentR4Section: Int
    @Published public var currentEJ5Articulation: EJ5Articulation
    @Published public var currentEJ5Section: Int
    @Published public var currentEJ10Articulation: EJ5Articulation
    @Published public var currentEJ10Section: Int
    @Published public var currentEJ11Articulation: EJ5Articulation
    @Published public var currentEJ11Section: Int
    @Published public var currentR1Articulation: EJ5Articulation
    @Published public var currentR1Section: Int
    @Published public var currentR5Articulation: EJ5Articulation
    @Published public var currentR5Section: Int

    @Published public var currentTonic: Tonic
    @Published public var currentMode: ModeType
    @Published public var currentArticulation: ArticulationPattern
    @Published public var currentModalScheme: ModalScheme

    // Conservatory Coach (Option 1) — 3-Step Practice Wizard state
    @Published public var showPracticeWizard: Bool = false
    @Published public var wizardDuration: PracticeWizardDuration = .min30
    @Published public var wizardFocus: PracticeWizardFocus = .modes
    @Published public var wizardTonic: Tonic = .doNatural
    @Published public var wizardMode: ModeType = .ionian

    @Published public var currentAbcScore: String = ""
    @Published public var showCompletionDialog: Bool = false
    @Published public var showEJ1CompletionDialog: Bool = false
    @Published public var showEJ2CompletionDialog: Bool = false
    @Published public var showEJ4CompletionDialog: Bool = false
    @Published public var showEJ5TypeCompletionDialog: Bool = false
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

        self.currentExercise = store.lastExerciseType
        self.currentEJ1Articulation = store.lastEJ1Articulation
        self.currentEJ2Articulation = store.lastEJ2Articulation
        self.currentEJ4Articulation = store.lastEJ4Articulation
        self.currentEJ4Section = store.lastEJ4Section
        self.currentR2Articulation = store.lastR2Articulation
        self.currentR2Section = store.lastR2Section
        self.currentR4Articulation = store.lastR4Articulation
        self.currentR4Section = store.lastR4Section
        self.currentEJ5Articulation = store.lastEJ5Articulation
        self.currentEJ5Section = store.lastEJ5Section
        self.currentEJ10Articulation = store.lastEJ10Articulation
        self.currentEJ10Section = store.lastEJ10Section
        self.currentEJ11Articulation = store.lastEJ11Articulation
        self.currentEJ11Section = store.lastEJ11Section
        self.currentR1Articulation = store.lastR1Articulation
        self.currentR1Section = store.lastR1Section
        self.currentR5Articulation = store.lastR5Articulation
        self.currentR5Section = store.lastR5Section
        self.currentModalScheme = .ej4
        store.lastModalScheme = .ej4

        // Restore last session if available, otherwise default to Do Jonico
        if let lastT = store.lastTonic, let lastM = store.lastMode, let lastA = store.lastArticulation {
            self.currentTonic = lastT
            self.currentMode = lastM
            self.currentArticulation = lastA
            self.wizardTonic = lastT
            self.wizardMode = lastM
        } else {
            self.currentTonic = .doNatural
            self.currentMode = .ionian
            self.currentArticulation = .allSlurred
            self.wizardTonic = .doNatural
            self.wizardMode = .ionian
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

    public var currentChromaticArticulation: EJ1Articulation {
        currentExercise == .ej2 ? currentEJ2Articulation : currentEJ1Articulation
    }

    public var currentEJ4TypeArticulation: EJ4Articulation {
        switch currentExercise {
        case .r2: return currentR2Articulation
        case .r4: return currentR4Articulation
        default:  return currentEJ4Articulation
        }
    }

    public var currentEJ4TypeSectionIndex: Int {
        switch currentExercise {
        case .r2: return currentR2Section
        case .r4: return currentR4Section
        default:  return currentEJ4Section
        }
    }

    public var currentEJ5TypeArticulation: EJ5Articulation {
        switch currentExercise {
        case .ej5:  return currentEJ5Articulation
        case .ej10: return currentEJ10Articulation
        case .ej11: return currentEJ11Articulation
        case .r1:   return currentR1Articulation
        case .r5:   return currentR5Articulation
        default:    return currentEJ5Articulation
        }
    }

    public var currentEJ5TypeSectionIndex: Int {
        switch currentExercise {
        case .ej5:  return currentEJ5Section
        case .ej10: return currentEJ10Section
        case .ej11: return currentEJ11Section
        case .r1:   return currentR1Section
        case .r5:   return currentR5Section
        default:    return 0
        }
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

    public func selectExercise(_ type: ExerciseType) {
        scorePlayer.stop()
        self.currentExercise = type
        store.lastExerciseType = type
        store.saveProgress()
        updateScore()
    }

    public func updateScore() {
        switch currentExercise {
        case .ej1:
            self.currentAbcScore = ExerciseGenerator.generateEJ1ABC(
                articulation: currentEJ1Articulation,
                tempoBPM: metronome.tempoBPM
            )
        case .ej2:
            self.currentAbcScore = ExerciseGenerator.generateEJ2ABC(
                articulation: currentEJ2Articulation,
                tempoBPM: metronome.tempoBPM
            )
        case .ej4:
            self.currentAbcScore = ExerciseGenerator.generateEJ4ABC(
                sectionIndex: currentEJ4Section,
                articulation: currentEJ4Articulation,
                tempoBPM: metronome.tempoBPM
            )
        case .r2:
            self.currentAbcScore = ExerciseGenerator.generateR2ABC(
                sectionIndex: currentR2Section,
                articulation: currentR2Articulation,
                tempoBPM: metronome.tempoBPM
            )
        case .r4:
            self.currentAbcScore = ExerciseGenerator.generateR4ABC(
                sectionIndex: currentR4Section,
                articulation: currentR4Articulation,
                tempoBPM: metronome.tempoBPM
            )
        case .ej5:
            self.currentAbcScore = ExerciseGenerator.generateEJ5ABC(
                sectionIndex: currentEJ5Section,
                articulation: currentEJ5Articulation,
                tempoBPM: metronome.tempoBPM
            )
        case .ej10:
            self.currentAbcScore = ExerciseGenerator.generateEJ10ABC(
                sectionIndex: currentEJ10Section,
                articulation: currentEJ10Articulation,
                tempoBPM: metronome.tempoBPM
            )
        case .ej11:
            self.currentAbcScore = ExerciseGenerator.generateEJ11ABC(
                sectionIndex: currentEJ11Section,
                articulation: currentEJ11Articulation,
                tempoBPM: metronome.tempoBPM
            )
        case .r1:
            self.currentAbcScore = ExerciseGenerator.generateR1ABC(
                sectionIndex: currentR1Section,
                articulation: currentR1Articulation,
                tempoBPM: metronome.tempoBPM
            )
        case .r5:
            self.currentAbcScore = ExerciseGenerator.generateR5ABC(
                sectionIndex: currentR5Section,
                articulation: currentR5Articulation,
                tempoBPM: metronome.tempoBPM
            )
        case .modos:
            self.currentAbcScore = ExerciseGenerator.generateABC(
                tonic: currentTonic,
                mode: currentMode,
                articulation: currentArticulation,
                tempoBPM: metronome.tempoBPM,
                scheme: currentModalScheme
            )
        }
    }

    public func toggleScorePlayback() {
        switch currentExercise {
        case .ej1:
            scorePlayer.toggleEJ1(
                articulation: currentEJ1Articulation,
                tempoBPM: metronome.tempoBPM
            )
        case .ej2:
            scorePlayer.toggleEJ2(
                articulation: currentEJ2Articulation,
                tempoBPM: metronome.tempoBPM
            )
        case .ej4, .r2, .r4:
            scorePlayer.toggleEJ4(
                exercise: currentExercise,
                sectionIndex: currentEJ4TypeSectionIndex,
                articulation: currentEJ4TypeArticulation,
                tempoBPM: metronome.tempoBPM
            )
        case .ej5, .ej10, .ej11, .r1, .r5:
            scorePlayer.toggleEJ5Type(
                exercise: currentExercise,
                sectionIndex: currentEJ5TypeSectionIndex,
                articulation: currentEJ5TypeArticulation,
                tempoBPM: metronome.tempoBPM
            )
        case .modos:
            scorePlayer.toggle(
                tonic: currentTonic,
                mode: currentMode,
                articulation: currentArticulation,
                tempoBPM: metronome.tempoBPM,
                scheme: currentModalScheme
            )
        }
    }

    // MARK: - E.J. 1 & E.J. 2 Articulation Navigation
    public func selectChromaticArticulation(_ articulation: EJ1Articulation, markPreviousCompleted: Bool = true) {
        if currentExercise == .ej2 {
            selectEJ2Articulation(articulation, markPreviousCompleted: markPreviousCompleted)
        } else {
            selectEJ1Articulation(articulation, markPreviousCompleted: markPreviousCompleted)
        }
    }

    public func advanceToNextChromaticArticulation() {
        if currentExercise == .ej2 {
            advanceToNextEJ2Articulation()
        } else {
            advanceToNextEJ1Articulation()
        }
    }

    public func selectEJ1Articulation(_ articulation: EJ1Articulation, markPreviousCompleted: Bool = true) {
        scorePlayer.stop()
        if markPreviousCompleted && articulation != currentEJ1Articulation && currentEJ1Articulation.rawValue >= 1 {
            store.markEJ1Completed(currentEJ1Articulation)
        }
        self.currentExercise = .ej1
        self.currentEJ1Articulation = articulation
        store.lastExerciseType = .ej1
        store.lastEJ1Articulation = articulation
        store.saveProgress()
        updateScore()
    }

    public func selectEJ2Articulation(_ articulation: EJ1Articulation, markPreviousCompleted: Bool = true) {
        scorePlayer.stop()
        if markPreviousCompleted && articulation != currentEJ2Articulation && currentEJ2Articulation.rawValue >= 1 {
            store.markEJ2Completed(currentEJ2Articulation)
        }
        self.currentExercise = .ej2
        self.currentEJ2Articulation = articulation
        store.lastExerciseType = .ej2
        store.lastEJ2Articulation = articulation
        store.saveProgress()
        updateScore()
    }

    public func advanceToNextEJ1Articulation() {
        scorePlayer.stop()
        if currentEJ1Articulation.rawValue >= 1 {
            store.markEJ1Completed(currentEJ1Articulation)
        }
        let practiceArts = EJ1Articulation.practiceCases
        if let idx = practiceArts.firstIndex(of: currentEJ1Articulation) {
            if idx + 1 < practiceArts.count {
                self.currentEJ1Articulation = practiceArts[idx + 1]
                store.lastEJ1Articulation = self.currentEJ1Articulation
                store.saveProgress()
                updateScore()
            } else {
                self.showEJ1CompletionDialog = true
            }
        } else {
            self.currentEJ1Articulation = .allSlurred8
            store.lastEJ1Articulation = .allSlurred8
            store.saveProgress()
            updateScore()
        }
    }

    public func advanceToNextEJ2Articulation() {
        scorePlayer.stop()
        if currentEJ2Articulation.rawValue >= 1 {
            store.markEJ2Completed(currentEJ2Articulation)
        }
        let practiceArts = EJ1Articulation.practiceCases
        if let idx = practiceArts.firstIndex(of: currentEJ2Articulation) {
            if idx + 1 < practiceArts.count {
                self.currentEJ2Articulation = practiceArts[idx + 1]
                store.lastEJ2Articulation = self.currentEJ2Articulation
                store.saveProgress()
                updateScore()
            } else {
                self.showEJ2CompletionDialog = true
            }
        } else {
            self.currentEJ2Articulation = .allSlurred8
            store.lastEJ2Articulation = .allSlurred8
            store.saveProgress()
            updateScore()
        }
    }

    public func restartEJ1Round() {
        scorePlayer.stop()
        self.currentEJ1Articulation = .allSlurred8
        store.lastEJ1Articulation = .allSlurred8
        store.saveProgress()
        updateScore()
    }

    public func restartEJ2Round() {
        scorePlayer.stop()
        self.currentEJ2Articulation = .allSlurred8
        store.lastEJ2Articulation = .allSlurred8
        store.saveProgress()
        updateScore()
    }

    // MARK: - 8-Articulation 25-Key Exercises (E.J. 4, R. 2, R. 4)
    public func selectEJ4Section(_ secIdx: Int, for exercise: ExerciseType? = nil) {
        scorePlayer.stop()
        let targetEx = exercise ?? (currentExercise.isEJ4Exercise ? currentExercise : .ej4)
        let clamped = max(0, min(EJ4Section.all.count - 1, secIdx))
        self.currentExercise = targetEx
        store.lastExerciseType = targetEx
        switch targetEx {
        case .r2:
            self.currentR2Section = clamped
            store.lastR2Section = clamped
        case .r4:
            self.currentR4Section = clamped
            store.lastR4Section = clamped
        default:
            self.currentEJ4Section = clamped
            store.lastEJ4Section = clamped
        }
        store.saveProgress()
        updateScore()
    }

    public func advanceToNextEJ4Section() {
        scorePlayer.stop()
        let nextSec = (currentEJ4TypeSectionIndex + 1) % EJ4Section.all.count
        selectEJ4Section(nextSec)
    }

    public func selectEJ4Articulation(_ articulation: EJ4Articulation, for exercise: ExerciseType? = nil, markPreviousCompleted: Bool = true) {
        scorePlayer.stop()
        let targetEx = exercise ?? (currentExercise.isEJ4Exercise ? currentExercise : .ej4)
        let prevArt: EJ4Articulation
        switch targetEx {
        case .r2: prevArt = currentR2Articulation
        case .r4: prevArt = currentR4Articulation
        default:  prevArt = currentEJ4Articulation
        }
        if markPreviousCompleted && articulation != prevArt && prevArt.rawValue >= 1 {
            store.markEJ4Completed(prevArt, for: targetEx)
        }
        self.currentExercise = targetEx
        store.lastExerciseType = targetEx
        switch targetEx {
        case .r2:
            self.currentR2Articulation = articulation
            store.lastR2Articulation = articulation
        case .r4:
            self.currentR4Articulation = articulation
            store.lastR4Articulation = articulation
        default:
            self.currentEJ4Articulation = articulation
            store.lastEJ4Articulation = articulation
        }
        store.saveProgress()
        updateScore()
    }

    public func advanceToNextEJ4Articulation() {
        scorePlayer.stop()
        let curArt = currentEJ4TypeArticulation
        if curArt.rawValue >= 1 {
            store.markEJ4Completed(curArt, for: currentExercise)
        }
        let practiceArts = EJ4Articulation.practiceCases
        if let idx = practiceArts.firstIndex(of: curArt) {
            if idx + 1 < practiceArts.count {
                selectEJ4Articulation(practiceArts[idx + 1], markPreviousCompleted: false)
            } else {
                self.showEJ4CompletionDialog = true
            }
        } else {
            selectEJ4Articulation(.allSlurred8, markPreviousCompleted: false)
        }
    }

    public func restartEJ4Round() {
        selectEJ4Articulation(.allSlurred8, markPreviousCompleted: false)
    }

    // MARK: - 10-Articulation Sectioned Exercises (E.J. 5, E.J. 10, E.J. 11, R. 1, R. 5)
    public func selectEJ5TypeSection(_ secIdx: Int, for exercise: ExerciseType? = nil) {
        scorePlayer.stop()
        let targetEx = exercise ?? currentExercise
        let maxSec = targetEx.sectionCount - 1
        let clamped = max(0, min(maxSec, secIdx))
        self.currentExercise = targetEx
        store.lastExerciseType = targetEx
        switch targetEx {
        case .ej5:
            self.currentEJ5Section = clamped
            store.lastEJ5Section = clamped
        case .ej10:
            self.currentEJ10Section = clamped
            store.lastEJ10Section = clamped
        case .ej11:
            self.currentEJ11Section = clamped
            store.lastEJ11Section = clamped
        case .r1:
            self.currentR1Section = clamped
            store.lastR1Section = clamped
        case .r5:
            self.currentR5Section = clamped
            store.lastR5Section = clamped
        default:
            break
        }
        store.saveProgress()
        updateScore()
    }

    public func advanceToNextEJ5TypeSection() {
        scorePlayer.stop()
        let nextSec = (currentEJ5TypeSectionIndex + 1) % currentExercise.sectionCount
        selectEJ5TypeSection(nextSec)
    }

    public func selectEJ5TypeArticulation(_ articulation: EJ5Articulation, for exercise: ExerciseType? = nil, markPreviousCompleted: Bool = true) {
        scorePlayer.stop()
        let targetEx = exercise ?? currentExercise
        let prevArt: EJ5Articulation
        switch targetEx {
        case .ej5:  prevArt = currentEJ5Articulation
        case .ej10: prevArt = currentEJ10Articulation
        case .ej11: prevArt = currentEJ11Articulation
        case .r1:   prevArt = currentR1Articulation
        case .r5:   prevArt = currentR5Articulation
        default:    prevArt = currentEJ5Articulation
        }
        if markPreviousCompleted && articulation != prevArt && prevArt.rawValue >= 1 {
            store.markEJ5TypeCompleted(prevArt, for: targetEx)
        }
        self.currentExercise = targetEx
        store.lastExerciseType = targetEx
        switch targetEx {
        case .ej5:
            self.currentEJ5Articulation = articulation
            store.lastEJ5Articulation = articulation
        case .ej10:
            self.currentEJ10Articulation = articulation
            store.lastEJ10Articulation = articulation
        case .ej11:
            self.currentEJ11Articulation = articulation
            store.lastEJ11Articulation = articulation
        case .r1:
            self.currentR1Articulation = articulation
            store.lastR1Articulation = articulation
        case .r5:
            self.currentR5Articulation = articulation
            store.lastR5Articulation = articulation
        default:
            break
        }
        store.saveProgress()
        updateScore()
    }

    public func advanceToNextEJ5TypeArticulation() {
        scorePlayer.stop()
        let curArt = currentEJ5TypeArticulation
        if curArt.rawValue >= 1 {
            store.markEJ5TypeCompleted(curArt, for: currentExercise)
        }
        let practiceArts = EJ5Articulation.practiceCases
        if let idx = practiceArts.firstIndex(of: curArt) {
            if idx + 1 < practiceArts.count {
                selectEJ5TypeArticulation(practiceArts[idx + 1], markPreviousCompleted: false)
            } else {
                self.showEJ5TypeCompletionDialog = true
            }
        } else {
            selectEJ5TypeArticulation(.allSlurred, markPreviousCompleted: false)
        }
    }

    public func restartEJ5TypeRound() {
        selectEJ5TypeArticulation(.allSlurred, markPreviousCompleted: false)
    }

    // MARK: - 84 Modes Articulation & Mode Navigation
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
                if store.areAllSevenModesPracticed(for: currentTonic) {
                    self.showCompletionDialog = true
                } else {
                    advanceToNextMode()
                }
            }
        }
    }

    public func selectMode(tonic: Tonic, mode: ModeType, scheme: ModalScheme? = nil) {
        scorePlayer.stop()
        self.currentExercise = .modos
        self.currentTonic = tonic
        self.currentMode = mode
        if let scheme = scheme {
            self.currentModalScheme = scheme
            store.lastModalScheme = scheme
        }
        store.lastExerciseType = .modos
        store.lastTonic = tonic
        store.lastMode = mode

        let uncompleted = ArticulationPattern.allCases.filter {
            !store.isCompleted(tonic: tonic, mode: mode, articulation: $0)
        }
        self.currentArticulation = uncompleted.first ?? .allSlurred
        store.lastArticulation = self.currentArticulation
        store.saveProgress()
        updateScore()
    }

    public func selectModalScheme(_ scheme: ModalScheme) {
        scorePlayer.stop()
        self.currentModalScheme = scheme
        store.lastModalScheme = scheme
        store.saveProgress()
        updateScore()
    }

    public var generatedRoutineBlocks: [PracticeRoutineBlock] {
        PracticeRoutineBlock.generateRoutine(
            duration: wizardDuration,
            focus: wizardFocus,
            tonic: wizardTonic,
            mode: wizardMode
        )
    }

    public func applyWizardRoutineBlock(_ block: PracticeRoutineBlock) {
        scorePlayer.stop()
        self.showPracticeWizard = false
        if block.exerciseType == .modos {
            selectMode(tonic: block.tonic, mode: block.mode, scheme: block.modalScheme)
        } else {
            self.currentTonic = block.tonic
            self.currentMode = block.mode
            self.currentModalScheme = block.modalScheme
            store.lastModalScheme = block.modalScheme
            selectExercise(block.exerciseType)
        }
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

    public func markCurrentCompletedAndAdvanceMode() {
        advanceToNextMode()
    }

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

    public func advanceToNextTonic() {
        scorePlayer.stop()
        self.currentTonic = store.nextTonic(after: currentTonic)
        self.currentMode = .ionian
        updateScore()
    }

    public func suggestNextExercise() {
        scorePlayer.stop()
        self.currentExercise = .modos
        store.lastExerciseType = .modos
        let unpracticedInCurrent = ModeType.allCases.filter {
            store.completedArticulationsCount(tonic: currentTonic, mode: $0) == 0
        }
        if let nextMode = unpracticedInCurrent.first {
            self.currentMode = nextMode
        } else {
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
