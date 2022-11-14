import logging

from Board import BLACK, WHITE, Board
from Player import Player


class GameController:
    def __init__(
        self, board: Board, player_black: Player, player_white: Player
    ) -> None:
        self.board = board
        self.player_black = player_black
        self.player_white = player_white

    def start_game(self) -> None:
        logging.info("starting game")
        while self.board.winner is None:
            if self.board.turn == BLACK:
                move: tuple[int, int] = self.player_black.get_move(self.board)
            else:  # self.board.turn == WHITE
                move: tuple[int, int] = self.player_white.get_move(self.board)
            self.board.push_move(move)
        else:
            logging.info(
                "game over: "
                + (
                    "black wins"
                    if self.board.winner == BLACK
                    else "white wins"
                    if self.board.winner == WHITE
                    else "draw"
                )
            )
