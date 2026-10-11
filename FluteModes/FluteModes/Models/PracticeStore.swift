import Foundation

public struct PracticeItem: Identifiable, Hashable, Codable {
    public let tonic: Tonic
    public let mode: ModeType

    public var id: String {
        "\(tonic.rawValue)_\(mode.rawValue)"
    }
}

public class PracticeStore: ObservableObject {
    private let storageKey = "FluteModes_CompletedArticulations_v1"
    private let ej1StorageKey = "FluteModes_EJ1_CompletedArticulations_v1"
    private let ej2StorageKey = "FluteModes_EJ2_CompletedArticulations_v1"
    private let ej4StorageKey = "FluteModes_EJ4_CompletedArticulations_v1"
    private let lastSessionKey = "FluteModes_LastSession_v1"

    // Map: "Tonic_Mode" -> Set of completed articulation IDs (1...8)
    @Published public var completedMap: [String: Set<Int>] = [:]

    // E.J. 1 completed articulation IDs (1...10)
    @Published public var ej1CompletedSet: Set<Int> = []

    // E.J. 2 completed articulation IDs (1...10)
    @Published public var ej2CompletedSet: Set<Int> = []

    // E.J. 4 completed articulation IDs (1...8)
    @Published public var ej4CompletedSet: Set<Int> = []

    @Published public var lastExerciseType: ExerciseType = .ej1
    @Published public var lastEJ1Articulation: EJ1Articulation = .allSlurred8
    @Published public var lastEJ2Articulation: EJ1Articulation = .allSlurred8
    @Published public var lastEJ4Articulation: EJ4Articulation = .allSlurred8
    @Published public var lastEJ4Section: Int = 0
    @Published public var lastTonic: Tonic?
    @Published public var lastMode: ModeType?
    @Published public var lastArticulation: ArticulationPattern?

    public init() {
        loadProgress()
    }

    // MARK: - E.J. 1 Progress (10 Official Articulations)
    public func isEJ1Completed(_ articulation: EJ1Articulation) -> Bool {
        guard articulation.rawValue >= 1 else { return false }
        return ej1CompletedSet.contains(articulation.rawValue)
    }

    public var ej1CompletedCount: Int {
        ej1CompletedSet.filter { (1...10).contains($0) }.count
    }

    public var isEJ1FullyCompleted: Bool {
        ej1CompletedCount == 10
    }

    public func markEJ1Completed(_ articulation: EJ1Articulation) {
        if articulation.rawValue >= 1 {
            ej1CompletedSet.insert(articulation.rawValue)
        }
        lastExerciseType = .ej1
        lastEJ1Articulation = articulation
        saveProgress()
    }

    public func unmarkEJ1Completed(_ articulation: EJ1Articulation) {
        ej1CompletedSet.remove(articulation.rawValue)
        saveProgress()
    }

    public func toggleEJ1Completed(_ articulation: EJ1Articulation) {
        guard articulation.rawValue >= 1 else { return }
        if isEJ1Completed(articulation) {
            unmarkEJ1Completed(articulation)
        } else {
            markEJ1Completed(articulation)
        }
    }

    // MARK: - E.J. 2 Progress (10 Official Articulations)
    public func isEJ2Completed(_ articulation: EJ1Articulation) -> Bool {
        guard articulation.rawValue >= 1 else { return false }
        return ej2CompletedSet.contains(articulation.rawValue)
    }

    public var ej2CompletedCount: Int {
        ej2CompletedSet.filter { (1...10).contains($0) }.count
    }

    public var isEJ2FullyCompleted: Bool {
        ej2CompletedCount == 10
    }

    public func markEJ2Completed(_ articulation: EJ1Articulation) {
        if articulation.rawValue >= 1 {
            ej2CompletedSet.insert(articulation.rawValue)
        }
        lastExerciseType = .ej2
        lastEJ2Articulation = articulation
        saveProgress()
    }

