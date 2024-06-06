#!/bin/python3

from package import *

obj = DataProcessor()

categories = [
    "Na",
    "Na + salt",
    "Na + magnet",
    "Na + magnet + salt",
    "Hg",
    "Hg + salt",
]

values = [
    obj.means[SODIUM]["without-salt"],
    obj.means[SODIUM]["with-salt"],
    obj.means[SODIUM_MAGNET]["without-salt"],
    obj.means[SODIUM_MAGNET]["with-salt"],
    obj.means[MERCURY]["without-salt"],
    obj.means[MERCURY]["with-salt"],
]

errors = [
    obj.errors[SODIUM]["without-salt"],
    obj.errors[SODIUM]["with-salt"],
    obj.errors[SODIUM_MAGNET]["without-salt"],
    obj.errors[SODIUM_MAGNET]["with-salt"],
    obj.errors[MERCURY]["without-salt"],
    obj.errors[MERCURY]["with-salt"],
]

errorKeyWords = {
    "ecolor": "red",
    "capsize": 5,
}

plt.bar(categories, values, yerr=errors, ecolor="red", error_kw=errorKeyWords)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("../report-plots/histogram")