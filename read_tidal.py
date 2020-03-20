import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

color_and_units = [
    ('g', 12),
    ('c', 18),
    ('m', 24), 
    ('y', 30),
    ('k', 36)
]

# using pandas because 36.56730818748474 vs 110.98377823829651
print("Reading file...")
positions = pd.read_csv("ac_positions_rmin20.csv", delimiter=",")
print("File read.")


snapshot_rows = np.linspace(0, len(positions)/2 - 1, 100, dtype=int)
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
    for color, num in color_and_units:
        test_particles_xs.append(all_test_particles_x[index:index + num])
        test_particles_ys.append(all_test_particles_y[index:index + num])
        index += num

    plt.clf()
    plt.scatter(central_x, central_y, color='b')
    plt.scatter(moving_x, moving_y, color='r')
    for idx, (color, num) in enumerate(color_and_units):
        plt.scatter(test_particles_xs[idx], test_particles_ys[idx], s=1, color=color)
        
    plt.xlim([-100, 100])
    plt.ylim([-100, 100])
    plt.pause(0.01)

final_row = snapshot_positions.iloc[-1]
time = final_row[0]
central_x = final_row[1]
central_y = final_row[2]
moving_x = final_row[3]
moving_y = final_row[4]
test_particles_positions = final_row[5:]
all_test_particles_x = [coord for idx, coord in enumerate(test_particles_positions) if idx % 2 == 0]
all_test_particles_y = [coord for idx, coord in enumerate(test_particles_positions) if idx % 2 == 1]

test_particles_xs = []
test_particles_ys = []
index = 0
for color, num in color_and_units:
    test_particles_xs.append(np.array(all_test_particles_x[index:index + num]))
    test_particles_ys.append(np.array(all_test_particles_y[index:index + num]))
    index += num

for idx in range(len(test_particles_xs)):
    distance_to_central = np.sqrt(np.square(test_particles_xs[idx] - central_x) + np.square(test_particles_ys[idx] - central_y))
    print(distance_to_central)