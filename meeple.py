from typing import Optional
from location import Location

class Meeple():

    def __init__(self, player: int):
        self.player = player
        self.location: Optional[Location] = None
