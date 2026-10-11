package com.seagomezar.flutemodes

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import com.seagomezar.flutemodes.audio.MetronomeEngine
import com.seagomezar.flutemodes.audio.ScoreAudioPlayer
import com.seagomezar.flutemodes.model.*
import com.seagomezar.flutemodes.ui.HomeScreen
import com.seagomezar.flutemodes.ui.PracticeScreen
import com.seagomezar.flutemodes.ui.ProgressMatrixScreen
import com.seagomezar.flutemodes.ui.theme.FluteModesTheme

sealed class Screen {
    object Home : Screen()
    data class Practice(
        val exerciseType: ExerciseType = ExerciseType.EJ1,
        val ej1Articulation: EJ1Articulation = EJ1Articulation.ORIGINAL,
        val ej2Articulation: EJ1Articulation = EJ1Articulation.ORIGINAL,
        val ej4Articulation: EJ4Articulation = EJ4Articulation.ORIGINAL,
        val ej4Section: EJ4Section = EJ4Section.C_MAJOR,
        val ej5Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
        val ej5Section: EJ5Section = EJ5Section.C_CHROM,
        val ej10Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
        val ej10Section: EJ10Section = EJ10Section.C_ARP,
        val ej11Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
        val ej11Section: EJ10Section = EJ10Section.C_ARP,
        val tonic: Tonic = Tonic.DO_NATURAL,
        val mode: ModeType = ModeType.IONIAN
    ) : Screen()
    object Matrix : Screen()
}

class MainActivity : ComponentActivity() {
    private val metronome = MetronomeEngine()
    private val scorePlayer = ScoreAudioPlayer()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val store = PracticeStore(applicationContext)
        val loc = LocalizationManager(applicationContext)

