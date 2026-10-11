"""
Test Helpers and Opaque-Box Utilities for FluteModes E2E Test Suite.

Provides independent, specification-derived validation functions for:
- ABC notation parsing, tokenization, and note counting
- Pitch extraction and MIDI mapping (flute register B3=59 .. D7=98)
- Mathematical frequency calculation (A4 = 440 Hz)
- Audio duration and triplet timing derivation
- Score template DOM and JavaScript engine inspection
- Web portal link and asset verification
"""

import os
import re
import math
import json
from pathlib import Path

# Workspace root
WORKSPACE_ROOT = Path("/Users/sebas/Desktop/partituras")

# Standard Flute Register
FLUTE_MIN_MIDI = 59  # B3 (B-footjoint)
FLUTE_MAX_MIDI = 98  # D7 (Standard modern flute ceiling)

# Standard Note to Pitch Offset within Octave
NOTE_OFFSETS = {
    "C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11,
    "c": 12, "d": 14, "e": 16, "f": 17, "g": 19, "a": 21, "b": 23
}


def midi_to_frequency(midi: float) -> float:
    """Derive standard equal-tempered frequency from MIDI note number (A4 = 440 Hz)."""
    return 440.0 * (2.0 ** ((midi - 69.0) / 12.0))


def frequency_to_midi(freq: float) -> float:
    """Derive MIDI note number from frequency."""
    if freq <= 0:
        return 0.0
    return 69.0 + 12.0 * math.log2(freq / 440.0)


def calculate_note_duration(tempo_bpm: int, subdivision: int = 4, is_triplet: bool = False) -> float:
    """
    Calculate note duration in seconds.
    - Quarter note (beat): 60.0 / BPM
    - Regular sixteenth note: (60.0 / BPM) / 4.0
    - Sixteenth-note triplet: (60.0 / BPM) / 6.0
    """
    beat_sec = 60.0 / float(tempo_bpm)
    divisor = 6.0 if is_triplet else float(subdivision)
    return beat_sec / divisor


def is_flute_pitch_in_range(midi: int, allow_b_foot: bool = True) -> bool:
    """Check if MIDI note is within standard flute range (B3..D7 or C4..D7)."""
    min_pitch = FLUTE_MIN_MIDI if allow_b_foot else 60
    return min_pitch <= midi <= FLUTE_MAX_MIDI


def parse_abc_headers(abc_text: str) -> dict:
    """Extract standard ABC headers from ABC notation string."""
    headers = {}
    for line in abc_text.splitlines():
        line = line.strip()
        if re.match(r"^[A-Z]:", line):
            key = line[0]
            val = line[2:].strip()
            headers[key] = val
    return headers


def clean_abc_score_body(abc_text: str) -> str:
    """
    Extract the clean musical body of an ABC score, stripping headers,
    comments (including inline % comments), text annotations, and bracketed directives like [V:1 stem=down].
    """
    lines = abc_text.splitlines()
    body_lines = []
    in_header = True
    for line in lines:
        line = line.strip()
        if in_header:
            if re.match(r"^[A-Z]:", line) or line.startswith("%%") or line.startswith("%"):
                continue
            else:
                in_header = False
        # Strip comments
        line = line.split("%")[0].strip()
        if not line:
            continue
        # Also skip any inline header re-declarations
        if re.match(r"^[A-Z]:", line):
            continue
        body_lines.append(line)

    body = " ".join(body_lines)
    # Remove text annotations in quotes like "^8va" or "^Reprise à l'octave"
    body = re.sub(r'"[^"]*"', '', body)
    # Remove bracketed inline directives like [V:1 stem=down], [K:C], etc.
    body = re.sub(r'\[[A-Za-z]:[^\]]*\]', '', body)
    return body


def count_abc_notes_in_body(abc_text: str) -> int:
    """
    Count musical note events in an ABC score body, ignoring rests, bar lines, and annotations.
    Recognizes ABC note pitches [A-Ga-g] with optional accidentals (^, _, =) and octave marks (,, ',).
    """
    body = clean_abc_score_body(abc_text)
    # Match note patterns: optional accidental (^, ^^, _, __, =), letter [A-Ga-g], optional octave (,+ or '+), optional duration digits
    note_pattern = re.compile(r'(\^{1,2}|_{1,2}|=)?[A-Ga-g][,\']*(\d+)?')
    matches = note_pattern.findall(body)
    return len(matches)


def extract_abc_midi_pitches(abc_text: str) -> list:
    """
    Parse an ABC score and map its notes to integer MIDI numbers.
    Assumes standard treble clef (C = C4 / MIDI 60, c = C5 / MIDI 72, C, = C3 / MIDI 48, c' = C6 / MIDI 84).
    """
    body = clean_abc_score_body(abc_text)

    # Tokenize notes
    # Each note has: accidentals, base char, octave modifiers
    token_pattern = re.compile(r'(\^{1,2}|_{1,2}|=)?([A-Ga-g])([,\']*)(\d+)?')
    midi_pitches = []
    for match in token_pattern.finditer(body):
        acc, base, oct_mod, dur = match.groups()
        # Base pitch for C4 = 60
        # Uppercase A-B is A3 (57), B3 (59); C-G is C4 (60) .. G4 (67)
        # In ABC standard:
        # C, D, E, F, G, A, B are in the octave below middle C up to B4
        # Specifically: C = C4 (60), D = D4 (62), E = E4 (64), F = F4 (65), G = G4 (67), A = A4 (69), B = B4 (71)
        # c = C5 (72), d = D5 (74), e = E5 (76), f = F5 (77), g = G5 (79), a = A5 (81), b = B5 (83)
        base_offsets = {
            'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71,
            'c': 72, 'd': 74, 'e': 76, 'f': 77, 'g': 79, 'a': 81, 'b': 83
        }
        pitch = base_offsets[base]
        # Octave modifiers
        if oct_mod:
            for ch in oct_mod:
                if ch == ',':
                    pitch -= 12
                elif ch == "'":
                    pitch += 12
        # Accidentals
        if acc == '^':
            pitch += 1
        elif acc == '^^':
            pitch += 2
        elif acc == '_':
            pitch -= 1
        elif acc == '__':
            pitch -= 2
        # '=' is natural, no offset to base
        midi_pitches.append(pitch)

    return midi_pitches


def load_score_template(platform: str = "ios") -> str:
    """Load score_template.html for iOS or Android."""
    if platform.lower() == "ios":
        path = WORKSPACE_ROOT / "FluteModes" / "FluteModes" / "Resources" / "score_template.html"
    else:
        path = WORKSPACE_ROOT / "FluteModesAndroid" / "app" / "src" / "main" / "assets" / "score_template.html"
    if not path.exists():
        raise FileNotFoundError(f"score_template.html not found at: {path}")
    return path.read_text(encoding="utf-8")


def load_json_file(rel_path: str) -> dict:
    """Load JSON file from repository relative path."""
    path = WORKSPACE_ROOT / rel_path
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found at: {path}")
    return json.loads(path.read_text(encoding="utf-8"))
