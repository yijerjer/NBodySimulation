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

# snapshot_rows = np.linspace(0, len(positions)- 1, 4, dtype=int)
snapshot_rows = [2550, 4050, 4250, 4550, 5050, 5550]
snapshot_positions = positions.iloc[snapshot_rows,:]

fig, axs = plt.subplots(3, 2, figsize=(6, 7.5))
axs_count = 0

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

    axs[axs_count % 3][1 if axs_count > 2 else 0].scatter(central_x, central_y, color='b')
    axs[axs_count % 3][1 if axs_count > 2 else 0].scatter(moving_x, moving_y, color='r')
    for idx, (radius, num, color) in enumerate(radii_units_colors):
        axs[axs_count % 3][1 if axs_count > 2 else 0].scatter(test_particles_xs[idx], test_particles_ys[idx], s=1, color=color, label=rf"$r = {radius}$")
        
    axs[axs_count % 3][1 if axs_count > 2 else 0].set_xlim([-60, 60])
    axs[axs_count % 3][1 if axs_count > 2 else 0].set_ylim([-80, 40])
    axs[axs_count % 3][1 if axs_count > 2 else 0].tick_params(axis='x', which='both', bottom=False, labelbottom=False)
    axs[axs_count % 3][1 if axs_count > 2 else 0].tick_params(axis='y', which='both', left=False, labelleft=False)
    axs[axs_count % 3][1 if axs_count > 2 else 0].set_title(rf"$t = {int(time - 405)}$")
    if axs_count == 0:
        axs[axs_count % 3][1 if axs_count > 3 else 0].legend()

    axs_count += 1

fig.tight_layout()
fig.savefig("report/images/anticlockwise_positions.png", dpi=400)