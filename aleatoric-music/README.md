# Aleatoric Music Generator

Name: Arpita Palakshappa Mudegoudar

## Description

This project generates aleatoric music using random song structures, chord loops, keys, tempo and melody notes. The melody is generated using sawtooth waves. The program can either play the song directly or write it to a WAV file.

# Features Implemented
Random song structure selection:
AABB/CC
ABAB/CD
AB/CDDD
Random chord loop assignment
Random key selection between A3 and A4
Random tempo between 80 and 160 BPM
Melody generation using notes from the current chord with high probability
Sawtooth wave synthesis
Direct playback through speakers
WAV file output (48000 Hz, mono, 16-bit)
harmony generation using the --harmony flag

## How to Run

Install dependencies:

pip install numpy scipy sounddevice

## How It Went

The project was successful. The program generates a random song structure, key, tempo, chord progression and melody each time it runs. The generated music can be played directly through the speakers or exported as a WAV file. Testing confirmed that the program produces valid audio output and creates the required ALEATORIC.wav file.

## Future Improvements

Possible future improvements include implementing bass lines, percussion, more advanced rhythm patterns, MIDI output and additional harmony options to make the generated music sound more realistic and varied.

# Files Included
aleatoric.py
README.md
ALEATORIC.wav