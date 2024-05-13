# from .private import _process_file
import matplotlib.pyplot as plt
import numpy as np
import os

# columnames end with a '\n' so it will be cut every now and again with [:-1]

PROGRES = 1
IGNORE = 2
debug_list = [IGNORE]

def print_dbg(identifier, *args, **kwargs):
    if identifier in debug_list:
        print(*args, **kwargs)

def _process_file(data, file, setupName):
    line = file.readline()                   # first columnname                
    while (True):                            # iterate over the columns
        columnName = line                  
        if (columnName == ""):               # check end of file (debug lamda)
            break 
                                             # add new column to data
        data[setupName][columnName] = np.zeros(4_098) # for some weird reason, 4_096 is not enough
        lineNr = 0
        while (True):                        # iterate till new column name is found
            line = file.readline()    
            try:                             # try to convert into float
                value = float(line)
                lineNr += 1
            except:                   
                break                        # line is non numeric => line is column name
            data[setupName][columnName][lineNr] = value   # add value to data
            
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
    for fileNr in [1, 2, 3, 5, 6, 9, 11]: 
        setupName = str(fileNr) + ".txt"
        data[setupName] = {}                 # add set-up dict to data
        with open("../processed-data/" + setupName) as file:
            _process_file(data, file, setupName)
            
    # separate_duplos(data)
    
    return data
            
                
# debug: don't forget to update the docstring

### structure:
# data[setupName][columnName][lineNr]

# where:
# data: one variable to contain all the data of the experiment
# data[setupName]: dictionary with:
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
            # print(e)
            print_dbg(IGNORE, f"Ignoring {columnName[:-1]}")
            continue

def separate_duplos(data):
    newData = {}
    for setupNumber in data:
        create_duploName_dictionaries(data, newData, setupNumber)
        fill_duploName_dictionaries(data, newData, setupNumber)

    return newData



def mkdir(filename):
    if not os.path.isdir(filename):
        os.system(f"mkdir {filename}")

def get_spectra_plot(data, setupName):
    print_dbg(1, f"getting  spectra plots    for {setupName}...")
    plt.title(f"{setupName}")
    for columnName in data[setupName]:
        if (columnName != "λ\n" and columnName != "Raw_E\n"):
            plt.plot(data[setupName]["λ\n"],
                     data[setupName][columnName],
                     label=columnName)
    plt.legend()
    plt.savefig(f"../plots/all-spectra/{setupName[0]}.png")
    plt.clf() # clear figure
    
def get_spectra_plots(data, setupName):
    print_dbg(PROGRES, f"getting all spectra plots for {setupName}...")
    for columnName in data[setupName]:
        if (columnName != "λ\n" and columnName != "Raw_E\n"):
            plt.plot(data[setupName]["λ\n"],
                    data[setupName][columnName])
            plt.ylim(0, 8_000)
            plt.title(columnName)
            plt.savefig(f"../plots/{setupName[0]}/{columnName}.png") 
            plt.clf()
    
def get_intensity(data, setupName):
    print_dbg(PROGRES, f"gettting intensities      for {setupName}")
    intensities = []
    for columnName in data[setupName]:
        if (columnName != "λ\n" and columnName != "Raw_E\n"):
            intensity = data[setupName][columnName].sum()
            intensities.append(intensity)
    plt.plot(intensities)
    plt.savefig(f"../plots/intensities/{setupName[0]}.png")
    plt.clf() #clear figure

def get_plots(data):
    mkdir(f"../plots/intensities")
    mkdir(f"../plots/all-spectra")
    for setupName in data:
        setupNumber = setupName.split(".")[0]
        mkdir(f"../plots/{setupNumber}")
        get_spectra_plot(data, setupName)
        get_spectra_plots(data, setupName)
        get_intensity(data, setupName)
            
def print_columnNames(data):
    for setupName in data:
        for columnName in data[setupName]:
            print(columnName[:-1])
        
        
# debug: would be more beautiful to only go once through all setupNames
# debug: would be better to change setupName into setupNumber
# debug: lambda is getting overwritten a lot of times
# debug: check whether a lambda column are the same
                  