from location import Coordinates
from tile import Deck, Tile, TileSet
from meeple import Meeple
from feature import City, Road, Monastery, Farm
from sets import base_set

class Game():

    def __init__(self, player_count: int, additional_tile_sets: list[TileSet] = []):
        assert player_count >= 2 and player_count <= 5, "Player count must be between 2 and 5"
        self.player_count = player_count
        self.additional_tile_sets = additional_tile_sets
        self.deck: Deck
        self.board: dict[Coordinates, Tile]
        self.frontier: set[Coordinates]
        self.current_player: int
        self.free_meeples: list[list[Meeple]]
        self.cities: list[City]
        self.roads: list[Road]
        self.monasteries: list[Monastery]
        self.farms: list[Farm]
        self.reset()

    def reset(self):
        self.deck = Deck(base_set, self.additional_tile_sets)
        start_tile: Tile = self.deck.get_next_tile()
        self.board = {Coordinates(0,0): start_tile}
        self.frontier = Coordinates(0,0).get_adjacent()
        self.current_player = 0
        self.free_meeples = [Meeple(player) for _ in range(7) for player in range(self.player_count)]
        # generate initial features
        self.cities = []
        for city in start_tile.cities:
            self.cities.append(city.generate_parent_feature(Coordinates(0,0)))
        self.roads = []
        for road in start_tile.roads:
            self.roads.append(road.generate_parent_feature(Coordinates(0,0)))
        self.monasteries = []
        if start_tile.monastery:
            self.monasteries.append(start_tile.monastery)
        self.farms = []
        for farm in start_tile.farms:
            self.farms.append(farm.generate_parent_feature(Coordinates(0,0)))


game = Game(2)
print(game.cities)

        