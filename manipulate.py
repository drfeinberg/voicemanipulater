#!/usr/bin/env python3

import parselmouth

from parselmouth.praat import call


def maniuplatePitch(wav_file, gender, factor, unit):
    sound = parselmouth.Sound(wav_file)
    if gender == "female":
        F0min = 100
        F0max = 500
    elif gender == "male":
        F0min = 60
        F0max = 300
    manipulation = call(sound, "To Manipulation", 0.001, F0min, F0max)
    pitch_tier = call(manipulation, "Extract pitch tier")
    call(pitch_tier, "Shift frequencies", F0min, F0max, factor, unit)
    call([pitch_tier, manipulation], "Replace pitch tier")
    manipulated_sound = call(manipulation, "Get resynthesis (overlap-add)")
    return manipulated_sound


def manipulateFormants(wav_file, gender, factor):
    sound = parselmouth.Sound(wav_file)
    if gender == "female":
        manipulated_sound = call(sound, "Change gender", 60, 300, factor, 0, 1, 1)
    elif gender == "male":
        manipulated_sound = call(sound, "Change gender", 100, 500, factor, 0, 1, 1)
    return manipulated_sound

def manipulatePitchAndFormants(wav_file, gender, pitchFactor, formantFactor):
    sound = parselmouth.Sound(wav_file)
    if gender == "female":
        F0min = 100
        F0max = 500
    elif gender == "male":
        F0min = 60
        F0max = 300
    pitch = call(sound, "To Pitch", 0.0, F0min, F0max)
    medianF0 = call(pitch, "Get median", 0, 0, "Hertz")  # get medianpitch
    pitch_median = medianF0 - pitchFactor
    if gender == "female":
        pitch = call(sound, "To Pitch", 0.0, 100, 500)
        medianF0 = call(pitch, "Get median", 0, 0, "Hertz")  # get medianpitch
        pitch_median = medianF0 - pitchFactor
        manipulated_sound = call(sound, "Change gender", 100, 500, formantFactor, pitch_median, 1, 1)
    elif gender == "male":
        manipulated_sound = call(sound, "Change gender", 60, 300, formantFactor, pitch_median, 1, 1)
    return manipulated_sound