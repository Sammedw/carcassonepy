from itertools import cycle
from game import Game
from randomagent import RandomAgent

game = Game(2)
random1 = RandomAgent(0,game)
random2 = RandomAgent(1,game)
players = [random1, random2]

for g in range(10000):
    player_cycle = cycle(players)
    game.reset()
    # play game
    while(not game.is_game_over()):
        next_tile = game.deck.peak_next_tile()
        # check for any valid moves
        if (len(game.get_valid_actions(next_tile)) == 0):
            continue
        next_player = next(player_cycle)
        next_player.make_move(next_tile)
    print(f"Game {g} complete")

avg_actions = (random1.total_action_count + random2.total_action_count) / (random1.turn_count + random2.turn_count)
print(f"--- average action count = {avg_actions} ---")