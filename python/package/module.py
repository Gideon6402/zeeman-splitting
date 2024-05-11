# from .private import _process_file
import numpy as np
import matplotlib.pyplot as plt

def _process_file(data, file, setupName):
    line = file.readline()                   # first columnname                
    while (True):                            # iterate over the columns
        columnName = line                  
        if (columnName == ""):               # check end of file (debug lamda)
            break 
                                             # add new column to data
        data[setupName][columnName] = np.zeros(10_000)
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

def get_spectra(data, setupName):
    print(f"Processing {setupName}...")
    plt.title(f"{setupName}")
    for columnName in data[setupName]:
        if ("λ" not in columnName):
            plt.plot(data[setupName]["λ\n"],
                     data[setupName][columnName],
                     label=columnName)
    plt.legend()
    plt.savefig("../plots/" + setupName[0] + "/all-spectra.png")
    

def get_plots(data):
    for setupName in data:
        get_spectra(data, setupName)
        

        
def get_plots_from_one_setup(data, setupName):
    for columnName in data[setupName]:
        print(f"processing {columnName}")
        plt.plot(data[setupName]["λ\n"],
                 data[setupName][columnName])
        plt.ylim(0, 8_000)
        plt.title(columnName)
        plt.savefig(f"../plots/{setupName[0]}/{columnName}.png") 
        plt.clf()
        
def get_intensity_plot(data, setupName):
    intensities = []
    for columnName in data[setupName]:
        if (columnName != "λ\n"):
            intensity = data[setupName][columnName].sum()
            intensities.append(intensity)
    plt.plot(intensities)
    plt.savefig(f"../plots/{setupName[0]}/intensity-vs-time.png")
        
        
                  