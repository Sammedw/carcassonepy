import copy
import random
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
        #print("get strategy")
        #print("current strategy: ", self.strategy)
        #print("strategy sum: ", self.strategy_sum)
        normalizing_sum = 0
        # set strategy[a] to positive regret or 0
        for a in range(self.action_count):
            if self.regret_sum[a] > 0:
                self.strategy[a] = self.regret_sum[a]
            else:
                self.strategy[a] = 0
            normalizing_sum += self.strategy[a]
            #print("add ",  self.strategy[a], " to normal sum")
        # normalise strategy to actions have probability that adds to one
        #print("regret matched strategy pre-normalizarion: ", self.strategy)
        #print("normal: ", normalizing_sum)
        for a in range(self.action_count): 
            if normalizing_sum > 0:
                self.strategy[a] /= normalizing_sum
            else:
                self.strategy[a] = 1 / self.action_count
            self.strategy_sum[a] += (iteration - self.iteration_marker) * reach_probability * self.strategy[a]
            # update iteration marker for node
            self.iteration_marker = iteration
        #print("return strategy: ", self.strategy)
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
    
    def __init__(self, player_num: int, game: Game, epsilon=0.6):
        super().__init__(player_num, game)
        self.node_dict: dict[str, Node] = {}
        self.epsilon = epsilon

    def cfr_iteration(self, current_state: Game, iteration: int, reach_probabilities: list[float], sample_probability: float, next_tile: Tile = None):
        # check if game in in terminal state
        if current_state.is_game_over():
            # return difference between own score and other highest score
            scores = current_state.compute_scores()
            own_score = scores.pop(self.player_num)
            utility = own_score - max(scores)
            #print("terminal: ", utility, sample_probability)
            return (utility, sample_probability)
        # select next tile at random and calculate probabilty of selecting given tile (unless base node)
        #print(list(map(str, (current_state.deck.tiles))))
        if next_tile:
            #next_tile = current_state.deck.get_tile_by_name(next_tile)
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
                    return self.cfr_iteration(current_state, iteration, reach_probabilities, sample_probability)
                # discard tile if no valid actions
                valid_actions = current_state.get_valid_actions(next_tile)
                if len(valid_actions) == 0:
                    return self.cfr_iteration(current_state, iteration, reach_probabilities, sample_probability)
                state_str = current_state.get_state_str() + f" NEXT_TILE: {next_tile}"
                node = Node(state_str, valid_actions)
                break
            self.node_dict[state_str] = node 
        # get current strategy for state
        strategy = node.get_strategy(reach_probabilities[self.player_num], iteration)
        #print("current strategy: ", strategy)
        # pick action at random if random is <= epsilon
        if random.random() <= self.epsilon:
            selected_action = random.choice(node.actions)
            action_probability = 1 / node.action_count
        # otherwise select action based on current strategy
        else:
            #print(random.choices(list(zip(node.actions, strategy)), weights=strategy))
            selected_action, action_probability = random.choices(list(zip(node.actions, strategy)), weights=strategy)[0]
        # create game copy and execute selected action
        next_state: Game = copy.deepcopy(current_state)
        next_state.make_action(selected_action)
        #print(tile_probability, action_probability)
        # update sample probability
        sample_probability *= tile_probability * action_probability 
        # calcuate reach probability for old state before updating
        reach_probability = math.prod(reach_probabilities)
        # update reach probability contribution for current player and chance player
        reach_probabilities[current_state.current_player] *= action_probability
        reach_probabilities[-1] *= tile_probability
        # recursive call
        terminal_utility, terminal_probability = self.cfr_iteration(next_state, iteration, reach_probabilities, sample_probability)
        # for each action, compute and accumulate sampled counterfactual regret
        counterfactual_reach_probability = 1
        for i in range(len(reach_probabilities)):
            if i != current_state.current_player:
                counterfactual_reach_probability *= reach_probabilities[i]

        W = (terminal_utility * counterfactual_reach_probability) / terminal_probability
        finish_probability = terminal_probability / reach_probability
        for i, action in enumerate(node.actions):
            if action is selected_action:
                node.regret_sum[i] += W * (finish_probability / action_probability - finish_probability)
            else:
                node.regret_sum[i] += (-W) * finish_probability
        #print("new regret sum: ", node.regret_sum)
        return (terminal_utility, terminal_probability)


    def get_action(self, strategy: list[float], actions: list[Action]):
        return random.choices(actions, weights=strategy)


    def make_move(self, next_tile: Tile):
        valid_actions = super().make_move(next_tile)
        for i in range(500):
            #print(i)
            self.cfr_iteration(self.game, i, [1 for _ in range(self.game.player_count + 1)], 1, next_tile)
        print(list(map(str, valid_actions)),  self.node_dict[self.game.get_state_str() + ' NEXT_TILE: ' + next_tile.name].get_average_strategy())
        action = self.get_action(self.node_dict[self.game.get_state_str() + ' NEXT_TILE: ' + next_tile.name].get_average_strategy(), valid_actions)[0]
        print(action)
        self.game.make_action(action)
