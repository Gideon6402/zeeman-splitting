#!/bin/python3

import chardet

def main():
    with open("data/1.txt", "rb") as rawdata:
        result = chardet.detect(rawdata.read(1000))
    
    encoding = result["encoding"]
    print("encoding type: ", encoding)
    
    with open("data/1.txt", "r", encoding="UTF-16") as file:
        for line in file:
            print(line)
            
    
if __name__ == "__main__":
    main()