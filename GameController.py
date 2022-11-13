from time import sleep
from Gomoku import Board, BLACK
from Player import Player


class GameController:
    def __init__(self, board: Board, player_black: Player, player_white: Player) -> None:
        self.board = board
        self.player_black = player_black
        self.player_white = player_white

    def start_game(self, delay: float) -> None:
        while self.board.game_over_str == '':
            if delay is not None:
                sleep(delay)
            if self.board.turn == BLACK:
                move: tuple[int, int] = self.player_black.get_move(self.board)
            else:  # self.board.turn == WHITE
                move: tuple[int, int] = self.player_white.get_move(self.board)
            self.board.push_move(move)
        else:
            print(self.board.game_over_str)
