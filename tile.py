from enum import Enum
from meeple import Meeple
from typing import Optional

class ConnectionType(Enum):
    CITY = "city"
    ROAD = "road"
    GRASS = "grass"
    RIVER = "river"

    def __str__(self):
        return self.name


class FeatureType(Enum):
    CITY = "city"
    ROAD = "road"
    FIELD = "field"
    MONASTERY = "monastery"

    def __str__(self):
        return self.name


class Side(Enum):
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"
    LEFT = "left"
    CENTER = "center"

    # farms
    TOPRIGHT = "topright"
    BOTTOMRIGHT = "bottomright"
    BOTTOMLEFT = "bottomleft"
    TOPLEFT = "topleft"

    TOPRIGHTTOP = "toprighttop"
    TOPRIGHTRIGHT = "toprightright"
    BOTTOMRIGHTRIGHT = "bottomrightright"
    BOTTOMRIGHTBOTTOM = "bottomrightbottom"
    BOTTOMLEFTBOTTOM = "bottomleftbottom"
    BOTTOMLEFTLEFT = "bottomleftleft"
    TOPLEFTLEFT = "topleftleft"
    TOPLEFTTOP = "toplefttop"

    def __str__(self):
        return self.name

    def rotate_clockwise(self):
        match self.name:
            case "TOP":
                return Side.RIGHT
            case "TOPRIGHT":
                return Side.BOTTOMRIGHT
            case "RIGHT":
                return Side.BOTTOM
            case "BOTTOMRIGHT":
                return Side.BOTTOMLEFT
            case "BOTTOM":
                return Side.LEFT
            case "BOTTOMLEFT":
                return Side.TOPLEFT
            case "LEFT":
                return Side.TOP
            case "TOPLEFT":
                return Side.TOPRIGHT
            case "TOPRIGHTTOP":
                return Side.BOTTOMRIGHTRIGHT
            case "TOPRIGHTRIGHT":
                return Side.BOTTOMRIGHTBOTTOM
            case "BOTTOMRIGHTRIGHT":
                return Side.BOTTOMLEFTBOTTOM
            case "BOTTOMRIGHTBOTTOM":
                return Side.BOTTOMLEFTLEFT
            case "BOTTOMLEFTBOTTOM":
                return Side.TOPLEFTLEFT
            case "BOTTOMLEFTLEFT":
                return Side.TOPLEFTTOP
            case "TOPLEFTLEFT":
                return Side.TOPRIGHTTOP
            case "TOPLEFTTOP":
                return Side.TOPRIGHTRIGHT

        return Side.CENTER


class Coordinates():

    def __init__(self, x: int, y: int):
        self.x = x;
        self.y = y;

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Location():

    def __init__(self, x: int, y: int, side: Side):
        self.coordinates = Coordinates(x, y)
        self.side = side
    
    def __eq__(self, other):
        return self.coordinates == other.coordinates and self.side == other.side


class TileAttribute(Enum):

    def __str__(self):
        return self.name


class TileFeatureAttribute(Enum):
    SHIELD = "shield"

    def __str__(self):
        return self.name


class TileFeature():

    def __init__(self, type: FeatureType, sides: list[Side], attributes: list[TileFeatureAttribute] = []):
        self.type = type
        self.sides = sides
        self.attributes = attributes
        self.meeple: Optional[Meeple]

    def __str__(self):
        return f"TileFeature<{str(self.type)} | {[str(side) for side in self.sides]}>"


class Tile():

    def __init__(self, top_type: ConnectionType, right_type: ConnectionType, bottom_type: ConnectionType, left_type: ConnectionType, 
                features: list[TileFeature] = [], attributes: list[TileAttribute] = []):        
        self.sides: dict[Side, ConnectionType] = {Side.TOP: top_type, Side.RIGHT: right_type, Side.BOTTOM: bottom_type, Side.LEFT: left_type}
        self.features = features
        self.attributes = attributes

    def __str__(self):
        return f"Tile<{[str(side) for side in self.sides.values()]} | {[str(feature) for feature in self.features]}>"

    def rotate_clockwise(self, times: int):
        if times <= 0:
            return 
        # rotate sides
        self.sides = {Side.TOP: self.sides[Side.LEFT], Side.RIGHT: self.sides[Side.TOP], Side.BOTTOM: self.sides[Side.RIGHT], Side.LEFT: self.sides[Side.BOTTOM]}
        # rotate features
        for feature in self.features:
            feature.sides = [side.rotate_clockwise() for side in feature.sides]
        # rotate n-1 more times    
        self.rotate_clockwise(times-1);