import SwiftUI

public struct HomeView: View {
    @ObservedObject var viewModel: PracticeViewModel
    @ObservedObject var loc = LocalizationManager.shared
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass
    @State private var navigateToPractice = false
    @State private var navigateToMatrix = false
    @State private var didHandleLaunchArgs = false

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
                        VStack(spacing: 12) {
                            if !isCompact {
                                Text(loc.t("app_name"))
                                    .font(.system(size: 32, weight: .bold))
                                    .foregroundColor(.primary)
                            }

                            // OPCIÓN 1: CONSERVATORY COACH HERO CARD & WIZARD LAUNCHER
                            conservatoryCoachHeroCard

                            // 3-Collection Exercise Selector (All 11 exercises visible on screen without horizontal scroll)
                            VStack(alignment: .leading, spacing: 10) {
                                // 1. Taffanel & Gaubert — 6 Exercises in 2 rows of 3
                                VStack(alignment: .leading, spacing: 5) {
                                    HStack(spacing: 5) {
                                        Image(systemName: "music.quarternote.3")
                                            .font(.caption2.bold())
                                            .foregroundColor(.secondary)
                                        Text("TAFFANEL & GAUBERT")
                                            .font(.system(size: 10.5, weight: .bold))
                                            .foregroundColor(.secondary)
                                    }
                                    .padding(.horizontal, 4)

                                    LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 6), count: 3), spacing: 6) {
                                        ForEach([ExerciseType.ej1, .ej2, .ej4, .ej5, .ej10, .ej11]) { exercise in
                                            exerciseGridButton(exercise)
                                        }
                                    }
                                }

                                // 2. M.-A. Reichert Op. 5 — 4 Exercises in 2 rows of 2 (or 4 columns)
                                VStack(alignment: .leading, spacing: 5) {
                                    HStack(spacing: 5) {
                                        Image(systemName: "music.note.list")
                                            .font(.caption2.bold())
                                            .foregroundColor(.indigo)
                                        Text("M.-A. REICHERT · OP. 5")
                                            .font(.system(size: 10.5, weight: .bold))
                                            .foregroundColor(.indigo)
                                    }
                                    .padding(.horizontal, 4)

                                    LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 6), count: isCompact ? 2 : 4), spacing: 6) {
                                        ForEach([ExerciseType.r1, .r2, .r4, .r5]) { exercise in
                                            exerciseGridButton(exercise, isReichert: true)
                                        }
                                    }
                                }

                                // 3. Sistema Modal Paralelo (84 Modos)
                                Button {
                                    withAnimation(.easeInOut(duration: 0.2)) {
                                        viewModel.selectExercise(.modos)
                                    }
                                } label: {
                                    let isSelected = viewModel.currentExercise == .modos
                                    HStack(spacing: 8) {
                                        Image(systemName: "dial.medium.fill")
                                            .font(.caption.bold())
                                        Text(ExerciseType.modos.homeButtonTitle)
                                            .font(.system(size: 13, weight: .bold))
                                            .lineLimit(1)
                                            .minimumScaleFactor(0.75)
                                        Spacer()
                                        Text(ExerciseType.modos.homeButtonSubtitle)
                                            .font(.system(size: 10.5, weight: .semibold))
                                            .opacity(0.8)
                                            .lineLimit(1)
                                            .minimumScaleFactor(0.8)
                                    }
                                    .padding(.vertical, 9)
                                    .padding(.horizontal, 12)
                                    .frame(maxWidth: .infinity)
                                    .background(isSelected ? Color.primary : Color(uiColor: .secondarySystemGroupedBackground))
                                    .foregroundColor(isSelected ? Color(uiColor: .systemBackground) : .primary)
                                    .cornerRadius(12)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 12)
                                            .stroke(isSelected ? Color.clear : Color(uiColor: .separator), lineWidth: 1)
                                    )
                                }
                            }

                            Text(headerTitle)
                                .font(isCompact ? .subheadline.weight(.semibold) : .headline)
                                .foregroundColor(.primary)
                                .multilineTextAlignment(.center)
                                .padding(.top, 2)

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
                        } else if viewModel.currentExercise.isEJ4Exercise {
                            let ex = viewModel.currentExercise
                            let secTitleKey = ex == .r2 ? "r2_select_section" : (ex == .r4 ? "r4_select_section" : "ej4_select_section")
                            let startBtnKey = ex == .r2 ? "r2_start_practice" : (ex == .r4 ? "r4_start_practice" : "ej4_start_practice")
                            let curSecIdx = viewModel.currentEJ4TypeSectionIndex
                            let curArt = viewModel.currentEJ4TypeArticulation

                            VStack(alignment: .leading, spacing: 10) {
                                Text(loc.t(secTitleKey).uppercased())
                                    .font(.caption.bold())
                                    .foregroundColor(.secondary)
                                    .padding(.horizontal, 4)

                                ScrollView(.horizontal, showsIndicators: false) {
                                    HStack(spacing: 8) {
                                        ForEach(EJ4Section.all) { sec in
                                            let isSelected = curSecIdx == sec.id
                                            Button {
                                                viewModel.selectEJ4Section(sec.id, for: ex)
                                            } label: {
                                                VStack(spacing: 2) {
                                                    Text(sec.shortName(for: ex))
                                                        .font(.system(size: 13, weight: isSelected ? .bold : .semibold))
                                                    Text(sec.measureRange(for: ex))
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
                                let curSec = EJ4Section.all[max(0, min(24, curSecIdx))]
                                Button {
                                    navigateToPractice = true
                                } label: {
                                    HStack(spacing: 10) {
                                        Image(systemName: "play.fill")
                                        Text("\(loc.t(startBtnKey)) (\(curSec.shortName(for: ex)) · \(curArt.shortTitle))")
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
                            let secTitleKey: String = {
                                switch ex {
                                case .ej5:  return "ej5_select_section"
                                case .ej10: return "ej10_select_section"
                                case .ej11: return "ej11_select_section"
                                case .r1:   return "r1_select_section"
                                case .r5:   return "r5_select_section"
                                default:    return "ej5_select_section"
                                }
                            }()
                            let startBtnKey: String = {
                                switch ex {
                                case .ej5:  return "ej5_start_practice"
                                case .ej10: return "ej10_start_practice"
                                case .ej11: return "ej11_start_practice"
                                case .r1:   return "r1_start_practice"
                                case .r5:   return "r5_start_practice"
                                default:    return "ej5_start_practice"
                                }
                            }()
                            let curSecIdx = viewModel.currentEJ5TypeSectionIndex
                            let curShortName: String = {
                                if ex.isReichertExercise {
                                    return EJ4Section.all[max(0, min(24, curSecIdx))].shortName(for: ex)
                                }
                                return ex == .ej5 ? EJ5Section.all[curSecIdx].shortName : EJ10Section.all[curSecIdx].shortName
                            }()

                            VStack(alignment: .leading, spacing: 10) {
                                Text(loc.t(secTitleKey).uppercased())
                                    .font(.caption.bold())
                                    .foregroundColor(.secondary)
                                    .padding(.horizontal, 4)

                                ScrollView(.horizontal, showsIndicators: false) {
                                    HStack(spacing: 8) {
                                        ForEach(0..<ex.sectionCount, id: \.self) { idx in
                                            let isSelected = curSecIdx == idx
                                            let shortName = ex.isReichertExercise
                                                ? EJ4Section.all[idx].shortName(for: ex)
                                                : (ex == .ej5 ? EJ5Section.all[idx].shortName : EJ10Section.all[idx].shortName)
                                            let mRange = ex.isReichertExercise
                                                ? EJ4Section.all[idx].measureRange(for: ex)
                                                : (ex == .ej5 ? EJ5Section.all[idx].measureRange : EJ10Section.all[idx].measureRange)
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
                            // 3-LEVEL MODES EXPLORER (84 Parallel Modes × 10 Technical Schemes = 840 Variations)
                            // LEVEL 1: SELECT TONIC (12 Chromatic Tonics)
                            VStack(alignment: .leading, spacing: 8) {
                                Text(CoachStrings.level1TonicLabel(loc))
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

                            // LEVEL 2: SELECT PARALLEL MODE (7 Modes)
                            VStack(alignment: .leading, spacing: 8) {
                                Text(CoachStrings.level2ModeLabel(loc))
                                    .font(.caption.bold())
                                    .foregroundColor(.secondary)
                                    .padding(.horizontal, 4)

                                ScrollView(.horizontal, showsIndicators: false) {
                                    HStack(spacing: 8) {
                                        ForEach(ModeType.allCases) { mode in
                                            let isSelected = viewModel.currentMode == mode
                                            Button {
                                                viewModel.selectMode(tonic: viewModel.currentTonic, mode: mode)
                                            } label: {
                                                Text("\(mode.rawValue). \(mode.localizedName)")
                                                    .font(.system(size: 13, weight: isSelected ? .bold : .semibold))
                                                    .padding(.horizontal, 14)
                                                    .padding(.vertical, 8)
                                                    .background(isSelected ? Color.indigo : Color(uiColor: .secondarySystemGroupedBackground))
                                                    .foregroundColor(isSelected ? .white : .primary)
                                                    .cornerRadius(16)
                                                    .overlay(
                                                        RoundedRectangle(cornerRadius: 16)
                                                            .stroke(isSelected ? Color.clear : Color(uiColor: .separator), lineWidth: 1)
                                                    )
                                            }
                                        }
                                    }
                                }
                            }

                            // LEVEL 3: SELECT TECHNICAL SCHEME (10 Schemes: Taffanel E.J. 1-11 & Reichert R. 1-5)
                            modalSchemesSelectorCard

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
                                    navigateToPractice = true
                                } label: {
                                    HStack(spacing: 10) {
                                        Image(systemName: "play.fill")
                                        Text("\(loc.t("start_practice")) (\(viewModel.currentTonic.rawValue) \(viewModel.currentMode.localizedName) · \(viewModel.currentModalScheme.shortName))")
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
            .sheet(isPresented: $viewModel.showPracticeWizard) {
                practiceWizardSheet
            }
            .onAppear {
                guard !didHandleLaunchArgs else { return }
                didHandleLaunchArgs = true
                for arg in CommandLine.arguments {
                    if arg.hasPrefix("exercise=") || arg.hasPrefix("-exercise=") {
                        if let valStr = arg.split(separator: "=").last,
                           let ex = ExerciseType(rawValue: String(valStr).uppercased()) {
                            viewModel.selectExercise(ex)
                        }
                    } else if arg.hasPrefix("ej1Art=") || arg.hasPrefix("-ej1Art=") {
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
                    } else if arg.hasPrefix("modalScheme=") || arg.hasPrefix("-modalScheme=") {
                        if let valStr = arg.split(separator: "=").last,
                           let scheme = ModalScheme(rawValue: String(valStr).lowercased()) {
                            viewModel.selectExercise(.modos)
                            viewModel.selectModalScheme(scheme)
                        }
                    }
                }
                if CommandLine.arguments.contains("-openWizard") || CommandLine.arguments.contains("openWizard") {
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                        viewModel.showPracticeWizard = true
                    }
                } else if CommandLine.arguments.contains("-openPractice") || CommandLine.arguments.contains("openPractice") {
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

    @ViewBuilder
    private func exerciseGridButton(_ exercise: ExerciseType, isReichert: Bool = false) -> some View {
        let isSelected = viewModel.currentExercise == exercise
        Button {
            withAnimation(.easeInOut(duration: 0.2)) {
                viewModel.selectExercise(exercise)
            }
        } label: {
            VStack(spacing: 2) {
                Text(exercise.homeButtonTitle)
                    .font(.system(size: isCompact ? 12.5 : 13.5, weight: .bold))
                    .lineLimit(1)
                    .minimumScaleFactor(0.85)
                Text(exercise.homeButtonSubtitle)
                    .font(.system(size: isCompact ? 9.5 : 10.5, weight: .medium))
                    .opacity(isSelected ? 0.9 : 0.72)
                    .lineLimit(1)
                    .minimumScaleFactor(0.8)
            }
            .padding(.vertical, 7)
            .padding(.horizontal, 6)
            .frame(maxWidth: .infinity)
            .background(
                isSelected
                    ? (isReichert ? Color.indigo : Color.primary)
                    : Color(uiColor: .secondarySystemGroupedBackground)
            )
            .foregroundColor(
                isSelected
                    ? (isReichert ? Color.white : Color(uiColor: .systemBackground))
                    : .primary
            )
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(
                        isSelected
                            ? Color.clear
                            : (isReichert ? Color.indigo.opacity(0.35) : Color(uiColor: .separator)),
                        lineWidth: 1
                    )
            )
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
        case .r1: return loc.t("r1_title")
        case .r2: return loc.t("r2_title")
        case .r4: return loc.t("r4_title")
        case .r5: return loc.t("r5_title")
        case .modos: return viewModel.currentModalScheme.title(loc)
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
        case .r1: return loc.t("r1_sub_desc")
        case .r2: return loc.t("r2_sub_desc")
        case .r4: return loc.t("r4_sub_desc")
        case .r5: return loc.t("r5_sub_desc")
        case .modos: return loc.t("sub_desc")
        }
    }

    private var ej5TypeArticulationsCard: some View {
        let ex = viewModel.currentExercise
        let completedCount = viewModel.store.ej5TypeCompletedCount(for: ex)
        let isAllDone = viewModel.store.isEJ5TypeFullyCompleted(for: ex)
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
        let headerInfoKey: String = {
            switch ex {
            case .ej5:  return "ej5_header_info"
            case .ej10: return "ej10_header_info"
            case .ej11: return "ej11_header_info"
            case .r1:   return "r1_header_info"
            case .r5:   return "r5_header_info"
            default:    return "ej5_header_info"
            }
        }()

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
                                Text("Original")
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
        let ex = viewModel.currentExercise
        let completedCount = viewModel.store.ej4TypeCompletedCount(for: ex)
        let isAllDone = viewModel.store.isEJ4TypeFullyCompleted(for: ex)
        let selectArtKey = ex == .r2 ? "r2_select_art" : (ex == .r4 ? "r4_select_art" : "ej4_select_art")
        let headerInfoKey = ex == .r2 ? "r2_header_info" : (ex == .r4 ? "r4_header_info" : "ej4_header_info")

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
                    let isSelected = viewModel.currentEJ4TypeArticulation == art
                    let isDone = viewModel.store.isEJ4Completed(art, for: ex)

                    Button {
                        viewModel.selectEJ4Articulation(art, for: ex, markPreviousCompleted: false)
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
                                Text("Original")
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
                                Text("Original")
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
                                Text("\(mode.rawValue). \(mode.localizedName)")
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

    // MARK: - Opción 1: Conservatory Coach Hero Card & 3-Step Practice Wizard
    private var currentSessionSummary: String {
        switch viewModel.currentExercise {
        case .ej1, .ej2:
            return "\(viewModel.currentExercise.shortBadge) · \(viewModel.currentChromaticArticulation.shortTitle)"
        case .ej4, .r2, .r4:
            let sec = EJ4Section.all[max(0, min(24, viewModel.currentEJ4TypeSectionIndex))]
            return "\(viewModel.currentExercise.shortBadge) · \(sec.shortName(for: viewModel.currentExercise))"
        case .ej5, .ej10, .ej11, .r1, .r5:
            let idx = viewModel.currentEJ5TypeSectionIndex
            let secName = viewModel.currentExercise.isReichertExercise
                ? EJ4Section.all[max(0, min(24, idx))].shortName(for: viewModel.currentExercise)
                : (viewModel.currentExercise == .ej5 ? EJ5Section.all[idx].shortName : EJ10Section.all[idx].shortName)
            return "\(viewModel.currentExercise.shortBadge) · \(secName)"
        case .modos:
            return "\(viewModel.currentTonic.rawValue) \(viewModel.currentMode.localizedName) · \(viewModel.currentModalScheme.shortName)"
        }
    }

    private var conservatoryCoachHeroCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .center, spacing: 6) {
                Text(CoachStrings.coachBadge(loc))
                    .font(.system(size: 8.5, weight: .heavy))
                    .lineLimit(1)
                    .minimumScaleFactor(0.6)
                    .padding(.horizontal, 7)
                    .padding(.vertical, 4)
                    .background(Color.indigo.opacity(0.18))
                    .foregroundColor(.indigo)
                    .cornerRadius(999)

                Spacer(minLength: 4)

                Button {
                    viewModel.showPracticeWizard = true
                } label: {
                    HStack(spacing: 3) {
                        Image(systemName: "sparkles")
                            .font(.system(size: 9.5, weight: .bold))
                        Text(CoachStrings.openWizardBtn(loc))
                            .font(.system(size: 10, weight: .bold))
                            .lineLimit(1)
                            .minimumScaleFactor(0.75)
                    }
                    .padding(.horizontal, 8)
                    .padding(.vertical, 5)
                    .background(Color.indigo)
                    .foregroundColor(.white)
                    .cornerRadius(999)
                }
                .fixedSize(horizontal: true, vertical: false)
            }

            VStack(alignment: .leading, spacing: 4) {
                Text(CoachStrings.coachTitle(loc))
                    .font(isCompact ? .headline.weight(.bold) : .title3.weight(.bold))
                    .foregroundColor(.primary)
                Text(CoachStrings.coachSubtitle(loc))
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .fixedSize(horizontal: false, vertical: true)
            }

            // 1-Tap Resume Banner ("Continuar última sesión")
            Button {
                navigateToPractice = true
            } label: {
                HStack(spacing: 10) {
                    Image(systemName: "play.circle.fill")
                        .font(.title3)
                        .foregroundColor(.green)
                    VStack(alignment: .leading, spacing: 1) {
                        Text(CoachStrings.resumeBannerTitle(loc))
                            .font(.system(size: 9.5, weight: .bold))
                            .foregroundColor(.green)
                        Text(currentSessionSummary)
                            .font(.subheadline.weight(.bold))
                            .foregroundColor(.primary)
                            .lineLimit(1)
                            .minimumScaleFactor(0.8)
                    }
                    Spacer()
                    HStack(spacing: 4) {
                        Text(CoachStrings.resumeAction(loc))
                            .font(.caption.bold())
                        Image(systemName: "arrow.right")
                            .font(.caption.bold())
                    }
                    .padding(.horizontal, 10)
                    .padding(.vertical, 5)
                    .background(Color.green.opacity(0.16))
                    .foregroundColor(.green)
                    .cornerRadius(999)
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 10)
                .background(Color(uiColor: .systemBackground))
                .cornerRadius(12)
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(Color.green.opacity(0.35), lineWidth: 1)
                )
            }

            // 3 Quick Time / Routine Preset Cards (15m Express, 30m Conservatorio, 45m Maestría)
            HStack(spacing: 6) {
                ForEach(PracticeWizardDuration.allCases) { dur in
                    let isSelected = viewModel.wizardDuration == dur
                    Button {
                        viewModel.wizardDuration = dur
                        viewModel.showPracticeWizard = true
                    } label: {
                        VStack(alignment: .leading, spacing: 3) {
                            HStack(spacing: 3) {
                                Image(systemName: "clock.fill")
                                    .font(.system(size: 9))
                                    .foregroundColor(.indigo)
                                Text(dur.presetTitle(loc))
                                    .font(.system(size: 10.5, weight: .bold))
                                    .foregroundColor(.primary)
                                    .lineLimit(1)
                                    .minimumScaleFactor(0.68)
                            }
                            Text(dur.subtitle(loc))
                                .font(.system(size: 9))
                                .foregroundColor(.secondary)
                                .lineLimit(2)
                                .minimumScaleFactor(0.75)
                                .multilineTextAlignment(.leading)
                        }
                        .padding(.horizontal, 7)
                        .padding(.vertical, 8)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(isSelected ? Color.indigo.opacity(0.12) : Color(uiColor: .systemBackground))
                        .cornerRadius(10)
                        .overlay(
                            RoundedRectangle(cornerRadius: 10)
                                .stroke(isSelected ? Color.indigo : Color(uiColor: .separator), lineWidth: 1)
                        )
                    }
                }
            }
        }
        .padding(14)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(
            LinearGradient(
                colors: [Color.indigo.opacity(0.10), Color(uiColor: .secondarySystemGroupedBackground)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        )
        .cornerRadius(18)
        .overlay(
            RoundedRectangle(cornerRadius: 18)
                .stroke(Color.indigo.opacity(0.35), lineWidth: 1)
        )
    }

    // MARK: - Level 3: 10 Modal Technical Schemes Card (6 Taffanel + 4 Reichert = 840 Variations)
    private var modalSchemesSelectorCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Text(CoachStrings.level3SchemeLabel(loc))
                    .font(.caption.bold())
                    .foregroundColor(.secondary)
                Spacer()
                Text("\(viewModel.currentModalScheme.totalNotes) notes · M:\(viewModel.currentModalScheme.meter)")
                    .font(.caption2.bold().monospacedDigit())
                    .padding(.horizontal, 8)
                    .padding(.vertical, 3)
                    .background(Color.indigo.opacity(0.14))
                    .foregroundColor(.indigo)
                    .cornerRadius(8)
            }
            .padding(.horizontal, 4)

            VStack(alignment: .leading, spacing: 10) {
                // Taffanel & Gaubert (6 Schemes: E.J. 1, 2, 4, 5, 10, 11)
                VStack(alignment: .leading, spacing: 6) {
                    Text(CoachStrings.taffanelGroupLabel(loc))
                        .font(.system(size: 11, weight: .semibold))
                        .foregroundColor(.secondary)

                    LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 6), count: isCompact ? 3 : 6), spacing: 6) {
                        ForEach(ModalScheme.taffanelSchemes) { scheme in
                            modalSchemeChip(scheme)
                        }
                    }
                }

                // Reichert Op. 5 (4 Schemes: R. 1, 2, 4, 5)
                VStack(alignment: .leading, spacing: 6) {
                    Text(CoachStrings.reichertGroupLabel(loc))
                        .font(.system(size: 11, weight: .semibold))
                        .foregroundColor(.indigo)

                    LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 6), count: 4), spacing: 6) {
                        ForEach(ModalScheme.reichertSchemes) { scheme in
                            modalSchemeChip(scheme)
                        }
                    }
                }

                Divider()

                // Active Scheme Pedagogical Description
                HStack(alignment: .top, spacing: 10) {
                    Image(systemName: viewModel.currentModalScheme.isReichert ? "sparkles" : "music.quarternote.3")
                        .font(.subheadline.bold())
                        .foregroundColor(viewModel.currentModalScheme.isReichert ? .indigo : .accentColor)
                        .padding(.top, 2)

                    VStack(alignment: .leading, spacing: 2) {
                        Text(viewModel.currentModalScheme.title(loc))
                            .font(.subheadline.bold())
                            .foregroundColor(.primary)
                        Text(viewModel.currentModalScheme.pedagogy(loc))
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }

                    Spacer()
                }
            }
            .padding(12)
            .background(Color(uiColor: .secondarySystemGroupedBackground))
            .cornerRadius(14)
            .overlay(
                RoundedRectangle(cornerRadius: 14)
                    .stroke(Color(uiColor: .separator), lineWidth: 0.5)
            )
        }
    }

    private func modalSchemeChip(_ scheme: ModalScheme) -> some View {
        let isSelected = viewModel.currentModalScheme == scheme
        let activeColor: Color = scheme.isReichert ? .indigo : .primary
        let activeFg: Color = scheme.isReichert ? .white : Color(uiColor: .systemBackground)

        return Button {
            viewModel.selectModalScheme(scheme)
        } label: {
            VStack(spacing: 2) {
                Text(scheme.shortName)
                    .font(.system(size: 12.5, weight: .bold))
                Text("M:\(scheme.meter)")
                    .font(.system(size: 9.5, weight: .medium).monospacedDigit())
                    .opacity(0.8)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 7)
            .background(isSelected ? activeColor : Color(uiColor: .systemBackground))
            .foregroundColor(isSelected ? activeFg : .primary)
            .cornerRadius(10)
            .overlay(
                RoundedRectangle(cornerRadius: 10)
                    .stroke(isSelected ? Color.clear : Color(uiColor: .separator), lineWidth: 1)
            )
        }
    }

    // MARK: - 3-Step Practice Wizard Sheet
    private var practiceWizardSheet: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 18) {
                    // Header
                    VStack(alignment: .leading, spacing: 4) {
                        Text(CoachStrings.coachBadge(loc))
                            .font(.caption2.bold())
                            .foregroundColor(.indigo)
                        Text(CoachStrings.coachTitle(loc))
                            .font(.title3.bold())
                        Text(CoachStrings.coachSubtitle(loc))
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }

                    // STEP 1: Available Time (15m / 30m / 45m)
                    VStack(alignment: .leading, spacing: 8) {
                        Text(CoachStrings.step1Title(loc))
                            .font(.caption.bold())
                            .foregroundColor(.secondary)

                        HStack(spacing: 8) {
                            ForEach(PracticeWizardDuration.allCases) { dur in
                                let isSelected = viewModel.wizardDuration == dur
                                Button {
                                    viewModel.wizardDuration = dur
                                } label: {
                                    Text(dur.label(loc))
                                        .font(.headline.bold())
                                        .frame(maxWidth: .infinity)
                                        .padding(.vertical, 12)
                                        .background(isSelected ? Color.indigo : Color(uiColor: .secondarySystemGroupedBackground))
                                        .foregroundColor(isSelected ? .white : .primary)
                                        .cornerRadius(12)
                                }
                            }
                        }
                    }

                    // STEP 2: Technical Focus
                    VStack(alignment: .leading, spacing: 8) {
                        Text(CoachStrings.step2Title(loc))
                            .font(.caption.bold())
                            .foregroundColor(.secondary)

                        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 8) {
                            ForEach(PracticeWizardFocus.allCases) { focus in
                                let isSelected = viewModel.wizardFocus == focus
                                Button {
                                    viewModel.wizardFocus = focus
                                } label: {
                                    VStack(alignment: .leading, spacing: 4) {
                                        HStack(spacing: 4) {
                                            Image(systemName: focus.iconName)
                                                .font(.caption.bold())
                                            Spacer(minLength: 2)
                                            Text(focus.badgeCode)
                                                .font(.system(size: 9, weight: .bold).monospaced())
                                                .lineLimit(1)
                                                .minimumScaleFactor(0.72)
                                        }
                                        Text(focus.title(loc))
                                            .font(.system(size: 13, weight: .bold))
                                            .lineLimit(1)
                                            .minimumScaleFactor(0.72)
                                        Text(focus.subtitle(loc))
                                            .font(.caption2)
                                            .opacity(0.85)
                                            .lineLimit(2)
                                            .minimumScaleFactor(0.8)
                                            .multilineTextAlignment(.leading)
                                    }
                                    .padding(10)
                                    .frame(maxWidth: .infinity, alignment: .leading)
                                    .background(isSelected ? Color.indigo : Color(uiColor: .secondarySystemGroupedBackground))
                                    .foregroundColor(isSelected ? .white : .primary)
                                    .cornerRadius(12)
                                }
                            }
                        }
                    }

                    // STEP 3: Tonic, Mode & Generated Routine
                    VStack(alignment: .leading, spacing: 10) {
                        Text(CoachStrings.step3Title(loc))
                            .font(.caption.bold())
                            .foregroundColor(.secondary)

                        ScrollView(.horizontal, showsIndicators: false) {
                            HStack(spacing: 6) {
                                ForEach(Tonic.allCases) { tonic in
                                    let isSelected = viewModel.wizardTonic == tonic
                                    Button {
                                        viewModel.wizardTonic = tonic
                                    } label: {
                                        Text(tonic.rawValue)
                                            .font(.caption.bold())
                                            .padding(.horizontal, 12)
                                            .padding(.vertical, 6)
                                            .background(isSelected ? Color.primary : Color(uiColor: .secondarySystemGroupedBackground))
                                            .foregroundColor(isSelected ? Color(uiColor: .systemBackground) : .primary)
                                            .cornerRadius(14)
                                    }
                                }
                            }
                        }

                        ScrollView(.horizontal, showsIndicators: false) {
                            HStack(spacing: 6) {
                                ForEach(ModeType.allCases) { mode in
                                    let isSelected = viewModel.wizardMode == mode
                                    Button {
                                        viewModel.wizardMode = mode
                                    } label: {
                                        Text("\(mode.rawValue). \(mode.localizedName)")
                                            .font(.caption.bold())
                                            .padding(.horizontal, 10)
                                            .padding(.vertical, 6)
                                            .background(isSelected ? Color.indigo : Color(uiColor: .secondarySystemGroupedBackground))
                                            .foregroundColor(isSelected ? .white : .primary)
                                            .cornerRadius(14)
                                    }
                                }
                            }
                        }

                        // 3 Generated Routine Blocks
                        VStack(spacing: 8) {
                            ForEach(viewModel.generatedRoutineBlocks) { block in
                                Button {
                                    viewModel.applyWizardRoutineBlock(block)
                                    navigateToPractice = true
                                } label: {
                                    HStack(spacing: 12) {
                                        VStack(alignment: .leading, spacing: 2) {
                                            HStack(spacing: 6) {
                                                Text(block.phaseTitle)
                                                    .font(.caption.bold())
                                                    .foregroundColor(.indigo)
                                                Text("· \(block.minutes) min")
                                                    .font(.caption2.bold().monospacedDigit())
                                                    .foregroundColor(.secondary)
                                            }
                                            Text(block.exerciseTitle)
                                                .font(.subheadline.bold())
                                                .foregroundColor(.primary)
                                            Text(block.detailSubtitle)
                                                .font(.caption2)
                                                .foregroundColor(.secondary)
                                        }
                                        Spacer()
                                        Image(systemName: "play.circle.fill")
                                            .font(.title3)
                                            .foregroundColor(.indigo)
                                    }
                                    .padding(12)
                                    .background(Color(uiColor: .secondarySystemGroupedBackground))
                                    .cornerRadius(12)
                                }
                            }
                        }
                    }

                    // Primary Launch Button (launches the first block of the routine)
                    Button {
                        if let firstBlock = viewModel.generatedRoutineBlocks.first {
                            viewModel.applyWizardRoutineBlock(firstBlock)
                            navigateToPractice = true
                        }
                    } label: {
                        HStack {
                            Spacer()
                            Text(CoachStrings.launchRoutineBtn(loc))
                                .font(.headline.bold())
                            Spacer()
                        }
                        .padding(.vertical, 14)
                        .background(Color.indigo)
                        .foregroundColor(.white)
                        .cornerRadius(16)
                    }
                }
                .padding(20)
            }
            .navigationTitle("Practice Wizard")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button(loc.t("cancel")) {
                        viewModel.showPracticeWizard = false
                    }
                }
            }
        }
    }
}

