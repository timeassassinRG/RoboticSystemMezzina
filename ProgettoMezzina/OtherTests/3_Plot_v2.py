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

import networkx as nx

# Crea un grafo vuoto con NetworkX
G = nx.Graph()

# Aggiungi i vertici del diagramma di Voronoi come nodi al grafo
for i, vertex in enumerate(vor.vertices):
    G.add_node(i, pos=vertex)

# Aggiungi gli archi tra i nodi vicini nel diagramma di Voronoi come archi pesati
for ridge in vor.ridge_vertices:
    if -1 not in ridge:
        distance = np.linalg.norm(vor.vertices[ridge[0]] - vor.vertices[ridge[1]])
        G.add_edge(ridge[0], ridge[1], weight=distance)

# Aggiungi i punti di partenza e arrivo come nodi al grafo
G.add_node('start', pos=tuple(start))
G.add_node('end', pos=tuple(end))

# Collega i punti di partenza e arrivo ai vertici più vicini nel diagramma di Voronoi
start_index = np.argmin(np.linalg.norm(vor.vertices - start, axis=1))
end_index = np.argmin(np.linalg.norm(vor.vertices - end, axis=1))

G.add_edge('start', start_index, weight=np.linalg.norm(start - vor.vertices[start_index]))
G.add_edge('end', end_index, weight=np.linalg.norm(end - vor.vertices[end_index]))

# Disegna il grafo
pos = nx.get_node_attributes(G, 'pos')
labels = {node: node if node not in ['start', 'end'] else None for node in G.nodes()}  # Labels con None per 'start' ed 'end'
node_colors = ['b' if node == 'start' else ('r' if node == 'end' else 'g') for node in G.nodes()]

plt.figure(figsize=(8, 8))
nx.draw(G, pos, with_labels=labels, node_size=300, node_color=node_colors, font_size=10)
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()