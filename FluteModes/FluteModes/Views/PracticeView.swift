import SwiftUI

public struct PracticeView: View {
    @ObservedObject var viewModel: PracticeViewModel
    @ObservedObject var metronome: MetronomeEngine
    @ObservedObject var scorePlayer: ScoreAudioPlayer
    @ObservedObject var loc = LocalizationManager.shared
    @Environment(\.dismiss) private var dismiss
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass
    @State private var navigateToMatrix = false

    private var isCompact: Bool {
        horizontalSizeClass == .compact
    }

    public init(viewModel: PracticeViewModel) {
        self.viewModel = viewModel
        self.metronome = viewModel.metronome
        self.scorePlayer = viewModel.scorePlayer
    }

    public var body: some View {
        VStack(spacing: 0) {
            // Top Navigation & Mode Information Bar
            if isCompact {
                mobileTopBar
                mobileModeHeaderCard
            } else {
                topBar
            }

            Divider()

            // Main Sheet Music Area
            ZStack {
                Color(uiColor: .systemBackground)
                    .ignoresSafeArea()

                ScoreWebView(
                    abcString: viewModel.currentAbcScore,
                    highlightedNoteIndex: scorePlayer.currentNoteIndex
                )
                    .padding(isCompact ? 4 : 12)
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)

            Divider()

            // Bottom Articulation Selector Chips
            articulationBar

            Divider()

            // Bottom Integrated Toolbar (Metronome + Actions)
            if isCompact {
                mobileControlToolbar
            } else {
                controlToolbar
            }
        }
        .navigationBarBackButtonHidden(true)
        .background(Color(uiColor: .systemBackground))
        .navigationDestination(isPresented: $navigateToMatrix) {
            ProgressMatrixView(viewModel: viewModel)
        }
        .onAppear {
            viewModel.updateScore()
            if viewModel.keepScreenAwake {
                UIApplication.shared.isIdleTimerDisabled = true
            }
        }
        .onChange(of: viewModel.keepScreenAwake) { isAwake in
            UIApplication.shared.isIdleTimerDisabled = isAwake
        }
        .onDisappear {
            scorePlayer.stop()
            metronome.stop()
            UIApplication.shared.isIdleTimerDisabled = false
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
        .confirmationDialog(
            loc.t("ej1_milestone_title"),
            isPresented: $viewModel.showEJ1CompletionDialog,
            titleVisibility: .visible
        ) {
            Button(loc.t("ej1_restart_round")) {
                viewModel.restartEJ1Round()
            }
            Button(loc.t("ej1_go_to_ej2")) {
                viewModel.selectExercise(.ej2)
            }
            Button(loc.t("ej1_go_to_ej4")) {
                viewModel.selectExercise(.ej4)
            }
            Button(loc.t("stay_mode"), role: .cancel) {}
        } message: {
            Text(loc.t("ej1_milestone_msg"))
        }
        .confirmationDialog(
            loc.t("ej2_milestone_title"),
            isPresented: $viewModel.showEJ2CompletionDialog,
            titleVisibility: .visible
        ) {
            Button(loc.t("ej2_restart_round")) {
                viewModel.restartEJ2Round()
            }
            Button(loc.t("ej2_go_to_ej4")) {
                viewModel.selectExercise(.ej4)
            }
            Button(loc.t("stay_mode"), role: .cancel) {}
        } message: {
            Text(loc.t("ej2_milestone_msg"))
        }
        .confirmationDialog(
            "¡\(viewModel.currentExercise.pillLabel) Completado (8/8 Articulaciones)!",
            isPresented: $viewModel.showEJ4CompletionDialog,
            titleVisibility: .visible
        ) {
            Button(loc.t("ej4_restart_round")) {
                viewModel.restartEJ4Round()
            }
            Button("🎵 Siguiente Tonalidad (\( (viewModel.currentEJ4TypeSectionIndex + 1) % 25 + 1 )/25)") {
                viewModel.advanceToNextEJ4Section()
            }
            Button(loc.t("ej4_go_to_modos")) {
                viewModel.selectExercise(.modos)
            }
            Button(loc.t("stay_mode"), role: .cancel) {}
        } message: {
            Text("Has completado las 8 articulaciones de \(viewModel.currentExercise.pillLabel).")
        }
        .confirmationDialog(
            "¡\(viewModel.currentExercise.pillLabel) Completado (10/10 Articulaciones)!",
            isPresented: $viewModel.showEJ5TypeCompletionDialog,
            titleVisibility: .visible
        ) {
            let secTotal = viewModel.currentExercise.sectionCount
            Button("🔁 Volver a Articulación 1") {
                viewModel.restartEJ5TypeRound()
            }
            Button("🎵 Siguiente Sección (\( (viewModel.currentEJ5TypeSectionIndex + 1) % secTotal + 1 )/\(secTotal))") {
                viewModel.advanceToNextEJ5TypeSection()
            }
            Button(loc.t("stay_mode"), role: .cancel) {}
        } message: {
            Text("Has completado las 10 articulaciones de \(viewModel.currentExercise.pillLabel).")
        }
    }

    // MARK: - Mobile Top Navigation Bar
    private var mobileTopBar: some View {
        HStack(alignment: .center, spacing: 6) {
            Button {
                dismiss()
            } label: {
                HStack(spacing: 4) {
                    Image(systemName: "chevron.left")
                        .font(.system(size: 15, weight: .semibold))
                    Text("Inicio")
                        .font(.subheadline.bold())
                }
                .foregroundColor(.primary)
            }

            // Exercise quick switcher (Horizontal Scroll for exercises)
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 2) {
                    ForEach(ExerciseType.allCases) { ex in
                        let isSel = viewModel.currentExercise == ex
                        Button {
                            viewModel.selectExercise(ex)
                        } label: {
                            Text(ex.pillLabel)
                                .font(.system(size: 11, weight: .bold))
                                .padding(.horizontal, 7)
                                .padding(.vertical, 5)
                                .background(isSel ? Color.primary : Color.clear)
                                .foregroundColor(isSel ? Color(uiColor: .systemBackground) : .primary)
                                .cornerRadius(8)
                        }
                    }
                }
                .padding(2)
                .background(Color(uiColor: .tertiarySystemFill))
                .cornerRadius(10)
            }

            if viewModel.currentExercise == .modos {
                Button {
                    navigateToMatrix = true
                } label: {
                    Image(systemName: "square.grid.3x3.fill")
                        .font(.caption)
                        .padding(7)
                        .background(Color(uiColor: .tertiarySystemFill))
                        .foregroundColor(.primary)
                        .clipShape(Circle())
                }
            }

            Button {
                loc.toggleLanguage()
            } label: {
                Text(loc.currentLanguage.flag)
                    .font(.subheadline)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 5)
                    .background(Color(uiColor: .tertiarySystemFill))
                    .cornerRadius(10)
            }
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
        .background(Color(uiColor: .secondarySystemBackground))
    }

    // MARK: - Mobile Mode Header Card
    @ViewBuilder
    private var mobileModeHeaderCard: some View {
        if viewModel.currentExercise.isChromaticExercise {
            let isEj2 = viewModel.currentExercise == .ej2
            let completed = viewModel.store.chromaticCompletedCount(for: viewModel.currentExercise)
            let isAllDone = viewModel.store.isChromaticFullyCompleted(for: viewModel.currentExercise)
            let currentArt = viewModel.currentChromaticArticulation

            VStack(spacing: 6) {
                HStack(alignment: .firstTextBaseline) {
                    VStack(alignment: .leading, spacing: 2) {
                        Text("\(viewModel.currentExercise.pillLabel) · \(currentArt.title)")
                            .font(.system(size: 17, weight: .bold))
                            .foregroundColor(.primary)
                            .lineLimit(1)

                        Text(loc.t(isEj2 ? "ej2_header_info" : "ej1_header_info"))
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }

                    Spacer()

                    Text("\(completed)/10 \(loc.t("arts_count"))")
                        .font(.caption2.bold().monospacedDigit())
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(isAllDone ? Color.green.opacity(0.18) : Color.blue.opacity(0.12))
                        .foregroundColor(isAllDone ? Color.green : Color.blue)
                        .cornerRadius(8)
                }

                HStack(spacing: 6) {
                    Text("A. L. 16.588")
                        .font(.caption2.bold())
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(Color(uiColor: .tertiarySystemFill))
                        .foregroundColor(.secondary)
                        .cornerRadius(6)

                    Text(currentArt.formulaBadge)
                        .font(.caption2.weight(.medium).monospaced())
                        .foregroundColor(.secondary)

                    Spacer()
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 10)
            .background(Color(uiColor: .systemBackground))
        } else if viewModel.currentExercise.isEJ4Exercise {
            let ex = viewModel.currentExercise
            let completed = viewModel.store.ej4TypeCompletedCount(for: ex)
            let isAllDone = viewModel.store.isEJ4TypeFullyCompleted(for: ex)
            let currentArt = viewModel.currentEJ4TypeArticulation
            let curSecIdx = viewModel.currentEJ4TypeSectionIndex
            let curSec = EJ4Section.all[max(0, min(24, curSecIdx))]

            VStack(spacing: 6) {
                HStack(alignment: .firstTextBaseline) {
                    VStack(alignment: .leading, spacing: 2) {
                        Text("\(ex.pillLabel) · \(curSec.fullName(for: ex))")
                            .font(.system(size: 16, weight: .bold))
                            .foregroundColor(.primary)
                            .lineLimit(1)

                        Text("\(currentArt.title) · \(curSec.measureRange(for: ex))")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .lineLimit(1)
                    }

                    Spacer()

                    Text("\(completed)/8 \(loc.t("arts_count"))")
                        .font(.caption2.bold().monospacedDigit())
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(isAllDone ? Color.green.opacity(0.18) : Color.blue.opacity(0.12))
                        .foregroundColor(isAllDone ? Color.green : Color.blue)
                        .cornerRadius(8)
                }

                // Horizontal Section Selector Bar (25 Keys)
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 6) {
                        ForEach(EJ4Section.all) { sec in
                            let isSel = curSecIdx == sec.id
                            Button {
                                viewModel.selectEJ4Section(sec.id, for: ex)
                            } label: {
                                Text("\(sec.shortName(for: ex)) (\(sec.measureRange(for: ex)))")
                                    .font(.system(size: 11, weight: isSel ? .bold : .medium))
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 5)
                                    .background(isSel ? Color.blue : Color(uiColor: .tertiarySystemFill))
                                    .foregroundColor(isSel ? .white : .primary)
                                    .cornerRadius(10)
                            }
                        }
                    }
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 8)
            .background(Color(uiColor: .systemBackground))
        } else if viewModel.currentExercise.isEJ5TypeExercise {
            let ex = viewModel.currentExercise
            let completed = viewModel.store.ej5TypeCompletedCount(for: ex)
            let isAllDone = viewModel.store.isEJ5TypeFullyCompleted(for: ex)
            let currentArt = viewModel.currentEJ5TypeArticulation
            let curSecIdx = viewModel.currentEJ5TypeSectionIndex
            let fullName = ex.isReichertExercise
                ? EJ4Section.all[max(0, min(24, curSecIdx))].fullName(for: ex)
                : (ex == .ej5 ? EJ5Section.all[curSecIdx].fullName : EJ10Section.all[curSecIdx].fullName)
            let mRange = ex.isReichertExercise
                ? EJ4Section.all[max(0, min(24, curSecIdx))].measureRange(for: ex)
                : (ex == .ej5 ? EJ5Section.all[curSecIdx].measureRange : EJ10Section.all[curSecIdx].measureRange)

            VStack(spacing: 6) {
                HStack(alignment: .firstTextBaseline) {
                    VStack(alignment: .leading, spacing: 2) {
                        Text("\(ex.pillLabel) · \(fullName)")
                            .font(.system(size: 16, weight: .bold))
                            .foregroundColor(.primary)
                            .lineLimit(1)

                        Text("\(currentArt.title(for: ex)) · \(mRange)")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .lineLimit(1)
                    }

                    Spacer()

                    Text("\(completed)/10 \(loc.t("arts_count"))")
                        .font(.caption2.bold().monospacedDigit())
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(isAllDone ? Color.green.opacity(0.18) : Color.blue.opacity(0.12))
                        .foregroundColor(isAllDone ? Color.green : Color.blue)
                        .cornerRadius(8)
                }

                // Horizontal Section Selector Bar
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 6) {
                        ForEach(0..<ex.sectionCount, id: \.self) { idx in
                            let isSel = curSecIdx == idx
                            let shortName = ex.isReichertExercise
                                ? EJ4Section.all[idx].shortName(for: ex)
                                : (ex == .ej5 ? EJ5Section.all[idx].shortName : EJ10Section.all[idx].shortName)
                            let rangeStr = ex.isReichertExercise
                                ? EJ4Section.all[idx].measureRange(for: ex)
                                : (ex == .ej5 ? EJ5Section.all[idx].measureRange : EJ10Section.all[idx].measureRange)
                            Button {
                                viewModel.selectEJ5TypeSection(idx)
                            } label: {
                                Text("\(shortName) (\(rangeStr))")
                                    .font(.system(size: 11, weight: isSel ? .bold : .medium))
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 5)
                                    .background(isSel ? Color.blue : Color(uiColor: .tertiarySystemFill))
                                    .foregroundColor(isSel ? .white : .primary)
                                    .cornerRadius(10)
                            }
                        }
                    }
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 8)
            .background(Color(uiColor: .systemBackground))
        } else {
            VStack(spacing: 6) {
                HStack(alignment: .firstTextBaseline) {
                    VStack(alignment: .leading, spacing: 2) {
                        Text("\(viewModel.currentTonic.rawValue) · \(viewModel.currentMode.name)")
                            .font(.system(size: 19, weight: .bold))
                            .foregroundColor(.primary)

                        Text(viewModel.currentMode.keyDescription(for: viewModel.currentTonic))
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }

                    Spacer()

                    Text("\(viewModel.practicedModesCountInCurrentTonic)/7 \(loc.t("modes_count"))")
                        .font(.caption2.bold().monospacedDigit())
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(viewModel.areAllModesInCurrentTonicPracticed ? Color.green.opacity(0.18) : Color.blue.opacity(0.12))
                        .foregroundColor(viewModel.areAllModesInCurrentTonicPracticed ? Color.green : Color.blue)
                        .cornerRadius(8)
                }

                HStack(spacing: 6) {
                    Text(viewModel.currentMode.family.rawValue)
                        .font(.caption2.bold())
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(Color(uiColor: .tertiarySystemFill))
                        .foregroundColor(.secondary)
                        .cornerRadius(6)

                    Text(viewModel.currentMode.accidentalBadge(for: viewModel.currentTonic))
                        .font(.caption2.weight(.medium))
                        .foregroundColor(.secondary)

                    Spacer()
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 10)
            .background(Color(uiColor: .systemBackground))
        }
    }

    // MARK: - Top Bar (Tablet)
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

            // Exercise Switcher Pill
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 2) {
                    ForEach(ExerciseType.allCases) { ex in
                        let isSel = viewModel.currentExercise == ex
                        Button {
                            viewModel.selectExercise(ex)
                        } label: {
                            Text(ex.pillLabel)
                                .font(.caption.bold())
                                .padding(.horizontal, 9)
                                .padding(.vertical, 5)
                                .background(isSel ? Color.primary : Color.clear)
                                .foregroundColor(isSel ? Color(uiColor: .systemBackground) : .primary)
                                .cornerRadius(8)
                        }
                    }
                }
                .padding(2)
                .background(Color(uiColor: .tertiarySystemFill))
                .cornerRadius(10)
            }

            Spacer()

            if viewModel.currentExercise.isChromaticExercise {
                let isEj2 = viewModel.currentExercise == .ej2
                let completed = viewModel.store.chromaticCompletedCount(for: viewModel.currentExercise)
                let isAllDone = viewModel.store.isChromaticFullyCompleted(for: viewModel.currentExercise)
                let currentArt = viewModel.currentChromaticArticulation

                VStack(spacing: 3) {
                    HStack(spacing: 8) {
                        Text("\(viewModel.currentExercise.pillLabel) · \(currentArt.title)")
                            .font(.system(size: 18, weight: .bold))
                            .foregroundColor(.primary)

                        Text("A. L. 16.588")
                            .font(.caption2.bold())
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(Color(uiColor: .tertiarySystemFill))
                            .cornerRadius(6)

                        Text("\(completed)/10 \(loc.t("arts_count"))")
                            .font(.caption2.bold().monospacedDigit())
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(isAllDone ? Color.green.opacity(0.18) : Color.blue.opacity(0.12))
                            .foregroundColor(isAllDone ? Color.green : Color.blue)
                            .cornerRadius(6)
                    }

                    Text("\(loc.t(isEj2 ? "ej2_header_info" : "ej1_header_info")) | \(currentArt.formulaBadge)")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            } else if viewModel.currentExercise.isEJ4Exercise {
                let ex = viewModel.currentExercise
                let completed = viewModel.store.ej4TypeCompletedCount(for: ex)
                let isAllDone = viewModel.store.isEJ4TypeFullyCompleted(for: ex)
                let currentArt = viewModel.currentEJ4TypeArticulation
                let curSecIdx = viewModel.currentEJ4TypeSectionIndex
                let curSec = EJ4Section.all[max(0, min(24, curSecIdx))]
                let totalMeas = ex == .r2 ? "200" : (ex == .r4 ? "100" : "194")
                let plateLabel = ex.isReichertExercise ? "Schott 20623" : "A. L. 16.588"

                VStack(spacing: 3) {
                    HStack(spacing: 8) {
                        Text("\(ex.pillLabel) · \(curSec.fullName(for: ex))")
                            .font(.system(size: 18, weight: .bold))
                            .foregroundColor(.primary)

                        Text(plateLabel)
                            .font(.caption2.bold())
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(Color(uiColor: .tertiarySystemFill))
                            .cornerRadius(6)

                        Text("\(completed)/8 \(loc.t("arts_count"))")
                            .font(.caption2.bold().monospacedDigit())
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(isAllDone ? Color.green.opacity(0.18) : Color.blue.opacity(0.12))
                            .foregroundColor(isAllDone ? Color.green : Color.blue)
                            .cornerRadius(6)
                    }

                    Text("\(currentArt.title) | \(curSec.measureRange(for: ex)) de \(totalMeas)")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            } else if viewModel.currentExercise.isEJ5TypeExercise {
                let ex = viewModel.currentExercise
                let completed = viewModel.store.ej5TypeCompletedCount(for: ex)
                let isAllDone = viewModel.store.isEJ5TypeFullyCompleted(for: ex)
                let currentArt = viewModel.currentEJ5TypeArticulation
                let curSecIdx = viewModel.currentEJ5TypeSectionIndex
                let fullName = ex.isReichertExercise
                    ? EJ4Section.all[max(0, min(24, curSecIdx))].fullName(for: ex)
                    : (ex == .ej5 ? EJ5Section.all[curSecIdx].fullName : EJ10Section.all[curSecIdx].fullName)
                let mRange = ex.isReichertExercise
                    ? EJ4Section.all[max(0, min(24, curSecIdx))].measureRange(for: ex)
                    : (ex == .ej5 ? EJ5Section.all[curSecIdx].measureRange : EJ10Section.all[curSecIdx].measureRange)
                let totalMeas = ex == .r1 ? "100" : (ex == .r5 ? "200" : (ex == .ej5 ? "60" : "121"))
                let plateLabel = ex.isReichertExercise ? "Schott 20623" : "A. L. 16.588"

                VStack(spacing: 3) {
                    HStack(spacing: 8) {
                        Text("\(ex.pillLabel) · \(fullName)")
                            .font(.system(size: 17, weight: .bold))
                            .foregroundColor(.primary)
                            .lineLimit(1)

                        Text(plateLabel)
                            .font(.caption2.bold())
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(Color(uiColor: .tertiarySystemFill))
                            .cornerRadius(6)

                        Text("\(completed)/10 \(loc.t("arts_count"))")
                            .font(.caption2.bold().monospacedDigit())
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(isAllDone ? Color.green.opacity(0.18) : Color.blue.opacity(0.12))
                            .foregroundColor(isAllDone ? Color.green : Color.blue)
                            .cornerRadius(6)
                    }

                    Text("\(currentArt.title(for: ex)) | \(mRange) de \(totalMeas)")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            } else {
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
    @ViewBuilder
    private var articulationBar: some View {
        if viewModel.currentExercise.isChromaticExercise {
            let ex = viewModel.currentExercise
            let completedCount = viewModel.store.chromaticCompletedCount(for: ex)
            let isAllDone = viewModel.store.isChromaticFullyCompleted(for: ex)

            VStack(spacing: 6) {
                HStack {
                    HStack(spacing: 6) {
                        Text(loc.t("articulations_title"))
                            .font(.caption.bold())
                            .foregroundColor(.primary)

                        if isAllDone {
                            Image(systemName: "checkmark.seal.fill")
                                .font(.system(size: 12))
                                .foregroundColor(.green)
                        }
                    }

                    Spacer()

                    Text("\(completedCount)/10 " + loc.t("arts_count"))
                        .font(.caption.bold().monospacedDigit())
                        .padding(.horizontal, 8)
                        .padding(.vertical, 3)
                        .background(isAllDone ? Color.green.opacity(0.18) : (completedCount > 0 ? Color.orange.opacity(0.15) : Color(uiColor: .tertiarySystemFill)))
                        .foregroundColor(isAllDone ? .green : (completedCount > 0 ? .orange : .secondary))
                        .cornerRadius(8)
                }
                .padding(.horizontal, 16)
                .padding(.top, 4)

                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(EJ1Articulation.allCases) { art in
                            let isCurrent = viewModel.currentChromaticArticulation == art
                            let isDone = viewModel.store.isChromaticCompleted(art, for: ex)

                            Button {
                                if isCurrent {
                                    if art != .original {
                                        _ = viewModel.store.toggleChromaticCompleted(art, for: ex)
                                    }
                                } else {
                                    viewModel.selectChromaticArticulation(art, markPreviousCompleted: true)
                                }
                            } label: {
                                HStack(spacing: 6) {
                                    if art == .original {
                                        Image(systemName: "book.pages.fill")
                                            .font(.system(size: 12, weight: .bold))
                                            .foregroundColor(isCurrent ? Color(uiColor: .systemBackground) : .indigo)
                                    } else {
                                        Image(systemName: isDone ? "checkmark.circle.fill" : (isCurrent ? "circle" : "circle.dashed"))
                                            .font(.system(size: 13, weight: .bold))
                                            .foregroundColor(isDone ? .green : (isCurrent ? Color(uiColor: .systemBackground) : .secondary))
                                    }

                                    Text(art.shortTitle)
                                        .font(.system(size: 13, weight: isCurrent ? .semibold : .regular))
                                }
                                .padding(.horizontal, 14)
                                .padding(.vertical, 8)
                                .background(isCurrent ? Color.primary : Color(uiColor: .secondarySystemGroupedBackground))
                                .foregroundColor(isCurrent ? Color(uiColor: .systemBackground) : .primary)
                                .cornerRadius(16)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 16)
                                        .stroke(isDone ? Color.green.opacity(0.4) : (isCurrent ? Color.clear : Color(uiColor: .separator)), lineWidth: 1)
                                )
                            }
                        }
                    }
                    .padding(.horizontal, 16)
                    .padding(.bottom, 6)
                }
            }
            .background(Color(uiColor: .systemGroupedBackground))
        } else if viewModel.currentExercise.isEJ4Exercise {
            let ex = viewModel.currentExercise
            let completedCount = viewModel.store.ej4TypeCompletedCount(for: ex)
            let isAllDone = viewModel.store.isEJ4TypeFullyCompleted(for: ex)
            let curSecIdx = viewModel.currentEJ4TypeSectionIndex
            let selectArtKey = ex == .r2 ? "r2_select_art" : (ex == .r4 ? "r4_select_art" : "ej4_select_art")

            VStack(spacing: 6) {
                if !isCompact {
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 6) {
                            ForEach(EJ4Section.all) { sec in
                                let isSel = curSecIdx == sec.id
                                Button {
                                    viewModel.selectEJ4Section(sec.id, for: ex)
                                } label: {
                                    Text("\(sec.shortName(for: ex)) (\(sec.measureRange(for: ex)))")
                                        .font(.system(size: 11.5, weight: isSel ? .bold : .medium))
                                        .padding(.horizontal, 10)
                                        .padding(.vertical, 5)
                                        .background(isSel ? Color.blue : Color(uiColor: .secondarySystemGroupedBackground))
                                        .foregroundColor(isSel ? .white : .primary)
                                        .cornerRadius(10)
                                }
                            }
                        }
                        .padding(.horizontal, 16)
                        .padding(.top, 4)
                    }
                }

                HStack {
                    HStack(spacing: 6) {
                        Text(loc.t(selectArtKey))
                            .font(.caption.bold())
                            .foregroundColor(.primary)

                        if isAllDone {
                            Image(systemName: "checkmark.seal.fill")
                                .font(.system(size: 12))
                                .foregroundColor(.green)
                        }
                    }

                    Spacer()

                    Text("\(completedCount)/8 " + loc.t("arts_count"))
                        .font(.caption.bold().monospacedDigit())
                        .padding(.horizontal, 8)
                        .padding(.vertical, 3)
                        .background(isAllDone ? Color.green.opacity(0.18) : (completedCount > 0 ? Color.orange.opacity(0.15) : Color(uiColor: .tertiarySystemFill)))
                        .foregroundColor(isAllDone ? .green : (completedCount > 0 ? .orange : .secondary))
                        .cornerRadius(8)
                }
                .padding(.horizontal, 16)
                .padding(.top, 4)

                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(EJ4Articulation.allCases) { art in
                            let isCurrent = viewModel.currentEJ4TypeArticulation == art
                            let isDone = viewModel.store.isEJ4Completed(art, for: ex)

                            Button {
                                if isCurrent {
                                    if art != .original {
                                        viewModel.store.toggleEJ4Completed(art, for: ex)
                                    }
                                } else {
                                    viewModel.selectEJ4Articulation(art, for: ex, markPreviousCompleted: true)
                                }
                            } label: {
                                HStack(spacing: 6) {
                                    if art == .original {
                                        Image(systemName: "book.pages.fill")
                                            .font(.system(size: 12, weight: .bold))
                                            .foregroundColor(isCurrent ? Color(uiColor: .systemBackground) : .indigo)
                                    } else {
                                        Image(systemName: isDone ? "checkmark.circle.fill" : (isCurrent ? "circle" : "circle.dashed"))
                                            .font(.system(size: 13, weight: .bold))
                                            .foregroundColor(isDone ? .green : (isCurrent ? Color(uiColor: .systemBackground) : .secondary))
                                    }

                                    Text(art.shortTitle)
                                        .font(.system(size: 13, weight: isCurrent ? .semibold : .regular))
                                }
                                .padding(.horizontal, 14)
                                .padding(.vertical, 8)
                                .background(isCurrent ? Color.primary : Color(uiColor: .secondarySystemGroupedBackground))
                                .foregroundColor(isCurrent ? Color(uiColor: .systemBackground) : .primary)
                                .cornerRadius(16)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 16)
                                        .stroke(isDone ? Color.green.opacity(0.4) : (isCurrent ? Color.clear : Color(uiColor: .separator)), lineWidth: 1)
                                )
                            }
                        }
                    }
                    .padding(.horizontal, 16)
                    .padding(.bottom, 6)
                }
            }
            .background(Color(uiColor: .systemGroupedBackground))
        } else if viewModel.currentExercise.isEJ5TypeExercise {
            let ex = viewModel.currentExercise
            let completedCount = viewModel.store.ej5TypeCompletedCount(for: ex)
            let isAllDone = viewModel.store.isEJ5TypeFullyCompleted(for: ex)
            let curSecIdx = viewModel.currentEJ5TypeSectionIndex
            let selectArtKey: String = {
                switch ex {
                case .ej5:  return "ej5_select_art"
                case .ej10: return "ej10_select_art"
                case .ej11: return "ej11_select_art"
                case .r1:   return "r1_select_art"
                case .r5:   return "r5_select_art"
                default:    return "ej5_select_art"
                }
            }()

            VStack(spacing: 6) {
                if !isCompact {
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 6) {
                            ForEach(0..<ex.sectionCount, id: \.self) { idx in
                                let isSel = curSecIdx == idx
                                let shortName = ex.isReichertExercise
                                    ? EJ4Section.all[idx].shortName(for: ex)
                                    : (ex == .ej5 ? EJ5Section.all[idx].shortName : EJ10Section.all[idx].shortName)
                                let mRange = ex.isReichertExercise
                                    ? EJ4Section.all[idx].measureRange(for: ex)
                                    : (ex == .ej5 ? EJ5Section.all[idx].measureRange : EJ10Section.all[idx].measureRange)
                                Button {
                                    viewModel.selectEJ5TypeSection(idx)
                                } label: {
                                    Text("\(shortName) (\(mRange))")
                                        .font(.system(size: 11.5, weight: isSel ? .bold : .medium))
                                        .padding(.horizontal, 10)
                                        .padding(.vertical, 5)
                                        .background(isSel ? Color.blue : Color(uiColor: .secondarySystemGroupedBackground))
                                        .foregroundColor(isSel ? .white : .primary)
                                        .cornerRadius(10)
                                }
                            }
                        }
                        .padding(.horizontal, 16)
                        .padding(.top, 4)
                    }
                }

                HStack {
                    HStack(spacing: 6) {
                        Text(loc.t(selectArtKey))
                            .font(.caption.bold())
                            .foregroundColor(.primary)

                        if isAllDone {
                            Image(systemName: "checkmark.seal.fill")
                                .font(.system(size: 12))
                                .foregroundColor(.green)
                        }
                    }

                    Spacer()

                    Text("\(completedCount)/10 " + loc.t("arts_count"))
                        .font(.caption.bold().monospacedDigit())
                        .padding(.horizontal, 8)
                        .padding(.vertical, 3)
                        .background(isAllDone ? Color.green.opacity(0.18) : (completedCount > 0 ? Color.orange.opacity(0.15) : Color(uiColor: .tertiarySystemFill)))
                        .foregroundColor(isAllDone ? .green : (completedCount > 0 ? .orange : .secondary))
                        .cornerRadius(8)
                }
                .padding(.horizontal, 16)
                .padding(.top, 4)

                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(EJ5Articulation.allCases) { art in
                            let isCurrent = viewModel.currentEJ5TypeArticulation == art
                            let isDone = viewModel.store.isEJ5TypeCompleted(art, for: ex)

                            Button {
                                if isCurrent {
                                    if art != .original {
                                        viewModel.store.toggleEJ5TypeCompleted(art, for: ex)
                                    }
                                } else {
                                    viewModel.selectEJ5TypeArticulation(art, markPreviousCompleted: true)
                                }
                            } label: {
                                HStack(spacing: 6) {
                                    if art == .original {
                                        Image(systemName: "book.pages.fill")
                                            .font(.system(size: 12, weight: .bold))
                                            .foregroundColor(isCurrent ? Color(uiColor: .systemBackground) : .indigo)
                                    } else {
                                        Image(systemName: isDone ? "checkmark.circle.fill" : (isCurrent ? "circle" : "circle.dashed"))
                                            .font(.system(size: 13, weight: .bold))
                                            .foregroundColor(isDone ? .green : (isCurrent ? Color(uiColor: .systemBackground) : .secondary))
                                    }

                                    Text(art.shortTitle(for: ex))
                                        .font(.system(size: 13, weight: isCurrent ? .semibold : .regular))
                                }
                                .padding(.horizontal, 14)
                                .padding(.vertical, 8)
                                .background(isCurrent ? Color.primary : Color(uiColor: .secondarySystemGroupedBackground))
                                .foregroundColor(isCurrent ? Color(uiColor: .systemBackground) : .primary)
                                .cornerRadius(16)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 16)
                                        .stroke(isDone ? Color.green.opacity(0.4) : (isCurrent ? Color.clear : Color(uiColor: .separator)), lineWidth: 1)
                                )
                            }
                        }
                    }
                    .padding(.horizontal, 16)
                    .padding(.bottom, 6)
                }
            }
            .background(Color(uiColor: .systemGroupedBackground))
        } else {
            let completedCount = viewModel.completedArticulationsInCurrentMode
            let isModeFull = completedCount == 8

            VStack(spacing: 6) {
                HStack {
                    HStack(spacing: 6) {
                        Text(loc.t("articulations_title"))
                            .font(.caption.bold())
                            .foregroundColor(.primary)

                        if isModeFull {
                            Image(systemName: "checkmark.seal.fill")
                                .font(.system(size: 12))
                                .foregroundColor(.green)
                        }
                    }

                    Spacer()

                    Text("\(completedCount)/8 " + loc.t("arts_count"))
                        .font(.caption.bold().monospacedDigit())
                        .padding(.horizontal, 8)
                        .padding(.vertical, 3)
                        .background(isModeFull ? Color.green.opacity(0.18) : (completedCount > 0 ? Color.orange.opacity(0.15) : Color(uiColor: .tertiarySystemFill)))
                        .foregroundColor(isModeFull ? .green : (completedCount > 0 ? .orange : .secondary))
                        .cornerRadius(8)
                }
                .padding(.horizontal, 16)
                .padding(.top, 4)

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
                                if isCurrent {
                                    viewModel.store.toggleCompleted(
                                        tonic: viewModel.currentTonic,
                                        mode: viewModel.currentMode,
                                        articulation: pattern
                                    )
                                } else {
                                    viewModel.selectArticulation(pattern, markPreviousCompleted: true)
                                }
                            } label: {
                                HStack(spacing: 6) {
                                    Image(systemName: isDone ? "checkmark.circle.fill" : (isCurrent ? "circle" : "circle.dashed"))
                                        .font(.system(size: 13, weight: .bold))
                                        .foregroundColor(isDone ? .green : (isCurrent ? Color(uiColor: .systemBackground) : .secondary))

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
                                        .stroke(isDone ? Color.green.opacity(0.4) : (isCurrent ? Color.clear : Color(uiColor: .separator)), lineWidth: 1)
                                )
                            }
                        }
                    }
                    .padding(.horizontal, 16)
                    .padding(.bottom, 6)
                }
            }
            .background(Color(uiColor: .systemGroupedBackground))
        }
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

            if viewModel.currentExercise.isChromaticExercise {
                let ex = viewModel.currentExercise
                let isAllDone = viewModel.store.isChromaticFullyCompleted(for: ex)
                let completedCount = viewModel.store.chromaticCompletedCount(for: ex)
                if isAllDone {
                    Button {
                        if ex == .ej2 {
                            viewModel.showEJ2CompletionDialog = true
                        } else {
                            viewModel.showEJ1CompletionDialog = true
                        }
                    } label: {
                        HStack(spacing: 8) {
                            Image(systemName: "checkmark.seal.fill")
                                .font(.system(size: 16))
                            Text("✓ \(loc.t(ex == .ej2 ? "ej2_ten_arts_completed" : "ej1_ten_arts_completed"))")
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
                    Button {
                        viewModel.advanceToNextChromaticArticulation()
                    } label: {
                        HStack(spacing: 8) {
                            Text(loc.t("next_art"))
                                .font(.subheadline.bold())
                            Text("\(completedCount)/10 \(loc.t("arts_count"))")
                                .font(.caption.bold().monospacedDigit())
                                .padding(.horizontal, 8)
                                .padding(.vertical, 3)
                                .background(Color(uiColor: .systemBackground).opacity(0.2))
                                .clipShape(Capsule())
                            Image(systemName: "arrow.right")
                        }
                        .padding(.horizontal, 20)
                        .padding(.vertical, 12)
                        .background(Color.primary)
                        .foregroundColor(Color(uiColor: .systemBackground))
                        .cornerRadius(20)
                    }
                }
            } else if viewModel.currentExercise.isEJ4Exercise {
                let ex = viewModel.currentExercise
                let isAllDone = viewModel.store.isEJ4TypeFullyCompleted(for: ex)
                let completedCount = viewModel.store.ej4TypeCompletedCount(for: ex)

                Button {
                    viewModel.advanceToNextEJ4Section()
                } label: {
                    HStack(spacing: 6) {
                        Text("Sig. Tonalidad")
                            .font(.subheadline.bold())
                        Text("\(viewModel.currentEJ4TypeSectionIndex + 1)/25")
                            .font(.caption.bold().monospacedDigit())
                            .padding(.horizontal, 8)
                            .padding(.vertical, 3)
                            .background(Color(uiColor: .tertiarySystemFill))
                            .clipShape(Capsule())
                    }
                    .padding(.horizontal, 16)
                    .padding(.vertical, 12)
                    .background(Color(uiColor: .secondarySystemFill))
                    .foregroundColor(.primary)
                    .cornerRadius(20)
                }

                if isAllDone {
                    Button {
                        viewModel.showEJ4CompletionDialog = true
                    } label: {
                        HStack(spacing: 8) {
                            Image(systemName: "checkmark.seal.fill")
                                .font(.system(size: 16))
                            Text("✓ \(loc.t("ej4_eight_arts_completed"))")
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
                    Button {
                        viewModel.advanceToNextEJ4Articulation()
                    } label: {
                        HStack(spacing: 8) {
                            Text(loc.t("next_art"))
                                .font(.subheadline.bold())
                            Text("\(completedCount)/8 \(loc.t("arts_count"))")
                                .font(.caption.bold().monospacedDigit())
                                .padding(.horizontal, 8)
                                .padding(.vertical, 3)
                                .background(Color(uiColor: .systemBackground).opacity(0.2))
                                .clipShape(Capsule())
                            Image(systemName: "arrow.right")
                        }
                        .padding(.horizontal, 20)
                        .padding(.vertical, 12)
                        .background(Color.primary)
                        .foregroundColor(Color(uiColor: .systemBackground))
                        .cornerRadius(20)
                    }
                }
            } else if viewModel.currentExercise.isEJ5TypeExercise {
                let ex = viewModel.currentExercise
                let isAllDone = viewModel.store.isEJ5TypeFullyCompleted(for: ex)
                let completedCount = viewModel.store.ej5TypeCompletedCount(for: ex)

                Button {
                    viewModel.advanceToNextEJ5TypeSection()
                } label: {
                    HStack(spacing: 6) {
                        Text(ex.isReichertExercise ? "Sig. Tonalidad" : (ex == .ej5 ? "Sig. Escala" : "Sig. Serie"))
                            .font(.subheadline.bold())
                        Text("\(viewModel.currentEJ5TypeSectionIndex + 1)/\(ex.sectionCount)")
                            .font(.caption.bold().monospacedDigit())
                            .padding(.horizontal, 8)
                            .padding(.vertical, 3)
                            .background(Color(uiColor: .tertiarySystemFill))
                            .clipShape(Capsule())
                    }
                    .padding(.horizontal, 16)
                    .padding(.vertical, 12)
                    .background(Color(uiColor: .secondarySystemFill))
                    .foregroundColor(.primary)
                    .cornerRadius(20)
                }

                if isAllDone {
                    Button {
                        viewModel.showEJ5TypeCompletionDialog = true
                    } label: {
                        HStack(spacing: 8) {
                            Image(systemName: "checkmark.seal.fill")
                                .font(.system(size: 16))
                            Text("✓ \(loc.t("ej1_ten_arts_completed"))")
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
                    Button {
                        viewModel.advanceToNextEJ5TypeArticulation()
                    } label: {
                        HStack(spacing: 8) {
                            Text(loc.t("next_art"))
                                .font(.subheadline.bold())
                            Text("\(completedCount)/10 \(loc.t("arts_count"))")
                                .font(.caption.bold().monospacedDigit())
                                .padding(.horizontal, 8)
                                .padding(.vertical, 3)
                                .background(Color(uiColor: .systemBackground).opacity(0.2))
                                .clipShape(Capsule())
                            Image(systemName: "arrow.right")
                        }
                        .padding(.horizontal, 20)
                        .padding(.vertical, 12)
                        .background(Color.primary)
                        .foregroundColor(Color(uiColor: .systemBackground))
                        .cornerRadius(20)
                    }
                }
            } else {
                // Next Articulation in Current Mode
                Button {
                    viewModel.advanceToNextArticulation()
                } label: {
                    HStack(spacing: 8) {
                        Text(loc.t("next_art"))
                            .font(.subheadline.bold())
                        Text("\(viewModel.completedArticulationsInCurrentMode)/8 \(loc.t("arts_count"))")
                            .font(.caption.bold().monospacedDigit())
                            .padding(.horizontal, 8)
                            .padding(.vertical, 3)
                            .background(Color(uiColor: .tertiarySystemFill))
                            .clipShape(Capsule())
                    }
                    .padding(.horizontal, 16)
                    .padding(.vertical, 12)
                    .background(Color(uiColor: .secondarySystemFill))
                    .foregroundColor(.primary)
                    .cornerRadius(20)
                }

                // Main Pedagogical Action Button
                if viewModel.areAllModesInCurrentTonicPracticed {
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
                } else if viewModel.store.isModeFullyCompleted(tonic: viewModel.currentTonic, mode: viewModel.currentMode) {
                    Button {
                        viewModel.advanceToNextMode()
                    } label: {
                        HStack(spacing: 8) {
                            Image(systemName: "checkmark.circle.fill")
                                .font(.system(size: 14, weight: .bold))
                            Text(loc.t("mode_done"))
                                .font(.subheadline.bold())
                            Text("\(viewModel.practicedModesCountInCurrentTonic)/7 \(loc.t("modes_count"))")
                                .font(.caption.bold().monospacedDigit())
                                .padding(.horizontal, 8)
                                .padding(.vertical, 3)
                                .background(Color.white.opacity(0.25))
                                .clipShape(Capsule())
                            Image(systemName: "arrow.right")
                        }
                        .padding(.horizontal, 20)
                        .padding(.vertical, 12)
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(20)
                    }
                } else {
                    Button {
                        viewModel.advanceToNextMode()
                    } label: {
                        HStack(spacing: 8) {
                            Text(loc.t("next_mode"))
                                .font(.subheadline.bold())
                            Text("\(viewModel.practicedModesCountInCurrentTonic)/7 \(loc.t("modes_count"))")
                                .font(.caption.bold().monospacedDigit())
                                .padding(.horizontal, 8)
                                .padding(.vertical, 3)
                                .background(Color(uiColor: .systemBackground).opacity(0.2))
                                .clipShape(Capsule())
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
        }
        .padding(.horizontal, 24)
        .padding(.vertical, 12)
        .background(Color(uiColor: .secondarySystemBackground))
    }

    // MARK: - Mobile Control Toolbar (2 Rows, Thumb-Friendly)
    private var mobileControlToolbar: some View {
        VStack(spacing: 10) {
            // Row 1: Metronome controls + BPM Stepper + Play Piano button
            HStack(spacing: 10) {
                Button {
                    metronome.toggle()
                } label: {
                    Image(systemName: metronome.isPlaying ? "pause.circle.fill" : "play.circle.fill")
                        .font(.system(size: 30))
                        .foregroundColor(.primary)
                }

                // 4 Beat Dots
                HStack(spacing: 5) {
                    ForEach(1...4, id: \.self) { beat in
                        Circle()
                            .fill(metronome.isPlaying && metronome.currentBeat == beat ? Color.primary : Color(uiColor: .tertiaryLabel))
                            .frame(width: 7, height: 7)
                            .scaleEffect(metronome.isPlaying && metronome.currentBeat == beat ? 1.3 : 1.0)
                    }
                }

                // BPM Stepper
                HStack(spacing: 4) {
                    Button {
                        metronome.setTempo(metronome.tempoBPM - 2)
                        viewModel.updateScore()
                    } label: {
                        Image(systemName: "minus")
                            .font(.system(size: 11, weight: .bold))
                            .frame(width: 26, height: 26)
                            .background(Color(uiColor: .tertiarySystemFill))
                            .cornerRadius(6)
                    }

                    Text("\(metronome.tempoBPM)")
                        .font(.caption.bold().monospacedDigit())
                        .frame(minWidth: 28)

                    Button {
                        metronome.setTempo(metronome.tempoBPM + 2)
                        viewModel.updateScore()
                    } label: {
                        Image(systemName: "plus")
                            .font(.system(size: 11, weight: .bold))
                            .frame(width: 26, height: 26)
                            .background(Color(uiColor: .tertiarySystemFill))
                            .cornerRadius(6)
                    }
                }
                .padding(.horizontal, 6)
                .padding(.vertical, 3)
                .background(Color(uiColor: .secondarySystemGroupedBackground))
                .cornerRadius(8)

                Spacer()

                // Play Piano button
                Button {
                    viewModel.toggleScorePlayback()
                } label: {
                    HStack(spacing: 6) {
                        Image(systemName: scorePlayer.isPlaying ? "stop.circle.fill" : "pianokeys")
                        Text(scorePlayer.isPlaying ? loc.t("stop_piano") : loc.t("play_piano"))
                            .font(.caption.bold())
                    }
                    .padding(.horizontal, 12)
                    .padding(.vertical, 7)
                    .background(scorePlayer.isPlaying ? Color.red : Color.indigo)
                    .foregroundColor(.white)
                    .cornerRadius(14)
                }
            }

            // Row 2: Thumb-friendly main actions
            if viewModel.currentExercise.isChromaticExercise {
                let ex = viewModel.currentExercise
                let isAllDone = viewModel.store.isChromaticFullyCompleted(for: ex)
                let completedCount = viewModel.store.chromaticCompletedCount(for: ex)
                HStack(spacing: 8) {
                    if isAllDone {
                        Button {
                            if ex == .ej2 {
                                viewModel.showEJ2CompletionDialog = true
                            } else {
                                viewModel.showEJ1CompletionDialog = true
                            }
                        } label: {
                            HStack(spacing: 6) {
                                Image(systemName: "checkmark.seal.fill")
                                    .font(.system(size: 14, weight: .bold))
                                Text("✓ \(loc.t(ex == .ej2 ? "ej2_ten_arts_completed" : "ej1_ten_arts_completed"))")
                                    .font(.system(size: 14, weight: .bold))
                                    .lineLimit(1)
                            }
                            .frame(maxWidth: .infinity)
                            .frame(height: 48)
                            .padding(.horizontal, 12)
                            .background(Color.green)
                            .foregroundColor(.white)
                            .cornerRadius(16)
                            .shadow(color: Color.green.opacity(0.3), radius: 4, x: 0, y: 2)
                        }
                    } else {
                        Button {
                            viewModel.advanceToNextChromaticArticulation()
                        } label: {
                            HStack(spacing: 8) {
                                Text(loc.t("next_art"))
                                    .font(.system(size: 14, weight: .bold))
                                    .lineLimit(1)
                                Text("\(completedCount)/10 \(loc.t("arts_count"))")
                                    .font(.system(size: 12, weight: .bold, design: .monospaced))
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 3)
                                    .background(Color(uiColor: .systemBackground).opacity(0.2))
                                    .clipShape(Capsule())
                                Image(systemName: "chevron.right")
                                    .font(.system(size: 12, weight: .bold))
                            }
                            .frame(maxWidth: .infinity)
                            .frame(height: 48)
                            .padding(.horizontal, 12)
                            .background(Color.primary)
                            .foregroundColor(Color(uiColor: .systemBackground))
                            .cornerRadius(16)
                        }
                    }
                }
            } else if viewModel.currentExercise.isEJ4Exercise {
                let ex = viewModel.currentExercise
                let isAllDone = viewModel.store.isEJ4TypeFullyCompleted(for: ex)
                let completedCount = viewModel.store.ej4TypeCompletedCount(for: ex)

                HStack(spacing: 8) {
                    Button {
                        viewModel.advanceToNextEJ4Section()
                    } label: {
                        HStack(spacing: 5) {
                            Text("Sig. Ton.")
                                .font(.system(size: 13, weight: .semibold))
                                .lineLimit(1)
                            Text("\(viewModel.currentEJ4TypeSectionIndex + 1)/25")
                                .font(.system(size: 11, weight: .bold, design: .monospaced))
                                .padding(.horizontal, 5)
                                .padding(.vertical, 2)
                                .background(Color(uiColor: .tertiarySystemFill))
                                .clipShape(Capsule())
                        }
                        .padding(.horizontal, 10)
                        .frame(height: 48)
                        .background(Color(uiColor: .secondarySystemFill))
                        .foregroundColor(.primary)
                        .cornerRadius(16)
                    }

                    if isAllDone {
                        Button {
                            viewModel.showEJ4CompletionDialog = true
                        } label: {
                            HStack(spacing: 5) {
                                Image(systemName: "checkmark.seal.fill")
                                    .font(.system(size: 14, weight: .bold))
                                Text("✓ \(loc.t("ej4_eight_arts_completed"))")
                                    .font(.system(size: 13, weight: .bold))
                                    .lineLimit(1)
                                    .minimumScaleFactor(0.85)
                            }
                            .frame(maxWidth: .infinity)
                            .frame(height: 48)
                            .padding(.horizontal, 10)
                            .background(Color.green)
                            .foregroundColor(.white)
                            .cornerRadius(16)
                            .shadow(color: Color.green.opacity(0.3), radius: 4, x: 0, y: 2)
                        }
                    } else {
                        Button {
                            viewModel.advanceToNextEJ4Articulation()
                        } label: {
                            HStack(spacing: 6) {
                                Text(loc.t("next_art"))
                                    .font(.system(size: 13, weight: .bold))
                                    .lineLimit(1)
                                Text("\(completedCount)/8")
                                    .font(.system(size: 11, weight: .bold, design: .monospaced))
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color(uiColor: .systemBackground).opacity(0.2))
                                    .clipShape(Capsule())
                                Image(systemName: "chevron.right")
                                    .font(.system(size: 11, weight: .bold))
                            }
                            .frame(maxWidth: .infinity)
                            .frame(height: 48)
                            .padding(.horizontal, 10)
                            .background(Color.primary)
                            .foregroundColor(Color(uiColor: .systemBackground))
                            .cornerRadius(16)
                        }
                    }
                }
            } else if viewModel.currentExercise.isEJ5TypeExercise {
                let ex = viewModel.currentExercise
                let isAllDone = viewModel.store.isEJ5TypeFullyCompleted(for: ex)
                let completedCount = viewModel.store.ej5TypeCompletedCount(for: ex)

                HStack(spacing: 8) {
                    Button {
                        viewModel.advanceToNextEJ5TypeSection()
                    } label: {
                        HStack(spacing: 5) {
                            Text(ex.isReichertExercise ? "Sig. Ton." : (ex == .ej5 ? "Sig. Esc." : "Sig. Serie"))
                                .font(.system(size: 13, weight: .semibold))
                                .lineLimit(1)
                            Text("\(viewModel.currentEJ5TypeSectionIndex + 1)/\(ex.sectionCount)")
                                .font(.system(size: 11, weight: .bold, design: .monospaced))
                                .padding(.horizontal, 5)
                                .padding(.vertical, 2)
                                .background(Color(uiColor: .tertiarySystemFill))
                                .clipShape(Capsule())
                        }
                        .padding(.horizontal, 10)
                        .frame(height: 48)
                        .background(Color(uiColor: .secondarySystemFill))
                        .foregroundColor(.primary)
                        .cornerRadius(16)
                    }

                    if isAllDone {
                        Button {
                            viewModel.showEJ5TypeCompletionDialog = true
                        } label: {
                            HStack(spacing: 5) {
                                Image(systemName: "checkmark.seal.fill")
                                    .font(.system(size: 14, weight: .bold))
                                Text("✓ \(loc.t("ej1_ten_arts_completed"))")
                                    .font(.system(size: 13, weight: .bold))
                                    .lineLimit(1)
                                    .minimumScaleFactor(0.85)
                            }
                            .frame(maxWidth: .infinity)
                            .frame(height: 48)
                            .padding(.horizontal, 10)
                            .background(Color.green)
                            .foregroundColor(.white)
                            .cornerRadius(16)
                            .shadow(color: Color.green.opacity(0.3), radius: 4, x: 0, y: 2)
                        }
                    } else {
                        Button {
                            viewModel.advanceToNextEJ5TypeArticulation()
                        } label: {
                            HStack(spacing: 6) {
                                Text(loc.t("next_art"))
                                    .font(.system(size: 13, weight: .bold))
                                    .lineLimit(1)
                                Text("\(completedCount)/10")
                                    .font(.system(size: 11, weight: .bold, design: .monospaced))
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color(uiColor: .systemBackground).opacity(0.2))
                                    .clipShape(Capsule())
                                Image(systemName: "chevron.right")
                                    .font(.system(size: 11, weight: .bold))
                            }
                            .frame(maxWidth: .infinity)
                            .frame(height: 48)
                            .padding(.horizontal, 10)
                            .background(Color.primary)
                            .foregroundColor(Color(uiColor: .systemBackground))
                            .cornerRadius(16)
                        }
                    }
                }
            } else {
                HStack(spacing: 8) {
                    Button {
                        viewModel.advanceToNextArticulation()
                    } label: {
                        HStack(spacing: 5) {
                            Text(loc.t("next_art"))
                                .font(.system(size: 13, weight: .semibold))
                                .lineLimit(1)
                            Text("\(viewModel.completedArticulationsInCurrentMode)/8")
                                .font(.system(size: 11, weight: .bold, design: .monospaced))
                                .padding(.horizontal, 5)
                                .padding(.vertical, 2)
                                .background(Color(uiColor: .tertiarySystemFill))
                                .clipShape(Capsule())
                        }
                        .padding(.horizontal, 10)
                        .frame(height: 48)
                        .background(Color(uiColor: .secondarySystemFill))
                        .foregroundColor(.primary)
                        .cornerRadius(16)
                    }

                    if viewModel.areAllModesInCurrentTonicPracticed {
                        Button {
                            viewModel.showCompletionDialog = true
                        } label: {
                            HStack(spacing: 5) {
                                Image(systemName: "checkmark.seal.fill")
                                    .font(.system(size: 14, weight: .bold))
                                Text("✓ \(loc.t("seven_modes_completed"))")
                                    .font(.system(size: 13, weight: .bold))
                                    .lineLimit(1)
                                    .minimumScaleFactor(0.85)
                            }
                            .frame(maxWidth: .infinity)
                            .frame(height: 48)
                            .padding(.horizontal, 10)
                            .background(Color.green)
                            .foregroundColor(.white)
                            .cornerRadius(16)
                            .shadow(color: Color.green.opacity(0.3), radius: 4, x: 0, y: 2)
                        }
                    } else if viewModel.store.isModeFullyCompleted(tonic: viewModel.currentTonic, mode: viewModel.currentMode) {
                        Button {
                            viewModel.advanceToNextMode()
                        } label: {
                            HStack(spacing: 5) {
                                Image(systemName: "checkmark.circle.fill")
                                    .font(.system(size: 13, weight: .bold))
                                Text(loc.t("mode_done"))
                                    .font(.system(size: 13, weight: .bold))
                                    .lineLimit(1)
                                Text("\(viewModel.practicedModesCountInCurrentTonic)/7")
                                    .font(.system(size: 11, weight: .bold, design: .monospaced))
                                    .padding(.horizontal, 5)
                                    .padding(.vertical, 2)
                                    .background(Color.white.opacity(0.25))
                                    .clipShape(Capsule())
                                Image(systemName: "chevron.right")
                                    .font(.system(size: 11, weight: .bold))
                            }
                            .frame(maxWidth: .infinity)
                            .frame(height: 48)
                            .padding(.horizontal, 10)
                            .background(Color.green)
                            .foregroundColor(.white)
                            .cornerRadius(16)
                        }
                    } else {
                        Button {
                            viewModel.advanceToNextMode()
                        } label: {
                            HStack(spacing: 5) {
                                Text(loc.t("next_mode"))
                                    .font(.system(size: 13, weight: .bold))
                                    .lineLimit(1)
                                Text("\(viewModel.practicedModesCountInCurrentTonic)/7")
                                    .font(.system(size: 11, weight: .bold, design: .monospaced))
                                    .padding(.horizontal, 5)
                                    .padding(.vertical, 2)
                                    .background(Color(uiColor: .systemBackground).opacity(0.2))
                                    .clipShape(Capsule())
                                Image(systemName: "chevron.right")
                                    .font(.system(size: 11, weight: .bold))
                            }
                            .frame(maxWidth: .infinity)
                            .frame(height: 48)
                            .padding(.horizontal, 10)
                            .background(Color.primary)
                            .foregroundColor(Color(uiColor: .systemBackground))
                            .cornerRadius(16)
                        }
                    }
                }
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 10)
        .background(Color(uiColor: .secondarySystemBackground))
    }
}
