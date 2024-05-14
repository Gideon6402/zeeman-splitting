def get_spectra_plots(spectraDictionary, name):
    print_dbg(PROGRES, f"getting all spectra plots for {name}...")
    for columnName in spectraDictionary:
        if (columnName != "λ" and columnName != "Raw_E"):
            plt.plot(spectraDictionary["λ"],
                    spectraDictionary[columnName])
            plt.ylim(0, 8_000)
            plt.title(columnName)
            mkdir(f"../plots/{name}")
            plt.savefig(f"../plots/{name}/{columnName}.png") 