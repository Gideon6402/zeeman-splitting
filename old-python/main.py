#!/bin/python3

from package import *

def main():
    # structure: data[setup number][column name][frequency index]
    # e.g. data[1]["background-1"][1] would be the value of the lowest frequency
    # of the first background measurement that is stored in 1.lab
    data = read_data()
                            
    # due to the nature of the data, there is no distinction between e.g.
    # firstRun-1 and secondRun-2. This function bundels all spectra with the 
    # same name into a dictionary: firstRun-1 and firsRun-2 etc go into
    # newData[setupNumber]["firstRun"] and secondRun-1 and secondRun-2 etc go 
    # into newData[setupNumber]["secondRun"]
    newData = separate_runs(data)

    # 10 spectra of the background were recorded and saved in a dictionary:
    background = get_average(newData[1]["background"])
    print(f"Average intensity from background: {background:.4g}")

    # dito:
    fireLight = get_average(newData[2]["fireOnly"])
    print(f"Average intensity from fire: {fireLight:.4g}")


    # Only 1 spectrum of the lamp light was recorded and this one is saved in
    # a numpy array:
    sodiumLightSpectrum = data[5]["LampShielded_E"]
    sodiumLight = sodiumLightSpectrum.sum()
    print(f"Average intensity from sodium vapor lamp: {sodiumLight:.4g}")

    sodiumLampAndFlameLight = get_sodiumLampAndFlameLight(newData)
        

    # Plot count vs time with background sources as horizontal lines
    plot_sodium(background, fireLight, sodiumLight, sodiumLampAndFlameLight,
                newData)
    plot_magnet(background, fireLight, sodiumLight, sodiumLampAndFlameLight,
                newData)
    plot_mercury(background, fireLight, newData)
    
if __name__ == "__main__":
    main()


