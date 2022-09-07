from typing import Optional
from tile import Location

class Meeple():

    def __init__(self, player: int):
        self.player = player
        self.location: Optional[Location] = None
