from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import numpy as np

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

class Der:
    def __init__(self, m):
        self.m = m

    def derivatives(self, t, vals):
        # vals = [x0, y0, x1, y1, m1_x0, m1_y0, m1_x1, m1_y1, m2_x0, m2_y0, m2_x1, m2_y1]
        r_1 = np.sqrt(np.square(vals[0] - 0) + np.square(vals[1] - 0))
        r_2 = np.sqrt(np.square(vals[0] - 0) + np.square(vals[1] - 0))
        x0_derivative = vals[2]
        y0_derivative = vals[3]
        x1_derivative = -self.m[0]*(vals[0] - 0)/r_1**3 - self.m[1]*(vals[0] - 0)/r_2**3
        y1_derivative = -self.m[0]*(vals[1] - 0)/r_1**3 - self.m[1]*(vals[1] - 0)/r_2**3
        # m1_x0_derivative = vals[6]
        # m1_y0_derivative = vals[7]
        # m2_x0_derivative = vals[10]
        # m2_y0_derivative = vals[11]
        # m1_x1_derivative = 
        # m1_y1_derivative = 0
        # m2_x1_derivative = 0
        # m2_y1_derivative = 0

        return (x0_derivative, y0_derivative, x1_derivative, y1_derivative) # , m1_x0_derivative, m1_y0_derivative, m1_x1_derivative, m1_y1_derivative, m2_x0_derivative, m2_y0_derivative, m2_x1_derivative, m2_y1_derivative)

    def solve(self, initial_conditions):
        sol = solve_ivp(self.derivatives, [0, 20], initial_conditions, t_eval=np.linspace(0, 20, 10e4))
        return sol


der = Der([1, 0])
sol = der.solve([1, 0, 0, 1])

fig, axs = plt.subplots(figsize=(5, 4))
axs.plot(sol.y[0], sol.y[1])
axs.set_xlabel("x")
axs.set_ylabel("y")
fig.tight_layout()
fig.savefig("report/images/RK45.png", dpi=500)

# print(len(sol.t) / 100)

# for idx in range(int(len(sol.t) / 100)):
#     plt.clf()
#     plt.scatter(sol.y[0][idx * 100], sol.y[1][idx * 10])
#     plt.scatter(sol.y[4][idx * 100], sol.y[5][idx * 10])
#     plt.scatter(sol.y[8][idx * 100], sol.y[9][idx * 10])
#     plt.pause(0.01)


