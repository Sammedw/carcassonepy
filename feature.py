from abc import abstractmethod
from ntpath import join
from tile import Location, TileFeature, Coordinates, Side
from meeple import Meeple

class Feature():

    def __init__(self):
        self.frontier_locations: list[Location] = []
        self.meeples: list[Meeple] = []
        self.tile_count = 1

    def merge_features(self, tile_feature: TileFeature, tile_feature_coordinates: Coordinates, joining_sides: list[Side], other_features = []):
        # merge tile feature
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

