import copy
import random
import math
from typing import Optional
from action import Action
from baseagent import BaseAgent
from enums import FeatureType
from feature import Farm
from game import Game
from tile import Tile

class ChanceNode: pass

class ChoiceNode:

    def __init__(self, state: Game, next_tile: Tile, incoming_action: Optional[Action], parent: ChanceNode):
        # current game state object
        self.state = state
        self.next_tile = next_tile
        # action taken to reach the current state
        self.incoming_action = incoming_action
        self.parent = parent
        # list of explored children
        self.children: list[ChanceNode] = []
        # visit and total sums used to calculate UCT
        self.visit_count = 0
        self.total_reward = 0
        # list of actions from given state that have not been explored
        if next_tile is not None:
            self.expandable_actions = self.state.get_valid_actions(next_tile)
        else:
            self.expandable_actions = []

    def add_child(self, child: ChanceNode):
        self.children.append(child)

    def has_expandable_actions(self):
        return len(self.expandable_actions) > 0
    
    def print_node(self, tab: int = 0):
        print('\t'*tab + f"Choice: ")
        for child in self.children:
            child.print_node(tab+1)
    

class ChanceNode:
    
    def __init__(self, state: Game, incoming_action: Optional[Action], parent: ChoiceNode | ChanceNode):
        # current game state object
        self.state = state
        # action taken to reach the current state
        self.incoming_action = incoming_action
        self.parent = parent
        # dict of explored children
        self.children: dict[Tile, ChoiceNode | ChanceNode] = {}
        # visit and total sums used to calculate UCT
        self.visit_count = 0
        self.total_reward = 0

    def is_terminal(self):
        # node is terminal of no tiles left
        return self.state.is_game_over()

    def select_random_child(self):
        # select random tile from deck if one exists
        if len(self.state.deck.tiles) > 0:
            tile = random.choice(self.state.deck.tiles)
            # check if node has already been explored
            if tile in self.children:
                return self.children[tile]
            else:
                # if not, create new choice node
                # check if there are any valid moves given random tile
                if (len(self.state.get_valid_actions(tile)) > 0):
                    new_child = ChoiceNode(self.state, tile, self.incoming_action, self)
                    self.children[tile] = new_child
                    return new_child
                else:
                    # no valid actions, so create chance node to select new tile
                    new_state = copy.deepcopy(self.state)
                    # add tile back into current state since it was removed
                    self.state.deck.tiles.append(tile)
                    new_child = ChanceNode(new_state, self.incoming_action, self)
                    self.children[tile] = new_child
                    return new_child


    def print_node(self, tab: int = 0):
        print('\t'*tab + f"Chance({UCT(self, self.parent.visit_count, 3)}): ")
        for child in self.children.values():
            child.print_node(tab+1)


def UCT(node: ChoiceNode, parent_visit_count: int,  exploration_constant: float, max=True):
    if node.visit_count == 0:
        return "infinity"
    value = (node.total_reward / node.visit_count)
    exploration = exploration_constant * math.sqrt((2*math.log(parent_visit_count))/node.visit_count)
    if max:
        return value + exploration
    else:
        return value - exploration


class UCTAgent(BaseAgent):
    
    def __init__(self, player_num: int, game: Game):
        super().__init__(player_num, game)
        self.exploration_constant = 3

    def expand(self, root: ChoiceNode) -> ChanceNode:
        # choose untried action from current state and remove from expandable actions
        untried_action = random.choice(root.expandable_actions)
        root.expandable_actions.remove(untried_action)
        # create new game state after applying action
        new_state = copy.deepcopy(root.state)
        new_state.make_action(untried_action)
        new_child = ChanceNode(new_state, untried_action, root)
        root.add_child(new_child)
        return new_child

    def best_child(self, node: ChoiceNode, exploration_constant: float, max=True):
        children = node.children
        argmax = children[0]
        valmax = UCT(children[0], node.visit_count, exploration_constant, max)
        for child in children:
            uct_val = UCT(child, node.visit_count, exploration_constant, max)
            if (max and uct_val > valmax) or (not max and uct_val < valmax):
                argmax = child
                valmax = uct_val
        return argmax

    def tree_policy(self, current_node: ChoiceNode | ChanceNode):
        # check if node is choice or chance
        if type(current_node) == ChoiceNode:
            # check if node not fully expanded
            if current_node.has_expandable_actions():
                # expand node
                return self.expand(current_node)
            else:
                # find best child of node, max value if agent is current player otherwise minimise
                #print(f"NEXT TILE: {current_node.next_tile}")
                #print(f"EXPANDABLE ACTIONS: {current_node.expandable_actions}")
                #print(f"CHILDREN: {current_node.children}")
                is_current_player = current_node.state.current_player == self.player_num
                return self.tree_policy(self.best_child(current_node, self.exploration_constant, is_current_player))
        else:
            # check if chance node is terminal
            if not current_node.is_terminal():
                # Select child at random for chance node
                return self.tree_policy(current_node.select_random_child())
            else:
                return current_node
    
    def default_policy(self, state: Game): 
        # play random moves until end of game
        while not state.is_game_over():
            valid_actions = state.get_valid_actions(random.choice(state.deck.tiles))
            if len(valid_actions) > 0:
                state.make_action(random.choice(valid_actions))
        # return difference between own score and other highest score
        scores = state.compute_final_score()
        own_score = scores.pop(self.player_num)
        best_opponent_score = max(scores)
        return own_score - best_opponent_score

    def backup(self, current_node: ChanceNode, payoff: float):
        # update reward and vist count for nodes on exploration path
        while(current_node):
            current_node.visit_count += 1
            current_node.total_reward += payoff
            current_node = current_node.parent
             
    def uct_search(self, start_state: Game, next_tile: Tile, iterations: int):
        # create root node
        root = ChoiceNode(start_state, next_tile, None, None)
        # simulate while within computational budget
        for _ in range(iterations):
            # select node to expand using tree policy
            node = self.tree_policy(root)
            #node.print_node()
            # simulate game from selected node
            simulate = copy.deepcopy(node.state)
            payoff = self.default_policy(simulate)
            # backup reward
            self.backup(node, payoff)
            #print("-----------------------------------------------------------------")
            #root.print_node()          
        # return best child after simulations (c=0 so one with best average reward)
        #root.print_node()
        return self.best_child(root, 0).incoming_action


    def make_move(self, next_tile: Tile):
        action = self.uct_search(self.game, next_tile, 500)
        self.game.make_action(action)