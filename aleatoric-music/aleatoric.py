import argparse
import random
import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd

SAMPLE_RATE = 48000

SONG_STRUCTURES = ["AABB/CC", "ABAB/CD", "AB/CDDD"]

CHORD_LOOPS = [
    ["I", "IV", "ii", "V"],
    ["I", "vi", "ii", "V"],
    ["I", "iii", "IV", "iv"],
    ["I", "V", "ii", "V"],
    ["I", "vi", "IV", "V"],
    ["IV", "I", "vi", "IV"],
    ["I", "V", "vi", "I"],
    ["I", "IV", "iv", "I"],
    ["IV", "V", "I", "I"],
    ["vi", "IV", "I", "V"],
]

SEMITONES = {
    "I":  [0, 4, 7],
    "ii": [2, 5, 9],
    "iii": [4, 7, 11],
    "IV": [5, 9, 12],
    "iv": [5, 8, 12],
    "V":  [7, 11, 14],
    "vi": [9, 12, 16],
}

MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11, 12]

KEYS = {
    "A3": 220.00,
    "A#3": 233.08,
    "B3": 246.94,
    "C4": 261.63,
    "C#4": 277.18,
    "D4": 293.66,
    "D#4": 311.13,
    "E4": 329.63,
    "F4": 349.23,
    "F#4": 369.99,
    "G4": 392.00,
    "G#4": 415.30,
    "A4": 440.00,
}


def semitone_to_freq(base_freq, semitone):
    return base_freq * (2 ** (semitone / 12))


def sawtooth(freq, duration, volume=0.25):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = 2 * (t * freq - np.floor(0.5 + t * freq))
    return volume * wave


def make_song(args):
    structure = random.choice(SONG_STRUCTURES)
    key_name, base_freq = random.choice(list(KEYS.items()))
    tempo = random.randint(80, 160)

    beat_duration = 60 / tempo
    eighth_duration = beat_duration / 2

    labels = sorted(set(structure.replace("/", "")))
    selected_loops = random.sample(CHORD_LOOPS, len(labels))
    label_to_loop = dict(zip(labels, selected_loops))

    song = []

    print("Song structure:", structure)
    print("Key:", key_name)
    print("Tempo:", tempo)
    print("Chord loops:", label_to_loop)

    for label in structure:
        if label == "/":
            continue

        chord_loop = label_to_loop[label]

        for chord in chord_loop:
            chord_notes = SEMITONES[chord]

            # 8 eighth notes per measure
            for _ in range(8):
                if random.random() < 0.8:
                    note = random.choice(chord_notes)
                else:
                    note = random.choice(MAJOR_SCALE)

                freq = semitone_to_freq(base_freq, note)
                sound = sawtooth(freq, eighth_duration)

                # optional harmony
                if args.harmony:
                    lower_notes = [n for n in chord_notes if n < note]
                    if lower_notes:
                        harmony_note = max(lower_notes)
                        harmony_freq = semitone_to_freq(base_freq, harmony_note)
                        sound += sawtooth(harmony_freq, eighth_duration, 0.15)

                song.append(sound)

    audio = np.concatenate(song)

    # normalize
    audio = audio / np.max(np.abs(audio))
    audio_int16 = np.int16(audio * 32767)

    return audio_int16


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Output WAV filename")
    parser.add_argument("--harmony", action="store_true")
    args = parser.parse_args()

    audio = make_song(args)

    if args.output:
        write(args.output, SAMPLE_RATE, audio)
        print("Wrote", args.output)
    else:
        sd.play(audio, SAMPLE_RATE)
        sd.wait()


if __name__ == "__main__":
    main()