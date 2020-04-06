import numpy as np

radii_units_colors = [
    (2, 120, 'g'),
    (3, 180, 'c'),
    (4, 240, 'm'), 
    (5, 300, 'y'),
    (6, 360, 'k')
]

# for a single simulation run, use mass = 20, r_min = 20
G = 1
clockwise = False
mass_arr = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.8, 2.2, 2.6, 3.0]
r_min_arr = [5, 10, 15, 20, 25, 30, 35, 40]
turns = [1, 2, 3]



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
        
        return self

    def update_speed_position(self, dt):
        self.v_x += dt * self.f_x / self.mass
        self.v_y += dt * self.f_y / self.mass
        self.x += dt * self.v_x
        self.y += dt * self.v_y

        return self


def initialise_moving_body(initial_x, r_min, mass, central_body, clockwise=False):
    # parabolic orbit: y^2 = 4 * r_min^2 - 4 * r_min * x
    moving_x = -50
    moving_y = (1 if clockwise else -1) * 2 * np.sqrt(r_min**2 - r_min * moving_x)
    
    dy_dx = (-1 if clockwise else 1) * r_min / np.sqrt(r_min**2 - r_min * moving_x)
    moving_v_mag = np.sqrt(2 * G * central_body.mass / np.sqrt(moving_x**2 + moving_y**2))
    moving_v_y = dy_dx * moving_v_mag / np.sqrt(1 + dy_dx**2)
    moving_v_x = moving_v_y / dy_dx

    return Body([moving_x, moving_y], [moving_v_x, moving_v_y], mass=mass)

def initialise_test_particles(central_body):
    all_particles = []

    for (radius, num_of_units, color) in radii_units_colors:
        thetas = np.random.rand(num_of_units) * 2 * np.pi
        v_mag = np.sqrt(G * central_body.mass / radius)

        init_x = lambda t : radius * np.cos(t)
        init_y = lambda t : radius * np.sin(t)
        init_v_x = lambda t : -v_mag * np.sin(t)
        init_v_y = lambda t : v_mag * np.cos(t)

        particles = [Body(
            [init_x(theta), init_y(theta)],
            [init_v_x(theta), init_v_y(theta)], 
            mass = 0.01 
        ) for theta in thetas]

        all_particles.append(particles)

    all_particles = [part for radius_particles in all_particles for part in radius_particles]
    return all_particles


def get_positions_from_row(row):
    time = row[0]
    central_x = row[1]
    central_y = row[2]
    moving_x = row[3]
    moving_y = row[4]
    particles_positions = row[5:]
    all_particles_x = [coord for idx, coord in enumerate(particles_positions) if idx % 2 == 0]
    all_particles_y = [coord for idx, coord in enumerate(particles_positions) if idx % 2 == 1]

    particles_xs = []
    particles_ys = []
    index = 0
    for radius, num, color in radii_units_colors:
        particles_xs.append(np.array(all_particles_x[index:index + num]))
        particles_ys.append(np.array(all_particles_y[index:index + num]))
        index += num

    return (time, central_x, central_y, moving_x, moving_y, particles_xs, particles_ys)

