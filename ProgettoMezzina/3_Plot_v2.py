import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# Genera punti casuali come siti di Voronoi
np.random.seed(np.random.randint(0, 1000))  # Inizializza il generatore di numeri casuali con un seed casuale
points = np.random.rand(20, 2)  # Genera 50 punti casuali con coordinate x e y comprese tra 0 e 1

# Aggiungi i punti di partenza e arrivo (start e end)
start = np.array([0.2, 0.2])  # Coordinate del punto di partenza
end = np.array([0.8, 0.8])    # Coordinate del punto di arrivo

# Calcola le distanze tra i punti casuali e i punti di partenza e arrivo
distances_start = np.linalg.norm(points - start, axis=1)  # Calcola la distanza euclidea tra i punti casuali e il punto di partenza
distances_end = np.linalg.norm(points - end, axis=1)      # Calcola la distanza euclidea tra i punti casuali e il punto di arrivo

# Scegli una soglia per la distanza minima dai punti di partenza e arrivo
threshold = 0.1  # Modifica questa soglia secondo le tue esigenze

# Filtra i punti troppo vicini ai punti di partenza e arrivo
filtered_points = points[(distances_start > threshold) & (distances_end > threshold)]  # Seleziona i punti che superano la soglia
removed_points = points[~((distances_start > threshold) & (distances_end > threshold))]   # Seleziona i punti rimossi

# Creazione della figura con subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Primo grafico: Start, End e Ostacoli (senza Voronoi)
ax1 = axes[0]
ax1.scatter(filtered_points[:, 0], filtered_points[:, 1], c='k', marker='o', label='Ostacoli')
ax1.plot(start[0], start[1], 'bs', markersize=10, label='Start')  # Punto di partenza
ax1.plot(end[0], end[1], 'gs', markersize=10, label='End')        # Punto di arrivo
ax1.legend()
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_title("Grafico con Start, End e Ostacoli (senza Voronoi)")

# Calcola il diagramma di Voronoi con i punti filtrati
vor = Voronoi(filtered_points)

# Secondo grafico: Diagramma di Voronoi con Start e End
ax2 = axes[1]
ax2.plot(filtered_points[:, 0], filtered_points[:, 1], 'ko')
voronoi_plot_2d(vor, ax=ax2, show_vertices=False, line_colors='orange', line_width=2)
ax2.plot(start[0], start[1], 'bs', markersize=10, label='Start')  # Punto di partenza
ax2.plot(end[0], end[1], 'gs', markersize=10, label='End')        # Punto di arrivo
ax2.legend()
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_title("Diagramma di Voronoi con Start ed End")

# Terzo grafico: Start, Punti Voronoi ed End (senza Ostacoli)
ax3 = axes[2]
ax3.scatter(vor.vertices[:, 0], vor.vertices[:, 1], c='orange', marker='o', label='Punti Voronoi')
ax3.plot(start[0], start[1], 'bs', markersize=10, label='Start')  # Punto di partenza
ax3.plot(end[0], end[1], 'gs', markersize=10, label='End')        # Punto di arrivo
ax3.legend()
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.set_title("Grafico con Start, Punti Voronoi ed End (senza Ostacoli)")

# Stampa i punti rimossi
print("Punti rimossi:")
for i, point in enumerate(removed_points):
    print(f"Punto {i+1}: {point}")

plt.tight_layout()
plt.show()