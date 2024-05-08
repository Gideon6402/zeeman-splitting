#!/bin/python3

import numpy as np
import pandas as pd
from matplotlib.pyplot import figure, show

def main():
    fig = figure()
    
    count = 0
    data = {}
    measurementIndex = 1
    for measurementNumber in [1, 2, 3, 5, 6, 9, 11]:
        with open("../processed-data/" + str(measurementNumber) + ".txt", "r") as file:
            columnName = file.readline()
            values = np.zeros(4096)
            valueIndex = 0
            for index, line in enumerate(file):
                if "END OF VALUES" in line:
                    break
                values[index] = float(line[:-1]) # debug maybe we can remove this one
            frame = fig.add_subplot(7, 1, measurementIndex)
            frame.plot(values)
        measurementIndex += 1
    

    show()


if __name__ == "__main__":
    main()