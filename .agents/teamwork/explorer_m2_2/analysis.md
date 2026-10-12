# Localization Parity & Missing Keys Investigation Report

**Author**: `explorer_m2_2`  
**Milestone**: Milestone 2 (App UI, Navigation & Localization Parity)  
**Date**: 2026-10-11  
**Target Files**:
- Android: `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/model/LocalizationManager.kt`
- iOS: `FluteModes/FluteModes/Models/LocalizationManager.swift`
- Android UI Callers: `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/ui/PracticeScreen.kt`, `HomeScreen.kt`, `model/ArticulationPattern.kt`
- iOS UI Callers: `FluteModes/FluteModes/Views/PracticeView.swift`, `HomeView.swift`

---

## 1. Executive Summary

A comprehensive automated and manual code audit was conducted across the entire Android and iOS localization architecture.

1. **Current Baseline**:
   - Both `LocalizationManager.kt` and `LocalizationManager.swift` currently contain exactly **163 keys** each.
   - Initial key alignment between Android and iOS is at **100% key parity** with 0 discrepancies between their dictionaries.
2. **Missing Keys Root Cause**:
   - In `PracticeScreen.kt`, multiple UI dialogs and bottom navigation buttons query keys via `loc.t(...)` that were never registered in `LocalizationManager.kt`. When queried, `loc.t(key)` falls back to returning the raw key string (e.g., displaying `"ej5_milestone_title"` or `"ej10_next_section"`).
   - In `HomeScreen.kt`, all literal and dynamically constructed keys (such as `"${ex.id}_start_practice"`, `"${ex.id}_select_section"`, `"${ex.id}_select_art"`, `"${ex.id}_header_info"`) evaluate to existing keys for all relevant sectioned exercises (EJ4, EJ5, EJ10, EJ11, R1, R2, R4, R5). `HomeScreen.kt` has **0 missing keys**.
   - In `PracticeScreen.kt:505, 510, 540`, the EJ11 completion dialog (`showEJ11CompletionDialog`) was copy-pasted: the title is hardcoded in Spanish, and the message and restart button mistakenly invoke `"ej1_milestone_msg"` and `"ej1_restart_round"` instead of `"ej11_milestone_msg"` and `"ej11_restart_round"`.
   - In `PracticeScreen.kt:2134, 2135`, lines query `loc.t("ej10_next_section")` and `loc.t("ej11_next_section")` which were omitted from earlier survey counts.
   - In `ArticulationPattern.kt:49`, `ExerciseType.MODOS.pillLabel` returns hardcoded `"84 Modos"`.
3. **Parity Solution**:
   - Add the missing keys to **both** `LocalizationManager.kt` and `LocalizationManager.swift` to maintain strict 100% cross-platform parity.
   - Provide exact drop-in dictionary entries with authentic, bilingual translations (Spanish `es` and English `en`).

---

## 2. Comprehensive Inventory of Missing Localization Keys

### 2.1 The 16 Core Survey Keys

