from typing import Optional
from location import Location, Coordinates
from enums import Side, TileFeatureAttribute
from meeple import Meeple


class TileFeature():

    def __init__(self, sides: list[Side], attributes: list[TileFeatureAttribute] = []):
        self.sides = sides
        self.attributes = attributes
        self.meeple: Optional[Meeple] = None
        self.parent_feature: Optional[Feature] = None

    def get_sides(self):
        return self.sides


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
        self.parent_feature = new_city
        return new_city


class TileRoad(TileFeature):

    def __init__(self, sides: list[Side], attributes: list[TileFeatureAttribute] = []):
        super().__init__(sides, attributes)

    def __str__(self):
        return f"TileRoad<{[str(side) for side in self.sides]}>"

    def generate_parent_feature(self, coordinates: Coordinates):
        new_road = Road([coordinates.get_location(side) for side in self.sides])
        if self.meeple:
            new_road.meeples = [self.meeple]
        self.parent_feature = new_road
        return new_road


class TileMonastery(TileFeature):

    def __init__(self, attributes: list[TileFeatureAttribute] = []):
        super().__init__([Side.CENTER], attributes)

    def __str__(self):
        return f"TileMonastery"

    def generate_parent_feature(self, coordinates: Coordinates, joining_sides: list[Side]):
        sides = list({Side.TOP, Side.RIGHT, Side.BOTTOM, Side.LEFT} - set(joining_sides))
        new_monastery = Monastery([coordinates.get_location(side) for side in sides])
        if self.meeple:
            new_monastery.meeples = [self.meeple]
        self.parent_feature = new_monastery
        return new_monastery


class TileFarm(TileFeature):

    def __init__(self, sides: list[Side], attributes: list[TileFeatureAttribute] = [], adjacent_cities = set()):
        super().__init__(sides, attributes)
        self.adjacent_cities = adjacent_cities

    def __str__(self):
        return f"TileFarm<{[str(side) for side in self.sides]}>"

    def generate_parent_feature(self, coordinates: Coordinates):
        new_farm = Farm([coordinates.get_location(side) for side in self.sides])
        if self.meeple:
            new_farm.meeples = [self.meeple]
        new_farm.adjacent_cities = self.adjacent_cities
        self.parent_feature = new_farm
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
        tile_feature.parent_feature = self
        self.tile_count += 1
        if (tile_feature.meeple):
            self.meeples.append(tile_feature.meeple)
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

    def has_meeples(self) -> bool:
        return len(self.meeples) > 0

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


class Road(Feature):

    def __init__(self, frontier_locations: list[Location] = []):
        super().__init__(frontier_locations)


class Monastery(Feature):

    def __init__(self, frontier_locations: list[Location] = []):
        super().__init__(frontier_locations)


class Farm(Feature):

    def __init__(self, frontier_locations: list[Location] = []):
        super().__init__(frontier_locations)
        self.adjacent_cities: set[City] = set()
        
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