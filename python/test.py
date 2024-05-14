#!/bin/python3

from package import *

data = acquire_data()
newData = separate_duplos(data)

lambdaArray = data[1]["λ"]
spectrum = newData[5]["SoFlameWithSlit"][1.0]


get_intensity(spectrum, lambdaArray)
