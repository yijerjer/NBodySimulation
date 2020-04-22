import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from core import radii_units_colors
from core import get_positions_from_row


try:
    if len(sys.argv) < 2:
        raise OSError("Provide an existing data file name from the data/ folder")

    filename = sys.argv[1]
    if not os.path.isfile(f"data/{filename}"):
        raise OSError(f"The file {filename} does not exist. Please provide an existing data file in the data/ folder")

    print("Reading file...")
    positions = pd.read_csv(f"data/{filename}", delimiter=",")
    print("File read.")

    animation_rows = np.linspace(0, len(positions)- 1, 100, dtype=int)
    animation_positions = positions.iloc[animation_rows,:]

    for idx, row in animation_positions.iterrows():
        (time, central_x, central_y, moving_x, moving_y, particles_xs, particles_ys) = get_positions_from_row(row)

        plt.clf()
        plt.scatter(central_x, central_y, color='b')
        plt.scatter(moving_x, moving_y, color='r')
        for idx, (radius, num, color) in enumerate(radii_units_colors):
            plt.scatter(particles_xs[idx], particles_ys[idx], s=1, color=color, label=rf"$r = {radius}$")
            
        plt.xlim([-100, 100])
        plt.ylim([-100, 100])
        plt.title(time)
        plt.pause(0.01)
    
except OSError as e:
    print(repr(e))