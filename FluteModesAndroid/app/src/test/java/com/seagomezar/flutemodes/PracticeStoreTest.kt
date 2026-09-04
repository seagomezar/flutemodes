package com.seagomezar.flutemodes

import android.content.Context
import android.content.ContextWrapper
import android.content.SharedPreferences
import com.seagomezar.flutemodes.model.*
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test

class PracticeStoreTest {

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
    fun testKeepScreenAwakeDefaultsToTrue() {
        assertTrue("keepScreenAwake should default to true", store.keepScreenAwake)
        store.setKeepScreenAwakeState(false)
        assertFalse("keepScreenAwake should update to false", store.keepScreenAwake)
        assertEquals(false, fakePrefs.getBoolean("keep_screen_awake", true))
        store.setKeepScreenAwakeState(true)
        assertTrue("keepScreenAwake should update back to true", store.keepScreenAwake)
    }

    @Test
    fun testMarkCompletedAndArticulationsCounting() {
        assertEquals(0, store.completedArticulationsCount(Tonic.DO_NATURAL, ModeType.IONIAN))
        assertFalse(store.isCompleted(Tonic.DO_NATURAL, ModeType.IONIAN, ArticulationPattern.ALL_SLURRED))

        // Mark 1 articulation
        store.markCompleted(Tonic.DO_NATURAL, ModeType.IONIAN, ArticulationPattern.ALL_SLURRED)
        assertTrue(store.isCompleted(Tonic.DO_NATURAL, ModeType.IONIAN, ArticulationPattern.ALL_SLURRED))
        assertFalse(store.isCompleted(Tonic.DO_NATURAL, ModeType.IONIAN, ArticulationPattern.ALL_STACCATO))
        assertEquals(1, store.completedArticulationsCount(Tonic.DO_NATURAL, ModeType.IONIAN))
        assertFalse(store.isModeFullyCompleted(Tonic.DO_NATURAL, ModeType.IONIAN))

        // Mark remaining 7 articulations
        for (art in ArticulationPattern.values()) {
            store.markCompleted(Tonic.DO_NATURAL, ModeType.IONIAN, art)
        }
        assertEquals(8, store.completedArticulationsCount(Tonic.DO_NATURAL, ModeType.IONIAN))
        assertTrue(store.isModeFullyCompleted(Tonic.DO_NATURAL, ModeType.IONIAN))
    }

    @Test
    fun testToggleAndUnmarkCompleted() {
        assertFalse(store.isCompleted(Tonic.SOL, ModeType.MIXOLYDIAN, ArticulationPattern.ALL_SLURRED))
        store.toggleCompleted(Tonic.SOL, ModeType.MIXOLYDIAN, ArticulationPattern.ALL_SLURRED)
        assertTrue(store.isCompleted(Tonic.SOL, ModeType.MIXOLYDIAN, ArticulationPattern.ALL_SLURRED))
        assertEquals(1, store.completedArticulationsCount(Tonic.SOL, ModeType.MIXOLYDIAN))

        store.toggleCompleted(Tonic.SOL, ModeType.MIXOLYDIAN, ArticulationPattern.ALL_SLURRED)
        assertFalse(store.isCompleted(Tonic.SOL, ModeType.MIXOLYDIAN, ArticulationPattern.ALL_SLURRED))
        assertEquals(0, store.completedArticulationsCount(Tonic.SOL, ModeType.MIXOLYDIAN))

        store.markCompleted(Tonic.SOL, ModeType.MIXOLYDIAN, ArticulationPattern.ALL_SLURRED)
        assertTrue(store.isCompleted(Tonic.SOL, ModeType.MIXOLYDIAN, ArticulationPattern.ALL_SLURRED))
        store.unmarkCompleted(Tonic.SOL, ModeType.MIXOLYDIAN, ArticulationPattern.ALL_SLURRED)
        assertFalse(store.isCompleted(Tonic.SOL, ModeType.MIXOLYDIAN, ArticulationPattern.ALL_SLURRED))
    }

    @Test
    fun testTonicMasteryAndProgressionCycles() {
        assertFalse(store.isTonicMastered(Tonic.DO_NATURAL))

        // Master all 7 modes for DO_NATURAL
        for (mode in ModeType.values()) {
            for (art in ArticulationPattern.values()) {
                store.markCompleted(Tonic.DO_NATURAL, mode, art)
            }
        }
        assertTrue(store.isTonicMastered(Tonic.DO_NATURAL))
        assertTrue(store.areAllSevenModesPracticed(Tonic.DO_NATURAL))
        assertEquals(7, store.practicedModesCount(Tonic.DO_NATURAL))
        assertEquals(56, store.totalArticulationsCompleted(Tonic.DO_NATURAL))

        // Next tonic cycling
        val nextTonic = store.nextTonic(Tonic.DO_NATURAL)
        assertEquals(Tonic.DO_SOSTENIDO, nextTonic)

        // Chromatic cycle wraps around: SI_BEMOL -> SI
        val wrapTonic = store.nextTonic(Tonic.SI_BEMOL)
        assertEquals(Tonic.SI, wrapTonic)
    }

    @Test
    fun testResetAllClearsStateAndPreferences() {
        store.markCompleted(Tonic.FA, ModeType.LYDIAN, ArticulationPattern.ALL_SLURRED)
        assertTrue(store.completedArticulationsCount(Tonic.FA, ModeType.LYDIAN) > 0)

        store.resetAll()
        assertEquals(0, store.completedArticulationsCount(Tonic.FA, ModeType.LYDIAN))
        assertNull(store.lastTonic)
        assertNull(store.lastMode)
        assertNull(store.lastArticulation)
        assertEquals(0, store.totalPracticedArticulationsCount)
    }
}
