import itertools
import numpy as np

times = (5,8,4,3)
array = [[i]*j for i, j in enumerate(times)]
array = np.array(list(itertools.chain.from_iterable(array)))
mean = np.sum(array)/array.size
v = np.sum((array-mean)**2)/array.size
print(v)