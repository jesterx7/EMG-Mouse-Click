import h5py
import matplotlib.pyplot as plt
from FeatureExtraction import FeatureExtract as fe

file    = h5py.File('../Datasets/marcell_sample_02_01.h5', 'r')
data1   = file['00:07:80:4D:2E:9E']['raw']['channel_1'][10000:11000,0]
data2   = file['00:07:80:4D:2E:9E']['raw']['channel_1'][4000:5000,0]

g1		=  plt.figure(1)
plt.ylim(22000, 40000)
plt.plot(data1)
plt.ylabel('mV')
plt.xlabel('freq')
g1.show()

wl_val1  = fe.wavelength(data1)
max_val1 = fe.maxValue(data1)
min_val1 = fe.minValue(data1)
mad_val1 = fe.meanAbsoluteDeviation(data1)
print(wl_val1, max_val1, min_val1, mad_val1)

g2		= plt.figure(2)
plt.ylim(22000, 40000)
plt.plot(data2)
plt.ylabel('mV')
plt.xlabel('freq')
plt.show()
wl_val2  = fe.wavelength(data2)
max_val2 = fe.maxValue(data2)
min_val2 = fe.minValue(data2)
mad_val2 = fe.meanAbsoluteDeviation(data2)
print(wl_val2, max_val2, min_val2, mad_val2)