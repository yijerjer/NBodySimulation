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

for val in [2.2, 2.6, 3.0]:
    dists = np.zeros([6, 3])
    for turn in [1, 2, 3]:

        # using pandas because 36.56730818748474 vs 110.98377823829651
        print("Reading file...")
        positions = pd.read_csv(f"positions_mass{val}_{turn}.csv", delimiter=",")
        print("File read.")
        
        print("VAL" + str(val))

        # snapshot_rows = np.linspace(len(positions)/13, len(positions)/5 - 1, 5, dtype=int)
        snapshot_rows = [6000]
        snapshot_positions = positions.iloc[snapshot_rows,:]

        # fig, axs = plt.subplots(6, 1, figsize=(7, 20))
        # axs_count = 0

        # for idx, row in snapshot_positions.iterrows():
        #     time = row[0]
        #     central_x = row[1]
        #     central_y = row[2]
        #     moving_x = row[3]
        #     moving_y = row[4]
        #     test_particles_positions = row[5:]
        #     all_test_particles_x = [coord for idx, coord in enumerate(test_particles_positions) if idx % 2 == 0]
        #     all_test_particles_y = [coord for idx, coord in enumerate(test_particles_positions) if idx % 2 == 1]

        #     test_particles_xs = []
        #     test_particles_ys = []
        #     index = 0
        #     for (radius, num, color) in radii_units_colors:
        #         test_particles_xs.append(all_test_particles_x[index:index + num])
        #         test_particles_ys.append(all_test_particles_y[index:index + num])
        #         index += num

            # plt.clf()
            # plt.scatter(central_x, central_y, color='b')
            # plt.scatter(moving_x, moving_y, color='r')
            # for idx, (radius, num, color) in enumerate(radii_units_colors):
            #     plt.scatter(test_particles_xs[idx], test_particles_ys[idx], s=1, color=color)
                
            # plt.xlim([-100, 100])
            # plt.ylim([-100, 100])
            # plt.show()
            # plt.pause(0.01)

            # axs[axs_count].scatter(central_x, central_y, color='b')
            # axs[axs_count].scatter(moving_x, moving_y, color='r')
            # for unit_idx, (color, num) in enumerate(radii_units_colors):
            #     axs[axs_count].scatter(test_particles_xs[unit_idx], test_particles_ys[unit_idx], s=1, color=color)
                
            # axs[axs_count].set_xlim([-100, 100])
            # axs[axs_count].set_ylim([-100, 100])
            # axs[axs_count].set_title(f"t = {time}, index = {idx}")
            # axs_count += 1

        # fig.savefig("c_positions.pdf")

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
        for radius, num, color in radii_units_colors:
            test_particles_xs.append(np.array(all_test_particles_x[index:index + num]))
            test_particles_ys.append(np.array(all_test_particles_y[index:index + num]))
            index += num

        for idx, (radius, num, color) in enumerate(radii_units_colors):
            distance_to_central = np.sqrt(np.square(test_particles_xs[idx] - central_x) + np.square(test_particles_ys[idx] - central_y))
            disturbed = [dist for dist in distance_to_central if dist > (radius + 0.5) or dist < (radius - 0.5)]
            print(f"Disturbed particles for radius {radius}: {len(disturbed)}/{num}")

            dists[idx][turn - 1] = len(disturbed)
            
        distance_to_moving = np.sqrt(np.square(np.array(all_test_particles_x) - moving_x) + np.square(np.array(all_test_particles_y) - moving_y))
        print(len(distance_to_moving))

        moving_orbit = [dist for dist in distance_to_moving if dist < 8]
        print(len(moving_orbit))
        dists[5][turn - 1] = len(moving_orbit)
    
    print(dists)
    dists_average = [np.average(dist) for dist in dists]
    dists_std = [np.std(dist) for dist in dists]
    print(dists_average)
    print(dists_std / np.sqrt(3))
    print()