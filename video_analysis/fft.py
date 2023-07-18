from numpy.fft import rfft, rfftfreq
from csv import reader
import numpy as np
import matplotlib.pyplot as plt

CAMERA_SECONDS_PER_FRAME = 0.033
# CAMERA_SECONDS_PER_FRAME_EPSILON = 0.005

start_frame=1000000000
start_time=100000000.0
end_frame=0
end_time=0.0

x_coodinates = []

with open('./video_analysis/iPhone_data/simple-fetch.csv', "r") as f:
    reader_object = reader(f)

    old_frame = 86 #131
    old_x = 1000000000
    i = 0
    for frame, t, x, _y, _r in reader_object:
        i += 1
        frame = int(frame)
        t = float(t)
        x = float(t)
        start_frame = min(start_frame, frame)
        start_time = min(start_time, t)
        end_frame = frame
        end_time = t

        # 足りないデータは線形補間
        while frame > old_frame + 1:
            old_frame += 1
            old_x = x + (x-old_x)/2.0
            x_coodinates.append(old_x)
            print('no data', old_frame)

        if i < 5000:
            x_coodinates.append(x)
        old_frame = frame
        old_x = x
    f.close()

# フレーム間隔（sec）
CAMERA_SECONDS_PER_FRAME = (end_time - start_time)/float((end_frame - start_frame)*1000)
print(CAMERA_SECONDS_PER_FRAME*1000, "ms")
print(float(end_frame - start_frame)/(end_time - start_time), "Hz")

# x_coodinates = np.array(x_coodinates)
fftResult = rfft(x_coodinates)
# fftResult = [abs(fx.real) for fx in fftResult]
fftResult = np.abs(fftResult)
n = len(x_coodinates)
freq = rfftfreq(n, d=CAMERA_SECONDS_PER_FRAME)
print(n)

# fftResultdB = 10*np.log10(np.abs(fftResult))
# fftResultdB = fftResultdB - max(fftResultdB)

# 直流成分が極端に大きく出たため、そこだけ取り除いた。（前処理不足）
plt.plot(freq[1:100], fftResult[1:100])
# plt.plot(freq, fftResult)
plt.yscale('log')
plt.xlabel("frequency / Hz")
plt.ylabel("amplitude / px")
plt.grid()
plt.show()