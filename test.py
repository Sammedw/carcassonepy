
from itertools import cycle
from CFRagent import CFRAgent
from UCTagent import UCTAgent
from randomagent import RandomAgent
from game import Game


game = Game(2)
#players = [RandomAgent(0, game), RandomAgent(1, game)] #UCTAgent(0, game)
players = [RandomAgent(0, game), UCTAgent(1, game)]
#players = [CFRAgent(0, game), RandomAgent(1, game)]

scores = [0,0]

for g in range(10000):
    player_cycle = cycle(players)
    while(not game.is_game_over()):
        next_tile = game.deck.peak_next_tile()
        # check for any valid moves
        if (len(game.get_valid_actions(next_tile)) == 0):
            continue
        next(player_cycle).make_move(next_tile)

    game.print_game_state()
    game_scores = game.compute_final_score()
    if game_scores[0] > game_scores[1]:
        scores[0] += 1
    elif game_scores[0] < game_scores[1]:
        scores[1] += 1

    print(f"GAMES: {scores}") 
    game.reset()
