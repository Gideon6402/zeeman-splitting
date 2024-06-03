#!/bin/python3

from package import *

processor = DataProcessor()
processor.read_data()
processor.separate_runs()  

lambdaArray = processor.data[1]["λ"]
print(lambdaArray[0])
plt.scatter(range(len(lambdaArray)), lambdaArray)
plt.show()

