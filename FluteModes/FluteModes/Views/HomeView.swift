import SwiftUI

public struct HomeView: View {
    @ObservedObject var viewModel: PracticeViewModel
    @ObservedObject var loc = LocalizationManager.shared
    @State private var navigateToPractice = false
    @State private var navigateToMatrix = false

    public init(viewModel: PracticeViewModel) {
        self.viewModel = viewModel
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                Color(uiColor: .systemGroupedBackground)
                    .ignoresSafeArea()

                ScrollView {
                    VStack(spacing: 24) {
                        // Top Bar with Language Switcher
                        HStack {
                            Spacer()
                            Button {
                                loc.toggleLanguage()
                            } label: {
                                HStack(spacing: 6) {
                                    Text(loc.currentLanguage.flag)
                                    Text(loc.currentLanguage.displayName)
                                        .font(.subheadline.bold())
                                    Image(systemName: "chevron.up.chevron.down")
                                        .font(.caption2)
                                }
                                .padding(.horizontal, 12)
                                .padding(.vertical, 6)
                                .background(Color(uiColor: .tertiarySystemFill))
                                .foregroundColor(.primary)
                                .cornerRadius(14)
                            }
                        }
                        .padding(.horizontal, 4)
                        .padding(.top, 8)

                        // Header / Hero
                        VStack(spacing: 6) {
                            Text(loc.t("app_name"))
                                .font(.system(size: 32, weight: .bold))
                                .foregroundColor(.primary)

                            Text(loc.t("subtitle"))
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }

                        // SELECT TONIC (Horizontal Chip Bar)
                        VStack(alignment: .leading, spacing: 10) {
                            Text(loc.t("select_tonic").uppercased())
                                .font(.caption.bold())
                                .foregroundColor(.secondary)
                                .padding(.horizontal, 4)

                            ScrollView(.horizontal, showsIndicators: false) {
                                HStack(spacing: 8) {
                                    ForEach(Tonic.allCases) { tonic in
                                        let isSelected = viewModel.currentTonic == tonic
                                        Button {
                                            viewModel.selectMode(tonic: tonic, mode: viewModel.currentMode)
                                        } label: {
                                            Text(tonic.rawValue)
                                                .font(.system(size: 14, weight: isSelected ? .bold : .medium))
                                                .padding(.horizontal, 16)
                                                .padding(.vertical, 8)
                                                .background(isSelected ? Color.primary : Color(uiColor: .secondarySystemGroupedBackground))
                                                .foregroundColor(isSelected ? Color(uiColor: .systemBackground) : .primary)
                                                .cornerRadius(18)
                                                .overlay(
                                                    RoundedRectangle(cornerRadius: 18)
                                                        .stroke(isSelected ? Color.clear : Color(uiColor: .separator), lineWidth: 1)
                                                )
                                        }
                                    }
                                }
                            }
                        }

                        // TWO PARALLEL FAMILIES (Mayor & Menor)
                        HStack(alignment: .top, spacing: 16) {
                            // Familia Mayor Card
                            familyCard(
                                title: loc.t("major_family"),
                                keyDesc: "\(loc.t("fixed_key")) \(viewModel.currentTonic.majorKey) (\(viewModel.currentTonic.majorDesc))",
                                modes: [.ionian, .lydian, .mixolydian]
                            )

                            // Familia Menor Card
                            familyCard(
                                title: loc.t("minor_family"),
                                keyDesc: "\(loc.t("fixed_key")) \(viewModel.currentTonic.minorKey) (\(viewModel.currentTonic.minorDesc))",
                                modes: [.dorian, .aeolian, .phrygian, .locrian]
                            )
                        }

                        // Actions Section
                        VStack(spacing: 12) {
                            Button {
                                viewModel.suggestNextExercise()
                                navigateToPractice = true
                            } label: {
                                HStack(spacing: 10) {
                                    Image(systemName: "play.fill")
                                    Text("\(loc.t("start_practice")) (\(viewModel.currentTonic.rawValue))")
                                        .font(.headline)
                                }
                                .foregroundColor(Color(uiColor: .systemBackground))
                                .frame(maxWidth: .infinity)
                                .frame(height: 52)
                                .background(Color.primary)
                                .cornerRadius(26)
                            }

                            Button {
                                navigateToMatrix = true
                            } label: {
                                HStack {
                                    Image(systemName: "square.grid.3x3.fill")
                                    Text(loc.t("practice_matrix"))
                                        .font(.headline)
                                }
                                .foregroundColor(.primary)
                                .frame(maxWidth: .infinity)
                                .frame(height: 50)
                                .background(Color(uiColor: .secondarySystemGroupedBackground))
                                .cornerRadius(25)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 25)
                                        .stroke(Color(uiColor: .separator), lineWidth: 1)
                                )
                            }
                        }

                        // Quick Metronome Settings Card
                        VStack(spacing: 0) {
                            HStack {
                                Label("Metrónomo (Blanca)", systemImage: "metronome")
                                Spacer()
                                Stepper("\(viewModel.metronome.tempoBPM) BPM", value: Binding(
                                    get: { viewModel.metronome.tempoBPM },
                                    set: { viewModel.metronome.setTempo($0) }
                                ), in: 40...160, step: 2)
                            }
                            .padding(.horizontal, 16)
                            .padding(.vertical, 12)

                            Divider()

                            HStack {
                                Label("Sonido de Clic", systemImage: viewModel.metronome.isAudioMuted ? "speaker.slash.fill" : "speaker.wave.2.fill")
                                Spacer()
                                Toggle("", isOn: Binding(
                                    get: { !viewModel.metronome.isAudioMuted },
                                    set: { viewModel.metronome.isAudioMuted = !$0 }
                                ))
                                .labelsHidden()
                            }
                            .padding(.horizontal, 16)
                            .padding(.vertical, 12)
                        }
                        .background(Color(uiColor: .secondarySystemGroupedBackground))
                        .cornerRadius(16)
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(Color(uiColor: .separator), lineWidth: 0.5)
                        )
                    }
                    .padding(.horizontal, 28)
                    .padding(.bottom, 24)
                }
            }
            .navigationDestination(isPresented: $navigateToPractice) {
                PracticeView(viewModel: viewModel)
            }
            .navigationDestination(isPresented: $navigateToMatrix) {
                ProgressMatrixView(viewModel: viewModel)
            }
        }
    }

    private func familyCard(title: String, keyDesc: String, modes: [ModeType]) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.title3.bold())
                    .foregroundColor(.primary)
                Text(keyDesc)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
            }

            VStack(spacing: 0) {
                ForEach(modes) { mode in
                    let isFullyDone = viewModel.store.isModeFullyCompleted(tonic: viewModel.currentTonic, mode: mode)
                    let count = viewModel.store.completedArticulationsCount(tonic: viewModel.currentTonic, mode: mode)

                    Button {
                        viewModel.selectMode(tonic: viewModel.currentTonic, mode: mode)
                        navigateToPractice = true
                    } label: {
                        HStack(spacing: 12) {
                            VStack(alignment: .leading, spacing: 2) {
                                Text("\(mode.rawValue). \(mode.name)")
                                    .font(.subheadline.bold())
                                    .foregroundColor(.primary)
                                Text(mode.accidentalBadge(for: viewModel.currentTonic))
                                    .font(.caption2)
                                    .foregroundColor(.secondary)
                            }

                            Spacer()

                            if isFullyDone {
                                Image(systemName: "checkmark.circle.fill")
                                    .foregroundColor(.green)
                            } else if count > 0 {
                                Text("\(count)/8")
                                    .font(.caption2.bold().monospacedDigit())
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.orange.opacity(0.15))
                                    .foregroundColor(.orange)
                                    .cornerRadius(6)
                            } else {
                                Image(systemName: "circle")
                                    .foregroundColor(.secondary)
                            }
                        }
                        .padding(.vertical, 10)
                        .padding(.horizontal, 12)
                    }

                    if mode.id != modes.last?.id {
                        Divider()
                    }
                }
            }
            .background(Color(uiColor: .systemBackground))
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color(uiColor: .separator), lineWidth: 0.5)
            )
        }
        .padding(16)
        .frame(maxWidth: .infinity)
        .background(Color(uiColor: .secondarySystemGroupedBackground))
        .cornerRadius(16)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(Color(uiColor: .separator), lineWidth: 0.5)
        )
    }
}
