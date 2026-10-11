package com.seagomezar.flutemodes.audio

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import com.seagomezar.flutemodes.model.ArticulationPattern
import com.seagomezar.flutemodes.model.EJ10Section
import com.seagomezar.flutemodes.model.EJ1Articulation
import com.seagomezar.flutemodes.model.EJ4Articulation
import com.seagomezar.flutemodes.model.EJ4Section
import com.seagomezar.flutemodes.model.EJ5Articulation
import com.seagomezar.flutemodes.model.EJ5Section
import com.seagomezar.flutemodes.model.ExerciseGenerator
import com.seagomezar.flutemodes.model.ExerciseType
import com.seagomezar.flutemodes.model.ModeType
import com.seagomezar.flutemodes.model.Tonic
import kotlinx.coroutines.*
import kotlin.math.*

class ScoreAudioPlayer {
    var isPlaying by mutableStateOf(false)
        private set

    var currentNoteIndex by mutableStateOf<Int?>(null)
        private set

    private var lastNoteDurations: List<Double> = emptyList()

    private var playbackJob: Job? = null
    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    private var currentTrack: AudioTrack? = null

    private val sampleRate = 44100

    fun toggle(tonic: Tonic, mode: ModeType, articulation: ArticulationPattern, tempoBPM: Int) {
        if (isPlaying) {
            stop()
        } else {
            play(tonic, mode, articulation, tempoBPM)
        }
    }

    fun toggleEJ1(articulation: EJ1Articulation, tempoBPM: Int) {
        if (isPlaying) {
            stop()
        } else {
            playEJ1(articulation, tempoBPM)
        }
    }

    fun toggleEJ2(articulation: EJ1Articulation, tempoBPM: Int) {
        if (isPlaying) {
            stop()
        } else {
            playEJ2(articulation, tempoBPM)
        }
    }

    fun toggleEJ4(exercise: ExerciseType = ExerciseType.EJ4, articulation: EJ4Articulation, section: EJ4Section, tempoBPM: Int) {
        if (isPlaying) {
            stop()
        } else {
            playEJ4(exercise, articulation, section, tempoBPM)
        }
    }

    fun toggleEJ5Type(exercise: ExerciseType, articulation: EJ5Articulation, sectionIndex: Int, tempoBPM: Int) {
        if (isPlaying) {
            stop()
        } else {
            playEJ5Type(exercise, articulation, sectionIndex, tempoBPM)
        }
    }

    fun toggleEJ5(articulation: EJ5Articulation, section: EJ5Section, tempoBPM: Int) {
        toggleEJ5Type(ExerciseType.EJ5, articulation, section.id, tempoBPM)
    }

    fun toggleEJ10(articulation: EJ5Articulation, section: EJ10Section, tempoBPM: Int) {
        toggleEJ5Type(ExerciseType.EJ10, articulation, section.id, tempoBPM)
    }

    fun toggleEJ11(articulation: EJ5Articulation, section: EJ10Section, tempoBPM: Int) {
        toggleEJ5Type(ExerciseType.EJ11, articulation, section.id, tempoBPM)
    }

