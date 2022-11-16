import copy
import random
from typing import Optional
from action import Action
from agents.baseagent import BaseAgent
from game import Game
from tile import Tile

class ChanceNode(Tree):
    
    def __init__(self):
        super().__init__(self)

class Tree:

    def __init__(self, state: Game, next_tile: Tile, incoming_action: Optional[Action]):
        # current game state object
        self.state = state
        self.next_tile = next_tile
        # action taken to reach the current state
        self.incoming_action = incoming_action
        # list of explored children
        self.children: list[Tree] = []
        # visit and total sums used to calculate UCT
        self.visit_rate = 0
        self.total_reward = 0
        # list of actions from given state that have not been explored
        self.expandable_actions: list[Action] = self.state.get_valid_actions(next_tile)

    def add_child(self, child: Tree):
        self.children.append(child)

    def is_leaf(self):
        return not(len(self.children))

    def has_expandable_actions(self):
        return len(self.expandable_actions) > 0




class UCTAgent(BaseAgent):
    
    def __init__(self, player_num: int, game: Game):
        super().__init__(player_num, game)

    def expand(self, root: Tree):
        # choose untried action from current state
        untried_action = random.choice(root.expandable_actions)
        # create new game state after applying action
        new_state = copy.deepcopy(root.state)
        new_state.make_action(untried_action)
        new_child = Tree()

    def tree_policy(self, root: Tree):
        current_node = root
        # loop while current node is non terminal
        while not root.is_leaf():
            # check if node is not fully expanded
            if root.has_expandable_actions():
                return self.expand(root)


    def uct_search(self, start_state: Game, incoming_action: Action, next_tile: Tile, iterations: int):
        # create root node
        root = Tree(copy.deepcopy(start_state), incoming_action, next_tile)
        # simulate while within computational budget
        for i in range(iterations):
            # select node to expand using tree policy
            pass


    def make_move(self, next_tile: Tile):
        valid_actions = super().make_move(next_tile)
        action = random.choice(valid_actions)
        self.game.make_action(action)
        print(action)