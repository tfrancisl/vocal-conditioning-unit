#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np

with open("pitches.csv", "r") as f:
    c_data = f.read().split(",")

c_data = np.array(c_data, dtype=np.float64)

print(c_data[0])
plt.plot(c_data[0:20])
plt.show()
plt.savefig("test.png")