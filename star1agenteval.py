from copy import deepcopy
import time
from action import Action
from baseagent import BaseAgent
from game import Game
from tile import Tile
from math import inf



class Star1AgentEval(BaseAgent):
    
    def __init__(self, player_num: int, game: Game, time_per_turn: int):
        super().__init__(player_num, game)
        self.upper = 350
        self.lower = -350
        self.time_per_turn = time_per_turn

    @staticmethod
    def build(player_num: int, game: Game):
        print("--- Build STAR1 EVAL agent ---")
        while True:
            try:
                time_per_turn = input("Time(s) per action: ")
                time_per_turn = int(time_per_turn)
                break
            except:
                print("Invalid inputs.")
        return Star1AgentEval(player_num, game, time_per_turn)

    def return_info(self):
        return f"STAR1 EVAL Agent(time={self.time_per_turn})"

    def eval_state(self, state: Game):
        # return difference between own virtual score and other highest virtual score
        scores = state.compute_scores()
        own_score = scores.pop(self.player_num)
        best_opponent_score = max(scores)
        meeples_left = len(state.free_meeples[self.player_num])
        eval = own_score - best_opponent_score
        if meeples_left > 0:
            progress = self.game.deck.get_tile_count() / self.game.deck.original_deck_size
            eval += 6 * progress
        return eval

    # calculate the score for a min or max node
    def minimax(self, state: Game, next_tile: Tile, alpha: int, beta: int, depth: int, best_actions: dict[str, Action], start_time: float):
        # get valid actions in current state
        valid_actions = state.get_valid_actions(next_tile)
        # attempt to get best action from previous iteration
        # state_str = state.get_state_str() + f" NEXT_TILE: {next_tile}"
        # if state_str in best_actions:
        #     best_action = best_actions[state_str]
        #     # put previous best action at front if it exists
        #     valid_actions.remove(best_action)
        #     valid_actions.insert(0, best_action)
        # else:
        best_action = None

        # min or max mode
        if state.current_player == self.player_num:
            # player is max
            max_val = - inf
            # iterate over possible actions
            #print(f"max node - actions: {list(map(str, state.get_valid_actions(next_tile)))}")    
            for action in valid_actions:
                #print(action)
                # create new game state with action applied
                new_state = deepcopy(state)
                new_state.make_action(action)
                # calculate value of subsequent chance node by calling star method
                val = self.star1(new_state, alpha, beta, depth - 1, best_actions, start_time)
                if val > max_val:
                    max_val = val
                    best_action = action
                #print(f"{str(action)} - new max: {max_val}")
                # prune if val is equal or exceeds beta value
                if max_val >= beta:
                    #print("Prune max - beta: ", beta)
                    break
                # update alpha value
                alpha = max(alpha, max_val)
            # check if max_val still inf
            if max_val == -inf:
                # no actions were available so get next random tile
                max_val = self.star1(state, alpha, beta, depth, best_actions, start_time)
            # save best action
           # best_actions[state_str] = best_action
            # return value of max node
            return max_val, best_action
        else:
            # player is min
            min_val = inf
            # iterate over possible actions
            #print("min node")
            for action in valid_actions:
                # create new game state with action applied
                new_state = deepcopy(state)
                new_state.make_action(action)
                # calculate value of subsequent chance node by calling star method
                val = self.star1(new_state, alpha, beta, depth - 1, best_actions, start_time)
                if val < min_val:
                    min_val = val
                    best_action = action
                #print(f"{str(action)} - new min: {min_val}")
                # prune if val is equal to or less than alpha value
                if min_val <= alpha:
                    break
                # update beta value
                beta = min(beta, min_val)
            if min_val == inf:
                # no actions were available so get next random tile
                min_val = self.star1(state, alpha, beta, depth, best_actions, start_time)
            # save best action
            #best_actions[state_str] = best_action
            # return value of min node
            return min_val, best_action

    # calculate the score for a chance node
    def star1(self, state: Game, alpha: int, beta: int, depth: int, best_actions: dict[str, Action], start_time: float):
        # check if game finished or depth reached or time reached
        if (state.is_game_over() or depth == 0 or time.time() - start_time > self.time_per_turn):
            if time.time() - start_time > self.time_per_turn:
                print("STAR out of time")
            # evaluate the position
            return self.eval_state(state)
        # initialise vars
        cur_x = 0 # stores cumulative value of explored nodes
        cur_y = 1 # stores the probabilty that the next tile is not explored
        # iterate over possible tiles
        #print("chance node")
        for tile, tile_count in state.deck.get_unique_tiles().items():
            if tile_count == 0:
                continue
            # calculate probability of picking tile
            prob = tile_count / len(state.deck.tiles)
            cur_y -= prob
            # calculate new alpha and beta values
            cur_alpha = (alpha - cur_x - self.upper * cur_y) / prob
            cur_beta = (beta - cur_x - self.lower * cur_y) / prob
            ax = max(self.lower, cur_alpha)
            bx = min(self.upper, cur_beta)
            # calculate value of node after selecting tile using minimax
            val, _ = self.minimax(state, state.deck.get_tile_by_name(tile), ax, bx, depth, best_actions, start_time)
            # prune if val is greater than beta or smaller than alpha
            if (val >= cur_beta):
                return beta
            if (val <= cur_alpha):
                return alpha
            cur_x += prob * val
            #print(f"curr x: {cur_x}")
        # return final value
        return cur_x


    def make_move(self, next_tile: Tile):
        best_actions = {}
        start_time = time.time()
        depth = 1
        while True:
            if time.time() - start_time > self.time_per_turn:
                break
            print(f"EXPECTIMAX entering depth {depth}")
            _, action = self.minimax(self.game, next_tile, - inf, inf, depth, best_actions, start_time)
            depth += 1
        print(f"STAR move: {action}")
            
        self.game.make_action(action)