from BoardGUI import BoardGUI
from GameController import GameController
from Board import Board
from Player import InputPlayer
from Player import RandomPlayer


board = Board(dim=15)
boardGUI = BoardGUI(board, 500)
player_black = InputPlayer(boardGUI)
player_white = RandomPlayer()
game_controller = GameController(board, player_black, player_white)

boardGUI.start_gui()
game_controller.start_game(delay=0.2)
