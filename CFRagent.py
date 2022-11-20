import copy
import random
from action import Action
from baseagent import BaseAgent
from game import Game
from tile import Tile



class Node:

    def __init__(self, state: str, action_count: int):
        self.state = state
        self.action_count = action_count
        self.regret_sum = [0 for _ in range(action_count)]
        self.strategy = [0 for _ in range(action_count)]
        self.strategy_sum = [0 for _ in range(action_count)]

    def get_strategy(self, reach_probability: float) -> list[float]:
        normalizing_sum = 0
        # set strategy[a] to positive regret or 0
        for a in range(self.action_count):
            if self.regret_sum[a] > 0:
                self.strategy[a] = self.regret_sum[a]
                normalizing_sum += self.strategy[a]
        # normalise strategy to actions have probability that adds to one
        for a in range(self.action_count): 
            if normalizing_sum > 0:
                self.strategy[a] /= normalizing_sum
            else:
                self.strategy[a] = 1 / self.action_count
            self.strategy_sum[a] += reach_probability * self.strategy[a]
        return self.strategy
        
    def get_average_strategy(self) -> list[float]:
        avg_strategy: list[float]
        normalizing_sum = sum(self.strategy_sum)
        if normalizing_sum > 0:
            avg_strategy = [x / normalizing_sum for x in self.strategy_sum]
        else:
            avg_strategy = [1/self.action_count for _ in self.action_count]
        return avg_strategy


class CFRAgent(BaseAgent):
    
    def __init__(self, player_num: int, game: Game):
        super().__init__(player_num, game)
        self.node_dict: dict[str, Node] = {}

    def cfr(self, current_state: Game, p0: float, p1: float):
        # check if game in in terminal state
        if current_state.is_game_over():
            # return node utility
            final_scores = current_state.compute_final_score()
            if current_state.current_player == 0:
                return final_scores[0] - final_scores[1]
            else:
                return final_scores[1] - final_scores[0]
        # get node or create one if doesn't exist
        state_str = current_state.get_state_str() + f" NEXT_TILE: {current_state.deck.peak_next_tile()}"
        node = self.node_dict.get(state_str)
        if node is None:
            while True:
                # discard tile if no valid actions
                if len(current_state.get_valid_actions(current_state.deck.peak_next_tile())) == 0:
                    continue
                state_str = current_state.get_state_str() + f" NEXT_TILE: {current_state.deck.peak_next_tile()}"
                node = Node(state_str)
                break
            self.node_dict[state_str] = node
        # for each action, recursively call cfr
        if current_state.current_player == 0:
            p = p0
        else:
            p = p1
        strategy = node.get_strategy(p)
        util = []
        node_util = 0
        print(f"CURRENT STATE: {current_state.get_state_str()}")
        for i, action in enumerate(valid_actions):
            print(action)
            next_state: Game = copy.deepcopy(current_state)
            next_state.make_action(action)
            print(f"NEXT STATE: {next_state.get_state_str()}")
            if current_state.current_player == 0:
                util.append(- self.cfr(next_state, p0 * strategy[i], p1))
            else:
                util.append(- self.cfr(next_state, p0, p1 * strategy[i]))
            node_util += strategy[i] * util[i]
        # for each action, compute and accumulate counterfactual regret
        for i in range(len(valid_actions)):
            regret = util[i] - node_util
            print(regret)
            node.regret_sum[i] += p * regret
        return node_util

    def train(self, game_state: Game, iterations: int):
        random_state = copy.deepcopy(game_state)
        util = 0
        for _ in range(iterations):
            random.shuffle(random_state.deck.tiles)
            util += self.cfr(random_state, 1, 1)
        print(f"Average game value: {util / iterations}")
        for state_str, node in self.node_dict.items():
            print(f"State: {state_str} | Average Strategy: {node.get_average_strategy()}")

    def make_move(self, next_tile: Tile):
        valid_actions = super().make_move(next_tile)
        self.train(self.game, 1000)
        action = random.choice(valid_actions)
        self.game.make_action(action)