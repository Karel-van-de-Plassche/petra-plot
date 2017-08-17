import matplotlib as mpl
from matplotlib import cycler
import matplotlib.pyplot as plt
plt.style.use('./paper.mplstyle') # Choose the settings file to use
import numpy as np
from IPython import embed
import pandas as pd
from itertools import chain
import os

def load_file(filename):
    with open(filename, 'r', encoding = "ISO-8859-1") as file_:
        lines = file_.readlines() # Read the complete file

        dfs = []
        while len(lines) > 0: # Keep reading until all chunks are read
            name_ind = lines.index('Curve Name:\n') # Look for 'Curve Name:'
            del lines[name_ind]
            curve_name = lines[name_ind].strip()
            print(curve_name)
            start_ind = lines.index('Curve Values:\n') # Values start after 'Curve Values'

            column_names = lines[start_ind+1].split() # The line after that are the column names
            column_units = lines[start_ind+2].split() # And after that the units

            results_ind = lines.index('Results:\n') # The values stop when we find 'Results:'
            df = pd.DataFrame(np.loadtxt(lines[start_ind+3:results_ind]),
                              columns=column_names) # Now put it in a table
            df.set_index('Tr', inplace=True) # The 'x-axis' is Tr
            dfs.append(df['Value']) # And we only need the Value column

            try:
                end_ind = lines.index('Curve Name:\n') # Try to find the next chunk
            except ValueError:
                end_ind = len(lines) # If we can't find it, we're done!
            del lines[:end_ind]

    #results = pd.concat(dfs, axis=1) # Now, merge all chuncks together
    heating = pd.concat(dfs[1::2], axis=1) # Merge all heating chunks
    cooling = pd.concat(dfs[0::2], axis=1) # And all cooling chunks
    for set in chain([heating, cooling]): # For both heating and cooling
        set.columns = reversed(range(1, len(set.columns) + 1)) # Number them N..1
        set.index.name = 'Temperature [$\degree$C]' # And rename the x-axis
    heating.columns = ['Heating ' + str(col) for col in heating.columns] # Now prepend Heating to the column names
    cooling.columns = ['Cooling ' + str(col) for col in cooling.columns] # And Cooling
    #labels = []
    #for ii in range(1, len(results.columns) // 2 + 1):
    #    labels.append('Heating ' + str(ii))
    #    labels.append('Cooling ' + str(ii))
    #labels = list(reversed(labels))
    #results.columns = labels

    return heating, cooling

def plot_heating_cooling(heating, cooling, shift=0.2, base_shift=0.0):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for ii in range(1, len(cooling.columns) + 1):
        cooling.iloc[:, ii:] = cooling.iloc[:, ii:] + shift # Shift all curves, the 2nd one the most
    cooling += base_shift # And shift all columns a set amount

    for ii in range(1, len(heating.columns) + 1):
        heating.iloc[:, ii:] = heating.iloc[:, ii:] - shift
    heating -= base_shift

    for ii in range(len(heating.columns)):
        for set in chain([heating, cooling]): # Now plot Heating ii and Cooling ii in pairs
            ax.plot(set.iloc[:, ii], label=set.iloc[:, ii].name)
    ax.legend() # Plot the legend
    #cooling.plot(ax=ax)
    #heating.plot(ax=ax)

cmap = plt.get_cmap('tab20') # Choose the colors by name: https://matplotlib.org/examples/color/colormaps_reference.html
plt.rc('axes', prop_cycle=(cycler('color', cmap.colors)))
root = 'DSC' # This is the main folder to look for files
for filename in os.listdir(root): # For every folder in the root folder
    if filename.endswith('.txt'): # If it ends with .txt
        path_to_file = os.path.join(root, filename)
        heating, cooling = load_file(path_to_file) # Read the file and put it in a table
        plot_heating_cooling(heating, cooling, shift=0.2, base_shift=0.0) # And plot the curves
plt.show()
