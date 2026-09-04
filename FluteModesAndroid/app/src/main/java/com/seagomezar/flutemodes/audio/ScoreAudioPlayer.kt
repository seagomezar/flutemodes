package com.seagomezar.flutemodes.audio

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import com.seagomezar.flutemodes.model.ArticulationPattern
import com.seagomezar.flutemodes.model.ModeType
import com.seagomezar.flutemodes.model.Tonic
import kotlinx.coroutines.*
import kotlin.math.*

class ScoreAudioPlayer {
    var isPlaying by mutableStateOf(false)
        private set

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
        isPlaying = false
    }

    fun play(tonic: Tonic, mode: ModeType, articulation: ArticulationPattern, tempoBPM: Int) {
        stop()
        isPlaying = true

        playbackJob = scope.launch {
            val buffer = generateScoreBuffer(tonic, mode, articulation, tempoBPM)
            if (!isActive || buffer.isEmpty()) {
                withContext(Dispatchers.Main) { isPlaying = false }
                return@launch
            }

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

                // Calculate total duration
                val durationMs = (buffer.size.toDouble() / sampleRate * 1000.0).toLong()
                delay(durationMs)
            } catch (e: Exception) {
                e.printStackTrace()
            } finally {
                withContext(Dispatchers.Main) {
                    isPlaying = false
                }
            }
        }
    }

    private data class NoteDef(val freq: Double, val duration: Double, val isStaccato: Boolean)

    private fun generateScoreBuffer(
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
            return 440.0 * 2.0.pow((midi - 69.0) / 12.0)
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
}
