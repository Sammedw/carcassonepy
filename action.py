from re import M
from typing import Optional
from enums import FeatureType
from location import Coordinates
from tile import Tile


class Action:

    def __init__(self, tile: Tile, rotation: int, coordinates: Coordinates, meeple_feature_type: Optional[FeatureType] = None, meeple_feature_number: int = 0):
        self.tile = tile
        self.rotation = rotation % 4
        self.coordinates = coordinates
        self.meeple_feature_type = meeple_feature_type
        self.meeple_feature_number = meeple_feature_number

    def __str__(self):
        return f"<{self.tile}, {self.rotation}, {self.coordinates}, {self.meeple_feature_type}, {self.meeple_feature_number}>"