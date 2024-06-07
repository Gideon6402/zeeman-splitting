#!/bin/python3

### Saves the bar graph at report-plots/bar-graph.png ###

from dataprocessor import * # package that I created

obj = DataProcessor()

categories = [
    "Na-lamp",
    "Na-lamp with magnet",
    "Hg-lamp"
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

# plt.bar(categories, values, yerr=errors, ecolor="red", error_kw=errorKeyWords)
# plt.ylabel(obj.ylabel)
# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()
# plt.savefig("../report-plots/histogram")

fig, axes = plt.subplots()

positions = np.arange(3)
barWidth = 0.35
plt.bar(positions - barWidth/2, values[0::2], barWidth, label="without salt",
        yerr=errors[0::2], error_kw=errorKeyWords)
plt.bar(positions + barWidth/2, values[1::2], barWidth, label="with-salt",
        yerr=errors[1::2], error_kw=errorKeyWords)
plt.legend()
plt.ylabel("count (a.u.)")
plt.tight_layout()

ax = plt.gca()
ax.set_xticks(positions)
ax.set_xticklabels(categories)
plt.savefig("../report-plots/bar-graph")
plt.show()