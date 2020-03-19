import matplotlib.pyplot as plt
import numpy as np

class Body:
    def __init__(self, mass, x=0, y=0, G=1):
        self.mass = mass
        self.x = x
        self.y = y


class TestParticle:
    def __init__(self, velocity, mass=1, init_x=0, init_y=0, G=1):
        self.mass = mass
        self.G = G
        self.x = init_x
        self.y = init_y
        self.v_x = velocity[0]
        self.v_y = velocity[1]
        self.f_x = 0
        self.f_y = 0

    def set_gforce(self, body):
        d_x = body.x - self.x
        d_y = body.y - self.y
        distance = np.sqrt(d_x**2 + d_y**2)
        force_mag = self.G * body.mass * self.mass / distance**2
        f_x = force_mag * d_x / distance
        f_y = force_mag * d_y / distance

        self.f_x = f_x
        self.f_y = f_y

    def update_speed_position(self, dt):
        self.v_x += dt * self.f_x / self.mass
        self.v_y += dt * self.f_y / self.mass
        self.x += dt * self.v_x
        self.y += dt * self.v_y

radii_and_units = [
    (2, 12),
    (3, 18),
    (4, 24), 
    (5, 30),
    (6, 36)
]

all_particles = []

G = 1
body = Body(1)
for (radius, num_of_units) in radii_and_units:
    print(num_of_units)
    thetas = np.random.rand(num_of_units) * 2 * np.pi
    v_mag = np.sqrt(G * body.mass / radius)
    init_x = lambda t : radius * np.cos(t)
    init_y = lambda t : radius * np.sin(t)
    init_v_x = lambda t : -v_mag * np.sin(t)
    init_v_y = lambda t : v_mag * np.cos(t)

    particles = [TestParticle(
        [init_v_x(theta), init_v_y(theta)], 
        mass = 0.01, 
        init_x = init_x(theta), 
        init_y = init_y(theta),
    ) for theta in thetas]

    all_particles.append(particles)


dt = 0.01
t = 0
t_arr = []
x_arr = []
y_arr = []
test = all_particles[1][0]

while (t < 1000):
    test.set_gforce(body)
    test.update_speed_position(dt)
    t_arr.append(t)
    x_arr.append(test.x)
    y_arr.append(test.y)
    t += dt

plt.plot(x_arr, y_arr)
plt.show()

