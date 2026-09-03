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
    private let lastSessionKey = "FluteModes_LastSession_v1"

    // Map: "Tonic_Mode" -> Set of completed articulation IDs (1...8)
    @Published public var completedMap: [String: Set<Int>] = [:]

    @Published public var lastTonic: Tonic?
    @Published public var lastMode: ModeType?
    @Published public var lastArticulation: ArticulationPattern?

    public init() {
        loadProgress()
    }

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

        lastTonic = tonic
        lastMode = mode
        lastArticulation = articulation

        saveProgress()
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
        lastTonic = nil
        lastMode = nil
        lastArticulation = nil
        UserDefaults.standard.removeObject(forKey: storageKey)
        UserDefaults.standard.removeObject(forKey: lastSessionKey)
    }

    private func saveProgress() {
        // Convert Set<Int> to Array<Int> for JSON encoding
        let encodable = completedMap.mapValues { Array($0) }
        if let data = try? JSONEncoder().encode(encodable) {
            UserDefaults.standard.set(data, forKey: storageKey)
        }

        if let t = lastTonic, let m = lastMode, let a = lastArticulation {
            let sessionData: [String: String] = [
                "tonic": t.rawValue,
                "mode": String(m.rawValue),
                "articulation": String(a.rawValue)
            ]
            UserDefaults.standard.set(sessionData, forKey: lastSessionKey)
        }
    }

    private func loadProgress() {
        if let data = UserDefaults.standard.data(forKey: storageKey),
           let decoded = try? JSONDecoder().decode([String: [Int]].self, from: data) {
            self.completedMap = decoded.mapValues { Set($0) }
        }

        if let sessionData = UserDefaults.standard.dictionary(forKey: lastSessionKey) as? [String: String] {
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
