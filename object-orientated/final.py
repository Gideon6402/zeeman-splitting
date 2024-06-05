#!/bin/python3

from package import *

formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((0, 0))  # Set the limits for using scientific notation

self = DataProcessor()

means = {}
errors = {}

for setupNr in [SODIUM, SODIUM_MAGNET, MERCURY]:
    means[setupNr] = {}
    errors[setupNr] = {}



# Sodium - no salt
intensities = np.array([
    self.get_intensities(self.newData[SODIUM]["SoFlameWithSlit"])[0],
    self.get_intensities(self.newData[SODIUM]["SoFlameWithSlitTwo"])[0],
    self.get_intensities(self.newData[SODIUM]["SoFlameWithSlitThree"])[0],
])

mean = intensities.mean()
error = np.std(intensities, ddof=1) # sample standard deviation
means[SODIUM]["without-salt"] = mean
errors[SODIUM]["with-salt"] = error

print(f"mean: {mean:.4e}, error: {error:.4e}")



