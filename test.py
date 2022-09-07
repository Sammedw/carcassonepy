from tile import *

tile = Tile(ConnectionType.GRASS, ConnectionType.GRASS, ConnectionType.ROAD, ConnectionType.GRASS, [TileFeature(FeatureType.ROAD, [Side.BOTTOM, Side.TOP])])

print(tile)

tile.rotate_clockwise(1)

print(tile)
