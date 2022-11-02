from feature import *
from tile import Tile

class FeatureManager:

    def __init__(self, start_tile: Tile):
        self.features: dict[Any, set[Feature]]
        self.monasteries: dict[TileMonastery, Coordinates]
        self.child_tile_features: dict[Feature, set[TileFeature]]
        self.parent_feature: dict[TileFeature, Feature]
        self.reset(start_tile)

    def reset(self, start_tile: Tile):
        self.features = {feature_type:set() for feature_type in [City, Road, Farm]}
        self.monasteries = dict()
        self.child_tile_features = dict()
        self.parent_feature = dict()

        for tile_feature in start_tile.cities + start_tile.roads + start_tile.farms:
            # generate start feature
            self.generate_parent_feature(tile_feature, Coordinates(0,0))
        if start_tile.monastery:
            self.add_monastery(start_tile.monastery)

    def add_feature(self, new_feature: Feature, child_tile_feature: TileFeature):
        self.features[type(new_feature)].add(new_feature)
        self.child_tile_features[new_feature] = set([child_tile_feature])
        self.parent_feature[child_tile_feature] = new_feature

    def add_monastery(self, new_monastery: TileMonastery, coordinates: Coordinates):
        self.monasteries[new_monastery] = coordinates           

    def merge_features(self, tile_feature: TileFeature, tile_feature_coordinates: Coordinates, joining_sides: list[Side], merging_features: set[Feature]) -> Feature:
        assert len(merging_features) >= 1, "There must be atleast one merging feature"
        # merge features
        merging_feature = merging_features.pop()
        merging_feature.merge_features(tile_feature, tile_feature_coordinates, joining_sides, merging_features)
        # remove old features
        for old_feature in merging_features:
            self.features[type(old_feature)].remove(old_feature)
        # update child and parent features
        self.parent_feature[tile_feature] = merging_feature
        self.child_tile_features[merging_feature].add(tile_feature)
        for other_feature in merging_features:
            child_features = self.child_tile_features[other_feature]
            for child_feature in child_features:
                self.parent_feature[child_feature] = merging_feature
            self.child_tile_features[merging_feature].union(child_features)
            del self.child_tile_features[other_feature]
        return merging_feature
    
    def generate_parent_feature(self, tile_feature: TileCity | TileRoad | TileFarm, coordinates: Coordinates):
        new_feature = tile_feature.generate_parent_feature(coordinates)
        self.add_feature(new_feature, tile_feature)
    
    def get_parent_feature(self, tile_feature: TileFeature) -> Optional[Feature]:
        if tile_feature in self.parent_feature:
            return self.parent_feature[tile_feature]
        else:
            return None

    def score_farms(self, player_count: int):
        scores = [0 for _ in range(player_count)]
        for farm in self.features[Farm]:
            # check if anyone controls farm
            controlling_players = farm.get_controlling_player(player_count)
            if len(controlling_players) == 0:
                continue
            # add 3 points per completed city adjacent to farm
            score = 0
            scored_cities = []
            for tile_city in farm.adjacent_cities: 
                city = self.get_parent_feature(tile_city)
                if (city.is_complete() and city not in scored_cities):
                    scored_cities.append(city)
                    score += 3
            # add score to each controlling player
            for player in controlling_players:
                scores[player] += score
            return score