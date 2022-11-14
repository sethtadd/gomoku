import random
from abc import abstractmethod
from time import sleep

import numpy as np

from Board import Board
from BoardGUI import BoardGUI


class Player:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_move(self, board: Board) -> tuple[int, int]:
        pass


class RandomPlayer(Player):
    def __init__(self, delay=None) -> None:
        super().__init__()
        self.delay = delay

    def get_move(self, board: Board) -> tuple[int, int]:
        if self.delay is not None:
            sleep(self.delay)
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
