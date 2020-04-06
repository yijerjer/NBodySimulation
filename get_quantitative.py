import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from core import radii_units_colors, r_min_arr, mass_arr, turns
from core import get_positions_from_row


try:
    if len(sys.argv) < 2 or sys.argv[1] not in ["rmin", "mass"]:
        raise OSError("An argument of 'rmin' or 'mass' needs to be provided in order to read the data")

    variable_type = sys.argv[1]
    variable_arr = r_min_arr if variable_type == "rmin" else mass_arr
    
    with open(f"data/quantitative_{variable_type}.csv", "w+") as file:

        for val in variable_arr:
            all_radii = np.zeros([len(radii_units_colors), 3])
            all_averages = np.zeros([len(radii_units_colors), 3])

            for turn in turns:
                print(f"Reading file ... (type: {variable_type}, value: {val}, Turn: {turn})")
                positions = pd.read_csv(f"data/positions_{variable_type}_{val}_{turn}.csv", delimiter=",")
                print("File read.")

                positions["pos_difference"] = np.sqrt(np.square(positions.central_x - positions.moving_x) + np.square(positions.central_y - positions.moving_y))
                closest_approach = positions[positions.pos_difference == positions.pos_difference.min()].iloc[0]

                # this snapshot is at approximately t = 50 units
                snapshot_row = closest_approach.name + 1000
                if snapshot_row > len(positions):
                    continue
                row = positions.iloc[snapshot_row]
                (time, central_x, central_y, moving_x, moving_y, particles_xs, particles_ys) = get_positions_from_row(row)

                for idx, (radius, num, color) in enumerate(radii_units_colors):
                    distance_to_central = np.sqrt(np.square(particles_xs[idx] - central_x) + np.square(particles_ys[idx] - central_y))
                    average = np.median(distance_to_central)
                    all_averages[idx][turn - 1] = average

                    disturbed_number = len([dist for dist in distance_to_central if dist > (radius + 0.5) or dist < (radius - 0.5)])
                    disturbed_frac = disturbed_number / num
                    all_radii[idx][turn - 1] = disturbed_frac
                    
                    print(f"RADIUS: {radius} - No. of disturbed particles: {disturbed_number}/{num}, Average distance: {average}")
                
            
            av_of_averages = np.average(all_averages, axis=1)
            err_of_averages = np.std(all_averages, axis=1) / np.sqrt(len(turns))
            av_of_averages = [str(av) for av in av_of_averages]
            err_of_averages = [str(std) for std in err_of_averages]

            av_of_radii = np.average(all_radii, axis=1)
            err_of_radii = np.std(all_radii, axis=1) / np.sqrt(len(turns))
            av_of_radii = [str(av) for av in av_of_radii]
            err_of_radii = [str(std) for std in err_of_radii]
            
            row = f"{val}"
            for av_std_arr in [av_of_averages, err_of_averages, av_of_radii, err_of_radii]:
                row += "," + ','.join(av_std_arr)
            row += "\n"
            file.write(row)
    
    print(f"Created file data/quantitative_{variable_type}.csv")

except OSError as e:
    print(repr(e))