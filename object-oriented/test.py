#!/bin/python3

from package import *

obj = DataProcessor() 

for i in range(3):
    print(obj.newData[SODIUM_MAGNET][obj.triploNames[SODIUM_MAGNET][i]][1].sum())