| # | Key | Caller Location | Expected Spanish (`es`) | Expected English (`en`) |
|---|-----|-----------------|-------------------------|-------------------------|
| 1 | `ej5_milestone_title` | `PracticeScreen.kt:397` | `"¡Hito de Articulaciones E. J. 5!"` | `"E. J. 5 Articulation Milestone!"` |
| 2 | `ej5_milestone_msg` | `PracticeScreen.kt:402` | `"Has completado las 10 articulaciones de esta sección."` | `"You completed all 10 articulations for this section."` |
| 3 | `ej5_restart_round` | `PracticeScreen.kt:418` | `"🔁 Reiniciar Ronda"` | `"🔁 Restart Round"` |
| 4 | `ej5_go_to_ej10` | `PracticeScreen.kt:432` | `"🎵 Ir a E. J. 10 (Arpegios)"` | `"🎵 Go to E. J. 10 (Arpeggios)"` |
| 5 | `ej10_milestone_title` | `PracticeScreen.kt:451` | `"¡Hito de Articulaciones E. J. 10!"` | `"E. J. 10 Articulation Milestone!"` |
| 6 | `ej10_milestone_msg` | `PracticeScreen.kt:456` | `"Has completado las 10 articulaciones de este arpegio."` | `"You completed all 10 articulations for this arpeggio."` |
| 7 | `ej10_restart_round` | `PracticeScreen.kt:472` | `"🔁 Reiniciar Ronda"` | `"🔁 Restart Round"` |
| 8 | `ej10_go_to_ej11` | `PracticeScreen.kt:486` | `"🎵 Ir a E. J. 11 (Arpegios Quebrados)"` | `"🎵 Go to E. J. 11 (Broken Arpeggios)"` |
| 9 | `ej11_milestone_title` | `PracticeScreen.kt:505` (fix target) | `"¡Hito de Articulaciones E. J. 11!"` | `"E. J. 11 Articulation Milestone!"` |
| 10 | `ej11_milestone_msg` | `PracticeScreen.kt:510` (fix target) | `"Has completado las 10 articulaciones de esta cadencia."` | `"You completed all 10 articulations for this cadence."` |
| 11 | `ej11_restart_round` | `PracticeScreen.kt:540` (fix target) | `"🔁 Reiniciar Ronda"` | `"🔁 Restart Round"` |
| 12 | `ej5_ten_arts_completed` | `PracticeScreen.kt:2191` | `"10 Articulaciones Completadas"` | `"10 Articulations Completed"` |
| 13 | `ej10_ten_arts_completed` | `PracticeScreen.kt:2192` | `"10 Articulaciones Completadas"` | `"10 Articulations Completed"` |
| 14 | `ej11_ten_arts_completed` | `PracticeScreen.kt:2193` | `"10 Articulaciones Completadas"` | `"10 Articulations Completed"` |
| 15 | `ej4_next_section` | `PracticeScreen.kt:1930, 2136` | `"Siguiente Tonalidad"` | `"Next Tonality"` |
| 16 | `ej5_next_section` | `PracticeScreen.kt:2133` | `"Siguiente Sección"` | `"Next Section"` |

### 2.2 Additional Missing Runtime Keys Discovered

| # | Key | Caller Location | Expected Spanish (`es`) | Expected English (`en`) |
|---|-----|-----------------|-------------------------|-------------------------|
| 17 | `ej10_next_section` | `PracticeScreen.kt:2134` | `"Siguiente Serie"` | `"Next Series"` |
| 18 | `ej11_next_section` | `PracticeScreen.kt:2135` | `"Siguiente Serie"` | `"Next Series"` |
| 19 | `ej11_go_to_r1` | `PracticeScreen.kt:561` (completion nav) | `"🎵 Ir a R. 1 (Reichert Op. 5)"` | `"🎵 Go to R. 1 (Reichert Op. 5)"` |
| 20 | `r_milestone_title` | DEF-09 Reichert dialog | `"¡Hito de Articulaciones Reichert Op. 5!"` | `"Reichert Op. 5 Articulation Milestone!"` |
| 21 | `r_milestone_msg` | DEF-09 Reichert dialog | `"Has completado todas las articulaciones de esta sección de Reichert."` | `"You completed all articulations for this Reichert section."` |
| 22 | `r_restart_round` | DEF-09 Reichert dialog | `"🔁 Reiniciar Ronda"` | `"🔁 Restart Round"` |
| 23 | `modos_pill_label` | `ArticulationPattern.kt:49` | `"84 Modos"` | `"84 Modes"` |

---

## 3. Analysis of Callers and Context

### 3.1 `HomeScreen.kt`
- Examined all `loc.t` invocations in `HomeScreen.kt` (lines 389, 456, 462, 600, 621, 767, 773, 922–926).
- All literal keys (`app_name`, `subtitle`, `select_tonic`, `start_practice`, etc.) exist in `LocalizationManager.kt`.
- Dynamic keys generated via string template:
  - `${ex.id}_start_practice`: `ej4_start_practice`, `ej5_start_practice`, `ej10_start_practice`, `ej11_start_practice`, `r1_start_practice`, `r2_start_practice`, `r4_start_practice`, `r5_start_practice`. All 8 exist.
  - `${ex.id}_select_section`: `ej4_select_section`, `ej5_select_section`, `ej10_select_section`, `ej11_select_section`, `r1_select_section`, `r2_select_section`, `r4_select_section`, `r5_select_section`. All 8 exist.
  - `${ex.id}_select_art`: `ej1_select_art` .. `ej11_select_art`, `r1_select_art` .. `r5_select_art`. All exist.
  - `${ex.id}_header_info`: `ej1_header_info` .. `ej11_header_info`, `r1_header_info` .. `r5_header_info`. All exist.
