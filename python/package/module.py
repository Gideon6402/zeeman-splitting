# from .private import _process_file
import matplotlib.pyplot as plt
import numpy as np
import os

# columnames end with a '\n' so it will be cut every now and again with [:-1]

PROGRES = 1
IGNORE = 2
debug_list = [PROGRES]

def print_dbg(identifier, *args, **kwargs):
    if identifier in debug_list:
        print(*args, **kwargs)

def _process_file(data, file, setupNumber):
    line = file.readline()                   # first columnname                
    while (True):                            # iterate over the columns
        columnName = line                  
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

def create_duploName_dictionaries(data, newData, setupNumber):
    newData[setupNumber] = {}
    for columnName in data[setupNumber]:
        if ("background" in columnName):
            separator = "_"
        else:
            separator = "-"
        duploName = columnName.split(separator)[0]
        newData[setupNumber][duploName] = {}
        
def add_lambdas(newData, data):
    for setupNumber in newData:
        for duploName in newData[setupNumber]:
            newData[setupNumber][duploName]["λ\n"] = data[1]["λ\n"]
                
        
def fill_duploName_dictionaries(data, newData, setupNumber):
    for columnName in list(data[setupNumber]):
        try:
            if ("background" in columnName):
                ## splitting up e.g. background_1_E
                duploName, duploNumber, _ = columnName.split("_") 
                duploNumber = float(duploNumber)
                newData[setupNumber][duploName][duploNumber] = data[setupNumber][columnName]
            else:
                ## splitting up e.g. fireOnly-10_E
                duploName, duploNumber = columnName.split("-")
                duploNumber = float(duploNumber.split("_")[0]) # remove the _E at the end of the column name
                newData[setupNumber][duploName][duploNumber] = data[setupNumber][columnName]
        except Exception as e:
            print_dbg(IGNORE, f"Ignoring {columnName[:-1]}")
    add_lambdas(newData, data)

def separate_duplos(data):
    newData = {}
    for setupNumber in data:
        create_duploName_dictionaries(data, newData, setupNumber)
        fill_duploName_dictionaries(data, newData, setupNumber)

    return newData



def mkdir(filename):
    if not os.path.isdir(filename):
        os.system(f"mkdir {filename}")

def get_spectra_plot(spectraDictionary, name):
    print_dbg(1, f"getting  spectra plots    for {name}...")
    plt.title(f"{name}")
    for columnName in spectraDictionary:
        if (columnName != "λ\n" and columnName != "Raw_E\n"):
            plt.plot(spectraDictionary["λ\n"],
                     spectraDictionary[columnName],
                     label=columnName)
    plt.legend()
    mkdir(f"../plots/all-spectra")
    plt.savefig(f"../plots/all-spectra/{name}.png")
    plt.clf() # clear figure
    
def get_spectra_plots(spectraDictionary, setupNumber):
    print_dbg(PROGRES, f"getting all spectra plots for {setupNumber}...")
    for columnName in spectraDictionary:
        if (columnName != "λ\n" and columnName != "Raw_E\n"):
            plt.plot(spectraDictionary["λ\n"],
                    spectraDictionary[columnName])
            plt.ylim(0, 8_000)
            plt.title(columnName)
            mkdir(f"../plots/{setupNumber}")
            plt.savefig(f"../plots/{setupNumber}/{columnName}.png") 
            plt.clf()
    
def get_intensity(spectraDictionary, setupNumber):
    print_dbg(PROGRES, f"getting intensities       for {setupNumber}...")
    intensities = []
    for columnName in spectraDictionary:
        if (columnName != "λ\n" and columnName != "Raw_E\n"):
            intensity = spectraDictionary[columnName].sum()
            intensities.append(intensity)
    plt.plot(intensities)
    mkdir(f"../plots/intensities")
    plt.savefig(f"../plots/intensities/{setupNumber}.png")
    plt.clf() #clear figure

def get_plots(data):
    for setupNumber in data:
        get_spectra_plot(data[setupNumber], setupNumber)
        get_spectra_plots(data[setupNumber], setupNumber)
        get_intensity(data[setupNumber], setupNumber)
        
def get_new_plots(newData):
    for setupNumber in newData:
        for duploName in newData[setupNumber]:
            spectra = newData[setupNumber][duploName]
            name = str(setupNumber) + duploName
            get_spectra_plot(spectra, name)
            get_spectra_plots(spectra, name)
            get_intensity(spectra, name)
            
def print_columnNames(data):
    for setupNumber in data:
        for columnName in data[setupNumber]:
            print(f"setup number {setupNumber}, column name: {columnName}")
        
        
# debug: would be more beautiful to only go once through all setupNumbers
# debug: would be better to change setupNumber into setupNumber
# debug: lambda is getting overwritten a lot of times
# debug: check whether a lambda column are the same
# debug: newData has a lot of empty entries, shouldn't cause to big of a problem
                  