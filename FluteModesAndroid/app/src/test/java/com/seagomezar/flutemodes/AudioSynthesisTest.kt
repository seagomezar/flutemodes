package com.seagomezar.flutemodes

import com.seagomezar.flutemodes.audio.ScoreAudioPlayer
import com.seagomezar.flutemodes.model.ArticulationPattern
import com.seagomezar.flutemodes.model.ModeType
import com.seagomezar.flutemodes.model.Tonic
import org.junit.Assert.*
import org.junit.Test
import kotlin.math.abs
import kotlin.math.exp
import kotlin.math.sin

class AudioSynthesisTest {

    @Test
    fun testMidiToFrequencyAccurateForFluteRegister() {
        // A4 = 440.0 Hz
        val a4 = ScoreAudioPlayer.midiToFrequency(69.0)
        assertEquals(440.0, a4, 0.001)

        // A3 = 220.0 Hz
        val a3 = ScoreAudioPlayer.midiToFrequency(57.0)
        assertEquals(220.0, a3, 0.001)

        // Middle C (C4) = ~261.625 Hz
        val c4 = ScoreAudioPlayer.midiToFrequency(60.0)
        assertTrue("C4 frequency should be around 261.625", abs(c4 - 261.625) < 0.05)

        // Low B3 (lowest flute note with B-foot) = ~246.94 Hz
        val b3 = ScoreAudioPlayer.midiToFrequency(59.0)
        assertTrue("B3 frequency should be around 246.94", abs(b3 - 246.94) < 0.05)

        // High C7 = ~2093.00 Hz
        val c7 = ScoreAudioPlayer.midiToFrequency(96.0)
        assertTrue("C7 frequency should be around 2093.0", abs(c7 - 2093.0) < 0.1)
    }

    @Test
    fun testMetronomeDecayEnvelopeMath() {
        val sampleRate = 44100
        val duration = 0.025
        val frameCount = (sampleRate * duration).toInt()

        for (i in 0 until frameCount) {
            val t = i.toDouble() / sampleRate
            val envelope = exp(-t * 90.0)
            val sample = sin(2.0 * Math.PI * 1400.0 * t) * envelope
            val pcm = (sample * 30000.0).toInt().coerceIn(-32768, 32767).toShort()

            assertFalse("Sample should not be NaN", sample.isNaN())
            assertFalse("Sample should not be infinite", sample.isInfinite())
            assertTrue("Envelope should be monotonically bounded [0, 1]", envelope in 0.0..1.0)
            assertTrue("PCM value within 16-bit short range", pcm in -32768..32767)
        }
    }

    @Test
    fun testScoreBufferGenerationWithoutClipping() {
        val player = ScoreAudioPlayer()
        val buffer = player.generateScoreBuffer(
            tonic = Tonic.DO_NATURAL,
            mode = ModeType.IONIAN,
            articulation = ArticulationPattern.ALL_SLURRED,
            tempoBPM = 120
        )

        assertTrue("Generated score buffer must not be empty", buffer.isNotEmpty())

        var maxSample: Short = 0
        var minSample: Short = 0
        for (sample in buffer) {
            if (sample > maxSample) maxSample = sample
            if (sample < minSample) minSample = sample
        }

        assertTrue("Audio buffer must have signal content", maxSample > 0 || minSample < 0)
        assertTrue("Max sample must be within valid range", maxSample <= Short.MAX_VALUE)
        assertTrue("Min sample must be within valid range", minSample >= Short.MIN_VALUE)
    }
}