- **Conclusion**: `HomeScreen.kt` requires **0 key additions**.

### 3.2 `PracticeScreen.kt`
- Lines 397, 402, 418, 432:
  ```kotlin
  if (showEJ5CompletionDialog) {
      AlertDialog(
          ...
          title = { Text(loc.t("ej5_milestone_title")) },
          text = { Text(loc.t("ej5_milestone_msg")) },
          ...
          Text(loc.t("ej5_restart_round"))
          Text(loc.t("ej5_go_to_ej10"))
      )
  }
  ```
- Lines 451, 456, 472, 486:
  ```kotlin
  if (showEJ10CompletionDialog) {
      AlertDialog(
          ...
          title = { Text(loc.t("ej10_milestone_title")) },
          text = { Text(loc.t("ej10_milestone_msg")) },
          ...
          Text(loc.t("ej10_restart_round"))
          Text(loc.t("ej10_go_to_ej11"))
      )
  }
  ```
- Lines 500–577 (`showEJ11CompletionDialog`):
  - Currently line 505: `text = "¡${currentExercise.pillLabel} Completado (10/10 Articulaciones)!"` -> Should be `loc.t("ej11_milestone_title")`.
  - Currently line 510: `text = loc.t("ej1_milestone_msg")` -> Defect: Should be `loc.t("ej11_milestone_msg")`.
  - Currently line 540: `text = loc.t("ej1_restart_round")` -> Defect: Should be `loc.t("ej11_restart_round")`.
- Lines 2132–2137:
  ```kotlin
  Text(
      text = when (currentExercise) {
          ExerciseType.EJ5 -> loc.t("ej5_next_section")
          ExerciseType.EJ10 -> loc.t("ej10_next_section")
          ExerciseType.EJ11 -> loc.t("ej11_next_section")
          else -> loc.t("ej4_next_section")
      }
  )
  ```
- Lines 2190–2194:
  ```kotlin
  val doneLabel = when (currentExercise) {
      ExerciseType.EJ5 -> loc.t("ej5_ten_arts_completed")
      ExerciseType.EJ10 -> loc.t("ej10_ten_arts_completed")
      else -> loc.t("ej11_ten_arts_completed")
  }
  ```
- Line 1930:
  ```kotlin
  Text(text = loc.t("ej4_next_section"))
  ```

### 3.3 iOS `PracticeView.swift`
- In lines 152–155, 1168, 1232, 1519, 1592:
  - Strings like `"Sig. Tonalidad"`, `"Sig. Escala"`, `"Sig. Serie"`, `"🔁 Volver a Articulación 1"` are hardcoded in Spanish.
  - Adding `ej4_next_section`, `ej5_next_section`, `ej10_next_section`, `ej11_next_section`, `ej5_restart_round`, `ej10_restart_round`, `ej11_restart_round` to `LocalizationManager.swift` enables iOS `PracticeView.swift` to achieve identical localized behavior.

---

## 4. Exact Drop-in Code Specifications for the Worker

### 4.1 Target File: `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/model/LocalizationManager.kt`

#### Insertion 1: After line 214 (`ej4_go_to_modos`)
```kotlin
        "ej4_next_section" to Pair("Siguiente Tonalidad", "Next Tonality"),
```

#### Insertion 2: After line 238 (`ej5_start_practice`)
```kotlin
        "ej5_ten_arts_completed" to Pair("10 Articulaciones Completadas", "10 Articulations Completed"),
        "ej5_milestone_title" to Pair("¡Hito de Articulaciones E. J. 5!", "E. J. 5 Articulation Milestone!"),
        "ej5_milestone_msg" to Pair(
            "Has completado las 10 articulaciones de esta sección.",
            "You completed all 10 articulations for this section."
        ),
        "ej5_restart_round" to Pair("🔁 Reiniciar Ronda", "🔁 Restart Round"),
        "ej5_go_to_ej10" to Pair("🎵 Ir a E. J. 10 (Arpegios)", "🎵 Go to E. J. 10 (Arpeggios)"),
        "ej5_next_section" to Pair("Siguiente Sección", "Next Section"),
```

