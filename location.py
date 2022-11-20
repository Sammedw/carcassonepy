from enums import Side

class Coordinates():

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.x < other.x:
            return True
        elif self.x == other.x and self.y < other.y:
            return True
        return False

    def __hash__(self):
        return hash(f"({self.x}, {self.y})")

    def get_adjacent(self, corners: bool=False):
        adjacent = {Side.TOP: Coordinates(self.x, self.y + 1), Side.RIGHT: Coordinates(self.x + 1, self.y), Side.BOTTOM: Coordinates(self.x, self.y - 1), Side.LEFT: Coordinates(self.x - 1, self.y)}
        if corners:
            adjacent.update({Side.TOPRIGHT: Coordinates(self.x + 1, self.y + 1), Side.BOTTOMRIGHT: Coordinates(self.x + 1, self.y - 1), Side.BOTTOMLEFT: Coordinates(self.x - 1, self.y - 1), Side.TOPLEFT: Coordinates(self.x - 1, self.y + 1)})
        return adjacent
        
    def get_location(self, side: Side):
        return Location(self.x, self.y, side)


class Location():

    def __init__(self, x: int, y: int, side: Side):
        self.coordinates = Coordinates(x, y)
        self.side = side

    def __str__(self):
        return f"({self.coordinates.x}, {self.coordinates.y}): {self.side}"
    
    def __eq__(self, other):
        return self.coordinates == other.coordinates and self.side == other.side