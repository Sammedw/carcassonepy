from location import Coordinates
from tile import Tile


class Action:

    def __init__(self, tile: Tile, rotation: int, coordinates: Coordinates, meeple_feature: str = None, meeple_feature_number: int = 0):
        assert meeple_feature == "city" or meeple_feature == "road" or meeple_feature == "monastery" or meeple_feature == "farm" or meeple_feature is None, "Not a valid feature for meeple"
        self.tile = tile
        self.rotation = rotation
        self.coordinates = coordinates
        self.meeple_feature = meeple_feature
        self.meeple_feature_number = meeple_feature_number

