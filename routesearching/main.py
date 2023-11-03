import cities
import bfs

city_network = cities.CityNetwork(5, True, False)

print(city_network)
city_network.print_graph()

shortest_path, total_cost = bfs.shortest_path(city_network.costs_matrix, 0)
print(f"The shortest path is: {shortest_path}\nThe total cost is: {total_cost}")