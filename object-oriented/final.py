#!/bin/python3

from package import *

formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((0, 0))  # Set the limits for using scientific notation

obj = DataProcessor() # object

means = {}
errors = {}

for setupNr in [SODIUM, SODIUM_MAGNET, MERCURY]:
    means[setupNr] = {}
    errors[setupNr] = {}

for setupNr in [SODIUM, SODIUM_MAGNET, MERCURY]:
    triplo1 = obj.get_intensities(
                  obj.newData[setupNr][obj.triploNames[setupNr][0]]
              )
    triplo2 = obj.get_intensities(
                  obj.newData[setupNr][obj.triploNames[setupNr][1]]
              )
    triplo3 = obj.get_intensities(
                  obj.newData[setupNr][obj.triploNames[setupNr][2]]
              )
    
    intensities = np.array([triplo1[0], triplo2[0], triplo3[0]])

    mean = intensities.mean()
    error = np.std(intensities, ddof=1) # sample standard deviation
    means[setupNr]["without-salt"] = mean
    errors[setupNr]["without-salt"] = error

    # setupNr - with salt
    intensities = np.concatenate((triplo1[1:], triplo2[1:], triplo3[3:]))
    mean = intensities.mean()
    error = np.std(intensities, ddof=1) # sample standard deviation
    means[setupNr]["with-salt"] = mean
    errors[setupNr]["with-salt"] = error



def print_table(array):
    for row in array:
        for element in row:
            if type(element) == str:
                print(f"{element:<12}", end='')
            else:
                print(f"{element:<12.4e}", end='')
        print()

print_table([["",          "mean",                         "error"                        ],
             ["Na",        means[SODIUM]["without-salt"],  errors[SODIUM]["without-salt"] ],
             ["Na + salt", means[SODIUM]["with-salt"],     errors[SODIUM]["with-salt"]    ],
             ["Hg",        means[MERCURY]["without-salt"], errors[MERCURY]["without-salt"]],
             ["Hg + salt", means[MERCURY]["with-salt"],    errors[MERCURY]["with-salt"]   ]]
)