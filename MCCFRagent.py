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
                #print("pick random")
                self.strategy[a] = 1 / self.action_count
            self.strategy_sum[a] += (iteration - self.iteration_marker) * reach_probability * self.strategy[a]
        # update iteration marker for node
        self.iteration_marker = iteration
        #print("return strategy: ", self.strategy)
        return self.strategy
        
    def get_average_strategy(self) -> list[float]:
        avg_strategy: list[float]
        normalizing_sum = sum(self.strategy_sum)
        #print("s sum: ", self.strategy_sum)
        if normalizing_sum > 0:
            avg_strategy = [x / normalizing_sum for x in self.strategy_sum]
        else:
            avg_strategy = [1/self.action_count for _ in range(self.action_count)]
        return avg_strategy


class MCCFRAgent(BaseAgent):
    
    def __init__(self, player_num: int, game: Game, iterations, epsilon=0.6):
        super().__init__(player_num, game)
        self.node_dict: dict[str, Node] = {}
        self.iterations = iterations
        self.epsilon = epsilon

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
        #print("next tile: ", next_tile)
        strategy = node.get_strategy(reach_probabilities[self.player_num], iteration)
        #print("current strategy: ", strategy)
        #print(random.choices(list(zip(node.actions, strategy)), weights=strategy))
        # select action using current strategy
        selected_action, action_probability = random.choices(list(zip(node.actions, strategy)), weights=strategy)[0]
        # overwrite action with random action if random is <= epsilon
        if random.random() <= self.epsilon:
            #print("select random")
            selected_action = random.choice(node.actions)    
        # create game copy and execute selected action
        next_state: Game = copy.deepcopy(current_state)
        next_state.make_action(selected_action)
        #print("selected action: ", str(selected_action))
        #print("tile prob: ", tile_probability, " | action_prob: ", action_probability)
        # update sample and terminal reach probability
        sample_probability *= tile_probability
        sample_probability = (sample_probability * self.epsilon * (1 / node.action_count)) + (sample_probability * (1-self.epsilon) * action_probability)
        terminal_reach_probability *= tile_probability * action_probability
        #print("new sample prob: ", sample_probability)
        # calcuate reach probability for old state before updating
        reach_probability = math.prod(reach_probabilities)
        # update reach probability contribution for current player and chance player
        #print("old reach probs: ", reach_probabilities)
        reach_probabilities[current_state.current_player] *= action_probability
        reach_probabilities[-1] *= tile_probability
        #print("new reach probs: ", reach_probabilities)
        # recursive call
        terminal_utilities, terminal_reach_probability, sample_probability = self.cfr_iteration(next_state, iteration, list(reach_probabilities), terminal_reach_probability, sample_probability)
        # for each action, compute and accumulate sampled counterfactual regret
        counterfactual_reach_probability = 1
        for i in range(len(reach_probabilities)):
            if i != current_state.current_player:
                counterfactual_reach_probability *= reach_probabilities[i]
        #print("player: ", current_state.current_player)
        #print("reach: ", reach_probabilities)
        #print("counter reach prob: ", counterfactual_reach_probability)
        #print("sample probability: ", sample_probability)
        #print("old regret sum: ", node.regret_sum)
        #print("terminal utilities: ", terminal_utilities)
        #print("current player: ", current_state.current_player)
        W = (terminal_utilities[current_state.current_player] * counterfactual_reach_probability) / sample_probability
        #print("W value: ", W)
        finish_probability = terminal_reach_probability / reach_probability
        for i, action in enumerate(node.actions):
            if action is selected_action:
                node.regret_sum[i] += W * (finish_probability / action_probability - finish_probability)
            else:
                node.regret_sum[i] += (-W) * finish_probability
        #print("new regret sum: ", node.regret_sum)
        return (terminal_utilities, terminal_reach_probability, sample_probability)


    def get_action(self, strategy: list[float], actions: list[Action]):
        return random.choices(actions, weights=strategy)


    def make_move(self, next_tile: Tile):
        valid_actions = super().make_move(next_tile)
        #print(list(map(str, valid_actions)))
        for i in range(self.iterations):
            #print(i)
            self.cfr_iteration(self.game, i, [1 for _ in range(self.game.player_count + 1)], 1, 1, next_tile)
        #print("regret sum: ", self.node_dict[self.game.get_state_str() + ' NEXT_TILE: ' + next_tile.name].regret_sum)
        #print("-----------------------------------------------------------------------------")
        print("AVG strategy: ", list(sorted(zip(self.node_dict[self.game.get_state_str() + ' NEXT_TILE: ' + next_tile.name].get_average_strategy(), list(map(str, valid_actions))), key = lambda x: x[0], reverse=True)))
        print("-----------------------------------------------------------------------------")
        action = list(sorted(zip(self.node_dict[self.game.get_state_str() + ' NEXT_TILE: ' + next_tile.name].get_average_strategy(), valid_actions), key = lambda x: x[0], reverse=True))[0][1]
        print()
        print(action)
        self.game.make_action(action)
