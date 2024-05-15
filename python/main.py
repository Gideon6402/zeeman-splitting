#!/bin/python3

from package import *

def main():
    data = acquire_data()
    newData = separate_duplos(data)
    # print_columnNames(newData)
    lambdaArray = data[1]["λ"] # lambda is found all over the place but they
                               # should all be the same
    
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
    
    # We want to see whether adding salt to the flame cast a shadow. The first
    # measurement always was without salt. Let's get the average of those
    
    sodiumNames = ["SoFlameWithSlit", "SoFlameWithSlitTwo", "SoFlameWithSlitThree"]
    sodiumWithMagnetNames = ["SodiumWithMagnetic", "Two", "Three"]
    mercuryNames = ["fireWithSodium", "two", "third"]
    
    noSaltSpectra = np.array([newData[5]["SoFlameWithSlit"][1],
                              newData[5]["SoFlameWithSlitTwo"][1],
                              newData[5]["SoFlameWithSlitThree"][1],
                              newData[6]["SodiumWithMagnetic"][1],
                              newData[6]["Two"][1],
                              newData[6]["Three"][1]])
    
    
    noSaltIntensities = [spectrum.sum() for spectrum in noSaltSpectra]
    averageIntensity = sum(noSaltIntensities) / len(noSaltIntensities)
    print(f"Average intensity of sodium vapor lamp and flame: {averageIntensity:.4g}")
    
    for name in sodiumNames:
        intensities = get_intensities(newData[5][name])
        plt.plot(range(len(intensities), intensities), label=name)
    
    
    
        

if __name__ == "__main__":
    main()
