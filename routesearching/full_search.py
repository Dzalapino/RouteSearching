from collections import deque
from sys import float_info
import cities
from util import measure_time, measure_memory

BFS = 'BFS'
DFS = 'DFS'

@measure_memory
@measure_time
def shortest_path(city_network: cities.CityNetwork, method = BFS, starting_city = 0, print_steps = False):
    # Create a queue/stack (deque used differently based on the method chosen)
    partial_paths: deque[deque] = deque()
    # Append starting city
    partial_paths.append(deque([starting_city]))
    # n_cities = city_network.get_n_cities()

    # Init values to return
    total_path = []
    total_cost = float_info.max

    while(len(partial_paths) > 0):
        if print_steps: print("\nEntering new iteration... The partial paths collection:\n", partial_paths)

        if method == BFS:
            # Pop the left partial path and use it in that iteration
            path = partial_paths.popleft()
        else:
            # Pop the right partial path and use it in that iteration
            path = partial_paths.pop()

        if print_steps: print("Popped the following path:\n", path)

        # Check if current path includes all cities
        if len(path) == city_network.get_n_cities():
            # Check if the last city in it is connected to the starting city
            if city_network.is_connection(path[-1], starting_city):
                # Calculate the total cost of path that will return to the starting city
                path.append(starting_city)
                cost = city_network.get_path_cost(path)

                # If the current path's total cost is lower  than the best known path's total cost, update best known path
                if cost < total_cost:
                    total_path = path
                    total_cost = cost
        
        # Add new paths with remaining unvisited cities in the current path to the queue
        for city in city_network.get_unvisited_cities(path):
            # Omit the non existing connections
            if city_network.is_connection(path[-1], city):
                new_path = deque(path)
                new_path.append(city)
                partial_paths.append(new_path)

    print(f"\n\n{method}:")
    print(f"The shortest path is: {total_path}\nThe total cost is: {total_cost}")