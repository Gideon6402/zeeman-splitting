#!/bin/python3

from package import *

def main():
    processor = DataProcessor() 
    processor.read_data()
    processor.separate_runs()

    intensities = processor.get_intensities(processor.newData[3]["onlySodiumLamp"])
    standardDevIntensities = np.std(intensities)

    timeArray = 4 * np.arange(len(intensities))

    plt.errorbar(timeArray, intensities, standardDevIntensities, .5)

    plt.show()

    # get_intensity_plot(newData[3]["onlySodiumLamp"], "sodium lamp")

if __name__ == "__main__":
    main()