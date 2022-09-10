from enums import GamePhase
from location import Coordinates
from tile import Deck, Tile
from meeple import Meeple
from feature import City, Road, Monastery, Farm

class Game():

    def __init__(self, player_count: int, decks: list[Deck], ):
        assert player_count >= 2 and player_count <= 5, "Player count must be between 2 and 5"

        self.board: dict[Coordinates, Tile] = {}
        self.frontier: set[Coordinates] = set()
        self.current_player: int = 1
        self.game_phase: GamePhase = GamePhase.TILE
        self.deck: Deck
        self.free_meeples: list[list[Meeple]]
        self.cities: list[City] = []
        self.roads: list[Road] = []
        self.monasteries: list[Monastery] = []
        self.farms: list[Farm] = []


        