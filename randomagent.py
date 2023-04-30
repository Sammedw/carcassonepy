import random
from baseagent import BaseAgent
from game import Game
from tile import Tile

class RandomAgent(BaseAgent):
    
    def __init__(self, player_num: int, game: Game):
        super().__init__(player_num, game)
        self.total_action_count = 0
        self.turn_count = 0

    @staticmethod
    def build(player_num: int, game: Game):
        print("--- Build Random agent ---")
        return RandomAgent(player_num, game)

    def return_info(self):
        return "Random Agent()"

    def make_move(self, next_tile: Tile):
        valid_actions = super().make_move(next_tile)
        self.total_action_count += len(valid_actions)
        self.turn_count += 1
        action = random.choice(valid_actions)
        self.game.make_action(action)