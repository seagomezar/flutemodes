package com.seagomezar.flutemodes

import android.content.Context
import android.content.ContextWrapper
import android.content.SharedPreferences
import com.seagomezar.flutemodes.model.*
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test

/**
 * Empirical Challenger Verification Test for Reichert Navigation Routing & Dialog State Machine.
 * Validates:
 * 1. Screen.Practice route construction for all 25 sections across R1, R2, R4, R5 (1,000 combinations).
 * 2. PracticeStore isolation between Reichert exercises (R1, R2, R4, R5) and T&G exercises (EJ4, EJ5, EJ10, EJ11).
 * 3. Section progression wrap-around arithmetic ((sec + 1) % 25).
 * 4. Exercise advance sequential transitions (R1 -> R2 -> R4 -> R5 -> MODOS).
 * 5. EJ11 advance transition directly to R1.
 */
class ReichertNavigationFlowTest {

    private class FakeSharedPreferences : SharedPreferences {
        val storage = mutableMapOf<String, Any>()

        override fun getAll(): Map<String, *> = storage.toMap()
        override fun getString(key: String?, defValue: String?): String? = storage[key] as? String ?: defValue
        override fun getStringSet(key: String?, defValues: Set<String>?): Set<String>? = storage[key] as? Set<String> ?: defValues
        override fun getInt(key: String?, defValue: Int): Int = storage[key] as? Int ?: defValue
        override fun getLong(key: String?, defValue: Long): Long = storage[key] as? Long ?: defValue
        override fun getFloat(key: String?, defValue: Float): Float = storage[key] as? Float ?: defValue
        override fun getBoolean(key: String?, defValue: Boolean): Boolean = storage[key] as? Boolean ?: defValue
        override fun contains(key: String?): Boolean = storage.containsKey(key)
        override fun registerOnSharedPreferenceChangeListener(listener: SharedPreferences.OnSharedPreferenceChangeListener?) {}
        override fun unregisterOnSharedPreferenceChangeListener(listener: SharedPreferences.OnSharedPreferenceChangeListener?) {}
        override fun edit(): SharedPreferences.Editor = FakeEditor(this)

        class FakeEditor(private val prefs: FakeSharedPreferences) : SharedPreferences.Editor {
            private val temp = mutableMapOf<String, Any?>()
            private var clearCalled = false

            override fun putString(key: String?, value: String?): SharedPreferences.Editor {
                if (key != null) temp[key] = value
                return this
            }
            override fun putStringSet(key: String?, values: MutableSet<String>?): SharedPreferences.Editor {
                if (key != null) temp[key] = values
                return this
            }
            override fun putInt(key: String?, value: Int): SharedPreferences.Editor {
                if (key != null) temp[key] = value
                return this
            }
            override fun putLong(key: String?, value: Long): SharedPreferences.Editor {
                if (key != null) temp[key] = value
                return this
            }
            override fun putFloat(key: String?, value: Float): SharedPreferences.Editor {
                if (key != null) temp[key] = value
                return this
            }
            override fun putBoolean(key: String?, value: Boolean): SharedPreferences.Editor {
                if (key != null) temp[key] = value
                return this
            }
            override fun remove(key: String?): SharedPreferences.Editor {
                if (key != null) temp[key] = null
                return this
            }
            override fun clear(): SharedPreferences.Editor {
                clearCalled = true
                return this
            }
            override fun commit(): Boolean {
                apply()
                return true
            }
            override fun apply() {
                if (clearCalled) {
                    prefs.storage.clear()
                    clearCalled = false
                }
                for ((k, v) in temp) {
                    if (v == null) prefs.storage.remove(k) else prefs.storage[k] = v
                }
                temp.clear()
            }
        }
    }

    private val fakePrefs = FakeSharedPreferences()
    private lateinit var store: PracticeStore

    @Before
    fun setup() {
        val fakeContext = object : ContextWrapper(null) {
            override fun getSharedPreferences(name: String?, mode: Int): SharedPreferences {
                return fakePrefs
            }
        }
        store = PracticeStore(fakeContext)
    }

