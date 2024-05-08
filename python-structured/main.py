#!/bin/python3

data = {}

def get_run(file):
    columnName = file.readline()
    for lineNr in range(4096):
        

def get_triplo_run_dictionary_from(file):
    dictionary = {}
    dictionary["run1"] = get_run(file)
    dictionary["run2"] = get_run(file)
    dictionary["run3"] = get_run(file)

def acquire_data():
    dataFileNames = get_data_file_names()
    for dataFileName in dataFileNames:
        with open(dataFileName) as file:
            triploRunsDictionary = get_triplo_run_dictionary_from(file)
            add_to_data(triploRunsDictionary)

def main():
    global data
    
    
        
            
    
if __name__ == "__main__":
    main()
