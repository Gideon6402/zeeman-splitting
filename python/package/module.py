# from .private import _process_file
import matplotlib.pyplot as plt
import numpy as np
import os


PROGRES = 1
IGNORE = 2
LAMBDA_MAX = 894.837
# Y_LIM = 8
debugList = [IGNORE]

def print_dbg(identifier, *args, **kwargs):
    """ prints if first argument is in debugList """
    if identifier in debugList:
        print(*args, **kwargs)
        
def avarage(list):
    return sum(list) / len(list)

def _process_file(data, file, setupNumber):
    line = file.readline()                   # first columnname                
    while (True):                            # iterate over the columns
        columnName = line[:-1]               # cut of the '\n' at the end of the line                  
        if (columnName == ""):               # check end of file (debug lamda)
            break 
                                             # add new column to data
        data[setupNumber][columnName] = np.zeros(4_098) # for some weird reason, 4_096 is not enough
        lineNr = 0
        while (True):                        # iterate till new column name is found
            line = file.readline()    
            try:                             # try to convert into float
                value = float(line)
                lineNr += 1
            except:                   
                break                        # line is non numeric => line is column name
            data[setupNumber][columnName][lineNr] = value   # add value to data
            
# process could fastened by deleting variable columnName

            
def acquire_data():
    """
    Reads data from a series of text files named by number ("1.txt", "2.txt", etc.) in the "../processed-data/" directory.
    Each file is expected to contain multiple sections, each starting with a single line denoting a column name,
    followed by 4096 lines of numerical data. This function reads the first file ("1.txt") and stores the data
    in a dictionary.

    The function is currently configured to only read from "1.txt" for demonstration purposes.

    Returns:
        dict: A nested dictionary where each key is the file name and its value is another dictionary. This nested
              dictionary's keys are the column names found in the file, and its values are numpy arrays of floats
              containing the data from the file.

    Raises:
        IOError: If there is an issue opening or reading the files.
        ValueError: If the data conversion to float fails.

    Example:
        data = acquire_data()
        print(data['1.txt']['SomeColumnName'])  # prints numpy array of data for 'SomeColumnName' in '1.txt'
    
    Notes:
        - The function assumes that each data section in the file has exactly 4096 numerical entries.
        - The function currently does not handle cases where files or expected data formats are missing or incorrect.
        - Debug statements (print) are included and may be removed or commented out in production use.
    """
    data = {}                             
    for setupNumber in [1, 2, 3, 5, 6, 9, 11]: 
        data[setupNumber] = {}                 # add set-up dict to data
        with open("../processed-data/" + str(setupNumber) + ".txt") as file:
            _process_file(data, file, setupNumber)
            
    # separate_duplos(data)
    
    return data
            
                
# debug: don't forget to update the docstring

### structure:
# data[setupNumber][columnName][lineNr]

# where:
# data: one variable to contain all the data of the experiment
# data[setupNumber]: dictionary with:
#                  - keys:     name of spectrum (like background_1)
#                  - values:   numpy array of the spectrum
#                                  last key contains numpy array of the wavelengths
# lineNr: nth entry of the spectrum   

from .module import *
 
def get_duploName_and_Number(columnName):
    if ("background" in columnName):
        duploName, duploNumber, _ = columnName.split("_")
    else:
        duploName, duploNumber = columnName.split("-")
        duploNumber = duploNumber.split("_")[0]
        
    duploNumber = int(duploNumber)
    return duploName, duploNumber
    

def create_duploName_dictionaries(data, newData, setupNumber):
    newData[setupNumber] = {}
    for columnName in data[setupNumber]:
        if "λ" not in columnName: # we'll use the λ of the old data
            try:
                duploName, _ = get_duploName_and_Number(columnName)
                newData[setupNumber][duploName] = {}
            except Exception as e:
                print_dbg(IGNORE, f"Ignoring {setupNumber}: {columnName}")
# Yes we are assigning dictionaries a lot of times but this process doesn't take long anyway
                

def fill_duploName_dictionaries(data, newData, setupNumber):
    for columnName in list(data[setupNumber]):
        if "λ" not in columnName:
            try:
                duploName, duploNumber = get_duploName_and_Number(columnName)
                newData[setupNumber][duploName][duploNumber] = data[setupNumber][columnName]
            except:
                # already printed that we are ignoring this one
                continue
                

def separate_duplos(data):
    newData = {}
    for setupNumber in data:
        create_duploName_dictionaries(data, newData, setupNumber)
        fill_duploName_dictionaries(data, newData, setupNumber)

    return newData



def make_directory(filename):
    if not os.path.isdir(filename):
        os.system(f"mkdir {filename}")

def get_spectra_plot(spectraDictionary, lamdaArray, name):
    print_dbg(1, f"getting  spectra plots    for {name}...")
    plt.title(f"{name}")
    for columnName in spectraDictionary:
        if (columnName != "λ" and columnName != "Raw_E"):
            plt.plot(lamdaArray,
                     spectraDictionary[columnName],
                     label=columnName)
    plt.title(f"Intensity vs wavelength for all runs")
    plt.xlim(0, LAMBDA_MAX)
    plt.xlabel(f"λ")
    plt.ylabel(f"intensity")
    plt.legend()
    make_directory(f"../plots/all-spectra")
    plt.savefig(f"../plots/all-spectra/{name}.png")
    plt.clf() # clear figure
    
