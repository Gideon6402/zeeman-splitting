#!/bin/python3

### Saves all spectra in report-plots/spectra ###

from dataprocessor import *

obj = DataProcessor()

# obj.make_directory(f"../report-plots/spectra/")
# obj.make_directory(f"../report-plots/spectra/1/")
# obj.make_directory(f"../report-plots/spectra/1/background/")

for setupNr in obj.newData:
    for name in obj.newData[setupNr]:
        for number in obj.newData[setupNr][name]:
            obj.plot_spectrum(setupNr, name, number)

