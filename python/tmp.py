def plot_experiment(background, fireLight, sodiumLight, sodiumLampAndFlameLight,
                    newData):  
    sodium = ["SoFlameWithSlit", "SoFlameWithSlitTwo", "SoFlameWithSlitThree"]
    sodiumWithMagnet = ["SodiumWithMagnetic", "Two", "Three"]
    mercury = ["fireWithSodium", "two", "third"]
    
    for setupNumber, runNames in [(5, sodium),
                                  (6, sodiumWithMagnet), 
                                  (9, mercury)]:
        plt.figure(figsize=(8, 6))
        for runName in runNames:
            intensities = get_intensities(newData[setupNumber][runName])
            plt.plot(intensities, label=runName, linestyle='-', marker = 'x', linewidth=0.5)
        plt.axhline(background, label="background", color="red")
        plt.axhline(fireLight, label="fire only", color="purple")
        plt.axhline(sodiumLampAndFlameLight, label="sodium lamp and fire together", color="brown")
        
        plt.title("intensity vs run number for all three triplo runs")
        plt.xlabel("run number")
        plt.ylabel(f"intensity (unknown unit)")
        plt.ylim(0, max(intensities)*1.1)
        plt.legend()
        make_directory("../report-plots")
        plt.savefig(f"../report-plots/{setupNumber}: intensity vs run.png")
        plt.clf()