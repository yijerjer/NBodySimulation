import matplotlib.pyplot as plt
import numpy as np


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

# radii_and_units = [
#     (2, 12),
#     (3, 18),
#     (4, 24), 
#     (5, 30),
#     (6, 36)
# ]

# init_x = lambda t : radius * np.cos(t)
# init_y = lambda t : radius * np.sin(t)
# init_v_x = lambda t : -v_mag * np.sin(t)
# init_v_y = lambda t : v_mag * np.cos(t)

# all_particles = []

# for (radius, num_of_units) in radii_and_units:
#     print(num_of_units)
#     thetas = np.random.rand(num_of_units) * 2 * np.pi
#     v_mag = np.sqrt(G * central_body.mass / radius)

#     particles = [Body(
#         [init_x(theta), init_y(theta)],
#         [init_v_x(theta), init_v_y(theta)], 
#         mass = 0.01 
#     ) for theta in thetas]

#     all_particles.append(particles)


# dt = 0.01

# for particles_in_radius in all_particles:
#     for particle in particles_in_radius:
#         t_arr = []
#         x_arr = []
#         y_arr = []
#         t = 0
#         while (t < 100):
#             particle.set_gforce([central_body])
#             particle.update_speed_position(dt)
#             t_arr.append(t)
#             x_arr.append(particle.x)
#             y_arr.append(particle.y)
#             t += dt
#         plt.plot(x_arr, y_arr)


# plt.show()

# parabolic orbit: y^2 = 4 * r_min^2 - 4 * r_min * x
# r_min = 10
# moving_mass = 1
# moving_x = -50
# moving_y = -2 * np.sqrt(r_min**2 - r_min * moving_x)
# dy_dx = r_min / np.sqrt(r_min**2 - r_min * moving_x)
# moving_v_mag = np.sqrt(2 * G * central_body.mass / np.sqrt(moving_x**2 + moving_y**2))
# moving_v_y = dy_dx * moving_v_mag / np.sqrt(1 + dy_dx**2)
# moving_v_x = moving_v_y / dy_dx
# moving_body = Body([moving_x, moving_y], [moving_v_x, moving_v_y], mass=1)

# dt = 0.01
# t = 0

# t_arr = []
# x_arr = []
# y_arr = []

# while (t < 1000):
#     moving_body.set_gforce([central_body])
#     moving_body.update_speed_position(dt)
#     t_arr.append(t)
#     x_arr.append(moving_body.x)
#     y_arr.append(moving_body.y)
#     t += dt

# plt.plot(x_arr, y_arr)
# plt.show()