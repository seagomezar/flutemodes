# FluteModes 🎶

> **Estudio Didáctico de Modos Paralelos para Flauta Traversa**  
> *Basado en el canon de Paul Taffanel & Philippe Gaubert (E.J. 4) y el Sistema Paralelo del Maestro.*

[![iOS / iPadOS](https://img.shields.io/badge/Platform-iOS%20%7C%20iPadOS%2017.0%2B-blue?logo=apple)](https://developer.apple.com)
[![SwiftUI](https://img.shields.io/badge/UI-SwiftUI-orange?logo=swift)](https://swift.org)
[![Audio](https://img.shields.io/badge/Audio-AVAudioEngine%20Physical%20Synth-purple)](https://developer.apple.com/documentation/avfaudio)
[![GitHub Pages](https://img.shields.io/badge/Landing%20Page-Live%20on%20GitHub%20Pages-emerald)](https://seagomezar.github.io/flutemodes/)
[![Privacy Compliant](https://img.shields.io/badge/Privacy-100%25%20Apple%20Compliant-success)](https://seagomezar.github.io/flutemodes/privacy.html)

---

## 🌐 Enlaces Oficiales / Official Links

- 🌟 **Sitio Web Oficial & Landing Page:** [https://seagomezar.github.io/flutemodes/](https://seagomezar.github.io/flutemodes/)
- 🔒 **Política de Privacidad (Apple Compliant):** [https://seagomezar.github.io/flutemodes/privacy.html](https://seagomezar.github.io/flutemodes/privacy.html)
- 🤝 **Centro de Soporte y Ayuda:** [https://seagomezar.github.io/flutemodes/support.html](https://seagomezar.github.io/flutemodes/support.html)
- 📘 **Descarga Directa: Método Completo en PDF (36 Págs):** [metodo_completo_modos_flauta.pdf](docs/downloads/pdf/metodo_completo_modos_flauta.pdf)

---

## 🇪🇸 Descripción en Español

**FluteModes** es una aplicación nativa para iPad y un compendio pedagógico diseñado para transformar el estudio técnico de la flauta traversa. Tomando como base la estructura periódica del célebre **Ejercicio Diario N° 4** de Paul Taffanel y Philippe Gaubert (*17 Grands Exercices Journaliers de Mécanisme*), FluteModes aplica el **Sistema Paralelo del Maestro** a lo largo de las 12 notas cromáticas.

### 🌟 Características Principales

1. **84 Modos Paralelos Canónicos (12 Tónicas × 7 Modos):**
   - A diferencia del enfoque relativo tradicional, todos los 7 modos se construyen **a partir de la misma nota tónica fundamental**.
   - **Familia Mayor (Armadura de Tónica Mayor):** Modo Jónico (base mayor), Modo Lidio (cuarta aumentada accidental $\sharp 4$) y Modo Mixolidio (séptima menor accidental $\flat 7$).
   - **Familia Menor (Armadura de Tónica Menor):** Modo Dórico (sexta mayor accidental $\natural 6$), Modo Eólico (menor natural), Modo Frigio (segunda menor accidental $\flat 2$) y Modo Lócrio (segunda menor $\flat 2$ y quinta disminuida $\flat 5$).
2. **Las 8 Fórmulas de Articulación Canónicas:**
   - Toda ligada, Ligado 4 y 4, Ligado 2 picado 2, Picado 1 ligado 2 picado 1, Picado 2 ligado 2, Picado 1 ligado 3, Ligado 3 picado 1 y Toda picada en staccato.
3. **Sintetizador Acústico de Piano de Cola en Swift:**
   - Modelo físico percusivo con ataque de macillo (3 ms), resonancia armónica de cuerdas, batimiento trichord ($\pm 0.35$ Hz) y corte de amortiguación diferenciado entre legato (96%) y staccato (45%).
4. **Metrónomo de Pulso Uniforme:**
   - Pulso rítmico a 1400 Hz sin jerarquías forzadas de tiempo fuerte o débil, favoreciendo la regularidad de dedos y la gestión del aire.
5. **Ambitus Completo (Pata de Si y Pata de Do):**
   - Desde el Si 3 (246.94 Hz, pata de Si) hasta el registro sobreagudo de la cuarta octava (Do 6, Re 6, Mi 6, Fa 6), con 3 octavas completas de tesitura.
6. **Internacionalización Nativa:**
   - Idioma español por defecto con selector dinámico a inglés (`🇪🇸 ES` / `🇬🇧 EN`).
7. **100% Privado y Offline:**
   - Cero recopilación de datos, sin anuncios, sin cuentas; todo el progreso se almacena localmente en el dispositivo.

---

## 🇬🇧 English Overview

**FluteModes** is a native iPad application and pedagogical sheet music compendium that reinvents daily woodwind technique. Adapting the classical periodic phrasing of **Daily Exercise No. 4** by Paul Taffanel & Philippe Gaubert (*17 Grands Exercices Journaliers de Mécanisme*), FluteModes implements the **Maestro's Parallel Modal Routine** across all 12 chromatic tonics.

### 🌟 Key Features

1. **84 Canonical Parallel Modes (12 Tonics × 7 Modes):**
   - Rather than practicing relative modes (which share key signatures), each mode begins from the exact same tonic note.
   - **Major Family (Fixed Major Key Signature):** Ionian (major base), Lydian (augmented fourth accidental $\sharp 4$), Mixolydian (minor seventh accidental $\flat 7$).
   - **Minor Family (Fixed Minor Key Signature):** Dorian (major sixth accidental $\natural 6$), Aeolian (natural minor), Phrygian (minor second accidental $\flat 2$), Locrian (minor second $\flat 2$ & diminished fifth $\flat 5$).
2. **The 8 Classical Articulation Patterns:**
   - All slurred, Slurred 4 & 4, Slur 2 staccato 2, Staccato 1 slur 2 staccato 1, Staccato 2 slur 2, Staccato 1 slur 3, Slur 3 staccato 1, and All staccato.
3. **Acoustic Grand Piano Synthesizer in Pure Swift:**
   - Pure mathematical physical modeling audio engine (`AVAudioEngine`): felt hammer strike impulse, string resonance, unison detuning chorus ($\pm 0.35$ Hz), and damper cutoff tailored to each articulation.
4. **Uniform Beat Metronome:**
   - Clean 1400 Hz percussive click without artificial strong/weak beat differentiation for unbiased finger dexterity.
5. **Full Concert Flute Ambitus (B-foot & C-foot Joints):**
   - Spans from low B3 (246.94 Hz) up to the extreme 4th-octave register (C6, D6, E6, F6), covering 3 full octaves in strict classical symmetry.
6. **Native Internationalization:**
   - Spanish by default with instant English language switcher (`🇪🇸 ES` / `🇬🇧 EN`).
7. **Zero-Tracking & Completely Offline:**
   - No user tracking, no accounts, no internet required. All practice records are saved locally on your device.

---

## 📂 Estructura del Repositorio / Repository Structure

```
flutemodes/
├── FluteModes/                   # Aplicación nativa iOS / iPadOS (Xcode + SwiftUI)
│   ├── App/                      # Ciclo de vida de la app y Info.plist
│   ├── Audio/                    # Sintetizador de Piano y Motor de Metrónomo
│   │   ├── MetronomeEngine.swift
│   │   └── ScoreAudioPlayer.swift
│   ├── Models/                   # Tónicas, Modos, Articulaciones e i18n
│   │   ├── LocalizationManager.swift
│   │   ├── MusicalMode.swift
│   │   ├── Tonic.swift
│   │   ├── ArticulationPattern.swift
│   │   ├── PracticeStore.swift
│   │   └── ExerciseGenerator.swift
│   ├── ViewModels/               # PracticeViewModel y gestión de estado
│   ├── Views/                    # HomeView, PracticeView, ProgressMatrixView, ScoreWebView
│   ├── Resources/                # Catálogo de Assets (AppIcon 1024x1024)
│   └── project.yml               # Configuración XcodeGen reproducible
├── docs/                         # Sitio Web / Landing Page alojada en GitHub Pages
│   ├── index.html                # Landing page super premium con atril interactivo
│   ├── privacy.html              # Política de Privacidad 100% conforme con Apple
│   ├── support.html              # Centro de ayuda, FAQ y soporte técnico
│   ├── app_icon.jpg              # Icono oficial de la aplicación
│   ├── abcjs-basic-min.js        # Motor de renderizado musical ABC en el navegador
│   └── downloads/                # Enlaces de descarga directa de PDFs y ABCs
│       ├── pdf/                  # 12 PDFs individuales + Método Completo (36 Págs)
│       └── abc/                  # 12 Partituras en notación ABC estándar
├── scores/                       # Partituras maestras organizadas
│   ├── pdf/
│   └── abc/
├── generate_parallel_modos.py    # Script generador de las 36 páginas del método
└── README.md                     # Documentación principal bilingüe
```

---

## 🛠️ Compilación y Ejecución / Build Instructions

### Requisitos / Prerequisites
- macOS Sonoma 14+ o macOS Sequoia 15+
- Xcode 15.0 o posterior
- [XcodeGen](https://github.com/yonaskolb/XcodeGen) (`brew install xcodegen`)

### Pasos / Steps
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/seagomezar/flutemodes.git
   cd flutemodes/FluteModes
   ```
2. Generar el proyecto de Xcode con XcodeGen:
   ```bash
   xcodegen generate
   ```
3. Abrir en Xcode:
   ```bash
   open FluteModes.xcodeproj
   ```
4. Seleccionar un simulador de iPad (por ejemplo, **iPad Pro 13-inch M4**) o dispositivo físico y presionar **Run (`⌘ + R`)**.

---

## 📜 Licencia y Créditos / License & Credits

- **Pedagogía Original:** Paul Taffanel & Philippe Gaubert (*17 Grands Exercices Journaliers de Mécanisme*, 1958, Alphonse Leduc / Dominio Público).
- **Adaptación Didáctica de Modos Paralelos:** Inspirado en la metodología pedagógica del Maestro.
- **Desarrollo, Diseño y Síntesis de Audio:** [Sebastián Gómez](https://github.com/seagomezar) (`seagomezar@gmail.com`).

© 2026 Sebastián Gómez. Todos los derechos reservados.
