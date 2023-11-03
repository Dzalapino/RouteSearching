import numpy as np
import cities
from sys import float_info
import time
from memory_profiler import profile

@profile
def shortest_path(costs_matrix: np.ndarray[float], starting_city: int):
    start_time = time.time()
    # Create a queue (list) with the chosen starting city
    partial_paths = [[starting_city]]
    n_cities = np.size(costs_matrix, 0)
    # Init values to return
    total_path = []
    total_cost = float_info.max

    while(len(partial_paths) > 0):
        # Pop the left partial path and use it in that iteration
        path = partial_paths.pop(0)

        # If current path includes all cities and the last city in it is connected to the starting city do the proper calculations
        if cities.includes_all_cities(path, n_cities):
            if cities.is_connection(path[-1], starting_city, costs_matrix):
                # Calculate the total cost of path that will return to the starting city
                path.append(starting_city)
                cost = cities.get_total_cost(path, costs_matrix)
                # If the current path total cost is shorter than the best known path's total cost, update best known path
                if cost < total_cost:
                    total_path = path
                    total_cost = cost
        
        # Add new paths with remaining unvisited cities in the current path to the queue
        for city in cities.get_unvisited(path, n_cities):
            # Omit the non existing connections
            if cities.is_connection(path[-1], city, costs_matrix):
                new_path = list(path)
                new_path.append(city)
                partial_paths.append(new_path)
    end_time = time.time()
    return total_path, total_cost, end_time-start_time