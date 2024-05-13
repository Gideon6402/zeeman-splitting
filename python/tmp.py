def mkdir(filename):
    if not os.path.isdir(filename):
        os.system(f"mkdir {filename}")

def get_spectra_plot(spectraDictionary, name):
    print_dbg(1, f"getting  spectra plots    for {name}...")
    plt.title(f"{name}")
    for columnName in spectraDictionary:
        if (columnName != "λ\n" and columnName != "Raw_E\n"):
            plt.plot(spectraDictionary["λ\n"],
                     spectraDictionary[columnName],
                     label=columnName)
    plt.legend()
    plt.savefig(f"../plots/all-spectra/{name}.png")
    plt.clf() # clear figure
    
def get_spectra_plots(spectraDictionary, setupNumber):
    print_dbg(PROGRES, f"getting all spectra plots for {setupNumber}...")
    for columnName in spectraDictionary:
        if (columnName != "λ\n" and columnName != "Raw_E\n"):
            plt.plot(spectraDictionary["λ\n"],
                    spectraDictionary[columnName])
            plt.ylim(0, 8_000)
            plt.title(columnName)
            plt.savefig(f"../plots/{setupNumber}/{columnName}.png") 
            plt.clf()
    
def get_intensity(spectraDictionary, setupNumber):
    print_dbg(PROGRES, f"getting intensities       for {setupNumber}...")
    intensities = []
    for columnName in spectraDictionary:
        if (columnName != "λ\n" and columnName != "Raw_E\n"):
            intensity = spectraDictionary[columnName].sum()
            intensities.append(intensity)
    plt.plot(intensities)
    plt.savefig(f"../plots/intensities/{setupNumber}.png")
    plt.clf() #clear figure

def get_plots(data):
    mkdir(f"../plots/intensities")
    mkdir(f"../plots/all-spectra")
    for setupNumber in data:
        mkdir(f"../plots/{setupNumber}")
        get_spectra_plot(data[setupNumber], setupNumber)
        get_spectra_plots(data[setupNumber], setupNumber)
        get_intensity(data[setupNumber], setupNumber)
            