def get_intensity_plot(spectraDictionary, label):
    print_dbg(PROGRES, f"getting intensities       for {label}...")
    
    intensities = get_intensities(spectraDictionary)
    
    plt.plot(intensities, linestyle='-',
             marker = 'x', linewidth=0.5)
    plt.title(f"Intensity vs run")
    plt.xlabel(f"run number")
    plt.ylabel(f"intensity")
    make_directory(f"../plots/intensities")
    plt.savefig(f"../plots/intensities/{label}.png")
    plt.clf() #clear figure