def get_spectra_plots(spectraDictionary, lambdaArray, name):
    print_dbg(PROGRES, f"getting all spectra plots for {name}...")
    for columnName in spectraDictionary:
        if (columnName != "λ" and columnName != "Raw_E"):
            plt.plot(lambdaArray,
                     spectraDictionary[columnName])
            plt.title(f"Intensity vs wavelength")
            plt.xlim(580, 600)
            plt.xlabel(f"λ")
            plt.ylabel(f"intensity")
            make_directory(f"../plots/{name}")
            plt.savefig(f"../plots/{name}/{columnName}.png") 
            plt.clf()
            
def get_intensities(spectraDictionary):
    intensities = []
    for spectrumNameOrNumber in spectraDictionary:
        if (spectrumNameOrNumber != "λ" and spectrumNameOrNumber != "Raw_E"): # just in case
            intensity = spectraDictionary[spectrumNameOrNumber].sum()
            intensities.append(intensity)
            
    return intensities

    
    
def get_intensity_plot(spectraDictionary, lambdaArray, dictionaryName):
    print_dbg(PROGRES, f"getting intensities       for {dictionaryName}...")
    
    intensities = get_intensities(spectraDictionary)
    
    plt.plot(range(len(intensities)), intensities)
    plt.title(f"Intensity vs run")
    plt.xlabel(f"run number")
    plt.ylabel(f"intensity")
    make_directory(f"../plots/intensities")
    plt.savefig(f"../plots/intensities/{dictionaryName}.png")
    plt.clf() #clear figure
    
# def plot_intensities():
    

def get_plots(data):
    for setupNumber in data:
        get_spectra_plot(data[setupNumber], setupNumber)
        get_spectra_plots(data[setupNumber], setupNumber)
        get_intensity_plot(data[setupNumber], setupNumber)
        
def get_new_plots(data, newData):
    lambdaArray = data[1]["λ"] # lambda is found all over the place but they should all be the same
    for setupNumber in newData:
        for duploName in newData[setupNumber]:
            spectra = newData[setupNumber][duploName]
            name = str(setupNumber) + duploName
            get_spectra_plot(spectra, lambdaArray, name)
            get_spectra_plots(spectra, lambdaArray, name)
            get_intensity_plot(spectra, lambdaArray, name)

def get_average(dictionary):
    """ Return the average intensity of all spectra in a dictionary """
    sumOfIntensities = 0
    nrOfSpectra = 0
    for spectrumName in dictionary:
        intensity = dictionary[spectrumName].sum()
        sumOfIntensities += intensity
        nrOfSpectra += 1
        
    return sumOfIntensities / nrOfSpectra
    
            
def print_duploNames(newData):
    for setupNumber in newData:
        for duploName in newData[setupNumber]:
            print(f"setup number {setupNumber}, duplo name: {duploName}")

def print_columnNames(data):
    for setupNumber in data:
        for columnName in data[setupNumber]:
            print(f"setup number {setupNumber}, column name: {columnName}")
            
def print_average_intensity_lamp_and_flame(newData):
    """ We want to see whether adding salt to the flame cast a shadow. The first
    measurement always was without salt. Let's get the average of those """
    noSaltSpectra = np.array([newData[5]["SoFlameWithSlit"][1],
                              newData[5]["SoFlameWithSlitTwo"][1],
                              newData[5]["SoFlameWithSlitThree"][1],
                              newData[6]["SodiumWithMagnetic"][1],
                              newData[6]["Two"][1],
                              newData[6]["Three"][1]])
    
    
    noSaltIntensities = [spectrum.sum() for spectrum in noSaltSpectra]
    averageIntensity = sum(noSaltIntensities) / len(noSaltIntensities)
    print(f"Average intensity of sodium vapor lamp and flame: {averageIntensity:.4g}")
    return averageIntensity

@staticmethod 
def plot_experiment(background, fireLight, sodiumLight, sodiumLampAndFlameLight,
                    newData, duploNameList, setupNumber):  
    
    plt.figure(figsize=(8, 6))
    for name in duploNameList:
        intensities = get_intensities(newData[setupNumber][name])
        plt.plot(intensities, label=name, linestyle='-', marker = 'x', linewidth=0.5)
    plt.axhline(background, label="background", color="red")
    plt.axhline(fireLight, label="fire only", color="purple")
    plt.axhline(sodiumLampAndFlameLight, label="sodium lamp and fire together", color="brown")
    
    plt.title("intensity vs run number for all three triplo runs")
    plt.xlabel("run number")
    plt.ylabel(f"intensity (unknown unit)")
    plt.ylim(0, max(intensities)*1.1)
    plt.legend()
    make_directory("../report-plots")
    plt.savefig(f"../report-plots/{setupNumber}: intensity vs run.png")
    plt.clf()

    
        
        
# debug: would be more beautiful to only go once through all setupNumbers
# debug: would be better to change setupNumber into setupNumber
# debug: lambda is getting overwritten a lot of times
# debug: check whether a lambda column are the same
# debug: newData has a lot of empty entries, shouldn't cause to big of a problem
# debug: creating a data class would have been better
# debug: figure out whether y values are intensity or counts
# debug: we could remove the setupNumber of newData

                  