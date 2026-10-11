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
    private let ej5StorageKey = "FluteModes_EJ5_CompletedArticulations_v1"
    private let ej10StorageKey = "FluteModes_EJ10_CompletedArticulations_v1"
    private let ej11StorageKey = "FluteModes_EJ11_CompletedArticulations_v1"
    private let r1StorageKey = "FluteModes_R1_CompletedArticulations_v1"
    private let r2StorageKey = "FluteModes_R2_CompletedArticulations_v1"
    private let r4StorageKey = "FluteModes_R4_CompletedArticulations_v1"
    private let r5StorageKey = "FluteModes_R5_CompletedArticulations_v1"
    private let lastSessionKey = "FluteModes_LastSession_v1"

    // Map: "Tonic_Mode" -> Set of completed articulation IDs (1...8)
    @Published public var completedMap: [String: Set<Int>] = [:]

    // E.J. 1 completed articulation IDs (1...10)
    @Published public var ej1CompletedSet: Set<Int> = []

    // E.J. 2 completed articulation IDs (1...10)
    @Published public var ej2CompletedSet: Set<Int> = []

    // 8-Articulation 24-Key Exercises: E.J. 4, R. 2, R. 4 (1...8)
    @Published public var ej4CompletedSet: Set<Int> = []
    @Published public var r2CompletedSet: Set<Int> = []
    @Published public var r4CompletedSet: Set<Int> = []

    // 10-Articulation Sectioned Exercises: E.J. 5, E.J. 10, E.J. 11, R. 1, R. 5 (1...10)
    @Published public var ej5CompletedSet: Set<Int> = []
    @Published public var ej10CompletedSet: Set<Int> = []
    @Published public var ej11CompletedSet: Set<Int> = []
    @Published public var r1CompletedSet: Set<Int> = []
    @Published public var r5CompletedSet: Set<Int> = []

    @Published public var lastExerciseType: ExerciseType = .ej1
    @Published public var lastEJ1Articulation: EJ1Articulation = .allSlurred8
    @Published public var lastEJ2Articulation: EJ1Articulation = .allSlurred8
    @Published public var lastEJ4Articulation: EJ4Articulation = .allSlurred8
    @Published public var lastEJ4Section: Int = 0
    @Published public var lastR2Articulation: EJ4Articulation = .allSlurred8
    @Published public var lastR2Section: Int = 0
    @Published public var lastR4Articulation: EJ4Articulation = .allSlurred8
    @Published public var lastR4Section: Int = 0
    @Published public var lastEJ5Articulation: EJ5Articulation = .allSlurred
    @Published public var lastEJ5Section: Int = 0
    @Published public var lastEJ10Articulation: EJ5Articulation = .allSlurred
    @Published public var lastEJ10Section: Int = 0
    @Published public var lastEJ11Articulation: EJ5Articulation = .allSlurred
    @Published public var lastEJ11Section: Int = 0
    @Published public var lastR1Articulation: EJ5Articulation = .allSlurred
    @Published public var lastR1Section: Int = 0
    @Published public var lastR5Articulation: EJ5Articulation = .allSlurred
    @Published public var lastR5Section: Int = 0
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

    // MARK: - 8-Articulation 25-Key Exercises Progress (E.J. 4, R. 2, R. 4)
    public func isEJ4Completed(_ articulation: EJ4Articulation, for exercise: ExerciseType = .ej4) -> Bool {
        guard articulation.rawValue >= 1 else { return false }
        switch exercise {
        case .r2: return r2CompletedSet.contains(articulation.rawValue)
        case .r4: return r4CompletedSet.contains(articulation.rawValue)
        default:  return ej4CompletedSet.contains(articulation.rawValue)
        }
    }

    public var ej4CompletedCount: Int {
        ej4CompletedSet.filter { (1...8).contains($0) }.count
    }
    public var r2CompletedCount: Int {
        r2CompletedSet.filter { (1...8).contains($0) }.count
    }
    public var r4CompletedCount: Int {
        r4CompletedSet.filter { (1...8).contains($0) }.count
    }

    public func ej4TypeCompletedCount(for exercise: ExerciseType = .ej4) -> Int {
        switch exercise {
        case .r2: return r2CompletedCount
        case .r4: return r4CompletedCount
        default:  return ej4CompletedCount
        }
    }

    public var isEJ4FullyCompleted: Bool {
        ej4CompletedCount == 8
    }

    public func isEJ4TypeFullyCompleted(for exercise: ExerciseType = .ej4) -> Bool {
        ej4TypeCompletedCount(for: exercise) == 8
    }

    public func markEJ4Completed(_ articulation: EJ4Articulation, for exercise: ExerciseType = .ej4) {
        if articulation.rawValue >= 1 {
            switch exercise {
            case .r2:
                r2CompletedSet.insert(articulation.rawValue)
                lastR2Articulation = articulation
            case .r4:
                r4CompletedSet.insert(articulation.rawValue)
                lastR4Articulation = articulation
            default:
                ej4CompletedSet.insert(articulation.rawValue)
                lastEJ4Articulation = articulation
            }
        }
        lastExerciseType = exercise
        saveProgress()
    }

    public func unmarkEJ4Completed(_ articulation: EJ4Articulation, for exercise: ExerciseType = .ej4) {
        switch exercise {
        case .r2: r2CompletedSet.remove(articulation.rawValue)
        case .r4: r4CompletedSet.remove(articulation.rawValue)
        default:  ej4CompletedSet.remove(articulation.rawValue)
        }
        saveProgress()
    }

    public func toggleEJ4Completed(_ articulation: EJ4Articulation, for exercise: ExerciseType = .ej4) {
        guard articulation.rawValue >= 1 else { return }
        if isEJ4Completed(articulation, for: exercise) {
            unmarkEJ4Completed(articulation, for: exercise)
        } else {
            markEJ4Completed(articulation, for: exercise)
        }
    }

    // MARK: - 10-Articulation Sectioned Exercises Progress (E.J. 5, E.J. 10, E.J. 11, R. 1, R. 5)
    public var ej5CompletedCount: Int {
        ej5CompletedSet.filter { (1...10).contains($0) }.count
    }
    public var isEJ5FullyCompleted: Bool { ej5CompletedCount == 10 }

    public var ej10CompletedCount: Int {
        ej10CompletedSet.filter { (1...10).contains($0) }.count
    }
    public var isEJ10FullyCompleted: Bool { ej10CompletedCount == 10 }

    public var ej11CompletedCount: Int {
        ej11CompletedSet.filter { (1...10).contains($0) }.count
    }
    public var isEJ11FullyCompleted: Bool { ej11CompletedCount == 10 }

    public var r1CompletedCount: Int {
        r1CompletedSet.filter { (1...10).contains($0) }.count
    }
    public var isR1FullyCompleted: Bool { r1CompletedCount == 10 }

    public var r5CompletedCount: Int {
        r5CompletedSet.filter { (1...10).contains($0) }.count
    }
    public var isR5FullyCompleted: Bool { r5CompletedCount == 10 }

    public func isEJ5TypeCompleted(_ articulation: EJ5Articulation, for exercise: ExerciseType) -> Bool {
        guard articulation.rawValue >= 1 else { return false }
        switch exercise {
        case .ej5:  return ej5CompletedSet.contains(articulation.rawValue)
        case .ej10: return ej10CompletedSet.contains(articulation.rawValue)
        case .ej11: return ej11CompletedSet.contains(articulation.rawValue)
        case .r1:   return r1CompletedSet.contains(articulation.rawValue)
        case .r5:   return r5CompletedSet.contains(articulation.rawValue)
        default:    return false
        }
    }

    public func ej5TypeCompletedCount(for exercise: ExerciseType) -> Int {
        switch exercise {
        case .ej5:  return ej5CompletedCount
        case .ej10: return ej10CompletedCount
        case .ej11: return ej11CompletedCount
        case .r1:   return r1CompletedCount
        case .r5:   return r5CompletedCount
        default:    return 0
        }
    }

    public func isEJ5TypeFullyCompleted(for exercise: ExerciseType) -> Bool {
        ej5TypeCompletedCount(for: exercise) == 10
    }

    public func markEJ5TypeCompleted(_ articulation: EJ5Articulation, for exercise: ExerciseType) {
        if articulation.rawValue >= 1 {
            switch exercise {
            case .ej5:
                ej5CompletedSet.insert(articulation.rawValue)
                lastEJ5Articulation = articulation
            case .ej10:
                ej10CompletedSet.insert(articulation.rawValue)
                lastEJ10Articulation = articulation
            case .ej11:
                ej11CompletedSet.insert(articulation.rawValue)
                lastEJ11Articulation = articulation
            case .r1:
                r1CompletedSet.insert(articulation.rawValue)
                lastR1Articulation = articulation
            case .r5:
                r5CompletedSet.insert(articulation.rawValue)
                lastR5Articulation = articulation
            default:
                break
            }
        }
        lastExerciseType = exercise
        saveProgress()
    }

    public func unmarkEJ5TypeCompleted(_ articulation: EJ5Articulation, for exercise: ExerciseType) {
        switch exercise {
        case .ej5:  ej5CompletedSet.remove(articulation.rawValue)
        case .ej10: ej10CompletedSet.remove(articulation.rawValue)
        case .ej11: ej11CompletedSet.remove(articulation.rawValue)
        case .r1:   r1CompletedSet.remove(articulation.rawValue)
        case .r5:   r5CompletedSet.remove(articulation.rawValue)
        default:    break
        }
        saveProgress()
    }

    public func toggleEJ5TypeCompleted(_ articulation: EJ5Articulation, for exercise: ExerciseType) {
        guard articulation.rawValue >= 1 else { return }
        if isEJ5TypeCompleted(articulation, for: exercise) {
            unmarkEJ5TypeCompleted(articulation, for: exercise)
        } else {
            markEJ5TypeCompleted(articulation, for: exercise)
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
        r2CompletedSet.removeAll()
        r4CompletedSet.removeAll()
        ej5CompletedSet.removeAll()
        ej10CompletedSet.removeAll()
        ej11CompletedSet.removeAll()
        r1CompletedSet.removeAll()
        r5CompletedSet.removeAll()
        lastTonic = nil
        lastMode = nil
        lastArticulation = nil
        lastEJ1Articulation = .allSlurred8
        lastEJ2Articulation = .allSlurred8
        lastEJ4Articulation = .allSlurred8
        lastEJ4Section = 0
        lastR2Articulation = .allSlurred8
        lastR2Section = 0
        lastR4Articulation = .allSlurred8
        lastR4Section = 0
        lastEJ5Articulation = .allSlurred
        lastEJ5Section = 0
        lastEJ10Articulation = .allSlurred
        lastEJ10Section = 0
        lastEJ11Articulation = .allSlurred
        lastEJ11Section = 0
        lastR1Articulation = .allSlurred
        lastR1Section = 0
        lastR5Articulation = .allSlurred
        lastR5Section = 0
        UserDefaults.standard.removeObject(forKey: storageKey)
        UserDefaults.standard.removeObject(forKey: ej1StorageKey)
        UserDefaults.standard.removeObject(forKey: ej2StorageKey)
        UserDefaults.standard.removeObject(forKey: ej4StorageKey)
        UserDefaults.standard.removeObject(forKey: r2StorageKey)
        UserDefaults.standard.removeObject(forKey: r4StorageKey)
        UserDefaults.standard.removeObject(forKey: ej5StorageKey)
        UserDefaults.standard.removeObject(forKey: ej10StorageKey)
        UserDefaults.standard.removeObject(forKey: ej11StorageKey)
        UserDefaults.standard.removeObject(forKey: r1StorageKey)
        UserDefaults.standard.removeObject(forKey: r5StorageKey)
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
        if let r2Data = try? JSONEncoder().encode(Array(r2CompletedSet)) {
            UserDefaults.standard.set(r2Data, forKey: r2StorageKey)
        }
        if let r4Data = try? JSONEncoder().encode(Array(r4CompletedSet)) {
            UserDefaults.standard.set(r4Data, forKey: r4StorageKey)
        }

        if let ej5Data = try? JSONEncoder().encode(Array(ej5CompletedSet)) {
            UserDefaults.standard.set(ej5Data, forKey: ej5StorageKey)
        }

        if let ej10Data = try? JSONEncoder().encode(Array(ej10CompletedSet)) {
            UserDefaults.standard.set(ej10Data, forKey: ej10StorageKey)
        }

        if let ej11Data = try? JSONEncoder().encode(Array(ej11CompletedSet)) {
            UserDefaults.standard.set(ej11Data, forKey: ej11StorageKey)
        }

        if let r1Data = try? JSONEncoder().encode(Array(r1CompletedSet)) {
            UserDefaults.standard.set(r1Data, forKey: r1StorageKey)
        }
        if let r5Data = try? JSONEncoder().encode(Array(r5CompletedSet)) {
            UserDefaults.standard.set(r5Data, forKey: r5StorageKey)
        }

        var sessionData: [String: String] = [
            "exerciseType": lastExerciseType.rawValue,
            "ej1Articulation": String(lastEJ1Articulation.rawValue),
            "ej2Articulation": String(lastEJ2Articulation.rawValue),
            "ej4Articulation": String(lastEJ4Articulation.rawValue),
            "ej4Section": String(lastEJ4Section),
            "r2Articulation": String(lastR2Articulation.rawValue),
            "r2Section": String(lastR2Section),
            "r4Articulation": String(lastR4Articulation.rawValue),
            "r4Section": String(lastR4Section),
            "ej5Articulation": String(lastEJ5Articulation.rawValue),
            "ej5Section": String(lastEJ5Section),
            "ej10Articulation": String(lastEJ10Articulation.rawValue),
            "ej10Section": String(lastEJ10Section),
            "ej11Articulation": String(lastEJ11Articulation.rawValue),
            "ej11Section": String(lastEJ11Section),
            "r1Articulation": String(lastR1Articulation.rawValue),
            "r1Section": String(lastR1Section),
            "r5Articulation": String(lastR5Articulation.rawValue),
            "r5Section": String(lastR5Section)
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
        if let r2Data = UserDefaults.standard.data(forKey: r2StorageKey),
           let decodedR2 = try? JSONDecoder().decode([Int].self, from: r2Data) {
            self.r2CompletedSet = Set(decodedR2)
        }
        if let r4Data = UserDefaults.standard.data(forKey: r4StorageKey),
           let decodedR4 = try? JSONDecoder().decode([Int].self, from: r4Data) {
            self.r4CompletedSet = Set(decodedR4)
        }

        if let ej5Data = UserDefaults.standard.data(forKey: ej5StorageKey),
           let decodedEJ5 = try? JSONDecoder().decode([Int].self, from: ej5Data) {
            self.ej5CompletedSet = Set(decodedEJ5)
        }

        if let ej10Data = UserDefaults.standard.data(forKey: ej10StorageKey),
           let decodedEJ10 = try? JSONDecoder().decode([Int].self, from: ej10Data) {
            self.ej10CompletedSet = Set(decodedEJ10)
        }

        if let ej11Data = UserDefaults.standard.data(forKey: ej11StorageKey),
           let decodedEJ11 = try? JSONDecoder().decode([Int].self, from: ej11Data) {
            self.ej11CompletedSet = Set(decodedEJ11)
        }

        if let r1Data = UserDefaults.standard.data(forKey: r1StorageKey),
           let decodedR1 = try? JSONDecoder().decode([Int].self, from: r1Data) {
            self.r1CompletedSet = Set(decodedR1)
        }
        if let r5Data = UserDefaults.standard.data(forKey: r5StorageKey),
           let decodedR5 = try? JSONDecoder().decode([Int].self, from: r5Data) {
            self.r5CompletedSet = Set(decodedR5)
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
            if let r2ArtStr = sessionData["r2Articulation"], let r2Int = Int(r2ArtStr), let r2Art = EJ4Articulation(rawValue: r2Int) {
                self.lastR2Articulation = r2Art
            }
            if let r2SecStr = sessionData["r2Section"], let r2Sec = Int(r2SecStr) {
                self.lastR2Section = max(0, min(24, r2Sec))
            }
            if let r4ArtStr = sessionData["r4Articulation"], let r4Int = Int(r4ArtStr), let r4Art = EJ4Articulation(rawValue: r4Int) {
                self.lastR4Articulation = r4Art
            }
            if let r4SecStr = sessionData["r4Section"], let r4Sec = Int(r4SecStr) {
                self.lastR4Section = max(0, min(24, r4Sec))
            }
            if let ej5ArtStr = sessionData["ej5Articulation"], let ej5Int = Int(ej5ArtStr), let ej5Art = EJ5Articulation(rawValue: ej5Int) {
                self.lastEJ5Articulation = ej5Art
            }
            if let ej5SecStr = sessionData["ej5Section"], let ej5Sec = Int(ej5SecStr) {
                self.lastEJ5Section = max(0, min(11, ej5Sec))
            }
            if let ej10ArtStr = sessionData["ej10Articulation"], let ej10Int = Int(ej10ArtStr), let ej10Art = EJ5Articulation(rawValue: ej10Int) {
                self.lastEJ10Articulation = ej10Art
            }
            if let ej10SecStr = sessionData["ej10Section"], let ej10Sec = Int(ej10SecStr) {
                self.lastEJ10Section = max(0, min(11, ej10Sec))
            }
            if let ej11ArtStr = sessionData["ej11Articulation"], let ej11Int = Int(ej11ArtStr), let ej11Art = EJ5Articulation(rawValue: ej11Int) {
                self.lastEJ11Articulation = ej11Art
            }
            if let ej11SecStr = sessionData["ej11Section"], let ej11Sec = Int(ej11SecStr) {
                self.lastEJ11Section = max(0, min(11, ej11Sec))
            }
            if let r1ArtStr = sessionData["r1Articulation"], let r1Int = Int(r1ArtStr), let r1Art = EJ5Articulation(rawValue: r1Int) {
                self.lastR1Articulation = r1Art
            }
            if let r1SecStr = sessionData["r1Section"], let r1Sec = Int(r1SecStr) {
                self.lastR1Section = max(0, min(24, r1Sec))
            }
            if let r5ArtStr = sessionData["r5Articulation"], let r5Int = Int(r5ArtStr), let r5Art = EJ5Articulation(rawValue: r5Int) {
                self.lastR5Articulation = r5Art
            }
            if let r5SecStr = sessionData["r5Section"], let r5Sec = Int(r5SecStr) {
                self.lastR5Section = max(0, min(24, r5Sec))
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
