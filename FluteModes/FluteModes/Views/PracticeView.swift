import SwiftUI

public struct PracticeView: View {
    @ObservedObject var viewModel: PracticeViewModel
    @ObservedObject var metronome: MetronomeEngine
    @ObservedObject var scorePlayer: ScoreAudioPlayer
    @ObservedObject var loc = LocalizationManager.shared
    @Environment(\.dismiss) private var dismiss

    public init(viewModel: PracticeViewModel) {
        self.viewModel = viewModel
        self.metronome = viewModel.metronome
        self.scorePlayer = viewModel.scorePlayer
    }

    public var body: some View {
        VStack(spacing: 0) {
            // Top Navigation & Mode Information Bar
            topBar

            Divider()

            // Main Sheet Music Area
            ZStack {
                Color(uiColor: .systemBackground)
                    .ignoresSafeArea()

                ScoreWebView(abcString: viewModel.currentAbcScore)
                    .padding(.horizontal, 8)
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)

            Divider()

            // Bottom Articulation Selector Chips
            articulationBar

            Divider()

            // Bottom Integrated Toolbar (Metronome + Actions)
            controlToolbar
        }
        .navigationBarBackButtonHidden(true)
        .background(Color(uiColor: .systemBackground))
        .onAppear {
            viewModel.updateScore()
        }
        .onDisappear {
            scorePlayer.stop()
            metronome.stop()
        }
        .confirmationDialog(
            String(format: loc.t("milestone_title"), viewModel.currentTonic.rawValue),
            isPresented: $viewModel.showCompletionDialog,
            titleVisibility: .visible
        ) {
            Button(loc.t("next_round") + " (\(viewModel.currentTonic.rawValue))") {
                viewModel.startNextArticulationRound()
            }
            Button(String(format: loc.t("advance_tonic"), viewModel.store.nextTonic(after: viewModel.currentTonic).rawValue)) {
                viewModel.advanceToNextTonic()
            }
            Button(loc.t("stay_mode"), role: .cancel) {}
        } message: {
            Text(String(format: loc.t("milestone_msg"), viewModel.currentTonic.rawValue, viewModel.totalArticulationsInCurrentTonic))
        }
    }

