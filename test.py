
from itertools import cycle
from agents.randomagent import RandomAgent
from game import Game
from location import Coordinates


game = Game(2);
players = [RandomAgent(p, game) for p in range(2)]

player_cycle = cycle(players)
while(not game.is_game_over()):
    next_tile = game.deck.peak_next_tile()
    # check for any valid moves
    if (len(game.get_valid_actions(next_tile)) == 0):
        continue
    next(player_cycle).make_move(next_tile)

game.print_game_state()