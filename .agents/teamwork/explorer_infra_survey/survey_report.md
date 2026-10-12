# FluteModes Ecosistema — Reporte Exhaustivo de Infraestructura (Survey Report)
**Autor:** explorer_infra_survey  
**Fecha:** 2026-10-11T14:10:00Z  
**Versión Objetivo:** v1.5.1 (iOS Build 10, Android versionCode 9, Web v1.5.1)  
**Workspace:** `/Users/sebas/Desktop/partituras`

---

## 1. Resumen Ejecutivo

Este reporte presenta los hallazgos de la auditoría técnica exhaustiva sobre la infraestructura de pruebas unitarias, versionado, compilación, firma digital, despliegue y control de versiones del ecosistema FluteModes.

### Hallazgos Principales:
1. **Suites de Pruebas Unitarias:**
   - **Android:** 25 pruebas unitarias passing (100% éxito) en `./gradlew testDebugUnitTest`. Cubre 84 Modos, E.J. 1, 2, 4, 5, 10, 11 y Reichert R. 1, 2, 4, 5, persistencia (`PracticeStore`), síntesis de audio y localización.
   - **iOS:** La suite `FluteModesTests.swift` **falla al compilar** con 7 errores de compilación de Swift (`** TEST FAILED **`). Además, no tiene pruebas unitarias implementadas para Taffanel & Gaubert E.J. 5, E.J. 10 y E.J. 11. Requiere corrección inmediata antes del despliegue.
2. **Versionado Multiplataforma:**
   - iOS se encuentra actualmente en `1.5.0` (Build `9`). Requiere actualización a `1.5.1` (Build `10`) en `project.pbxproj` y `project.yml`.
   - Android se encuentra actualmente en `versionCode = 8`, `versionName = "1.5.0"`. Requiere actualización a `versionCode = 9`, `versionName = "1.5.1"` en `app/build.gradle.kts`.
   - Web se encuentra actualmente en `v1.5.0` en `docs/index.html`. Requiere actualización a `v1.5.1` y enlace a `FluteModes-v1.5.1-release.apk`.
3. **Android Build & Signing:**
   - El keystore `FluteModesAndroid/app/flutemodes-release.jks` existe, es válido hasta 2054 (Alias: `flutemodes`, clave: `flutemodes2026`).
   - `./gradlew assembleRelease` compila exitosamente en 1s. El APK `app-release.apk` fue verificado con `apksigner` confirmando firma válida bajo esquema V2.
4. **iOS Archive & Upload:**
   - El esquema es `FluteModes`. La firma automática con el Team `QWY6U4KSA6` (Sebastian Gomez) y certificado `Apple Development: Sebastian Gomez (W3XW7Y6ERG)` está activa en el llavero local.
   - El archivo `FluteModes/build/ExportOptions.plist` está configurado para `method: app-store-connect` y `destination: upload`.
   - La compilación `xcodebuild build ... -configuration Release` finalizó con `** BUILD SUCCEEDED **`.
   - La cuenta de App Store Connect está vinculada a Xcode y subió exitosamente el Build 9 hace pocas horas (Adam ID `6808083041`).
5. **Estado de Git:**
   - Rama `main`, sincronizada con `origin/main` (`https://github.com/seagomezar/flutemodes.git`).
   - Árbol limpio de cambios de código (solo `.agents/` no rastreado).
   - Último tag existente: `v1.5.0`.

---

## 2. Auditoría de Suites de Pruebas Unitarias

### 2.1. iOS (`FluteModes/FluteModesTests/FluteModesTests.swift`)

