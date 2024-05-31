#!/bin/python3

from package import *

data = acquire_data()
newData = separate_runs(data)
# print_columnNames(newData)
                            
process_newData(data, newData)
