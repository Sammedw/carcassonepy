from tile import Location, TileFeature
from meeple import Meeple

class Feature():

    def __init__(self):
        self.frontier_locations: list[Location] = []
        self.meeples: list[Meeple] = []
        self.tile_count = 0

    def merge_features(self, tile_feature: TileFeature, other_features = []):
        self.tile_count += 1
        for other_feature in other_features:
            # merge frontiers and meeples
            self.frontier_locations += other_feature.frontier_locations
            self.meeples += other_feature.meeples
            # add tile count
            self.tile_count += other_feature.tile_count
