#!/bin/python3

from package import *

def main():
    data = acquire_data()
    
    # get_plots(data)
    # get_plots_from_one_setup(data, "5.txt")
    get_intensity_plot(data, "5.txt")
        

if __name__ == "__main__":
    main()
