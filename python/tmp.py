def get_average(dictionary):
    """ Return the average value of all values in a dictionary"""
    sumOfValues = 0
    nrOfValues = 0
    for key in dictionary:
        for value in dictionary[key]:
            sumOfValues += value
            nrOfValues += 1
    return sumOfValues / nrOfValues