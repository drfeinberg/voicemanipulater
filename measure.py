import parselmouth
from parselmouth.praat import call


def measurePitch(voiceID, f0min, f0max, unit):
    sound = parselmouth.Sound(voiceID) # read the sound
    duration = call(sound, "Get total duration") # duration
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max) #create a praat pitch object
    meanF0 = call(pitch, "Get mean", 0, 0, unit) # get mean pitch
    stdevF0 = call(pitch, "Get standard deviation", 0 ,0, unit) # get standard deviation
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, f0min, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer = call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer = call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    return duration, meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, \
           localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer


def measureFormants(sound):
    sound = parselmouth.Sound(sound)  # read the sound
    pointProcess = call(sound, "To PointProcess (periodic, cc)", 75, 500)
    pitch = call(sound, "To Pitch", 0.0, 75, 500)  # check pitch to set formant settings
    meanF0 = call(pitch, "Get mean", 0, 0, "Hertz")  # get mean pitch
    if meanF0 > 150:
        maxFormant = 5500
    else:
        maxFormant = 5000
    formants = call(sound, "To Formant (burg)", 0.0025, 5, maxFormant, 0.025, 50)
    numPoints = call(pointProcess, "Get number of points")

    f1_list = []
    f2_list = []
    f3_list = []
    f4_list = []

    # Measure formants only at glottal pulses
    for point in range(0, numPoints):
        point += 1
        t = call(pointProcess, "Get time from index", point)
        f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        f3 = call(formants, "Get value at time", 3, t, 'Hertz', 'Linear')
        f4 = call(formants, "Get value at time", 4, t, 'Hertz', 'Linear')
        f1_list.append(f1)
        f2_list.append(f2)
        f3_list.append(f3)
        f4_list.append(f4)
        if isinstance(f1, float) == True:
            f1_list.append(f1)
        if isinstance(f2, float) == True:
            f2_list.append(f2)
        if isinstance(f3, float) == True:
            f3_list.append(f3)
        if isinstance(f4, float) == True:
            f4_list.append(f4)
    # calculate mean formants across pulses
    if len(f1_list) > 0:
        f1_mean = sum(f1_list) / len(f1_list)
    else:
        f1_mean = "N/A"
    if len(f2_list) > 0:
        f2_mean = sum(f2_list) / len(f2_list)
    else:
        f2_mean = "N/A"
    if len(f3_list) > 0:
        f3_mean = sum(f3_list) / len(f3_list)
    else:
        f3_mean = "N/A"
    if len(f4_list) > 0:
        f4_mean = sum(f4_list) / len(f4_list)
    else:
        f4_mean = "N/A"

    # calculate median formants across pulses, this is what is used in all subsequent calcualtions
    # you can use mean if you want, just edit the code in the boxes below to replace median with mean

    return f1_mean, f2_mean, f3_mean, f4_mean