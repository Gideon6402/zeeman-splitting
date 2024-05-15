#!/bin/python3

from package import *

def main():
    # structure: data[setup number][column name][frequency index]
    # e.g. data[1]["background-1"][1] would be the value of the lowest frequency
    # of the first background measurement that is stored in 1.lab
    data = acquire_data()
                         
    # due to the nature of the data, there is no distinction between e.g.
    # firstRun-1 and secondRun-2. This function bundels all spectra with the 
    # same name into a dictionary: firstRun-1 and firsRun-2 etc go into
    # newData[setupNumber]["firstRun"] and secondRun-1 and secondRun-2 etc go 
    # into newData[setupNumber]["secondRun"]
    newData = separate_duplos(data)
    
    lambdaArray = data[1]["λ"] # lambda is found all over the place but they
                               # should all be the same
                               # debug: maybe remove
    
    # 10 spectra of the background were recorded and saved in a dictionary:
    averageBackgroundLight = get_average(newData[1]["background"])
    print(f"Average intensity from background: {averageBackgroundLight:.4g}")
    
    # dito:
    averageFireLight = get_average(newData[2]["fireOnly"])
    print(f"Average intensity from fire: {averageFireLight:.4g}")

    
    # Only 1 spectrum of the lamp light was recorded and this one is saved in
    # a numpy array:
    lampLightSpectrum = data[5]["LampShielded_E"]
    LampLight = lampLightSpectrum.sum()
    print(f"Average intensity from sodium vapor lamp: {LampLight:.4g}")
    
    print_average_intensity_lamp_and_flame(newData)
    
    # Let's plot the real experiment: during the experiment we gave somewhat 
    # weird and inconsistent names to the runs but here they are:
    sodiumNames = ["SoFlameWithSlit", "SoFlameWithSlitTwo", "SoFlameWithSlitThree"]
    sodiumWithMagnetNames = ["SodiumWithMagnetic", "Two", "Three"]
    mercuryNames = ["fireWithSodium", "two", "third"]

    # Let's plot:
    plot_experiment(data, newData, sodiumNames, 5)
    plot_experiment(data, newData, sodiumWithMagnetNames, 6)
    plot_experiment(data, newData, mercuryNames, 9)
    
    
        

if __name__ == "__main__":
    main()
