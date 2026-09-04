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
    data class Practice(val tonic: Tonic, val mode: ModeType) : Screen()
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
                                    currentScreen = Screen.Practice(tonic, mode)
                                },
                                onOpenMatrix = {
                                    currentScreen = Screen.Matrix
                                }
                            )
                        }
                        is Screen.Practice -> {
                            PracticeScreen(
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
                                    currentScreen = Screen.Practice(tonic, mode)
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
