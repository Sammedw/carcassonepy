from enum import Enum

class ConnectionType(Enum):
    CITY = "city"
    ROAD = "road"
    GRASS = "grass"
    RIVER = "river"

class FeatureType(Enum):
    CITY = "city"
    ROAD = "road"
    FIELD = "field"

class Side(Enum):
    TOP = "top"
    TOPRIGHT = "topright"
    RIGHT = "right"
    BOTTOMRIGHT = "bottomright"
    BOTTOM = "bottom"
    BOTTOMLEFT = "bottomleft"
    LEFT = "left"
    TOPLEFT = "topleft"
    CENTER = "center"

class TileAttribute(Enum):
    MONASTERY = "monastery"

class TileFeatureAttribute(Enum):
    SHIELD = "shield"


class TileFeature():

    def __init__(self, type: FeatureType, sides: list[Side], attributes: list[TileFeatureAttribute]):
        self.type = type
        self.sides = sides
        self.attributes = attributes


class Tile():

    def __init__(self, top_type: ConnectionType, right_type: ConnectionType, bottom_type: ConnectionType, left_type: ConnectionType, 
                features: list[TileFeature], attributes: list[TileAttribute]):        
        self.top_type = top_type
        self.right_type = right_type
        self.bottom_type = bottom_type
        self.left_type = left_type
        self.features = features
        self.attributes = attributes


    def get_sides(self) -> dict[Side, ConnectionType]:
        return {Side.TOP: self.top_type, Side.RIGHT: self.right_type, Side.BOTTOM: self.bottom_type, Side.LEFT: self.left_type}
