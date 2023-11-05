from collections import deque
from sys import float_info
import cities
from util import measure_memory, measure_time

@measure_memory
@measure_time
def shortest_path(city_network: cities.CityNetwork, print_steps = False):
    # Init path list and starting city
    starting_city = 0
    path = deque([starting_city])

    while len(path) < city_network.get_n_cities():
        if print_steps: print("\nEntering new iteration... Current path:\n", path)

        nearest_city = None
        smallest_cost = float_info.max

        if print_steps: print("Printing neighbors:")
        # Get the unvisited cities in path
        for city in city_network.get_unvisited_cities(path):
            # Omit the non existing connections
            if city_network.is_connection(path[-1], city):
                if print_steps: print(city)

                # Check for the nearest neighbor
                cost = city_network.get_single_cost(path[-1], city)
                if cost < smallest_cost:
                    nearest_city = city
                    smallest_cost = cost
        
        if nearest_city is not None:
            if print_steps: print("Nearest neighbor is: ", nearest_city)

            # Add the new nearest neighbor to the path
            path.append(nearest_city)

            # Check if that's final iteration
            if len(path) == city_network.get_n_cities():
                # Check if final city is connected with startng city
                if city_network.is_connection(path[-1], starting_city) == False:
                    # Cannot reach starting city from final city, choose another starting city
                    starting_city = choose_another_starting_city(starting_city, path)
        else:
            # No reachable cities were found, choose another starting city
            starting_city = choose_another_starting_city(starting_city, path)

            if print_steps: print("No reachable cities were found... Starting again with starting city: ", starting_city)
    
    path.append(starting_city)
    print(f"\n\nNearest Neighbor:\nThe shortest path is: {path}\nThe total cost is: {city_network.get_path_cost(path)}")

def choose_another_starting_city(starting_city: int, path: deque[int]) -> int:
    path.clear()
    starting_city += 1
    path.append(starting_city)
    return starting_city