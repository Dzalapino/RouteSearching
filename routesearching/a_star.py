from queue import PriorityQueue
from routesearching import cities
from util import measure_memory, measure_time, print_shortest_path


def admissible_heuristic(city1, city2, city_network):
    return city_network.get_single_cost(city1, city2)


def inadmissible_heuristic(city1, city2):
    return 100


@measure_memory
@measure_time
def tsp_a_star(city_network: cities.CityNetwork, starting_city=0, heuristic_type='ADMISSIBLE'):
    n = city_network.get_n_cities()
    Q = PriorityQueue()
    Q.put((0, (starting_city, frozenset([starting_city]))))  # (priority, (current_city, visited_cities))

    g_score = {(starting_city, frozenset([starting_city])): 0}
    came_from = {(starting_city, frozenset([starting_city])): None}

    while not Q.empty():
        _, state = Q.get()
        current_city, visited_cities = state

        if len(visited_cities) == n:
            path = [current_city]
            while state is not None:
                path.append(came_from[state][0])  # Extract the city from the tuple
                state = came_from[state]
            path.reverse()
            # Append the starting city to the end of the path
            path.append(starting_city)
            print_shortest_path(path, g_score[(current_city, visited_cities)])  # Print path and cost
            return

        for neighbor in range(n):
            if neighbor not in visited_cities:
                new_visited_cities = visited_cities | {neighbor}
                if heuristic_type == 'ADMISSIBLE':
                    heuristic = admissible_heuristic(current_city, neighbor, city_network)
                else:
                    heuristic = inadmissible_heuristic(current_city, neighbor)
                tentative_g_score = g_score[(current_city, visited_cities)] + city_network.get_single_cost(current_city, neighbor) + heuristic

                if (neighbor, new_visited_cities) not in g_score or tentative_g_score < g_score[(neighbor, new_visited_cities)]:
                    g_score[(neighbor, new_visited_cities)] = tentative_g_score
                    came_from[(neighbor, new_visited_cities)] = (current_city, visited_cities)
                    Q.put((tentative_g_score, (neighbor, new_visited_cities)))

    print("No path found.")
