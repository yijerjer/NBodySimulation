import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

radii_units_colors = [
    (2, 120, 'g'),
    (3, 180, 'c'),
    (4, 240, 'm'), 
    (5, 300, 'y'),
    (6, 360, 'k')
]


print("Reading file...")
positions = pd.read_csv(f"ac_positions.csv", delimiter=",")
print("File read.")

snapshot_rows = np.linspace(0, len(positions)- 1, 100, dtype=int)
snapshot_positions = positions.iloc[snapshot_rows,:]

for idx, row in snapshot_positions.iterrows():
    time = row[0]
    central_x = row[1]
    central_y = row[2]
    moving_x = row[3]
    moving_y = row[4]
    test_particles_positions = row[5:]
    all_test_particles_x = [coord for idx, coord in enumerate(test_particles_positions) if idx % 2 == 0]
    all_test_particles_y = [coord for idx, coord in enumerate(test_particles_positions) if idx % 2 == 1]

    test_particles_xs = []
    test_particles_ys = []
    index = 0
    for (radius, num, color) in radii_units_colors:
        test_particles_xs.append(all_test_particles_x[index:index + num])
        test_particles_ys.append(all_test_particles_y[index:index + num])
        index += num

    plt.clf()
    plt.scatter(central_x, central_y, color='b')
    plt.scatter(moving_x, moving_y, color='r')
    for idx, (radius, num, color) in enumerate(radii_units_colors):
        plt.scatter(test_particles_xs[idx], test_particles_ys[idx], s=1, color=color, label=rf"$r = {radius}$")
        
    plt.xlim([-100, 100])
    plt.ylim([-100, 100])
    plt.pause(0.01)
