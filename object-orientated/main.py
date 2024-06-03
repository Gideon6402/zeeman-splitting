#!/bin/python3

from package import * # also imports the capital case ENUMS

def main():
    # plots are plotted in folder "report-plots" #

    processor = DataProcessor()
    # structure: data[setup number][column name][frequency index]
    # e.g. data[1]["background-1"][1] would be the value of the lowest frequency
    # of the first background measurement that is stored in 1.lab
    processor.read_data()
                            
    # due to the nature of the data, there is no distinction between e.g.
    # firstRun-1 and secondRun-2. This function bundels all spectra with the 
    # same name into a dictionary: firstRun-1 and firsRun-2 etc go into
    # newData[setupNumber]["firstRun"] and secondRun-1 and secondRun-2 etc go 
    # into newData[setupNumber]["secondRun"]
    processor.separate_runs()  

    processor.get_backgrounds()  

    # plot first spectrum where no salt was added to the fire yet for all
    # three duplo runs
    processor.plot_same_time_triplo_spectra(SODIUM, 1)
    # plot 5th spectrum where the salt is blocking the light
    processor.plot_same_time_triplo_spectra(SODIUM, 5)
    for i in range(10):
        processor.plot_spectrum(FIRE_ONLY, "fireOnly", i + 1)




    # Plot count vs time with background sources as horizontal lines
    processor.plot_sodium()
    processor.plot_magnet()
    processor.plot_mercury()
    
if __name__ == "__main__":
    main()


