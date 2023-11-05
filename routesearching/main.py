import cities
import full_search
import nearest_neighbor

city_network = cities.CityNetwork(5, True, False)

print(city_network)
# city_network.print_graph()

full_search.shortest_path(city_network, full_search.BFS)
full_search.shortest_path(city_network, full_search.DFS)

try:
    nearest_neighbor.shortest_path(city_network)
except Exception as e:
    print(f"\n{e}")