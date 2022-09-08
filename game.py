from enums import GamePhase
from location import Coordinates
from tile import Tile
from meeple import Meeple
from feature import City, Road, Monastery, Farm

class Game():

    def __init__(self, player_count: int):
        self.board: dict[Coordinates, Tile] = {}
        self.frontier: set[Coordinates] = set()
        self.current_player: int = 1
        self.game_phase: GamePhase = GamePhase.TILE
        self.deck: list[Tile]
        self.free_meeples: list[list[Meeple]]
        self.cities: list[City] = []
        self.roads: list[Road] = []
        self.monasteries: list[Monastery] = []
        self.farms: list[Farm] = []
        