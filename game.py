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

    def get_adjacent_tiles(self, coordinates: Coordinates) -> dict[Side, Optional[Tile]]:
        # return adjacent tiles (TRBL)
        adjacent_tiles: dict[Side, Optional[Tile]] = {Side.TOP: None, Side.RIGHT: None, Side.BOTTOM: None, Side.LEFT: None}
        adjacent_coordinates = coordinates.get_adjacent()
        for side in adjacent_coordinates.keys():
            if adjacent_coordinates[side] in self.board:
                adjacent_tiles[side] = self.board[adjacent_coordinates[side]]
        return adjacent_tiles

    def does_tile_fit(self, tile: Tile, coordinates: Coordinates) -> bool:
        # check if given tile fits at given coordinates
        if not coordinates in self.frontier:
            return False
        adjacent_tiles = self.get_adjacent_tiles(coordinates)
        # check each side
        for side in adjacent_tiles.keys():
            if (adjacent_tiles[side]):
                if adjacent_tiles[side].sides[side.get_opposite()] == tile.sides[side]: 
                    return False
        return True

    def can_place_meeple(self, tile: Tile, coordinates: Coordinates, player: int, feature_type: FeatureType, feature_number: int = 0) -> bool:
        # check player has enough meeples
        if not len(self.free_meeples[player]) > 0:
            return False
        # check if given feature exists
        feature_count = 0
        if feature_type == FeatureType.CITY:
            feature_count = len(tile.cities)
            feature_list = tile.cities
        elif feature_type == FeatureType.ROAD:
            feature_count = len(tile.roads)
            feature_list = tile.roads
        elif feature_type == FeatureType.FARM:
            feature_count = len(tile.farms)
            feature_list = tile.farms
        elif tile.monastery is None:
            return False
        if feature_number >= feature_count:
            return False
        # check all connections to feature and check for existing meeples
        tile_feature = feature_list[feature_number]
        adjacent_tiles = self.get_adjacent_tiles(coordinates)

        # check for features on adjacent tiles that already have meeples
        for side in tile_feature.get_sides():
            if feature_type == FeatureType.FARM:
                side = side.facing()
            if adjacent_tiles[side]:
                connecting_feature = adjacent_tiles[side].get_tile_feature_from_side(side.get_opposite(), feature_type)
                if not connecting_feature:
                    continue
                if connecting_feature.parent_feature:
                    if connecting_feature.parent_feature.has_meeples():
                        return False
        return True            
        
    def is_action_valid(self, action: Action):
        # check if tile fits at location
        action.tile.rotate_clockwise(action.rotation)



game = Game(2)
print(game.cities)
next = game.deck.get_next_tile()
print(next)
print(next.get_tile_feature_from_side(Side.RIGHT, FeatureType.CITY))
print(game.deck.get_next_tile())
print(game.deck.get_next_tile())

        