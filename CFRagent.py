import random
from baseagent import BaseAgent
from game import Game
from tile import Tile

class Node:

    def __init__(self, state: str):
        self.state = state
        

class CFRAgent(BaseAgent):
    
    def __init__(self, player_num: int, game: Game):
        super().__init__(player_num, game)

    def make_move(self, next_tile: Tile):
        valid_actions = super().make_move(next_tile)
        action = random.choice(valid_actions)
        self.game.make_action(action)
        print(action)