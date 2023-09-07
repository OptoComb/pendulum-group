from numpy.fft import rfft, rfftfreq
from csv import reader
import numpy as np
import matplotlib.pyplot as plt

CAMERA_SECONDS_PER_FRAME = 0.033
CAMERA_SECONDS_PER_FRAME_EPSILON = 0.005

x_coodinates = []

with open("./gui/simple-pendulum-fetch.csv", "r") as f:
    reader_object = reader(f)
    old_t = 190.8394623
    old_x = 196.5
    for t, x1 in reader_object:
        t = float(t)
        x1 = float(x1)

        # 足りないデータは線形補間
        while t > (old_t + CAMERA_SECONDS_PER_FRAME + CAMERA_SECONDS_PER_FRAME_EPSILON):
            old_t += CAMERA_SECONDS_PER_FRAME
            old_x = x1 + (x1 - old_x) / ((t - old_t) / CAMERA_SECONDS_PER_FRAME)
            x_coodinates.append(old_x)

        x_coodinates.append(x1)
        old_t = t
        old_x = x1
    f.close()

# x_coodinates = np.array(x_coodinates)
fftResult = rfft(x_coodinates)
n = len(x_coodinates)
freq = rfftfreq(n, d=CAMERA_SECONDS_PER_FRAME)

# 0Hz 成分が極端に大きく出たため、そこだけ取り除いた。
plt.plot(freq[1:], fftResult[1:])
plt.xlabel("frequency / Hz")
plt.ylabel("amplitude / px")
plt.grid()
plt.show()
