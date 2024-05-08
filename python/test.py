#!/bin/python3

import matplotlib.pyplot as plt

for measurementNumber in [1, 2, 3, 5, 6, 9, 11]:
    with open("../processed-data/" + str(measurementNumber) + ".txt", "r") as file:
        for line in file:
            if "END OF VALUES" in line:
                column = 