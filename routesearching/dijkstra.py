from sys import float_info
import cities
from util import measure_memory, measure_time

@measure_memory
@measure_time
def shortest_path(city_network: cities.CityNetwork, starting_city = 0, print_steps = False):
    # Init the list of tuples(shortest path, previous city) with highest floats and infinities beside starting city
    shortest_paths = [[float_info.max, None] if city != starting_city else [0., None] for city in range(city_network.get_n_cities())]
    # Init the visited cities set
    visited_cities = set()

    print("\n\nDijkstra:")
    while len(visited_cities) < city_network.get_n_cities():
        if print_steps: 
            print("\nEntering new iteration... Visited cities so far:\n", visited_cities)
            print_shortest_paths(shortest_paths)

        # Get the city with the shortest path so far that isn't in the visited cities set
        current_city_with_cost = [None, float_info.max]
        for i, (smallest_cost, _) in enumerate(shortest_paths):
            if i in visited_cities: continue
            if smallest_cost < current_city_with_cost[1]:
                current_city_with_cost[0] = i
                current_city_with_cost[1] = smallest_cost

        if print_steps: print(f"Chosen current city: {current_city_with_cost[0]}")

        # Get the unvisited neighbors of the city
        unvisited_neighbors = city_network.get_neighbors(current_city_with_cost[0]) - visited_cities

        if print_steps: print("Iterating through unvisited neighbors:")

        new_cost = float_info.max
        update_neighbor = -1
        # Iterate through neighbors
        for neighbor in unvisited_neighbors:
            # Get the total cost of the shortest path untill now and the cost of going from current city to neighbor combined
            cost_to_neighbor = city_network.get_single_cost(current_city_with_cost[0], neighbor)
            cost_combined = cost_to_neighbor + current_city_with_cost[1]

            if print_steps: print(f"Cost of going from {current_city_with_cost[0]} to {neighbor}: {cost_to_neighbor}")

            # If the cost combined is smaller than the shortest known path to that neighbor, update best known path
            if cost_combined < shortest_paths[neighbor][0]:
                shortest_paths[neighbor][0] = cost_combined
                shortest_paths[neighbor][1] = current_city_with_cost[0]
                new_cost = cost_combined
                update_neighbor = neighbor

        if update_neighbor != -1:
            shortest_paths[update_neighbor][0] = new_cost
            shortest_paths[update_neighbor][1] = current_city_with_cost[0]
        
        # Add the current city to the visited set
        visited_cities.add(current_city_with_cost[0])
    
    # Print results
    print_shortest_paths(shortest_paths)

def print_shortest_paths(shortest_paths: list[list[float, int]]):
    i = 0
    print("Shortest paths table:")
    for path in shortest_paths:
        print(f"{i}: Shortest path: {path[0]}, Previous city: {path[1]}")
        i += 1