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
                                    store.lastExerciseType = ExerciseType.EJ4
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ExerciseType.EJ4,
                                        ej1Articulation = store.lastEJ1Articulation,
                                        ej2Articulation = store.lastEJ2Articulation,
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
                                    store.lastExerciseType = ExerciseType.EJ4
                                    store.saveLastSelection()
                                    currentScreen = Screen.Practice(
                                        exerciseType = ExerciseType.EJ4,
                                        ej1Articulation = store.lastEJ1Articulation,
                                        ej2Articulation = store.lastEJ2Articulation,
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
        scorePlayer.release()
    }
}
