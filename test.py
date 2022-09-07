from tile import *
from feature import *
from meeple import *

tile = Tile(ConnectionType.GRASS, ConnectionType.GRASS, ConnectionType.ROAD, ConnectionType.GRASS, [TileFeature(FeatureType.ROAD, [Side.BOTTOM, Side.TOP])])

print(tile)

tile.rotate_clockwise(1)

print(tile)

city1 = City()
city1.frontier_locations = [1,3,4]
city1.meeples = [1,2]
city1.tile_count = 2

city2 = City()
city2.frontier_locations = [2]
city2.meeples = [3,4]
city2.tile_count = 3

city3 = City()
city3.frontier_locations = [6,7]
city3.meeples = [8,6]
city3.tile_count = 1


farm1 = Farm()
farm1.frontier_locations = [1,2]
farm1.meeples = [1]
farm1.tile_count = 1
farm1.adjacent_cities = {city2}

farm2 = Farm()
farm2.frontier_locations = [3,4]
farm2.meeples = [2]
farm2.tile_count = 3
farm2.adjacent_cities = {city1, city2}

tilecity = TileFeature(FeatureType.CITY, [], [])
tilefarm = TileFarm([], [], {tilecity})

farm1.merge_features(tilefarm, Coordinates(2,4), [Side.TOP], [farm2])

print(farm1.frontier_locations)
print(farm1.meeples)
print(farm1.tile_count)
for city in farm1.adjacent_cities:
    print(city)




