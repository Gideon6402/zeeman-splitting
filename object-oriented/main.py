#!/bin/python3

from package import * # also imports the capital case ENUMS

def main():
    processor = DataProcessor() 
    processor.show_table()
    
if __name__ == "__main__":
    main()