    // MARK: - Top Bar
    private var topBar: some View {
        HStack(alignment: .center, spacing: 14) {
            Button {
                dismiss()
            } label: {
                HStack(spacing: 6) {
                    Image(systemName: "chevron.left")
                        .font(.system(size: 16, weight: .semibold))
                    Text("FluteModes")
                        .font(.headline)
                }
                .foregroundColor(.primary)
            }

            Spacer()

            // Mode Details Badge (Parallel System)
            VStack(spacing: 3) {
                HStack(spacing: 8) {
                    Text("\(viewModel.currentTonic.rawValue) \(viewModel.currentMode.name)")
                        .font(.system(size: 18, weight: .bold))
                        .foregroundColor(.primary)

                    Text(viewModel.currentMode.family.rawValue)
                        .font(.caption2.bold())
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(Color(uiColor: .tertiarySystemFill))
                        .cornerRadius(6)

                    // Tonic modes progress badge (e.g. 3/7)
                    Text("\(viewModel.practicedModesCountInCurrentTonic)/7 \(loc.t("modes_count"))")
                        .font(.caption2.bold().monospacedDigit())
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(viewModel.areAllModesInCurrentTonicPracticed ? Color.green.opacity(0.18) : Color.blue.opacity(0.12))
                        .foregroundColor(viewModel.areAllModesInCurrentTonicPracticed ? Color.green : Color.blue)
                        .cornerRadius(6)
                }

                Text("\(viewModel.currentMode.keyDescription(for: viewModel.currentTonic)) | \(viewModel.currentMode.accidentalBadge(for: viewModel.currentTonic))")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            Spacer()

            // Audio Playback of the Score (Piano)
            Button {
                viewModel.toggleScorePlayback()
            } label: {
                HStack(spacing: 6) {
                    Image(systemName: scorePlayer.isPlaying ? "stop.circle.fill" : "pianokeys")
                    Text(scorePlayer.isPlaying ? loc.t("stop_piano") : loc.t("play_piano"))
                        .font(.subheadline.bold())
                }
                .padding(.horizontal, 14)
                .padding(.vertical, 7)
                .background(scorePlayer.isPlaying ? Color.red : Color.indigo)
                .foregroundColor(.white)
                .cornerRadius(16)
                .shadow(color: (scorePlayer.isPlaying ? Color.red : Color.indigo).opacity(0.3), radius: 4, x: 0, y: 2)
            }

            // Metronome Status Pill
            Button {
                metronome.toggle()
            } label: {
                HStack(spacing: 6) {
                    Image(systemName: metronome.isPlaying ? "pause.fill" : "play.fill")
                    Text("d = \(metronome.tempoBPM)")
                        .font(.subheadline.monospacedDigit())
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(metronome.isPlaying ? Color.primary : Color(uiColor: .secondarySystemFill))
                .foregroundColor(metronome.isPlaying ? Color(uiColor: .systemBackground) : .primary)
                .cornerRadius(16)
            }
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 10)
        .background(Color(uiColor: .secondarySystemBackground))
    }

    // MARK: - Articulation Bar
    private var articulationBar: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                ForEach(ArticulationPattern.allCases) { pattern in
                    let isCurrent = viewModel.currentArticulation == pattern
                    let isDone = viewModel.store.isCompleted(
                        tonic: viewModel.currentTonic,
                        mode: viewModel.currentMode,
                        articulation: pattern
                    )

                    Button {
                        viewModel.selectArticulation(pattern)
                    } label: {
                        HStack(spacing: 6) {
                            if isDone {
                                Image(systemName: "checkmark")
                                    .font(.system(size: 11, weight: .bold))
                                    .foregroundColor(isCurrent ? Color(uiColor: .systemBackground) : .secondary)
                            }
                            Text(pattern.shortTitle)
                                .font(.system(size: 13, weight: isCurrent ? .semibold : .regular))
                        }
                        .padding(.horizontal, 14)
                        .padding(.vertical, 8)
                        .background(isCurrent ? Color.primary : Color(uiColor: .secondarySystemGroupedBackground))
                        .foregroundColor(isCurrent ? Color(uiColor: .systemBackground) : .primary)
                        .cornerRadius(16)
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(isCurrent ? Color.clear : Color(uiColor: .separator), lineWidth: 1)
                        )
                    }
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 10)
        }
        .background(Color(uiColor: .systemGroupedBackground))
    }

    // MARK: - Control Toolbar
    private var controlToolbar: some View {
        HStack(spacing: 20) {
            // Metronome Play / Pause
            Button {
                metronome.toggle()
            } label: {
                Image(systemName: metronome.isPlaying ? "pause.circle.fill" : "play.circle.fill")
                    .font(.system(size: 38))
                    .foregroundColor(.primary)
            }

            // 4 Visual Beat Indicators
            HStack(spacing: 8) {
                ForEach(1...4, id: \.self) { beat in
                    Circle()
                        .fill(metronome.isPlaying && metronome.currentBeat == beat ? Color.primary : Color(uiColor: .tertiaryLabel))
                        .frame(width: 10, height: 10)
                        .scaleEffect(metronome.isPlaying && metronome.currentBeat == beat ? 1.4 : 1.0)
                        .animation(.easeInOut(duration: 0.1), value: metronome.currentBeat)
                }
            }

            // BPM Stepper
            HStack(spacing: 8) {
                Button {
                    metronome.setTempo(metronome.tempoBPM - 2)
                    viewModel.updateScore()
                } label: {
                    Image(systemName: "minus")
                        .font(.system(size: 14, weight: .bold))
                        .frame(width: 32, height: 32)
                        .background(Color(uiColor: .tertiarySystemFill))
                        .cornerRadius(8)
                }

                Text("\(metronome.tempoBPM) BPM")
                    .font(.subheadline.bold().monospacedDigit())
                    .frame(minWidth: 70)

                Button {
                    metronome.setTempo(metronome.tempoBPM + 2)
                    viewModel.updateScore()
                } label: {
                    Image(systemName: "plus")
                        .font(.system(size: 14, weight: .bold))
                        .frame(width: 32, height: 32)
                        .background(Color(uiColor: .tertiarySystemFill))
                        .cornerRadius(8)
                }
            }
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(Color(uiColor: .secondarySystemGroupedBackground))
            .cornerRadius(12)

            Spacer()

            // Next Articulation in Current Mode
            Button {
                let all = ArticulationPattern.allCases
                if let idx = all.firstIndex(of: viewModel.currentArticulation) {
                    let nextIdx = (idx + 1) % all.count
                    viewModel.selectArticulation(all[nextIdx])
                }
            } label: {
                Text(loc.t("next_art"))
                    .font(.subheadline.bold())
                    .padding(.horizontal, 16)
                    .padding(.vertical, 12)
                    .background(Color(uiColor: .secondarySystemFill))
                    .foregroundColor(.primary)
                    .cornerRadius(20)
            }

            // Main Pedagogical Action Button
            if viewModel.areAllModesInCurrentTonicPracticed {
                // Milestone: All 7 modes in this tonic practiced!
                Button {
                    viewModel.showCompletionDialog = true
                } label: {
                    HStack(spacing: 8) {
                        Image(systemName: "checkmark.seal.fill")
                            .font(.system(size: 16))
                        Text("✓ \(loc.t("seven_modes_completed")) (\(viewModel.currentTonic.rawValue))")
                            .font(.subheadline.bold())
                    }
                    .padding(.horizontal, 20)
                    .padding(.vertical, 12)
                    .background(Color.green)
                    .foregroundColor(.white)
                    .cornerRadius(20)
                    .shadow(color: Color.green.opacity(0.35), radius: 6, x: 0, y: 3)
                }
            } else {
                // Standard: Advance to next mode within current tonic
                Button {
                    viewModel.markCurrentCompletedAndAdvanceMode()
                } label: {
                    HStack(spacing: 8) {
                        Text("\(loc.t("complete_and_next")) (\(viewModel.practicedModesCountInCurrentTonic)/7)")
                            .font(.subheadline.bold())
                        Image(systemName: "arrow.right")
                    }
                    .padding(.horizontal, 20)
                    .padding(.vertical, 12)
                    .background(Color.primary)
                    .foregroundColor(Color(uiColor: .systemBackground))
                    .cornerRadius(20)
                }
            }
        }
        .padding(.horizontal, 24)
        .padding(.vertical, 12)
        .background(Color(uiColor: .secondarySystemBackground))
    }
}
