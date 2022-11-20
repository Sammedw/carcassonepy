
from itertools import cycle
from action import Action
from enums import FeatureType

from game import Game
from location import Coordinates


game = Game(2)

game.make_action(Action(game.deck.get_tile_by_name("monastery"), 0, Coordinates(-1, 0)))
game.print_game_state()
game.make_action(Action(game.deck.get_tile_by_name("city_cap_straight_road"), 2, Coordinates(0, 1), FeatureType.CITY, 0))
game.print_game_state()
game.make_action(Action(game.deck.get_tile_by_name("monastery"), 0, Coordinates(-2, 0), FeatureType.FARM, 0))
game.print_game_state()
game.make_action(Action(game.deck.get_tile_by_name("city_cap_straight_road"), 2, Coordinates(1, 0)))
game.print_game_state()
game.make_action(Action(game.deck.get_tile_by_name("monastery_road"), 2, Coordinates(0, -1)))
game.print_game_state()
game.make_action(Action(game.deck.get_tile_by_name("monastery_road"), 2, Coordinates(1, -1)))
game.print_game_state()
game.make_action(Action(game.deck.get_tile_by_name("city_cap_straight_road"), 0, Coordinates(0, 2)))
game.print_game_state()

print(game.get_state_str())