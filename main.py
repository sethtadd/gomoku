from time import sleep

from Board import Board
from BoardGUI import BoardGUI
from Engine import Engine
from GameController import GameController
from Player import InputPlayer

board = Board(dim=3, num_to_win=3)
boardGUI = BoardGUI(board, 1000)
player_black = Engine()
player_white = InputPlayer(boardGUI)
game_controller = GameController(board, player_black, player_white)

boardGUI.start_gui()
sleep(0.2)
game_controller.start_game()
