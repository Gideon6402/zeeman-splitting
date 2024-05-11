import numpy as np

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
    # for setupNr in [1, 2, 3, 5, 6, 9, 11]:  # number of data files
    for setupNr in [1]:  # number of data files
        setupName = str(setupNr) + ".txt"
        data[setupName] = {}
        with open("../processed-data/" + setupName) as file:
            endOfFile = False
            while (not endOfFile):
                columnName = file.readline()
                if (columnName == ""):  # readline() returns empy string at the end of file
                    endOfFile = True
                print(columnName) # debug
                data[setupName][columnName] = np.zeros(4096)
                for lineNr in range(4096):
                    line = file.readline()
                    try:
                        value = float(line)
                    except:
                        print(f"{line} cannot be converted to a float")
                        break
                    data[setupName][columnName][lineNr] = value
                junk = file.readline()  # we don't need this line
                
# debug: don't forget to update the docstring
                
            