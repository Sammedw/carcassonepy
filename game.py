import random
from typing import Optional
from action import Action
from enums import ConnectionType, FeatureType, Side
from location import Coordinates, Location
from tile import Deck, Tile, TileSet
from meeple import Meeple
from feature import City, Road, Farm, Feature, TileFarm, TileMonastery
from featuremanager import FeatureManager
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
        self.scores: list[int]
        self.free_meeples: list[list[Meeple]]
        self.active_meeples: list[Meeple]
        self.feature_manager: FeatureManager
        self.reset()
        # action sequence
        self.action_sequence: list[Action]

    def reset(self):
        self.deck = Deck(base_set, self.additional_tile_sets)
        start_tile: Tile = self.deck.get_next_tile()
        self.board = {Coordinates(0,0): start_tile}
        self.frontier: set[Coordinates] = set(Coordinates(0,0).get_adjacent().values())
        self.current_player = 0
        self.scores = [0 for _ in range(self.player_count)]
        self.free_meeples = [[Meeple(player) for _ in range(7)] for player in range(self.player_count)]
        self.active_meeples = []
        # generate initial features
        self.feature_manager = FeatureManager(start_tile)
        self.action_sequence = []

    # return a random tile remaining from the deck
    def get_random_tile(self):
        return random.choice(self.deck.tiles)

    # return adjacent tiles (TRBL)
    def get_adjacent_tiles(self, coordinates: Coordinates, corners: bool = False) -> dict[Side, Optional[Tile]]:   
        adjacent_tiles: dict[Side, Optional[Tile]] = {Side.TOP: None, Side.RIGHT: None, Side.BOTTOM: None, Side.LEFT: None}
        # include corners if specified
        if corners:
            adjacent_tiles.update({Side.TOPRIGHT: None, Side.BOTTOMRIGHT: None,  Side.BOTTOMLEFT: None, Side.TOPLEFT: None})
        adjacent_coordinates = coordinates.get_adjacent(corners=corners)
        # iterate over adjacent coordinates to find tiles on board
        for side in adjacent_coordinates.keys():
            if adjacent_coordinates[side] in self.board:
                adjacent_tiles[side] = self.board[adjacent_coordinates[side]]
        return adjacent_tiles

    # check if given tile fits at given coordinates
    def does_tile_fit(self, tile: Tile, coordinates: Coordinates) -> bool:
        # check if coordinats are in frontier     
        if not coordinates in self.frontier:
            return False
        adjacent_tiles = self.get_adjacent_tiles(coordinates)
        # check each side fits
        for side in adjacent_tiles.keys():
            if (adjacent_tiles[side]):
                if adjacent_tiles[side].sides[side.get_opposite()] != tile.sides[side]: 
                    return False
        return True

    # returns true if player can place meeple on given feature
    def can_place_meeple(self, tile: Tile, coordinates: Coordinates, player: int, feature_type: FeatureType, feature_number: int = 0) -> bool:
        # check player has enough meeples
        if not len(self.free_meeples[player]) > 0:
            return False
        # can place meeple on monastery
        if tile.monastery is not None and feature_type == FeatureType.MONASTERY:
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
        # iterate over adjacent tile features
        for side in feature_sides:
            if adjacent_tiles[side.facing()]: 
                connecting_tile_feature = adjacent_tiles[side.facing()].get_tile_feature_from_side(side.get_opposite())
                if not connecting_tile_feature:
                    continue
                # get parent feature of adjacent tile feature
                parent_feature = self.feature_manager.get_parent_feature(connecting_tile_feature)
                if parent_feature:
                    # check if it has any meeples
                    if parent_feature.has_meeples():
                        return False
        return True            

    # returns true if a given action is valid 
    def is_action_valid(self, action: Action) -> bool:
        tile = self.deck.get_tile_by_name(action.tile_name)
        # check if tile exists in the deck
        if not tile:
            return False
        # check if tile fits at location
        valid = False
        tile.rotate_clockwise(action.rotation)
        if self.does_tile_fit(tile, action.coordinates):
            # check if the meeple can be placed
            if (action.meeple_feature_type):
                if self.can_place_meeple(tile, action.coordinates, self.current_player, action.meeple_feature_type, action.meeple_feature_number):
                    valid = True
            else:
                valid = True
        if action.rotation != 0:
            tile.rotate_clockwise(4 - action.rotation)
        return valid
    
    # returns a list of all valid actions
    def get_valid_actions(self, next_tile: Tile) -> list[Action]:
        valid_actions: list[Action] = []
        # iterate over all possible actions and check if they are valid
        for coordinates in self.frontier:
            # calculate number of rotations needed based on symmetry of tile
            for rotation in range(next_tile.get_unique_rotations()):
                # iterate over all possible ways to place meeple on features
                for feature_num in range(len(next_tile.cities)):
                    new_action = Action(next_tile.name, rotation, coordinates, FeatureType.CITY, feature_num)
                    if self.is_action_valid(new_action):
                        valid_actions.append(new_action)

                for feature_num in range(len(next_tile.roads)):
                    new_action = Action(next_tile.name, rotation, coordinates, FeatureType.ROAD, feature_num)
                    if self.is_action_valid(new_action):
                        valid_actions.append(new_action)

                for feature_num in range(len(next_tile.farms)):
                    new_action = Action(next_tile.name, rotation, coordinates, FeatureType.FARM, feature_num)
                    if self.is_action_valid(new_action):
                        valid_actions.append(new_action)

                if next_tile.monastery:
                    new_action = Action(next_tile.name, rotation, coordinates, FeatureType.MONASTERY, feature_num)
                    if self.is_action_valid(new_action):
                        valid_actions.append(new_action)

                new_action = Action(next_tile.name, rotation, coordinates)
                if self.is_action_valid(new_action):
                    valid_actions.append(new_action)
        # discard tile if no valid actions
        if len(valid_actions) == 0 and next_tile in self.deck.tiles:
            self.deck.tiles.remove(next_tile)
        return valid_actions

    # execute given action
    def make_action(self, action: Action) -> bool:
        if (self.is_action_valid(action)):
            # place tile
            tile = self.deck.get_tile_by_name(action.tile_name)
            tile.rotate_clockwise(action.rotation)
            self.board[action.coordinates] = tile
            # update frontier
            self.frontier.remove(action.coordinates)
            adjacent_tiles = self.get_adjacent_tiles(action.coordinates)
            adjacent_coordiantes = action.coordinates.get_adjacent()
            for side, adj_tile in adjacent_tiles.items():
                if adj_tile is None:
                    self.frontier.add(adjacent_coordiantes[side])
            # place meeple
            if action.meeple_feature_type is not None:
                meeple = self.free_meeples[self.current_player].pop()
                self.active_meeples.append(meeple)
                tile.place_meeple(meeple, action.coordinates, action.meeple_feature_number, action.meeple_feature_type)
            # merge features
            for tile_feature in tile.cities + tile.roads + tile.farms:
                joining_sides: list[Side] = []
                merging_features: set[Feature] = set()
                for tile_feature_side in tile_feature.get_sides():
                    # ignore side.center
                    if tile_feature_side == Side.CENTER:
                        continue
                    if adjacent_tiles[tile_feature_side.facing()] is not None:
                        if type(tile_feature) == TileFarm:
                            joining_sides += tile_feature_side.decompose()
                        else:
                            joining_sides.append(tile_feature_side)
                        # get adjacent parent feature
                        merging_feature = self.feature_manager.get_parent_feature(adjacent_tiles[tile_feature_side.facing()].get_tile_feature_from_side(tile_feature_side.get_opposite()))
                        merging_features.add(merging_feature)
                # connect features
                if len(merging_features) > 0:
                    combined_feature = self.feature_manager.merge_features(tile_feature, action.coordinates, joining_sides, merging_features)
                    # check if feature is complete
                    if combined_feature.is_complete():
                        # find meeple majority
                        controlling_players = combined_feature.get_controlling_player(self.player_count)
                        # add score
                        score = combined_feature.score()
                        for player in controlling_players:
                            self.scores[player] += score
                        # return meeples to players
                        for meeple in combined_feature.meeples:
                            self.active_meeples.remove(meeple)
                            meeple.location = None
                            self.free_meeples[meeple.player].append(meeple)
                # create new feature
                else:
                    self.feature_manager.generate_parent_feature(tile_feature, action.coordinates)

            # track monastery if meeple placed on it
            if (action.meeple_feature_type == FeatureType.MONASTERY):
                self.feature_manager.add_monastery(tile.monastery, action.coordinates)
            # check for complete monasteries
            for monastery, coordinates in list(self.feature_manager.monasteries.items()):
                if None not in self.get_adjacent_tiles(coordinates, corners=True).values():
                    # score completed monastery
                    self.scores[monastery.meeple.player] += 9
                    del self.feature_manager.monasteries[monastery]
            # remove tile from deck
            self.deck.tiles.remove(tile)
            # update player
            self.current_player = (self.current_player + 1) % self.player_count
            # add to action list
            self.action_sequence.append(action)
            return True
        else:
            return False

    def is_game_over(self) -> bool:
        # check if there are any tiles left
        if len(self.deck.tiles) > 0:
            return False
        else:
            return True

    def compute_scores(self) -> list[int]:
        final_scores = [0 for _ in range(self.player_count)]
        # iterate over incomplete features
        for feature in self.feature_manager.features[City].union(self.feature_manager.features[Road]):
            if not feature.is_complete():
                # find meeple majority
                controlling_players = feature.get_controlling_player(self.player_count)
                # add score
                score = feature.score()
                for player in controlling_players:
                    final_scores[player] += score 
        # iterate over incomplete monasteries
        for monastery, coordinates in self.feature_manager.monasteries.items():
            final_scores[monastery.meeple.player] += len(list(filter(None, self.get_adjacent_tiles(coordinates, corners=True).values()))) + 1
        # add current scores and farm scores
        farm_scores = self.feature_manager.score_farms(self.player_count)
        for player in range(self.player_count):
            final_scores[player] += self.scores[player] + farm_scores[player]

        return final_scores

    def print_game_state(self):
        print("Action sequence ---------------------------")
        for action in self.action_sequence:
            print(action)
        print("-------------------------------------------")
        print("Cities: ", len(self.feature_manager.features[City]))
        print("Roads: ", len(self.feature_manager.features[Road]))
        print("Farms: ", len(self.feature_manager.features[Farm]))
        print("FINAL SCORES: ", self.compute_scores())

    def get_action_history_str(self):
        return " | ".join(list(map(str, self.action_sequence)))

    def get_state_str(self):
        state_str = "BOARD: {"
        sorted_board = sorted(self.board.items(), key=lambda loc: loc[0])
        # add board with sorted locations
        state_str += ", ".join(list(map(lambda loc: f"{loc[0]}: <{loc[1]}, {loc[1].rotation}>", sorted_board))) + "}"
        # add sorted tiles in deck
        state_str += f" DECK: {list(map(str, sorted(self.deck.tiles, key=lambda tile: tile.name)))}"
        # add sorted location of meeples
        sorted_meeples = sorted(self.active_meeples, key=lambda meeple: meeple.location.coordinates)
        state_str += " MEEPLES: [" + ", ".join(list(map(lambda meeple: f"<{meeple.location.coordinates}, {meeple.location.side}, {meeple.player}>", sorted_meeples))) + "]"
        # add scores
        state_str += f" SCORES: {self.scores}"
        return state_str
