import copy
import random
import time
from action import Action
from baseagent import BaseAgent
from game import Game
from tile import Tile
import math


class Node:

    def __init__(self, state: str, actions: list[Action]):
        self.state = state
        self.actions = actions
        self.action_count = len(actions)
        self.regret_sum = [0 for _ in range(self.action_count)]
        self.strategy = [0 for _ in range(self.action_count)]
        self.strategy_sum = [0 for _ in range(self.action_count)]
        self.iteration_marker = 0

    def get_strategy(self, reach_probability: float, iteration: int):
        normalizing_sum = 0
        # set strategy[a] to positive regret or 0
        for a in range(self.action_count):
            if self.regret_sum[a] > 0:
                self.strategy[a] = self.regret_sum[a]
            else:
                self.strategy[a] = 0
            normalizing_sum += self.strategy[a]
        # normalise strategy to actions have probability that adds to one
        for a in range(self.action_count): 
            if normalizing_sum > 0:
                self.strategy[a] /= normalizing_sum
            else:
                #print("pick random")
                self.strategy[a] = 1 / self.action_count
            self.strategy_sum[a] += (iteration - self.iteration_marker) * reach_probability * self.strategy[a]
        # update iteration marker for node
        self.iteration_marker = iteration
        return self.strategy
        
    def get_average_strategy(self) -> list[float]:
        avg_strategy: list[float]
        normalizing_sum = sum(self.strategy_sum)
        if normalizing_sum > 0:
            avg_strategy = [x / normalizing_sum for x in self.strategy_sum]
        else:
            avg_strategy = [1/self.action_count for _ in range(self.action_count)]
        return avg_strategy


