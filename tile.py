from enum import Enum
from typing import Optional, Type
from enums import *
from location import *
from feature import TileFeature


class Tile():

    def __init__(self, top_type: ConnectionType, right_type: ConnectionType, bottom_type: ConnectionType, left_type: ConnectionType, 
                cities: list[Type[TileFeature]] = [], roads: list[Type[TileFeature]] = [], monastery: Optional[Type[TileFeature]] = None, farms: list[Type[TileFeature]] = [],
                attributes: list[TileAttribute] = []):        
        self.sides: dict[Side, ConnectionType] = {Side.TOP: top_type, Side.RIGHT: right_type, Side.BOTTOM: bottom_type, Side.LEFT: left_type}
        self.cities = cities
        self.roads = roads
        self.monastery = monastery
        self.farms = farms
        self.attributes = attributes

    def __str__(self):
        return f"Tile<{[str(side) for side in self.sides.values()]} | {[str(feature) for feature in self.get_features()]}>"

    def rotate_clockwise(self, times: int):
        if times <= 0:
            return 
        # rotate sides
        self.sides = {Side.TOP: self.sides[Side.LEFT], Side.RIGHT: self.sides[Side.TOP], Side.BOTTOM: self.sides[Side.RIGHT], Side.LEFT: self.sides[Side.BOTTOM]}
        # rotate features
        for feature in self.cities + self.roads + self.farms:
            feature.sides = [side.rotate_clockwise() for side in feature.sides]
        # rotate n-1 more times    
        self.rotate_clockwise(times-1);

    def get_features(self) -> list[Type[TileFeature]]:
        features = (self.cities + self.roads + self.farms)
        if self.monastery:
            features.append(self.monastery)
        return features