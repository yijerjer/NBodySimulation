import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("data/plot_mass.csv", delimiter=',')
data = np.transpose(data)
print(data)

for i in range(1, 6):
    plt.plot(data[0], data[i])

plt.show()