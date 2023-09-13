import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

# Genera punti casuali come siti di Voronoi
np.random.seed(np.random.randint(0, 1000))
points = np.random.rand(50, 2)

# Aggiungi i punti di partenza e arrivo (start e end)
start = np.array([0.2, 0.2])
end = np.array([0.8, 0.8])

# Calcola le distanze tra i punti casuali e i punti di partenza e arrivo
distances_start = np.linalg.norm(points - start, axis=1)
distances_end = np.linalg.norm(points - end, axis=1)

# Scegli una soglia per la distanza minima dai punti di partenza e arrivo
threshold = 0.1  # Modifica questa soglia secondo le tue esigenze

# Filtra i punti troppo vicini ai punti di partenza e arrivo
filtered_points = points[(distances_start > threshold) & (distances_end > threshold)]
removed_points = points[~((distances_start > threshold) & (distances_end > threshold))]

# Plotta il grafico con start, end e tutti gli ostacoli (senza effettuare Voronoi)
plt.figure(1)
plt.scatter(filtered_points[:, 0], filtered_points[:, 1], c='k', marker='o', label='Ostacoli')
plt.plot(start[0], start[1], 'bs', markersize=10, label='Start')  # Punto di partenza
plt.plot(end[0], end[1], 'gs', markersize=10, label='End')  # Punto di arrivo
plt.legend()
plt.title("Grafico con Start, End e Ostacoli (senza Voronoi)")

# Plotta il diagramma di Voronoi
plt.figure(2)
vor = Voronoi(filtered_points)
ax = plt.subplot()
ax.plot(filtered_points[:, 0], filtered_points[:, 1], 'ko')
voronoi_plot_2d(vor, ax=ax)
plt.plot(start[0], start[1], 'bs', markersize=10, label='Start')  # Punto di partenza
plt.plot(end[0], end[1], 'gs', markersize=10, label='End')  # Punto di arrivo
plt.legend()
plt.title("Diagramma di Voronoi con Start e End")

# Plotta il grafico con start, punti Voronoi ed end (senza ostacoli)
plt.figure(3)
plt.scatter(vor.vertices[:, 0], vor.vertices[:, 1], c='k', marker='o', label='Punti Voronoi')
plt.plot(start[0], start[1], 'bs', markersize=10, label='Start')  # Punto di partenza
plt.plot(end[0], end[1], 'gs', markersize=10, label='End')  # Punto di arrivo
plt.legend()
plt.title("Grafico con Start, Punti Voronoi ed End (senza Ostacoli)")

# Stampa i punti rimossi
print("Punti rimossi:")
for i, point in enumerate(removed_points):
    print(f"Punto {i+1}: {point}")

plt.show()
