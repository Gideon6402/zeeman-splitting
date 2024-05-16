#!/bin/python3

from package import *

def main():
    data = acquire_data()
    newData = separate_runs(data)
    background = get_average(newData[1]["background"])
    fireLight = get_average(newData[2]["fireOnly"])
    sodiumLight = data[5]["LampShielded_E"].sum()
    sodiumLampAndFlameLight = get_sodiumLampAndFlameLight(newData)
    
    plot_sodium( background, fireLight, sodiumLight, sodiumLampAndFlameLight, newData)
    plot_magnet( background, fireLight, sodiumLight, sodiumLampAndFlameLight, newData)
    plot_mercury(background, fireLight, sodiumLight, sodiumLampAndFlameLight, newData)
    
if __name__ == "__main__":
    main()