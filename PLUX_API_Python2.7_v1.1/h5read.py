import h5py
import matplotlib.pyplot as plt

file    = h5py.File('marcel-01.h5', 'r')
data    = file['00:07:80:4D:2E:9E']['raw']['channel_1'][8000:12000,0]

#plt.ylim(30000, 40000)
plt.plot(data)
plt.ylabel('freq')
plt.show()