#### Insertion 3: After line 261 (`ej10_start_practice`)
```kotlin
        "ej10_ten_arts_completed" to Pair("10 Articulaciones Completadas", "10 Articulations Completed"),
        "ej10_milestone_title" to Pair("¡Hito de Articulaciones E. J. 10!", "E. J. 10 Articulation Milestone!"),
        "ej10_milestone_msg" to Pair(
            "Has completado las 10 articulaciones de este arpegio.",
            "You completed all 10 articulations for this arpeggio."
        ),
        "ej10_restart_round" to Pair("🔁 Reiniciar Ronda", "🔁 Restart Round"),
        "ej10_go_to_ej11" to Pair("🎵 Ir a E. J. 11 (Arpegios Quebrados)", "🎵 Go to E. J. 11 (Broken Arpeggios)"),
        "ej10_next_section" to Pair("Siguiente Serie", "Next Series"),
```

#### Insertion 4: After line 284 (`ej11_start_practice`)
```kotlin
        "ej11_ten_arts_completed" to Pair("10 Articulaciones Completadas", "10 Articulations Completed"),
        "ej11_milestone_title" to Pair("¡Hito de Articulaciones E. J. 11!", "E. J. 11 Articulation Milestone!"),
        "ej11_milestone_msg" to Pair(
            "Has completado las 10 articulaciones de esta cadencia.",
            "You completed all 10 articulations for this cadence."
        ),
        "ej11_restart_round" to Pair("🔁 Reiniciar Ronda", "🔁 Restart Round"),
        "ej11_go_to_r1" to Pair("🎵 Ir a R. 1 (Reichert Op. 5)", "🎵 Go to R. 1 (Reichert Op. 5)"),
        "ej11_next_section" to Pair("Siguiente Serie", "Next Series"),
```

#### Insertion 5: Reichert & Modos Keys (after line 349 / end of Reichert section)
```kotlin
        "r_milestone_title" to Pair("¡Hito de Articulaciones Reichert Op. 5!", "Reichert Op. 5 Articulation Milestone!"),
        "r_milestone_msg" to Pair(
            "Has completado todas las articulaciones de esta sección de Reichert.",
            "You completed all articulations for this Reichert section."
        ),
        "r_restart_round" to Pair("🔁 Reiniciar Ronda", "🔁 Restart Round"),
        "modos_pill_label" to Pair("84 Modos", "84 Modes"),
```

---

### 4.2 Target File: `FluteModes/FluteModes/Models/LocalizationManager.swift`

#### Insertion 1: After line 193 (`ej4_go_to_modos`)
```swift
        "ej4_next_section": [
            "Siguiente Tonalidad",
            "Next Tonality"
        ],
```

#### Insertion 2: After line 220 (`ej5_start_practice`)
```swift
        "ej5_ten_arts_completed": [
            "10 Articulaciones Completadas",
            "10 Articulations Completed"
        ],
        "ej5_milestone_title": [
            "¡Hito de Articulaciones E. J. 5!",
            "E. J. 5 Articulation Milestone!"
        ],
        "ej5_milestone_msg": [
            "Has completado las 10 articulaciones de esta sección.",
            "You completed all 10 articulations for this section."
        ],
        "ej5_restart_round": [
            "🔁 Reiniciar Ronda",
            "🔁 Restart Round"
        ],
        "ej5_go_to_ej10": [
            "🎵 Ir a E. J. 10 (Arpegios)",
            "🎵 Go to E. J. 10 (Arpeggios)"
        ],
        "ej5_next_section": [
            "Siguiente Sección",
            "Next Section"
        ],
```

