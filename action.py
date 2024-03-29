from typing import Optional
from enums import FeatureType
from location import Coordinates
from tile import Tile


class Action:

    def __init__(self, tile_name: str, rotation: int, coordinates: Coordinates, meeple_feature_type: Optional[FeatureType] = None, meeple_feature_number: int = 0):
        self.tile_name = tile_name
        self.rotation = rotation % 4
        self.coordinates = coordinates
        self.meeple_feature_type = meeple_feature_type
        self.meeple_feature_number = meeple_feature_number

    def __str__(self):
        return f"<{self.tile_name}, {self.rotation}, {self.coordinates}, {self.meeple_feature_type}, {self.meeple_feature_number}>"

    def __eq__(self, other):
        return self.tile_name == other.tile_name and self.rotation == other.rotation and self.coordinates == other.coordinates and self.meeple_feature_type == other.meeple_feature_type and self.meeple_feature_number == other.meeple_feature_number