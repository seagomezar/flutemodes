package com.seagomezar.flutemodes.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.seagomezar.flutemodes.model.*

@Composable
fun HomeScreen(
    store: PracticeStore,
    loc: LocalizationManager,
    onStartPractice: (Tonic, ModeType) -> Unit,
    onStartEJ1Practice: (EJ1Articulation) -> Unit,
    onStartEJ2Practice: (EJ1Articulation) -> Unit,
    onStartEJ4Practice: (EJ4Articulation, EJ4Section) -> Unit,
    onStartEJ5Practice: (EJ5Articulation, EJ5Section) -> Unit,
    onStartEJ10Practice: (EJ5Articulation, EJ10Section) -> Unit,
    onStartEJ11Practice: (EJ5Articulation, EJ10Section) -> Unit,
    onStartReichertPractice: (ExerciseType, Any, Any) -> Unit = { _, _, _ -> },
    onOpenMatrix: () -> Unit
) {
    var selectedExercise by remember { mutableStateOf(store.lastExerciseType) }
    var selectedEJ1Art by remember { mutableStateOf(store.lastEJ1Articulation) }
    var selectedEJ2Art by remember { mutableStateOf(store.lastEJ2Articulation) }
    var selectedEJ4Art by remember { mutableStateOf(store.lastEJ4Articulation) }
    var selectedEJ4Section by remember { mutableStateOf(store.lastEJ4Section) }
    var selectedEJ5Art by remember { mutableStateOf(store.lastEJ5Articulation) }
    var selectedEJ5Section by remember { mutableStateOf(store.lastEJ5Section) }
    var selectedEJ10Art by remember { mutableStateOf(store.lastEJ10Articulation) }
    var selectedEJ10Section by remember { mutableStateOf(store.lastEJ10Section) }
    var selectedEJ11Art by remember { mutableStateOf(store.lastEJ11Articulation) }
    var selectedEJ11Section by remember { mutableStateOf(store.lastEJ11Section) }
    var selectedR1Art by remember { mutableStateOf(store.lastR1Articulation) }
    var selectedR1Section by remember { mutableStateOf(store.lastR1Section) }
    var selectedR2Art by remember { mutableStateOf(store.lastR2Articulation) }
    var selectedR2Section by remember { mutableStateOf(store.lastR2Section) }
    var selectedR4Art by remember { mutableStateOf(store.lastR4Articulation) }
    var selectedR4Section by remember { mutableStateOf(store.lastR4Section) }
    var selectedR5Art by remember { mutableStateOf(store.lastR5Articulation) }
    var selectedR5Section by remember { mutableStateOf(store.lastR5Section) }
    var selectedTonic by remember { mutableStateOf(store.lastTonic ?: Tonic.DO_NATURAL) }
    var selectedMode by remember { mutableStateOf(store.lastMode ?: ModeType.IONIAN) }
    var selectedModalScheme by remember { mutableStateOf(store.lastModalScheme) }
    var showPracticeWizard by remember { mutableStateOf(false) }
    var wizardDuration by remember { mutableStateOf(PracticeWizardDuration.MIN_30) }
    var wizardFocus by remember { mutableStateOf(PracticeWizardFocus.MODES840) }
    var wizardTonic by remember { mutableStateOf(selectedTonic) }
    var wizardMode by remember { mutableStateOf(selectedMode) }

    val majorModes = listOf(ModeType.IONIAN, ModeType.LYDIAN, ModeType.MIXOLYDIAN)
    val minorModes = listOf(ModeType.DORIAN, ModeType.AEOLIAN, ModeType.PHRYGIAN, ModeType.LOCRIAN)

    fun launchRoutineBlock(block: PracticeRoutineBlock) {
        showPracticeWizard = false
        val secIdx = block.sectionIndex
        when (block.exercise) {
            ExerciseType.EJ1 -> onStartEJ1Practice(selectedEJ1Art)
            ExerciseType.EJ2 -> onStartEJ2Practice(selectedEJ2Art)
            ExerciseType.EJ4 -> {
                val sec = EJ4Section.entries.getOrElse(secIdx) { EJ4Section.C_MAJOR }
                selectedEJ4Section = sec
                onStartEJ4Practice(selectedEJ4Art, sec)
            }
            ExerciseType.EJ5 -> {
                val sec = EJ5Section.entries.getOrElse(secIdx % 12) { EJ5Section.C_CHROM }
                selectedEJ5Section = sec
                onStartEJ5Practice(selectedEJ5Art, sec)
            }
            ExerciseType.EJ10 -> {
                val sec = EJ10Section.entries.getOrElse(secIdx % 12) { EJ10Section.C_ARP }
                selectedEJ10Section = sec
                onStartEJ10Practice(selectedEJ10Art, sec)
            }
            ExerciseType.EJ11 -> {
                val sec = EJ10Section.entries.getOrElse(secIdx % 12) { EJ10Section.C_ARP }
                selectedEJ11Section = sec
                onStartEJ11Practice(selectedEJ11Art, sec)
            }
            ExerciseType.R1 -> {
                val sec = EJ4Section.entries.getOrElse(secIdx) { EJ4Section.C_MAJOR }
                selectedR1Section = sec
                onStartReichertPractice(ExerciseType.R1, selectedR1Art, sec)
            }
            ExerciseType.R2 -> {
                val sec = EJ4Section.entries.getOrElse(secIdx) { EJ4Section.C_MAJOR }
                selectedR2Section = sec
                onStartReichertPractice(ExerciseType.R2, selectedR2Art, sec)
            }
            ExerciseType.R4 -> {
                val sec = EJ4Section.entries.getOrElse(secIdx) { EJ4Section.C_MAJOR }
                selectedR4Section = sec
                onStartReichertPractice(ExerciseType.R4, selectedR4Art, sec)
            }
            ExerciseType.R5 -> {
                val sec = EJ4Section.entries.getOrElse(secIdx) { EJ4Section.C_MAJOR }
                selectedR5Section = sec
                onStartReichertPractice(ExerciseType.R5, selectedR5Art, sec)
            }
            ExerciseType.MODOS -> {
                selectedTonic = block.tonic
                selectedMode = block.mode
                selectedModalScheme = block.modalScheme
                store.lastTonic = block.tonic
                store.lastMode = block.mode
                store.lastModalScheme = block.modalScheme
                store.saveLastSelection()
                onStartPractice(block.tonic, block.mode)
            }
        }
    }

    fun resumeLastSession() {
        when (selectedExercise) {
            ExerciseType.EJ1 -> onStartEJ1Practice(selectedEJ1Art)
            ExerciseType.EJ2 -> onStartEJ2Practice(selectedEJ2Art)
            ExerciseType.EJ4 -> onStartEJ4Practice(selectedEJ4Art, selectedEJ4Section)
            ExerciseType.EJ5 -> onStartEJ5Practice(selectedEJ5Art, selectedEJ5Section)
            ExerciseType.EJ10 -> onStartEJ10Practice(selectedEJ10Art, selectedEJ10Section)
            ExerciseType.EJ11 -> onStartEJ11Practice(selectedEJ11Art, selectedEJ11Section)
            ExerciseType.R1 -> onStartReichertPractice(ExerciseType.R1, selectedR1Art, selectedR1Section)
            ExerciseType.R2 -> onStartReichertPractice(ExerciseType.R2, selectedR2Art, selectedR2Section)
            ExerciseType.R4 -> onStartReichertPractice(ExerciseType.R4, selectedR4Art, selectedR4Section)
            ExerciseType.R5 -> onStartReichertPractice(ExerciseType.R5, selectedR5Art, selectedR5Section)
            ExerciseType.MODOS -> {
                store.lastModalScheme = selectedModalScheme
                store.saveLastSelection()
                onStartPractice(selectedTonic, selectedMode)
            }
        }
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
                        .padding(horizontal = 20.dp, vertical = 14.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = loc.t("app_name"),
                            fontSize = 24.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        Text(
                            text = if (selectedExercise == ExerciseType.MODOS) selectedModalScheme.title(loc) else if (selectedExercise.isReichertExercise) "M.-A. Reichert · Op. 5" else "Taffanel & Gaubert",
                            fontSize = 11.5.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }

                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        IconButton(
                            onClick = onOpenMatrix,
                            modifier = Modifier
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.primaryContainer)
                        ) {
                            Icon(
                                Icons.Default.GridView,
                                contentDescription = "Matrix",
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
                            contentPadding = PaddingValues(horizontal = 10.dp, vertical = 6.dp)
                        ) {
                            Text("${loc.currentLanguage.flag} ${loc.currentLanguage.displayName}", fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
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
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 16.dp, vertical = 12.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Opción 1 (Conservatory Coach) Hero Card + 1-Tap Resume + 3-Step Practice Wizard
            ConservatoryCoachHeroCard(
                loc = loc,
                selectedExercise = selectedExercise,
                selectedTonic = selectedTonic,
                selectedMode = selectedMode,
                selectedModalScheme = selectedModalScheme,
                wizardDuration = wizardDuration,
                onSelectDurationPreset = { dur ->
                    wizardDuration = dur
                    wizardTonic = selectedTonic
                    wizardMode = selectedMode
                    showPracticeWizard = true
                },
                onResumeLastSession = { resumeLastSession() },
                onOpenWizard = {
                    wizardTonic = selectedTonic
                    wizardMode = selectedMode
                    showPracticeWizard = true
                }
            )

            // 3-Collection Exercise Selector (All 11 exercises visible on screen without horizontal scroll)
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                // 1. Taffanel & Gaubert — 6 Exercises in 2 rows of 3
                Text(
                    text = "TAFFANEL & GAUBERT",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(horizontal = 4.dp)
                )
                val tgRows = listOf(
                    listOf(ExerciseType.EJ1, ExerciseType.EJ2, ExerciseType.EJ4),
                    listOf(ExerciseType.EJ5, ExerciseType.EJ10, ExerciseType.EJ11)
                )
                tgRows.forEach { rowExs ->
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        rowExs.forEach { ex ->
                            val isSel = selectedExercise == ex
                            Surface(
                                onClick = {
                                    selectedExercise = ex
                                    store.lastExerciseType = ex
                                    store.saveLastSelection()
                                },
                                modifier = Modifier.weight(1f),
                                shape = RoundedCornerShape(12.dp),
                                color = if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                tonalElevation = if (isSel) 4.dp else 0.dp
                            ) {
                                Column(
                                    modifier = Modifier.padding(horizontal = 6.dp, vertical = 8.dp),
                                    horizontalAlignment = Alignment.CenterHorizontally
                                ) {
                                    Text(
                                        text = ex.homeButtonTitle,
                                        fontSize = 12.sp,
                                        fontWeight = FontWeight.Bold,
                                        maxLines = 1,
                                        color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                    Text(
                                        text = ex.homeButtonSubtitle(loc),
                                        fontSize = 9.sp,
                                        maxLines = 1,
                                        color = if (isSel) MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.85f) else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.75f)
                                    )
                                }
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(2.dp))

                // 2. M.-A. Reichert Op. 5 — 4 Exercises in 2 rows of 2
                Text(
                    text = "M.-A. REICHERT · OP. 5",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF6366F1),
                    modifier = Modifier.padding(horizontal = 4.dp)
                )
                val reichertRows = listOf(
                    listOf(ExerciseType.R1, ExerciseType.R2),
                    listOf(ExerciseType.R4, ExerciseType.R5)
                )
                reichertRows.forEach { rowExs ->
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        rowExs.forEach { ex ->
                            val isSel = selectedExercise == ex
                            Surface(
                                onClick = {
                                    selectedExercise = ex
                                    store.lastExerciseType = ex
                                    store.saveLastSelection()
                                },
                                modifier = Modifier.weight(1f),
                                shape = RoundedCornerShape(12.dp),
                                color = if (isSel) Color(0xFF6366F1) else MaterialTheme.colorScheme.surfaceVariant,
                                border = if (!isSel) androidx.compose.foundation.BorderStroke(1.dp, Color(0xFF6366F1).copy(alpha = 0.35f)) else null,
                                tonalElevation = if (isSel) 4.dp else 0.dp
                            ) {
                                Column(
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 8.dp),
                                    horizontalAlignment = Alignment.CenterHorizontally
                                ) {
                                    Text(
                                        text = ex.homeButtonTitle,
                                        fontSize = 12.sp,
                                        fontWeight = FontWeight.Bold,
                                        maxLines = 1,
                                        color = if (isSel) Color.White else MaterialTheme.colorScheme.onSurface
                                    )
                                    Text(
                                        text = ex.homeButtonSubtitle(loc),
                                        fontSize = 9.5.sp,
                                        maxLines = 1,
                                        color = if (isSel) Color.White.copy(alpha = 0.9f) else MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(2.dp))

                // 3. Sistema Modal Paralelo (84 Modos)
                val isModosSel = selectedExercise == ExerciseType.MODOS
                Surface(
                    onClick = {
                        selectedExercise = ExerciseType.MODOS
                        store.lastExerciseType = ExerciseType.MODOS
                        store.saveLastSelection()
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    color = if (isModosSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                    tonalElevation = if (isModosSel) 4.dp else 0.dp
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 14.dp, vertical = 10.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Default.GridView,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp),
                                tint = if (isModosSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = ExerciseType.MODOS.homeButtonTitle,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (isModosSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                        Text(
                            text = ExerciseType.MODOS.homeButtonSubtitle(loc),
                            fontSize = 11.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = if (isModosSel) MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.85f) else MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }

            // Header Description
            Card(
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer),
                shape = RoundedCornerShape(16.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = when (selectedExercise) {
                            ExerciseType.EJ1 -> loc.t("ej1_title")
                            ExerciseType.EJ2 -> loc.t("ej2_title")
                            ExerciseType.EJ4 -> loc.t("ej4_title")
                            ExerciseType.EJ5 -> loc.t("ej5_title")
                            ExerciseType.EJ10 -> loc.t("ej10_title")
                            ExerciseType.EJ11 -> loc.t("ej11_title")
                            ExerciseType.R1 -> loc.t("r1_title")
                            ExerciseType.R2 -> loc.t("r2_title")
                            ExerciseType.R4 -> loc.t("r4_title")
                            ExerciseType.R5 -> loc.t("r5_title")
                            ExerciseType.MODOS -> selectedModalScheme.title(loc)
                        },
                        fontSize = 15.sp,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = when (selectedExercise) {
                            ExerciseType.EJ1 -> loc.t("ej1_sub_desc")
                            ExerciseType.EJ2 -> loc.t("ej2_sub_desc")
                            ExerciseType.EJ4 -> loc.t("ej4_sub_desc")
                            ExerciseType.EJ5 -> loc.t("ej5_sub_desc")
                            ExerciseType.EJ10 -> loc.t("ej10_sub_desc")
                            ExerciseType.EJ11 -> loc.t("ej11_sub_desc")
                            ExerciseType.R1 -> loc.t("r1_sub_desc")
                            ExerciseType.R2 -> loc.t("r2_sub_desc")
                            ExerciseType.R4 -> loc.t("r4_sub_desc")
                            ExerciseType.R5 -> loc.t("r5_sub_desc")
                            ExerciseType.MODOS -> loc.t("sub_desc")
                        },
                        fontSize = 12.sp,
                        color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.85f)
                    )
                }
            }

            if (selectedExercise.isChromaticExercise) {
                val isEJ2 = selectedExercise == ExerciseType.EJ2
                val doneCount = store.chromaticCompletedCount(selectedExercise)
                val allDone = store.isChromaticFullyCompleted(selectedExercise)
                val currentSelArt = if (isEJ2) selectedEJ2Art else selectedEJ1Art

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = loc.t(if (isEJ2) "ej2_select_art" else "ej1_select_art"),
                            fontSize = 15.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary
                        )
                        Text(
                            text = loc.t(if (isEJ2) "ej2_header_info" else "ej1_header_info"),
                            fontSize = 11.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }

                    Surface(
                        shape = RoundedCornerShape(8.dp),
                        color = if (allDone) Color(0xFF10B981).copy(alpha = 0.2f) else MaterialTheme.colorScheme.primary.copy(alpha = 0.15f)
                    ) {
                        Text(
                            text = "$doneCount/10 ${loc.t("arts_count")}",
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            color = if (allDone) Color(0xFF10B981) else MaterialTheme.colorScheme.primary,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                        )
                    }
                }

                EJ1Articulation.entries.forEach { art ->
                    val isSelected = currentSelArt == art
                    val isDone = store.isChromaticCompleted(art, selectedExercise)

                    Surface(
                        onClick = {
                            if (isEJ2) {
                                selectedEJ2Art = art
                                onStartEJ2Practice(art)
                            } else {
                                selectedEJ1Art = art
                                onStartEJ1Practice(art)
                            }
                        },
                        shape = RoundedCornerShape(14.dp),
                        color = if (isSelected) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surface,
                        border = if (isSelected) androidx.compose.foundation.BorderStroke(2.dp, MaterialTheme.colorScheme.primary) else androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(
                            modifier = Modifier
                                .padding(14.dp)
                                .fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = art.title(loc),
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                Spacer(modifier = Modifier.height(2.dp))
                                Text(
                                    text = art.formulaBadge,
                                    fontSize = 11.sp,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }

                            if (art == EJ1Articulation.ORIGINAL) {
                                Surface(
                                    shape = RoundedCornerShape(8.dp),
                                    color = Color(0xFF6366F1).copy(alpha = 0.18f)
                                ) {
                                    Text(
                                        text = "Original",
                                        fontSize = 11.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = Color(0xFF6366F1),
                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                    )
                                }
                            } else if (isDone) {
                                Surface(
                                    shape = RoundedCornerShape(8.dp),
                                    color = Color(0xFF10B981).copy(alpha = 0.2f)
                                ) {
                                    Row(
                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(4.dp)
                                    ) {
                                        Icon(
                                            Icons.Default.CheckCircle,
                                            contentDescription = null,
                                            tint = Color(0xFF10B981),
                                            modifier = Modifier.size(12.dp)
                                        )
                                        Text(
                                            text = loc.t("completed"),
                                            fontSize = 11.sp,
                                            fontWeight = FontWeight.Bold,
                                            color = Color(0xFF10B981)
                                        )
                                    }
                                }
                            } else {
                                Icon(
                                    Icons.Default.ArrowForward,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.size(16.dp)
                                )
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(4.dp))

                Button(
                    onClick = {
                        if (isEJ2) {
                            onStartEJ2Practice(selectedEJ2Art)
                        } else {
                            onStartEJ1Practice(selectedEJ1Art)
                        }
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp),
                    shape = RoundedCornerShape(18.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "${loc.t(if (isEJ2) "ej2_start_practice" else "ej1_start_practice")} (${currentSelArt.shortTitle(loc)})",
                        fontSize = 15.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            } else if (selectedExercise.isEJ4Exercise) {
                val ex = selectedExercise
                val doneCount = store.ej4TypeCompletedCount(ex)
                val allDone = store.isEJ4TypeFullyCompleted(ex)
                val curSec = when (ex) {
                    ExerciseType.R2 -> selectedR2Section
                    ExerciseType.R4 -> selectedR4Section
                    else -> selectedEJ4Section
                }
                val curArt = when (ex) {
                    ExerciseType.R2 -> selectedR2Art
                    ExerciseType.R4 -> selectedR4Art
                    else -> selectedEJ4Art
                }

                Column {
                    Text(
                        text = loc.t("${ex.id}_select_section"),
                        fontSize = 14.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(horizontal = 4.dp, vertical = 4.dp)
                    )

                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .horizontalScroll(rememberScrollState()),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        EJ4Section.entries.forEach { sec ->
                            val isSel = sec == curSec
                            Surface(
                                onClick = {
                                    when (ex) {
                                        ExerciseType.R2 -> {
                                            selectedR2Section = sec
                                            store.lastR2Section = sec
                                        }
                                        ExerciseType.R4 -> {
                                            selectedR4Section = sec
                                            store.lastR4Section = sec
                                        }
                                        else -> {
                                            selectedEJ4Section = sec
                                            store.lastEJ4Section = sec
                                        }
                                    }
                                    store.saveLastSelection()
                                },
                                shape = RoundedCornerShape(12.dp),
                                color = if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                tonalElevation = if (isSel) 4.dp else 0.dp,
                                modifier = Modifier.padding(vertical = 4.dp)
                            ) {
                                Column(
                                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
                                    horizontalAlignment = Alignment.CenterHorizontally
                                ) {
                                    Text(
                                        text = sec.shortBadge(ex),
                                        fontSize = 13.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                    Text(
                                        text = sec.measureRange(ex),
                                        fontSize = 10.sp,
                                        color = if (isSel) MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.8f) else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                                    )
                                }
                            }
                        }
                    }
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = loc.t("${ex.id}_select_art"),
                            fontSize = 15.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary
                        )
                        Text(
                            text = loc.t("${ex.id}_header_info"),
                            fontSize = 11.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }

                    Surface(
                        shape = RoundedCornerShape(8.dp),
                        color = if (allDone) Color(0xFF10B981).copy(alpha = 0.2f) else MaterialTheme.colorScheme.primary.copy(alpha = 0.15f)
                    ) {
                        Text(
                            text = "$doneCount/8 ${loc.t("arts_count")}",
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            color = if (allDone) Color(0xFF10B981) else MaterialTheme.colorScheme.primary,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                        )
                    }
                }

                EJ4Articulation.entries.forEach { art ->
                    val isSelected = curArt == art
                    val isDone = store.isEJ4Completed(art, ex)

                    Surface(
                        onClick = {
                            when (ex) {
                                ExerciseType.R2 -> {
                                    selectedR2Art = art
                                    store.lastR2Articulation = art
                                    onStartReichertPractice(ex, art, selectedR2Section)
                                }
                                ExerciseType.R4 -> {
                                    selectedR4Art = art
                                    store.lastR4Articulation = art
                                    onStartReichertPractice(ex, art, selectedR4Section)
                                }
                                else -> {
                                    selectedEJ4Art = art
                                    onStartEJ4Practice(art, selectedEJ4Section)
                                }
                            }
                        },
                        shape = RoundedCornerShape(14.dp),
                        color = if (isSelected) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surface,
                        border = if (isSelected) androidx.compose.foundation.BorderStroke(2.dp, MaterialTheme.colorScheme.primary) else androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(
                            modifier = Modifier
                                .padding(14.dp)
                                .fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = art.title(loc),
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                Spacer(modifier = Modifier.height(2.dp))
                                Text(
                                    text = art.formulaBadge,
                                    fontSize = 11.sp,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }

                            if (art == EJ4Articulation.ORIGINAL) {
                                Surface(
                                    shape = RoundedCornerShape(8.dp),
                                    color = Color(0xFF6366F1).copy(alpha = 0.18f)
                                ) {
                                    Text(
                                        text = "Original",
                                        fontSize = 11.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = Color(0xFF6366F1),
                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                    )
                                }
                            } else if (isDone) {
                                Surface(
                                    shape = RoundedCornerShape(8.dp),
                                    color = Color(0xFF10B981).copy(alpha = 0.2f)
                                ) {
                                    Row(
                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(4.dp)
                                    ) {
                                        Icon(
                                            Icons.Default.CheckCircle,
                                            contentDescription = null,
                                            tint = Color(0xFF10B981),
                                            modifier = Modifier.size(12.dp)
                                        )
                                        Text(
                                            text = loc.t("completed"),
                                            fontSize = 11.sp,
                                            fontWeight = FontWeight.Bold,
                                            color = Color(0xFF10B981)
                                        )
                                    }
                                }
                            } else {
                                Icon(
                                    Icons.Default.ArrowForward,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.size(16.dp)
                                )
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(4.dp))

                Button(
                    onClick = {
                        if (ex.isReichertExercise) {
                            val curArt = if (ex == ExerciseType.R2) selectedR2Art else selectedR4Art
                            val curSec = if (ex == ExerciseType.R2) selectedR2Section else selectedR4Section
                            onStartReichertPractice(ex, curArt, curSec)
                        } else {
                            onStartEJ4Practice(selectedEJ4Art, selectedEJ4Section)
                        }
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp),
                    shape = RoundedCornerShape(18.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "${loc.t("${ex.id}_start_practice")} (${curSec.shortBadge(ex)} · ${curArt.shortTitle(loc)})",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1
                    )
                }
            } else if (selectedExercise.isEJ5TypeExercise) {
                val ex = selectedExercise
                val doneCount = store.ej5TypeCompletedCount(ex)
                val allDone = store.isEJ5TypeFullyCompleted(ex)
                val currentSelArt = when (ex) {
                    ExerciseType.EJ5 -> selectedEJ5Art
                    ExerciseType.EJ10 -> selectedEJ10Art
                    ExerciseType.EJ11 -> selectedEJ11Art
                    ExerciseType.R1 -> selectedR1Art
                    ExerciseType.R5 -> selectedR5Art
                    else -> selectedEJ5Art
                }

                Column {
                    Text(
                        text = loc.t("${ex.id}_select_section"),
                        fontSize = 14.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(horizontal = 4.dp, vertical = 4.dp)
                    )

                    if (ex.isReichertExercise) {
                        val curSec = if (ex == ExerciseType.R5) selectedR5Section else selectedR1Section
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .horizontalScroll(rememberScrollState()),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            EJ4Section.entries.forEach { sec ->
                                val isSel = sec == curSec
                                Surface(
                                    onClick = {
                                        if (ex == ExerciseType.R5) {
                                            selectedR5Section = sec
                                            store.lastR5Section = sec
                                        } else {
                                            selectedR1Section = sec
                                            store.lastR1Section = sec
                                        }
                                        store.saveLastSelection()
                                    },
                                    shape = RoundedCornerShape(12.dp),
                                    color = if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                    tonalElevation = if (isSel) 4.dp else 0.dp,
                                    modifier = Modifier.padding(vertical = 4.dp)
                                ) {
                                    Column(
                                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
                                        horizontalAlignment = Alignment.CenterHorizontally
                                    ) {
                                        Text(
                                            text = sec.shortBadge(ex),
                                            fontSize = 13.sp,
                                            fontWeight = FontWeight.Bold,
                                            color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                                        )
                                        Text(
                                            text = sec.measureRange(ex),
                                            fontSize = 10.sp,
                                            color = if (isSel) MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.8f) else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                                        )
                                    }
                                }
                            }
                        }
                    } else if (ex == ExerciseType.EJ5) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .horizontalScroll(rememberScrollState()),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            EJ5Section.entries.forEach { sec ->
                                val isSel = sec == selectedEJ5Section
                                Surface(
                                    onClick = {
                                        selectedEJ5Section = sec
                                        store.lastEJ5Section = sec
                                        store.saveLastSelection()
                                    },
                                    shape = RoundedCornerShape(12.dp),
                                    color = if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                    tonalElevation = if (isSel) 4.dp else 0.dp,
                                    modifier = Modifier.padding(vertical = 4.dp)
                                ) {
                                    Column(
                                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp),
                                        horizontalAlignment = Alignment.CenterHorizontally
                                    ) {
                                        Text(
                                            text = sec.title(loc),
                                            fontSize = 13.sp,
                                            fontWeight = FontWeight.Bold,
                                            color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                                        )
                                        Text(
                                            text = sec.measureRange,
                                            fontSize = 10.sp,
                                            color = if (isSel) MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.8f) else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                                        )
                                    }
                                }
                            }
                        }
                    } else {
                        val curSec = if (ex == ExerciseType.EJ11) selectedEJ11Section else selectedEJ10Section
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .horizontalScroll(rememberScrollState()),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            EJ10Section.entries.forEach { sec ->
                                val isSel = sec == curSec
                                Surface(
                                    onClick = {
                                        if (ex == ExerciseType.EJ11) {
                                            selectedEJ11Section = sec
                                            store.lastEJ11Section = sec
                                        } else {
                                            selectedEJ10Section = sec
                                            store.lastEJ10Section = sec
                                        }
                                        store.saveLastSelection()
                                    },
                                    shape = RoundedCornerShape(12.dp),
                                    color = if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                    tonalElevation = if (isSel) 4.dp else 0.dp,
                                    modifier = Modifier.padding(vertical = 4.dp)
                                ) {
                                    Column(
                                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
                                        horizontalAlignment = Alignment.CenterHorizontally
                                    ) {
                                        Text(
                                            text = sec.shortBadge,
                                            fontSize = 13.sp,
                                            fontWeight = FontWeight.Bold,
                                            color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                                        )
                                        Text(
                                            text = sec.measureRange,
                                            fontSize = 10.sp,
                                            color = if (isSel) MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.8f) else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                                        )
                                    }
                                }
                            }
                        }
                    }
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = loc.t("${ex.id}_select_art"),
                            fontSize = 15.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary
                        )
                        Text(
                            text = loc.t("${ex.id}_header_info"),
                            fontSize = 11.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }

                    Surface(
                        shape = RoundedCornerShape(8.dp),
                        color = if (allDone) Color(0xFF10B981).copy(alpha = 0.2f) else MaterialTheme.colorScheme.primary.copy(alpha = 0.15f)
                    ) {
                        Text(
                            text = "$doneCount/10 ${loc.t("arts_count")}",
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            color = if (allDone) Color(0xFF10B981) else MaterialTheme.colorScheme.primary,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                        )
                    }
                }

                EJ5Articulation.entries.forEach { art ->
                    val isSelected = currentSelArt == art
                    val isDone = store.isEJ5TypeCompleted(art, ex)

                    Surface(
                        onClick = {
                            when (ex) {
                                ExerciseType.EJ5 -> {
                                    selectedEJ5Art = art
                                    onStartEJ5Practice(art, selectedEJ5Section)
                                }
                                ExerciseType.EJ10 -> {
                                    selectedEJ10Art = art
                                    onStartEJ10Practice(art, selectedEJ10Section)
                                }
                                ExerciseType.EJ11 -> {
                                    selectedEJ11Art = art
                                    onStartEJ11Practice(art, selectedEJ11Section)
                                }
                                ExerciseType.R1 -> {
                                    selectedR1Art = art
                                    store.lastR1Articulation = art
                                    onStartReichertPractice(ex, art, selectedR1Section)
                                }
                                ExerciseType.R5 -> {
                                    selectedR5Art = art
                                    store.lastR5Articulation = art
                                    onStartReichertPractice(ex, art, selectedR5Section)
                                }
                                else -> {}
                            }
                        },
                        shape = RoundedCornerShape(14.dp),
                        color = if (isSelected) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surface,
                        border = if (isSelected) androidx.compose.foundation.BorderStroke(2.dp, MaterialTheme.colorScheme.primary) else androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(
                            modifier = Modifier
                                .padding(14.dp)
                                .fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = art.title(loc, ex),
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                Spacer(modifier = Modifier.height(2.dp))
                                Text(
                                    text = art.formulaBadge(ex),
                                    fontSize = 11.sp,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }

                            if (art == EJ5Articulation.ORIGINAL) {
                                Surface(
                                    shape = RoundedCornerShape(8.dp),
                                    color = Color(0xFF6366F1).copy(alpha = 0.18f)
                                ) {
                                    Text(
                                        text = "Original",
                                        fontSize = 11.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = Color(0xFF6366F1),
                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                    )
                                }
                            } else if (isDone) {
                                Surface(
                                    shape = RoundedCornerShape(8.dp),
                                    color = Color(0xFF10B981).copy(alpha = 0.2f)
                                ) {
                                    Row(
                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(4.dp)
                                    ) {
                                        Icon(
                                            Icons.Default.CheckCircle,
                                            contentDescription = null,
                                            tint = Color(0xFF10B981),
                                            modifier = Modifier.size(12.dp)
                                        )
                                        Text(
                                            text = loc.t("completed"),
                                            fontSize = 11.sp,
                                            fontWeight = FontWeight.Bold,
                                            color = Color(0xFF10B981)
                                        )
                                    }
                                }
                            } else {
                                Icon(
                                    Icons.Default.ArrowForward,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.size(16.dp)
                                )
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(4.dp))

                Button(
                    onClick = {
                        when (ex) {
                            ExerciseType.EJ5 -> onStartEJ5Practice(selectedEJ5Art, selectedEJ5Section)
                            ExerciseType.EJ10 -> onStartEJ10Practice(selectedEJ10Art, selectedEJ10Section)
                            ExerciseType.EJ11 -> onStartEJ11Practice(selectedEJ11Art, selectedEJ11Section)
                            ExerciseType.R1 -> onStartReichertPractice(ex, selectedR1Art, selectedR1Section)
                            ExerciseType.R5 -> onStartReichertPractice(ex, selectedR5Art, selectedR5Section)
                            else -> {}
                        }
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp),
                    shape = RoundedCornerShape(18.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    val startLabel = when (ex) {
                        ExerciseType.EJ5 -> "${loc.t("ej5_start_practice")} (${selectedEJ5Section.shortBadge} · ${selectedEJ5Art.shortTitle(loc, ex)})"
                        ExerciseType.EJ10 -> "${loc.t("ej10_start_practice")} (${selectedEJ10Section.shortBadge} · ${selectedEJ10Art.shortTitle(loc, ex)})"
                        ExerciseType.EJ11 -> "${loc.t("ej11_start_practice")} (${selectedEJ11Section.shortBadge} · ${selectedEJ11Art.shortTitle(loc, ex)})"
                        ExerciseType.R1 -> "${loc.t("r1_start_practice")} (${selectedR1Section.shortBadge(ex)} · ${selectedR1Art.shortTitle(loc, ex)})"
                        ExerciseType.R5 -> "${loc.t("r5_start_practice")} (${selectedR5Section.shortBadge(ex)} · ${selectedR5Art.shortTitle(loc, ex)})"
                        else -> ""
                    }
                    Text(
                        text = startLabel,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1
                    )
                }
            } else {
                // 3-Level Modes Explorer: Nivel 1 · Tónica Cromática (12)
                Column {
                    Text(
                        text = CoachStrings.level1TonicHeader(loc),
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.padding(horizontal = 4.dp)
                    )
                    Text(
                        text = loc.t("select_tonic"),
                        fontSize = 16.sp,
                        fontWeight = FontWeight.SemiBold,
                        modifier = Modifier.padding(horizontal = 4.dp, vertical = 4.dp)
                    )

                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .horizontalScroll(rememberScrollState()),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Tonic.entries.forEach { tonic ->
                            val isSelected = tonic == selectedTonic
                            val completedInTonic = store.practicedModesCount(tonic)

                            Surface(
                                onClick = {
                                    selectedTonic = tonic
                                    store.lastTonic = tonic
                                    store.saveLastSelection()
                                },
                                shape = RoundedCornerShape(14.dp),
                                color = if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                                tonalElevation = if (isSelected) 4.dp else 0.dp,
                                modifier = Modifier.padding(vertical = 4.dp)
                            ) {
                                Column(
                                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                                    horizontalAlignment = Alignment.CenterHorizontally
                                ) {
                                    Text(
                                        text = tonic.displayName,
                                        fontSize = 16.sp,
                                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                                        color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                    Text(
                                        text = "$completedInTonic/7 ${loc.t("modes_count")}",
                                        fontSize = 10.sp,
                                        color = if (isSelected) MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.8f) else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                                    )
                                }
                            }
                        }
                    }
                }

                // Nivel 2 · Modo Paralelo (7)
                Text(
                    text = CoachStrings.level2ModeHeader(loc),
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.padding(horizontal = 4.dp)
                )

                Text(
                    text = "${selectedTonic.displayName} · ${loc.t("major_family")}",
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary
                )

                majorModes.forEach { mode ->
                    ModeSelectionCard(
                        tonic = selectedTonic,
                        mode = mode,
                        isSelected = (mode == selectedMode),
                        loc = loc,
                        store = store,
                        onClick = {
                            selectedMode = mode
                            store.lastMode = mode
                            store.saveLastSelection()
                        }
                    )
                }

                Spacer(modifier = Modifier.height(4.dp))

                Text(
                    text = "${selectedTonic.displayName} · ${loc.t("minor_family")}",
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.secondary
                )

                minorModes.forEach { mode ->
                    ModeSelectionCard(
                        tonic = selectedTonic,
                        mode = mode,
                        isSelected = (mode == selectedMode),
                        loc = loc,
                        store = store,
                        onClick = {
                            selectedMode = mode
                            store.lastMode = mode
                            store.saveLastSelection()
                        }
                    )
                }

                Spacer(modifier = Modifier.height(6.dp))

                // Nivel 3 · Esquema Técnico (10 · 840 Variaciones)
                ModalSchemesSelectorCard(
                    loc = loc,
                    selectedTonic = selectedTonic,
                    selectedMode = selectedMode,
                    selectedModalScheme = selectedModalScheme,
                    onSelectScheme = { scheme ->
                        selectedModalScheme = scheme
                        store.lastModalScheme = scheme
                        store.saveLastSelection()
                    }
                )

                Spacer(modifier = Modifier.height(8.dp))

                // Start Practice Button
                Button(
                    onClick = {
                        store.lastModalScheme = selectedModalScheme
                        store.saveLastSelection()
                        onStartPractice(selectedTonic, selectedMode)
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp),
                    shape = RoundedCornerShape(18.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (selectedModalScheme.isReichert) Color(0xFF6366F1) else MaterialTheme.colorScheme.primary
                    )
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "${loc.t("start_practice")} (${selectedTonic.displayName} ${selectedMode.getName(loc)} · ${selectedModalScheme.shortName})",
                        fontSize = 15.sp,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1
                    )
                }

                // Matrix Button
                OutlinedButton(
                    onClick = onOpenMatrix,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(50.dp),
                    shape = RoundedCornerShape(18.dp)
                ) {
                    Icon(Icons.Default.GridView, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = loc.t("practice_matrix"),
                        fontSize = 14.sp,
                        fontWeight = FontWeight.SemiBold
                    )
                }
            }

            Spacer(modifier = Modifier.height(4.dp))

            // Practice Settings Card
            Card(
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)),
                shape = RoundedCornerShape(18.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = loc.t("settings_title"),
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Spacer(modifier = Modifier.height(10.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(
                            modifier = Modifier.weight(1f),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.Info,
                                contentDescription = null,
                                tint = if (store.keepScreenAwake) Color(0xFFF59E0B) else MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Column {
                                Text(
                                    text = loc.t("keep_screen_awake"),
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                Text(
                                    text = loc.t("keep_screen_awake_desc"),
                                    fontSize = 11.sp,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }

                        Switch(
                            checked = store.keepScreenAwake,
                            onCheckedChange = { store.setKeepScreenAwakeState(it) }
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))
        }

        if (showPracticeWizard) {
            PracticeWizardDialog(
                loc = loc,
                duration = wizardDuration,
                focus = wizardFocus,
                tonic = wizardTonic,
                mode = wizardMode,
                onSelectDuration = { wizardDuration = it },
                onSelectFocus = { wizardFocus = it },
                onSelectTonic = { wizardTonic = it },
                onSelectMode = { wizardMode = it },
                onLaunchBlock = { launchRoutineBlock(it) },
                onDismiss = { showPracticeWizard = false }
            )
        }
    }
}

@Composable
fun ConservatoryCoachHeroCard(
    loc: LocalizationManager,
    selectedExercise: ExerciseType,
    selectedTonic: Tonic,
    selectedMode: ModeType,
    selectedModalScheme: ModalScheme,
    wizardDuration: PracticeWizardDuration,
    onSelectDurationPreset: (PracticeWizardDuration) -> Unit,
    onResumeLastSession: () -> Unit,
    onOpenWizard: () -> Unit
) {
    val resumeLabel = when (selectedExercise) {
        ExerciseType.MODOS -> "${selectedTonic.displayName} ${selectedMode.getName(loc)} · ${selectedModalScheme.shortName}"
        else -> selectedExercise.displayTitle(loc)
    }

    Card(
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.65f)
        ),
        border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.25f)),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Surface(
                    shape = RoundedCornerShape(6.dp),
                    color = MaterialTheme.colorScheme.primary.copy(alpha = 0.14f),
                    modifier = Modifier.weight(1f, fill = false)
                ) {
                    Text(
                        text = "✨ ${CoachStrings.coachBadge(loc)}",
                        fontSize = 8.5.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = MaterialTheme.colorScheme.primary,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.padding(horizontal = 7.dp, vertical = 3.dp)
                    )
                }

                Spacer(modifier = Modifier.width(6.dp))

                TextButton(
                    onClick = onOpenWizard,
                    contentPadding = PaddingValues(horizontal = 6.dp, vertical = 2.dp)
                ) {
                    Text(
                        text = CoachStrings.openWizardButton(loc),
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1
                    )
                }
            }

            Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
                Text(
                    text = CoachStrings.coachHeroTitle(loc),
                    fontSize = 17.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Text(
                    text = CoachStrings.coachHeroSubtitle(loc),
                    fontSize = 11.5.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            // 1-Tap Resume Banner
            Surface(
                onClick = onResumeLastSession,
                shape = RoundedCornerShape(12.dp),
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = CoachStrings.resumeLastSession(loc),
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.85f)
                        )
                        Text(
                            text = resumeLabel,
                            fontSize = 13.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = MaterialTheme.colorScheme.onPrimary,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                    Icon(
                        imageVector = Icons.Default.PlayArrow,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onPrimary
                    )
                }
            }

            // 3 Quick Duration Preset Cards (15m Express, 30m Conservatorio, 45m Maestría)
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                PracticeWizardDuration.entries.forEach { dur ->
                    val isSel = wizardDuration == dur
                    Surface(
                        onClick = { onSelectDurationPreset(dur) },
                        shape = RoundedCornerShape(10.dp),
                        color = if (isSel) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surface,
                        border = androidx.compose.foundation.BorderStroke(
                            1.dp,
                            if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant
                        ),
                        modifier = Modifier.weight(1f)
                    ) {
                        Column(
                            modifier = Modifier.padding(horizontal = 6.dp, vertical = 7.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                text = dur.title(loc),
                                fontSize = 9.5.sp,
                                fontWeight = FontWeight.Bold,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            Text(
                                text = dur.subtitle(loc),
                                fontSize = 8.sp,
                                maxLines = 2,
                                overflow = TextOverflow.Ellipsis,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ModalSchemesSelectorCard(
    loc: LocalizationManager,
    selectedTonic: Tonic,
    selectedMode: ModeType,
    selectedModalScheme: ModalScheme,
    onSelectScheme: (ModalScheme) -> Unit
) {
    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.45f)
        ),
        border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Text(
                text = CoachStrings.level3SchemeHeader(loc),
                fontSize = 11.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
            Text(
                text = CoachStrings.level3SchemeSubtitle(loc),
                fontSize = 11.5.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            // Group A: Taffanel & Gaubert (6 schemes in 2 rows of 3)
            Text(
                text = "TAFFANEL & GAUBERT",
                fontSize = 10.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            val tgRows = listOf(
                listOf(ModalScheme.EJ1, ModalScheme.EJ2, ModalScheme.EJ4),
                listOf(ModalScheme.EJ5, ModalScheme.EJ10, ModalScheme.EJ11)
            )
            tgRows.forEach { rowSchemes ->
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    rowSchemes.forEach { scheme ->
                        val isSel = selectedModalScheme == scheme
                        Surface(
                            onClick = { onSelectScheme(scheme) },
                            shape = RoundedCornerShape(10.dp),
                            color = if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surface,
                            border = if (!isSel) androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant) else null,
                            modifier = Modifier.weight(1f)
                        ) {
                            Column(
                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 8.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                Text(
                                    text = scheme.shortName,
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface
                                )
                                Text(
                                    text = "${scheme.subtitle(loc)} · ${scheme.meter}",
                                    fontSize = 9.sp,
                                    maxLines = 1,
                                    color = if (isSel) MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.85f) else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }
            }

            // Group B: M.-A. Reichert Op. 5 (4 schemes in 2 rows of 2)
            Text(
                text = "M.-A. REICHERT · OP. 5",
                fontSize = 10.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF6366F1)
            )
            val reichertRows = listOf(
                listOf(ModalScheme.R1, ModalScheme.R2),
                listOf(ModalScheme.R4, ModalScheme.R5)
            )
            reichertRows.forEach { rowSchemes ->
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    rowSchemes.forEach { scheme ->
                        val isSel = selectedModalScheme == scheme
                        Surface(
                            onClick = { onSelectScheme(scheme) },
                            shape = RoundedCornerShape(10.dp),
                            color = if (isSel) Color(0xFF6366F1) else MaterialTheme.colorScheme.surface,
                            border = if (!isSel) androidx.compose.foundation.BorderStroke(1.dp, Color(0xFF6366F1).copy(alpha = 0.35f)) else null,
                            modifier = Modifier.weight(1f)
                        ) {
                            Column(
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 8.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                Text(
                                    text = scheme.shortName,
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (isSel) Color.White else MaterialTheme.colorScheme.onSurface
                                )
                                Text(
                                    text = "${scheme.subtitle(loc)} · ${scheme.meter}",
                                    fontSize = 9.5.sp,
                                    maxLines = 1,
                                    color = if (isSel) Color.White.copy(alpha = 0.9f) else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }
            }

            // Active Scheme Detail Banner
            Surface(
                shape = RoundedCornerShape(12.dp),
                color = MaterialTheme.colorScheme.surface,
                border = androidx.compose.foundation.BorderStroke(
                    1.dp,
                    if (selectedModalScheme.isReichert) Color(0xFF6366F1).copy(alpha = 0.45f) else MaterialTheme.colorScheme.primary.copy(alpha = 0.35f)
                ),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(
                    modifier = Modifier.padding(12.dp),
                    verticalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "${selectedTonic.displayName} ${selectedMode.getName(loc)} · ${selectedModalScheme.title(loc)}",
                            fontSize = 12.5.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface,
                            modifier = Modifier.weight(1f)
                        )
                        Surface(
                            shape = RoundedCornerShape(6.dp),
                            color = if (selectedModalScheme.isReichert) Color(0xFF6366F1).copy(alpha = 0.15f) else MaterialTheme.colorScheme.primaryContainer
                        ) {
                            Text(
                                text = "${selectedModalScheme.meter} · ${selectedModalScheme.totalNotes} n.",
                                fontSize = 10.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (selectedModalScheme.isReichert) Color(0xFF6366F1) else MaterialTheme.colorScheme.onPrimaryContainer,
                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                            )
                        }
                    }
                    Text(
                        text = selectedModalScheme.pedagogy(loc),
                        fontSize = 11.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}

@Composable
fun PracticeWizardDialog(
    loc: LocalizationManager,
    duration: PracticeWizardDuration,
    focus: PracticeWizardFocus,
    tonic: Tonic,
    mode: ModeType,
    onSelectDuration: (PracticeWizardDuration) -> Unit,
    onSelectFocus: (PracticeWizardFocus) -> Unit,
    onSelectTonic: (Tonic) -> Unit,
    onSelectMode: (ModeType) -> Unit,
    onLaunchBlock: (PracticeRoutineBlock) -> Unit,
    onDismiss: () -> Unit
) {
    val blocks = remember(duration, focus, tonic, mode, loc.currentLanguage) {
        PracticeRoutineBlock.generateRoutine(duration, focus, tonic, mode, loc)
    }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = {
            Text(
                text = CoachStrings.wizardTitle(loc),
                fontSize = 17.sp,
                fontWeight = FontWeight.Bold
            )
        },
        text = {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .verticalScroll(rememberScrollState()),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                // Step 1: Duration
                Text(
                    text = CoachStrings.step1Title(loc),
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary
                )
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    PracticeWizardDuration.entries.forEach { dur ->
                        val isSel = duration == dur
                        Surface(
                            onClick = { onSelectDuration(dur) },
                            shape = RoundedCornerShape(10.dp),
                            color = if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                            modifier = Modifier.weight(1f)
                        ) {
                            Column(
                                modifier = Modifier.padding(6.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                Text(
                                    text = "${dur.minutes} min",
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface
                                )
                            }
                        }
                    }
                }

                // Step 2: Focus
                Text(
                    text = CoachStrings.step2Title(loc),
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary
                )
                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    PracticeWizardFocus.entries.forEach { item ->
                        val isSel = focus == item
                        Surface(
                            onClick = { onSelectFocus(item) },
                            shape = RoundedCornerShape(10.dp),
                            color = if (isSel) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.6f),
                            border = if (isSel) androidx.compose.foundation.BorderStroke(1.5.dp, MaterialTheme.colorScheme.primary) else null,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 8.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                Text(text = item.icon, fontSize = 16.sp)
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(
                                        text = item.title(loc),
                                        fontSize = 12.5.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = MaterialTheme.colorScheme.onSurface
                                    )
                                    Text(
                                        text = item.subtitle(loc),
                                        fontSize = 10.5.sp,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                            }
                        }
                    }
                }

                // Step 3: Tonic, Mode & Generated Routine
                Text(
                    text = CoachStrings.step3Title(loc),
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary
                )
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    Tonic.entries.forEach { t ->
                        val isSel = tonic == t
                        Surface(
                            onClick = { onSelectTonic(t) },
                            shape = RoundedCornerShape(8.dp),
                            color = if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant
                        ) {
                            Text(
                                text = t.displayName,
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface,
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp)
                            )
                        }
                    }
                }
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    ModeType.entries.forEach { m ->
                        val isSel = mode == m
                        Surface(
                            onClick = { onSelectMode(m) },
                            shape = RoundedCornerShape(8.dp),
                            color = if (isSel) MaterialTheme.colorScheme.secondary else MaterialTheme.colorScheme.surfaceVariant
                        ) {
                            Text(
                                text = m.getName(loc),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (isSel) MaterialTheme.colorScheme.onSecondary else MaterialTheme.colorScheme.onSurface,
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp)
                            )
                        }
                    }
                }

                blocks.forEach { block ->
                    Surface(
                        onClick = { onLaunchBlock(block) },
                        shape = RoundedCornerShape(12.dp),
                        color = MaterialTheme.colorScheme.surface,
                        border = androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(
                            modifier = Modifier.padding(10.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = "${block.title} (${block.minutes} min)",
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                Text(
                                    text = block.detail,
                                    fontSize = 10.5.sp,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                            Surface(
                                shape = RoundedCornerShape(8.dp),
                                color = MaterialTheme.colorScheme.primary
                            ) {
                                Text(
                                    text = CoachStrings.startBlockButton(loc),
                                    fontSize = 10.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.onPrimary,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 5.dp)
                                )
                            }
                        }
                    }
                }
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    blocks.firstOrNull()?.let { onLaunchBlock(it) }
                }
            ) {
                Text(CoachStrings.startBlockButton(loc))
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("✕")
            }
        }
    )
}

@Composable
fun ModeSelectionCard(
    tonic: Tonic,
    mode: ModeType,
    isSelected: Boolean,
    loc: LocalizationManager,
    store: PracticeStore,
    onClick: () -> Unit
) {
    val completedCount = store.completedArticulationsCount(tonic, mode)

    Surface(
        onClick = onClick,
        shape = RoundedCornerShape(14.dp),
        color = if (isSelected) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surface,
        border = if (isSelected) androidx.compose.foundation.BorderStroke(2.dp, MaterialTheme.colorScheme.primary) else androidx.compose.foundation.BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .padding(14.dp)
                .fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(
                        text = "Modo ${mode.id}: ${mode.getName(loc)}",
                        fontSize = 15.sp,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Surface(
                        shape = RoundedCornerShape(6.dp),
                        color = MaterialTheme.colorScheme.surfaceVariant
                    ) {
                        Text(
                            text = mode.formula,
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Medium,
                            modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                        )
                    }
                }

                Spacer(modifier = Modifier.height(3.dp))

                Text(
                    text = "${mode.keyDescription(tonic)} | ${mode.accidentalBadge(loc)}",
                    fontSize = 11.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            Surface(
                shape = RoundedCornerShape(8.dp),
                color = if (completedCount == 8) Color(0xFF10B981).copy(alpha = 0.2f) else if (completedCount > 0) MaterialTheme.colorScheme.primary.copy(alpha = 0.15f) else MaterialTheme.colorScheme.surfaceVariant
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    if (completedCount == 8) {
                        Icon(
                            Icons.Default.CheckCircle,
                            contentDescription = null,
                            tint = Color(0xFF10B981),
                            modifier = Modifier.size(12.dp)
                        )
                    }
                    Text(
                        text = "$completedCount/8 ${loc.t("arts_count")}",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        color = if (completedCount == 8) Color(0xFF10B981) else if (completedCount > 0) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}
