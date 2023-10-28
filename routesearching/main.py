import cities
import numpy

cities_list : list[cities.City] = cities.generate_cities(5)
for city in cities_list:
    print(city.x, city.y, city.z)

cities_matrix = cities.generate_costs_matrix(cities_list, True)
print(cities_matrix)

cities.dicard_20percent_connections(cities_matrix)
print(cities_matrix)