import cities
import numpy

cities_list : list[cities.City] = cities.generate_cities(5)
for city in cities_list:
    print(city.x, city.y, city.z)

costs_matrix = cities.generate_costs_matrix(cities_list, False)
print(costs_matrix)

cities.dicard_20percent_connections(costs_matrix)
print(costs_matrix)

cities.print_graph(costs_matrix, cities_list)