        setContent {
            FluteModesTheme {
                // Keep screen awake if setting is enabled
                LaunchedEffect(store.keepScreenAwake) {
                    if (store.keepScreenAwake) {
                        window.addFlags(android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
                    } else {
                        window.clearFlags(android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
                    }
                }

                Surface(modifier = Modifier.fillMaxSize()) {
                    var currentScreen by remember { mutableStateOf<Screen>(Screen.Home) }

                    BackHandler(enabled = currentScreen !is Screen.Home) {
                        metronome.stop()
                        scorePlayer.stop()
                        currentScreen = Screen.Home
                    }

                    when (val screen = currentScreen) {
                        is Screen.Home -> {
                            HomeScreen(
                                store = store,
                                loc = loc,
                                onStartPractice = { tonic, mode ->
                                    store.lastExerciseType = ExerciseType.MODOS
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ExerciseType.MODOS,
                                        ej1Articulation = store.lastEJ1Articulation,
                                        ej2Articulation = store.lastEJ2Articulation,
                                        ej4Articulation = store.lastEJ4Articulation,
                                        ej4Section = store.lastEJ4Section,
                                        ej5Articulation = store.lastEJ5Articulation,
                                        ej5Section = store.lastEJ5Section,
                                        ej10Articulation = store.lastEJ10Articulation,
                                        ej10Section = store.lastEJ10Section,
                                        ej11Articulation = store.lastEJ11Articulation,
                                        ej11Section = store.lastEJ11Section,
                                        tonic = tonic,
                                        mode = mode
                                    )
                                },
                                onStartEJ1Practice = { art ->
                                    store.lastExerciseType = ExerciseType.EJ1
                                    store.lastEJ1Articulation = art
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ExerciseType.EJ1,
                                        ej1Articulation = art,
                                        ej2Articulation = store.lastEJ2Articulation,
                                        ej4Articulation = store.lastEJ4Articulation,
                                        ej4Section = store.lastEJ4Section,
                                        ej5Articulation = store.lastEJ5Articulation,
                                        ej5Section = store.lastEJ5Section,
                                        ej10Articulation = store.lastEJ10Articulation,
                                        ej10Section = store.lastEJ10Section,
                                        ej11Articulation = store.lastEJ11Articulation,
                                        ej11Section = store.lastEJ11Section,
                                        tonic = store.lastTonic ?: Tonic.DO_NATURAL,
                                        mode = store.lastMode ?: ModeType.IONIAN
                                    )
                                },
                                onStartEJ2Practice = { art ->
                                    store.lastExerciseType = ExerciseType.EJ2
                                    store.lastEJ2Articulation = art
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ExerciseType.EJ2,
                                        ej1Articulation = store.lastEJ1Articulation,
                                        ej2Articulation = art,
                                        ej4Articulation = store.lastEJ4Articulation,
                                        ej4Section = store.lastEJ4Section,
                                        ej5Articulation = store.lastEJ5Articulation,
                                        ej5Section = store.lastEJ5Section,
                                        ej10Articulation = store.lastEJ10Articulation,
                                        ej10Section = store.lastEJ10Section,
                                        ej11Articulation = store.lastEJ11Articulation,
                                        ej11Section = store.lastEJ11Section,
                                        tonic = store.lastTonic ?: Tonic.DO_NATURAL,
                                        mode = store.lastMode ?: ModeType.IONIAN
                                    )
                                },
                                onStartEJ4Practice = { art, sec ->
                                    store.lastExerciseType = ExerciseType.EJ4
                                    store.lastEJ4Articulation = art
                                    store.lastEJ4Section = sec
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ExerciseType.EJ4,
                                        ej1Articulation = store.lastEJ1Articulation,
                                        ej2Articulation = store.lastEJ2Articulation,
                                        ej4Articulation = art,
                                        ej4Section = sec,
                                        ej5Articulation = store.lastEJ5Articulation,
                                        ej5Section = store.lastEJ5Section,
                                        ej10Articulation = store.lastEJ10Articulation,
                                        ej10Section = store.lastEJ10Section,
                                        ej11Articulation = store.lastEJ11Articulation,
                                        ej11Section = store.lastEJ11Section,
                                        tonic = store.lastTonic ?: Tonic.DO_NATURAL,
                                        mode = store.lastMode ?: ModeType.IONIAN
                                    )
                                },
                                onStartEJ5Practice = { art, sec ->
                                    store.lastExerciseType = ExerciseType.EJ5
                                    store.lastEJ5Articulation = art
                                    store.lastEJ5Section = sec
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ExerciseType.EJ5,
                                        ej1Articulation = store.lastEJ1Articulation,
                                        ej2Articulation = store.lastEJ2Articulation,
                                        ej4Articulation = store.lastEJ4Articulation,
                                        ej4Section = store.lastEJ4Section,
                                        ej5Articulation = art,
                                        ej5Section = sec,
                                        ej10Articulation = store.lastEJ10Articulation,
                                        ej10Section = store.lastEJ10Section,
                                        ej11Articulation = store.lastEJ11Articulation,
                                        ej11Section = store.lastEJ11Section,
                                        tonic = store.lastTonic ?: Tonic.DO_NATURAL,
                                        mode = store.lastMode ?: ModeType.IONIAN
                                    )
                                },
                                onStartEJ10Practice = { art, sec ->
                                    store.lastExerciseType = ExerciseType.EJ10
                                    store.lastEJ10Articulation = art
                                    store.lastEJ10Section = sec
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ExerciseType.EJ10,
                                        ej1Articulation = store.lastEJ1Articulation,
                                        ej2Articulation = store.lastEJ2Articulation,
                                        ej4Articulation = store.lastEJ4Articulation,
                                        ej4Section = store.lastEJ4Section,
                                        ej5Articulation = store.lastEJ5Articulation,
                                        ej5Section = store.lastEJ5Section,
                                        ej10Articulation = art,
                                        ej10Section = sec,
                                        ej11Articulation = store.lastEJ11Articulation,
                                        ej11Section = store.lastEJ11Section,
                                        tonic = store.lastTonic ?: Tonic.DO_NATURAL,
                                        mode = store.lastMode ?: ModeType.IONIAN
                                    )
                                },
                                onStartEJ11Practice = { art, sec ->
                                    store.lastExerciseType = ExerciseType.EJ11
                                    store.lastEJ11Articulation = art
                                    store.lastEJ11Section = sec
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ExerciseType.EJ11,
                                        ej1Articulation = store.lastEJ1Articulation,
                                        ej2Articulation = store.lastEJ2Articulation,
                                        ej4Articulation = store.lastEJ4Articulation,
                                        ej4Section = store.lastEJ4Section,
                                        ej5Articulation = store.lastEJ5Articulation,
                                        ej5Section = store.lastEJ5Section,
                                        ej10Articulation = store.lastEJ10Articulation,
                                        ej10Section = store.lastEJ10Section,
                                        ej11Articulation = art,
                                        ej11Section = sec,
                                        tonic = store.lastTonic ?: Tonic.DO_NATURAL,
                                        mode = store.lastMode ?: ModeType.IONIAN
                                    )
                                },
                                onStartReichertPractice = { ex ->
                                    store.lastExerciseType = ex
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ex,
                                        ej1Articulation = store.lastEJ1Articulation,
                                        ej2Articulation = store.lastEJ2Articulation,
                                        ej4Articulation = store.lastEJ4Articulation,
                                        ej4Section = store.lastEJ4Section,
                                        ej5Articulation = store.lastEJ5Articulation,
                                        ej5Section = store.lastEJ5Section,
                                        ej10Articulation = store.lastEJ10Articulation,
                                        ej10Section = store.lastEJ10Section,
                                        ej11Articulation = store.lastEJ11Articulation,
                                        ej11Section = store.lastEJ11Section,
                                        tonic = store.lastTonic ?: Tonic.DO_NATURAL,
                                        mode = store.lastMode ?: ModeType.IONIAN
                                    )
                                },
                                onOpenMatrix = {
                                    currentScreen = Screen.Matrix
                                }
                            )
                        }
                        is Screen.Practice -> {
                            PracticeScreen(
                                initialExercise = screen.exerciseType,
                                initialEJ1Articulation = screen.ej1Articulation,
                                initialEJ2Articulation = screen.ej2Articulation,
                                initialEJ4Articulation = screen.ej4Articulation,
                                initialEJ4Section = screen.ej4Section,
                                initialEJ5Articulation = screen.ej5Articulation,
                                initialEJ5Section = screen.ej5Section,
                                initialEJ10Articulation = screen.ej10Articulation,
                                initialEJ10Section = screen.ej10Section,
                                initialEJ11Articulation = screen.ej11Articulation,
                                initialEJ11Section = screen.ej11Section,
                                initialTonic = screen.tonic,
                                initialMode = screen.mode,
                                store = store,
                                loc = loc,
                                metronome = metronome,
                                scorePlayer = scorePlayer,
                                onBack = {
                                    metronome.stop()
                                    scorePlayer.stop()
                                    currentScreen = Screen.Home
                                },
                                onOpenMatrix = {
                                    metronome.stop()
                                    scorePlayer.stop()
                                    currentScreen = Screen.Matrix
                                }
                            )
                        }
                        is Screen.Matrix -> {
                            ProgressMatrixScreen(
                                store = store,
                                loc = loc,
                                onSelectCell = { tonic, mode ->
                                    store.lastExerciseType = ExerciseType.MODOS
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ExerciseType.MODOS,
                                        ej1Articulation = store.lastEJ1Articulation,
                                        ej2Articulation = store.lastEJ2Articulation,
                                        ej4Articulation = store.lastEJ4Articulation,
                                        ej4Section = store.lastEJ4Section,
                                        ej5Articulation = store.lastEJ5Articulation,
                                        ej5Section = store.lastEJ5Section,
                                        ej10Articulation = store.lastEJ10Articulation,
                                        ej10Section = store.lastEJ10Section,
                                        ej11Articulation = store.lastEJ11Articulation,
                                        ej11Section = store.lastEJ11Section,
                                        tonic = tonic,
                                        mode = mode
                                    )
                                },
                                onBack = {
                                    currentScreen = Screen.Home
                                }
                            )
                        }
                    }
                }
            }
        }
    }

    override fun onStop() {
        super.onStop()
        metronome.stop()
        scorePlayer.stop()
    }

    override fun onDestroy() {
        super.onDestroy()
        metronome.release()
        scorePlayer.stop()
    }
}
