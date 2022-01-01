import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

x = np.array([1, 2, 3, 3, 7])
y = np.array([1, 2, 2, 2, 2, 2, 2, 4])

a = np.array([1, 2, 2, 2, 3, 3, 3, 5])
b = np.array([1, 2, 2, 2, 2, 3, 3, 4, 3])

distance, path = fastdtw(x, y, dist=euclidean)

print(distance)
print(path)

distance, path = fastdtw(a, b, dist=euclidean)

print(distance)
print(path)

# 5.0p
# [(0, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 5), (3, 6), (4, 7)]