#### Qué está actualmente probado (15 métodos de prueba):
1. `testAll84ModalExercisesGenerateValidAbc`: 672 combinaciones (12 tónicas × 7 modos × 8 articulaciones), cabeceras X:1, M:4/2, L:1/8, Q:1/2=90, 8 compases y barra final `|]`.
2. `testFlutePitchRangeSafety`: Rango de notas flauta entre MIDI 59 (B3) y 98 (D7).
3. `testAll8ArticulationPatternsParenthesesBalanced`: Balance de paréntesis de articulación.
4. `testAccidentalMapDegreesWithinBounds`: Grados modales en rango 0..6 y símbolos ABC válidos.
5. `testAudioSynthesisFrequencies`: Frecuencias matemáticas de afinación A4=440Hz, A3=220Hz, C4=261.625Hz, B3=246.94Hz, C7=2093Hz.
6. `testLocalizationKeyParity`: Alternancia español/inglés.
7. `testKeepScreenAwakeSettingPersistence`: Persistencia de pantalla activa en `UserDefaults`.
8. `testPracticeStoreCompletionAndToggle`: Marcado, toggle y conteo de progreso modal.
9. `testViewModelAdvanceToNextArticulationMarksCompleted`: Avance automático entre articulaciones.
10. `testEJ1AndEJ2AllArticulationsGenerateValidAbc`: 30 compases cromáticos, cabeceras `% EJ1_LEDUC_ART`, `% EJ2_LEDUC_ART`, alteraciones `^^F` y `^B`.
11. `testEJ1AndEJ2PracticeStoreTracking`: Seguimiento de 10 articulaciones de E.J. 1 y E.J. 2.
12. `testEJ4AllSectionsAndArticulationsGenerateValidAbc`: 25 secciones, 8 articulaciones, 128/29 notas MIDI y descenso menor armónico en La menor.
13. `testEJ4PracticeStoreTracking`: Seguimiento de 8 articulaciones de E.J. 4.
14. `testReichertR1ToR5AllSectionsAndArticulationsGenerateValidAbc`: 25 secciones de R. 1 (43 notas), R. 2 (61 notas), R. 4 (61 notas) y R. 5 (91 notas).
15. `testReichertR1ToR5PracticeStoreTracking`: Seguimiento de práctica para R. 1, 2, 4, 5.

#### Qué está faltando en iOS:
1. **Taffanel & Gaubert E.J. 5, E.J. 10 y E.J. 11:** No tienen ninguna prueba unitaria en `FluteModesTests.swift`. Faltan:
   - Verificación de generación ABC y secuencias MIDI para las 12 tonalidades y 10 articulaciones de E.J. 5, E.J. 10 y E.J. 11.
   - Verificación de persistencia y seguimiento en `PracticeStore` para E.J. 5, E.J. 10 y E.J. 11 (`ej5TypeCompletedCount`, `isEJ5TypeFullyCompleted`, etc.).
2. **Defectos Críticos de Compilación en `FluteModesTests.swift` (7 errores):**
   Al ejecutar `xcodebuild test`, el compilador arrojó:
   - **Error 1 (Línea 230):** `Value of type 'EJ4Section' has no member 'shortTitle'`  
     *Causa:* La propiedad en `EJ4Section` (en `ArticulationPattern.swift:290`) es `shortName`, no `shortTitle`.
   - **Errores 2 y 3 (Líneas 296, 297):** `Value of type 'PracticeStore' has no member 'markR1Completed'` y `markR5Completed`  
     *Causa:* En `PracticeStore.swift:273`, la firma es `markEJ5TypeCompleted(art, for: .r1)` y `markEJ5TypeCompleted(art, for: .r5)`.
   - **Errores 4 y 5 (Líneas 300, 301):** `Value of type 'PracticeStore' has no member 'markR2Completed'` y `markR4Completed`  
     *Causa:* En `PracticeStore.swift:184`, la firma es `markEJ4Completed(art, for: .r2)` y `markEJ4Completed(art, for: .r4)`.
   - **Errores 6 y 7 (Líneas 309, 310):** `Value of type 'PracticeStore' has no member 'isR2FullyCompleted'` y `isR4FullyCompleted`  
     *Causa:* En `PracticeStore.swift:180`, el método es `isEJ4TypeFullyCompleted(for: .r2)` e `isEJ4TypeFullyCompleted(for: .r4)`.

#### Cómo ejecutar las pruebas de iOS:
```bash
cd /Users/sebas/Desktop/partituras/FluteModes
xcodebuild test -project FluteModes.xcodeproj -scheme FluteModes -destination 'platform=iOS Simulator,name=iPhone 17'
```
*Simuladores disponibles confirmados:* `iPhone 17` (iOS 26.4 / 26.5), `iPhone 15` (iOS 17.2), `iPad Pro 11-inch (M5)`, `iPad Air (5th generation)`.

---

### 2.2. Android (`FluteModesAndroid/app/src/test/java/com/seagomezar/flutemodes/`)

