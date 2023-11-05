import cities
import full_search
import nearest_neighbor

city_network = cities.CityNetwork(10, True, False)

print(city_network)
city_network.print_graph()

full_search.shortest_path(city_network, full_search.BFS)
full_search.shortest_path(city_network, full_search.DFS)
nearest_neighbor.shortest_path(city_network, False)