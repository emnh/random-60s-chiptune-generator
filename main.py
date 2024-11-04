#!/usr/bin/env python3

import numpy as np
from scipy.io.wavfile import write
import random

# Define the sample rate and duration
SAMPLE_RATE = 44100  # Standard for audio
DURATION = 60  # Duration in seconds

# Frequencies for some common chiptune scales (C major in this case)
NOTES_FREQ = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]

# Define waveform generation functions
def square_wave(frequency, duration, amplitude=0.5, sample_rate=SAMPLE_RATE):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    return wave

def triangle_wave(frequency, duration, amplitude=0.5, sample_rate=SAMPLE_RATE):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * (2 * np.abs(2 * (frequency * t - np.floor(frequency * t + 0.5))) - 1)
    return wave

def noise(duration, amplitude=0.5, sample_rate=SAMPLE_RATE):
    wave = amplitude * (2 * np.random.rand(int(sample_rate * duration)) - 1)
    return wave

# Randomly choose waveform types and pitches
def generate_random_sequence(duration, sample_rate=SAMPLE_RATE):
    audio_sequence = np.array([], dtype=np.float32)
    time_elapsed = 0
    while time_elapsed < duration:
        wave_type = random.choice(['square', 'triangle', 'noise'])
        frequency = random.choice(NOTES_FREQ)
        note_duration = random.uniform(0.1, 0.5)  # Note duration between 0.1s and 0.5s

        if wave_type == 'square':
            wave = square_wave(frequency, note_duration)
        elif wave_type == 'triangle':
            wave = triangle_wave(frequency, note_duration)
        elif wave_type == 'noise':
            wave = noise(note_duration)

        # Concatenate to the audio sequence
        audio_sequence = np.concatenate((audio_sequence, wave))
        time_elapsed += note_duration

    # Truncate or pad the sequence to exactly the desired duration
    audio_sequence = audio_sequence[:int(sample_rate * duration)]
    return audio_sequence

# Generate the sequence and save it to a file
audio_data = generate_random_sequence(DURATION)
write("chiptune_sequence.wav", SAMPLE_RATE, audio_data.astype(np.float32))
