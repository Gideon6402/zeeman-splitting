    def show_all_intensities(self):
        
        for setupNr in self.newData:
            for runNr, name in enumerate(self.newData[setupNr]):
                intensities = self.get_intensities(self.newData[setupNr][name])
                timeArray = 4 * np.arange(len(intensities))
                plt.scatter(timeArray, intensities,
                            marker='.',
                            label=self.triploNames[setupNr][runNr])
            plt.savefig(f"../plots/intensities/{setupNr}:{name}.png")
            plt.clf()