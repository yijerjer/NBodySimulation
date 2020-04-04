import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

radii_units_colors = [
    (2, 120, 'g'),
    (3, 180, 'c'),
    (4, 240, 'm'), 
    (5, 300, 'y'),
    (6, 360, 'k')
]

with open("data/plot_mass.csv", "w+") as file:

    for r_min in [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.8, 2.2, 2.6, 3.0]:
        all_averages = np.zeros([len(radii_units_colors), 3])
        for turn in [1, 2, 3]:

            print("Reading file...")
            positions = pd.read_csv(f"data/null_ac_positions_mass_{r_min}_{turn}.csv", delimiter=",")
            print("File read.")

            snapshot_row = 4550

            final_row = positions.iloc[snapshot_row]
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
                # plt.hist(distance_to_central, 50)
                # plt.show()
                average = np.average(distance_to_central)
                std = np.std(distance_to_central)
                all_averages[idx][turn - 1] = average

                disturbed = [dist for dist in distance_to_central if dist > (radius + 0.5) or dist < (radius - 0.5)]
                print(f"Disturbed particles for radius {radius}: {len(disturbed)}/{num}")
                print(f"Average: {average}, Std: {std}")

            
            distance_to_moving = np.sqrt(np.square(np.array(all_test_particles_x) - moving_x) + np.square(np.array(all_test_particles_y) - moving_y))
            moving_orbit = [dist for dist in distance_to_moving if dist < 8]
            print(f"Particles orbiting perturbing galaxy: {len(moving_orbit)}/{len(distance_to_moving)}")
        
        all_averages = np.average(all_averages, axis=1)
        all_averages = [str(av) for av in all_averages]
        row = f"{r_min},{','.join(all_averages)} \n"
        file.write(row)

    plt.show()
