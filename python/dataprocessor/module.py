import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
import time

from .utils import get_variable_name

# formatter to put scientific notation on y-axis
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((0, 0))  # Set the limits for using scientific notation

## contstants
LAMBDA_MIN = 360.127 # minimal wavelength
LAMBDA_MAX = 894.837 # maximal wavelength

## set-up numbers
BACKGROUND = 1
FIRE_ONLY = 2
SODIUM = 5
SODIUM_MAGNET = 6
MERCURY = 9
FIRE_SALT = 11

## printing options
PROGRES = 1
IGNORE = 2
debugList = [IGNORE]

# some stuff to get exponential on y axis
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((0, 0))  # Set the limits for using scientific notation

class DataProcessor:
    def __init__(self):
        self.data = {}
        self.newData = {}
        self.background = None
        self.fireLight = None
        self.sodiumLight = None
        self.sodiumLampAndFlameLight = None
        self.lineStyleKeywords = {"linestyle": "", "marker": '.',
                                   "linewidth": 0.5}
        self.ylabel = "count (a.u.)"
        
        self.triploNames = {}
        self.triploNames[SODIUM] =  [
            "SoFlameWithSlit",
            "SoFlameWithSlitTwo",
            "SoFlameWithSlitThree"
        ]
        self.triploNames[SODIUM_MAGNET] = [
            "One",
            "Two", 
            "Three"
        ]
        self.triploNames[MERCURY] = [
            "fireWithSodium",
            "two", 
            "third"
        ]

        self.means = {}
        self.errors = {}

        
                                     
        # debug
        self.noSaltIntensties = None

        # structure: data[setup number][column name][frequency index]
        # e.g. data[1]["background-1"][1] would be the value of the lowest frequency
        # of the first background measurement that is stored in 1.lab #
        self.read_data()
        # due to the nature of the data, there is no distinction between e.g.
        # firstRun-1 and secondRun-2. This function bundels all spectra with the 
        # same name into a dictionary: firstRun-1 and firsRun-2 etc go into
        # newData[setupNumber]["firstRun"] and secondRun-1 and secondRun-2 etc go 
        # into newData[setupNumber]["secondRun"]
        self.separate_runs()
        self.get_backgrounds()
        self.calculate_results()

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
            self.create_duploName_dictionaries(setupNumber)
            self.fill_duploName_dictionaries(setupNumber)

 

    ## utility funcitons
    @staticmethod
    def make_directory(filename):
        if not os.path.isdir(filename):
            os.system(f"mkdir {filename}")
            DataProcessor.print_dbg(PROGRES, f"mkdir {filename}")

    def print_duploNames(self):
        for setupNumber in self.newData:
            for duploName in self.newData[setupNumber]:
                nrSpectra = len(self.newData[setupNumber][duploName].keys())
                print(f"{setupNumber:>2}, {duploName:<32}: {nrSpectra:>2} runs")

    def print_columnNames(self):
        for setupNumber in self.newData:
            for columnName in self.newData[setupNumber]:
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
        
        # index 1 might seem as mistake but index comes from number in column names
        # and that one starts with 1
        
        
        noSaltIntensities = [spectrum.sum() for spectrum in noSaltSpectra]
        self.noSaltIntensties = noSaltIntensities # debug
        averageIntensity = sum(noSaltIntensities) / len(noSaltIntensities)
        return averageIntensity    
                    
    ## plotting the data     
    @staticmethod
    def get_intensities(spectraDictionary):
        intensities = np.zeros(max(spectraDictionary.keys()))
        for spectrumNumber in spectraDictionary: 
            index = int(spectrumNumber) - 1 #
            intensity = spectraDictionary[spectrumNumber].sum()
            intensities[index] = intensity 
        return intensities   
    
    def get_backgrounds(self):
        # 10 spectra of the background were recorded and saved in a dictionary:
        self.background = self.get_average(self.newData[1]["background"])

        # dito:
        self.fireLight = self.get_average(self.newData[2]["fireOnly"])


        # Only 1 spectrum of the lamp light was recorded and this one is saved in
        # a numpy array:
        self.sodiumLightSpectrum = self.data[5]["LampShielded_E"]
        self.sodiumLight = self.sodiumLightSpectrum.sum()

        self.sodiumLampAndFlameLight = self.get_sodiumLampAndFlameLight()

    @staticmethod
    def fix_layout():
        plt.xlabel("time (s)")
        plt.ylabel("a.u. (related to count)")
        plt.ylim(bottom=0)
        plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.subplots_adjust(right=0.75, top=0.95)
        axes = plt.gca() 
        axes.yaxis.set_major_formatter(formatter)

    def plot(self, intensities, label):
        """ Plot intensity vs time.
        Intensity (np.array)
        label (str)"""
        intensityError = 1e4
        timeArray = 4 * np.arange(len(intensities)) # measurement every 4 seconds
        timeError = 1
        print(len(timeArray), len(intensities))
        plt.errorbar(timeArray, intensities, intensityError, timeError,
                     label=label, **self.lineStyleKeywords)
        self.make_directory(f"../plots")
        self.make_directory(f"../plots/intensities")
        plt.savefig(f"../plots/intensities/{label}.png")
        plt.clf()

        
    def plot_spectrum(self, setupNumber, name, timeIndex):
        lambdaArray = self.data[1]["λ"] # all lambda arrays are the same
        self.newData[setupNumber]
        self.newData[setupNumber][name]
        self.newData[setupNumber][name][timeIndex]
        intensityArray = self.newData[setupNumber][name][timeIndex]
        plt.scatter(lambdaArray, intensityArray, **self.lineStyleKeywords)
        plt.xlabel(f"wavelength (nm)")
        plt.ylabel(self.ylabel)
        # plt.xlim(LAMBDA_MIN, LAMBDA_MAX)
        xlim = (588.5, 591.5)
        plt.xlim(*xlim)
        plt.ylim(0, 8000)
        self.make_directory(f"../report-plots/focussed-spectra/")
        self.make_directory(f"../report-plots/focussed-spectra/{setupNumber}-{name}/")
        plt.savefig(        f"../report-plots/focussed-spectra/{setupNumber}-{name}/{timeIndex}") 
                    # f"with bounds: {xlim}.png")
        plt.clf()

        
    def plot_same_time_triplo_spectra(self, setupNumber, timeIndex):
        lambdaArray = self.data[1]["λ"] # all lambda arrays are the same
        for runNumber, runName in enumerate(self.triploNames[setupNumber]):
            intensityArray = self.newData[setupNumber][runName][timeIndex]
            plt.scatter(lambdaArray, intensityArray, **self.lineStyleKeywords,
                        label=f"triplo {runNumber}")
        plt.xlabel(f"wavelength (nm)")
        plt.ylabel(self.ylabel)
        plt.xlim(587, 592)
        plt.legend()
        self.make_directory("../report-plots/spectra")
        self.print_dbg(PROGRES, f"saving /spectra/{setupNumber}:{timeIndex}")
        plt.savefig(f"../report-plots/spectra/{setupNumber}:{timeIndex}")
        plt.clf()


    def plot_background_spectrum(self):
        lambdaArray = self.data[1]["λ"] # all lambda arrays are the same
        intensities = self.get_intensities(self.newData[1]["background"][1])
        plt.scatter(lambdaArray, intensities)
        plt.xlabel("λ (nm)")
        plt.ylabel("a.u. (related to count)")
        plt.xlim(LAMBDA_MIN, LAMBDA_MAX)

    def plot_mercury_spectra(self):
        lambdaArray = self.data[1]["λ"] # all lambda arrays are the same
        intensities1 = self.newData[MERCURY]["fireWithSodium"][1]
        intensities2 = self.newData[MERCURY]["fireWithSodium"][5]
        plt.scatter(lambdaArray, intensities1)
        plt.scatter(lambdaArray, intensities2)
        plt.xlabel("λ (nm)")
        plt.ylabel("a.u. (related to count)")
        plt.xlim(LAMBDA_MIN, LAMBDA_MAX)
    

    def plot_sodium(self):  
        runNames = [("SoFlameWithSlit", "triplo 1"),
                    ("SoFlameWithSlitTwo", "triplo 2"),
                    ("SoFlameWithSlitThree", "triplo 3")]
        
        plt.figure(figsize=(10, 6))
        for runName, label in runNames:
            intensities = self.get_intensities(self.newData[5][runName])
            self.plot(intensities, label)

        fireWithSaltIntensities = self.get_intensities(self.newData[11]["fireWithSodium"])
        self.plot(fireWithSaltIntensities, "flame with salt")
        # self.plot(self.noSaltIntensties, "no salt (debug)")
        plt.axhline(self.sodiumLampAndFlameLight, label="sodium lamp and flame",
                    color="purple", linestyle='--')
        plt.axhline(self.background, label="background", color="pink", linestyle='--')
        plt.axhline(self.fireLight, label="flame", color="grey", linestyle='--')
        plt.axhline(self.sodiumLight, label="lamp", color="brown", linestyle='--')
        
        self.fix_layout()
        self.make_directory("../report-plots")
        plt.savefig("../report-plots/5: intensity vs run.png")
        plt.clf()
        
        
    def plot_magnet(self):  
        runNames = ["One", "Two", "Three"]
        
        plt.figure(figsize=(10, 6))
        for index, runName in enumerate(runNames):
            intensities = self.get_intensities(self.newData[6][runName])
            self.plot(intensities, f"triplo {index + 1}")
            
        fireWithSaltIntensities = self.get_intensities(self.newData[11]["fireWithSodium"])
        self.plot(fireWithSaltIntensities, "flame with salt")
        
        plt.axhline(self.sodiumLampAndFlameLight, label="sodium lamp and flame",
                    color="purple", linestyle='--')
        plt.axhline(self.background, label="background", color="pink", linestyle='--')
        plt.axhline(self.fireLight, label="flame", color="grey", linestyle='--')
        plt.axhline(self.sodiumLight, label="lamp", color="brown", linestyle='--')
        
        self.fix_layout()
        self.make_directory("../report-plots")
        plt.savefig(f"../report-plots/6: intensity vs run.png")
        plt.clf()
        
    def plot_mercury(self):  
        runNames = ["fireWithSodium", "two", "third"]
        
        plt.figure(figsize=(10, 6))
        for index, runName in enumerate(runNames):
            intensities = self.get_intensities(self.newData[9][runName])
            self.plot(intensities, f"triplo {index + 1}")
            
        fireWithSaltIntensities = self.get_intensities(self.newData[11]["fireWithSodium"])
        self.plot(fireWithSaltIntensities, "fire with salt")
        
        plt.axhline(self.background, label="background", color="pink", linestyle='--')
        plt.axhline(self.fireLight, label="flame", color="purple", linestyle='--')
        
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
        
        plt.scatter(intensities)
        plt.title(f"Intensity vs run")
        plt.xlabel(f"run number")
        plt.ylabel(f"intensity")
        DataProcessor.make_directory(f"../plots")
        DataProcessor.make_directory(f"../plots/intensities")
        plt.savefig(f"../plots/intensities/{label}.png")
        plt.clf() #clear figure

    def process_data(self):
        for setupNumber in self.data:
            self.get_spectra_plot(self.data[setupNumber], setupNumber)
            self.get_spectra_plots(self.data[setupNumber], setupNumber)
            self.get_intensity_plot(self.data[setupNumber], setupNumber)

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


    # create table:

    def calculate_results(self):
        """ Create table of intensities of the different runs:
        Na/Hg + salt/no salt + magnet/no magnet """

        def get_error(intensities):
            """ Local function to get the standard error in the mean """
            error = (np.std(intensities, ddof=1)
                     / (intensities.size)**0.5
            )
            return error

        for setupNr in [SODIUM, SODIUM_MAGNET, MERCURY]:
            self.means[setupNr] = {}
            self.errors[setupNr] = {}

        # background
        intensities = self.get_intensities(
            self.newData[BACKGROUND]["background"]
        )

        self.means[BACKGROUND] = intensities.mean()
        self.errors[BACKGROUND] = get_error(intensities)

        # fire
        intensities = self.get_intensities(
                        self.newData[FIRE_ONLY]["fireOnly"]
                    )
        
        self.means[FIRE_ONLY] = intensities.mean()
        self.errors[FIRE_ONLY] = get_error(intensities)

        # fire with salt
        intensities = self.get_intensities(
                          self.newData[FIRE_SALT]["fireWithSodium"]
                      )
        
        self.means[FIRE_SALT] = intensities.mean()
        self.errors[FIRE_SALT] = get_error(intensities)

        # sodium lamp, sodium lamp with magnet and mercury lamp
        for setupNr in [SODIUM, SODIUM_MAGNET, MERCURY]:
            triplo1 = self.get_intensities(
                        self.newData[setupNr][self.triploNames[setupNr][0]]
                      )
            triplo2 = self.get_intensities(
                        self.newData[setupNr][self.triploNames[setupNr][1]]
                      )
            triplo3 = self.get_intensities(
                        self.newData[setupNr][self.triploNames[setupNr][2]]
                      )
            
            ## without salt
            intensities = np.array([triplo1[0], triplo2[0], triplo3[0]])

            mean = intensities.mean()
            error = get_error(intensities)

            # substract background
            mean -= self.means[FIRE_ONLY]
            # add error of background
            error = (error**2 + self.errors[FIRE_ONLY]**2)**0.5

            # save
            self.means[setupNr]["without-salt"] = mean
            self.errors[setupNr]["without-salt"] = error

            ## with salt
            intensities = np.concatenate((triplo1[1:], triplo2[1:], triplo3[1:]))

            mean = intensities.mean()
            error = get_error(intensities)

            # subtract background
            mean -= self.means[FIRE_SALT]
            # add error of background
            error = (error**2 + self.errors[FIRE_SALT]**2)**0.5

            # save
            self.means[setupNr]["with-salt"] = mean
            self.errors[setupNr]["with-salt"] = error

    def show_table(self):
        def to_string(element):
            if type(element) == str:
                return element
            else:
                return f"{element:.4e}"

        def print_table(array):
            widths = [0 for i in range(len(array))]
            for row in array:
                for i, element in enumerate(row):
                    widths[i] = max(len(to_string(element)) + 2, widths[i])

            for row in array:
                for i, element in enumerate(row):
                    print(f"{to_string(element):<{widths[i]}}", end='')
                print()


        print_table([["lamp",   "salt", "magnet", "mean",                                     "error"                                   ],
                     ["Na",     "",     "",        self.means[SODIUM]["without-salt"],         self.errors[SODIUM]["without-salt"]       ],
                     ["Na",     "salt", "",        self.means[SODIUM]["with-salt"],            self.errors[SODIUM]["with-salt"]          ],
                     ["Na",     "",     "magnet",  self.means[SODIUM_MAGNET]["without-salt"],  self.errors[SODIUM_MAGNET]["without-salt"]],
                     ["Na",     "salt", "magnet",  self.means[SODIUM_MAGNET]["with-salt"],     self.errors[SODIUM_MAGNET]["with-salt"]   ],
                     ["Hg",     "",     "",        self.means[MERCURY]["without-salt"],        self.errors[MERCURY]["without-salt"]      ],
                     ["Hg",     "salt", "",        self.means[MERCURY]["with-salt"],           self.errors[MERCURY]["with-salt"]         ]]
        )

    def show_ratios(self):
        def print_ratios(setupNr, name):
            withSalt = self.means[setupNr]['with-salt']
            withoutSalt = self.means[setupNr]['without-salt']
            withSaltError = self.errors[setupNr]["with-salt"]
            withoutSaltError = self.errors[setupNr]["without-salt"]

            ratio = withSalt / withoutSalt
            error = np.sqrt(withSaltError**2 + withoutSaltError**2)

            print(f"{name}: {ratio} pm {error}")

        print(f"Sodium lamp ratio {self.means[SODIUM]['without-salt']/self.means[SODIUM]['with-salt']:.2f}")
        print(f"Sodium lamp with magnet ratio {self.means[SODIUM_MAGNET]['without-salt']/self.means[SODIUM_MAGNET]['with-salt']:.2f}")
        print(f"Sodium lamp with magnet ratio {self.means[MERCURY]['without-salt']/self.means[MERCURY]['with-salt']:.2f}")
        
        

        
    def show_all_intensities(self):
        for setupNr in self.newData:
            for runNr, name in enumerate(self.newData[setupNr]):
                intensities = self.get_intensities(self.newData[setupNr][name])
                timeArray = 4 * np.arange(len(intensities))
                plt.scatter(timeArray, intensities,
                            marker='.',
                            label=name)
            plt.ylim(bottom=0)
            plt.legend()
            plt.savefig(f"../plots/intensities/{setupNr}.png")
            plt.clf()   

    

            
        
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
