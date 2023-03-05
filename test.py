
from itertools import cycle, permutations
import time
from CFRagent import CFRAgent
from MCCFRagent import MCCFRAgent
from UCTagent import UCTAgent
from randomagent import RandomAgent
from game import Game
from star1agent import Star1Agent
from human import Human
from copy import copy
from random import sample
from multiprocessing import Process, Queue
import sys

def simulate_games(perm_num, game, game_list, players, queue, human):

    scores = [0 for _ in range(len(players))]
    total_times = [0 for _ in range(len(players))]
    total_points = [0 for _ in range(len(players))]

    start = time.time()
    out = ""

    out += "\n--- Player Configuration ---\n"
    for i, player in enumerate(players):
        out += f"Player {i}: {player[1].return_info()}\n"
    out += "-----------------------------\n\n"

    for g in range(len(game_list)): 
        times = [0 for _ in range(len(players))]
        print(players)
        for player in players:
            print(player[1].player_num, player[1].return_info())
        player_cycle = cycle(players)
        # load tiles
        game.reset(game_list[g])
        # play game
        while(not game.is_game_over()):
            next_tile = game.deck.peak_next_tile()
            # check for any valid moves
            if (len(game.get_valid_actions(next_tile)) == 0):
                continue
            next_player = next(player_cycle)[1]
            #print(next_player)
            turn_start = time.time()
            next_player.make_move(next_tile)
            times[next_player.player_num] += time.time() - turn_start
            print("turn complete")

        # write details of game
        out += f"--- Game {g+1} ----------------\n"
        for action in game.action_sequence:
            out += str(action) + "\n"
        out += f"--- End Game Stats -------------\n"
        out += "Points: " + str(game.compute_scores()) + "\n"
        out += "Times: " + str(times) + "\n"
        out += f"------------------------------\n\n"
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

    duration = time.time() - start


    avg_scores_str = "Average Points: " + str(list(map(lambda x: x / len(game_list), total_points)))
    avg_times_str = "Average Times: " + str(list(map(lambda x: x / len(game_list), total_times)))
    avg_duration_str = "Average Game Duration: " + str(duration / len(game_list)) + " seconds"

    out += "\n --- Game Batch Stats ------------\n"
    out += f"Results: {scores}\n"
    out += avg_scores_str + "\n"
    out += avg_times_str + "\n"
    out += avg_duration_str + "\n"
    out += "-----------------------------\n\n"

    print("--------------------------------------------")
    print(avg_scores_str)
    print(avg_times_str)
    print(avg_duration_str)

    print(f"--- THREAD {perm_num} FINISHED ---")

    if human:
        return (perm_num, out, {player:score for (player, score) in zip(players, scores)}, {player:score for (player, score) in zip(players, total_points)})
    else:
        queue.put((perm_num, out, {player:score for (player, score) in zip(players, scores)}, {player:score for (player, score) in zip(players, total_points)}))
    


if __name__ == "__main__":
    available_agents = {"uct": UCTAgent, "mccfr": MCCFRAgent, "random": RandomAgent, "human": Human}

    if len(sys.argv) == 3 and sys.argv[1] == "-l":
        # read game config from file
        filename = sys.argv[2]
        with open(filename, "r") as f:
            lines = f.readlines()
        games = int(lines[0].strip("\n"))
        player_count = int(lines[1].strip("\n"))
        log_file = lines[2].strip("\n")
        game = Game(player_count)
        players = []
        # read players from file
        for p in range(player_count):
            player_string = lines[3+p].strip("\n")
            player_params = player_string.split(",")
            player_name = player_params[0]
            player_params = player_params[1:]
            players.append(available_agents[player_name](p, game, *map(float, player_params)))
    else:
        # get game info
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


    
    # create permutations of players
    player_permutations = list(permutations(enumerate(players)))
    player_permutations_temp = []
    # update player number for each permutation
    for p, permutation in enumerate(player_permutations):
        player_permutations_temp.append([])
        for i in range(player_count):
            # copy player and update player num
            player = permutation[i]
            new_player = copy(player[1]) #remove copy
            new_player.player_num = i
            new_player = (player[0], new_player)
            player_permutations_temp[p].append(new_player)
    player_permutations = player_permutations_temp

    # generate the tile orders for given number of games
    deck = game.deck.get_tile_list()
    game_list = [" ".join(sample(deck, len(deck))) for _ in range(games)]

    processes = []
    results = []
    queue = Queue()
    for p, permutation in enumerate(player_permutations):
        if any(type(x) == Human for x in players):
            results.append(simulate_games(p, game, game_list, permutation, queue, True))
        else:
            process = Process(target=simulate_games, args=(p, game, game_list, permutation, queue, False))
            processes.append(process)
            process.start()

    # empty queue and order results
    if not any(type(x) == Human for x in players):
        while True:
            while not queue.empty():
                results.append(queue.get())
            if not any(p.is_alive() for p in processes):
                break

    results.sort(key = lambda x: x[0])
    batch_strings = [r[1] for r in results]

    # calculate overall result and average score
    total_scores = [0 for p in range(player_count)]
    total_points = [0 for p in range(player_count)]
    print(players)
    for result in results:
        sorted_scores = dict(sorted(result[2].items(), key=lambda x: x[0][0]))
        sorted_points = dict(sorted(result[3].items(), key=lambda x: x[0][0]))
        total_scores = [sum(x) for x in zip(total_scores, sorted_scores.values())]
        total_points = [sum(x) for x in zip(total_points, sorted_points.values())]

    print("\n--- Full Stats --------------")
    print(f"Total Points: {total_points}")
    print(f"Total Scores: {total_scores}")

    # write results to file
    with open(log_file + ".txt", "a") as f:
        f.writelines(batch_strings)
        f.write("\n--- Full Stats --------------\n")
        f.write(f"Total Points: {total_points}\n")
        f.write(f"Total Scores: {total_scores}\n")


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