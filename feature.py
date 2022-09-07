from typing import Optional
from location import Location, Coordinates
from enums import FeatureType, Side, TileFeatureAttribute
from meeple import Meeple


class TileFeature():

    def __init__(self, type: FeatureType, sides: list[Side], attributes: list[TileFeatureAttribute] = []):
        self.type = type
        self.sides = sides
        self.attributes = attributes
        self.meeple: Optional[Meeple] = None
        self.parent_feature: Optional[Feature] = None

    def __str__(self):
        return f"TileFeature<{str(self.type)} | {[str(side) for side in self.sides]}>"


class TileFarm(TileFeature):

    def __init__(self, sides: list[Side], attributes: list[TileFeatureAttribute], adjacent_cities: set[TileFeature] = set()):
        super().__init__(FeatureType.FARM, sides, attributes)
        self.adjacent_cities = adjacent_cities

class Feature():

    def __init__(self):
        self.frontier_locations: list[Location] = []
        self.meeples: list[Meeple] = []
        self.tile_count = 1

    def merge_features(self, tile_feature: TileFeature, tile_feature_coordinates: Coordinates, joining_sides: list[Side], other_features = []):
        # merge tile feature
        tile_feature.parent_feature = self
        self.tile_count += 1
        # add locations of tile feature to frontier that are not involved with connection
        for side in tile_feature.sides:
            if side not in joining_sides:
                self.frontier_locations.append(Location(tile_feature_coordinates.x, tile_feature_coordinates.y, side))


        # merge other features
        for other_feature in other_features:
            # merge frontiers and meeples
            self.frontier_locations += other_feature.frontier_locations
            self.meeples += other_feature.meeples
            # add tile count
            self.tile_count += other_feature.tile_count

    def is_complete(self) -> bool:
        return (len(self.frontier_locations) == 0)

    def score(self) -> int:
        return self.tile_count


class City(Feature):

    def __init__(self):
        super().__init__();
        self.shield_count: int = 0

    def score(self) -> int:
        score: int = self.tile_count + self.shield_count
        if self.is_complete():
            score *= 2
        return score


class Road(Feature):

    def __init__(self):
        super().__init__()


class Monastery(Feature):

    def __init__(self):
        super().__init__()


class Farm(Feature):

    def __init__(self):
        super().__init__()
        self.adjacent_cities: set[City] = []

    def merge_features(self, tile_feature, tile_feature_coordinates: Coordinates, joining_sides: list[Side], other_features=[]):
        super().merge_features(tile_feature, tile_feature_coordinates, joining_sides, other_features)
        # merge adjacent cities
        self.adjacent_cities.union(tile_feature.adjacent_cities)
        for other_feature in other_features:
            self.adjacent_cities = self.adjacent_cities.union(other_feature.adjacent_cities)

    def score(self) -> int:
        score: int = 0
        for city in self.adjacent_cities:
            if (city.is_complete()):
                score += 3
        return score