    public func unmarkEJ2Completed(_ articulation: EJ1Articulation) {
        ej2CompletedSet.remove(articulation.rawValue)
        saveProgress()
    }

    public func toggleEJ2Completed(_ articulation: EJ1Articulation) {
        guard articulation.rawValue >= 1 else { return }
        if isEJ2Completed(articulation) {
            unmarkEJ2Completed(articulation)
        } else {
            markEJ2Completed(articulation)
        }
    }

    // MARK: - E.J. 4 Progress (8 Official Articulations)
    public func isEJ4Completed(_ articulation: EJ4Articulation) -> Bool {
        guard articulation.rawValue >= 1 else { return false }
        return ej4CompletedSet.contains(articulation.rawValue)
    }

    public var ej4CompletedCount: Int {
        ej4CompletedSet.filter { (1...8).contains($0) }.count
    }

    public var isEJ4FullyCompleted: Bool {
        ej4CompletedCount == 8
    }

    public func markEJ4Completed(_ articulation: EJ4Articulation) {
        if articulation.rawValue >= 1 {
            ej4CompletedSet.insert(articulation.rawValue)
        }
        lastExerciseType = .ej4
        lastEJ4Articulation = articulation
        saveProgress()
    }

    public func unmarkEJ4Completed(_ articulation: EJ4Articulation) {
        ej4CompletedSet.remove(articulation.rawValue)
        saveProgress()
    }

    public func toggleEJ4Completed(_ articulation: EJ4Articulation) {
        guard articulation.rawValue >= 1 else { return }
        if isEJ4Completed(articulation) {
            unmarkEJ4Completed(articulation)
        } else {
            markEJ4Completed(articulation)
        }
    }

    // MARK: - Unified Chromatic Exercise Helpers (E.J. 1 & E.J. 2)
    public func isChromaticCompleted(exercise: ExerciseType, articulation: EJ1Articulation) -> Bool {
        exercise == .ej2 ? isEJ2Completed(articulation) : isEJ1Completed(articulation)
    }

    public func isChromaticCompleted(_ articulation: EJ1Articulation, for exercise: ExerciseType) -> Bool {
        isChromaticCompleted(exercise: exercise, articulation: articulation)
    }

    public func chromaticCompletedCount(for exercise: ExerciseType) -> Int {
        exercise == .ej2 ? ej2CompletedCount : ej1CompletedCount
    }

    public func isChromaticFullyCompleted(for exercise: ExerciseType) -> Bool {
        exercise == .ej2 ? isEJ2FullyCompleted : isEJ1FullyCompleted
    }

    public func toggleChromaticCompleted(exercise: ExerciseType, articulation: EJ1Articulation) {
        if exercise == .ej2 {
            toggleEJ2Completed(articulation)
        } else {
            toggleEJ1Completed(articulation)
        }
    }

    public func toggleChromaticCompleted(_ articulation: EJ1Articulation, for exercise: ExerciseType) -> Bool {
        toggleChromaticCompleted(exercise: exercise, articulation: articulation)
        return isChromaticCompleted(exercise: exercise, articulation: articulation)
    }

    // MARK: - 84 Modes Progress (84 Modes x 8 Articulations)
    public func isCompleted(tonic: Tonic, mode: ModeType, articulation: ArticulationPattern) -> Bool {
        let key = "\(tonic.rawValue)_\(mode.rawValue)"
        return completedMap[key]?.contains(articulation.rawValue) ?? false
    }

    public func completedArticulationsCount(tonic: Tonic, mode: ModeType) -> Int {
        let key = "\(tonic.rawValue)_\(mode.rawValue)"
        return completedMap[key]?.count ?? 0
    }

    public func isModeFullyCompleted(tonic: Tonic, mode: ModeType) -> Bool {
        return completedArticulationsCount(tonic: tonic, mode: mode) == 8
    }

