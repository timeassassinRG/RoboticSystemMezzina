import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

# Genera punti casuali come siti di Voronoi
np.random.seed(1234)
points = np.random.rand(20, 2)
print(points)

# Calcola il diagramma di Voronoi
vor = Voronoi(points)

# Plotta il diagramma di Voronoi
fig, ax = plt.subplots()
ax.plot(points[:, 0], points[:, 1], 'ko')
voronoi_plot_2d(vor, ax=ax)
plt.show()
