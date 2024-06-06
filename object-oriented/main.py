#!/bin/python3

from package import * # also imports the capital case ENUMS

def main():
    # plots are plotted in folder "report-plots" #

    processor = DataProcessor() 

    # plot first spectrum where no salt was added to the fire yet for all
    # three duplo runs
    # processor.plot_same_time_triplo_spectra(SODIUM, 1)
    # plot 5th spectrum where the salt is blocking the light
    # processor.plot_same_time_triplo_spectra(SODIUM, 5)

    # processor.plot_mercury_spectra()
    # processor.plot_spectrum(FIRE_ONLY, "fireOnly", 5).




    # Plot count vs time with background sources as horizontal lines
    processor.plot_sodium()
    processor.plot_magnet()
    processor.plot_mercury()
    
if __name__ == "__main__":
    main()


