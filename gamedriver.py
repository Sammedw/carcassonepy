from agents.baseagent import BaseAgent
from game import Game
from tile import TileSet
from itertools import cycle


class GameDriver:

    def __init__(self, players: list[BaseAgent], additional_tile_sets: list[TileSet] = []):
        self.players = players
        # create new game
        self.game = Game(len(players), additional_tile_sets)
    

    