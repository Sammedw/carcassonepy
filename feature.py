from tile import Location
from meeple import Meeple

class Feature():

    def __init__(self):
        self.frontier_locations: list[Location] = []
        self.meeples: list[Meeple] = []

    def merge_features(self, other_features):
        pass
