import random
import math

class City:
    def __init__(self):
        self.x = random.randint(-100, 100)
        self.y = random.randint(-100, 100)
        self.z = random.randint(0, 50)

def generate_cities(n: int):
    cities = []
    for _ in range(n):
        cities.append(City())
    return cities

def count_cost_symmetrical(city1: City, city2: City):
    return math.sqrt((city2.x - city1.x)**2 + (city2.y - city1.y)**2 + (city2.z - city1.z)**2)

def count_cost_asymmetrical(city1: City, city2: City):
    height = city2.z - city1.z
    if height < 0:
        height*=11/10
    else:
        height*=9/10
    return math.sqrt((city2.x - city1.x)**2 + (city2.y - city1.y)**2 + (height)**2)