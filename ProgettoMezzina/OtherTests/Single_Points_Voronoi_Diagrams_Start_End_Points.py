import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

# Genera punti casuali come siti di Voronoi
np.random.seed(123)
points = np.random.rand(50, 2)

# Aggiungi i punti di partenza e arrivo (start e end)
start = np.array([0.2, 0.2])
end = np.array([0.8, 0.8])
points = np.vstack((points))

# Calcola il diagramma di Voronoi
vor = Voronoi(points)

# Plotta il diagramma di Voronoi
fig, ax = plt.subplots()
ax.plot(points[:, 0], points[:, 1], 'ko')
voronoi_plot_2d(vor, ax=ax)
plt.plot(start[0], start[1], 'bs', markersize=10, label='Start')  # Punto di partenza
plt.plot(end[0], end[1], 'gs', markersize=10, label='End')  # Punto di arrivo
plt.legend()
plt.show()