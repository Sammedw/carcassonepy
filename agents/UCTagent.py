import copy
import random
from agents.baseagent import BaseAgent
from game import Game
from tile import Tile

class Tree:

    def __init__(self, state: Game):
        self.state = state
        self.children: list[Tree] = []

    def add_child(self, child: Tree):
        self.children.append(child)

    def is_leaf(self):
        return not(len(self.children))


class UCTAgent(BaseAgent):
    
    def __init__(self, player_num: int, game: Game):
        super().__init__(player_num, game)

    def tree_policy(root: Tree):
        current_node = root
        # loop while current node is non terminal
        while not root.is_leaf():
            if 


    def uct_search(start_state: Game, iterations: int):
        # create root node
        root = Tree(copy.deepcopy(start_state))
        # simulate while within computational budget
        for i in range(iterations):
            # select node to expand using tree policy
            pass


    def make_move(self, next_tile: Tile):
        valid_actions = super().make_move(next_tile)
        action = random.choice(valid_actions)
        self.game.make_action(action)
        print(action)