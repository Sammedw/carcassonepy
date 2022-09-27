from typing import Optional
from enums import FeatureType
from location import Coordinates
from tile import Tile


class Action:

    def __init__(self, tile: Tile, rotation: int, coordinates: Coordinates, meeple_feature: Optional[FeatureType] = None, meeple_feature_number: int = 0):
        self.tile = tile
        self.rotation = rotation
        self.coordinates = coordinates
        self.meeple_feature = meeple_feature
        self.meeple_feature_number = meeple_feature_number

