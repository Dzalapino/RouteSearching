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
    def __init__(self, n, is_discarded=False, is_symmetrical=True, from_file=False):
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
        self.costs_matrix = self.generate_costs_matrix()
        if is_discarded:
            self.discard_20percent_connections()

    def __str__(self) -> str:
        s = "Cities coordinates:"
        for city in self.cities:
            s += f"\n{city}"
        s += "\nCosts matrix"
        s += " symmetrical" if self.is_symmetrical else " asymmetrical"
        s += " after discarding 20% of connections:\n" if self.is_discarded else " without discarding 20% of connections:\n"
        s += str(self.costs_matrix)
        return s
    
    def get_n_cities(self) -> int: return len(self.cities)

    def is_connection(self, city1: int, city2: int) -> bool: return True if self.costs_matrix[city1, city2] != 0. else False

    def get_single_cost(self, city1: int, city2: int) -> float: return self.costs_matrix[city1, city2]

    def get_path_cost(self, path: list[int]) -> float:
        """
        Get the total cost of travel through the path.
        The cost is the sum of all single costs of travel between cities in the path
        :param path: Path to calculate the total cost
        :return: The total cost of travel through the path
        """
        total_cost = 0.

        # Loop through cities in path and increment cost of every single travel
        for i in range(np.size(path) - 1):
            total_cost += self.get_single_cost(path[i], path[i+1])

        return total_cost

    def get_unvisited_cities(self, path: list[int]) -> set[int]:
        """
        Get the set of unvisited cities from the path.
        :param path: Path to check
        :return: Set of unvisited cities from the path
        """
        # Create a set of expected cities from 0 to n
        expected_cities = set(range(self.get_n_cities()))

        # Convert the path to a set of cities
        cities = set(path)

        # Return a subset of expected cities without already visited cities from path
        return expected_cities.difference(cities)
    
    def get_neighbors(self, city: int) -> set[int]:
        """
        Get the set of neighbors of the city.
        A neighbor is a city that is connected to the city.
        :param city: City to get the neighbors
        :return: Set of neighbors of the city
        """
        return set(n for n in range(self.get_n_cities()) if n != city and self.is_connection(city, n))
    
    def get_unvisited_neighbors(self, path: list[int]):
        """
        Get the set of unvisited neighbors of the last city in path.
        :param path: Path to check
        :return: Set of unvisited neighbors of the last city in path
        """
        # Get the neighbors of last city in path
        neighbors = self.get_neighbors(path[-1])

        # Return the intersection of unvisited cities in path and the neighbors of last city
        return set.intersection(neighbors, self.get_unvisited_cities(path))

    def is_path_including_all_cities(self, path: str) -> bool:
        """
        Check if the path includes all cities
        :param path: Path to check
        :return: True if the path includes all cities, False otherwise
        """
        # Create a set of expected cities from 0 to n
        expected_cities = set(range(self.get_n_cities()))

        # Convert the path to a set of cities
        cities = set(path)

        # Check if the expected_cities set is a subset of cities set
        return expected_cities.issubset(cities)

    def print_graph(self) -> None:
        """
        Print the graph of cities and connections between them.
        Used for visualization purposes with matplotlib and networkx
        :return: None
        """
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

    def generate_single_cost(self, city1: City, city2: City):
        """
        Generate the cost of travel between two cities using Euclidean distance
        :param city1: City 1
        :param city2: City 2
        :return: The cost of travel between two cities
        """
        height = city2.z - city1.z
        if not self.is_symmetrical:
            if height > 0:
                height *= 11/10
            else:
                height *= 9/10
        # Calculate the euclidean distance
        return np.sqrt((city2.x - city1.x)**2 + (city2.y - city1.y)**2 + height**2)

    def generate_costs_matrix(self) -> np.ndarray:
        """
        Generate the costs matrix of travel between cities
        :return: The costs matrix of travel between cities
        """
        n = np.size(self.cities)
        costs_matrix = np.zeros((n, n))

        # Populate the zeros matrix with the travel costs
        for i in range(n):
            for j in range(n):
                # Omit diagonal
                if i == j:
                    continue
                costs_matrix[i, j] = round(self.generate_single_cost(self.cities[i], self.cities[j]), 2)
        return costs_matrix

    def discard_20percent_connections(self) -> None:
        """
        Discard 20% of connections in the costs matrix
        :return: None
        """
        # Generate the list with unique connections
        n = self.costs_matrix.shape[0]
        unique_connections = [(i, j) for i in range(n) for j in range(i + 1, n)]

        # Shuffle the list and select the first 20% of unique connections to discard
        random.shuffle(unique_connections)
        total_to_discard = int(np.floor(0.2 * np.size(unique_connections, 0)))
        connections_to_discard = unique_connections[:total_to_discard]

        # Discard selected connections
        for connection in connections_to_discard:
            i, j = connection
            self.costs_matrix[i, j] = 0.
            self.costs_matrix[j, i] = 0.
