from tile import *
from feature import *
from meeple import *

tile = Tile(ConnectionType.GRASS, ConnectionType.GRASS, ConnectionType.ROAD, ConnectionType.GRASS, [TileFeature(FeatureType.ROAD, [Side.BOTTOM, Side.TOP])])

print(tile)

tile.rotate_clockwise(1)

print(tile)

city1 = Feature()
city1.frontier_locations = [1,3,4]
city1.meeples = [1,2]
city1.tile_count = 2

city2 = Feature()
city2.frontier_locations = [2]
city2.meeples = [3,4]
city2.tile_count = 3

city1.merge_features("tile feature", [city2])

print(city1.frontier_locations)
print(city1.meeples)
print(city1.tile_count)
print(city2.meeples)
