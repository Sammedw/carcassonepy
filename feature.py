import random
from typing import Any, Optional, Type
from location import Location, Coordinates
from enums import Side, TileFeatureAttribute
from meeple import Meeple


class TileFeature():

    def __init__(self, sides: list[Side], attributes: list[TileFeatureAttribute] = []):
        self.sides = sides
        self.attributes = attributes
        self.meeple: Optional[Meeple] = None

    def get_sides(self):
        return self.sides
    
    def place_meeple(self, meeple: Meeple, coordinates: Coordinates):
        if self.meeple is None:
            self.meeple = meeple
            meeple_sides = list(self.sides)
            if Side.CENTER in meeple_sides and len(meeple_sides) > 1:
                meeple_sides.remove(Side.CENTER)
            meeple.location = Location(coordinates.x, coordinates.y, random.choice(meeple_sides))


class TileCity(TileFeature):

    def __init__(self, sides: list[Side], attributes: list[TileFeatureAttribute] = []):
        super().__init__(sides, attributes)

    def __str__(self):
        return f"TileCity<{[str(side) for side in self.sides]}>"

    def generate_parent_feature(self, coordinates: Coordinates):
        new_city = City([coordinates.get_location(side) for side in self.sides])
        if TileFeatureAttribute.SHIELD in self.attributes:
            new_city.shield_count = 1
        if self.meeple:
            new_city.meeples = [self.meeple]
        return new_city


class TileRoad(TileFeature):

    def __init__(self, sides: list[Side], attributes: list[TileFeatureAttribute] = []):
        super().__init__(sides, attributes)

    def __str__(self):
        return f"TileRoad<{[str(side) for side in self.sides]}>"

    def generate_parent_feature(self, coordinates: Coordinates):
        sides = list(self.sides)
        if Side.CENTER in self.sides:
            sides.remove(Side.CENTER)
        new_road = Road([coordinates.get_location(side) for side in sides])
        if self.meeple:
            new_road.meeples = [self.meeple]
        return new_road


class TileMonastery(TileFeature):

    def __init__(self, attributes: list[TileFeatureAttribute] = []):
        super().__init__([Side.CENTER], attributes)

    def __str__(self):
        return f"TileMonastery"
        

class TileFarm(TileFeature):

    def __init__(self, sides: list[Side], attributes: list[TileFeatureAttribute] = [], adjacent_cities = set()):
        super().__init__(sides, attributes)
        assert Side.TOP not in sides and Side.RIGHT not in sides and Side.BOTTOM not in sides and Side.LEFT not in sides, "Farms must be defined using corners"
        self.adjacent_cities = adjacent_cities

    def __str__(self):
        return f"TileFarm<{[str(side) for side in self.sides]}>"

    def generate_parent_feature(self, coordinates: Coordinates):
        decomposed_sides = []
        for side in self.sides:
            decomposed_sides += side.decompose()
        new_farm = Farm([coordinates.get_location(halfside) for halfside in decomposed_sides])
        if self.meeple:
            new_farm.meeples = [self.meeple]
        new_farm.adjacent_cities = self.adjacent_cities
        return new_farm
    
    def get_sides(self):
        feature_sides: list[Side] = []
        # break down corners into half sides for farms
        for side in self.sides:
            feature_sides += side.decompose()
        return feature_sides


class Feature():

    def __init__(self, frontier_locations: list[Location] = []):
        self.frontier_locations = frontier_locations
        self.meeples: list[Meeple] = []
        self.tile_count = 1

    def merge_features(self, tile_feature: TileFeature, tile_feature_coordinates: Coordinates, joining_sides: list[Side], other_features = []):
        # merge tile feature
        self.tile_count += 1
        if (tile_feature.meeple):
            self.meeples.append(tile_feature.meeple)
        # add locations of tile feature to frontier that are not involved with connection
        for side in tile_feature.get_sides():
            if side not in joining_sides and side != Side.CENTER:
                self.frontier_locations.append(Location(tile_feature_coordinates.x, tile_feature_coordinates.y, side))
        # merge other features
        for other_feature in other_features:
            # merge frontiers and meeples
            self.frontier_locations += other_feature.frontier_locations
            self.meeples += other_feature.meeples
            # add tile count
            self.tile_count += other_feature.tile_count
        # remove locations no longer on frontier
        adjacent_coordinates = tile_feature_coordinates.get_adjacent()
        for side in joining_sides:
            adjacent_coordinate = adjacent_coordinates[side.facing()]
            self.frontier_locations.remove(Location(adjacent_coordinate.x, adjacent_coordinate.y, side.get_opposite()))

    def is_complete(self) -> bool:
        return (len(self.frontier_locations) == 0)

    def has_meeples(self) -> bool:
        return len(self.meeples) > 0

    def in_frontier(self, location: Location) -> bool:
        for frontier_location in self.frontier_locations:
            if frontier_location == location:
                return True
        return False

    def get_controlling_player(self, player_count: int) -> list[int]:
        if not self.has_meeples():
            return []
        meeple_counts = [0 for _ in range(player_count)]
        for meeple in self.meeples:
            meeple_counts[meeple.player] += 1
        controlling_players: list[int] = []
        max_meeples: int = 1
        for player, player_meeple_count in enumerate(meeple_counts):
            if player_meeple_count > max_meeples:
                max_meeples = player_meeple_count
                controlling_players = []
            if player_meeple_count >= max_meeples:
                controlling_players.append(player)
        return controlling_players

    def score(self) -> int:
        return self.tile_count


class City(Feature):

    def __init__(self, frontier_locations: list[Location] = []):
        super().__init__(frontier_locations)
        self.shield_count: int = 0
        
    def score(self) -> int:
        score: int = self.tile_count + self.shield_count
        if self.is_complete():
            score *= 2
        return score

    def merge_features(self, tile_feature: TileFeature, tile_feature_coordinates: Coordinates, joining_sides: list[Side], other_features = []):
        super().merge_features(tile_feature, tile_feature_coordinates, joining_sides, other_features)
        # add shields from other cities
        if TileFeatureAttribute.SHIELD in tile_feature.attributes:
            self.shield_count += 1
        for other_feature in other_features:
            self.shield_count += other_feature.shield_count


class Road(Feature):

    def __init__(self, frontier_locations: list[Location] = []):
        super().__init__(frontier_locations)


class Farm(Feature):

    def __init__(self, frontier_locations: list[Location] = []):
        super().__init__(frontier_locations)
        self.adjacent_cities: set[TileCity] = set()
        
    def merge_features(self, tile_feature, tile_feature_coordinates: Coordinates, joining_sides: list[Side], other_features=[]):
        super().merge_features(tile_feature, tile_feature_coordinates, joining_sides, other_features)
        # merge adjacent cities
        self.adjacent_cities = self.adjacent_cities.union(tile_feature.adjacent_cities)
        for other_feature in other_features:
            self.adjacent_cities = self.adjacent_cities.union(other_feature.adjacent_cities)

    def is_complete(self) -> bool:
        return False

    def score(self) -> int:
        return 0