package com.seagomezar.flutemodes

import com.seagomezar.flutemodes.model.*
import org.junit.Assert.*
import org.junit.Test

class ExerciseGeneratorTest {

    private class DummySharedPreferences : android.content.SharedPreferences {
        override fun getAll(): Map<String, *> = emptyMap<String, Any>()
        override fun getString(key: String?, defValue: String?): String? = defValue
        override fun getStringSet(key: String?, defValues: Set<String>?): Set<String>? = defValues
        override fun getInt(key: String?, defValue: Int): Int = defValue
        override fun getLong(key: String?, defValue: Long): Long = defValue
        override fun getFloat(key: String?, defValue: Float): Float = defValue
        override fun getBoolean(key: String?, defValue: Boolean): Boolean = defValue
        override fun contains(key: String?): Boolean = false
        override fun registerOnSharedPreferenceChangeListener(listener: android.content.SharedPreferences.OnSharedPreferenceChangeListener?) {}
        override fun unregisterOnSharedPreferenceChangeListener(listener: android.content.SharedPreferences.OnSharedPreferenceChangeListener?) {}
        override fun edit(): android.content.SharedPreferences.Editor = DummyEditor()

        class DummyEditor : android.content.SharedPreferences.Editor {
            override fun putString(key: String?, value: String?) = this
            override fun putStringSet(key: String?, values: MutableSet<String>?) = this
            override fun putInt(key: String?, value: Int) = this
            override fun putLong(key: String?, value: Long) = this
            override fun putFloat(key: String?, value: Float) = this
            override fun putBoolean(key: String?, value: Boolean) = this
            override fun remove(key: String?) = this
            override fun clear() = this
            override fun commit() = true
            override fun apply() {}
        }
    }

    private val loc = LocalizationManager(object : android.content.ContextWrapper(null) {
        override fun getSharedPreferences(name: String?, mode: Int): android.content.SharedPreferences {
            return DummySharedPreferences()
        }
    })

    @Test
    fun testAll84ModalCombinationsGenerateValidAbc() {
        var count = 0
        for (tonic in Tonic.values()) {
            for (mode in ModeType.values()) {
                for (art in ArticulationPattern.values()) {
                    val abc = ExerciseGenerator.generateABC(
                        tonic = tonic,
                        mode = mode,
                        articulation = art,
                        tempoBPM = 90,
                        loc = loc
                    )

                    // Verifications
                    assertNotNull(abc)
                    assertTrue("ABC should start with X:1 header", abc.startsWith("X:1"))
                    assertTrue("ABC should have time signature 4/2", abc.contains("M:4/2"))
                    assertTrue("ABC should have unit length 1/8", abc.contains("L:1/8"))
                    assertTrue("ABC should have tempo definition", abc.contains("Q:1/2=90"))
                    assertTrue("ABC should define treble clef", abc.contains("V:1 clef=treble"))
                    assertTrue("ABC should finish with terminal bar |]", abc.trimEnd().endsWith("|]"))

                    // Count measures: should have 8 measures separated by |
                    val measures = abc.substringAfter("%%score 1\n").split("|").map { it.trim() }.filter { it.isNotEmpty() && it != "]" }
                    assertEquals("Exercise must consist of 8 measures for ${tonic.name} ${mode.name} with ${art.name}", 8, measures.size)

                    count++
                }
            }
        }
        assertEquals("Should have tested all 12 tonics * 7 modes * 8 articulations = 672 combinations", 672, count)
    }

    @Test
    fun testFlutePitchRangeSafety() {
        for (tonic in Tonic.values()) {
            // Flute lowest note is B3 (59) or C4 (60)
            assertTrue("Root MIDI of ${tonic.name} must be >= 59 (B3)", tonic.rootMidi >= 59)
            assertTrue("Root MIDI of ${tonic.name} must be <= 71 (B4)", tonic.rootMidi <= 71)

            // ABC note sequence size
            assertEquals("Tonic ${tonic.name} must have 16 base notes in sequence", 16, tonic.abcNoteSequence.size)

            for (mode in ModeType.values()) {
                val intervals = mode.intervals
                assertEquals("Mode ${mode.name} must define 7 diatonic intervals", 7, intervals.size)

                // Check highest pitch index reached (index 14 at peak)
                val apexDegree = 14 % 7
                val apexOctave = 14 / 7
                val apexSemitones = intervals[apexDegree] + (apexOctave * 12)
                val apexMidi = tonic.rootMidi + apexSemitones

                // Highest playable flute note in pedagogical repertoire is around C7 (96) or D7 (98)
                assertTrue("Peak note of ${tonic.name} ${mode.name} (MIDI $apexMidi) must not exceed 98 (D7)", apexMidi <= 98)
            }
        }
    }

    @Test
    fun testAll8ArticulationPatternsParenthesesBalanced() {
        val dummyNotes = listOf("C", "D", "E", "F", "G", "A", "B", "c")
        for (art in ArticulationPattern.values()) {
            val formatted = art.apply(dummyNotes)
            val openCount = formatted.count { it == '(' }
            val closeCount = formatted.count { it == ')' }
            assertEquals("Parentheses must balance for articulation ${art.name}", openCount, closeCount)
        }
    }

    @Test
    fun testAccidentalMapDegreesWithinBounds() {
        for (tonic in Tonic.values()) {
            for (mode in ModeType.values()) {
                val accMap = tonic.accidentalMap(mode)
                for (degree in accMap.keys) {
                    assertTrue("Accidental degree $degree must be in range 0..6", degree in 0..6)
                    val acc = accMap[degree]
                    assertTrue("Accidental must be valid ABC symbol (^, ^^, =, _)", acc in listOf("^", "^^", "=", "_"))
                }
            }
        }
    }

    @Test
    fun testKeySignaturesValid() {
        for (tonic in Tonic.values()) {
            for (mode in ModeType.values()) {
                val key = mode.keySignature(tonic)
                assertNotNull(key)
                assertTrue("Key signature must not be blank for ${tonic.name} ${mode.name}", key.isNotBlank())
            }
        }
    }
}
