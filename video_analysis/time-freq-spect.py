# -*- coding: utf-8 -*
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import signal

plt.close("all")

input_file = "./video_analysis/iPhone_data/cycloid-fetch.csv"
framenumber, time, data = np.loadtxt(
    input_file, unpack=True, delimiter=",", usecols=(0, 1, 2)
)


# サンプリング周波数
# fs = (framenumber[-1]-framenumber[0])/(time[-1]-time[0])
# print(fs, 'Hz') # 21.2405442036222257
fs = 59.96
f, t, Sxx = signal.spectrogram(data, fs)  # nperseg=512)
print(Sxx)

plt.figure()
# plt.pcolormesh(t,fftpack.fftshift(f), fftpack.fftshift(Sxx, axes=0), shading='gouraud')
plt.pcolormesh(t, f, Sxx, shading="gouraud")
# plt.xlim([0,500])
plt.xlabel("time [sec]")
plt.ylabel("freqency [Hz]")
cbar = plt.colorbar()  # カラーバー表示のため追加
cbar.ax.set_ylabel("Intensity")  # カラーバーの名称表示のため追加
plt.show()
