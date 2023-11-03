import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class City:
    def __init__(self):
        self.x = random.randint(-100, 100)
        self.y = random.randint(-100, 100)
        self.z = random.randint(0, 50)
    def __str__(self) -> str:
        return f"( {self.x}, {self.y}, {self.z} )"

class CityNetwork:
    def __init__(self, n, is_discarded = False, is_symmetrical = True, from_file = False):
        self.cities = []
        self.is_discarded = is_discarded
        self.is_symmetrical = is_symmetrical
        if from_file:
            # Import cities list from file
            print()
        else:
            # Generate n random cities
            for _ in range(n):
                self.cities.append(City())
        self.costs_matrix = generate_costs_matrix(self.cities, is_symmetrical)
        if is_discarded:
            discard_20percent_connections(self.costs_matrix)
    def __str__(self) -> str:
        s = "Cities coordinates:"
        for city in self.cities:
            s += f"\n{city}"
        s += "\nCosts matrix"
        s += " symmetrical" if self.is_symmetrical else " asymmetrical"
        s += " after discarding 20% of connections:\n" if self.is_discarded else " without discarding 20% of connections:\n"
        s += str(self.costs_matrix)
        return s
    def print_graph(self) -> None:
        # Create an empty directed graph
        G = nx.Graph()

        for i in range(self.costs_matrix.shape[0]):
            # Add nodes with cities positions
            G.add_node(i, pos=(self.cities[i].x, self.cities[i].y))
            for j in range(self.costs_matrix.shape[1]):
                if j > i and self.costs_matrix[i, j] > 0.:
                    if self.is_symmetrical:
                        # Add edges with costs as weights
                        G.add_edge(i, j, weight = self.costs_matrix[i, j])
                    else:
                        G.add_edge(j, i, weight = f"{self.costs_matrix[j, i]}\n{self.costs_matrix[i, j]}")

        # Use the 'pos' attribute to position nodes during visualization
        node_positions = nx.get_node_attributes(G, 'pos')

        # Draw nodes and edges using specified positions
        nx.draw_networkx_nodes(G, node_positions, node_size=300, node_color='skyblue')
        nx.draw_networkx_edges(G, node_positions, edgelist=G.edges(), edge_color='gray')
        nx.draw_networkx_labels(G, node_positions, font_size=10, font_color='black')
        nx.draw_networkx_edge_labels(G, node_positions, edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)}, font_size=7)
        
        # X and y axes and it's labels
        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(0, color='black', linewidth=1)
        plt.text(100, -5, 'X', fontsize=12)
        plt.text(-5, 100, 'Y', fontsize=12)

        # Add ticks and grid
        plt.xticks(np.arange(-100, 100, 10))
        plt.yticks(np.arange(-100, 100, 10))
        plt.grid(True)

        # Set axis limits
        plt.xlim(-100, 100)
        plt.ylim(-100, 100)

        plt.show()

def count_cost(city1: City, city2: City, symmetrical_problem = True):
    height = city2.z - city1.z
    if symmetrical_problem == False:
        if height > 0:
            height*=11/10
        else:
            height*=9/10
    # Calculate the euclidean distance
    return np.sqrt((city2.x - city1.x)**2 + (city2.y - city1.y)**2 + (height)**2)

def generate_costs_matrix(cities_list: list[City], symmetrical_problem = True):
    n = np.size(cities_list)
    costs_matrix = np.zeros((n, n))

    # Populate the zeros matrix with the travel costs
    for i in range(n):
        for j in range(n):
            # Omit diagonal
            if i == j:
                continue
            costs_matrix[i, j] = round(count_cost(cities_list[i], cities_list[j], symmetrical_problem), 2)
    return costs_matrix

def discard_20percent_connections(costs_matrix: np.ndarray[float]):
    # Generate the list with unique connections
    n = costs_matrix.shape[0]
    unique_connections = [(i, j) for i in range(n) for j in range(i + 1, n)]
    
    # Shuffle the list and select the first 20% of unique connections to discard
    random.shuffle(unique_connections)
    total_to_discard = int(np.floor(0.2 * np.size(unique_connections, 0)))
    connections_to_discard = unique_connections[:total_to_discard]

    # Discard selected connections
    for connection in connections_to_discard:
        i, j = connection
        costs_matrix[i, j] = 0.
        costs_matrix[j, i] = 0.

def is_connection(city1: int, city2: int, costs_matrix: np.ndarray[float]) -> bool:
    return True if costs_matrix[city1][city2] != 0. else False

def includes_all_cities(path: str, n_cities: int) -> bool:
    # Create a set of expected cities from 1 to n
    expected_cities = set(range(n_cities))

    # Convert the path to a set of cities
    cities = set(path)

    # Check if the expected_cities set is a subset of cities set
    return expected_cities.issubset(cities)

def get_unvisited(path: list[int], n_cities: int) -> set[int]:
    # Create a set of expected cities from 1 to n
    expected_cities = set(range(n_cities))

    # Convert the path to a set of cities
    cities = set(path)

    # Return a subset of expected cities without already visited cities from path
    return expected_cities.difference(cities)

def get_total_cost(path: list[int], costs_matrix: np.ndarray[float]) -> float:
    total_cost = 0.

    # Loop through cities in path and increment cost of every single travel
    for i in range(np.size(path) - 1):
        total_cost += costs_matrix[path[i]][path[i+1]]

    return total_cost