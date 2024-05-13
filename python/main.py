#!/bin/python3

from package import *

def main():
    data = acquire_data()
    # newData = separate_duplos(data)
    get_plots(data)
        

if __name__ == "__main__":
    main()
