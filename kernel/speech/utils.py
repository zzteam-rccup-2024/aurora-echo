import numpy as np


def db_level(data):
    value = 20 * np.log10(np.sqrt(np.mean(data ** 2)))
    print(value, value)
    return value

#%%
