#!/bin/python3

from package import *

data = acquire_data()
newData = separate_runs(data)

print_duploNames(newData)
# print_columnNames(data)
