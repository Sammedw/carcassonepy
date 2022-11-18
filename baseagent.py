from game import Game
from tile import Tile

class BaseAgent:

    def __init__(self, player_num: int, game: Game):
        self.player_num = player_num
        self.game = game

    def make_move(self, next_tile: Tile):
        # check if it is agent's turn
        if self.game.current_player != self.player_num:
            return
        return self.game.get_valid_actions(next_tile)
