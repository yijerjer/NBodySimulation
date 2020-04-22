# Tidal Tails: N Body Simulation
### A computational project for Part II Physics at University of Cambridge

#### Summary of the contents of `.py` files:
* `core.py` : 
   
    Contains `Body` class which is used to represents the massive bodies and massless test particles, and `initialise...` methods to determine initial conditions of the perturbing galaxy and test particles. 
    
    It also contains commonly used lists and constants. These lists can be tweaked to change the number of repeats of the simulation and the variables of the simulation.

* `simulation.py`

    The simulation of the interaction between bodies and particles are located here. The results of the simulation are written to the `data/` folder. It requires an argument of either `single` (a single simulation run), `rmin` (multiple simulations at different `r_min` values) or `mass` (multiple simulations at different `mass` values).

* `animation.py` and `snapshots.py`

    These two files are very similar. The first creates a simple animation of the simulation with `matplotlib`, whilst the second creates a plot of 6 scatter graphs (snapshots) at different times. It requires an argument of the data file name in the `data/` folder.

* `get_quantitative.py` and `plot_quantitative.py`

    The former extracts quantitative details, such as the number of perturbed test particles and the average distance of stars to the central galaxy from the results of the simulation. The latter uses the extracted quantitative details to plot relevant graphs. It requires an argument of either `rmin` or `mass` to plot the relevant graphs.
   


   
