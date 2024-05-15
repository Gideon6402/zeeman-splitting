def get_intensity_plot(spectraDictionary, lambdaArray, dictionaryName):
    print_dbg(PROGRES, f"getting intensities       for {dictionaryName}...")
    intensities = []
    for spectrumNameOrNumber in spectraDictionary:
        if (spectrumNameOrNumber != "λ" and spectrumNameOrNumber != "Raw_E"):
            intensity = get_intensity(spectraDictionary[spectrumNameOrNumber], lambdaArray)
            intensities.append(intensity)
            plt.plot(range(len(intensities)), intensities, label=spectrumNameOrNumber)
    plt.title(f"Intensity vs run")
    # plt.xlim(580, 600)
    plt.xlabel(f"run number")
    plt.ylabel(f"intensity")
    make_directory(f"../plots/intensities")
    plt.savefig(f"../plots/intensities/{dictionaryName}.png")
    plt.clf() #clear figure