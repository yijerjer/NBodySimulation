import numpy as np
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
fig, axs = plt.subplots(figsize=(5, 4))

mass_data = np.loadtxt("plots/mass_data.csv")
mass_data = np.transpose(mass_data)

rmin_data = np.loadtxt("plots/rmin_data.csv")
rmin_data = np.transpose(rmin_data)

# radii_units_colors = [
#     (2, 120, 'g'),
#     (3, 180, 'c'),
#     (4, 240, 'm'), 
#     (5, 300, 'y'),
#     (6, 360, 'k')
# ]

# for i in range(0, 5):
#     axs.errorbar(
#         mass_data[0], mass_data[2*i + 1] / radii_units_colors[i][1], yerr=mass_data[2*i + 2] / radii_units_colors[i][1], 
#         marker=None, linewidth=0.2, elinewidth=1, capsize=2, 
#         color=radii_units_colors[i][2], label=rf"$r = {radii_units_colors[i][0]}$"
#     )

# axs.errorbar(
#     mass_data[0], mass_data[11] / 1200, yerr=mass_data[12] / 1200, 
#     marker=None, linewidth=0.2, elinewidth=1, capsize=2, 
#     label="mass"
# )

axs.errorbar(
    rmin_data[0], rmin_data[11] / 1200, yerr=rmin_data[12] / 1200, 
    marker=None, linewidth=0.2, elinewidth=1, capsize=2, 
    label="rmin"
)

axs.legend()
axs.set_xlabel("Mass of perturbing galaxy / units")
axs.set_ylabel("Fraction of disturbed stars")
fig.tight_layout()
# fig.savefig("report/images/test.png", dpi=400)
plt.show()