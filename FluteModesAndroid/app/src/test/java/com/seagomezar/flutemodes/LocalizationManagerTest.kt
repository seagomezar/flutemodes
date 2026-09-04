package com.seagomezar.flutemodes

import android.content.Context
import android.content.ContextWrapper
import android.content.SharedPreferences
import com.seagomezar.flutemodes.model.AppLanguage
import com.seagomezar.flutemodes.model.LocalizationManager
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test

class LocalizationManagerTest {

    private class TestSharedPreferences : SharedPreferences {
        val map = mutableMapOf<String, Any>()
        override fun getAll(): Map<String, *> = map
        override fun getString(key: String?, defValue: String?): String? = map[key] as? String ?: defValue
        override fun getStringSet(key: String?, defValues: Set<String>?): Set<String>? = null
        override fun getInt(key: String?, defValue: Int): Int = 0
        override fun getLong(key: String?, defValue: Long): Long = 0L
        override fun getFloat(key: String?, defValue: Float): Float = 0f
        override fun getBoolean(key: String?, defValue: Boolean): Boolean = false
        override fun contains(key: String?): Boolean = map.containsKey(key)
        override fun registerOnSharedPreferenceChangeListener(listener: SharedPreferences.OnSharedPreferenceChangeListener?) {}
        override fun unregisterOnSharedPreferenceChangeListener(listener: SharedPreferences.OnSharedPreferenceChangeListener?) {}
        override fun edit(): SharedPreferences.Editor = TestEditor(this)

        class TestEditor(private val prefs: TestSharedPreferences) : SharedPreferences.Editor {
            override fun putString(key: String?, value: String?): SharedPreferences.Editor {
                if (key != null && value != null) prefs.map[key] = value
                return this
            }
            override fun putStringSet(key: String?, values: MutableSet<String>?): SharedPreferences.Editor = this
            override fun putInt(key: String?, value: Int): SharedPreferences.Editor = this
            override fun putLong(key: String?, value: Long): SharedPreferences.Editor = this
            override fun putFloat(key: String?, value: Float): SharedPreferences.Editor = this
            override fun putBoolean(key: String?, value: Boolean): SharedPreferences.Editor = this
            override fun remove(key: String?): SharedPreferences.Editor {
                if (key != null) prefs.map.remove(key)
                return this
            }
            override fun clear(): SharedPreferences.Editor {
                prefs.map.clear()
                return this
            }
            override fun commit(): Boolean = true
            override fun apply() {}
        }
    }

    private lateinit var loc: LocalizationManager
    private val testPrefs = TestSharedPreferences()

    @Before
    fun setup() {
        val context = object : ContextWrapper(null) {
            override fun getSharedPreferences(name: String?, mode: Int): SharedPreferences {
                return testPrefs
            }
        }
        loc = LocalizationManager(context)
    }

    @Test
    fun testAllKeysHaveValidSpanishAndEnglishTranslations() {
        val keys = loc.strings.keys
        assertTrue("Localization dictionary must contain keys", keys.isNotEmpty())

        for (key in keys) {
            val (es, en) = loc.strings[key] ?: error("Missing key: $key")
            assertTrue("Spanish translation for '$key' should not be blank", es.isNotBlank())
            assertTrue("English translation for '$key' should not be blank", en.isNotBlank())
        }
    }

    @Test
    fun testLanguageToggle() {
        assertEquals(AppLanguage.SPANISH, loc.currentLanguage)
        val initialEs = loc.t("settings_title")
        assertEquals("Ajustes de Estudio", initialEs)

        loc.toggleLanguage()
        assertEquals(AppLanguage.ENGLISH, loc.currentLanguage)
        val toggledEn = loc.t("settings_title")
        assertEquals("Practice Settings", toggledEn)

        loc.toggleLanguage()
        assertEquals(AppLanguage.SPANISH, loc.currentLanguage)
        assertEquals("Ajustes de Estudio", loc.t("settings_title"))
    }

    @Test
    fun testFallbacksForMissingKey() {
        val unknown = loc.t("non_existent_key_12345")
        assertEquals("non_existent_key_12345", unknown)
    }
}
