#!/bin/python3

from package import *

data = acquire_data()
plt.plot(data[1]["λ"])
plt.show()