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
    initialTonic: Tonic,
    initialMode: ModeType,
    store: PracticeStore,
    loc: LocalizationManager,
    metronome: MetronomeEngine,
    scorePlayer: ScoreAudioPlayer,
    onBack: () -> Unit,
    onOpenMatrix: () -> Unit
) {
    var currentTonic by remember { mutableStateOf(initialTonic) }
    var currentMode by remember { mutableStateOf(initialMode) }
    var currentArticulation by remember { mutableStateOf(ArticulationPattern.ALL_SLURRED) }
    var showCompletionDialog by remember { mutableStateOf(false) }

    val currentAbcScore = remember(currentTonic, currentMode, currentArticulation, metronome.tempoBPM, loc.currentLanguage) {
        ExerciseGenerator.generateABC(
            tonic = currentTonic,
            mode = currentMode,
            articulation = currentArticulation,
            tempoBPM = metronome.tempoBPM,
            loc = loc
        )
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
                        .padding(horizontal = 14.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.clickable { onBack() }
                    ) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("FluteModes", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    }

                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        IconButton(
                            onClick = onOpenMatrix,
                            modifier = Modifier
                                .size(36.dp)
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.primaryContainer)
                        ) {
                            Icon(
                                Icons.Default.GridView,
                                contentDescription = "Matrix",
                                modifier = Modifier.size(18.dp),
                                tint = MaterialTheme.colorScheme.onPrimaryContainer
                            )
                        }

                        Button(
                            onClick = { loc.toggleLanguage() },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = MaterialTheme.colorScheme.primaryContainer,
                                contentColor = MaterialTheme.colorScheme.onPrimaryContainer
                            ),
                            shape = RoundedCornerShape(12.dp),
                            contentPadding = PaddingValues(horizontal = 10.dp, vertical = 4.dp),
                            modifier = Modifier.height(34.dp)
                        ) {
                            Text("${loc.currentLanguage.flag} ${loc.currentLanguage.displayName}", fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
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
            // Mode Header Card
            Surface(
                color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f),
                modifier = Modifier.fillMaxWidth()
            ) {
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
                                scorePlayer.toggle(
                                    tonic = currentTonic,
                                    mode = currentMode,
                                    articulation = currentArticulation,
                                    tempoBPM = metronome.tempoBPM
                                )
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
