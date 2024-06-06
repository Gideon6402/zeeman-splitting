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

# background
intensities = obj.get_intensities(
    obj.newData[BACKGROUND]["background"]
)
means[BACKGROUND] = intensities.mean()
errors[BACKGROUND] = np.std(intensities, ddof=1)

# fire
intensities = obj.get_intensities(
                  obj.newData[FIRE_ONLY]["fireOnly"]
              )
means[FIRE_ONLY] = intensities.mean()
errors[FIRE_ONLY] = np.std(intensities, ddof=1)



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

    # substract background
    mean -= means[FIRE_ONLY]
    error = (error**2 + errors[FIRE_ONLY]**2)**0.5 # error propagation

    means[setupNr]["without-salt"] = mean
    errors[setupNr]["without-salt"] = error

    # setupNr - with salt
    intensities = np.concatenate((triplo1[1:], triplo2[1:], triplo3[1:]))
    mean = intensities.mean()
    error = np.std(intensities, ddof=1) # sample standard deviation
    means[setupNr]["with-salt"] = mean
    errors[setupNr]["with-salt"] = error

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


print_table([["",                   "mean",                               "error"                              ],
             ["background",         means[BACKGROUND],                    errors[BACKGROUND]                   ],
             ["fire",               means[FIRE_ONLY],                     errors[FIRE_ONLY]                    ],
             ["Na",                 means[SODIUM]["without-salt"],        errors[SODIUM]["without-salt"]       ],
             ["Na + salt",          means[SODIUM]["with-salt"],           errors[SODIUM]["with-salt"]          ],
             ["Na + magnet",        means[SODIUM_MAGNET]["without-salt"], errors[SODIUM_MAGNET]["without-salt"]],
             ["Na + magnet + salt", means[SODIUM_MAGNET]["with-salt"],    errors[SODIUM_MAGNET]["with-salt"]   ],
             ["Hg",                 means[MERCURY]["without-salt"],       errors[MERCURY]["without-salt"]      ],
             ["Hg + salt",          means[MERCURY]["with-salt"],          errors[MERCURY]["with-salt"]         ]]
)

