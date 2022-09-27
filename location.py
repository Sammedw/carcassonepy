from enums import Side

class Coordinates():

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(f"({self.x}, {self.y})")

    def get_adjacent(self):
        return {Coordinates(self.x, self.y + 1), Coordinates(self.x + 1, self.y), Coordinates(self.x, self.y - 1), Coordinates(self.x - 1, self.y)}

    def get_location(self, side: Side):
        return Location(self.x, self.y, side)


class Location():

    def __init__(self, x: int, y: int, side: Side):
        self.coordinates = Coordinates(x, y)
        self.side = side

    def __str__(self):
        return 
    
    def __eq__(self, other):
        return self.coordinates == other.coordinates and self.side == other.side