from copy import deepcopy
from typing import Optional, Type
from enums import *
from location import *
from feature import *
from random import shuffle


class Tile():

    def __init__(self, name: str, top_type: ConnectionType, right_type: ConnectionType, bottom_type: ConnectionType, left_type: ConnectionType, 
                cities: list[TileCity] = [], roads: list[TileRoad] = [], monastery: Optional[TileMonastery] = None, farms: list[TileFarm] = [],
                attributes: list[TileAttribute] = []):     
        self.name = name   
        self.sides: dict[Side, ConnectionType] = {Side.TOP: top_type, Side.RIGHT: right_type, Side.BOTTOM: bottom_type, Side.LEFT: left_type}
        self.cities = cities
        self.roads = roads
        self.monastery = monastery
        self.farms = farms
        self.attributes = attributes

    def __str__(self):
        return self.name

    def rotate_clockwise(self, times: int):
        if times <= 0:
            return 
        # rotate sides
        self.sides = {Side.TOP: self.sides[Side.LEFT], Side.RIGHT: self.sides[Side.TOP], Side.BOTTOM: self.sides[Side.RIGHT], Side.LEFT: self.sides[Side.BOTTOM]}
        # rotate features
        for city in self.cities:
            city.sides = [side.rotate_clockwise() for side in city.sides]
        for road in self.roads:
            road.sides = [side.rotate_clockwise() for side in road.sides]
        for farm in self.farms:
            farm.sides = [side.rotate_clockwise() for side in farm.sides]
        # rotate n-1 more times    
        self.rotate_clockwise(times-1)

    def get_tile_feature_from_side(self, side: Side, feature_type: FeatureType) -> Optional[TileFeature]:
        assert not side == Side.CENTER, "Cannot find feature in center"
        assert not feature_type == FeatureType.MONASTERY, "Monasteries are always in the center"
        assert (not feature_type == FeatureType.FARM) or (side == Side.TOP or side == Side.RIGHT or side == Side.BOTTOM or side == Side.LEFT)
        
        if feature_type == FeatureType.CITY:
            feature_list = self.cities
        elif feature_type == FeatureType.ROAD:
            feature_list = self.roads
        elif feature_type == FeatureType.FARM:
            feature_list = self.farms
        
        for feature in feature_list:
            if side in feature.get_sides():
                return feature
        
        return None


class TileSet():

    def __init__(self, name: str,  tiles: dict[Tile, int], start_tile: Optional[Tile] = None, end_tile: Optional[Tile] = None):
        self.name = name
        self.tiles = tiles
        self.start_tile = start_tile
        self.end_tile = end_tile

    def return_tile_list(self) -> list[Tile]:
        tile_list: list[Tile] = []
        # add tiles to list depending on their qty
        for tile, qty in self.tiles.items():
            for _ in range(qty):
                tile_list.append(deepcopy(tile))
        return tile_list


class Deck():

    def __init__(self, base_tile_set: TileSet, additional_tile_sets: list[TileSet] = []):
        self.tiles: list[Tile] = []
        # look for river set
        for tile_set in additional_tile_sets:
            if tile_set.name == "river":
                # add river to start of deck
                assert isinstance(tile_set.start_tile, Tile), "River must include a start tile"
                self.tiles.append(tile_set.start_tile)
                river_tiles = tile_set.return_tile_list()
                shuffle(river_tiles)
                self.tiles += river_tiles
                assert isinstance(tile_set.end_tile, Tile), "River must include an end tile"
                self.tiles.append(tile_set.end_tile)
                additional_tile_sets.pop(additional_tile_sets.index(tile_set))
                break
        else:
            # no river found, add normal start tile
            assert isinstance(base_tile_set.start_tile, Tile), "Base set must include a start tile"
            self.tiles.append(base_tile_set.start_tile)

        # add rest of tiles
        tile_list: list[Tile] = base_tile_set.return_tile_list()
        for additional_tile_set in additional_tile_sets:
            tile_list += additional_tile_set.return_tile_list()
        shuffle(tile_list)
        self.tiles += tile_list
        self.next_tile = 0

    def get_next_tile(self) -> Tile:
        next_tile_obj = self.tiles[self.next_tile]
        self.next_tile += 1
        return next_tile_obj

    def peak_next_tile(self) -> Tile:
        return self.tiles[self.next_tile]