def plot_spectrum(self, setupNumber, name, timeIndex):
    for i in range(max(self.newData[setupNumber][name].keys())):
        lambdaArray = self.data[1]["λ"] # all lambda arrays are the same
        intensityArray = self.newData[setupNumber][name][i + 1]
        plt.scatter(lambdaArray, intensityArray, **self.lineStyleKeywords)
        plt.xlabel(f"wavelength (nm)")
        plt.ylabel(self.ylabel)
        plt.xlim(LAMBDA_MIN, LAMBDA_MAX)
        self.make_directory("../report-plots/spectra")
    plt.show()