#### Qué está actualmente probado (25 pruebas unitarias en 4 clases):
1. **`ExerciseGeneratorTest.kt` (10 pruebas):**
   - `testAll84ModalCombinationsGenerateValidAbc` (672 combinaciones).
   - `testFlutePitchRangeSafety` (MIDI 59..98).
   - `testAll8ArticulationPatternsParenthesesBalanced`.
   - `testAccidentalMapDegreesWithinBounds`.
   - `testKeySignaturesValid`.
   - `testEJ1AndEJ2AllArticulationsGenerateValidAbc` (30 compases, ^^F, ^B).
   - `testEJ4AllSectionsAndArticulationsGenerateValidAbc` (25 secciones, La m descenso 80, 77).
   - `testEJ5AllSectionsAndArticulationsGenerateValidAbcAndMidi` (12 secciones, 10 articulaciones).
   - `testEJ10AndEJ11AllSectionsAndArticulationsGenerateValidAbcAndMidi` (12 secciones de EJ10 y EJ11).
   - `testReichertR1R2R4R5AllSectionsAndArticulationsGenerateValidAbcAndMidi` (25 secciones R1, R2, R4, R5).
2. **`PracticeStoreTest.kt` (9 pruebas):**
   - `testKeepScreenAwakeDefaultsToTrue` y actualización.
   - `testMarkCompletedAndArticulationsCounting`.
   - `testToggleAndUnmarkCompleted`.
   - `testTonicMasteryAndProgressionCycles`.
   - `testResetAllClearsStateAndPreferences`.
   - `testEJ1AndEJ2CompletionTracking`.
   - `testEJ4CompletionTracking`.
   - `testEJ5EJ10AndEJ11CompletionTracking`.
   - `testReichertCompletionTracking`.
3. **`AudioSynthesisTest.kt` (3 pruebas):**
   - `testMidiToFrequencyAccurateForFluteRegister`.
   - `testMetronomeDecayEnvelopeMath`.
   - `testScoreBufferGenerationWithoutClipping`.
4. **`LocalizationManagerTest.kt` (3 pruebas):**
   - `testAllKeysHaveValidSpanishAndEnglishTranslations`.
   - `testLanguageToggle`.
   - `testFallbacksForMissingKey`.

#### Cómo ejecutar las pruebas de Android:
```bash
cd /Users/sebas/Desktop/partituras/FluteModesAndroid
./gradlew testDebugUnitTest
```
*Resultado verificado:* `BUILD SUCCESSFUL in 8s`, 25 pruebas, 0 fallos, 100% éxito.  
*Reporte HTML generado en:* `FluteModesAndroid/app/build/reports/tests/testDebugUnitTest/index.html`.

---

## 3. Configuración de Versionado Multiplataforma

| Componente | Archivo | Versión Actual | Versión Objetivo v1.5.1 | Ubicación Exacta |
|---|---|---|---|---|
| **iOS Version** | `FluteModes/project.yml` | `MARKETING_VERSION: "1.5.0"` | `MARKETING_VERSION: "1.5.1"` | Línea 44 |
| **iOS Build** | `FluteModes/project.yml` | `CURRENT_PROJECT_VERSION: "9"` | `CURRENT_PROJECT_VERSION: "10"` | Línea 45 |
| **iOS PBXProj** | `FluteModes/FluteModes.xcodeproj/project.pbxproj` | `MARKETING_VERSION = 1.5.0;`<br>`CURRENT_PROJECT_VERSION = 9;` | `MARKETING_VERSION = 1.5.1;`<br>`CURRENT_PROJECT_VERSION = 10;` | Líneas 502, 509, 522, 529 |
| **Android Version** | `FluteModesAndroid/app/build.gradle.kts` | `versionName = "1.5.0"` | `versionName = "1.5.1"` | Línea 15 |
| **Android Code** | `FluteModesAndroid/app/build.gradle.kts` | `versionCode = 8` | `versionCode = 9` | Línea 14 |
| **Web Enlace** | `docs/index.html` | `downloads/apk/FluteModes-v1.5.0-release.apk` | `downloads/apk/FluteModes-v1.5.1-release.apk` | Línea 799 |
| **Web Texto** | `docs/index.html` | `Descargar APK v1.5.0 (Android)` | `Descargar APK v1.5.1 (Android)` | Línea 801 |

