import SwiftUI

public struct HomeView: View {
    @ObservedObject var viewModel: PracticeViewModel
    @ObservedObject var loc = LocalizationManager.shared
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass
    @State private var navigateToPractice = false
    @State private var navigateToMatrix = false

    private var isCompact: Bool {
        horizontalSizeClass == .compact
    }

    public init(viewModel: PracticeViewModel) {
        self.viewModel = viewModel
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                Color(uiColor: .systemGroupedBackground)
                    .ignoresSafeArea()

                ScrollView {
                    VStack(spacing: isCompact ? 18 : 24) {
                        // Top Bar with Language Switcher & Quick Matrix
                        HStack {
                            if isCompact {
                                HStack(spacing: 8) {
                                    Image(systemName: "music.note.list")
                                        .foregroundColor(.accentColor)
                                    Text(loc.t("app_name"))
                                        .font(.headline.weight(.bold))
                                }
                            }

                            Spacer()

                            Button {
                                navigateToMatrix = true
                            } label: {
                                Image(systemName: "square.grid.3x3.fill")
                                    .font(.subheadline)
                                    .padding(8)
                                    .background(Color(uiColor: .tertiarySystemFill))
                                    .foregroundColor(.primary)
                                    .clipShape(Circle())
                            }

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
                        .padding(.top, isCompact ? 4 : 8)

                        // Header / Hero
                        VStack(spacing: 10) {
                            if !isCompact {
                                Text(loc.t("app_name"))
                                    .font(.system(size: 32, weight: .bold))
                                    .foregroundColor(.primary)
                            }

                            // Exercise Selector (E.J. 1 | E.J. 2 | E.J. 4 | E.J. 5 | E.J. 10 | E.J. 11 | 84 Modos)
                            ScrollView(.horizontal, showsIndicators: false) {
                                HStack(spacing: 8) {
                                    ForEach(ExerciseType.allCases) { exercise in
                                        let isSelected = viewModel.currentExercise == exercise
                                        Button {
                                            withAnimation(.easeInOut(duration: 0.2)) {
                                                viewModel.selectExercise(exercise)
                                            }
                                        } label: {
                                            HStack(spacing: 5) {
                                                Image(systemName: exercise.isLeducExercise ? "music.quarternote.3" : "dial.medium.fill")
                                                    .font(.caption2.bold())
                                                Text(isCompact ? exercise.pillLabel : exercise.displayTitle)
                                                    .font(.system(size: isCompact ? 13 : 13.5, weight: .bold))
                                                    .lineLimit(1)
                                            }
                                            .padding(.vertical, 10)
                                            .padding(.horizontal, isCompact ? 14 : 16)
                                            .background(isSelected ? Color.primary : Color(uiColor: .secondarySystemGroupedBackground))
                                            .foregroundColor(isSelected ? Color(uiColor: .systemBackground) : .primary)
                                            .cornerRadius(14)
                                            .overlay(
                                                RoundedRectangle(cornerRadius: 14)
                                                    .stroke(isSelected ? Color.clear : Color(uiColor: .separator), lineWidth: 1)
                                            )
                                        }
                                    }
                                }
                                .padding(.horizontal, 2)
                            }

                            Text(headerTitle)
                                .font(isCompact ? .subheadline.weight(.semibold) : .headline)
                                .foregroundColor(.primary)
                                .multilineTextAlignment(.center)

                            Text(headerSubDesc)
                                .font(.caption)
                                .foregroundColor(.secondary)
                                .multilineTextAlignment(.center)
                        }

                        if viewModel.currentExercise.isChromaticExercise {
                            ej1ArticulationsCard

                            VStack(spacing: 12) {
                                Button {
                                    navigateToPractice = true
                                } label: {
                                    HStack(spacing: 10) {
                                        Image(systemName: "play.fill")
                                        Text("\(loc.t(viewModel.currentExercise == .ej2 ? "ej2_start_practice" : "ej1_start_practice")) (\(viewModel.currentChromaticArticulation.shortTitle))")
                                            .font(.headline)
                                    }
                                    .foregroundColor(Color(uiColor: .systemBackground))
                                    .frame(maxWidth: .infinity)
                                    .frame(height: 52)
                                    .background(Color.primary)
                                    .cornerRadius(26)
                                }
                            }
                        } else if viewModel.currentExercise == .ej4 {
                            // E.J. 4 Section Selector (25 Tonal Sections)
                            VStack(alignment: .leading, spacing: 10) {
                                Text(loc.t("ej4_select_section").uppercased())
                                    .font(.caption.bold())
                                    .foregroundColor(.secondary)
                                    .padding(.horizontal, 4)

                                ScrollView(.horizontal, showsIndicators: false) {
                                    HStack(spacing: 8) {
                                        ForEach(EJ4Section.all) { sec in
                                            let isSelected = viewModel.currentEJ4Section == sec.id
                                            Button {
                                                viewModel.selectEJ4Section(sec.id)
                                            } label: {
                                                VStack(spacing: 2) {
                                                    Text(sec.shortName)
                                                        .font(.system(size: 13, weight: isSelected ? .bold : .semibold))
                                                    Text(sec.measureRange)
                                                        .font(.system(size: 10))
                                                        .opacity(0.8)
                                                }
                                                .padding(.horizontal, 12)
                                                .padding(.vertical, 7)
                                                .background(isSelected ? Color.primary : Color(uiColor: .secondarySystemGroupedBackground))
                                                .foregroundColor(isSelected ? Color(uiColor: .systemBackground) : .primary)
                                                .cornerRadius(14)
                                                .overlay(
                                                    RoundedRectangle(cornerRadius: 14)
                                                        .stroke(isSelected ? Color.clear : Color(uiColor: .separator), lineWidth: 1)
                                                )
                                            }
                                        }
                                    }
                                }
                            }

                            ej4ArticulationsCard

                            VStack(spacing: 12) {
                                let curSec = EJ4Section.all[max(0, min(24, viewModel.currentEJ4Section))]
                                Button {
                                    navigateToPractice = true
                                } label: {
                                    HStack(spacing: 10) {
                                        Image(systemName: "play.fill")
                                        Text("\(loc.t("ej4_start_practice")) (\(curSec.shortName) · \(viewModel.currentEJ4Articulation.shortTitle))")
                                            .font(.headline)
                                            .lineLimit(1)
                                            .minimumScaleFactor(0.8)
                                    }
                                    .foregroundColor(Color(uiColor: .systemBackground))
                                    .frame(maxWidth: .infinity)
                                    .frame(height: 52)
                                    .background(Color.primary)
                                    .cornerRadius(26)
                                }
                            }
                        } else if viewModel.currentExercise.isEJ5TypeExercise {
                            let ex = viewModel.currentExercise
                            let secTitleKey = ex == .ej5 ? "ej5_select_section" : (ex == .ej10 ? "ej10_select_section" : "ej11_select_section")
                            let startBtnKey = ex == .ej5 ? "ej5_start_practice" : (ex == .ej10 ? "ej10_start_practice" : "ej11_start_practice")
                            let curSecIdx = viewModel.currentEJ5TypeSectionIndex
                            let curShortName = ex == .ej5 ? EJ5Section.all[curSecIdx].shortName : EJ10Section.all[curSecIdx].shortName

                            VStack(alignment: .leading, spacing: 10) {
                                Text(loc.t(secTitleKey).uppercased())
                                    .font(.caption.bold())
                                    .foregroundColor(.secondary)
                                    .padding(.horizontal, 4)

                                ScrollView(.horizontal, showsIndicators: false) {
                                    HStack(spacing: 8) {
                                        ForEach(0..<12, id: \.self) { idx in
                                            let isSelected = curSecIdx == idx
                                            let shortName = ex == .ej5 ? EJ5Section.all[idx].shortName : EJ10Section.all[idx].shortName
                                            let mRange = ex == .ej5 ? EJ5Section.all[idx].measureRange : EJ10Section.all[idx].measureRange
                                            Button {
                                                viewModel.selectEJ5TypeSection(idx)
                                            } label: {
                                                VStack(spacing: 2) {
                                                    Text(shortName)
                                                        .font(.system(size: 13, weight: isSelected ? .bold : .semibold))
                                                    Text(mRange)
                                                        .font(.system(size: 10))
                                                        .opacity(0.8)
                                                }
                                                .padding(.horizontal, 12)
                                                .padding(.vertical, 7)
                                                .background(isSelected ? Color.primary : Color(uiColor: .secondarySystemGroupedBackground))
                                                .foregroundColor(isSelected ? Color(uiColor: .systemBackground) : .primary)
                                                .cornerRadius(14)
                                                .overlay(
                                                    RoundedRectangle(cornerRadius: 14)
                                                        .stroke(isSelected ? Color.clear : Color(uiColor: .separator), lineWidth: 1)
                                                )
                                            }
                                        }
                                    }
                                }
                            }

                            ej5TypeArticulationsCard

                            VStack(spacing: 12) {
                                Button {
                                    navigateToPractice = true
                                } label: {
                                    HStack(spacing: 10) {
                                        Image(systemName: "play.fill")
                                        Text("\(loc.t(startBtnKey)) (\(curShortName) · \(viewModel.currentEJ5TypeArticulation.shortTitle(for: ex)))")
                                            .font(.headline)
                                            .lineLimit(1)
                                            .minimumScaleFactor(0.8)
                                    }
                                    .foregroundColor(Color(uiColor: .systemBackground))
                                    .frame(maxWidth: .infinity)
                                    .frame(height: 52)
                                    .background(Color.primary)
                                    .cornerRadius(26)
                                }
                            }
                        } else {
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
                            if isCompact {
                                VStack(spacing: 14) {
                                    majorFamilyCard
                                    minorFamilyCard
                                }
                            } else {
                                HStack(alignment: .top, spacing: 16) {
                                    majorFamilyCard
                                    minorFamilyCard
                                }
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
                                Label(loc.t("click_sound"), systemImage: viewModel.metronome.isAudioMuted ? "speaker.slash.fill" : "speaker.wave.2.fill")
                                Spacer()
                                Toggle("", isOn: Binding(
                                    get: { !viewModel.metronome.isAudioMuted },
                                    set: { viewModel.metronome.isAudioMuted = !$0 }
                                ))
                                .labelsHidden()
                            }
                            .padding(.horizontal, 16)
                            .padding(.vertical, 12)

                            Divider()

                            HStack {
                                Label {
                                    VStack(alignment: .leading, spacing: 2) {
                                        Text(loc.t("keep_screen_awake"))
                                            .font(.body)
                                        Text(loc.t("keep_screen_awake_desc"))
                                            .font(.caption)
                                            .foregroundColor(.secondary)
                                    }
                                } icon: {
                                    Image(systemName: viewModel.keepScreenAwake ? "sun.max.fill" : "moon.fill")
                                        .foregroundColor(viewModel.keepScreenAwake ? .orange : .secondary)
                                }
                                Spacer()
                                Toggle("", isOn: $viewModel.keepScreenAwake)
                                    .labelsHidden()
                            }
                            .padding(.horizontal, 16)
                            .padding(.vertical, 10)
                        }
                        .background(Color(uiColor: .secondarySystemGroupedBackground))
                        .cornerRadius(16)
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(Color(uiColor: .separator), lineWidth: 0.5)
                        )
                    }
                    .padding(.horizontal, isCompact ? 16 : 28)
                    .padding(.bottom, 24)
                }
            }
            .navigationDestination(isPresented: $navigateToPractice) {
                PracticeView(viewModel: viewModel)
            }
            .navigationDestination(isPresented: $navigateToMatrix) {
                ProgressMatrixView(viewModel: viewModel)
            }
            .onAppear {
                for arg in CommandLine.arguments {
                    if arg.hasPrefix("ej1Art=") || arg.hasPrefix("-ej1Art=") {
                        if let valStr = arg.split(separator: "=").last,
                           let raw = Int(valStr),
                           let art = EJ1Articulation(rawValue: raw) {
                            viewModel.selectExercise(.ej1)
                            viewModel.selectEJ1Articulation(art, markPreviousCompleted: false)
                        }
                    } else if arg.hasPrefix("ej2Art=") || arg.hasPrefix("-ej2Art=") {
                        if let valStr = arg.split(separator: "=").last,
                           let raw = Int(valStr),
                           let art = EJ1Articulation(rawValue: raw) {
                            viewModel.selectExercise(.ej2)
                            viewModel.selectEJ2Articulation(art, markPreviousCompleted: false)
                        }
                    } else if arg.hasPrefix("ej4Art=") || arg.hasPrefix("-ej4Art=") {
                        if let valStr = arg.split(separator: "=").last,
                           let raw = Int(valStr),
                           let art = EJ4Articulation(rawValue: raw) {
                            viewModel.selectExercise(.ej4)
                            viewModel.selectEJ4Articulation(art, markPreviousCompleted: false)
                        }
                    } else if arg.hasPrefix("ej4Sec=") || arg.hasPrefix("-ej4Sec=") {
                        if let valStr = arg.split(separator: "=").last,
                           let sec = Int(valStr) {
                            viewModel.selectExercise(.ej4)
                            viewModel.selectEJ4Section(sec)
                        }
                    }
                }
                if CommandLine.arguments.contains("-openPractice") || CommandLine.arguments.contains("openPractice") {
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                        navigateToPractice = true
                    }
                } else if CommandLine.arguments.contains("-openMatrix") || CommandLine.arguments.contains("openMatrix") {
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                        navigateToMatrix = true
                    }
                }
            }
        }
    }

    private var headerTitle: String {
        switch viewModel.currentExercise {
        case .ej1: return loc.t("ej1_title")
        case .ej2: return loc.t("ej2_title")
        case .ej4: return loc.t("ej4_title")
        case .ej5: return loc.t("ej5_title")
        case .ej10: return loc.t("ej10_title")
        case .ej11: return loc.t("ej11_title")
        case .modos: return loc.t("subtitle")
        }
    }

    private var headerSubDesc: String {
        switch viewModel.currentExercise {
        case .ej1: return loc.t("ej1_sub_desc")
        case .ej2: return loc.t("ej2_sub_desc")
        case .ej4: return loc.t("ej4_sub_desc")
        case .ej5: return loc.t("ej5_sub_desc")
        case .ej10: return loc.t("ej10_sub_desc")
        case .ej11: return loc.t("ej11_sub_desc")
        case .modos: return loc.t("sub_desc")
        }
    }

    private var ej5TypeArticulationsCard: some View {
        let ex = viewModel.currentExercise
        let completedCount = viewModel.store.ej5TypeCompletedCount(for: ex)
        let isAllDone = viewModel.store.isEJ5TypeFullyCompleted(for: ex)
        let selectArtKey = ex == .ej5 ? "ej5_select_art" : (ex == .ej10 ? "ej10_select_art" : "ej11_select_art")
        let headerInfoKey = ex == .ej5 ? "ej5_header_info" : (ex == .ej10 ? "ej10_header_info" : "ej11_header_info")

        return VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .firstTextBaseline) {
                VStack(alignment: .leading, spacing: 4) {
                    Text(loc.t(selectArtKey))
                        .font(.title3.bold())
                        .foregroundColor(.primary)
                    Text(loc.t(headerInfoKey))
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                Spacer()

                HStack(spacing: 4) {
                    if isAllDone {
                        Image(systemName: "checkmark.seal.fill")
                            .foregroundColor(.green)
                    }
                    Text("\(completedCount)/10 \(loc.t("arts_count"))")
                        .font(.caption.bold().monospacedDigit())
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(isAllDone ? Color.green.opacity(0.18) : (completedCount > 0 ? Color.orange.opacity(0.15) : Color(uiColor: .tertiarySystemFill)))
                        .foregroundColor(isAllDone ? .green : (completedCount > 0 ? .orange : .secondary))
                        .cornerRadius(8)
                }
            }

            VStack(spacing: 0) {
                ForEach(EJ5Articulation.allCases) { art in
                    let isSelected = viewModel.currentEJ5TypeArticulation == art
                    let isDone = viewModel.store.isEJ5TypeCompleted(art, for: ex)

                    Button {
                        viewModel.selectEJ5TypeArticulation(art, markPreviousCompleted: false)
                        navigateToPractice = true
                    } label: {
                        HStack(spacing: 12) {
                            VStack(alignment: .leading, spacing: 2) {
                                Text(art.title(for: ex))
                                    .font(.subheadline.weight(isSelected ? .bold : .semibold))
                                    .foregroundColor(.primary)
                                    .multilineTextAlignment(.leading)
                                Text(art.formulaBadge(for: ex))
                                    .font(.caption2.monospaced())
                                    .foregroundColor(.secondary)
                            }

                            Spacer()

                            if art == .original {
                                Text("Urtext")
                                    .font(.caption2.bold())
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 3)
                                    .background(Color.indigo.opacity(0.15))
                                    .foregroundColor(.indigo)
                                    .cornerRadius(6)
                            } else if isDone {
                                HStack(spacing: 4) {
                                    Image(systemName: "checkmark.circle.fill")
                                        .foregroundColor(.green)
                                    Text(loc.t("completed"))
                                        .font(.caption2.bold())
                                        .foregroundColor(.green)
                                }
                            } else if isSelected {
                                Text(loc.t("in_progress"))
                                    .font(.caption2.bold())
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.orange.opacity(0.15))
                                    .foregroundColor(.orange)
                                    .cornerRadius(6)
                            } else {
                                Image(systemName: "chevron.right")
                                    .font(.caption2.bold())
                                    .foregroundColor(.secondary)
                            }
                        }
                        .padding(.vertical, 10)
                        .padding(.horizontal, 12)
                        .background(isSelected ? Color.primary.opacity(0.05) : Color.clear)
                    }

                    if art.id != EJ5Articulation.allCases.last?.id {
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

    private var ej4ArticulationsCard: some View {
        let completedCount = viewModel.store.ej4CompletedCount
        let isAllDone = viewModel.store.isEJ4FullyCompleted

        return VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .firstTextBaseline) {
                VStack(alignment: .leading, spacing: 4) {
                    Text(loc.t("ej4_select_art"))
                        .font(.title3.bold())
                        .foregroundColor(.primary)
                    Text(loc.t("ej4_header_info"))
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                Spacer()

                HStack(spacing: 4) {
                    if isAllDone {
                        Image(systemName: "checkmark.seal.fill")
                            .foregroundColor(.green)
                    }
                    Text("\(completedCount)/8 \(loc.t("arts_count"))")
                        .font(.caption.bold().monospacedDigit())
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(isAllDone ? Color.green.opacity(0.18) : (completedCount > 0 ? Color.orange.opacity(0.15) : Color(uiColor: .tertiarySystemFill)))
                        .foregroundColor(isAllDone ? .green : (completedCount > 0 ? .orange : .secondary))
                        .cornerRadius(8)
                }
            }

            VStack(spacing: 0) {
                ForEach(EJ4Articulation.allCases) { art in
                    let isSelected = viewModel.currentEJ4Articulation == art
                    let isDone = viewModel.store.isEJ4Completed(art)

                    Button {
                        viewModel.selectEJ4Articulation(art, markPreviousCompleted: false)
                        navigateToPractice = true
                    } label: {
                        HStack(spacing: 12) {
                            VStack(alignment: .leading, spacing: 2) {
                                Text(art.title)
                                    .font(.subheadline.weight(isSelected ? .bold : .semibold))
                                    .foregroundColor(.primary)
                                    .multilineTextAlignment(.leading)
                                Text(art.formulaBadge)
                                    .font(.caption2.monospaced())
                                    .foregroundColor(.secondary)
                            }

                            Spacer()

                            if art == .original {
                                Text("Urtext")
                                    .font(.caption2.bold())
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 3)
                                    .background(Color.indigo.opacity(0.15))
                                    .foregroundColor(.indigo)
                                    .cornerRadius(6)
                            } else if isDone {
                                HStack(spacing: 4) {
                                    Image(systemName: "checkmark.circle.fill")
                                        .foregroundColor(.green)
                                    Text(loc.t("completed"))
                                        .font(.caption2.bold())
                                        .foregroundColor(.green)
                                }
                            } else if isSelected {
                                Text(loc.t("in_progress"))
                                    .font(.caption2.bold())
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.orange.opacity(0.15))
                                    .foregroundColor(.orange)
                                    .cornerRadius(6)
                            } else {
                                Image(systemName: "chevron.right")
                                    .font(.caption2.bold())
                                    .foregroundColor(.secondary)
                            }
                        }
                        .padding(.vertical, 10)
                        .padding(.horizontal, 12)
                        .background(isSelected ? Color.primary.opacity(0.05) : Color.clear)
                    }

                    if art.id != EJ4Articulation.allCases.last?.id {
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

    private var ej1ArticulationsCard: some View {
        let isEj2 = viewModel.currentExercise == .ej2
        let completedCount = viewModel.store.chromaticCompletedCount(for: viewModel.currentExercise)
        let isAllDone = viewModel.store.isChromaticFullyCompleted(for: viewModel.currentExercise)

        return VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .firstTextBaseline) {
                VStack(alignment: .leading, spacing: 4) {
                    Text(loc.t(isEj2 ? "ej2_select_art" : "ej1_select_art"))
                        .font(.title3.bold())
                        .foregroundColor(.primary)
                    Text(loc.t(isEj2 ? "ej2_header_info" : "ej1_header_info"))
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                Spacer()

                HStack(spacing: 4) {
                    if isAllDone {
                        Image(systemName: "checkmark.seal.fill")
                            .foregroundColor(.green)
                    }
                    Text("\(completedCount)/10 \(loc.t("arts_count"))")
                        .font(.caption.bold().monospacedDigit())
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(isAllDone ? Color.green.opacity(0.18) : (completedCount > 0 ? Color.orange.opacity(0.15) : Color(uiColor: .tertiarySystemFill)))
                        .foregroundColor(isAllDone ? .green : (completedCount > 0 ? .orange : .secondary))
                        .cornerRadius(8)
                }
            }

            VStack(spacing: 0) {
                ForEach(EJ1Articulation.allCases) { art in
                    let isSelected = viewModel.currentChromaticArticulation == art
                    let isDone = viewModel.store.isChromaticCompleted(exercise: viewModel.currentExercise, articulation: art)

                    Button {
                        viewModel.selectChromaticArticulation(art, markPreviousCompleted: false)
                        navigateToPractice = true
                    } label: {
                        HStack(spacing: 12) {
                            VStack(alignment: .leading, spacing: 2) {
                                Text(art.title)
                                    .font(.subheadline.weight(isSelected ? .bold : .semibold))
                                    .foregroundColor(.primary)
                                    .multilineTextAlignment(.leading)
                                Text(art.formulaBadge)
                                    .font(.caption2.monospaced())
                                    .foregroundColor(.secondary)
                            }

                            Spacer()

                            if art == .original {
                                Text("Urtext")
                                    .font(.caption2.bold())
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 3)
                                    .background(Color.indigo.opacity(0.15))
                                    .foregroundColor(.indigo)
                                    .cornerRadius(6)
                            } else if isDone {
                                HStack(spacing: 4) {
                                    Image(systemName: "checkmark.circle.fill")
                                        .foregroundColor(.green)
                                    Text(loc.t("completed"))
                                        .font(.caption2.bold())
                                        .foregroundColor(.green)
                                }
                            } else if isSelected {
                                Text(loc.t("in_progress"))
                                    .font(.caption2.bold())
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.orange.opacity(0.15))
                                    .foregroundColor(.orange)
                                    .cornerRadius(6)
                            } else {
                                Image(systemName: "chevron.right")
                                    .font(.caption2.bold())
                                    .foregroundColor(.secondary)
                            }
                        }
                        .padding(.vertical, 10)
                        .padding(.horizontal, 12)
                        .background(isSelected ? Color.primary.opacity(0.05) : Color.clear)
                    }

                    if art.id != EJ1Articulation.allCases.last?.id {
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

    private var majorFamilyCard: some View {
        familyCard(
            title: loc.t("major_family"),
            keyDesc: "\(loc.t("fixed_key")) \(viewModel.currentTonic.majorKey) (\(viewModel.currentTonic.majorDesc))",
            modes: [.ionian, .lydian, .mixolydian]
        )
    }

    private var minorFamilyCard: some View {
        familyCard(
            title: loc.t("minor_family"),
            keyDesc: "\(loc.t("fixed_key")) \(viewModel.currentTonic.minorKey) (\(viewModel.currentTonic.minorDesc))",
            modes: [.dorian, .aeolian, .phrygian, .locrian]
        )
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
                                HStack(spacing: 4) {
                                    Image(systemName: "checkmark.circle.fill")
                                        .foregroundColor(.green)
                                    Text("8/8 \(loc.t("arts_count"))")
                                        .font(.caption2.bold().monospacedDigit())
                                        .foregroundColor(.green)
                                }
                            } else if count > 0 {
                                Text("\(count)/8 \(loc.t("arts_count"))")
                                    .font(.caption2.bold().monospacedDigit())
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.orange.opacity(0.15))
                                    .foregroundColor(.orange)
                                    .cornerRadius(6)
                            } else {
                                Text("0/8 \(loc.t("arts_count"))")
                                    .font(.caption2.monospacedDigit())
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
