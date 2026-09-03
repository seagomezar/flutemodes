import SwiftUI

@main
struct FluteModesApp: App {
    @StateObject private var viewModel = PracticeViewModel()

    var body: some Scene {
        WindowGroup {
            HomeView(viewModel: viewModel)
        }
    }
}
