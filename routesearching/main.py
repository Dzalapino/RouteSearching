import cities
import bfs

city_network = cities.CityNetwork(10, True, False)

print(city_network)
city_network.print_graph()

print("\n\nBFS:")
shortest_path, total_cost, execution_time = bfs.shortest_path(city_network.costs_matrix, 0)
print("Execution time:", execution_time)
print(f"The shortest path is: {shortest_path}\nThe total cost is: {total_cost}")