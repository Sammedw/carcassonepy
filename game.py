from typing import Optional
from action import Action
from enums import FeatureType, Side
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
            self.monasteries.append(start_tile.monastery.generate_parent_feature(Coordinates(0,0), []))
        self.farms = []
        for farm in start_tile.farms:
            self.farms.append(farm.generate_parent_feature(Coordinates(0,0)))

    def get_adjacent_tiles(self, coordinates: Coordinates) -> list[Optional[Tile]]:
        # return adjacent tiles (TRBL)
        adjacent: list[Optional[Tile]] = []
        for coordinate in coordinates.get_adjacent():
            if coordinate in self.board:
                adjacent.append(self.board[coordinate])
            else:
                adjacent.append(None)
        return adjacent

    def does_tile_fit(self, tile: Tile, coordinates: Coordinates) -> bool:
        # check if given tile fits at given coordinates
        if not coordinates in self.frontier:
            return False
        adjacent_tiles = self.get_adjacent_tiles(coordinates)
        # check each side
        if (not adjacent_tiles[0]) or adjacent_tiles[0].sides[Side.BOTTOM] == tile.sides[Side.TOP]: 
            return False
        if (not adjacent_tiles[1]) or adjacent_tiles[1].sides[Side.LEFT] == tile.sides[Side.RIGHT]: 
            return False
        if (not adjacent_tiles[2]) or adjacent_tiles[2].sides[Side.TOP] == tile.sides[Side.BOTTOM]: 
            return False
        if (not adjacent_tiles[3]) or adjacent_tiles[3].sides[Side.RIGHT] == tile.sides[Side.LEFT]: 
            return False
        return True

    def can_place_meeple(self, tile: Tile, player: int, feature_type: FeatureType, feature_number: int = 0):
        # check if given feature exists
        feature_count = 0
        if feature_type == FeatureType.CITY:
            feature_count = len(tile.cities)
        elif feature_type == FeatureType.ROAD:
            feature_count = len(tile.roads)
        elif feature_type == FeatureType.FARM:
            feature_count = len(tile.farms)
        elif tile.monastery is None:
            return False
        
        if feature_number >= feature_count:
            return False

        # check all connections to feature and check for existing meeples
        
        
        
    def is_action_valid(self, action: Action):
        # check if tile fits at location
        action.tile.rotate_clockwise(action.rotation)



game = Game(2)
print(game.cities)
print(game.deck.get_next_tile())
print(game.deck.get_next_tile())
print(game.deck.get_next_tile())

        