import matplotlib.pyplot as plt
import numpy as np
import os

## contstants
LAMBDA_MAX = 894.837

## Printing options
PROGRES = 1
IGNORE = 2
debugList = [IGNORE]

class DataProcessor:
    def __init__(self):
        self.data = {}
        self.newData = {}
        self.background = None
        self.fireLight = None
        self.sodiumLight = None
        self.sodiumLampAndFlameLight = None

    @staticmethod
    def print_dbg(identifier, *args, **kwargs):
        """ prints if first argument is in debugList """
        if identifier in debugList:
            print(*args, **kwargs)
            


    ## data acquisition
    def _process_file(self, file, setupNumber):
        line = file.readline()                   # first columnname                
        while (True):                            # iterate over the columns
            columnName = line[:-1]               # cut of the '\n' at the end of the
                                                # line                  
            if (columnName == ""):               # check end of file, readline()
                                                # returns "" at end of file
                break 
                                                # add new column to data
            self.data[setupNumber][columnName] = np.zeros(4_098) # for some weird reason,
                                                            # 4_096 is not enough
            lineNr = 0
            while (True):                        # iterate till new column name is
                                                # found
                line = file.readline()    
                try:                             # try to convert into float
                    value = float(line)
                    self.data[setupNumber][columnName][lineNr] = value   # add value to
                                                                    # data       
                    lineNr += 1
                except:                   
                    break           # line is non numeric => line is column name
    # process could fastened by deleting variable columnName
            
    def read_data(self):                             
        for setupNumber in [1, 2, 3, 5, 6, 9, 11]: 
            self.data[setupNumber] = {}                 # add set-up dict to data
            with open("../processed-data/" + str(setupNumber) + ".txt") as file:
                self._process_file(file, setupNumber)                
    # debug: don't forget to update the docstring

    @staticmethod
    def get_duploName_and_Number(columnName):
        if ("background" in columnName):
            duploName, duploNumber, _ = columnName.split("_")
        else:
            duploName, duploNumber = columnName.split("-")
            duploNumber = duploNumber.split("_")[0]
            
        duploNumber = int(duploNumber)
        return duploName, duploNumber
    

    def create_duploName_dictionaries(self, setupNumber):
        self.newData[setupNumber] = {}
        for columnName in self.data[setupNumber]:
            if "λ" not in columnName: # we'll use the λ of the old data
                try:
                    duploName, _ = self.get_duploName_and_Number(columnName)
                    self.newData[setupNumber][duploName] = {}
                except Exception as e:
                    self.print_dbg(IGNORE, f"Ignoring {setupNumber}: {columnName}")
    # Yes we are assigning dictionaries a lot of times but this process doesn't
    # take long anyway
                    
    def fill_duploName_dictionaries(self, setupNumber):
        for columnName in list(self.data[setupNumber]):
            if "λ" not in columnName:
                try:
                    duploName, duploNumber = self.get_duploName_and_Number(columnName)
                    self.newData[setupNumber][duploName][duploNumber] = self.data[setupNumber][columnName]
                except:
                    # already printed that we are ignoring this one
                    continue
                    
    def separate_runs(self):
        for setupNumber in self.data:
            self.create_duploName_dictionaries(self.data, self.newData, setupNumber)
            self.fill_duploName_dictionaries(self.data, self.newData, setupNumber)



    ## utility funcitons
    @staticmethod
    def make_directory(filename):
        if not os.path.isdir(filename):
            os.system(f"mkdir {filename}")

    def print_duploNames(self):
        for setupNumber in self.newData:
            for duploName in self.newData[setupNumber]:
                print(f"{setupNumber}, {duploName}")

    def print_columnNames(self):
        for setupNumber in self.data:
            for columnName in self.data[setupNumber]:
                print(f"{setupNumber}, {columnName}")

    @staticmethod
    def get_average(dictionary):
        """ Return the average intensity of all spectra in a dictionary """
        sumOfIntensities = 0
        nrOfSpectra = 0
        for spectrumName in dictionary:
            intensity = dictionary[spectrumName].sum()
            sumOfIntensities += intensity
            nrOfSpectra += 1
        return sumOfIntensities / nrOfSpectra
    
    def get_sodiumLampAndFlameLight(self):
        """ We want to see whether adding salt to the flame cast a shadow. The first
        measurement always was without salt. Let's get the average of those: """
        noSaltSpectra = np.array([self.newData[5]["SoFlameWithSlit"][1],
                                  self.newData[5]["SoFlameWithSlitTwo"][1],
                                  self.newData[5]["SoFlameWithSlitThree"][1],
                                  self.newData[6]["SodiumWithMagnetic"][1],
                                  self.newData[6]["Two"][1],
                                  self.newData[6]["Three"][1]])
        
        
        noSaltIntensities = [spectrum.sum() for spectrum in noSaltSpectra]
        averageIntensity = sum(noSaltIntensities) / len(noSaltIntensities)
        return averageIntensity    
            
                    
    ## plotting the data     
    @staticmethod
    def get_intensities(spectraDictionary):
        intensities = []
        for spectrumNameOrNumber in spectraDictionary: 
                                                                # just in case
            if (spectrumNameOrNumber != "λ" and spectrumNameOrNumber != "Raw_E"): 
                intensity = spectraDictionary[spectrumNameOrNumber].sum()
                intensities.append(intensity)
        return intensities   

    @staticmethod
    def fix_layout():
        plt.xlabel("run number")
        plt.ylabel("count (unkown scale)")
        plt.ylim(bottom=0)
        plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.subplots_adjust(right=0.7) 

    def plot_sodium(self):  
        runNames = [("SoFlameWithSlit", "run 1"),
                    ("SoFlameWithSlitTwo", "run 2"),
                    ("SoFlameWithSlitThree", "run 3")]
        
        plt.figure(figsize=(10, 6))
        for runName, label in runNames:
            intensities = self.get_intensities(self.newData[5][runName])
            intensityError = np.std(intensities)
            timeArray = 4 * np.arange(len(intensities))
            timeError = .5
            plt.errorbar(timeArray, intensities, intensityError, timeError, label=label, linestyle='-', marker = 'x',
                        linewidth=0.5)
        fireWithSaltIntensities = self.get_intensities(self.newData[11]["fireWithSodium"])
        
        plt.plot(fireWithSaltIntensities, label="flame with salt", linestyle='-',
                marker = 'x', linewidth=0.5)
        plt.axhline(self.sodiumLampAndFlameLight, label="sodium lamp and flame",
                    color="purple")
        plt.axhline(self.background, label="background", color="pink")
        plt.axhline(self.fireLight, label="flame", color="grey")
        plt.axhline(self.sodiumLight, label="lamp", color="brown")
        
        self.fix_layout()
        self.make_directory("../report-plots")
        plt.savefig("../report-plots/5: intensity vs run <new>.png")
        plt.clf()
        
        
    def plot_magnet(self):  
        runNames = ["One", "Two", "Three"]
        
        plt.figure(figsize=(10, 6))
        for index, runName in enumerate(runNames):
            intensities = self.get_intensities(self.newData[6][runName])
            plt.plot(intensities, label=f"run {index + 1}", linestyle='-',
                    marker = 'x', linewidth=0.5)
            
        fireWithSaltIntensities = self.get_intensities(newData[11]["fireWithSodium"])
        plt.plot(fireWithSaltIntensities, label="flame with salt", linestyle='-',
                marker = 'x', linewidth=0.5)
        
        plt.axhline(self.sodiumLampAndFlameLight, label="sodium lamp and flame",
                    color="purple")
        plt.axhline(self.background, label="background", color="pink")
        plt.axhline(self.fireLight, label="flame", color="grey")
        plt.axhline(self.sodiumLight, label="lamp", color="brown")
        
        self.fix_layout()
        self.make_directory("../report-plots")
        plt.savefig(f"../report-plots/6: intensity vs run.png")
        plt.clf()
        
    def plot_mercury(self):  
        runNames = ["fireWithSodium", "two", "third"]
        
        plt.figure(figsize=(10, 6))
        for index, runName in enumerate(runNames):
            intensities = self.get_intensities(self.newData[9][runName])
            plt.plot(intensities, label=f"run {index + 1}", linestyle='-',
                    marker = 'x', linewidth=0.5)
            
        fireWithSaltIntensities = self.get_intensities(newData[11]["fireWithSodium"])
        plt.plot(fireWithSaltIntensities, label="flame with salt", linestyle='-',
                marker = 'x', linewidth=0.5)
        
        plt.axhline(self.background, label="background", color="pink")
        plt.axhline(self.fireLight, label="flame", color="purple")
        
        self.fix_layout()
        self.make_directory("../report-plots")
        plt.savefig(f"../report-plots/9: intensity vs run.png")
        plt.clf()

    ## Functions to inspect data:
    @staticmethod
    def get_spectra_plot(spectraDictionary, lamdaArray, name):
        DataProcessor.print_dbg(1, f"getting  spectra plots    for {name}...")
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
        DataProcessor.make_directory(f"../plots/all-spectra")
        plt.savefig(f"../plots/all-spectra/{name}.png")
        plt.clf() # clear figure
    
    @staticmethod
    def get_spectra_plots(spectraDictionary, lambdaArray, name):
        DataProcessor.print_dbg(PROGRES, f"getting all spectra plots for {name}...")
        for columnName in spectraDictionary:
            if (columnName != "λ" and columnName != "Raw_E"):
                plt.plot(lambdaArray,
                        spectraDictionary[columnName])
                plt.title(f"Intensity vs wavelength")
                plt.xlim(580, 600)
                plt.xlabel(f"λ")
                plt.ylabel(f"intensity")
                DataProcessor.make_directory(f"../plots/{name}")
                plt.savefig(f"../plots/{name}/{columnName}.png") 
                plt.clf()

    @staticmethod       
    def get_intensity_plot(spectraDictionary, label):
        DataProcessor.print_dbg(PROGRES, f"getting intensities       for {label}...")
        
        intensities = DataProcessor.get_intensities(spectraDictionary)
        
        plt.plot(intensities, linestyle='-',
                marker = 'x', linewidth=0.5)
        plt.title(f"Intensity vs run")
        plt.xlabel(f"run number")
        plt.ylabel(f"intensity")
        DataProcessor.make_directory(f"../plots/intensities")
        plt.savefig(f"../plots/intensities/{label}.png")
        plt.show()
        plt.clf() #clear figure

    def process_data(self):
        for setupNumber in self.data:
            self.get_spectra_plot(data[setupNumber], setupNumber)
            self.get_spectra_plots(data[setupNumber], setupNumber)
            self.get_intensity_plot(data[setupNumber], setupNumber)

    def process_newData(self):
        lambdaArray = self.data[1]["λ"] # lambda is found all over the place but they
                                # should all be the same
        for setupNumber in self.newData:
            for duploName in self.newData[setupNumber]:
                spectra = self.newData[setupNumber][duploName]
                name = str(setupNumber) + duploName
                self.get_spectra_plot(spectra, lambdaArray, name)
                self.get_spectra_plots(spectra, lambdaArray, name)
                self.get_intensity_plot(spectra, lambdaArray, name)
            
        
    # debug: would be more beautiful to only go once through all setupNumbers
    # debug: lambda is getting overwritten a lot of times
    # debug: check whether a lambda column are the same
    # debug: creating a data class would have been better
    # debug: figure out whether y values are intensity or counts IMPORTANT
    # debug: we could remove the setupNumber of newData


    ## structure:
    # data[setupNumber][columnName][wavelengthIndex]

    # where:
    # data: one variable to contain all the data of the experiment
    # data[setupNumber]: dictionary with:
    #                  - keys:     name of spectrum (like background_1)
    #                  - values:   numpy array of the spectrum
    #                              last key contains numpy array of the wavelengths
    # lineNr: nth entry of the spectrum  

    # newData[setupNumber][duploName][duploNumber][wavelengthIndex]