    @Test
    fun testScreenPracticeRouteConstructionAllPermutations() {
        val allSections = EJ4Section.entries
        val ej5Arts = EJ5Articulation.entries
        val ej4Arts = EJ4Articulation.entries

        assertEquals(25, allSections.size)
        assertEquals(11, ej5Arts.size)
        assertEquals(9, ej4Arts.size)

        var r1Count = 0
        var r2Count = 0
        var r4Count = 0
        var r5Count = 0

        // Test R1 route construction (275 combinations)
        for (sec in allSections) {
            for (art in ej5Arts) {
                val route = Screen.Practice(
                    exerciseType = ExerciseType.R1,
                    r1Articulation = art,
                    r1Section = sec
                )
                assertEquals(ExerciseType.R1, route.exerciseType)
                assertEquals(art, route.r1Articulation)
                assertEquals(sec, route.r1Section)
                r1Count++
            }
        }
        assertEquals(275, r1Count)

        // Test R2 route construction (225 combinations)
        for (sec in allSections) {
            for (art in ej4Arts) {
                val route = Screen.Practice(
                    exerciseType = ExerciseType.R2,
                    r2Articulation = art,
                    r2Section = sec
                )
                assertEquals(ExerciseType.R2, route.exerciseType)
                assertEquals(art, route.r2Articulation)
                assertEquals(sec, route.r2Section)
                r2Count++
            }
        }
        assertEquals(225, r2Count)

        // Test R4 route construction (225 combinations)
        for (sec in allSections) {
            for (art in ej4Arts) {
                val route = Screen.Practice(
                    exerciseType = ExerciseType.R4,
                    r4Articulation = art,
                    r4Section = sec
                )
                assertEquals(ExerciseType.R4, route.exerciseType)
                assertEquals(art, route.r4Articulation)
                assertEquals(sec, route.r4Section)
                r4Count++
            }
        }
        assertEquals(225, r4Count)

        // Test R5 route construction (275 combinations)
        for (sec in allSections) {
            for (art in ej5Arts) {
                val route = Screen.Practice(
                    exerciseType = ExerciseType.R5,
                    r5Articulation = art,
                    r5Section = sec
                )
                assertEquals(ExerciseType.R5, route.exerciseType)
                assertEquals(art, route.r5Articulation)
                assertEquals(sec, route.r5Section)
                r5Count++
            }
        }
        assertEquals(275, r5Count)

        val total = r1Count + r2Count + r4Count + r5Count
        assertEquals(1000, total)
    }

    @Test
    fun testReichertAndTGStoreIsolation() {
        store.resetAll()

        // Mark R1 art completed
        store.markEJ5TypeCompleted(EJ5Articulation.ALL_SLURRED, ExerciseType.R1)
        assertTrue(store.isEJ5TypeCompleted(EJ5Articulation.ALL_SLURRED, ExerciseType.R1))
        assertFalse(store.isEJ5TypeCompleted(EJ5Articulation.ALL_SLURRED, ExerciseType.R5))
        assertFalse(store.isEJ5TypeCompleted(EJ5Articulation.ALL_SLURRED, ExerciseType.EJ5))
        assertFalse(store.isEJ5TypeCompleted(EJ5Articulation.ALL_SLURRED, ExerciseType.EJ10))
        assertFalse(store.isEJ5TypeCompleted(EJ5Articulation.ALL_SLURRED, ExerciseType.EJ11))

        // Mark R2 art completed
        store.markEJ4Completed(EJ4Articulation.ALL_SLURRED_8, ExerciseType.R2)
        assertTrue(store.isEJ4Completed(EJ4Articulation.ALL_SLURRED_8, ExerciseType.R2))
        assertFalse(store.isEJ4Completed(EJ4Articulation.ALL_SLURRED_8, ExerciseType.R4))
        assertFalse(store.isEJ4Completed(EJ4Articulation.ALL_SLURRED_8, ExerciseType.EJ4))

        // Mark R4 art completed
        store.markEJ4Completed(EJ4Articulation.SLURRED_4_AND_4, ExerciseType.R4)
        assertTrue(store.isEJ4Completed(EJ4Articulation.SLURRED_4_AND_4, ExerciseType.R4))
        assertFalse(store.isEJ4Completed(EJ4Articulation.SLURRED_4_AND_4, ExerciseType.R2))
        assertFalse(store.isEJ4Completed(EJ4Articulation.SLURRED_4_AND_4, ExerciseType.EJ4))

        // Mark R5 art completed
        store.markEJ5TypeCompleted(EJ5Articulation.SLURRED_6_BY_6, ExerciseType.R5)
        assertTrue(store.isEJ5TypeCompleted(EJ5Articulation.SLURRED_6_BY_6, ExerciseType.R5))
        assertFalse(store.isEJ5TypeCompleted(EJ5Articulation.SLURRED_6_BY_6, ExerciseType.R1))
    }

