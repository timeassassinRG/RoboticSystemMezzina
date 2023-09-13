import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import networkx as nx

"""
  Algoritmo di path planning da un punto di vista teorico con molti commenti e grafici a supporto
"""


# Genera punti casuali come siti di Voronoi
np.random.seed(np.random.randint(0, 1000))
points = np.random.rand(10, 2)
#points= np.array([(0.25, 0.35), (0.4, 0.05), (0.55, 0.25), (0.75, 0.15)])
# Aggiungi i punti di partenza e arrivo (start e end)
start = np.array([0.2, 0.2])
end = np.array([0.6, 0.6])

# Calcola le distanze tra i punti casuali e i punti di partenza e arrivo
distances_start = np.linalg.norm(points - start, axis=1)
distances_end = np.linalg.norm(points - end, axis=1)

# Scegli una soglia per la distanza minima dai punti di partenza e arrivo
threshold = 0.1

# Filtra i punti troppo vicini ai punti di partenza e arrivo
filtered_points = points[(distances_start > threshold) & (distances_end > threshold)]
removed_points = points[~((distances_start > threshold) & (distances_end > threshold))]

# Creazione della figura con subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# Primo grafico: Start, End e Ostacoli (senza Voronoi)
ax1 = axes[0]
ax1.scatter(filtered_points[:, 0], filtered_points[:, 1], c='k', marker='o', label='Ostacoli')
ax1.plot(start[0], start[1], 'bs', markersize=10, label='Start')
ax1.plot(end[0], end[1], 'gs', markersize=10, label='End')
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
ax2.plot(start[0], start[1], 'bs', markersize=10, label='Start')
ax2.plot(end[0], end[1], 'gs', markersize=10, label='End')
ax2.legend()
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_title("Diagramma di Voronoi con Start ed End")

# Terzo grafico: Start, Punti Voronoi ed End (senza Ostacoli)
ax3 = axes[2]
ax3.scatter(vor.vertices[:, 0], vor.vertices[:, 1], c='orange', marker='o', label='Punti Voronoi')
ax3.plot(start[0], start[1], 'bs', markersize=10, label='Start')
ax3.plot(end[0], end[1], 'gs', markersize=10, label='End')
ax3.legend()
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.set_title("Grafico con Start, Punti Voronoi ed End (senza Ostacoli)")

# Stampa i punti rimossi
print("Punti rimossi:")
if len(removed_points) == 0:
  print("non sono stati rimossi punti")
else:
  for i, point in enumerate(removed_points):
      print(f"Punto {i+1}: {point}")

plt.tight_layout()
plt.show()

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
labels = {node: node if node not in ['start', 'end'] else None for node in G.nodes()}
node_colors = ['b' if node == 'start' else ('r' if node == 'end' else 'g') for node in G.nodes()]

plt.figure(figsize=(8, 8))
nx.draw(G, pos, with_labels=labels, node_size=300, node_color=node_colors, font_size=10)
#plt.xlim(0, 1)
#plt.ylim(0, 1)
plt.show()

print(G.number_of_nodes())
print(list(G.nodes))
source = 'start'
target = 'end'
print(nx.has_path(G, source, target))
# Calcola il cammino minimo da 'start' a 'end' utilizzando l'algoritmo di Dijkstra
shortest_path = nx.shortest_path(G, source, target)
print(shortest_path)

# Crea una nuova figura per il grafo con il cammino minimo evidenziato
plt.figure(figsize=(8, 8))

node_colors = ['r' if node in shortest_path else 'b' for node in G.nodes()]
labels = nx.get_edge_attributes(G, 'weight')
print(labels)
for key, value in labels.items():
  labels[key] = round(value, 2)
print(labels)
nx.draw(G, pos, with_labels=True, node_size=300, node_color = node_colors, font_size = 10, width = 2)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size = 10)

#plt.xlim(0, 1)
#plt.ylim(0, 1)
plt.show()

shortest_path_coordinates = [G.nodes[node]['pos'] for node in shortest_path]
for x,y in shortest_path_coordinates: #OTTENUTI I PUNTI DA FAR SEGUIRE AL ROBOT VIRUTALE
  print(f'Coordinate: ({round(x,2)}, {round(y,2)})')
for x,y in shortest_path_coordinates: #OTTENUTI I PUNTI DA FAR SEGUIRE AL ROBOT VIRUTALE
  print(f'({round(x,2)}, {round(y,2)})')