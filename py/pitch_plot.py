#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np

def get_data(fname):
    with open(fname, "r") as f:
        dat = f.read().split(",")[:-1]

    return np.array(dat, dtype=np.float64)

pitches = get_data("py_pitches.csv")
c_data = get_data("c_pitches.csv")
near_pitches = get_data("near_pitches.csv")

plt.plot(pitches, color="red")
plt.plot(c_data, color="blue")
plt.plot(near_pitches, color="yellow")
plt.legend(['Py', 'C', 'Nearest 12TET'])
plt.ylim(0, 1000)
plt.title("Pitch Detection in C and Python")
plt.xlabel("Sample index")
plt.ylabel("Frequency (Hz)")
plt.show()
plt.grid()
plt.savefig("pitch_plot.png")