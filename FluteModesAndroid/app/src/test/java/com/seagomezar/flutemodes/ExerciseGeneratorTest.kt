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

    @Test
    fun testEJ1AndEJ2AllArticulationsGenerateValidAbc() {
        assertEquals(30, ExerciseGenerator.ej1RawMeasures.size)
        assertEquals(30, ExerciseGenerator.ej2RawMeasures.size)

        for (art in EJ1Articulation.entries) {
            val ej1Abc = ExerciseGenerator.generateEJ1ABC(articulation = art, tempoBPM = 120, loc = loc)
            assertTrue(ej1Abc.contains("% EJ1_LEDUC_ART:${art.id}"))
            assertTrue(ej1Abc.contains("Q:1/4=120"))

            val ej2Abc = ExerciseGenerator.generateEJ2ABC(articulation = art, tempoBPM = 120, loc = loc)
            assertTrue(ej2Abc.contains("% EJ2_LEDUC_ART:${art.id}"))
            assertTrue(ej2Abc.contains("Q:1/4=120"))
            assertTrue(ej2Abc.contains("^^F"))
            assertTrue(ej2Abc.contains("^B"))
        }
    }

    @Test
    fun testEJ4AllSectionsAndArticulationsGenerateValidAbc() {
        assertEquals(25, EJ4Section.entries.size)
        assertEquals(25, ExerciseGenerator.ej4SectionMidiNotes.size)
        val aMinorNotes = ExerciseGenerator.ej4SectionMidiNotes[1]
        assertEquals(80, aMinorNotes[10])
        assertEquals(77, aMinorNotes[11])
        assertEquals(80, aMinorNotes[106])
        assertEquals(77, aMinorNotes[107])

        for (sec in EJ4Section.entries) {
            for (art in EJ4Articulation.entries) {
                val ej4Abc = ExerciseGenerator.generateEJ4ABC(articulation = art, section = sec, tempoBPM = 120)
                assertTrue(ej4Abc.contains("% EJ4_LEDUC_ART:${art.id}:SEC:${sec.id}"))
                assertTrue(ej4Abc.contains("Q:1/2=120"))
            }
            val midiNotes = ExerciseGenerator.ej4SectionMidiNotes[sec.id]
            val expectedNotes = if (sec.id < 24) 128 else 29
            assertEquals("Section ${sec.name} should generate $expectedNotes MIDI notes", expectedNotes, midiNotes.size)
        }
    }

    @Test
    fun testEJ5AllSectionsAndArticulationsGenerateValidAbcAndMidi() {
        assertEquals(12, EJ5Section.entries.size)
        assertEquals(12, ExerciseGenerator.ej5SectionMidiNotes.size)

        for (sec in EJ5Section.entries) {
            assertTrue("EJ5 section ${sec.name} must have MIDI notes", ExerciseGenerator.ej5SectionMidiNotes[sec.id].isNotEmpty())
            for (art in EJ5Articulation.entries) {
                val ej5Abc = ExerciseGenerator.generateEJ5ABC(articulation = art, section = sec, tempoBPM = 120)
                assertTrue(ej5Abc.contains("% EJ5_LEDUC_ART:${art.id}:SEC:${sec.id}"))
                assertTrue(ej5Abc.contains("Q:1/4=120"))
            }
        }
    }

    @Test
    fun testEJ10AndEJ11AllSectionsAndArticulationsGenerateValidAbcAndMidi() {
        assertEquals(12, EJ10Section.entries.size)
        assertEquals(12, ExerciseGenerator.ej10SectionMidiNotes.size)
        assertEquals(12, ExerciseGenerator.ej11SectionMidiNotes.size)

        for (sec in EJ10Section.entries) {
            assertTrue("EJ10 section ${sec.name} must have MIDI notes", ExerciseGenerator.ej10SectionMidiNotes[sec.id].isNotEmpty())
            assertTrue("EJ11 section ${sec.name} must have MIDI notes", ExerciseGenerator.ej11SectionMidiNotes[sec.id].isNotEmpty())
            for (art in EJ5Articulation.entries) {
                val ej10Abc = ExerciseGenerator.generateEJ10ABC(articulation = art, section = sec, tempoBPM = 120)
                assertTrue(ej10Abc.contains("% EJ10_LEDUC_ART:${art.id}:SEC:${sec.id}"))
                val ej11Abc = ExerciseGenerator.generateEJ11ABC(articulation = art, section = sec, tempoBPM = 120)
                assertTrue(ej11Abc.contains("% EJ11_LEDUC_ART:${art.id}:SEC:${sec.id}"))
            }
        }
    }

    @Test
    fun testReichertR1R2R4R5AllSectionsAndArticulationsGenerateValidAbcAndMidi() {
        assertEquals(25, ExerciseGenerator.r1SectionMidiNotes.size)
        assertEquals(25, ExerciseGenerator.r2SectionMidiNotes.size)
        assertEquals(25, ExerciseGenerator.r4SectionMidiNotes.size)
        assertEquals(25, ExerciseGenerator.r5SectionMidiNotes.size)

        for (sec in EJ4Section.entries) {
            assertTrue("R1 section ${sec.name} must have MIDI notes", ExerciseGenerator.r1SectionMidiNotes[sec.id].isNotEmpty())
            assertTrue("R2 section ${sec.name} must have MIDI notes", ExerciseGenerator.r2SectionMidiNotes[sec.id].isNotEmpty())
            assertTrue("R4 section ${sec.name} must have MIDI notes", ExerciseGenerator.r4SectionMidiNotes[sec.id].isNotEmpty())
            assertTrue("R5 section ${sec.name} must have MIDI notes", ExerciseGenerator.r5SectionMidiNotes[sec.id].isNotEmpty())

            for (art in EJ5Articulation.entries) {
                val r1Abc = ExerciseGenerator.generateR1ABC(articulation = art, section = sec, tempoBPM = 92)
                assertTrue(r1Abc.contains("% R1_SCHOTT_ART:${art.id}:SEC:${sec.id}"))
                val r5Abc = ExerciseGenerator.generateR5ABC(articulation = art, section = sec, tempoBPM = 160)
                assertTrue(r5Abc.contains("% R5_SCHOTT_ART:${art.id}:SEC:${sec.id}"))
            }
            for (art in EJ4Articulation.entries) {
                val r2Abc = ExerciseGenerator.generateR2ABC(articulation = art, section = sec, tempoBPM = 132)
                assertTrue(r2Abc.contains("% R2_SCHOTT_ART:${art.id}:SEC:${sec.id}"))
                val r4Abc = ExerciseGenerator.generateR4ABC(articulation = art, section = sec, tempoBPM = 126)
                assertTrue(r4Abc.contains("% R4_SCHOTT_ART:${art.id}:SEC:${sec.id}"))
            }
        }
    }

    @Test
    fun testAll840ModalSchemesGenerateValidAbcAndMidi() {
        var count = 0
        for (tonic in Tonic.entries) {
            for (mode in ModeType.entries) {
                for (scheme in ModalScheme.entries) {
                    val abc = ExerciseGenerator.generateABC(
                        tonic = tonic,
                        mode = mode,
                        articulation = ArticulationPattern.ALL_SLURRED,
                        tempoBPM = 96,
                        loc = loc,
                        scheme = scheme
                    )
                    assertTrue(abc.startsWith("X:1"))
                    assertTrue(abc.contains("M:${scheme.meter}"))
                    assertTrue(abc.contains("Esquema: ${scheme.code}"))
                    assertTrue(abc.trimEnd().endsWith("|]"))

                    val midi = ExerciseGenerator.generateModalSchemeMidiNotes(
                        tonic = tonic,
                        mode = mode,
                        scheme = scheme
                    )
                    assertEquals(
                        "Scheme ${scheme.code} in ${tonic.name} ${mode.name} should have ${scheme.totalNotes} MIDI notes",
                        scheme.totalNotes,
                        midi.size
                    )
                    for (m in midi) {
                        assertTrue("MIDI note $m must be >= 58", m >= 58)
                        assertTrue("MIDI note $m must be <= 98", m <= 98)
                    }
                    count++
                }
            }
        }
        assertEquals("Should have verified all 12 tonics * 7 modes * 10 schemes = 840 combinations", 840, count)

        // Verify double flats in E-flat Locrian and A-flat Phrygian/Locrian
        val ebLocAbc = ExerciseGenerator.generateABC(
            tonic = Tonic.MI_BEMOL,
            mode = ModeType.LOCRIAN,
            articulation = ArticulationPattern.ALL_SLURRED,
            tempoBPM = 96,
            loc = loc,
            scheme = ModalScheme.EJ4
        )
        assertTrue(ebLocAbc.contains("__B") || ebLocAbc.contains("__b"))

        val abLocAbc = ExerciseGenerator.generateABC(
            tonic = Tonic.LA_BEMOL,
            mode = ModeType.LOCRIAN,
            articulation = ArticulationPattern.ALL_SLURRED,
            tempoBPM = 96,
            loc = loc,
            scheme = ModalScheme.R1
        )
        assertTrue(abLocAbc.contains("__E") || abLocAbc.contains("__e"))
        assertTrue(abLocAbc.contains("__B") || abLocAbc.contains("__b"))
    }

    @Test
    fun testConservatoryCoachPracticeWizardRoutines() {
        for (duration in PracticeWizardDuration.entries) {
            for (focus in PracticeWizardFocus.entries) {
                val blocks = PracticeRoutineBlock.generateRoutine(
                    duration = duration,
                    focus = focus,
                    tonic = Tonic.RE,
                    mode = ModeType.DORIAN,
                    loc = loc
                )
                assertEquals(3, blocks.size)
                val totalMinutes = blocks.sumOf { it.minutes }
                assertEquals(duration.minutes, totalMinutes)
            }
        }

        assertEquals(1, ModalScheme.EJ1.barsPerStaff)
        assertEquals(1, ModalScheme.EJ2.barsPerStaff)
        assertEquals(2, ModalScheme.EJ4.barsPerStaff)
        assertEquals(2, ModalScheme.EJ5.barsPerStaff)
        assertEquals(2, ModalScheme.EJ10.barsPerStaff)
        assertEquals(2, ModalScheme.EJ11.barsPerStaff)
        assertEquals(2, ModalScheme.R1.barsPerStaff)
        assertEquals(2, ModalScheme.R4.barsPerStaff)
        assertEquals(4, ModalScheme.R2.barsPerStaff)
        assertEquals(4, ModalScheme.R5.barsPerStaff)

        assertTrue(CoachStrings.coachHeroTitle(loc) != "coach_title")
        assertTrue(CoachStrings.openWizardButton(loc) != "coach_open_wizard")
        assertTrue(CoachStrings.level3SchemeHeader(loc) != "coach_level3_scheme")
        assertFalse(CoachStrings.coachBadge(loc).contains("OPCIÓN 1"))
        assertFalse(CoachStrings.coachBadge(loc).contains("OPTION 1"))
        assertEquals("CONSERVATORY COACH · ASISTENTE GUIADO", CoachStrings.coachBadge(loc))

        val ej4ModalAbc = ExerciseGenerator.generateABC(
            tonic = Tonic.DO_NATURAL,
            mode = ModeType.AEOLIAN,
            articulation = ArticulationPattern.ALL_SLURRED,
            tempoBPM = 96,
            loc = loc,
            scheme = ModalScheme.EJ4
        )
        assertTrue(ej4ModalAbc.contains("T:Modo 5: Do Eólico (E.J. 4)"))
        assertFalse(ej4ModalAbc.contains("(Menor Natural)"))
    }
}


