import json

import numpy as np
from pandas import read_csv
from tqdm import tqdm
from scipy.io import wavfile
from matplotlib import pyplot as plt
from scipy.fft import fftfreq, fft, ifft
import math

def find_nearest(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return array[idx-1]
    else:
        return array[idx]

def ACF(f, W, t, lag):    
    return np.sum(
        f[t : t + W] *
        f[lag + t : lag + t + W]
    )


def DF(f, W, t, lag):
    return ACF(f, W, t, 0)\
        + ACF(f, W, t + lag, 0)\
        - (2 * ACF(f, W, t, lag))


def memo_CMNDF(f, W, t, lag_max):
    running_sum = 0
    vals = []
    for lag in range(0, lag_max):
        if lag == 0:
            vals.append(1)
            running_sum += 0
        else:
            running_sum += DF(f, W, t, lag)
            vals.append(DF(f, W, t, lag) / running_sum * lag)
    return vals


def augmented_detect_pitch_CMNDF(f, W, t, sample_rate, bounds, thresh=0.1):  # Also uses memoization
    CMNDF_vals = memo_CMNDF(f, W, t, bounds[-1])[bounds[0]:]

    sample = None
    for i, val in enumerate(CMNDF_vals):
        if val < thresh:
            sample = i + bounds[0]
            break
    if sample is None:
        sample = np.argmin(CMNDF_vals) + bounds[0]
    return sample_rate / (sample + 1)

def detect_main():
    twelve_tet = 440*np.power(2, (1/12)*np.linspace(-54,53,108))
    sample_rate, data = wavfile.read("demo.wav")
    data = data.astype(np.float64)[0:440999] #convert to np.float64 and cut to 10 seconds long
    #window_size = int(5 / 441 * 44100)
    #bounds = [20, 1001]
    window_size = 250
    n = data.shape[0] // (window_size+1)
    # the maximum upper bound is approx data.shape[0]-window_size*n
    bounds = [20, (data.shape[0]-window_size*n)//2]

    with open('vals.txt', 'w') as f:
        #np.savetxt(f, data[:, 0], fmt="")
        for i in data[:, 0]:
            f.write(str(i) + ",")

    print(f"Hyperparams:\nW={window_size}\nbounds={bounds}\nNUM={data.shape[0]//(window_size+1)}")
    pitches = []
    # this is quite literally decimation
    print("Pitch detection:")
    for i in tqdm(range(n)):
        p = augmented_detect_pitch_CMNDF(
                data,
                window_size,
                i * window_size,
                sample_rate,
                bounds
            )
        pitches.append(p)

    near_pitches = np.zeros((n,))
    start = 1
    print("Generating \"nearest pitches\" ...")
    for i in tqdm(range(n)):
        if abs(1200*math.log2(pitches[i]/start))>100: # if the pitch varies no more than a semitone, dont change the nearest pitch
            start = pitches[i]
        near_pitches[i] = find_nearest(twelve_tet, start)

    with open("py_pitches.csv", "w+") as f:
        for p in pitches:
            f.write(f"{p},")
    
    with open("near_pitches.csv", "w+") as f:
        for p in near_pitches:
            f.write(f"{p},")

    #c_data = list(read_csv("pitches.csv", dtype=np.float64))
    #with open("pitches.csv", "r") as f:
    #    c_data = f.read().split(",")

    #c_data = np.array(c_data, dtype=np.float64)

    #plt.plot(pitches, color="red")
    #plt.plot(c_data, color="blue")
    #plt.plot(near_pitches, color="yellow")
    #plt.ylim(0, 1000)
    #plt.show()
    #plt.savefig("nearest.png")

    


if __name__ == '__main__':
    detect_main()
