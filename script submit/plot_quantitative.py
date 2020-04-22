import sys
import matplotlib.pyplot as plt
import numpy as np
from core import radii_units_colors

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

try:
    if len(sys.argv) < 2 or sys.argv[1] not in ["rmin", "mass"]:
        raise OSError("An argument of 'rmin' or 'mass' needs to be provided in order to plot the graphs.")
    
    variable_type = sys.argv[1]
    
    data = np.loadtxt(f"data/quantitative_{variable_type}.csv", delimiter=',')
    data = np.transpose(data)
    print(data)

    fig1, axs1 = plt.subplots(figsize=(5, 4))
    fig2, axs2 = plt.subplots(figsize=(5, 4))

    for i, (r, u, color) in enumerate(radii_units_colors):
        axs1.errorbar(
            data[0], data[i + 1], yerr=data[i + 6], label=rf"$r = {r}$",
            elinewidth=1, linewidth=0.2, capsize=2, marker='o', ms='2', color=color
        )
        axs2.errorbar(
            data[0], data[i + 11], yerr=data[i + 16], label=rf"$r = {r}$",
            elinewidth=1, linewidth=0.2, capsize=2, marker='o', ms='2', color=color
        )

    if variable_type == "mass":
        axs1.set_xlabel("Mass of perturbing galaxy / units")
        axs2.set_xlabel("Mass of perturbing galaxy / units")
    elif variable_type == "rmin":
        axs1.set_xlabel("Distance of closest approach / units")
        axs2.set_xlabel("Distance of closest approach / units")

    axs1.set_ylabel("Median distance from central galaxy / units")
    axs2.set_ylabel("Fraction of disturbed stars / units")
    axs1.legend()
    axs2.legend()
    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig(f"report/images/plot_distance_{variable_type}.png", dpi=400)
    fig2.savefig(f"report/images/plot_fraction_{variable_type}.png", dpi=400)

except OSError as e:
    print(repr(e))