class MCCFRAgent(BaseAgent):
    
    def __init__(self, player_num: int, game: Game, time_per_turn: int, epsilon=0.6):
        super().__init__(player_num, game)
        self.node_dict: dict[str, Node] = {}
        self.time_per_turn = time_per_turn
        self.epsilon = epsilon

    @staticmethod
    def build(player_num: int, game: Game):
        print("--- Build MCCFR agent ---")
        while True:
            try:
                time_per_turn = input("Time(s) per action: ")
                time_per_turn = int(time_per_turn)
                epsilon = input("Epsilon: ")
                epsilon = float(epsilon)
                break
            except:
                print("Invalid inputs.")
        return MCCFRAgent(player_num, game, time_per_turn, epsilon=epsilon)

    def return_info(self):
        return f"MCCFR Agent(time={self.time_per_turn}, epsilon={self.epsilon})"

    def cfr_iteration(self, current_state: Game, iteration: int, reach_probabilities: list[float], terminal_reach_probability: float, sample_probability: float, next_tile: Tile = None):
        # check if game in in terminal state
        if current_state.is_game_over():
            # calculate utility for each player by finding difference between own score and max other score
            utilities = [0 for _ in range(self.game.player_count)]
            scores = current_state.compute_scores()
            for p in range(self.game.player_count):
                temp_scores = list(scores)
                own_score = temp_scores.pop(p)
                utilities[p] = own_score - max(temp_scores)
            #print("terminal: ", utility, sample_probability)
            return (utilities, terminal_reach_probability, sample_probability)
        # select next tile at random and calculate probabilty of selecting given tile (unless base node)
        if next_tile:
            tile_probability = 1
        else:
            next_tile = random.choice(current_state.deck.tiles)
            tile_probability = current_state.deck.get_unique_tiles()[next_tile.name] / len(current_state.deck.tiles)
        # get game state node or create it if not explored
        state_str = current_state.get_state_str() + f" NEXT_TILE: {next_tile}"
        node = self.node_dict.get(state_str)
        if node is None:
            while True:
                # if no tiles left then get node utility
                if len(current_state.deck.tiles) == 0:
                    return self.cfr_iteration(current_state, iteration, reach_probabilities, terminal_reach_probability, sample_probability)
                # discard tile if no valid actions
                valid_actions = current_state.get_valid_actions(next_tile)
                if len(valid_actions) == 0:
                    return self.cfr_iteration(current_state, iteration, reach_probabilities, terminal_reach_probability, sample_probability)
                state_str = current_state.get_state_str() + f" NEXT_TILE: {next_tile}"
                node = Node(state_str, valid_actions)
                break
            self.node_dict[state_str] = node 
        # get current strategy for state
        strategy = node.get_strategy(reach_probabilities[self.player_num], iteration)
        # select action using current strategy
        selected_action, action_probability = random.choices(list(zip(node.actions, strategy)), weights=strategy)[0]
        # overwrite action with random action if random is <= epsilon
        if random.random() <= self.epsilon:
            selected_action = random.choice(node.actions)    
        # create game copy and execute selected action
        next_state: Game = copy.deepcopy(current_state)
        next_state.make_action(selected_action)
        # update sample and terminal reach probability
        sample_probability *= tile_probability
        sample_probability = (sample_probability * self.epsilon * (1 / node.action_count)) + (sample_probability * (1-self.epsilon) * action_probability)
        terminal_reach_probability *= tile_probability * action_probability
        # calcuate reach probability for old state before updating
        reach_probability = math.prod(reach_probabilities)
        # update reach probability contribution for current player and chance player
        reach_probabilities[current_state.current_player] *= action_probability
        reach_probabilities[-1] *= tile_probability
        # recursive call
        terminal_utilities, terminal_reach_probability, sample_probability = self.cfr_iteration(next_state, iteration, list(reach_probabilities), terminal_reach_probability, sample_probability)
        # calcuate counterfactual reach probability
        counterfactual_reach_probability = 1
        for i in range(len(reach_probabilities)):
            if i != current_state.current_player:
                counterfactual_reach_probability *= reach_probabilities[i]
        # calculate W value
        W = (terminal_utilities[current_state.current_player] * counterfactual_reach_probability) / sample_probability
        # calculate probability sampled terminal history is reached from current history
        finish_probability = terminal_reach_probability / reach_probability
        # for each action, compute and accumulate sampled counterfactual regret
        for i, action in enumerate(node.actions):
            if action is selected_action:
                node.regret_sum[i] += W * (finish_probability / action_probability - finish_probability)
            else:
                node.regret_sum[i] += (-W) * finish_probability

        return (terminal_utilities, terminal_reach_probability, sample_probability)


    def get_action(self, strategy: list[float], actions: list[Action]):
        return random.choices(actions, weights=strategy)


    def make_move(self, next_tile: Tile):
        valid_actions = super().make_move(next_tile)
        # start time 
        start = time.time()
        i = 0
        # calculate ratio of tiles left to number at start
        progress = self.game.deck.get_tile_count() / self.game.deck.original_deck_size
        print(f"MCCFR MAKE MOVE IN {self.time_per_turn*progress} time")
        # simulate while within computational budget
        while (time.time() - start) < self.time_per_turn*progress:
            #print(i)
            self.cfr_iteration(self.game, i, [1 for _ in range(self.game.player_count + 1)], 1, 1, next_tile)
            i += 1
        #print("regret sum: ", self.node_dict[self.game.get_state_str() + ' NEXT_TILE: ' + next_tile.name].regret_sum)
        #print("-----------------------------------------------------------------------------")
        #print("AVG strategy: ", list(sorted(zip(self.node_dict[self.game.get_state_str() + ' NEXT_TILE: ' + next_tile.name].get_average_strategy(), list(map(str, valid_actions))), key = lambda x: x[0], reverse=True)))
        #print("-----------------------------------------------------------------------------")
        action = list(sorted(zip(self.node_dict[self.game.get_state_str() + ' NEXT_TILE: ' + next_tile.name].get_average_strategy(), valid_actions), key = lambda x: x[0], reverse=True))[0][1]
        self.game.make_action(action)