*Nota:* Tras modificar `project.yml`, si se usa `xcodegen` se puede regenerar `FluteModes.xcodeproj`, o alternativamente editar tanto `project.yml` como `project.pbxproj` directamente para garantizar sincronización perfecta.

---

## 4. Infraestructura de Compilación y Firma de Android

### 4.1. Keystore y Configuración de Firma
- **Ruta del Keystore:** `FluteModesAndroid/app/flutemodes-release.jks` (2,768 bytes, PKCS12).
- **Configuración en `app/build.gradle.kts`:**
  ```kotlin
  signingConfigs {
      create("release") {
          storeFile = file("flutemodes-release.jks")
          storePassword = "flutemodes2026"
          keyAlias = "flutemodes"
          keyPassword = "flutemodes2026"
          enableV1Signing = true
          enableV2Signing = true
      }
  }
  buildTypes {
      release {
          isMinifyEnabled = false
          signingConfig = signingConfigs.getByName("release")
          proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
      }
  }
  ```
- **Detalles del Certificado (verificados con `keytool`):**
  - **Alias:** `flutemodes`
  - **Propietario:** `CN=Sebastian Gomez, OU=FluteModes, O=FluteModes, L=Medellin, ST=Antioquia, C=CO`
  - **Vigencia:** 3 de septiembre de 2026 hasta 19 de enero de 2054
  - **Algoritmo:** 2048-bit RSA, SHA384withRSA
  - **Huella SHA256:** `E5:D3:AE:EB:0F:17:35:98:34:98:61:5C:4F:13:1C:6A:D4:C0:19:FB:F2:F8:D9:CC:87:8F:97:A4:31:97:37:11`

### 4.2. Compilación y Destino del APK
- **Comando de Compilación:**
  ```bash
  cd /Users/sebas/Desktop/partituras/FluteModesAndroid
  ./gradlew assembleRelease
  ```
- **Ruta de Salida Generada:**
  `FluteModesAndroid/app/build/outputs/apk/release/app-release.apk`
- **Verificación de Firma:**
  Ejecutado con `/Users/sebas/Library/Android/sdk/build-tools/36.0.0/apksigner verify --verbose`:
  - `Verifies: true`
  - `Verified using v2 scheme (APK Signature Scheme v2): true`
  - `Number of signers: 1`
- **Destino Final Requerido:**
  Copiar a `/Users/sebas/Desktop/partituras/docs/downloads/apk/FluteModes-v1.5.1-release.apk`.

---

## 5. Infraestructura de Archivo y Subida a iOS (TestFlight / App Store)

### 5.1. Esquemas y Configuración de Firma
- **Proyecto Xcode:** `FluteModes.xcodeproj`
- **Esquema:** `FluteModes`
- **Configuración:** `Release`
- **Identidad de Firma en Llavero macOS:**
  `ADD68B794F911954A5DBE23ECE316E4F777E34A5 "Apple Development: Sebastian Gomez (W3XW7Y6ERG)"`
- **Development Team ID:** `QWY6U4KSA6`
- **Estilo de Firma:** Automático (`CODE_SIGN_STYLE = Automatic`), gestionado con perfiles de aprovisionamiento de equipo mediante `-allowProvisioningUpdates`.
- **Verificación de Compilación Release:**
  `xcodebuild build -project FluteModes.xcodeproj -scheme FluteModes -configuration Release -destination 'generic/platform=iOS'` finalizó con `** BUILD SUCCEEDED **` y código de salida 0.

