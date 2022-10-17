from enum import Enum


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
    FARM = "farm"
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
    
    # decomposes a corner into its two half sides
    def decompose(self):
        match self.name:
            case "TOPRIGHT":
                return [Side.TOPRIGHTTOP, Side.TOPRIGHTRIGHT]
            case "BOTTOMRIGHT":
                return [Side.BOTTOMRIGHTRIGHT, Side.BOTTOMRIGHTBOTTOM]
            case "BOTTOMLEFT":
                return [Side.BOTTOMLEFTBOTTOM, Side.BOTTOMLEFTLEFT]
            case "TOPLEFT":
                return [Side.TOPLEFTLEFT, Side.TOPLEFTTOP]
        return [self]

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

    def get_opposite(self):
        match self.name:
            case "TOP":
                return Side.BOTTOM
            case "RIGHT":
                return Side.LEFT
            case "BOTTOM":
                return Side.TOP
            case "LEFT":
                return Side.RIGHT
            case "TOPRIGHTTOP":
                return Side.BOTTOMRIGHTBOTTOM
            case "TOPRIGHTRIGHT":
                return Side.TOPLEFTLEFT
            case "BOTTOMRIGHTRIGHT":
                return Side.BOTTOMLEFTLEFT
            case "BOTTOMRIGHTBOTTOM":
                return Side.TOPRIGHTTOP
            case "BOTTOMLEFTBOTTOM":
                return Side.TOPLEFTTOP
            case "BOTTOMLEFTLEFT":
                return Side.BOTTOMRIGHTRIGHT
            case "TOPLEFTLEFT":
                return Side.TOPRIGHTRIGHT
            case "TOPLEFTTOP":
                return Side.BOTTOMLEFTBOTTOM
        return Side.CENTER

class TileFeatureAttribute(Enum):
    SHIELD = "shield"

    def __str__(self):
        return self.name

    
class TileAttribute(Enum):

    def __str__(self):
        return self.name