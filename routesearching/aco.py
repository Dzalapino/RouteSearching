from sys import float_info
from collections import deque
import numpy as np
import random
import cities
from util import measure_memory, measure_time, print_shortest_path

@measure_memory
@measure_time
def shortest_path(city_network: cities.CityNetwork, max_path_cost: float, starting_city = 0, n_ants = 10, init_pheromone = 0.1, evaporation_rate = 0.25, print_steps = False):
    # Generate pheromones matrix
    n_cities = city_network.get_n_cities()
    pheromone_matrix = np.full((n_cities, n_cities), init_pheromone)
    np.fill_diagonal(pheromone_matrix, 0)
    best_path = deque()
    smallest_cost = float_info.max

    print("\n\nAnt Colony Approximation:")
    while smallest_cost >= max_path_cost: # Termination criterion
        if print_steps:
            print("Pheromone matrix:\n", pheromone_matrix)
            print(f"Current best path found by colony and it's cost: {best_path}, {smallest_cost}")

        # Chosing paths for predefined number of ants based on the pheromone matrix
        ants_paths = deque(deque()) # Init empty list of ants paths
        
        if print_steps: print(f"Searching paths for {n_ants} ants...")

        # Find paths for every ant based on probability
        while len(ants_paths) < n_ants:
            ant_path = deque([starting_city]) # Init the path of an ant with the starting city in it

            if print_steps: print(f"\nFound paths so far: {ants_paths}")

            # Find the new path for an ant
            for _ in range(n_cities-1):
                probabilities = deque()
                sum_partial_probs = .0
                neighbors = city_network.get_unvisited_neighbors(ant_path)
                
                # If there is no connection to other unvisited cities abandon this path
                if len(neighbors) == 0 and len(ant_path) < n_cities:
                    if print_steps: print(f"\nNeighbors length: {len(neighbors)}, ant path length: {len(ant_path)}, no suitable neighbor connection found for path {ant_path}")
                    break

                if print_steps: print(f"Neighbors found for path {ant_path}:")

                # Iterate through neighbors of the last city in path and count partial probabilities
                for neighbor in neighbors:
                    partial_prob = pheromone_matrix[ant_path[-1], neighbor] / city_network.costs_matrix[ant_path[-1], neighbor]
                    probabilities.append([neighbor, partial_prob])
                    sum_partial_probs += partial_prob
                
                # Divide partial probabilities by sum of all partial probabilities
                for prob in probabilities:
                    prob[1] /= sum_partial_probs
                    if print_steps: print(f"Probability to go to {prob[0]} is {prob[1]}")

                ant_path.append(chose_next_city_probabilistic(probabilities)) # Add the random path based on probabilities
                if print_steps: print(f"Random neighbor chosen: {ant_path[-1]}")
            
            if print_steps: print(f"\nChecking if {ant_path} is valid path for ant number {len(ants_paths)}")

            if len(ant_path) == n_cities: # If path consists of all cities
                if print_steps: print(f"Path {ant_path} consist of all cities to visit")

                # If there is connection between starting city and the last city in the path add the path with added starting city
                if city_network.is_connection(ant_path[-1], starting_city):
                    if print_steps: print(f"There is a connection between {ant_path[-1]} and {starting_city}, adding the path for another ant")
                    ant_path.append(starting_city)
                    ants_paths.append(ant_path)

        if print_steps: print("\nAnts exploring chosen paths...")

        # Every ant explores it's chosen path
        for ant_path in ants_paths:
            total_cost = .0

            if print_steps: print(f"\nExploring path {ant_path}")

            # Every value in the pheromone matrix is being updated
            for i in range(len(ant_path) - 1):
                single_cost = city_network.get_single_cost(ant_path[i], ant_path[i + 1])

                if print_steps: print(f"Cost of going from {ant_path[i]} to {ant_path[i + 1]}: {single_cost}")

                total_cost += single_cost                           # Total cost of the path is being incremented
                if print_steps: print(f"Pheromone {ant_path[i], ant_path[i + 1]} before update: ", pheromone_matrix[ant_path[i], ant_path[i + 1]])
                pheromone_matrix[ant_path[i], ant_path[i + 1]] *= 1 - evaporation_rate  # Pheromones evaporate
                if print_steps: print(f"Pheromone {ant_path[i], ant_path[i + 1]} after evaporation: ", pheromone_matrix[ant_path[i], ant_path[i + 1]])
                pheromone_matrix[ant_path[i], ant_path[i + 1]] += 1 / single_cost       # Ants add more pheromones
                if print_steps: print(f"Pheromone {ant_path[i], ant_path[i + 1]} after update: ", pheromone_matrix[ant_path[i], ant_path[i + 1]])
            
            if print_steps: print(f"Total cost of the path: {total_cost}")

            if total_cost < smallest_cost: # Found new best path
                smallest_cost = total_cost
                best_path = ant_path
                if print_steps: print(f"Found new best path: {best_path} with it's cost being: {smallest_cost}")
        
    print_shortest_path(best_path, smallest_cost)


def chose_next_city_probabilistic(probabilities: deque[tuple[int, float]]):
    # Sort probabilistic values descending
    sorted_probabilities_desc = deque(sorted(probabilities, key=lambda x: x[1], reverse=True))

    # Turn probabilistic values to cumulative ones
    cumulative_desc = deque()
    for _ in range(len(sorted_probabilities_desc)):
        cumulative_desc.append((sorted_probabilities_desc[0][0], sum(item[1] for item in sorted_probabilities_desc)))
        sorted_probabilities_desc.popleft()

    # Generate random number <0, 1> and return the city that random belongs to
    random_n = random.random()
    for i in range(len(cumulative_desc) - 1):
        if cumulative_desc[i][1] >= random_n > cumulative_desc[i + 1][1]:
            return cumulative_desc[i][0]
        
    return cumulative_desc[-1][0]
