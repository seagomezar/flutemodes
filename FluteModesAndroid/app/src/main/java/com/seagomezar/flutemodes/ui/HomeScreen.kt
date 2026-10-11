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

    val majorModes = listOf(ModeType.IONIAN, ModeType.LYDIAN, ModeType.MIXOLYDIAN)
    val minorModes = listOf(ModeType.DORIAN, ModeType.AEOLIAN, ModeType.PHRYGIAN, ModeType.LOCRIAN)

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
                    Column {
                        Text(
                            text = loc.t("app_name"),
                            fontSize = 24.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary
                        )
                        Text(
                            text = if (selectedExercise.isReichertExercise) "M.-A. Reichert · Op. 5 (Schott 20623)" else if (selectedExercise.isChromaticExercise || selectedExercise.isEJ4Exercise || selectedExercise.isEJ5TypeExercise) "Taffanel & Gaubert · A. L. 16.588" else "Maestro León Giraldo",
                            fontSize = 12.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
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
            // Exercise Switcher
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                ExerciseType.entries.forEach { ex ->
                    val isSel = selectedExercise == ex
                    Surface(
                        onClick = {
                            selectedExercise = ex
                            store.lastExerciseType = ex
                            store.saveLastSelection()
                        },
                        shape = RoundedCornerShape(14.dp),
                        color = if (isSel) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                        tonalElevation = if (isSel) 4.dp else 0.dp
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 11.dp),
                            horizontalArrangement = Arrangement.Center,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                imageVector = if (ex.isChromaticExercise || ex.isEJ4Exercise || ex.isEJ5TypeExercise) Icons.Default.MusicNote else Icons.Default.GridView,
                                contentDescription = null,
                                modifier = Modifier.size(14.dp),
                                tint = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Text(
                                text = ex.pillLabel,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold,
                                maxLines = 1,
                                color = if (isSel) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
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
                            ExerciseType.MODOS -> loc.t("subtitle")
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
                                        text = "Urtext",
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
                                    text = if (art == EJ4Articulation.ORIGINAL && ex.isReichertExercise) "Schott 20623" else art.formulaBadge,
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
                                        text = "Urtext",
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
                                        text = "Urtext",
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
                // Tonic Picker
                Column {
                    Text(
                        text = loc.t("select_tonic"),
                        fontSize = 16.sp,
                        fontWeight = FontWeight.SemiBold,
                        modifier = Modifier.padding(horizontal = 4.dp, vertical = 6.dp)
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
                                onClick = { selectedTonic = tonic },
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

                // Parallel System Cards (Major & Minor Families)
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
                        onClick = { selectedMode = mode }
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
                        onClick = { selectedMode = mode }
                    )
                }

                Spacer(modifier = Modifier.height(8.dp))

                // Start Practice Button
                Button(
                    onClick = { onStartPractice(selectedTonic, selectedMode) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp),
                    shape = RoundedCornerShape(18.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "${loc.t("start_practice")} (${selectedTonic.displayName} ${selectedMode.getName(loc)})",
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold
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
    }
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
