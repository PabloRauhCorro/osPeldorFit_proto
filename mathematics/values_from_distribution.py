import numpy as np

def values_from_distribution(mean, width, type_of_distribution, size):
        values = 0
        if(width == 0):
            values = mean
        else:
            if(type_of_distribution == "uniform"):
                values = np.random.uniform(low=mean - 0.5 * width, high=mean + 0.5 * width, size=size)
            elif(type_of_distribution == "normal"):
                values = np.random.normal(mean, width, size=size)
        return values