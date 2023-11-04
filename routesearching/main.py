import cities
import full_search

city_network = cities.CityNetwork(7, True, False)

print(city_network)
# city_network.print_graph()

full_search.shortest_path(city_network.costs_matrix, 0, full_search.BFS)
full_search.shortest_path(city_network.costs_matrix, 0, full_search.DFS)