    /// Number of modes in this tonic that have at least 1 articulation completed (0...7)
    public func practicedModesCount(for tonic: Tonic) -> Int {
        return ModeType.allCases.filter { mode in
            completedArticulationsCount(tonic: tonic, mode: mode) > 0
        }.count
    }

    /// True if all 7 modes in this tonic have been practiced with at least 1 articulation
    public func areAllSevenModesPracticed(for tonic: Tonic) -> Bool {
        return practicedModesCount(for: tonic) == 7
    }

    /// True if all 7 modes have all 8 articulations completed (56/56 total)
    public func isTonicMastered(for tonic: Tonic) -> Bool {
        return ModeType.allCases.allSatisfy { mode in
            isModeFullyCompleted(tonic: tonic, mode: mode)
        }
    }

    /// Total articulations completed in this tonic (0...56)
    public func totalArticulationsCompleted(for tonic: Tonic) -> Int {
        return ModeType.allCases.reduce(0) { sum, mode in
            sum + completedArticulationsCount(tonic: tonic, mode: mode)
        }
    }

    public func markCompleted(tonic: Tonic, mode: ModeType, articulation: ArticulationPattern) {
        let key = "\(tonic.rawValue)_\(mode.rawValue)"
        var current = completedMap[key] ?? Set<Int>()
        current.insert(articulation.rawValue)
        completedMap[key] = current

        lastExerciseType = .modos
        lastTonic = tonic
        lastMode = mode
        lastArticulation = articulation

        saveProgress()
    }

    public func unmarkCompleted(tonic: Tonic, mode: ModeType, articulation: ArticulationPattern) {
        let key = "\(tonic.rawValue)_\(mode.rawValue)"
        var current = completedMap[key] ?? Set<Int>()
        current.remove(articulation.rawValue)
        completedMap[key] = current
        saveProgress()
    }

    public func toggleCompleted(tonic: Tonic, mode: ModeType, articulation: ArticulationPattern) {
        if isCompleted(tonic: tonic, mode: mode, articulation: articulation) {
            unmarkCompleted(tonic: tonic, mode: mode, articulation: articulation)
        } else {
            markCompleted(tonic: tonic, mode: mode, articulation: articulation)
        }
    }

    public func nextTonic(after current: Tonic) -> Tonic {
        let all = Tonic.allCases
        guard let idx = all.firstIndex(of: current) else { return all[0] }
        return all[(idx + 1) % all.count]
    }

    public var totalModesCount: Int {
        return Tonic.allCases.count * ModeType.allCases.count // 84
    }

    public var completedModesCount: Int {
        var count = 0
        for t in Tonic.allCases {
            for m in ModeType.allCases {
                if isModeFullyCompleted(tonic: t, mode: m) {
                    count += 1
                }
            }
        }
        return count
    }

    public var totalPracticedArticulationsCount: Int {
        return completedMap.values.reduce(0) { $0 + $1.count }
    }

    public func resetAll() {
        completedMap.removeAll()
        ej1CompletedSet.removeAll()
        ej2CompletedSet.removeAll()
        ej4CompletedSet.removeAll()
        lastTonic = nil
        lastMode = nil
        lastArticulation = nil
        lastEJ1Articulation = .allSlurred8
        lastEJ2Articulation = .allSlurred8
        lastEJ4Articulation = .allSlurred8
        lastEJ4Section = 0
        UserDefaults.standard.removeObject(forKey: storageKey)
        UserDefaults.standard.removeObject(forKey: ej1StorageKey)
        UserDefaults.standard.removeObject(forKey: ej2StorageKey)
        UserDefaults.standard.removeObject(forKey: ej4StorageKey)
        UserDefaults.standard.removeObject(forKey: lastSessionKey)
    }

