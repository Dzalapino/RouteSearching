import random
import numpy as np

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
    cities_matrix = np.zeros((n, n))

    # Populate the zeros matrix with the travel costs
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            cities_matrix[i, j] = count_cost(cities_list[i], cities_list[j], symmetrical_problem)
    return cities_matrix

def dicard_20percent_connections(cities_matrix):
    # Generate the lit with unique connections
    n = np.size(cities_matrix, 0)
    unique_connections = [(i, j) for i in range(n) for j in range(i + 1, n)]
    
    # Shuffle the list and select the first 20% of unique connections to discard
    random.shuffle(unique_connections)
    total_to_discard = int(np.floor(0.2 * np.size(unique_connections)))
    connections_to_discard = unique_connections[:total_to_discard]

    # Discard selected connections
    for connection in connections_to_discard:
        i, j = connection
        cities_matrix[i, j] = 0.
        cities_matrix[j, i] = 0.