from enum import Enum
from re import L


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
        if self.name == "TOPRIGHT":
            return [Side.TOPRIGHTTOP, Side.TOPRIGHTRIGHT]
        elif self.name ==  "BOTTOMRIGHT":
            return [Side.BOTTOMRIGHTRIGHT, Side.BOTTOMRIGHTBOTTOM]
        elif self.name ==  "BOTTOMLEFT":
            return [Side.BOTTOMLEFTBOTTOM, Side.BOTTOMLEFTLEFT]
        elif self.name == "TOPLEFT":
            return [Side.TOPLEFTLEFT, Side.TOPLEFTTOP]
        return [self]

    # returns the main side of a half side
    def facing(self):
        if self.name.endswith("TOP"):
            return Side.TOP
        elif self.name.endswith("RIGHT"):
            return Side.RIGHT
        elif self.name.endswith("BOTTOM"):
            return Side.BOTTOM
        else:
            return Side.LEFT
            
    def rotate_clockwise(self):
        if self.name == "TOP":
            return Side.RIGHT
        elif self.name ==  "TOPRIGHT":
            return Side.BOTTOMRIGHT
        elif self.name ==  "RIGHT":
            return Side.BOTTOM
        elif self.name ==  "BOTTOMRIGHT":
            return Side.BOTTOMLEFT
        elif self.name ==  "BOTTOM":
            return Side.LEFT
        elif self.name ==  "BOTTOMLEFT":
            return Side.TOPLEFT
        elif self.name ==  "LEFT":
            return Side.TOP
        elif self.name ==  "TOPLEFT":
            return Side.TOPRIGHT
        elif self.name ==  "TOPRIGHTTOP":
            return Side.BOTTOMRIGHTRIGHT
        elif self.name ==  "TOPRIGHTRIGHT":
            return Side.BOTTOMRIGHTBOTTOM
        elif self.name ==  "BOTTOMRIGHTRIGHT":
            return Side.BOTTOMLEFTBOTTOM
        elif self.name ==  "BOTTOMRIGHTBOTTOM":
            return Side.BOTTOMLEFTLEFT
        elif self.name ==  "BOTTOMLEFTBOTTOM":
            return Side.TOPLEFTLEFT
        elif self.name ==  "BOTTOMLEFTLEFT":
            return Side.TOPLEFTTOP
        elif self.name ==  "TOPLEFTLEFT":
            return Side.TOPRIGHTTOP
        elif self.name ==  "TOPLEFTTOP":
            return Side.TOPRIGHTRIGHT
        return Side.CENTER

    def get_opposite(self):
        if self.name == "TOP":
            return Side.BOTTOM
        elif self.name ==  "RIGHT":
            return Side.LEFT
        elif self.name ==  "BOTTOM":
            return Side.TOP
        elif self.name ==  "LEFT":
            return Side.RIGHT
        elif self.name ==  "TOPRIGHTTOP":
            return Side.BOTTOMRIGHTBOTTOM
        elif self.name ==  "TOPRIGHTRIGHT":
            return Side.TOPLEFTLEFT
        elif self.name ==  "BOTTOMRIGHTRIGHT":
            return Side.BOTTOMLEFTLEFT
        elif self.name ==  "BOTTOMRIGHTBOTTOM":
            return Side.TOPRIGHTTOP
        elif self.name ==  "BOTTOMLEFTBOTTOM":
            return Side.TOPLEFTTOP
        elif self.name ==  "BOTTOMLEFTLEFT":
            return Side.BOTTOMRIGHTRIGHT
        elif self.name ==  "TOPLEFTLEFT":
            return Side.TOPRIGHTRIGHT
        elif self.name ==  "TOPLEFTTOP":
            return Side.BOTTOMLEFTBOTTOM
        return Side.CENTER

class TileFeatureAttribute(Enum):
    SHIELD = "shield"

    def __str__(self):
        return self.name

    
class TileAttribute(Enum):

    def __str__(self):
        return self.name