    public func saveProgress() {
        let encodable = completedMap.mapValues { Array($0) }
        if let data = try? JSONEncoder().encode(encodable) {
            UserDefaults.standard.set(data, forKey: storageKey)
        }

        if let ej1Data = try? JSONEncoder().encode(Array(ej1CompletedSet)) {
            UserDefaults.standard.set(ej1Data, forKey: ej1StorageKey)
        }

        if let ej2Data = try? JSONEncoder().encode(Array(ej2CompletedSet)) {
            UserDefaults.standard.set(ej2Data, forKey: ej2StorageKey)
        }

        if let ej4Data = try? JSONEncoder().encode(Array(ej4CompletedSet)) {
            UserDefaults.standard.set(ej4Data, forKey: ej4StorageKey)
        }

        var sessionData: [String: String] = [
            "exerciseType": lastExerciseType.rawValue,
            "ej1Articulation": String(lastEJ1Articulation.rawValue),
            "ej2Articulation": String(lastEJ2Articulation.rawValue),
            "ej4Articulation": String(lastEJ4Articulation.rawValue),
            "ej4Section": String(lastEJ4Section)
        ]
        if let t = lastTonic, let m = lastMode, let a = lastArticulation {
            sessionData["tonic"] = t.rawValue
            sessionData["mode"] = String(m.rawValue)
            sessionData["articulation"] = String(a.rawValue)
        }
        UserDefaults.standard.set(sessionData, forKey: lastSessionKey)
    }

    private func loadProgress() {
        if let data = UserDefaults.standard.data(forKey: storageKey),
           let decoded = try? JSONDecoder().decode([String: [Int]].self, from: data) {
            self.completedMap = decoded.mapValues { Set($0) }
        }

        if let ej1Data = UserDefaults.standard.data(forKey: ej1StorageKey),
           let decodedEJ1 = try? JSONDecoder().decode([Int].self, from: ej1Data) {
            self.ej1CompletedSet = Set(decodedEJ1)
        }

        if let ej2Data = UserDefaults.standard.data(forKey: ej2StorageKey),
           let decodedEJ2 = try? JSONDecoder().decode([Int].self, from: ej2Data) {
            self.ej2CompletedSet = Set(decodedEJ2)
        }

        if let ej4Data = UserDefaults.standard.data(forKey: ej4StorageKey),
           let decodedEJ4 = try? JSONDecoder().decode([Int].self, from: ej4Data) {
            self.ej4CompletedSet = Set(decodedEJ4)
        }

        if let sessionData = UserDefaults.standard.dictionary(forKey: lastSessionKey) as? [String: String] {
            if let exStr = sessionData["exerciseType"], let ex = ExerciseType(rawValue: exStr) {
                self.lastExerciseType = ex
            }
            if let ej1ArtStr = sessionData["ej1Articulation"], let ej1Int = Int(ej1ArtStr), let ej1Art = EJ1Articulation(rawValue: ej1Int) {
                self.lastEJ1Articulation = ej1Art
            }
            if let ej2ArtStr = sessionData["ej2Articulation"], let ej2Int = Int(ej2ArtStr), let ej2Art = EJ1Articulation(rawValue: ej2Int) {
                self.lastEJ2Articulation = ej2Art
            }
            if let ej4ArtStr = sessionData["ej4Articulation"], let ej4Int = Int(ej4ArtStr), let ej4Art = EJ4Articulation(rawValue: ej4Int) {
                self.lastEJ4Articulation = ej4Art
            }
            if let ej4SecStr = sessionData["ej4Section"], let ej4Sec = Int(ej4SecStr) {
                self.lastEJ4Section = max(0, min(24, ej4Sec))
            }
            if let tStr = sessionData["tonic"], let t = Tonic(rawValue: tStr) {
                self.lastTonic = t
            }
            if let mStr = sessionData["mode"], let mInt = Int(mStr), let m = ModeType(rawValue: mInt) {
                self.lastMode = m
            }
            if let aStr = sessionData["articulation"], let aInt = Int(aStr), let a = ArticulationPattern(rawValue: aInt) {
                self.lastArticulation = a
            }
        }
    }
}
