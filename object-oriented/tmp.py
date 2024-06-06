    def plot_Na_no_salt_spectrum(self, setupNumber):
        lambdaArray = self.data[1]["λ"]
        for runName, label in self.triploNames[setupNumber]:
            intensityArray = self.newData[setupNumber][runName][1]
            plt.scatter(lambdaArray, intensityArray, **self.lineStyleKeywords,
                        label=label)
        plt.xlabel(f"wavelength (nm)")
        plt.ylabel(self.ylabel)
        plt.xlim(587, 592)
        plt.legend()
        self.make_directory("../report-plots/spectra")
        plt.savefig(f"../report-plots/spectra/{setupNumber}-no-salt")
        plt.clf()