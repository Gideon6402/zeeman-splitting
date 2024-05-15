#!/bin/python3

from package import *

data = acquire_data()
newData = separate_duplos(data)

print_duploNames(newData)
# print_columnNames(data)
