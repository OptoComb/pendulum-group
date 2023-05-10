from numpy.fft import fft, fftfreq
from csv import reader
import matplotlib.pyplot as plt

with open(self.csvfile, "w", newline = '') as f:
                writer_object = writer(f)
                writer_object.writerow(columns_name)
                f.close()