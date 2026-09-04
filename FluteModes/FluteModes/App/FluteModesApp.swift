import SwiftUI

@main
struct FluteModesApp: App {
    @StateObject private var viewModel = PracticeViewModel()

    init() {
        // Prime audio session immediately on launch for low latency and physical device speaker playback
        AppAudioEngine.shared.configureSession()
    }

    var body: some Scene {
        WindowGroup {
            HomeView(viewModel: viewModel)
        }
    }
}
