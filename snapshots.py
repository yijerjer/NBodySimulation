import os
import sys
import time
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

    positions["pos_difference"] = np.sqrt(np.square(positions.central_x - positions.moving_x) + np.square(positions.central_y - positions.moving_y))
    closest_approach = positions[positions.pos_difference == positions.pos_difference.min()].iloc[0]
    closest_approach_idx = closest_approach.name
    snapshot_rows = np.array([-1000, 0, 250, 500, 1000, 1250]) + closest_approach_idx
    snapshot_positions = positions.iloc[snapshot_rows,:]
    snapshot_positions["time"] = snapshot_positions["time"] - closest_approach.time

    fig, axs = plt.subplots(3, 2, figsize=(6, 7.5))
    axs_count = 0

    for idx, row in snapshot_positions.iterrows():
        (time, central_x, central_y, moving_x, moving_y, particles_xs, particles_ys) = get_positions_from_row(row)

        axs[axs_count % 3][1 if axs_count > 2 else 0].scatter(central_x, central_y, color='b')
        axs[axs_count % 3][1 if axs_count > 2 else 0].scatter(moving_x, moving_y, color='r')
        for idx, (radius, num, color) in enumerate(radii_units_colors):
            axs[axs_count % 3][1 if axs_count > 2 else 0].scatter(particles_xs[idx], particles_ys[idx], s=1, color=color, label=rf"$r = {radius}$")
            
        axs[axs_count % 3][1 if axs_count > 2 else 0].set_xlim([-60, 60])
        if filename.find("clockwise") >= 0:
            axs[axs_count % 3][1 if axs_count > 2 else 0].set_ylim([-40, 80])
        else:
            axs[axs_count % 3][1 if axs_count > 2 else 0].set_ylim([-80, 40])
        axs[axs_count % 3][1 if axs_count > 2 else 0].tick_params(axis='x', which='both', bottom=False, labelbottom=False)
        axs[axs_count % 3][1 if axs_count > 2 else 0].tick_params(axis='y', which='both', left=False, labelleft=False)
        axs[axs_count % 3][1 if axs_count > 2 else 0].set_title(rf"$t = {int(time)}$")
        if axs_count == 0:
            axs[axs_count % 3][1 if axs_count > 3 else 0].legend()

        axs_count += 1

    fig.tight_layout()
    fig.savefig(f"report/images/plot_{filename}.png", dpi=400)

except OSError as e:
    print(repr(e))