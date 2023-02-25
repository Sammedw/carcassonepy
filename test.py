
from itertools import cycle, permutations
import time
from CFRagent import CFRAgent
from MCCFRagent import MCCFRAgent
from UCTagent import UCTAgent
from randomagent import RandomAgent
from game import Game
from star1agent import Star1Agent
from human import Human

# get game info
available_agents = {"uct": UCTAgent}
print("--- Game Configuration ---")
while True:
    try:
        games = int(input("> Number of games: "))
        player_count = int(input("> Number of players: "))
        log_file = input("> Log file name: ")
        break
    except ValueError:
        print("Invalid input.")

game = Game(player_count)
players = []

# get player info
print("--- Player Configuration ---")
print(f"Available players: {', '.join(available_agents.keys())}")
for p in range(player_count):
    while True:
        player_type = input(f"> Agent type for player {p}: ")
        if player_type in available_agents.keys():
            new_player = available_agents[player_type].build(p, game)
            players.append(new_player)
            break
        else:
            print("Invalid agent type.")

# write game info into head of file
with open(log_file + ".txt", "w") as f:
    f.write("--- Game Configuration ---\n")
    f.write(f"Game count: {games}\n")
    f.write(f"Player count: {player_count}\n")
    f.write(f"Deck: {game.deck.tile_counts}\n")
    
    f.write("--- Player Configuration ---\n")
    for i, player in enumerate(players):
        f.write(f"Player {i}: {player.return_info()}\n")
    f.write("-----------------------------\n\n")
    

#players = [RandomAgent(0, game), RandomAgent(1, game)] #UCTAgent(0, game)
#players = [RandomAgent(0, game), UCTAgent(1, game, 1000, trees = 6)]
#players = [RandomAgent(0, game), CFRAgent(1, game)]
#players = [CFRAgent(0, game), UCTAgent(1, game)]
#players = [Star1Agent(0, game), RandomAgent(1, game)]
#players = [Human(0, game), UCTAgent(1, game)]
#players = [Star1Agent(0, game), UCTAgent(1, game)]
#players = [UCTAgent(0, game, 1000), MCCFRAgent(1, game, 1000)]
#players = [UCTAgent(0, game, 1000), UCTAgent(1, game, 6000, trees = 6)]
#players = [UCTAgent(0, game, 100), UCTAgent(1, game, 100)]
#players = [UCTAgent(0, game, 500), MCCFRAgent(1, game, 1000), UCTAgent(2, game, 1000)]


scores = [0 for _ in range(len(players))]
total_times = [0 for _ in range(len(players))]
total_points = [0 for _ in range(len(players))]

# create permutations of players
player_permutations = list(permutations(players))


start = time.time()
game_list = []
for g in range(games*player_count): 
    times = [0 for _ in range(len(players))]
    # update player order if in new batch of games
    if (g % games) == 0:
        players = player_permutations[g // games]

    player_cycle = cycle(players)
    # save tile list
    if g < games:
        game_list.append(game.deck.get_tile_list_string())
    # otherwise load game
    else:
        game.reset(game_list[g % games])
    while(not game.is_game_over()):
        print("hello")
        next_tile = game.deck.peak_next_tile()
        # check for any valid moves
        if (len(game.get_valid_actions(next_tile)) == 0):
            continue
        next_player = next(player_cycle)
        #print(next_player)
        turn_start = time.time()
        next_player.make_move(next_tile)
        times[next_player.player_num] += time.time() - turn_start
        print("turn complete")

    with open(log_file + ".txt", "a") as f:
        f.write(f"--- Game {g+1} ----------------\n")
        for action in game.action_sequence:
            f.write(str(action) + "\n")
        f.write(f"--- End Game Stats -------------\n")
        f.write("Scores: " + str(game.compute_scores()) + "\n")
        f.write("Times: " + str(times) + "\n")
        f.write(f"------------------------------\n\n")
    game.print_game_state()
    print(f"TIMES: {times}")
    game_scores = game.compute_scores()
    # sort scores
    sorted_scores = sorted(enumerate(game_scores), key = lambda x: x[1], reverse=True)
    best_score = sorted_scores[0][1]
    # check if there is a draw
    if sorted_scores[1][1] == best_score:
        # add 0.5 to each drawing player score
        for player, score in sorted_scores:
            if score == best_score:
                scores[player] += 0.5
            else:
                break          
    else:
        # add 1 to winning player
        scores[sorted_scores[0][0]] += 1

    for player in range(len(players)):
        total_times[player] += times[player]
        total_points[player] += game_scores[player]

    print(f"GAMES: {scores}") 
    game.reset()

duration = time.time() - start


avg_scores_str = "Average Scores: " + str(list(map(lambda x: x / games, total_points)))
avg_times_str = "Average Times: " + str(list(map(lambda x: x / games, total_times)))
avg_duration_str = "Average Game Duration: " + str(duration/games) + " seconds"

with open(log_file + ".txt", "a") as f:
    f.write("\n --- Game Batch Stats ------------\n")
    f.write(avg_scores_str + "\n")
    f.write(avg_times_str + "\n")
    f.write(avg_duration_str + "\n")

print("--------------------------------------------")
print(avg_scores_str)
print(avg_times_str)
print(avg_duration_str)
print(game_list)

# time_sum = 0 

# for g in range(100):
#     start = time.time() 
#     player_cycle = cycle(players) 
#     while(not game.is_game_over()):
#         next_tile = game.deck.peak_next_tile()
#         # check for any valid moves
#         if (len(game.get_valid_actions(next_tile)) == 0):
#             continue
#         next(player_cycle).make_move(next_tile)

#     game.print_game_state()
#     game.reset()
#     duration = time.time() - start
#     time_sum += duration
#     print("GAME DURATION: " + str(duration) + " seconds")

# print("AVERAGE RANDOM GAME DURATION: " + str(time_sum/100) + " seconds")