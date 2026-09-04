import SwiftUI

public struct ProgressMatrixView: View {
    @ObservedObject var viewModel: PracticeViewModel
    @ObservedObject var loc = LocalizationManager.shared
    @Environment(\.dismiss) private var dismiss
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    @State private var filterSelection: FilterOption = .todos
    @State private var showResetConfirmation = false

    private var isCompact: Bool {
        horizontalSizeClass == .compact
    }

    enum FilterOption: String, CaseIterable, Identifiable {
        case todos = "Todos"
        case pendientes = "Pendientes"
        case completados = "Completados"

        var id: String { rawValue }

        var localizedTitle: String {
            let isEn = LocalizationManager.shared.currentLanguage == .english
            switch self {
            case .todos: return isEn ? "All" : "Todos"
            case .pendientes: return isEn ? "Pending" : "Pendientes"
            case .completados: return isEn ? "Completed" : "Completados"
            }
        }
    }

    public init(viewModel: PracticeViewModel) {
        self.viewModel = viewModel
    }

    public var body: some View {
        VStack(spacing: 0) {
            // Top Navigation Bar
            HStack {
                Button {
                    dismiss()
                } label: {
                    HStack(spacing: 6) {
                        Image(systemName: "chevron.left")
                        Text(loc.t("back"))
                    }
                    .foregroundColor(.primary)
                }

                Spacer()

                Text(loc.t("matrix_title"))
                    .font(.headline)

                Spacer()

                Button(role: .destructive) {
                    showResetConfirmation = true
                } label: {
                    HStack(spacing: 4) {
                        Image(systemName: "arrow.counterclockwise")
                        Text(loc.t("reset_all"))
                    }
                    .font(.subheadline)
                }
            }
            .padding(.horizontal, isCompact ? 16 : 24)
            .padding(.vertical, 14)
            .background(Color(uiColor: .secondarySystemBackground))

            Divider()

            ScrollView {
                VStack(spacing: 20) {
                    // Summary KPI Cards
                    kpiSection

                    // Segmented Filter
                    Picker("Filtro", selection: $filterSelection) {
                        ForEach(FilterOption.allCases) { opt in
                            Text(opt.localizedTitle).tag(opt)
                        }
                    }
                    .pickerStyle(.segmented)
                    .padding(.horizontal, isCompact ? 16 : 24)

                    // 12x7 Matrix Table
                    matrixTable

                    // Legend Bar
                    legendBar
                }
                .padding(.vertical, 20)
            }
            .background(Color(uiColor: .systemGroupedBackground))
        }
        .navigationBarBackButtonHidden(true)
        .confirmationDialog(
            loc.t("reset_confirm_title"),
            isPresented: $showResetConfirmation,
            titleVisibility: .visible
        ) {
            Button(loc.t("reset_all"), role: .destructive) {
                viewModel.store.resetAll()
            }
            Button(loc.t("cancel"), role: .cancel) {}
        } message: {
            Text(loc.t("reset_confirm_msg"))
        }
    }

    // MARK: - KPI Section
    private var kpiSection: some View {
        Group {
            if isCompact {
                VStack(spacing: 8) {
                    HStack(spacing: 10) {
                        kpiCard(title: loc.currentLanguage == .english ? "Total Modes" : "Total Modos", value: "\(viewModel.store.totalModesCount)")
                        kpiCard(
                            title: loc.currentLanguage == .english ? "Completed" : "Completados",
                            value: "\(viewModel.store.completedModesCount) / \(viewModel.store.totalModesCount)",
                            subtitle: "\(completionPercentage)%"
                        )
                    }
                    kpiCard(
                        title: loc.currentLanguage == .english ? "Articulations Practiced" : "Articulaciones Practicadas",
                        value: "\(viewModel.store.totalPracticedArticulationsCount) / 672"
                    )
                }
                .padding(.horizontal, 16)
            } else {
                HStack(spacing: 16) {
                    kpiCard(title: loc.currentLanguage == .english ? "Total Modes" : "Total Modos", value: "\(viewModel.store.totalModesCount)")
                    kpiCard(
                        title: loc.currentLanguage == .english ? "Completed" : "Completados",
                        value: "\(viewModel.store.completedModesCount) / \(viewModel.store.totalModesCount)",
                        subtitle: "\(completionPercentage)%"
                    )
                    kpiCard(
                        title: loc.currentLanguage == .english ? "Articulations" : "Articulaciones",
                        value: "\(viewModel.store.totalPracticedArticulationsCount) / 672"
                    )
                }
                .padding(.horizontal, 24)
            }
        }
    }

