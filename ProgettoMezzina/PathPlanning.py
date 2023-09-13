import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import networkx as nx

class PathPlanning:
    def __init__(self, start, obstacles):
        self.start = start  # Posizione iniziale
        self.obstacles = obstacles #impostiamo gli ostacoli fissi
        self.checkpoints = []  # Destinazioni
        self.graph = nx.Graph()  # Grafo di Voronoi
        self.vor = None  # Diagramma di Voronoi
        
        self._compute_voronoi()  # Calcola il diagramma di Voronoi
        self._update_graph()  # Calcola il grafo di Voronoi


    def set_start(self, start_position):
        self.start = start_position

    def add_goal(self, goal_position):
        self.checkpoints.append(goal_position)
    
    def clear_goals(self):
        self.checkpoints = []

    def _compute_voronoi(self):
        # Calcola il diagramma di Voronoi tenendo in considerazione gli ostacoli
        self.vor = Voronoi(self.obstacles)
        # Aggiungi i vertici del diagramma di Voronoi come nodi al grafo
        for i, vertex in enumerate(self.vor.vertices):
            self.graph.add_node(i, pos=vertex)
        #aggiungiamo gli archi tra i nodi vicini nel diagramma di Voronoi come archi pesati
        for ridge in self.vor.ridge_vertices:
            if -1 not in ridge:
                distance = np.linalg.norm(self.vor.vertices[ridge[0]] - self.vor.vertices[ridge[1]])
                self.graph.add_edge(ridge[0], ridge[1], weight=distance)

    def _new_graph(self):
        self.graph = nx.Graph()
        self._compute_voronoi()
        self._update_graph()

    def _update_graph(self):
        # Aggiungi il punto di partenza al grafo
        self.graph.add_node('start', pos=tuple(self.start))
        # Collega i punti di partenza e arrivo ai vertici più vicini nel diagramma di Voronoi
        start_index = np.argmin(np.linalg.norm(self.vor.vertices - self.start, axis=1))
        self.graph.add_edge('start', start_index, weight=np.linalg.norm(self.start - self.vor.vertices[start_index]))

        # Aggiungi i checkpoint come nodi al grafo
        for i, checkpoint in enumerate(self.checkpoints):
            node_name = 'checkpoint ' + str(i)
            self.graph.add_node(node_name, pos=tuple(checkpoint))
            # Trova il vertice più vicino nel diagramma di Voronoi per il checkpoint
            checkpoint_index = np.argmin(np.linalg.norm(self.vor.vertices - checkpoint, axis=1))
            # Collega il checkpoint al vertice più vicino nel diagramma di Voronoi
            self.graph.add_edge(node_name, checkpoint_index, weight=np.linalg.norm(checkpoint - self.vor.vertices[checkpoint_index]))
      
    def plot_graph(self): # only per test
        #self._update_graph() #per essere sicuri che il grafo sia stato computato
        pos = nx.get_node_attributes(self.graph, 'pos')
        labels = {node: node if node not in ['start', 'checkpoint'] else None for node in self.graph.nodes()}
        node_colors = ['b' if node == 'start' else ('r' if node == 'checkpoint' else 'g') for node in self.graph.nodes()]
        plt.figure(figsize=(8, 8))
        nx.draw(self.graph, pos, with_labels=labels, node_size=300, node_color=node_colors, font_size=10)
        plt.show()

    def find_path(self):
        if self.start is None or not self.checkpoints:
            raise ValueError("Start and at least one checkpoint must be set before finding a path.") 
        source = 'start'
        target = 'checkpoint 0'
        if not nx.has_path(self.graph, source, target):
            print("No path found.")
            return None
        shortest_path = nx.shortest_path(self.graph, source, target, weight='weight')
        shortest_path_coordinates = [tuple(round(coord, 2) for coord in self.graph.nodes[node]['pos']) for node in shortest_path]
        return shortest_path_coordinates

    def reached_checkpoint(self, index=0):
        self.set_start(self.checkpoints[index])
        del self.checkpoints[index]
        self._new_graph()

if __name__ == '__main__':
    '''
    #esempio di utilizzo facendo finta di aver raggiunto i punti
    start_pos = np.array([0.2, 0.2])
    obstacles = np.array([(0.25, 0.35), (0.4, 0.05), (0.55, 0.25), (0.75, 0.15), (0.80, 0.35)])
    path_planner = PathPlanning(start_pos, obstacles)
    path_planner.plot_graph()
    path_planner.add_goal(np.array([0.5, 0.5]))
    path_planner.add_goal(np.array([1,1]))
    path_planner.add_goal(np.array([0.1, 0.1]))
    path_planner._update_graph()
    path_planner.plot_graph()

    #go to 0.5,0.5
    path_planner.reached_checkpoint()
    path_planner.plot_graph()
    #go to 1,1
    path_planner.reached_checkpoint()
    path_planner.plot_graph()
    #go to 0.1,0.1
    path_planner.reached_checkpoint()
    path_planner.plot_graph()
    '''
    start_pos = np.array([0.0, 0.0])
    obstacles = np.array([(0.25, 0.35), (0.4, 0.05), (0.55, 0.25), (0.82, 0.15), (0.80, 0.35)])
    path_planner = PathPlanning(start_pos, obstacles)
    path_planner.add_goal(np.array([0.2, 0.2]))
    path_planner.plot_graph()
    path_planner._update_graph()
    path_planner.add_goal(np.array([0.5, 0.5]))
    path_planner.plot_graph()
    path_planner._update_graph()
    path_planner.plot_graph()
    shortes = path_planner.find_path()
    print(shortes)
    path_planner.reached_checkpoint()
    path_planner.plot_graph()
    shortes = path_planner.find_path()
    print(shortes)
    path_planner.reached_checkpoint()
    path_planner.plot_graph()