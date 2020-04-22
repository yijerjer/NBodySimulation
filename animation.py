import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from core import radii_units_colors
from core import get_positions_from_row


class AnimateSimulation:
    def __init__(self, positions):
        self.fig, self.axs = plt.subplots()
        self.axs.set_xlim([-100, 100])
        self.axs.set_ylim([-100, 100])

        animation_rows = np.linspace(0, len(positions) - 1, 500, dtype=int)
        self.animation_positions = positions.iloc[animation_rows, :]
        self.first_row = self.animation_positions.iloc[0]
        self.setup_scatter()

        self.animation = animation.FuncAnimation(self.fig, self.update_scatter, blit=True, interval=5, frames=500)
        
    def setup_scatter(self):
        X, Y, C, S = self.get_xycs(self.first_row)
        self.scat = self.axs.scatter(X, Y, c=C, s=S)
        return self.scat,

    def update_scatter(self, i):
        row = self.animation_positions.iloc[i]
        X, Y, _, _ = self.get_xycs(row)
        self.scat.set_offsets(np.transpose([X, Y]))
        return self.scat,

    def get_xycs(self, row):
        X = [pos for idx, pos in enumerate(row[1:]) if idx % 2 == 0]
        Y = [pos for idx, pos in enumerate(row[1:]) if idx % 2 == 1]
        C = ['b', 'r'] + [c for arr in [[color] * num for _, num, color in radii_units_colors] for c in arr]
        S = [10] * 2 + [1] * 1200
        return X, Y, C, S
        

try:
    if len(sys.argv) < 2:
        raise OSError("Provide an existing data file name from the data/ folder")

    filename = sys.argv[1]
    if not os.path.isfile(f"data/{filename}"):
        raise OSError(f"The file {filename} does not exist. Please provide an existing data file in the data/ folder")

    print("Reading file...")
    positions = pd.read_csv(f"data/{filename}", delimiter=",")
    print("File read.")

    a = AnimateSimulation(positions)
    a.animation.save(f"{filename[:-4]}.mp4", writer=animation.FFMpegWriter(fps=30, codec="libx264"))
    # plt.show()
    
except OSError as e:
    print(repr(e))