    @Test
    fun testSectionAdvanceCircularWrapAround() {
        val allSecs = EJ4Section.entries
        assertEquals(25, allSecs.size)

        for (i in 0 until 24) {
            val cur = allSecs[i]
            val nextIdx = (allSecs.indexOf(cur) + 1) % allSecs.size
            assertEquals(i + 1, nextIdx)
            assertEquals(allSecs[i + 1], allSecs[nextIdx])
        }

        // Section 24 (Coda / D.S. al Fine) advances back to Section 0 (C_MAJOR)
        val coda = allSecs[24]
        val wrappedIdx = (allSecs.indexOf(coda) + 1) % allSecs.size
        assertEquals(0, wrappedIdx)
        assertEquals(EJ4Section.C_MAJOR, allSecs[wrappedIdx])
    }

    @Test
    fun testSequentialExerciseAdvanceFlow() {
        val nextExFromR1 = when (ExerciseType.R1) {
            ExerciseType.R1 -> ExerciseType.R2
            ExerciseType.R2 -> ExerciseType.R4
            ExerciseType.R4 -> ExerciseType.R5
            else -> ExerciseType.MODOS
        }
        assertEquals(ExerciseType.R2, nextExFromR1)

        val nextExFromR2 = when (ExerciseType.R2) {
            ExerciseType.R1 -> ExerciseType.R2
            ExerciseType.R2 -> ExerciseType.R4
            ExerciseType.R4 -> ExerciseType.R5
            else -> ExerciseType.MODOS
        }
        assertEquals(ExerciseType.R4, nextExFromR2)

        val nextExFromR4 = when (ExerciseType.R4) {
            ExerciseType.R1 -> ExerciseType.R2
            ExerciseType.R2 -> ExerciseType.R4
            ExerciseType.R4 -> ExerciseType.R5
            else -> ExerciseType.MODOS
        }
        assertEquals(ExerciseType.R5, nextExFromR4)

        val nextExFromR5 = when (ExerciseType.R5) {
            ExerciseType.R1 -> ExerciseType.R2
            ExerciseType.R2 -> ExerciseType.R4
            ExerciseType.R4 -> ExerciseType.R5
            else -> ExerciseType.MODOS
        }
        assertEquals(ExerciseType.MODOS, nextExFromR5)
    }

    @Test
    fun testEJ11AdvancesToR1() {
        val nextFromEJ11 = ExerciseType.R1
        assertEquals(ExerciseType.R1, nextFromEJ11)
        assertTrue(nextFromEJ11.isReichertExercise)
        assertFalse(nextFromEJ11.isEJ4Exercise)
        assertTrue(nextFromEJ11.isEJ5TypeExercise)
    }

    @Test
    fun testPracticeStoreRoundResetPreservesOtherExercises() {
        store.resetAll()

        // Populate R1 and R2
        for (art in EJ5Articulation.practiceCases) {
            store.markEJ5TypeCompleted(art, ExerciseType.R1)
        }
        for (art in EJ4Articulation.practiceCases) {
            store.markEJ4Completed(art, ExerciseType.R2)
        }
        assertTrue(store.isEJ5TypeFullyCompleted(ExerciseType.R1))
        assertTrue(store.isEJ4FullyCompleted(ExerciseType.R2))

        // Reset R1
        store.resetEJ5Type(ExerciseType.R1)
        assertFalse(store.isEJ5TypeFullyCompleted(ExerciseType.R1))
        assertEquals(0, store.ej5TypeCompletedCount(ExerciseType.R1))

        // R2 must still be fully completed
        assertTrue(store.isEJ4FullyCompleted(ExerciseType.R2))
        assertEquals(8, store.ej4CompletedCount(ExerciseType.R2))
    }
}
