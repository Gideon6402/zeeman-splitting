#!/bin/python3

from package import *

processor = DataProcessor() 
processor.read_data()
processor.separate_runs()

processor.print_duploNames()
# print_columnNames(data)