    fun stop() {
        playbackJob?.cancel()
        playbackJob = null
        try {
            currentTrack?.let {
                if (it.playState == AudioTrack.PLAYSTATE_PLAYING) {
                    it.stop()
                }
                it.release()
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        currentTrack = null
        currentNoteIndex = null
        isPlaying = false
    }

    fun play(tonic: Tonic, mode: ModeType, articulation: ArticulationPattern, tempoBPM: Int) {
        stop()
        isPlaying = true

        playbackJob = scope.launch {
            val buffer = generateScoreBuffer(tonic, mode, articulation, tempoBPM)
            playPcmBuffer(buffer)
        }
    }

    fun playEJ1(articulation: EJ1Articulation, tempoBPM: Int) {
        stop()
        isPlaying = true

        playbackJob = scope.launch {
            val buffer = generateEJ1ScoreBuffer(articulation, tempoBPM)
            playPcmBuffer(buffer)
        }
    }

    fun playEJ2(articulation: EJ1Articulation, tempoBPM: Int) {
        stop()
        isPlaying = true

        playbackJob = scope.launch {
            val buffer = generateEJ2ScoreBuffer(articulation, tempoBPM)
            playPcmBuffer(buffer)
        }
    }

    fun playEJ4(exercise: ExerciseType = ExerciseType.EJ4, articulation: EJ4Articulation, section: EJ4Section, tempoBPM: Int) {
        stop()
        isPlaying = true

        playbackJob = scope.launch {
            val buffer = generateEJ4ScoreBuffer(exercise, articulation, section, tempoBPM)
            playPcmBuffer(buffer)
        }
    }

    fun playEJ5Type(exercise: ExerciseType, articulation: EJ5Articulation, sectionIndex: Int, tempoBPM: Int) {
        stop()
        isPlaying = true

        playbackJob = scope.launch {
            val buffer = generateEJ5TypeScoreBuffer(exercise, articulation, sectionIndex, tempoBPM)
            playPcmBuffer(buffer)
        }
    }

    fun playEJ5(articulation: EJ5Articulation, section: EJ5Section, tempoBPM: Int) {
        playEJ5Type(ExerciseType.EJ5, articulation, section.id, tempoBPM)
    }

    fun playEJ10(articulation: EJ5Articulation, section: EJ10Section, tempoBPM: Int) {
        playEJ5Type(ExerciseType.EJ10, articulation, section.id, tempoBPM)
    }

    fun playEJ11(articulation: EJ5Articulation, section: EJ10Section, tempoBPM: Int) {
        playEJ5Type(ExerciseType.EJ11, articulation, section.id, tempoBPM)
    }

    private suspend fun CoroutineScope.playPcmBuffer(buffer: ShortArray) {
        if (!isActive || buffer.isEmpty()) {
            withContext(Dispatchers.Main) {
                isPlaying = false
                currentNoteIndex = null
            }
            return
        }

        val durations = lastNoteDurations
        var highlightJob: Job? = null
        try {
            val attributes = AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_MEDIA)
                .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                .build()

            val format = AudioFormat.Builder()
                .setSampleRate(sampleRate)
                .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                .build()

            val minBufferSize = AudioTrack.getMinBufferSize(
                sampleRate,
                AudioFormat.CHANNEL_OUT_MONO,
                AudioFormat.ENCODING_PCM_16BIT
            )
            val bufferSize = max(minBufferSize, buffer.size * 2)

            val track = AudioTrack(
                attributes,
                format,
                bufferSize,
                AudioTrack.MODE_STATIC,
                android.media.AudioManager.AUDIO_SESSION_ID_GENERATE
            )
            currentTrack = track

            track.write(buffer, 0, buffer.size)
            track.play()

            highlightJob = launch(Dispatchers.Main) {
                for ((index, dur) in durations.withIndex()) {
                    if (!isActive) break
                    currentNoteIndex = index
                    delay((dur * 1000.0).toLong())
                }
                currentNoteIndex = null
            }

            val durationMs = (buffer.size.toDouble() / sampleRate * 1000.0).toLong()
            delay(durationMs)
        } catch (e: Exception) {
            e.printStackTrace()
        } finally {
            highlightJob?.cancel()
            withContext(Dispatchers.Main) {
                currentNoteIndex = null
                isPlaying = false
            }
        }
    }

    private data class NoteDef(val freq: Double, val duration: Double, val isStaccato: Boolean)

    internal fun generateScoreBuffer(
        tonic: Tonic,
        mode: ModeType,
        articulation: ArticulationPattern,
        tempoBPM: Int
    ): ShortArray {
        val rootMidi = tonic.rootMidi
        val intervals = mode.intervals

        fun freqForIndex(idx: Int): Double {
            val octave = idx / 7
            val degree = idx % 7
            val semitones = intervals[degree] + (octave * 12)
            val midi = (rootMidi + semitones).toDouble()
            return midiToFrequency(midi)
        }

        val eighthDuration = (60.0 / tempoBPM.toDouble()) / 4.0
        val halfDuration = eighthDuration * 4.0

        fun isStaccatoAt(beatSubIndex: Int): Boolean {
            val i = beatSubIndex % 4
            return when (articulation) {
                ArticulationPattern.ALL_SLURRED, ArticulationPattern.SLURRED_FOUR_AND_FOUR -> false
                ArticulationPattern.SLUR_TWO_STACCATO_TWO -> (i >= 2)
                ArticulationPattern.STACCATO_SLUR_TWO_STACCATO -> (i == 0 || i == 3)
                ArticulationPattern.STACCATO_TWO_SLUR_TWO -> (i < 2)
                ArticulationPattern.STACCATO_ONE_SLUR_THREE -> (i == 0)
                ArticulationPattern.SLUR_THREE_STACCATO_ONE -> (i == 3)
                ArticulationPattern.ALL_STACCATO -> true
            }
        }

        val notes = mutableListOf<NoteDef>()
        fun addNotes(indices: List<Int>) {
            indices.forEachIndexed { subIdx, idx ->
                notes.add(
                    NoteDef(
                        freq = freqForIndex(idx),
                        duration = eighthDuration,
                        isStaccato = isStaccatoAt(subIdx)
                    )
                )
            }
        }

        // Measure 1
        addNotes(listOf(0, 1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2, 1))
        // Measure 2
        addNotes(listOf(2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3))
        // Measure 3
        addNotes(listOf(4, 5, 6, 7, 8, 9, 10, 11, 12, 11, 10, 9, 8, 7, 6, 5))
        // Measure 4 (Peak)
        addNotes(listOf(6, 7, 8, 9, 10, 11, 12, 13, 14, 13, 12, 11, 10, 9, 8, 7))
        // Measure 5
        addNotes(listOf(6, 7, 8, 9, 10, 11, 12, 13, 12, 11, 10, 9, 8, 7, 6, 5))
        // Measure 6
        addNotes(listOf(4, 5, 6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6, 5, 4, 3))
        // Measure 7
        addNotes(listOf(2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1))
        // Measure 8
        addNotes(listOf(0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1))
        // Final tonic half note
        notes.add(NoteDef(freq = freqForIndex(0), duration = halfDuration, isStaccato = false))

        return renderNotesToPcm(notes)
    }

    internal fun generateEJ1ScoreBuffer(
        articulation: EJ1Articulation,
        tempoBPM: Int
    ): ShortArray {
        return generateChromaticPentachordBuffer(isMinor = false, articulation = articulation, tempoBPM = tempoBPM)
    }

    internal fun generateEJ2ScoreBuffer(
        articulation: EJ1Articulation,
        tempoBPM: Int
    ): ShortArray {
        return generateChromaticPentachordBuffer(isMinor = true, articulation = articulation, tempoBPM = tempoBPM)
    }

    internal fun generateEJ5TypeScoreBuffer(
        exercise: ExerciseType,
        articulation: EJ5Articulation,
        sectionIndex: Int,
        tempoBPM: Int
    ): ShortArray {
        val sixteenthDuration = when (exercise) {
            ExerciseType.R5 -> (60.0 / tempoBPM.toDouble()) / 6.0
            else -> (60.0 / tempoBPM.toDouble()) / 4.0
        }
        val finalDuration = sixteenthDuration * 6.0

        fun isStaccatoAt(subIndex: Int): Boolean {
            val i = subIndex % 6
            return when (articulation) {
                EJ5Articulation.ORIGINAL,
                EJ5Articulation.ALL_SLURRED,
                EJ5Articulation.SLURRED_6_BY_6,
                EJ5Articulation.SLURRED_3_BY_3,
                EJ5Articulation.SLUR_PAIRS_2_BY_2 -> false
                EJ5Articulation.SLUR_4_STACC_2 -> (i == 4 || i == 5)
                EJ5Articulation.STACC_2_SLUR_4 -> (i == 0 || i == 1)
                EJ5Articulation.SLUR_2_STACC_4 -> (i >= 2)
                EJ5Articulation.SLUR_3_STACC_3 -> (i >= 3)
                EJ5Articulation.SLUR_SYNCOPATED -> (i == 0 || i == 5)
                EJ5Articulation.ALL_STACCATO -> true
            }
        }

        val allSections = when (exercise) {
            ExerciseType.EJ5 -> ExerciseGenerator.ej5SectionMidiNotes
            ExerciseType.EJ10 -> ExerciseGenerator.ej10SectionMidiNotes
            ExerciseType.EJ11 -> ExerciseGenerator.ej11SectionMidiNotes
            ExerciseType.R1 -> ExerciseGenerator.r1SectionMidiNotes
            ExerciseType.R5 -> ExerciseGenerator.r5SectionMidiNotes
            else -> ExerciseGenerator.ej5SectionMidiNotes
        }
        val secIdx = sectionIndex.coerceIn(0, allSections.size - 1)
        val midiNotes = allSections[secIdx]
        val notes = mutableListOf<NoteDef>()
        for ((idx, m) in midiNotes.withIndex()) {
            val isLast = (idx == midiNotes.size - 1)
            if (isLast && (exercise == ExerciseType.R1 || exercise == ExerciseType.R5)) {
                notes.add(
                    NoteDef(
                        freq = midiToFrequency(m.toDouble()),
                        duration = sixteenthDuration * 2.0,
                        isStaccato = true
                    )
                )
            } else {
                val isLongFinal = isLast && (exercise == ExerciseType.EJ5 || (!exercise.isReichertExercise && secIdx == 11))
                notes.add(
                    NoteDef(
                        freq = midiToFrequency(m.toDouble()),
                        duration = if (isLongFinal) finalDuration else sixteenthDuration,
                        isStaccato = if (isLongFinal) false else isStaccatoAt(idx)
                    )
                )
            }
        }
        return renderNotesToPcm(notes)
    }

    internal fun generateEJ4ScoreBuffer(
        exercise: ExerciseType = ExerciseType.EJ4,
        articulation: EJ4Articulation,
        section: EJ4Section,
        tempoBPM: Int
    ): ShortArray {
        val eighthDuration = (60.0 / tempoBPM.toDouble()) / 4.0
        val finalDuration = eighthDuration * 4.0

        fun isStaccatoAt(subIndex: Int): Boolean {
            val i = subIndex % 8
            return when (articulation) {
                EJ4Articulation.ORIGINAL,
                EJ4Articulation.ALL_SLURRED_8,
                EJ4Articulation.SLURRED_4_AND_4,
                EJ4Articulation.SLUR_PAIRS_2_BY_2 -> false
                EJ4Articulation.STACC_1_SLUR_3 -> (i == 0 || i == 4)
                EJ4Articulation.SLUR_2_STACC_2 -> (i == 2 || i == 3 || i == 6 || i == 7)
                EJ4Articulation.STACC_2_SLUR_2 -> (i == 0 || i == 1 || i == 4 || i == 5)
                EJ4Articulation.STACC_1_SLUR_2_STACC_1 -> (i == 0 || i == 3 || i == 4 || i == 7)
                EJ4Articulation.SLUR_SYNCOPATED -> (i == 0 || i == 7)
            }
        }

        val allSections = when (exercise) {
            ExerciseType.R2 -> ExerciseGenerator.r2SectionMidiNotes
            ExerciseType.R4 -> ExerciseGenerator.r4SectionMidiNotes
            else -> ExerciseGenerator.ej4SectionMidiNotes
        }
        val secIdx = section.id.coerceIn(0, allSections.size - 1)
        val midiNotes = allSections[secIdx]
        val isCoda = (section == EJ4Section.C_CODA)

        val notes = mutableListOf<NoteDef>()
        for ((idx, m) in midiNotes.withIndex()) {
            val isLast = (idx == midiNotes.size - 1)
            if (isLast && (exercise == ExerciseType.R2 || exercise == ExerciseType.R4)) {
                notes.add(
                    NoteDef(
                        freq = midiToFrequency(m.toDouble()),
                        duration = eighthDuration * 2.0,
                        isStaccato = true
                    )
                )
            } else {
                val isLastInCoda = isCoda && isLast
                val subIdx = if (exercise == ExerciseType.R2) {
                    if (idx >= 4) (idx - 4) else (idx + 4)
                } else idx
                notes.add(
                    NoteDef(
                        freq = midiToFrequency(m.toDouble()),
                        duration = if (isLastInCoda) finalDuration else eighthDuration,
                        isStaccato = if (isLastInCoda) false else isStaccatoAt(subIdx)
                    )
                )
            }
        }
        return renderNotesToPcm(notes)
    }

    private fun generateChromaticPentachordBuffer(
        isMinor: Boolean,
        articulation: EJ1Articulation,
        tempoBPM: Int
    ): ShortArray {
        val sixteenthDuration = (60.0 / tempoBPM.toDouble()) / 4.0
        val finalDuration = sixteenthDuration * 4.0

        fun isStaccatoAt(subIndex: Int): Boolean {
            val i = subIndex % 8
            return when (articulation) {
                EJ1Articulation.ORIGINAL,
                EJ1Articulation.ALL_SLURRED_8,
                EJ1Articulation.SLURRED_4_AND_4,
                EJ1Articulation.SLUR_PAIRS_2_BY_2 -> false
                EJ1Articulation.STACC_1_SLUR_3 -> (i == 0 || i == 4)
                EJ1Articulation.SLUR_3_STACC_1 -> (i == 3 || i == 7)
                EJ1Articulation.SLUR_2_STACC_2 -> (i == 2 || i == 3 || i == 6 || i == 7)
                EJ1Articulation.STACC_2_SLUR_2 -> (i == 0 || i == 1 || i == 4 || i == 5)
                EJ1Articulation.STACC_1_SLUR_2_STACC_1 -> (i == 0 || i == 3 || i == 4 || i == 7)
                EJ1Articulation.SLUR_SYNCOPATED -> (i == 0 || i == 7)
                EJ1Articulation.ALL_STACCATO -> true
            }
        }

        val notes = mutableListOf<NoteDef>()
        fun addGroup(midiNotes: List<Int>) {
            midiNotes.forEachIndexed { idx, m ->
                notes.add(
                    NoteDef(
                        freq = midiToFrequency(m.toDouble()),
                        duration = sixteenthDuration,
                        isStaccato = isStaccatoAt(idx)
                    )
                )
            }
        }

        val thirdOffset = if (isMinor) 3 else 4
        val dimFourthSemitone = if (isMinor) 4 else 5

        // 15 chromatic pairs (Measures 1..30), starting on D4 (MIDI 62) up to F5 (MIDI 77)
        for (k in 0 until 15) {
            val base = 62 + k
            // Odd measure: Major (0, 2, 4, 5, 7) or Minor (0, 2, 3, 5, 7) pentachord
            val pent = listOf(base, base + 2, base + thirdOffset, base + 5, base + 7)
            val pentGroup = listOf(pent[0], pent[1], pent[2], pent[3], pent[4], pent[3], pent[2], pent[1])
            repeat(4) {
                addGroup(pentGroup)
            }

            // Even measure: Diminished 7th vii° resolving to base + 1
            val dim = listOf(base, base + 1, base + 3, base + (if (isMinor) 4 else 5), base + 6)
            val dimGroup = listOf(dim[0], dim[1], dim[2], dim[3], dim[4], dim[3], dim[2], dim[1])
            val dimTurn  = listOf(dim[0], dim[1], dim[2], dim[3], dim[4], dim[2], dim[1], dim[0])
            repeat(3) {
                addGroup(dimGroup)
            }
            addGroup(dimTurn)
        }

        // Final measure M.31: F5 quarter note (MIDI 77)
        notes.add(
            NoteDef(
                freq = midiToFrequency(77.0),
                duration = finalDuration,
                isStaccato = false
            )
        )

        return renderNotesToPcm(notes)
    }

    private fun renderNotesToPcm(notes: List<NoteDef>): ShortArray {
        lastNoteDurations = notes.map { it.duration }
        val totalDuration = notes.sumOf { it.duration }
        val totalFrames = (sampleRate * totalDuration).toInt()
        val buffer = ShortArray(totalFrames)

        val pianoHarmonics = listOf(
            Triple(1.0, 1.00, 1.00),
            Triple(2.0, 0.55, 0.72),
            Triple(3.0, 0.35, 0.52),
            Triple(4.0, 0.20, 0.38),
            Triple(5.0, 0.12, 0.28),
            Triple(6.0, 0.06, 0.18)
        )
        val unisons = listOf(-0.35, 0.0, 0.35)

        var currentFrame = 0
        for (note in notes) {
            val noteFrames = (note.duration * sampleRate).toInt()
            val soundGate = if (note.isStaccato) 0.45 else 0.96
            val soundFrames = (noteFrames * soundGate).toInt()

            val attackFrames = max(1, (0.003 * sampleRate).toInt())
            val damperReleaseFrames = (0.020 * sampleRate).toInt()
            val decayBase = max(0.40, 0.85 - (note.freq / 2000.0) * 0.35)

            for (i in 0 until noteFrames) {
                val frameIndex = currentFrame + i
                if (frameIndex >= totalFrames) break

                if (i < soundFrames) {
                    val t = i.toDouble() / sampleRate
                    val attackEnv = if (i < attackFrames) i.toDouble() / attackFrames else 1.0
                    val releaseEnv = if (i > soundFrames - damperReleaseFrames) {
                        (soundFrames - i).toDouble() / damperReleaseFrames
                    } else 1.0

                    var noteSample = 0.0
                    for ((fMult, amp, dScale) in pianoHarmonics) {
                        val hDecay = exp(-t / (decayBase * dScale))
                        val hFreq = note.freq * fMult
                        for (u in unisons) {
                            noteSample += amp * (1.0 / 3.0) * sin(2.0 * Math.PI * (hFreq + u) * t) * hDecay
                        }
                    }

                    if (t < 0.008) {
                        val hammerNoise = sin(2.0 * Math.PI * 820.0 * t) * exp(-t / 0.002)
                        noteSample += hammerNoise * 0.10
                    }

                    val sample = noteSample * attackEnv * releaseEnv * 0.26
                    buffer[frameIndex] = (sample * 30000.0).toInt().coerceIn(-32768, 32767).toShort()
                } else {
                    buffer[frameIndex] = 0
                }
            }
            currentFrame += noteFrames
        }

        return buffer
    }

    fun release() {
        stop()
        scope.cancel()
    }

    companion object {
        fun midiToFrequency(midi: Double): Double {
            return 440.0 * 2.0.pow((midi - 69.0) / 12.0)
        }
    }
}
