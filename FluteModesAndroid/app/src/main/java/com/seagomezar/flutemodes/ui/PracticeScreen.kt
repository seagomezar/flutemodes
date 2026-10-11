package com.seagomezar.flutemodes.ui

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.seagomezar.flutemodes.audio.MetronomeEngine
import com.seagomezar.flutemodes.audio.ScoreAudioPlayer
import com.seagomezar.flutemodes.model.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PracticeScreen(
    initialExercise: ExerciseType = ExerciseType.EJ1,
    initialEJ1Articulation: EJ1Articulation = EJ1Articulation.ORIGINAL,
    initialEJ2Articulation: EJ1Articulation = EJ1Articulation.ORIGINAL,
    initialEJ4Articulation: EJ4Articulation = EJ4Articulation.ORIGINAL,
    initialEJ4Section: EJ4Section = EJ4Section.C_MAJOR,
    initialEJ5Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
    initialEJ5Section: EJ5Section = EJ5Section.C_CHROM,
    initialEJ10Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
    initialEJ10Section: EJ10Section = EJ10Section.C_ARP,
    initialEJ11Articulation: EJ5Articulation = EJ5Articulation.ORIGINAL,
    initialEJ11Section: EJ10Section = EJ10Section.C_ARP,
    initialTonic: Tonic,
    initialMode: ModeType,
    store: PracticeStore,
    loc: LocalizationManager,
    metronome: MetronomeEngine,
    scorePlayer: ScoreAudioPlayer,
    onBack: () -> Unit,
    onOpenMatrix: () -> Unit
) {
    var currentExercise by remember { mutableStateOf(initialExercise) }
    var currentEJ1Articulation by remember { mutableStateOf(initialEJ1Articulation) }
    var currentEJ2Articulation by remember { mutableStateOf(initialEJ2Articulation) }
    var currentEJ4Articulation by remember { mutableStateOf(initialEJ4Articulation) }
    var currentEJ4Section by remember { mutableStateOf(initialEJ4Section) }
    var currentEJ5Articulation by remember { mutableStateOf(initialEJ5Articulation) }
    var currentEJ5Section by remember { mutableStateOf(initialEJ5Section) }
    var currentEJ10Articulation by remember { mutableStateOf(initialEJ10Articulation) }
    var currentEJ10Section by remember { mutableStateOf(initialEJ10Section) }
    var currentEJ11Articulation by remember { mutableStateOf(initialEJ11Articulation) }
    var currentEJ11Section by remember { mutableStateOf(initialEJ11Section) }
    var currentR1Articulation by remember { mutableStateOf(store.lastR1Articulation) }
    var currentR1Section by remember { mutableStateOf(store.lastR1Section) }
    var currentR2Articulation by remember { mutableStateOf(store.lastR2Articulation) }
    var currentR2Section by remember { mutableStateOf(store.lastR2Section) }
    var currentR4Articulation by remember { mutableStateOf(store.lastR4Articulation) }
    var currentR4Section by remember { mutableStateOf(store.lastR4Section) }
    var currentR5Articulation by remember { mutableStateOf(store.lastR5Articulation) }
    var currentR5Section by remember { mutableStateOf(store.lastR5Section) }
    var currentTonic by remember { mutableStateOf(initialTonic) }
    var currentMode by remember { mutableStateOf(initialMode) }
    var currentArticulation by remember { mutableStateOf(ArticulationPattern.ALL_SLURRED) }
    var showCompletionDialog by remember { mutableStateOf(false) }
    var showEJ1CompletionDialog by remember { mutableStateOf(false) }
    var showEJ2CompletionDialog by remember { mutableStateOf(false) }
    var showEJ4CompletionDialog by remember { mutableStateOf(false) }
    var showEJ5CompletionDialog by remember { mutableStateOf(false) }
    var showEJ10CompletionDialog by remember { mutableStateOf(false) }
    var showEJ11CompletionDialog by remember { mutableStateOf(false) }

    val currentAbcScore = remember(
        currentExercise,
        currentEJ1Articulation,
        currentEJ2Articulation,
        currentEJ4Articulation,
        currentEJ4Section,
        currentEJ5Articulation,
        currentEJ5Section,
        currentEJ10Articulation,
        currentEJ10Section,
        currentEJ11Articulation,
        currentEJ11Section,
        currentR1Articulation,
        currentR1Section,
        currentR2Articulation,
        currentR2Section,
        currentR4Articulation,
        currentR4Section,
        currentR5Articulation,
        currentR5Section,
        currentTonic,
        currentMode,
        currentArticulation,
        metronome.tempoBPM,
        loc.currentLanguage
    ) {
        when (currentExercise) {
            ExerciseType.EJ1 -> ExerciseGenerator.generateEJ1ABC(
                articulation = currentEJ1Articulation,
                tempoBPM = metronome.tempoBPM,
                loc = loc
            )
            ExerciseType.EJ2 -> ExerciseGenerator.generateEJ2ABC(
                articulation = currentEJ2Articulation,
                tempoBPM = metronome.tempoBPM,
                loc = loc
            )
            ExerciseType.EJ4 -> ExerciseGenerator.generateEJ4ABC(
                articulation = currentEJ4Articulation,
                section = currentEJ4Section,
                tempoBPM = metronome.tempoBPM
            )
            ExerciseType.EJ5 -> ExerciseGenerator.generateEJ5ABC(
                articulation = currentEJ5Articulation,
                section = currentEJ5Section,
                tempoBPM = metronome.tempoBPM
            )
            ExerciseType.EJ10 -> ExerciseGenerator.generateEJ10ABC(
                articulation = currentEJ10Articulation,
                section = currentEJ10Section,
                tempoBPM = metronome.tempoBPM
            )
            ExerciseType.EJ11 -> ExerciseGenerator.generateEJ11ABC(
                articulation = currentEJ11Articulation,
                section = currentEJ11Section,
                tempoBPM = metronome.tempoBPM
            )
            ExerciseType.R1 -> ExerciseGenerator.generateR1ABC(
                articulation = currentR1Articulation,
                section = currentR1Section,
                tempoBPM = metronome.tempoBPM
            )
            ExerciseType.R2 -> ExerciseGenerator.generateR2ABC(
                articulation = currentR2Articulation,
                section = currentR2Section,
                tempoBPM = metronome.tempoBPM
            )
            ExerciseType.R4 -> ExerciseGenerator.generateR4ABC(
                articulation = currentR4Articulation,
                section = currentR4Section,
                tempoBPM = metronome.tempoBPM
            )
            ExerciseType.R5 -> ExerciseGenerator.generateR5ABC(
                articulation = currentR5Articulation,
                section = currentR5Section,
                tempoBPM = metronome.tempoBPM
            )
            ExerciseType.MODOS -> ExerciseGenerator.generateABC(
                tonic = currentTonic,
                mode = currentMode,
                articulation = currentArticulation,
                tempoBPM = metronome.tempoBPM,
                loc = loc
            )
        }
    }

    DisposableEffect(Unit) {
        onDispose {
            metronome.stop()
            scorePlayer.stop()
        }
    }

    val practicedModesCount = store.practicedModesCount(currentTonic)
    val areAllModesPracticed = store.areAllSevenModesPracticed(currentTonic)
    val completedArtCount = store.completedArticulationsCount(currentTonic, currentMode)
    val isModeFullyDone = store.isModeFullyCompleted(currentTonic, currentMode)

    val chromaticDoneCount = store.chromaticCompletedCount(currentExercise)
    val isChromaticFullyDone = store.isChromaticFullyCompleted(currentExercise)

    val ej4DoneCount = store.ej4TypeCompletedCount(currentExercise)
    val isEJ4FullyDone = store.isEJ4TypeFullyCompleted(currentExercise)

    val ej5TypeDoneCount = store.ej5TypeCompletedCount(currentExercise)
    val isEJ5TypeFullyDone = store.isEJ5TypeFullyCompleted(currentExercise)

    if (showEJ1CompletionDialog) {
        AlertDialog(
            onDismissRequest = { showEJ1CompletionDialog = false },
            title = {
                Text(
                    text = loc.t("ej1_milestone_title"),
                    fontWeight = FontWeight.Bold
                )
            },
            text = {
                Text(text = loc.t("ej1_milestone_msg"))
            },
            confirmButton = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            store.resetEJ1()
                            currentEJ1Articulation = EJ1Articulation.ALL_SLURRED_8
                            showEJ1CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("ej1_restart_round"))
                    }

                    Button(
                        onClick = {
                            scorePlayer.stop()
                            currentExercise = ExerciseType.EJ2
                            store.lastExerciseType = ExerciseType.EJ2
                            store.saveLastSelection()
                            showEJ1CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(loc.t("ej1_go_to_ej2"))
                    }

                    Button(
                        onClick = {
                            scorePlayer.stop()
                            currentExercise = ExerciseType.EJ4
                            store.lastExerciseType = ExerciseType.EJ4
                            store.saveLastSelection()
                            showEJ1CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.tertiary)
                    ) {
                        Text(loc.t("ej1_go_to_ej4"))
                    }

                    TextButton(
                        onClick = { showEJ1CompletionDialog = false },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("stay_mode"))
                    }
                }
            }
        )
    }

    if (showEJ2CompletionDialog) {
        AlertDialog(
            onDismissRequest = { showEJ2CompletionDialog = false },
            title = {
                Text(
                    text = loc.t("ej2_milestone_title"),
                    fontWeight = FontWeight.Bold
                )
            },
            text = {
                Text(text = loc.t("ej2_milestone_msg"))
            },
            confirmButton = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            store.resetEJ2()
                            currentEJ2Articulation = EJ1Articulation.ALL_SLURRED_8
                            showEJ2CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("ej2_restart_round"))
                    }

                    Button(
                        onClick = {
                            scorePlayer.stop()
                            currentExercise = ExerciseType.EJ4
                            store.lastExerciseType = ExerciseType.EJ4
                            store.saveLastSelection()
                            showEJ2CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(loc.t("ej2_go_to_ej4"))
                    }

                    TextButton(
                        onClick = { showEJ2CompletionDialog = false },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("stay_mode"))
                    }
                }
            }
        )
    }

    if (showEJ4CompletionDialog) {
        AlertDialog(
            onDismissRequest = { showEJ4CompletionDialog = false },
            title = {
                Text(
                    text = "¡${currentExercise.pillLabel} Completado (8/8 Articulaciones)!",
                    fontWeight = FontWeight.Bold
                )
            },
            text = {
                Text(text = loc.t("ej4_milestone_msg"))
            },
            confirmButton = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            store.resetEJ4(currentExercise)
                            when (currentExercise) {
                                ExerciseType.R2 -> {
                                    currentR2Articulation = EJ4Articulation.ALL_SLURRED_8
                                    store.lastR2Articulation = currentR2Articulation
                                }
                                ExerciseType.R4 -> {
                                    currentR4Articulation = EJ4Articulation.ALL_SLURRED_8
                                    store.lastR4Articulation = currentR4Articulation
                                }
                                else -> {
                                    currentEJ4Articulation = EJ4Articulation.ALL_SLURRED_8
                                    store.lastEJ4Articulation = currentEJ4Articulation
                                }
                            }
                            store.saveLastSelection()
                            showEJ4CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("ej4_restart_round"))
                    }

                    Button(
                        onClick = {
                            scorePlayer.stop()
                            val nextEx = when (currentExercise) {
                                ExerciseType.R2 -> ExerciseType.R4
                                ExerciseType.R4 -> ExerciseType.R5
                                else -> ExerciseType.EJ5
                            }
                            currentExercise = nextEx
                            store.lastExerciseType = nextEx
                            store.saveLastSelection()
                            showEJ4CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(
                            when (currentExercise) {
                                ExerciseType.R2 -> loc.t("r4_title")
                                ExerciseType.R4 -> loc.t("r5_title")
                                else -> loc.t("ej5_title")
                            }
                        )
                    }

                    TextButton(
                        onClick = { showEJ4CompletionDialog = false },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("stay_mode"))
                    }
                }
            }
        )
    }

    if (showEJ5CompletionDialog) {
        AlertDialog(
            onDismissRequest = { showEJ5CompletionDialog = false },
            title = {
                Text(
                    text = loc.t("ej5_milestone_title"),
                    fontWeight = FontWeight.Bold
                )
            },
            text = {
                Text(text = loc.t("ej5_milestone_msg"))
            },
            confirmButton = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            store.resetEJ5Type(ExerciseType.EJ5)
                            currentEJ5Articulation = EJ5Articulation.ALL_SLURRED
                            showEJ5CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("ej5_restart_round"))
                    }

                    Button(
                        onClick = {
                            scorePlayer.stop()
                            currentExercise = ExerciseType.EJ10
                            store.lastExerciseType = ExerciseType.EJ10
                            store.saveLastSelection()
                            showEJ5CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(loc.t("ej5_go_to_ej10"))
                    }

                    TextButton(
                        onClick = { showEJ5CompletionDialog = false },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("stay_mode"))
                    }
                }
            }
        )
    }

    if (showEJ10CompletionDialog) {
        AlertDialog(
            onDismissRequest = { showEJ10CompletionDialog = false },
            title = {
                Text(
                    text = loc.t("ej10_milestone_title"),
                    fontWeight = FontWeight.Bold
                )
            },
            text = {
                Text(text = loc.t("ej10_milestone_msg"))
            },
            confirmButton = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            store.resetEJ5Type(ExerciseType.EJ10)
                            currentEJ10Articulation = EJ5Articulation.ALL_SLURRED
                            showEJ10CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("ej10_restart_round"))
                    }

                    Button(
                        onClick = {
                            scorePlayer.stop()
                            currentExercise = ExerciseType.EJ11
                            store.lastExerciseType = ExerciseType.EJ11
                            store.saveLastSelection()
                            showEJ10CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(loc.t("ej10_go_to_ej11"))
                    }

                    TextButton(
                        onClick = { showEJ10CompletionDialog = false },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("stay_mode"))
                    }
                }
            }
        )
    }

    if (showEJ11CompletionDialog) {
        AlertDialog(
            onDismissRequest = { showEJ11CompletionDialog = false },
            title = {
                Text(
                    text = "¡${currentExercise.pillLabel} Completado (10/10 Articulaciones)!",
                    fontWeight = FontWeight.Bold
                )
            },
            text = {
                Text(text = loc.t("ej1_milestone_msg"))
            },
            confirmButton = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            store.resetEJ5Type(currentExercise)
                            when (currentExercise) {
                                ExerciseType.R1 -> {
                                    currentR1Articulation = EJ5Articulation.ALL_SLURRED
                                    store.lastR1Articulation = currentR1Articulation
                                }
                                ExerciseType.R5 -> {
                                    currentR5Articulation = EJ5Articulation.ALL_SLURRED
                                    store.lastR5Articulation = currentR5Articulation
                                }
                                else -> {
                                    currentEJ11Articulation = EJ5Articulation.ALL_SLURRED
                                    store.lastEJ11Articulation = currentEJ11Articulation
                                }
                            }
                            store.saveLastSelection()
                            showEJ11CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("ej1_restart_round"))
                    }

                    Button(
                        onClick = {
                            scorePlayer.stop()
                            val nextEx = when (currentExercise) {
                                ExerciseType.EJ11 -> ExerciseType.R1
                                ExerciseType.R1 -> ExerciseType.R2
                                else -> ExerciseType.MODOS
                            }
                            currentExercise = nextEx
                            store.lastExerciseType = nextEx
                            store.saveLastSelection()
                            showEJ11CompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(
                            when (currentExercise) {
                                ExerciseType.EJ11 -> loc.t("r1_title")
                                ExerciseType.R1 -> loc.t("r2_title")
                                else -> loc.t("ej4_go_to_modos")
                            }
                        )
                    }

                    TextButton(
                        onClick = { showEJ11CompletionDialog = false },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("stay_mode"))
                    }
                }
            }
        )
    }

    if (showCompletionDialog) {
        AlertDialog(
            onDismissRequest = { showCompletionDialog = false },
            title = {
                Text(
                    text = String.format(loc.t("milestone_title"), currentTonic.displayName),
                    fontWeight = FontWeight.Bold
                )
            },
            text = {
                Text(
                    text = String.format(
                        loc.t("milestone_msg"),
                        currentTonic.displayName,
                        store.totalArticulationsCompleted(currentTonic)
                    )
                )
            },
            confirmButton = {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = {
                            scorePlayer.stop()
                            val allArt = ArticulationPattern.entries
                            val curIdx = allArt.indexOf(currentArticulation)
                            currentArticulation = allArt[(curIdx + 1) % allArt.size]
                            currentMode = ModeType.IONIAN
                            showCompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("next_round") + " (${currentTonic.displayName})")
                    }

                    Button(
                        onClick = {
                            scorePlayer.stop()
                            currentTonic = store.nextTonic(currentTonic)
                            currentMode = ModeType.IONIAN
                            showCompletionDialog = false
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) {
                        Text(String.format(loc.t("advance_tonic"), store.nextTonic(currentTonic).displayName))
                    }

                    TextButton(
                        onClick = { showCompletionDialog = false },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(loc.t("stay_mode"))
                    }
                }
            }
        )
    }

    Scaffold(
        topBar = {
            Surface(
                color = MaterialTheme.colorScheme.surface,
                tonalElevation = 2.dp
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 12.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.clickable { onBack() }
                    ) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }

                    Row(
                        modifier = Modifier.weight(1f).padding(start = 8.dp),
                        horizontalArrangement = Arrangement.End,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        // Exercise Switcher (E.J. 1 | E.J. 2 | E.J. 4 | E.J. 5 | E.J. 10 | E.J. 11 | 84 Modos)
                        Surface(
                            shape = RoundedCornerShape(10.dp),
                            color = MaterialTheme.colorScheme.surfaceVariant,
                            modifier = Modifier.weight(1f, fill = false)
                        ) {
                            Row(
                                modifier = Modifier
                                    .horizontalScroll(rememberScrollState())
                                    .padding(2.dp)
                            ) {
                                ExerciseType.entries.forEach { ex ->
                                    val isSel = currentExercise == ex
                                    Surface(
                                        onClick = {
                                            scorePlayer.stop()
                                            currentExercise = ex
                                            store.lastExerciseType = ex
                                            store.saveLastSelection()
                                        },
                                        shape = RoundedCornerShape(8.dp),
                                        color = if (isSel) MaterialTheme.colorScheme.primary else Color.Transparent
                                    ) {
                                        Text(
                                            text = ex.pillLabel,
                                            fontSize = 10.sp,
                                            fontWeight = FontWeight.Bold,
                                            maxLines = 1,
                                            color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                                            modifier = Modifier.padding(horizontal = 6.dp, vertical = 4.dp)
                                        )
                                    }
                                }
                            }
                        }

                        if (currentExercise == ExerciseType.MODOS) {
                            IconButton(
                                onClick = onOpenMatrix,
                                modifier = Modifier
                                    .size(32.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.primaryContainer)
                            ) {
                                Icon(
                                    Icons.Default.GridView,
                                    contentDescription = "Matrix",
                                    modifier = Modifier.size(16.dp),
                                    tint = MaterialTheme.colorScheme.onPrimaryContainer
                                )
                            }
                        }

                        Button(
                            onClick = { loc.toggleLanguage() },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = MaterialTheme.colorScheme.primaryContainer,
                                contentColor = MaterialTheme.colorScheme.onPrimaryContainer
                            ),
                            shape = RoundedCornerShape(10.dp),
                            contentPadding = PaddingValues(horizontal = 6.dp, vertical = 4.dp),
                            modifier = Modifier.height(30.dp)
                        ) {
                            Text(loc.currentLanguage.flag, fontSize = 12.sp)
                        }
                    }
                }
            }
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            // Mode / Exercise Header Card
            Surface(
                color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f),
                modifier = Modifier.fillMaxWidth()
            ) {
                if (currentExercise.isChromaticExercise) {
                    val isEJ2 = currentExercise == ExerciseType.EJ2
                    val curArt = if (isEJ2) currentEJ2Articulation else currentEJ1Articulation
                    Column(
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 10.dp),
                        verticalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = "${currentExercise.pillLabel} · ${curArt.title(loc)}",
                                fontSize = 16.sp,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                                modifier = Modifier.weight(1f)
                            )

                            Spacer(modifier = Modifier.width(8.dp))

                            Surface(
                                shape = RoundedCornerShape(8.dp),
                                color = if (isChromaticFullyDone) Color(0xFF10B981).copy(alpha = 0.2f) else MaterialTheme.colorScheme.primary.copy(alpha = 0.15f)
                            ) {
                                Text(
                                    text = "$chromaticDoneCount/10 ${loc.t("arts_count")}",
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (isChromaticFullyDone) Color(0xFF10B981) else MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                )
                            }
                        }

                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            Surface(
                                shape = RoundedCornerShape(6.dp),
                                color = MaterialTheme.colorScheme.surfaceVariant
                            ) {
                                Text(
                                    text = "A. L. 16.588",
                                    fontSize = 10.sp,
                                    fontWeight = FontWeight.Bold,
                                    modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp),
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }

                            Text(
                                text = "${loc.t(if (isEJ2) "ej2_header_info" else "ej1_header_info")} | ${curArt.formulaBadge}",
                                fontSize = 11.sp,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                    }
                } else if (currentExercise.isEJ4Exercise) {
                    val curArt = when (currentExercise) {
                        ExerciseType.R2 -> currentR2Articulation
                        ExerciseType.R4 -> currentR4Articulation
                        else -> currentEJ4Articulation
                    }
                    val curSec = when (currentExercise) {
                        ExerciseType.R2 -> currentR2Section
                        ExerciseType.R4 -> currentR4Section
                        else -> currentEJ4Section
                    }
                    val curMeasRange = when (currentExercise) {
                        ExerciseType.R2 -> curSec.r2MeasureRange
                        ExerciseType.R4 -> curSec.r1MeasureRange
                        else -> curSec.measureRange
                    }

                    Column(
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = "${currentExercise.pillLabel} · ${curSec.title(loc)}",
                                    fontSize = 15.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis
                                )
                                Text(
                                    text = "${curArt.title(loc)} · $curMeasRange",
                                    fontSize = 11.sp,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis
                                )
                            }

                            Spacer(modifier = Modifier.width(8.dp))

                            Surface(
                                shape = RoundedCornerShape(8.dp),
                                color = if (isEJ4FullyDone) Color(0xFF10B981).copy(alpha = 0.2f) else MaterialTheme.colorScheme.primary.copy(alpha = 0.15f)
                            ) {
                                Text(
                                    text = "$ej4DoneCount/8 ${loc.t("arts_count")}",
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (isEJ4FullyDone) Color(0xFF10B981) else MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                )
                            }
                        }

                        // 25 Tonal Sections Bar
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .horizontalScroll(rememberScrollState()),
                            horizontalArrangement = Arrangement.spacedBy(6.dp)
                        ) {
                            EJ4Section.entries.forEach { sec ->
                                val isSel = sec == curSec
                                val secRange = when (currentExercise) {
                                    ExerciseType.R2 -> sec.r2MeasureRange
                                    ExerciseType.R4 -> sec.r1MeasureRange
                                    else -> sec.measureRange
                                }
                                Surface(
                                    onClick = {
                                        scorePlayer.stop()
                                        when (currentExercise) {
                                            ExerciseType.R2 -> {
                                                currentR2Section = sec
                                                store.lastR2Section = sec
                                            }
                                            ExerciseType.R4 -> {
                                                currentR4Section = sec
                                                store.lastR4Section = sec
                                            }
                                            else -> {
                                                currentEJ4Section = sec
                                                store.lastEJ4Section = sec
                                            }
                                        }
                                        store.saveLastSelection()
                                    },
                                    shape = RoundedCornerShape(10.dp),
                                    color = if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant
                                ) {
                                    Text(
                                        text = "${sec.shortBadge} ($secRange)",
                                        fontSize = 11.sp,
                                        fontWeight = if (isSel) FontWeight.Bold else FontWeight.Medium,
                                        color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                    )
                                }
                            }
                        }
                    }
                } else if (currentExercise.isEJ5TypeExercise) {
                    val curArt = when (currentExercise) {
                        ExerciseType.EJ5 -> currentEJ5Articulation
                        ExerciseType.EJ10 -> currentEJ10Articulation
                        ExerciseType.EJ11 -> currentEJ11Articulation
                        ExerciseType.R1 -> currentR1Articulation
                        ExerciseType.R5 -> currentR5Articulation
                        else -> currentEJ5Articulation
                    }
                    val secTitle = when (currentExercise) {
                        ExerciseType.EJ5 -> "E.J. 5 · ${currentEJ5Section.title(loc)}"
                        ExerciseType.EJ10 -> "E.J. 10 · ${currentEJ10Section.title(loc)}"
                        ExerciseType.EJ11 -> "E.J. 11 · ${currentEJ11Section.title(loc)}"
                        ExerciseType.R1 -> "R. 1 · ${currentR1Section.title(loc)}"
                        ExerciseType.R5 -> "R. 5 · ${currentR5Section.title(loc)}"
                        else -> ""
                    }
                    val measRange = when (currentExercise) {
                        ExerciseType.EJ5 -> currentEJ5Section.measureRange
                        ExerciseType.EJ10 -> currentEJ10Section.measureRange
                        ExerciseType.EJ11 -> currentEJ11Section.measureRange
                        ExerciseType.R1 -> currentR1Section.r1MeasureRange
                        ExerciseType.R5 -> currentR5Section.r5MeasureRange
                        else -> ""
                    }

                    Column(
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = secTitle,
                                    fontSize = 15.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis
                                )
                                Text(
                                    text = "${curArt.title(loc, currentExercise)} · $measRange",
                                    fontSize = 11.sp,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis
                                )
                            }

                            Spacer(modifier = Modifier.width(8.dp))

                            Surface(
                                shape = RoundedCornerShape(8.dp),
                                color = if (isEJ5TypeFullyDone) Color(0xFF10B981).copy(alpha = 0.2f) else MaterialTheme.colorScheme.primary.copy(alpha = 0.15f)
                            ) {
                                Text(
                                    text = "$ej5TypeDoneCount/10 ${loc.t("arts_count")}",
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (isEJ5TypeFullyDone) Color(0xFF10B981) else MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                )
                            }
                        }

                        if (currentExercise == ExerciseType.EJ5) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .horizontalScroll(rememberScrollState()),
                                horizontalArrangement = Arrangement.spacedBy(6.dp)
                            ) {
                                EJ5Section.entries.forEach { sec ->
                                    val isSel = sec == currentEJ5Section
                                    Surface(
                                        onClick = {
                                            scorePlayer.stop()
                                            currentEJ5Section = sec
                                            store.lastEJ5Section = sec
                                            store.saveLastSelection()
                                        },
                                        shape = RoundedCornerShape(10.dp),
                                        color = if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant
                                    ) {
                                        Text(
                                            text = "${sec.shortBadge} (${sec.measureRange})",
                                            fontSize = 11.sp,
                                            fontWeight = if (isSel) FontWeight.Bold else FontWeight.Medium,
                                            color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                        )
                                    }
                                }
                            }
                        } else if (currentExercise.isReichertExercise) {
                            val curSec = if (currentExercise == ExerciseType.R5) currentR5Section else currentR1Section
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .horizontalScroll(rememberScrollState()),
                                horizontalArrangement = Arrangement.spacedBy(6.dp)
                            ) {
                                EJ4Section.entries.forEach { sec ->
                                    val isSel = sec == curSec
                                    val mRange = if (currentExercise == ExerciseType.R5) sec.r5MeasureRange else sec.r1MeasureRange
                                    Surface(
                                        onClick = {
                                            scorePlayer.stop()
                                            if (currentExercise == ExerciseType.R5) {
                                                currentR5Section = sec
                                                store.lastR5Section = sec
                                            } else {
                                                currentR1Section = sec
                                                store.lastR1Section = sec
                                            }
                                            store.saveLastSelection()
                                        },
                                        shape = RoundedCornerShape(10.dp),
                                        color = if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant
                                    ) {
                                        Text(
                                            text = "${sec.shortBadge} ($mRange)",
                                            fontSize = 11.sp,
                                            fontWeight = if (isSel) FontWeight.Bold else FontWeight.Medium,
                                            color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                        )
                                    }
                                }
                            }
                        } else {
                            val curSec = if (currentExercise == ExerciseType.EJ11) currentEJ11Section else currentEJ10Section
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .horizontalScroll(rememberScrollState()),
                                horizontalArrangement = Arrangement.spacedBy(6.dp)
                            ) {
                                EJ10Section.entries.forEach { sec ->
                                    val isSel = sec == curSec
                                    val mRange = sec.measureRange
                                    Surface(
                                        onClick = {
                                            scorePlayer.stop()
                                            if (currentExercise == ExerciseType.EJ11) {
                                                currentEJ11Section = sec
                                                store.lastEJ11Section = sec
                                            } else {
                                                currentEJ10Section = sec
                                                store.lastEJ10Section = sec
                                            }
                                            store.saveLastSelection()
                                        },
                                        shape = RoundedCornerShape(10.dp),
                                        color = if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant
                                    ) {
                                        Text(
                                            text = "${sec.shortBadge} ($mRange)",
                                            fontSize = 11.sp,
                                            fontWeight = if (isSel) FontWeight.Bold else FontWeight.Medium,
                                            color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                        )
                                    }
                                }
                            }
                        }
                    }
                } else {
                    Column(
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 10.dp),
                        verticalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = "${currentTonic.displayName} · ${currentMode.getName(loc)}",
                                fontSize = 18.sp,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )

                            Surface(
                                shape = RoundedCornerShape(8.dp),
                                color = if (areAllModesPracticed) Color(0xFF10B981).copy(alpha = 0.2f) else MaterialTheme.colorScheme.primary.copy(alpha = 0.15f)
                            ) {
                                Text(
                                    text = "$practicedModesCount/7 ${loc.t("modes_count")}",
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (areAllModesPracticed) Color(0xFF10B981) else MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                )
                            }
                        }

                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            Surface(
                                shape = RoundedCornerShape(6.dp),
                                color = MaterialTheme.colorScheme.surfaceVariant
                            ) {
                                Text(
                                    text = currentMode.family.displayName,
                                    fontSize = 10.sp,
                                    fontWeight = FontWeight.Bold,
                                    modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp),
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }

                            Text(
                                text = "${currentMode.keyDescription(currentTonic)} | ${currentMode.accidentalBadge(loc)}",
                                fontSize = 11.sp,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }

            HorizontalDivider()

            // Main Interactive Sheet Music Area
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .background(Color.White)
            ) {
                ScoreWebView(
                    abcString = currentAbcScore,
                    modifier = Modifier.fillMaxSize()
                )
            }

            HorizontalDivider()

            // Articulation Section Header
            if (currentExercise.isChromaticExercise) {
                val isEJ2 = currentExercise == ExerciseType.EJ2
                val curArt = if (isEJ2) currentEJ2Articulation else currentEJ1Articulation

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(MaterialTheme.colorScheme.surface)
                        .padding(horizontal = 16.dp, vertical = 6.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text(
                            text = loc.t("articulations_title"),
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        if (isChromaticFullyDone) {
                            Icon(
                                Icons.Default.CheckCircle,
                                contentDescription = null,
                                tint = Color(0xFF10B981),
                                modifier = Modifier.size(14.dp)
                            )
                        }
                    }

                    Surface(
                        shape = RoundedCornerShape(6.dp),
                        color = if (isChromaticFullyDone) Color(0xFF10B981).copy(alpha = 0.2f) else if (chromaticDoneCount > 0) MaterialTheme.colorScheme.primary.copy(alpha = 0.15f) else MaterialTheme.colorScheme.surfaceVariant
                    ) {
                        Text(
                            text = "$chromaticDoneCount/10 ${loc.t("arts_count")}",
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            color = if (isChromaticFullyDone) Color(0xFF10B981) else if (chromaticDoneCount > 0) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                        )
                    }
                }

                // E.J. 1 / E.J. 2 Articulation Bar Chips (0..10)
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState())
                        .background(MaterialTheme.colorScheme.surface)
                        .padding(horizontal = 14.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    EJ1Articulation.entries.forEach { art ->
                        val isSelected = art == curArt
                        val isCompleted = store.isChromaticCompleted(art, currentExercise)

                        Surface(
                            onClick = {
                                scorePlayer.stop()
                                if (isSelected) {
                                    if (art != EJ1Articulation.ORIGINAL) {
                                        store.toggleChromaticCompleted(art, currentExercise)
                                    }
                                } else {
                                    if (curArt != EJ1Articulation.ORIGINAL) {
                                        store.markChromaticCompleted(curArt, currentExercise)
                                    }
                                    if (isEJ2) {
                                        currentEJ2Articulation = art
                                        store.lastEJ2Articulation = art
                                    } else {
                                        currentEJ1Articulation = art
                                        store.lastEJ1Articulation = art
                                    }
                                    store.saveLastSelection()
                                }
                            },
                            shape = RoundedCornerShape(16.dp),
                            color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                            tonalElevation = if (isSelected) 3.dp else 0.dp
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 12.dp, vertical = 7.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(4.dp)
                            ) {
                                if (isCompleted) {
                                    Icon(
                                        Icons.Default.CheckCircle,
                                        contentDescription = null,
                                        modifier = Modifier.size(13.dp),
                                        tint = if (isSelected) MaterialTheme.colorScheme.onPrimary else Color(0xFF10B981)
                                    )
                                }
                                Text(
                                    text = art.shortTitle(loc),
                                    fontSize = 12.sp,
                                    fontWeight = if (isSelected) FontWeight.SemiBold else FontWeight.Normal,
                                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }
            } else if (currentExercise.isEJ4Exercise) {
                val curArt = when (currentExercise) {
                    ExerciseType.R2 -> currentR2Articulation
                    ExerciseType.R4 -> currentR4Articulation
                    else -> currentEJ4Articulation
                }

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(MaterialTheme.colorScheme.surface)
                        .padding(horizontal = 16.dp, vertical = 6.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text(
                            text = loc.t("ej4_select_art"),
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        if (isEJ4FullyDone) {
                            Icon(
                                Icons.Default.CheckCircle,
                                contentDescription = null,
                                tint = Color(0xFF10B981),
                                modifier = Modifier.size(14.dp)
                            )
                        }
                    }

                    Surface(
                        shape = RoundedCornerShape(6.dp),
                        color = if (isEJ4FullyDone) Color(0xFF10B981).copy(alpha = 0.2f) else if (ej4DoneCount > 0) MaterialTheme.colorScheme.primary.copy(alpha = 0.15f) else MaterialTheme.colorScheme.surfaceVariant
                    ) {
                        Text(
                            text = "$ej4DoneCount/8 ${loc.t("arts_count")}",
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            color = if (isEJ4FullyDone) Color(0xFF10B981) else if (ej4DoneCount > 0) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                        )
                    }
                }

                // E.J. 4 / R. 2 / R. 4 Articulation Bar Chips (0..8)
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState())
                        .background(MaterialTheme.colorScheme.surface)
                        .padding(horizontal = 14.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    EJ4Articulation.entries.forEach { art ->
                        val isSelected = art == curArt
                        val isCompleted = store.isEJ4Completed(art, currentExercise)

                        Surface(
                            onClick = {
                                scorePlayer.stop()
                                if (isSelected) {
                                    if (art != EJ4Articulation.ORIGINAL) {
                                        store.toggleEJ4Completed(art, currentExercise)
                                    }
                                } else {
                                    if (curArt != EJ4Articulation.ORIGINAL) {
                                        store.markEJ4Completed(curArt, currentExercise)
                                    }
                                    when (currentExercise) {
                                        ExerciseType.R2 -> {
                                            currentR2Articulation = art
                                            store.lastR2Articulation = art
                                        }
                                        ExerciseType.R4 -> {
                                            currentR4Articulation = art
                                            store.lastR4Articulation = art
                                        }
                                        else -> {
                                            currentEJ4Articulation = art
                                            store.lastEJ4Articulation = art
                                        }
                                    }
                                    store.saveLastSelection()
                                }
                            },
                            shape = RoundedCornerShape(16.dp),
                            color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                            tonalElevation = if (isSelected) 3.dp else 0.dp
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 12.dp, vertical = 7.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(4.dp)
                            ) {
                                if (isCompleted) {
                                    Icon(
                                        Icons.Default.CheckCircle,
                                        contentDescription = null,
                                        modifier = Modifier.size(13.dp),
                                        tint = if (isSelected) MaterialTheme.colorScheme.onPrimary else Color(0xFF10B981)
                                    )
                                }
                                Text(
                                    text = art.shortTitle(loc),
                                    fontSize = 12.sp,
                                    fontWeight = if (isSelected) FontWeight.SemiBold else FontWeight.Normal,
                                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }
            } else if (currentExercise.isEJ5TypeExercise) {
                val curArt = when (currentExercise) {
                    ExerciseType.EJ5 -> currentEJ5Articulation
                    ExerciseType.EJ10 -> currentEJ10Articulation
                    ExerciseType.EJ11 -> currentEJ11Articulation
                    ExerciseType.R1 -> currentR1Articulation
                    ExerciseType.R5 -> currentR5Articulation
                    else -> currentEJ5Articulation
                }

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(MaterialTheme.colorScheme.surface)
                        .padding(horizontal = 16.dp, vertical = 6.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text(
                            text = loc.t("articulations_title"),
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        if (isEJ5TypeFullyDone) {
                            Icon(
                                Icons.Default.CheckCircle,
                                contentDescription = null,
                                tint = Color(0xFF10B981),
                                modifier = Modifier.size(14.dp)
                            )
                        }
                    }

                    Surface(
                        shape = RoundedCornerShape(6.dp),
                        color = if (isEJ5TypeFullyDone) Color(0xFF10B981).copy(alpha = 0.2f) else if (ej5TypeDoneCount > 0) MaterialTheme.colorScheme.primary.copy(alpha = 0.15f) else MaterialTheme.colorScheme.surfaceVariant
                    ) {
                        Text(
                            text = "$ej5TypeDoneCount/10 ${loc.t("arts_count")}",
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            color = if (isEJ5TypeFullyDone) Color(0xFF10B981) else if (ej5TypeDoneCount > 0) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                        )
                    }
                }

                // E.J. 5 / E.J. 10 / E.J. 11 / R. 1 / R. 5 Articulation Bar Chips (0..10)
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState())
                        .background(MaterialTheme.colorScheme.surface)
                        .padding(horizontal = 14.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    EJ5Articulation.entries.forEach { art ->
                        val isSelected = art == curArt
                        val isCompleted = store.isEJ5TypeCompleted(art, currentExercise)

                        Surface(
                            onClick = {
                                scorePlayer.stop()
                                if (isSelected) {
                                    if (art != EJ5Articulation.ORIGINAL) {
                                        store.toggleEJ5TypeCompleted(art, currentExercise)
                                    }
                                } else {
                                    if (curArt != EJ5Articulation.ORIGINAL) {
                                        store.markEJ5TypeCompleted(curArt, currentExercise)
                                    }
                                    when (currentExercise) {
                                        ExerciseType.EJ5 -> {
                                            currentEJ5Articulation = art
                                            store.lastEJ5Articulation = art
                                        }
                                        ExerciseType.EJ10 -> {
                                            currentEJ10Articulation = art
                                            store.lastEJ10Articulation = art
                                        }
                                        ExerciseType.EJ11 -> {
                                            currentEJ11Articulation = art
                                            store.lastEJ11Articulation = art
                                        }
                                        ExerciseType.R1 -> {
                                            currentR1Articulation = art
                                            store.lastR1Articulation = art
                                        }
                                        ExerciseType.R5 -> {
                                            currentR5Articulation = art
                                            store.lastR5Articulation = art
                                        }
                                        else -> {}
                                    }
                                    store.saveLastSelection()
                                }
                            },
                            shape = RoundedCornerShape(16.dp),
                            color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                            tonalElevation = if (isSelected) 3.dp else 0.dp
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 12.dp, vertical = 7.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(4.dp)
                            ) {
                                if (isCompleted) {
                                    Icon(
                                        Icons.Default.CheckCircle,
                                        contentDescription = null,
                                        modifier = Modifier.size(13.dp),
                                        tint = if (isSelected) MaterialTheme.colorScheme.onPrimary else Color(0xFF10B981)
                                    )
                                }
                                Text(
                                    text = art.shortTitle(loc, currentExercise),
                                    fontSize = 12.sp,
                                    fontWeight = if (isSelected) FontWeight.SemiBold else FontWeight.Normal,
                                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }
            } else {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(MaterialTheme.colorScheme.surface)
                        .padding(horizontal = 16.dp, vertical = 6.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text(
                            text = loc.t("articulations_title"),
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        if (isModeFullyDone) {
                            Icon(
                                Icons.Default.CheckCircle,
                                contentDescription = null,
                                tint = Color(0xFF10B981),
                                modifier = Modifier.size(14.dp)
                            )
                        }
                    }

                    Surface(
                        shape = RoundedCornerShape(6.dp),
                        color = if (isModeFullyDone) Color(0xFF10B981).copy(alpha = 0.2f) else if (completedArtCount > 0) MaterialTheme.colorScheme.primary.copy(alpha = 0.15f) else MaterialTheme.colorScheme.surfaceVariant
                    ) {
                        Text(
                            text = "$completedArtCount/8 ${loc.t("arts_count")}",
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            color = if (isModeFullyDone) Color(0xFF10B981) else if (completedArtCount > 0) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                        )
                    }
                }

                // Articulation Bar Chips
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState())
                        .background(MaterialTheme.colorScheme.surface)
                        .padding(horizontal = 14.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    ArticulationPattern.entries.forEach { pattern ->
                        val isSelected = pattern == currentArticulation
                        val isCompleted = store.isCompleted(currentTonic, currentMode, pattern)

                        Surface(
                            onClick = {
                                scorePlayer.stop()
                                if (isSelected) {
                                    store.toggleCompleted(currentTonic, currentMode, pattern)
                                } else {
                                    store.markCompleted(currentTonic, currentMode, currentArticulation)
                                    currentArticulation = pattern
                                }
                            },
                            shape = RoundedCornerShape(16.dp),
                            color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                            tonalElevation = if (isSelected) 3.dp else 0.dp
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 12.dp, vertical = 7.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(4.dp)
                            ) {
                                if (isCompleted) {
                                    Icon(
                                        Icons.Default.CheckCircle,
                                        contentDescription = null,
                                        modifier = Modifier.size(13.dp),
                                        tint = if (isSelected) MaterialTheme.colorScheme.onPrimary else Color(0xFF10B981)
                                    )
                                }
                                Text(
                                    text = pattern.shortTitle(loc),
                                    fontSize = 12.sp,
                                    fontWeight = if (isSelected) FontWeight.SemiBold else FontWeight.Normal,
                                    color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }
            }

            HorizontalDivider()

            // Control Toolbar (Metronome + Piano + Action)
            Surface(
                color = MaterialTheme.colorScheme.surface,
                tonalElevation = 4.dp
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 10.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    // Row 1: Metronome + BPM + Piano Play
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        // Metronome Toggle
                        IconButton(
                            onClick = { metronome.toggle() },
                            modifier = Modifier.size(38.dp)
                        ) {
                            Icon(
                                if (metronome.isPlaying) Icons.Default.PauseCircleFilled else Icons.Default.PlayCircleFilled,
                                contentDescription = "Metronome",
                                modifier = Modifier.size(34.dp),
                                tint = MaterialTheme.colorScheme.primary
                            )
                        }

                        // 4 Beat Dots
                        Row(
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            (1..4).forEach { beat ->
                                val isActive = metronome.isPlaying && metronome.currentBeat == beat
                                val scale by animateFloatAsState(if (isActive) 1.4f else 1.0f, label = "dotScale")
                                val color by animateColorAsState(
                                    if (isActive) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant,
                                    label = "dotColor"
                                )
                                Box(
                                    modifier = Modifier
                                        .size(8.dp)
                                        .scale(scale)
                                        .clip(CircleShape)
                                        .background(color)
                                )
                            }
                        }

                        // BPM Stepper
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier
                                .clip(RoundedCornerShape(8.dp))
                                .background(MaterialTheme.colorScheme.surfaceVariant)
                                .padding(horizontal = 6.dp, vertical = 2.dp)
                        ) {
                            IconButton(
                                onClick = { metronome.setTempo(metronome.tempoBPM - 2) },
                                modifier = Modifier.size(28.dp)
                            ) {
                                Icon(Icons.Default.Remove, contentDescription = "Minus", modifier = Modifier.size(14.dp))
                            }

                            Text(
                                text = "${metronome.tempoBPM}",
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                modifier = Modifier.padding(horizontal = 4.dp)
                            )

                            IconButton(
                                onClick = { metronome.setTempo(metronome.tempoBPM + 2) },
                                modifier = Modifier.size(28.dp)
                            ) {
                                Icon(Icons.Default.Add, contentDescription = "Plus", modifier = Modifier.size(14.dp))
                            }
                        }

                        // Play Piano Button
                        Button(
                            onClick = {
                                when (currentExercise) {
                                    ExerciseType.EJ1 -> scorePlayer.toggleEJ1(
                                        articulation = currentEJ1Articulation,
                                        tempoBPM = metronome.tempoBPM
                                    )
                                    ExerciseType.EJ2 -> scorePlayer.toggleEJ2(
                                        articulation = currentEJ2Articulation,
                                        tempoBPM = metronome.tempoBPM
                                    )
                                    ExerciseType.EJ4 -> scorePlayer.toggleEJ4(
                                        articulation = currentEJ4Articulation,
                                        section = currentEJ4Section,
                                        tempoBPM = metronome.tempoBPM,
                                        exercise = ExerciseType.EJ4
                                    )
                                    ExerciseType.EJ5 -> scorePlayer.toggleEJ5(
                                        articulation = currentEJ5Articulation,
                                        section = currentEJ5Section,
                                        tempoBPM = metronome.tempoBPM
                                    )
                                    ExerciseType.EJ10 -> scorePlayer.toggleEJ10(
                                        articulation = currentEJ10Articulation,
                                        section = currentEJ10Section,
                                        tempoBPM = metronome.tempoBPM
                                    )
                                    ExerciseType.EJ11 -> scorePlayer.toggleEJ11(
                                        articulation = currentEJ11Articulation,
                                        section = currentEJ11Section,
                                        tempoBPM = metronome.tempoBPM
                                    )
                                    ExerciseType.R1 -> scorePlayer.toggleEJ5Type(
                                        articulation = currentR1Articulation,
                                        sectionIndex = currentR1Section.id,
                                        tempoBPM = metronome.tempoBPM,
                                        exercise = ExerciseType.R1
                                    )
                                    ExerciseType.R2 -> scorePlayer.toggleEJ4(
                                        articulation = currentR2Articulation,
                                        section = currentR2Section,
                                        tempoBPM = metronome.tempoBPM,
                                        exercise = ExerciseType.R2
                                    )
                                    ExerciseType.R4 -> scorePlayer.toggleEJ4(
                                        articulation = currentR4Articulation,
                                        section = currentR4Section,
                                        tempoBPM = metronome.tempoBPM,
                                        exercise = ExerciseType.R4
                                    )
                                    ExerciseType.R5 -> scorePlayer.toggleEJ5Type(
                                        articulation = currentR5Articulation,
                                        sectionIndex = currentR5Section.id,
                                        tempoBPM = metronome.tempoBPM,
                                        exercise = ExerciseType.R5
                                    )
                                    ExerciseType.MODOS -> scorePlayer.toggle(
                                        tonic = currentTonic,
                                        mode = currentMode,
                                        articulation = currentArticulation,
                                        tempoBPM = metronome.tempoBPM
                                    )
                                }
                            },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = if (scorePlayer.isPlaying) Color(0xFFEF4444) else Color(0xFF6366F1)
                            ),
                            shape = RoundedCornerShape(14.dp),
                            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp),
                            modifier = Modifier.height(36.dp)
                        ) {
                            Icon(
                                if (scorePlayer.isPlaying) Icons.Default.Stop else Icons.Default.MusicNote,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp)
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Text(
                                text = if (scorePlayer.isPlaying) loc.t("stop_piano") else loc.t("play_piano"),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }

                    // Row 2: Action Buttons
                    if (currentExercise.isChromaticExercise) {
                        val isEJ2 = currentExercise == ExerciseType.EJ2
                        val curArt = if (isEJ2) currentEJ2Articulation else currentEJ1Articulation

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            if (isChromaticFullyDone) {
                                Button(
                                    onClick = {
                                        if (isEJ2) showEJ2CompletionDialog = true else showEJ1CompletionDialog = true
                                    },
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(48.dp),
                                    shape = RoundedCornerShape(16.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF10B981)),
                                    contentPadding = PaddingValues(horizontal = 12.dp)
                                ) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                                    ) {
                                        Icon(
                                            Icons.Default.CheckCircle,
                                            contentDescription = null,
                                            modifier = Modifier.size(16.dp)
                                        )
                                        Text(
                                            text = "✓ ${loc.t(if (isEJ2) "ej2_ten_arts_completed" else "ej1_ten_arts_completed")}",
                                            fontSize = 13.sp,
                                            fontWeight = FontWeight.Bold,
                                            maxLines = 1
                                        )
                                    }
                                }
                            } else {
                                Button(
                                    onClick = {
                                        scorePlayer.stop()
                                        if (curArt == EJ1Articulation.ORIGINAL) {
                                            if (isEJ2) {
                                                currentEJ2Articulation = EJ1Articulation.ALL_SLURRED_8
                                                store.lastEJ2Articulation = currentEJ2Articulation
                                            } else {
                                                currentEJ1Articulation = EJ1Articulation.ALL_SLURRED_8
                                                store.lastEJ1Articulation = currentEJ1Articulation
                                            }
                                            store.saveLastSelection()
                                        } else {
                                            store.markChromaticCompleted(curArt, currentExercise)
                                            if (store.isChromaticFullyCompleted(currentExercise)) {
                                                if (isEJ2) showEJ2CompletionDialog = true else showEJ1CompletionDialog = true
                                            } else {
                                                val allPractice = EJ1Articulation.practiceCases
                                                val idx = allPractice.indexOf(curArt)
                                                if (idx >= 0) {
                                                    val nextArt = allPractice[(idx + 1) % allPractice.size]
                                                    if (isEJ2) {
                                                        currentEJ2Articulation = nextArt
                                                        store.lastEJ2Articulation = nextArt
                                                    } else {
                                                        currentEJ1Articulation = nextArt
                                                        store.lastEJ1Articulation = nextArt
                                                    }
                                                    store.saveLastSelection()
                                                }
                                            }
                                        }
                                    },
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(48.dp),
                                    shape = RoundedCornerShape(16.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
                                    contentPadding = PaddingValues(horizontal = 12.dp)
                                ) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                                    ) {
                                        Text(
                                            text = loc.t("next_art"),
                                            fontSize = 14.sp,
                                            fontWeight = FontWeight.Bold,
                                            maxLines = 1
                                        )
                                        Surface(
                                            shape = RoundedCornerShape(percent = 50),
                                            color = Color.White.copy(alpha = 0.2f)
                                        ) {
                                            Text(
                                                text = "$chromaticDoneCount/10 ${loc.t("arts_count")}",
                                                fontSize = 11.sp,
                                                fontWeight = FontWeight.Bold,
                                                fontFamily = FontFamily.Monospace,
                                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                                            )
                                        }
                                        Icon(
                                            Icons.Default.ArrowForward,
                                            contentDescription = null,
                                            modifier = Modifier.size(16.dp)
                                        )
                                    }
                                }
                            }
                        }
                    } else if (currentExercise.isEJ4Exercise) {
                        val curArt = when (currentExercise) {
                            ExerciseType.R2 -> currentR2Articulation
                            ExerciseType.R4 -> currentR4Articulation
                            else -> currentEJ4Articulation
                        }
                        val curSec = when (currentExercise) {
                            ExerciseType.R2 -> currentR2Section
                            ExerciseType.R4 -> currentR4Section
                            else -> currentEJ4Section
                        }

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            OutlinedButton(
                                onClick = {
                                    scorePlayer.stop()
                                    val allSecs = EJ4Section.entries
                                    val idx = allSecs.indexOf(curSec)
                                    if (idx >= 0) {
                                        val nextSec = allSecs[(idx + 1) % allSecs.size]
                                        when (currentExercise) {
                                            ExerciseType.R2 -> {
                                                currentR2Section = nextSec
                                                store.lastR2Section = nextSec
                                            }
                                            ExerciseType.R4 -> {
                                                currentR4Section = nextSec
                                                store.lastR4Section = nextSec
                                            }
                                            else -> {
                                                currentEJ4Section = nextSec
                                                store.lastEJ4Section = nextSec
                                            }
                                        }
                                        store.saveLastSelection()
                                    }
                                },
                                shape = RoundedCornerShape(16.dp),
                                modifier = Modifier.height(48.dp),
                                contentPadding = PaddingValues(horizontal = 10.dp)
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.spacedBy(5.dp)
                                ) {
                                    Text(
                                        text = loc.t("ej4_next_section"),
                                        fontSize = 12.sp,
                                        fontWeight = FontWeight.SemiBold,
                                        maxLines = 1
                                    )
                                    Surface(
                                        shape = RoundedCornerShape(percent = 50),
                                        color = MaterialTheme.colorScheme.surfaceVariant
                                    ) {
                                        Text(
                                            text = "${curSec.id + 1}/25",
                                            fontSize = 10.sp,
                                            fontWeight = FontWeight.Bold,
                                            fontFamily = FontFamily.Monospace,
                                            modifier = Modifier.padding(horizontal = 5.dp, vertical = 2.dp)
                                        )
                                    }
                                }
                            }

                            if (isEJ4FullyDone) {
                                Button(
                                    onClick = { showEJ4CompletionDialog = true },
                                    modifier = Modifier
                                        .weight(1f)
                                        .height(48.dp),
                                    shape = RoundedCornerShape(16.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF10B981)),
                                    contentPadding = PaddingValues(horizontal = 10.dp)
                                ) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(5.dp)
                                    ) {
                                        Icon(
                                            Icons.Default.CheckCircle,
                                            contentDescription = null,
                                            modifier = Modifier.size(16.dp)
                                        )
                                        Text(
                                            text = "✓ ${loc.t("ej4_eight_arts_completed")}",
                                            fontSize = 12.sp,
                                            fontWeight = FontWeight.Bold,
                                            maxLines = 1,
                                            overflow = TextOverflow.Ellipsis
                                        )
                                    }
                                }
                            } else {
                                Button(
                                    onClick = {
                                        scorePlayer.stop()
                                        if (curArt == EJ4Articulation.ORIGINAL) {
                                            val firstArt = EJ4Articulation.ALL_SLURRED_8
                                            when (currentExercise) {
                                                ExerciseType.R2 -> {
                                                    currentR2Articulation = firstArt
                                                    store.lastR2Articulation = firstArt
                                                }
                                                ExerciseType.R4 -> {
                                                    currentR4Articulation = firstArt
                                                    store.lastR4Articulation = firstArt
                                                }
                                                else -> {
                                                    currentEJ4Articulation = firstArt
                                                    store.lastEJ4Articulation = firstArt
                                                }
                                            }
                                            store.saveLastSelection()
                                        } else {
                                            store.markEJ4Completed(curArt, currentExercise)
                                            if (store.isEJ4FullyCompleted(currentExercise)) {
                                                showEJ4CompletionDialog = true
                                            } else {
                                                val allPractice = EJ4Articulation.practiceCases
                                                val idx = allPractice.indexOf(curArt)
                                                if (idx >= 0) {
                                                    val nextArt = allPractice[(idx + 1) % allPractice.size]
                                                    when (currentExercise) {
                                                        ExerciseType.R2 -> {
                                                            currentR2Articulation = nextArt
                                                            store.lastR2Articulation = nextArt
                                                        }
                                                        ExerciseType.R4 -> {
                                                            currentR4Articulation = nextArt
                                                            store.lastR4Articulation = nextArt
                                                        }
                                                        else -> {
                                                            currentEJ4Articulation = nextArt
                                                            store.lastEJ4Articulation = nextArt
                                                        }
                                                    }
                                                    store.saveLastSelection()
                                                }
                                            }
                                        }
                                    },
                                    modifier = Modifier
                                        .weight(1f)
                                        .height(48.dp),
                                    shape = RoundedCornerShape(16.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
                                    contentPadding = PaddingValues(horizontal = 10.dp)
                                ) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                                    ) {
                                        Text(
                                            text = loc.t("next_art"),
                                            fontSize = 13.sp,
                                            fontWeight = FontWeight.Bold,
                                            maxLines = 1
                                        )
                                        Surface(
                                            shape = RoundedCornerShape(percent = 50),
                                            color = Color.White.copy(alpha = 0.2f)
                                        ) {
                                            Text(
                                                text = "$ej4DoneCount/8",
                                                fontSize = 10.sp,
                                                fontWeight = FontWeight.Bold,
                                                fontFamily = FontFamily.Monospace,
                                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                            )
                                        }
                                        Icon(
                                            Icons.Default.ArrowForward,
                                            contentDescription = null,
                                            modifier = Modifier.size(14.dp)
                                        )
                                    }
                                }
                            }
                        }
                    } else if (currentExercise.isEJ5TypeExercise) {
                        val curArt = when (currentExercise) {
                            ExerciseType.EJ5 -> currentEJ5Articulation
                            ExerciseType.EJ10 -> currentEJ10Articulation
                            ExerciseType.EJ11 -> currentEJ11Articulation
                            ExerciseType.R1 -> currentR1Articulation
                            ExerciseType.R5 -> currentR5Articulation
                            else -> currentEJ5Articulation
                        }

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            OutlinedButton(
                                onClick = {
                                    scorePlayer.stop()
                                    if (currentExercise == ExerciseType.EJ5) {
                                        val allSecs = EJ5Section.entries
                                        val idx = allSecs.indexOf(currentEJ5Section)
                                        if (idx >= 0) {
                                            val nextSec = allSecs[(idx + 1) % allSecs.size]
                                            currentEJ5Section = nextSec
                                            store.lastEJ5Section = nextSec
                                            store.saveLastSelection()
                                        }
                                    } else if (currentExercise.isReichertExercise) {
                                        val allSecs = EJ4Section.entries
                                        val curSec = if (currentExercise == ExerciseType.R5) currentR5Section else currentR1Section
                                        val idx = allSecs.indexOf(curSec)
                                        if (idx >= 0) {
                                            val nextSec = allSecs[(idx + 1) % allSecs.size]
                                            if (currentExercise == ExerciseType.R5) {
                                                currentR5Section = nextSec
                                                store.lastR5Section = nextSec
                                            } else {
                                                currentR1Section = nextSec
                                                store.lastR1Section = nextSec
                                            }
                                            store.saveLastSelection()
                                        }
                                    } else {
                                        val allSecs = EJ10Section.entries
                                        val curSec = if (currentExercise == ExerciseType.EJ11) currentEJ11Section else currentEJ10Section
                                        val idx = allSecs.indexOf(curSec)
                                        if (idx >= 0) {
                                            val nextSec = allSecs[(idx + 1) % allSecs.size]
                                            if (currentExercise == ExerciseType.EJ11) {
                                                currentEJ11Section = nextSec
                                                store.lastEJ11Section = nextSec
                                            } else {
                                                currentEJ10Section = nextSec
                                                store.lastEJ10Section = nextSec
                                            }
                                            store.saveLastSelection()
                                        }
                                    }
                                },
                                shape = RoundedCornerShape(16.dp),
                                modifier = Modifier.height(48.dp),
                                contentPadding = PaddingValues(horizontal = 10.dp)
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.spacedBy(5.dp)
                                ) {
                                    Text(
                                        text = when (currentExercise) {
                                            ExerciseType.EJ5 -> loc.t("ej5_next_section")
                                            ExerciseType.EJ10 -> loc.t("ej10_next_section")
                                            ExerciseType.EJ11 -> loc.t("ej11_next_section")
                                            else -> loc.t("ej4_next_section")
                                        },
                                        fontSize = 12.sp,
                                        fontWeight = FontWeight.SemiBold,
                                        maxLines = 1
                                    )
                                    Surface(
                                        shape = RoundedCornerShape(percent = 50),
                                        color = MaterialTheme.colorScheme.surfaceVariant
                                    ) {
                                        val secCountLabel = when (currentExercise) {
                                            ExerciseType.EJ5 -> "${currentEJ5Section.id + 1}/12"
                                            ExerciseType.EJ10 -> "${currentEJ10Section.id + 1}/12"
                                            ExerciseType.EJ11 -> "${currentEJ11Section.id + 1}/12"
                                            ExerciseType.R1 -> "${currentR1Section.id + 1}/25"
                                            ExerciseType.R5 -> "${currentR5Section.id + 1}/25"
                                            else -> ""
                                        }
                                        Text(
                                            text = secCountLabel,
                                            fontSize = 10.sp,
                                            fontWeight = FontWeight.Bold,
                                            fontFamily = FontFamily.Monospace,
                                            modifier = Modifier.padding(horizontal = 5.dp, vertical = 2.dp)
                                        )
                                    }
                                }
                            }

                            if (isEJ5TypeFullyDone) {
                                Button(
                                    onClick = {
                                        when (currentExercise) {
                                            ExerciseType.EJ5 -> showEJ5CompletionDialog = true
                                            ExerciseType.EJ10 -> showEJ10CompletionDialog = true
                                            else -> showEJ11CompletionDialog = true
                                        }
                                    },
                                    modifier = Modifier
                                        .weight(1f)
                                        .height(48.dp),
                                    shape = RoundedCornerShape(16.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF10B981)),
                                    contentPadding = PaddingValues(horizontal = 10.dp)
                                ) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(5.dp)
                                    ) {
                                        Icon(
                                            Icons.Default.CheckCircle,
                                            contentDescription = null,
                                            modifier = Modifier.size(16.dp)
                                        )
                                        val doneLabel = when (currentExercise) {
                                            ExerciseType.EJ5 -> loc.t("ej5_ten_arts_completed")
                                            ExerciseType.EJ10 -> loc.t("ej10_ten_arts_completed")
                                            else -> loc.t("ej11_ten_arts_completed")
                                        }
                                        Text(
                                            text = "✓ $doneLabel",
                                            fontSize = 12.sp,
                                            fontWeight = FontWeight.Bold,
                                            maxLines = 1,
                                            overflow = TextOverflow.Ellipsis
                                        )
                                    }
                                }
                            } else {
                                Button(
                                    onClick = {
                                        scorePlayer.stop()
                                        if (curArt == EJ5Articulation.ORIGINAL) {
                                            when (currentExercise) {
                                                ExerciseType.EJ5 -> {
                                                    currentEJ5Articulation = EJ5Articulation.ALL_SLURRED
                                                    store.lastEJ5Articulation = currentEJ5Articulation
                                                }
                                                ExerciseType.EJ10 -> {
                                                    currentEJ10Articulation = EJ5Articulation.ALL_SLURRED
                                                    store.lastEJ10Articulation = currentEJ10Articulation
                                                }
                                                ExerciseType.EJ11 -> {
                                                    currentEJ11Articulation = EJ5Articulation.ALL_SLURRED
                                                    store.lastEJ11Articulation = currentEJ11Articulation
                                                }
                                                ExerciseType.R1 -> {
                                                    currentR1Articulation = EJ5Articulation.ALL_SLURRED
                                                    store.lastR1Articulation = currentR1Articulation
                                                }
                                                ExerciseType.R5 -> {
                                                    currentR5Articulation = EJ5Articulation.ALL_SLURRED
                                                    store.lastR5Articulation = currentR5Articulation
                                                }
                                                else -> {}
                                            }
                                            store.saveLastSelection()
                                        } else {
                                            store.markEJ5TypeCompleted(curArt, currentExercise)
                                            if (store.isEJ5TypeFullyCompleted(currentExercise)) {
                                                when (currentExercise) {
                                                    ExerciseType.EJ5 -> showEJ5CompletionDialog = true
                                                    ExerciseType.EJ10 -> showEJ10CompletionDialog = true
                                                    else -> showEJ11CompletionDialog = true
                                                }
                                            } else {
                                                val allPractice = EJ5Articulation.practiceCases
                                                val idx = allPractice.indexOf(curArt)
                                                if (idx >= 0) {
                                                    val nextArt = allPractice[(idx + 1) % allPractice.size]
                                                    when (currentExercise) {
                                                        ExerciseType.EJ5 -> {
                                                            currentEJ5Articulation = nextArt
                                                            store.lastEJ5Articulation = nextArt
                                                        }
                                                        ExerciseType.EJ10 -> {
                                                            currentEJ10Articulation = nextArt
                                                            store.lastEJ10Articulation = nextArt
                                                        }
                                                        ExerciseType.EJ11 -> {
                                                            currentEJ11Articulation = nextArt
                                                            store.lastEJ11Articulation = nextArt
                                                        }
                                                        ExerciseType.R1 -> {
                                                            currentR1Articulation = nextArt
                                                            store.lastR1Articulation = nextArt
                                                        }
                                                        ExerciseType.R5 -> {
                                                            currentR5Articulation = nextArt
                                                            store.lastR5Articulation = nextArt
                                                        }
                                                        else -> {}
                                                    }
                                                    store.saveLastSelection()
                                                }
                                            }
                                        }
                                    },
                                    modifier = Modifier
                                        .weight(1f)
                                        .height(48.dp),
                                    shape = RoundedCornerShape(16.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
                                    contentPadding = PaddingValues(horizontal = 10.dp)
                                ) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                                    ) {
                                        Text(
                                            text = loc.t("next_art"),
                                            fontSize = 13.sp,
                                            fontWeight = FontWeight.Bold,
                                            maxLines = 1
                                        )
                                        Surface(
                                            shape = RoundedCornerShape(percent = 50),
                                            color = Color.White.copy(alpha = 0.2f)
                                        ) {
                                            Text(
                                                text = "$ej5TypeDoneCount/10",
                                                fontSize = 10.sp,
                                                fontWeight = FontWeight.Bold,
                                                fontFamily = FontFamily.Monospace,
                                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                            )
                                        }
                                        Icon(
                                            Icons.Default.ArrowForward,
                                            contentDescription = null,
                                            modifier = Modifier.size(14.dp)
                                        )
                                    }
                                }
                            }
                        }
                    } else {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            OutlinedButton(
                                onClick = {
                                    scorePlayer.stop()
                                    store.markCompleted(currentTonic, currentMode, currentArticulation)
                                    val allArt = ArticulationPattern.entries
                                    val curIdx = allArt.indexOf(currentArticulation)
                                    if (curIdx + 1 < allArt.size) {
                                        currentArticulation = allArt[curIdx + 1]
                                    } else {
                                        if (store.areAllSevenModesPracticed(currentTonic)) {
                                            showCompletionDialog = true
                                        } else {
                                            val modeOrder = listOf(
                                                ModeType.IONIAN, ModeType.LYDIAN, ModeType.MIXOLYDIAN,
                                                ModeType.DORIAN, ModeType.AEOLIAN, ModeType.PHRYGIAN, ModeType.LOCRIAN
                                            )
                                            val mIdx = modeOrder.indexOf(currentMode)
                                            if (mIdx >= 0) {
                                                currentMode = modeOrder[(mIdx + 1) % modeOrder.size]
                                                currentArticulation = ArticulationPattern.ALL_SLURRED
                                            }
                                        }
                                    }
                                },
                                shape = RoundedCornerShape(16.dp),
                                modifier = Modifier.height(48.dp),
                                contentPadding = PaddingValues(horizontal = 10.dp)
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.spacedBy(5.dp)
                                ) {
                                    Text(
                                        text = loc.t("next_art"),
                                        fontSize = 12.sp,
                                        fontWeight = FontWeight.SemiBold,
                                        maxLines = 1
                                    )
                                    Surface(
                                        shape = RoundedCornerShape(percent = 50),
                                        color = MaterialTheme.colorScheme.surfaceVariant
                                    ) {
                                        Text(
                                            text = "$completedArtCount/8",
                                            fontSize = 10.sp,
                                            fontWeight = FontWeight.Bold,
                                            fontFamily = FontFamily.Monospace,
                                            modifier = Modifier.padding(horizontal = 5.dp, vertical = 2.dp)
                                        )
                                    }
                                }
                            }

                            if (areAllModesPracticed) {
                                Button(
                                    onClick = { showCompletionDialog = true },
                                    modifier = Modifier
                                        .weight(1f)
                                        .height(48.dp),
                                    shape = RoundedCornerShape(16.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF10B981)),
                                    contentPadding = PaddingValues(horizontal = 10.dp)
                                ) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(5.dp)
                                    ) {
                                        Icon(
                                            Icons.Default.CheckCircle,
                                            contentDescription = null,
                                            modifier = Modifier.size(16.dp)
                                        )
                                        Text(
                                            text = "✓ ${loc.t("seven_modes_completed")}",
                                            fontSize = 12.sp,
                                            fontWeight = FontWeight.Bold,
                                            maxLines = 1,
                                            overflow = TextOverflow.Ellipsis
                                        )
                                    }
                                }
                            } else if (isModeFullyDone) {
                                Button(
                                    onClick = {
                                        scorePlayer.stop()
                                        val modeOrder = listOf(
                                            ModeType.IONIAN, ModeType.LYDIAN, ModeType.MIXOLYDIAN,
                                            ModeType.DORIAN, ModeType.AEOLIAN, ModeType.PHRYGIAN, ModeType.LOCRIAN
                                        )
                                        val curIdx = modeOrder.indexOf(currentMode)
                                        if (curIdx >= 0) {
                                            currentMode = modeOrder[(curIdx + 1) % modeOrder.size]
                                            currentArticulation = ArticulationPattern.ALL_SLURRED
                                        }
                                        if (store.areAllSevenModesPracticed(currentTonic)) {
                                            showCompletionDialog = true
                                        }
                                    },
                                    modifier = Modifier
                                        .weight(1f)
                                        .height(48.dp),
                                    shape = RoundedCornerShape(16.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF10B981)),
                                    contentPadding = PaddingValues(horizontal = 10.dp)
                                ) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(5.dp)
                                    ) {
                                        Icon(
                                            Icons.Default.CheckCircle,
                                            contentDescription = null,
                                            modifier = Modifier.size(16.dp)
                                        )
                                        Text(
                                            text = loc.t("mode_done"),
                                            fontSize = 12.sp,
                                            fontWeight = FontWeight.Bold,
                                            maxLines = 1
                                        )
                                        Surface(
                                            shape = RoundedCornerShape(percent = 50),
                                            color = Color.White.copy(alpha = 0.25f)
                                        ) {
                                            Text(
                                                text = "$practicedModesCount/7",
                                                fontSize = 10.sp,
                                                fontWeight = FontWeight.Bold,
                                                fontFamily = FontFamily.Monospace,
                                                modifier = Modifier.padding(horizontal = 5.dp, vertical = 2.dp)
                                            )
                                        }
                                        Icon(
                                            Icons.Default.ArrowForward,
                                            contentDescription = null,
                                            modifier = Modifier.size(14.dp)
                                        )
                                    }
                                }
                            } else {
                                Button(
                                    onClick = {
                                        scorePlayer.stop()
                                        store.markCompleted(currentTonic, currentMode, currentArticulation)

                                        val wasAllPracticed = store.areAllSevenModesPracticed(currentTonic)

                                        val modeOrder = listOf(
                                            ModeType.IONIAN, ModeType.LYDIAN, ModeType.MIXOLYDIAN,
                                            ModeType.DORIAN, ModeType.AEOLIAN, ModeType.PHRYGIAN, ModeType.LOCRIAN
                                        )
                                        val curIdx = modeOrder.indexOf(currentMode)
                                        if (curIdx >= 0) {
                                            currentMode = modeOrder[(curIdx + 1) % modeOrder.size]
                                            currentArticulation = ArticulationPattern.ALL_SLURRED
                                        }

                                        if (wasAllPracticed) {
                                            showCompletionDialog = true
                                        }
                                    },
                                    modifier = Modifier
                                        .weight(1f)
                                        .height(48.dp),
                                    shape = RoundedCornerShape(16.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
                                    contentPadding = PaddingValues(horizontal = 10.dp)
                                ) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(5.dp)
                                    ) {
                                        Text(
                                            text = loc.t("next_mode"),
                                            fontSize = 12.sp,
                                            fontWeight = FontWeight.Bold,
                                            maxLines = 1
                                        )
                                        Surface(
                                            shape = RoundedCornerShape(percent = 50),
                                            color = Color.White.copy(alpha = 0.2f)
                                        ) {
                                            Text(
                                                text = "$practicedModesCount/7",
                                                fontSize = 10.sp,
                                                fontWeight = FontWeight.Bold,
                                                fontFamily = FontFamily.Monospace,
                                                modifier = Modifier.padding(horizontal = 5.dp, vertical = 2.dp)
                                            )
                                        }
                                        Icon(
                                            Icons.Default.ArrowForward,
                                            contentDescription = null,
                                            modifier = Modifier.size(14.dp)
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
