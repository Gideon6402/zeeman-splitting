#!/bin/python3

from package import *

data = acquire_data()
newData = separate_duplos(data)
# print_columnNames(newData)
lambdaArray = data[1]["λ"] # lambda is found all over the place but they
                            # should all be the same
                            
get_new_plots(data, newData)
