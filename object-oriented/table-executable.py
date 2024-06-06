#!/bin/python3

from package import *

def create_table(self):
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0, 0))  # Set the limits for using scientific notation

    obj = DataProcessor() # object

    for setupNr in [SODIUM, SODIUM_MAGNET, MERCURY]:
        obj.means[setupNr] = {}
        obj.errors[setupNr] = {}

    # background
    intensities = obj.get_intensities(
        obj.newData[BACKGROUND]["background"]
    )
    obj.means[BACKGROUND] = intensities.mean()
    obj.errors[BACKGROUND] = np.std(intensities, ddof=1)

    # fire
    intensities = obj.get_intensities(
                    obj.newData[FIRE_ONLY]["fireOnly"]
                )
    obj.means[FIRE_ONLY] = intensities.mean()
    obj.errors[FIRE_ONLY] = np.std(intensities, ddof=1)



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
        mean -= obj.means[FIRE_ONLY]
        error = (error**2 + obj.errors[FIRE_ONLY]**2)**0.5

        obj.means[setupNr]["without-salt"] = mean
        obj.errors[setupNr]["without-salt"] = error

        # setupNr - with salt
        intensities = np.concatenate((triplo1[1:], triplo2[1:], triplo3[1:]))
        mean = intensities.mean()
        error = np.std(intensities, ddof=1) # sample standard deviation
        obj.means[setupNr]["with-salt"] = mean
        obj.errors[setupNr]["with-salt"] = error

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
                #  ["background",         obj.means[BACKGROUND],                    obj.errors[BACKGROUND]                   ],
                #  ["fire",               obj.means[FIRE_ONLY],                     obj.errors[FIRE_ONLY]                    ],
                ["Na",                 obj.means[SODIUM]["without-salt"],        obj.errors[SODIUM]["without-salt"]       ],
                ["Na + salt",          obj.means[SODIUM]["with-salt"],           obj.errors[SODIUM]["with-salt"]          ],
                ["Na + magnet",        obj.means[SODIUM_MAGNET]["without-salt"], obj.errors[SODIUM_MAGNET]["without-salt"]],
                ["Na + magnet + salt", obj.means[SODIUM_MAGNET]["with-salt"],    obj.errors[SODIUM_MAGNET]["with-salt"]   ],
                ["Hg",                 obj.means[MERCURY]["without-salt"],       obj.errors[MERCURY]["without-salt"]      ],
                ["Hg + salt",          obj.means[MERCURY]["with-salt"],          obj.errors[MERCURY]["with-salt"]         ]]
    )

