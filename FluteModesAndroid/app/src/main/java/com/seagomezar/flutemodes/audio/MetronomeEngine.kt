package com.seagomezar.flutemodes.audio

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import kotlinx.coroutines.*
import kotlin.math.exp
import kotlin.math.sin

class MetronomeEngine {
    var isPlaying by mutableStateOf(false)
        private set

    var tempoBPM by mutableIntStateOf(90)
        private set

    var currentBeat by mutableIntStateOf(0)
        private set

    var isAudioMuted by mutableStateOf(false)

    private var metronomeJob: Job? = null
    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())

    private val sampleRate = 44100
    private var clickTrack: AudioTrack? = null

    init {
        setupClickBuffer()
    }

    private fun setupClickBuffer() {
        try {
            val duration = 0.025 // 25ms sharp decay click
            val frameCount = (sampleRate * duration).toInt()
            val buffer = ShortArray(frameCount)

            for (i in 0 until frameCount) {
                val t = i.toDouble() / sampleRate
                val envelope = exp(-t * 90.0) // sharp percussive decay
                val sample = sin(2.0 * Math.PI * 1400.0 * t) * envelope
                buffer[i] = (sample * 30000.0).toInt().coerceIn(-32768, 32767).toShort()
            }

            val attributes = AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_MEDIA)
                .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                .build()

            val format = AudioFormat.Builder()
                .setSampleRate(sampleRate)
                .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                .build()

            val track = AudioTrack(
                attributes,
                format,
                buffer.size * 2,
                AudioTrack.MODE_STATIC,
                android.media.AudioManager.AUDIO_SESSION_ID_GENERATE
            )
            track.write(buffer, 0, buffer.size)
            clickTrack = track
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun toggle() {
        if (isPlaying) stop() else start()
    }

    fun start() {
        stop()
        isPlaying = true
        currentBeat = 0

        metronomeJob = scope.launch {
            val intervalNanos = (60.0 / tempoBPM * 1_000_000_000L).toLong()
            var nextTickTime = System.nanoTime()

            while (isActive && isPlaying) {
                tick()

                nextTickTime += intervalNanos
                val sleepNanos = nextTickTime - System.nanoTime()
                if (sleepNanos > 0) {
                    val millis = sleepNanos / 1_000_000L
                    val nanos = (sleepNanos % 1_000_000L).toInt()
                    delay(millis)
                }
            }
        }
    }

    fun stop() {
        isPlaying = false
        currentBeat = 0
        metronomeJob?.cancel()
        metronomeJob = null
    }

    fun setTempo(newBPM: Int) {
        val clamped = newBPM.coerceIn(40, 160)
        tempoBPM = clamped
        if (isPlaying) {
            start() // restart with new interval
        }
    }

    private fun tick() {
        currentBeat = (currentBeat % 4) + 1

        if (!isAudioMuted) {
            try {
                clickTrack?.let { track ->
                    if (track.state == AudioTrack.STATE_INITIALIZED) {
                        track.stop()
                        track.reloadStaticData()
                        track.play()
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    fun release() {
        stop()
        clickTrack?.release()
        clickTrack = null
        scope.cancel()
    }
}
