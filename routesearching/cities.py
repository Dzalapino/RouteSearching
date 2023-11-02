import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class City:
    def __init__(self):
        self.x = random.randint(-100, 100)
        self.y = random.randint(-100, 100)
        self.z = random.randint(0, 50)

def generate_cities(n: int):
    cities = []
    for _ in range(n):
        cities.append(City())
    return cities

def count_cost(city1: City, city2: City, symmetrical_problem = True):
    height = city2.z - city1.z
    if symmetrical_problem == False:
        if height < 0:
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
            if i == j:
                continue
            costs_matrix[i, j] = round(count_cost(cities_list[i], cities_list[j], symmetrical_problem), 2)
    return costs_matrix

def dicard_20percent_connections(costs_matrix: np.ndarray[float]):
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

def print_graph(costs_matrix: np.ndarray[float], cities_list: list[City], symmetrical_problem = True):
    # Create an empty directed graph
    G = nx.Graph() if symmetrical_problem else nx.MultiDiGraph()

    for i in range(costs_matrix.shape[0]):
        # Add nodes with cities positions
        G.add_node(i+1, pos=(cities_list[i].x, cities_list[i].y))
        for j in range(costs_matrix.shape[1]):
            if j > i and costs_matrix[i, j] > 0.:
                # Add edges with costs as weights
                G.add_edge(i+1, j+1, weight=costs_matrix[i, j])
                if symmetrical_problem == False:
                    G.add_edge(j+1, i+1, weight=costs_matrix[j, i])

    # Now you can use the 'pos' attribute to position nodes during visualization
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

    # Add ticks and labels to the axes
    plt.xticks(np.arange(-100, 100, 10))
    plt.yticks(np.arange(-100, 100, 10))
    plt.grid(True)

    # Set axis limits
    plt.xlim(-100, 100)
    plt.ylim(-100, 100)

    plt.show()