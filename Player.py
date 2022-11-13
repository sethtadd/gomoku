import random
import numpy as np

from abc import abstractmethod
from typing import Optional

from Gomoku import Board
from BoardGUI import BoardGUI


class Player():
    def __init__(self, engine: bool = False, boardGUI: Optional[BoardGUI] = None) -> None:
        self.boardGUI = boardGUI

    @abstractmethod
    def get_move(self, board: Board) -> tuple[int, int]:
        pass


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def get_move(self, board: Board) -> tuple[int, int]:
        open_positions = board.get_open_positions()
        # choose random open position
        move = random.choice(list(open_positions))
        return move


class InputPlayer(Player):
    def __init__(self, boardGUI: BoardGUI) -> None:
        super().__init__()
        self.boardGUI = boardGUI

    def get_move(self, board: Board) -> tuple[int, int]:
        self.boardGUI.click_pos = None

        # loop until user clicks a position
        while True:
            if self.boardGUI.click_pos is not None:
                break

        # calculate position indices nearest to click
        pos = np.array(self.boardGUI.click_pos)
        pos = pos / self.boardGUI.line_spacing
        pos = np.round(pos)
        pos = pos - 1
        pos = pos.astype(dtype=int)
        pos = tuple(pos)

        if pos not in board.get_open_positions():
            print("can't move there!")
            return self.get_move(board)
        else:
            return pos
