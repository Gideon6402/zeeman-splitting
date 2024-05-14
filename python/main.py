#!/bin/python3

from package import *

def main():
    data = acquire_data()
    newData = separate_duplos(data)
    # print_columnNames(newData)
    get_new_plots(data, newData)
        

if __name__ == "__main__":
    main()
