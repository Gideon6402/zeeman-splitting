#!/bin/python3

from package import *

def main():
    data = acquire_data()
    newData = separate_duplos(data)
    # print_columnNames(newData)
    lambdaArray = data[1]["λ"] # lambda is found all over the place but they should all be the same
    
    averageBackgroundLight = get_average(newData[1]["background"])
    print(f"Average intensity from background: {averageBackgroundLight}")
    
    averageFireLight = get_average(newData[2]["fireOnly"])
    print(f"Average intensity from fire: {averageFireLight}")
    
    # averageLampLight = get_average(data[5]["LampShielded_E"])
    # print(f"Average intensity from sodium vapor lamp: {averageLampLight}")
    
    
    # backgroundValues = []
    # for value in newData[1]["background"]:
    #     backgroundValues.append(value)
    # avarageBackground = avarage(backgroundValues)
    # print(f"Avarage background: {avarageBackground}")
    
    # fireValues = []
    # for value in newData[1]["fireOnly"]:
    #     fireValues.append(value)
    # avarageFire = avarage(fireValues)
    # print(f"Avarage intensity from fire: {avarageFire}")
    
    
    
    # for setupNumber in newData:
    #     for duploName in newData[setupNumber]:
    #         spectra = newData[setupNumber][duploName]
    #         name = str(setupNumber) + duploName
    #         get_spectra_plot(spectra, lambdaArray, name)
    #         get_spectra_plots(spectra, lambdaArray, name)
    #         get_intensity_plots(spectra, lambdaArray, name)
        

if __name__ == "__main__":
    main()
