import random
from baseagent import BaseAgent
from game import Game
from tile import Tile
from action import Action
from location import Coordinates
from enums import FeatureType

class Human(BaseAgent):
    
    def __init__(self, player_num: int, game: Game):
        super().__init__(player_num, game)

    def make_move(self, next_tile: Tile):
        valid_actions = super().make_move(next_tile)
        # check if there are any valid moves
        #print(list(map(str, valid_actions)))
        if len(valid_actions) == 0:
            print("WHY")

        print(f"Player {self.player_num} - Next tile: {next_tile}")
        new_action = None
        while True:
            try:
                x_coord = input("X: ")
                y_coord = input("Y: ")
                rotation = input("Rotation: ")
                meeple_location = input("Meeple location (city, road, farm, monastery, none): ")
                meeple_location = {"city": FeatureType.CITY, "road": FeatureType.ROAD, "farm": FeatureType.FARM, "monastery": FeatureType.MONASTERY, "none": None}[meeple_location]
                meeple_location_num = input("Feature number: ")
                new_action = Action(next_tile.name, int(rotation), Coordinates(int(x_coord), int(y_coord)), meeple_location, int(meeple_location_num))
                print(str(new_action))
                if not self.game.is_action_valid(new_action):
                #if not any(new_action == action for action in valid_actions):
                    raise Exception("Not a valid action")
                break
            except (ValueError, KeyError, Exception):
                print("--- Invalid action ---")
        self.game.make_action(new_action)