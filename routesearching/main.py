import cities
import full_search
import nearest_neighbor
import dijkstra
import aco
import numpy as np

np.random.seed(0)

city_network = cities.CityNetwork(7, True, False)

print(city_network)
city_network.print_graph()

full_search.shortest_path(city_network, full_search.BFS)
full_search.shortest_path(city_network, full_search.DFS)

try:
    _, nn_cost = nearest_neighbor.shortest_path(city_network)
    aco.shortest_path(city_network, nn_cost, 0, 10, 0.1, 0.25, False)
except Exception as e:
    print(f"\n{e}")

dijkstra.shortest_path(city_network, 0, dijkstra.HeuristicType.DIJKSTRA)
