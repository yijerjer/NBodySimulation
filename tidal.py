import matplotlib.pyplot as plt
import numpy as np
import datetime


G = 1

class Body:
    def __init__(self, position, velocity, mass=1, G=G):
        self.mass = mass
        self.G = G
        self.x = position[0]
        self.y = position[1]
        self.v_x = velocity[0]
        self.v_y = velocity[1]
        self.f_x = 0
        self.f_y = 0

    def set_gforce(self, bodies):
        self.f_x = 0
        self.f_y = 0

        for body in bodies:
            d_x = body.x - self.x
            d_y = body.y - self.y
            distance = np.sqrt(d_x**2 + d_y**2)
            force_mag = self.G * body.mass * self.mass / distance**2
            self.f_x += force_mag * d_x / distance
            self.f_y += force_mag * d_y / distance

    def update_speed_position(self, dt):
        self.v_x += dt * self.f_x / self.mass
        self.v_y += dt * self.f_y / self.mass
        self.x += dt * self.v_x
        self.y += dt * self.v_y


central_body = Body([0, 0], [0, 0], mass=1)

radii_and_units = [
    (2, 12),
    (3, 18),
    (4, 24), 
    (5, 30),
    (6, 36)
]

init_x = lambda t : radius * np.cos(t)
init_y = lambda t : radius * np.sin(t)
init_v_x = lambda t : -v_mag * np.sin(t)
init_v_y = lambda t : v_mag * np.cos(t)

all_particles = []

for (radius, num_of_units) in radii_and_units:
    print(num_of_units)
    thetas = np.random.rand(num_of_units) * 2 * np.pi
    v_mag = np.sqrt(G * central_body.mass / radius)

    particles = [Body(
        [init_x(theta), init_y(theta)],
        [init_v_x(theta), init_v_y(theta)], 
        mass = 0.01 
    ) for theta in thetas]

    all_particles.append(particles)



# parabolic orbit: y^2 = 4 * r_min^2 - 4 * r_min * x
r_min = 20
moving_mass = 1
moving_x = -50
moving_y = -2 * np.sqrt(r_min**2 - r_min * moving_x)
dy_dx = r_min / np.sqrt(r_min**2 - r_min * moving_x)
moving_v_mag = np.sqrt(2 * G * central_body.mass / np.sqrt(moving_x**2 + moving_y**2))
moving_v_y = dy_dx * moving_v_mag / np.sqrt(1 + dy_dx**2)
moving_v_x = moving_v_y / dy_dx
moving_body = Body([moving_x, moving_y], [moving_v_x, moving_v_y], mass=1)

dt = 0.01
t = 0

t_arr = []
central_x_arr = []
central_y_arr = []
moving_x_arr = []
moving_y_arr = []
particles_x_arrs = []
particles_y_arrs = []
for radius, num_of_units in radii_and_units:
    particles_x_arrs.append([[]] * num_of_units)
    particles_y_arrs.append([[]] * num_of_units)

datetime_now = datetime.datetime.now().strftime("%H:%M:%S %Y-%m-%d")
with open(f"{datetime_now}-position-data.csv", "w+") as file:
    header = "central_x,central_y,moving_x,moving_y"
    for radius, num_of_units in radii_and_units:
        header_str = ",".join([f"particle_{radius}_{i}_x,particle_{radius}_{i}_y" for i in range(num_of_units)])
        header += "," + header_str
    
    file.write(header + "\n")

    count = 0
    while (t < 5000):
        t_arr.append(t)

        row = ""
        
        central_body.set_gforce([moving_body])
        central_body.update_speed_position(dt)
        # central_x_arr.append(central_body.x)
        # central_y_arr.append(central_body.y)
        row += str(central_body.x) + "," + str(central_body.y)
        
        moving_body.set_gforce([central_body])
        moving_body.update_speed_position(dt)
        # moving_x_arr.append(moving_body.x)
        # moving_y_arr.append(moving_body.y)
        row += "," + str(moving_body.x) + "," + str(moving_body.y)

        for i, radius_particles in enumerate(all_particles):
            for j, particle in enumerate(radius_particles):
                particle.set_gforce([central_body, moving_body])
                particle.update_speed_position(dt)
                row += "," + str(particle.x) + "," + str(particle.y)
                # particles_x_arrs[i][j].append(particle.x)
                # particles_y_arrs[i][j].append(particle.y)

        file.write(row)

        t += dt
        if count % 500 == 0:
            # plt.clf()
            # plt.scatter(moving_x_arr[-1], moving_y_arr[-1], color='r')
            # plt.scatter(central_x_arr[-1], central_y_arr[-1], color='b')
            # plt.scatter(particles_x_arrs[0][0][-1], particles_y_arrs[0][0][-1], color='g', s=5)
            # plt.ylim([-100, 100])
            # plt.xlim([-100, 100])
            # plt.pause(0.01)
            print(t)

        count += 1
        
    
# plt.title("Done")
# plt.plot(moving_x_arr, moving_y_arr, color='r')
# plt.plot(central_x_arr, central_y_arr, color='b')
# plt.show()