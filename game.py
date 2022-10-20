from calendar import c
from msilib.schema import Feature
from typing import Optional
from action import Action
from enums import FeatureType, Side
from location import Coordinates, Location
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
        self.frontier: list[Coordinates] = list(Coordinates(0,0).get_adjacent().values())
        self.current_player = 0
        self.free_meeples = [[Meeple(player) for _ in range(7)] for player in range(self.player_count)]
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
                if adjacent_tiles[side].sides[side.get_opposite()] != tile.sides[side]: 
                    return False
        return True

    def can_place_meeple(self, tile: Tile, coordinates: Coordinates, player: int, feature_type: FeatureType, feature_number: int = 0) -> bool:
        # check player has enough meeples
        if not len(self.free_meeples[player]) > 0:
            return False
        # can place meeple on monastery
        if tile.monastery is not None:
            return True
        # check if given feature exists
        tile_feature = tile.get_tile_feature_by_num(feature_number, feature_type)
        if tile_feature is None:
            return False
        # check all connections to feature and check for existing meeples
        adjacent_tiles = self.get_adjacent_tiles(coordinates)
        feature_sides = tile_feature.get_sides()
        if Side.CENTER in feature_sides:
            feature_sides.remove(Side.CENTER)
        for side in feature_sides:
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
        
    def is_action_valid(self, action: Action) -> bool:
        # check if tile fits at location
        valid = False
        action.tile.rotate_clockwise(action.rotation)
        if action.tile is self.deck.peak_next_tile():
            if self.does_tile_fit(action.tile, action.coordinates):
                # check if the meeple can be placed
                if (action.meeple_feature_type):
                    if self.can_place_meeple(action.tile, action.coordinates, self.current_player, action.meeple_feature_type, action.meeple_feature_number):
                        valid = True
                else:
                    valid = True
        if action.rotation != 0:
            action.tile.rotate_clockwise(4 - action.rotation)
        return valid
        
    def get_valid_actions(self) -> list[Action]:
        next_tile = self.deck.peak_next_tile()
        valid_actions: list[Action] = []
        # iterate over all possible actions and check if they are valid
        for coordinates in self.frontier:
            # calculate number of rotations needed based on symmetry of tile
            for rotation in range(next_tile.get_unique_rotations()):
                for feature_num in range(len(next_tile.cities)):
                    new_action = Action(next_tile, rotation, coordinates, FeatureType.CITY, feature_num)
                    if self.is_action_valid(new_action):
                        valid_actions.append(new_action)

                for feature_num in range(len(next_tile.roads)):
                    new_action = Action(next_tile, rotation, coordinates, FeatureType.ROAD, feature_num)
                    if self.is_action_valid(new_action):
                        valid_actions.append(new_action)

                for feature_num in range(len(next_tile.farms)):
                    new_action = Action(next_tile, rotation, coordinates, FeatureType.FARM, feature_num)
                    if self.is_action_valid(new_action):
                        valid_actions.append(new_action)

                if next_tile.monastery:
                    new_action = Action(next_tile, rotation, coordinates, FeatureType.MONASTERY, feature_num)
                    if self.is_action_valid(new_action):
                        valid_actions.append(new_action)

                new_action = Action(next_tile, rotation, coordinates)
                if self.is_action_valid(new_action):
                    valid_actions.append(new_action)

        return valid_actions

    def make_action(self, action: Action) -> bool:
        if (self.is_action_valid(action)):
            # place tile
            self.board[action.coordinates] = action.tile.rotate_clockwise(action.rotation)
            # place meeple
            if action.meeple_feature_type is not None:
                action.tile.place_meeple(self.free_meeples[self.current_player].pop(), action.coordinates, action.meeple_feature_number, action.meeple_feature_type)
            adjacent_tiles = self.get_adjacent_tiles(action.coordinates)
            for tile_feature in action.tile.cities + action.tile.roads + action.tile.farms:
                for tile_feature_side in tile_feature.get_sides():
                    connecting_sides: list[Side] = []
                    merging_features = []
                    if adjacent_tiles[tile_feature_side.facing()] is not None:
                        connecting_sides.append(tile_feature_side)
                        # get adjacent parent feature
                        merging_feature = adjacent_tiles[tile_feature_side.facing()].get_tile_feature_from_side(tile_feature_side.get_opposite())
                        merging_features.append(merging_feature)



game = Game(2)
print(game.deck)
print(game.board)
for action in game.get_valid_actions():
    print(action)