### 5.2. Archivo y Opciones de Exportación
- **Archivo de Opciones Existente:** `FluteModes/build/ExportOptions.plist`
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
  <plist version="1.0">
  <dict>
  	<key>destination</key>
  	<string>upload</string>
  	<key>method</key>
  	<string>app-store-connect</string>
  	<key>signingStyle</key>
  	<string>automatic</string>
  	<key>teamID</key>
  	<string>QWY6U4KSA6</string>
  	<key>stripSwiftSymbols</key>
  	<true/>
  	<key>uploadSymbols</key>
  	<true/>
  </dict>
  </plist>
  ```
- **Historial de Subida Previo (`FluteModes/build/FluteModes.xcarchive/Info.plist`):**
  - **Adam ID de la App:** `6808083041`
  - **Build 9 subido:** `2026-10-11T06:39:01Z` con estado `success` (`Uploaded to Apple`).
  - **Método de autenticación:** Sesión activa de Xcode / Keychain para la cuenta de desarrollador (`seagomezar@gmail.com`).

### 5.3. Comandos Canónicos para v1.5.1 (Build 10)
1. **Generar Archivo (.xcarchive):**
   ```bash
   cd /Users/sebas/Desktop/partituras/FluteModes
   xcodebuild -project FluteModes.xcodeproj \
              -scheme FluteModes \
              -configuration Release \
              -archivePath build/FluteModes.xcarchive \
              clean archive \
              -allowProvisioningUpdates
   ```
2. **Exportar y Subir a App Store Connect / TestFlight:**
   ```bash
   xcodebuild -exportArchive \
              -archivePath build/FluteModes.xcarchive \
              -exportOptionsPlist build/ExportOptions.plist \
              -exportPath build/export \
              -allowProvisioningUpdates
   ```

---

## 6. Estado del Repositorio Git

### 6.1. Inspección de Git
- **Rama Actual:** `main`
- **Sincronización:** `Tu rama está actualizada con 'origin/main'`
- **Remote Origin:** `https://github.com/seagomezar/flutemodes.git`
- **Archivos sin seguimiento:** `.agents/` (directorio de metadatos de agentes, protegido)
- **Árbol de trabajo:** Limpio (0 archivos modificados en el índice de Git al inicio de la inspección).
- **Tags Existentes:**
  - `v1.4.0`
  - `v1.5.0` (commit `c56db36` con fecha Sun Oct 11 01:39:36 2026 -0500)

### 6.2. Procedimiento de Publicación v1.5.1
1. **Staging y Commit:**
   ```bash
   git add FluteModes/project.yml \
           FluteModes/FluteModes.xcodeproj/project.pbxproj \
           FluteModes/FluteModesTests/FluteModesTests.swift \
           FluteModesAndroid/app/build.gradle.kts \
           docs/index.html \
           docs/downloads/apk/FluteModes-v1.5.1-release.apk
   git commit -m "release: v1.5.1 (iOS build 10, Android versionCode 9, Urtext musicological audit parity)"
   ```
2. **Creación de Tag Anotado:**
   ```bash
   git tag -a v1.5.1 -m "v1.5.1: Urtext musicological audit & multiplatform parity release"
   ```
3. **Push a GitHub:**
   ```bash
   git push origin main --tags
   ```

---

## 7. Plan de Acción Recomendado para Implementadores

1. **Reparar y Expandir Pruebas en iOS (`FluteModesTests.swift`):**
   - Reemplazar `sec.shortTitle` por `sec.shortName` en la línea 230.
   - Usar las firmas correctas de `PracticeStore`:
     - `store.markEJ5TypeCompleted(art, for: .r1)` y `.r5`.
     - `store.markEJ4Completed(art, for: .r2)` y `.r4`.
     - `store.isEJ4TypeFullyCompleted(for: .r2)` y `.r4`.
   - Incorporar pruebas para E.J. 5, E.J. 10 y E.J. 11 (tanto de generación ABC/MIDI como de tracking en `PracticeStore`).
   - Validar con `xcodebuild test` pasando con 0 fallos.
2. **Actualizar Versiones:**
   - Subir iOS a 1.5.1 (Build 10) en `project.yml` y `project.pbxproj`.
   - Subir Android a `versionCode = 9`, `versionName = "1.5.1"` en `app/build.gradle.kts`.
   - Actualizar enlace y texto en `docs/index.html`.
3. **Compilar y Desplegar Android:**
   - Ejecutar `./gradlew testDebugUnitTest assembleRelease`.
   - Copiar `app/build/outputs/apk/release/app-release.apk` a `docs/downloads/apk/FluteModes-v1.5.1-release.apk`.
   - Verificar firma con SDK `apksigner`.
4. **Archivar y Subir iOS:**
   - Ejecutar `xcodebuild archive` con `-allowProvisioningUpdates`.
   - Ejecutar `xcodebuild -exportArchive` con `-allowProvisioningUpdates`.
5. **Publicar en Git:**
   - Commit, tag `v1.5.1` y push a `origin main --tags`.
