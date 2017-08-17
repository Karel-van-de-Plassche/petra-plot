import matplotlib.pyplot as plt
import numpy as np
from IPython import embed
import pandas as pd

np.load
with open('./XRD/c010-RT.uxd', 'r', encoding = "ISO-8859-1") as file_:
    lines = [line for line in file_]

    start_ind = lines.index('; 2THETA\tCnt2_D1\t\n')

    column_names = ['2theta', 'Intensity']
    df = pd.DataFrame(np.loadtxt(lines[start_ind+1:]), columns=column_names)
    df.plot(x='2theta', y='Intensity')
plt.show()
