#!/bin/python3

import numpy as np
import pandas as pd
from matplotlib.pyplot import figure, show

def main():
    count = 0
    data = {}
    for measurementNumber in [1, 2, 3, 5, 6, 9, 11]:
        with open("../processed-data/" + str(measurementNumber) + ".txt", "r") as file:
            columnName = file.readline()
            values = np.zeros((3200, 20))
            index = 0
            for line in file:
                if "END OF VALUES" in line:
                    break
                values[index] = float(line[:-1]) # debug maybe we can remove this one
                index += 1

if __name__ == "__main__":
    main()