    private func kpiCard(title: String, value: String, subtitle: String? = nil) -> some View {
        VStack(spacing: 6) {
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
            Text(value)
                .font(.title2.bold())
                .foregroundColor(.primary)
            if let sub = subtitle {
                Text(sub)
                    .font(.caption2.bold())
                    .foregroundColor(.secondary)
            }
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 14)
        .background(Color(uiColor: .secondarySystemGroupedBackground))
        .cornerRadius(14)
        .overlay(
            RoundedRectangle(cornerRadius: 14)
                .stroke(Color(uiColor: .separator), lineWidth: 0.5)
        )
    }

    // MARK: - Matrix Grid
    private var matrixTable: some View {
        ScrollView(.horizontal, showsIndicators: true) {
            VStack(spacing: 0) {
                // Table Header (Mode Column Names)
                HStack(spacing: 0) {
                    Text(loc.currentLanguage == .english ? "Tonic" : "Tónica")
                        .font(.caption.bold())
                        .frame(width: 80, alignment: .leading)
                        .padding(.leading, 12)

                    ForEach(ModeType.allCases) { mode in
                        Text(mode.name.components(separatedBy: " ").first ?? "")
                            .font(.caption.bold())
                            .frame(width: isCompact ? 68 : 80)
                    }
                }
                .padding(.vertical, 12)
                .background(Color(uiColor: .tertiarySystemFill))

                Divider()

                // 12 Rows of Tonics
                ForEach(Tonic.allCases) { tonic in
                    if shouldShowRow(tonic: tonic) {
                        HStack(spacing: 0) {
                            Text(tonic.rawValue)
                                .font(.subheadline.bold())
                                .frame(width: 80, alignment: .leading)
                                .padding(.leading, 12)

                            ForEach(ModeType.allCases) { mode in
                                let count = viewModel.store.completedArticulationsCount(tonic: tonic, mode: mode)
                                Button {
                                    viewModel.selectMode(tonic: tonic, mode: mode)
                                    dismiss()
                                } label: {
                                    cellView(completedCount: count)
                                }
                                .frame(width: isCompact ? 68 : 80)
                            }
                        }
                        .padding(.vertical, 10)

                        Divider()
                    }
                }
            }
            .background(Color(uiColor: .secondarySystemGroupedBackground))
            .cornerRadius(16)
            .overlay(
                RoundedRectangle(cornerRadius: 16)
                    .stroke(Color(uiColor: .separator), lineWidth: 0.5)
            )
            .padding(.horizontal, isCompact ? 16 : 24)
        }
    }

    private func cellView(completedCount: Int) -> some View {
        VStack(spacing: 3) {
            if completedCount == 8 {
                Image(systemName: "checkmark.circle.fill")
                    .font(.system(size: 18))
                    .foregroundColor(.green)
            } else if completedCount > 0 {
                Image(systemName: "circle.circle")
                    .font(.system(size: 18))
                    .foregroundColor(.orange)
            } else {
                Image(systemName: "circle")
                    .font(.system(size: 18))
                    .foregroundColor(.secondary)
            }

            Text("\(completedCount)/8")
                .font(.system(size: 10, weight: .medium, design: .monospaced))
                .foregroundColor(.secondary)
        }
        .frame(height: 38)
    }

    private func shouldShowRow(tonic: Tonic) -> Bool {
        switch filterSelection {
        case .todos:
            return true
        case .pendientes:
            return ModeType.allCases.contains { !viewModel.store.isModeFullyCompleted(tonic: tonic, mode: $0) }
        case .completados:
            return ModeType.allCases.contains { viewModel.store.isModeFullyCompleted(tonic: tonic, mode: $0) }
        }
    }

    // MARK: - Legend Bar
    private var legendBar: some View {
        HStack(spacing: 24) {
            HStack(spacing: 6) {
                Image(systemName: "checkmark.circle.fill")
                    .foregroundColor(.green)
                Text(loc.t("legend_completed"))
                    .font(.caption)
            }

            HStack(spacing: 6) {
                Image(systemName: "circle.circle")
                    .foregroundColor(.orange)
                Text(loc.t("legend_in_progress"))
                    .font(.caption)
            }

            HStack(spacing: 6) {
                Image(systemName: "circle")
                    .foregroundColor(.secondary)
                Text(loc.t("legend_not_started"))
                    .font(.caption)
            }
        }
        .foregroundColor(.secondary)
        .padding(.vertical, 8)
    }

    private var completionPercentage: Int {
        let total = viewModel.store.totalModesCount
        guard total > 0 else { return 0 }
        return Int((Double(viewModel.store.completedModesCount) / Double(total)) * 100)
    }
}
