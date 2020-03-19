import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time


# using pandas because 36.56730818748474 vs 110.98377823829651
print("Reading file...")
positions = pd.read_csv("position_data.csv", delimiter=",")
print("File read.")


snapshot_rows = np.linspace(0, len(positions) / 3 - 1, 100, dtype=int)
snapshot_positions = positions.iloc[snapshot_rows,:]

for idx, row in snapshot_positions.iterrows():
    time = row[0]
    central_x = row[1]
    central_y = row[2]
    moving_x = row[3]
    moving_y = row[4]
    test_particles_positions = row[5:]
    test_particles_x = [coord for idx, coord in enumerate(test_particles_positions) if idx % 2 == 0]
    test_particles_y = [coord for idx, coord in enumerate(test_particles_positions) if idx % 2 == 1]

    plt.clf()
    plt.scatter(central_x, central_y, color='b')
    plt.scatter(moving_x, moving_y, color='r')
    plt.scatter(test_particles_x, test_particles_y, color='g', s=1)
    # plt.xlim([-100, 100])
    # plt.ylim([-100, 100])
    plt.pause(0.01)