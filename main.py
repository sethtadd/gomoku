import logging
from time import sleep

from Board import Board
from BoardGUI import BoardGUI
from Engine import Engine
from GameController import GameController
from Player import InputPlayer, RandomPlayer

# https://stackoverflow.com/a/44401529/1781821
logging.basicConfig(
    filename="log.txt",
    format="%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.DEBUG,
)

board = Board(dim=3, num_to_win=3)
boardGUI = BoardGUI(board, 1000)
player_black = RandomPlayer()
player_white = Engine()
game_controller = GameController(board, player_black, player_white)

boardGUI.start_gui()
sleep(0.2)
game_controller.start_game()
