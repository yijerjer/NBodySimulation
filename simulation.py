import os
import time
import sys
import matplotlib.pyplot as plt
import numpy as np
from core import Body, initialise_moving_body, initialise_test_particles
from core import G, turns, r_min_arr, mass_arr, radii_units_colors, clockwise


try:
    if len(sys.argv) < 2 or sys.argv[1] not in ["rmin", "mass", "single"]:
        raise OSError("An argument of 'single', 'rmin' or 'mass' needs to be provided in order to read the data")

    variable_type = sys.argv[1]
    variable_arr = []
    if variable_type == "single":
        variable_arr = [0]
        turns = [0]
    else:
        variable_arr = r_min_arr if variable_type == "rmin" else mass_arr
    
    if not os.path.isdir('data/'):
        os.mkdir('data')
    
    for val in variable_arr:
        for turn in turns:
            print(f"Simulating {variable_type}: {val}, turn: {turn}")
            start = time.time()

            # initialising the central galaxy
            central_body = Body([0, 0], [0, 0], mass=1)

            # initialising the perturbing galaxy
            r_min = 20
            moving_mass = 1
            if variable_type != "single":
                r_min = val if variable_type == "rmin" else 20
                moving_mass = val if variable_type == "mass" else 1
                
            moving_body = initialise_moving_body(-40, r_min, moving_mass, central_body, clockwise=clockwise)

            # initialising the test particles
            all_particles = initialise_test_particles(central_body)

            dt = 0.1
            t = 0
            t_max = 700

            with open(f"data/positions_{'clockwise_' if clockwise else ''}{variable_type}_{val}_{turn}.csv", "w+") as file:
                header = "time,central_x,central_y,moving_x,moving_y"
                for radius, num_of_units, color in radii_units_colors:
                    header_str = ",".join([f"particle_{radius}_{i}_x,particle_{radius}_{i}_y" for i in range(num_of_units)])
                    header += "," + header_str
                file.write(header + "\n")

                count = 0
                while (t < t_max):
                    row = str(t) + ","
                    
                    # update the force, position and velocity of the central galaxy
                    central_body.set_gforce([moving_body])
                    central_body.update_speed_position(dt)
                    row += str(central_body.x) + "," + str(central_body.y)
                    
                    # update the force, position and velocity of the perturbing galaxy
                    moving_body.set_gforce([central_body])
                    moving_body.update_speed_position(dt)
                    row += "," + str(moving_body.x) + "," + str(moving_body.y)

                    # update the force, position and velocity of all the test particles
                    all_particles = [part.set_gforce([central_body, moving_body]) for part in all_particles]
                    all_particles = [part.update_speed_position(dt) for part in all_particles]
                    particle_positions = [str(part.x) + "," + str(part.y) for part in all_particles]
                    row += "," + ",".join(particle_positions)

                    file.write(row + "\n")

                    t += dt
                    if count % 1000 == 0:
                        print(f"Simulation at t = {int(t)} / {t_max} units")

                    count += 1

            end = time.time()
            print(f"Time taken for simulation: {end - start} \n")

except OSError as e:
    print(repr(e))