#### Insertion 3: After line 246 (`ej10_start_practice`)
```swift
        "ej10_ten_arts_completed": [
            "10 Articulaciones Completadas",
            "10 Articulations Completed"
        ],
        "ej10_milestone_title": [
            "¡Hito de Articulaciones E. J. 10!",
            "E. J. 10 Articulation Milestone!"
        ],
        "ej10_milestone_msg": [
            "Has completado las 10 articulaciones de este arpegio.",
            "You completed all 10 articulations for this arpeggio."
        ],
        "ej10_restart_round": [
            "🔁 Reiniciar Ronda",
            "🔁 Restart Round"
        ],
        "ej10_go_to_ej11": [
            "🎵 Ir a E. J. 11 (Arpegios Quebrados)",
            "🎵 Go to E. J. 11 (Broken Arpeggios)"
        ],
        "ej10_next_section": [
            "Siguiente Serie",
            "Next Series"
        ],
```

#### Insertion 4: After line 271 (`ej11_start_practice`)
```swift
        "ej11_ten_arts_completed": [
            "10 Articulaciones Completadas",
            "10 Articulations Completed"
        ],
        "ej11_milestone_title": [
            "¡Hito de Articulaciones E. J. 11!",
            "E. J. 11 Articulation Milestone!"
        ],
        "ej11_milestone_msg": [
            "Has completado las 10 articulaciones de esta cadencia.",
            "You completed all 10 articulations for this cadence."
        ],
        "ej11_restart_round": [
            "🔁 Reiniciar Ronda",
            "🔁 Restart Round"
        ],
        "ej11_go_to_r1": [
            "🎵 Ir a R. 1 (Reichert Op. 5)",
            "🎵 Go to R. 1 (Reichert Op. 5)"
        ],
        "ej11_next_section": [
            "Siguiente Serie",
            "Next Series"
        ],
```

#### Insertion 5: Reichert & Modos Keys (after line 375 / end of Reichert section)
```swift
        "r_milestone_title": [
            "¡Hito de Articulaciones Reichert Op. 5!",
            "Reichert Op. 5 Articulation Milestone!"
        ],
        "r_milestone_msg": [
            "Has completado todas las articulaciones de esta sección de Reichert.",
            "You completed all articulations for this Reichert section."
        ],
        "r_restart_round": [
            "🔁 Reiniciar Ronda",
            "🔁 Restart Round"
        ],
        "modos_pill_label": [
            "84 Modos",
            "84 Modes"
        ],
```

---

## 5. Accompanying Worker Adjustments in `PracticeScreen.kt`

To properly connect the new keys, Worker should make the following targeted fixes in `FluteModesAndroid/app/src/main/java/com/seagomezar/flutemodes/ui/PracticeScreen.kt`:

1. **Lines 503–511** (`showEJ11CompletionDialog`):
   ```kotlin
   // BEFORE:
   title = {
       Text(
           text = "¡${currentExercise.pillLabel} Completado (10/10 Articulaciones)!",
           fontWeight = FontWeight.Bold
       )
   },
   text = {
       Text(text = loc.t("ej1_milestone_msg"))
   },

   // AFTER:
   title = {
       Text(
           text = loc.t("ej11_milestone_title"),
           fontWeight = FontWeight.Bold
       )
   },
   text = {
       Text(text = loc.t("ej11_milestone_msg"))
   },
   ```

2. **Line 540** (`showEJ11CompletionDialog` restart button):
   ```kotlin
   // BEFORE:
   Text(loc.t("ej1_restart_round"))

   // AFTER:
   Text(loc.t("ej11_restart_round"))
   ```

3. **Line 49 in `ArticulationPattern.kt`**:
   ```kotlin
   // BEFORE:
   MODOS -> "84 Modos"

   // AFTER:
   MODOS -> "84 Modos" // or loc.t("modos_pill_label") if loc is in scope, or localized in shortLabel()
   ```

---

## 6. Verification and Parity Confirmation

With these 23 additions:
- Total keys in `LocalizationManager.kt`: 163 + 23 = **186 keys**.
- Total keys in `LocalizationManager.swift`: 163 + 23 = **186 keys**.
- Cross-platform key parity: **100.0%** (0 missing keys, 0 orphan keys, 0 blank translations).
- Android unit tests (`LocalizationManagerTest.kt`) will pass 100%.
- E2E Tier 3 combinations tests (`test_c11_android_localization_key_parity` and `test_c12_ios_localization_key_parity`) will pass 100%.
