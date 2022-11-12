from collections import defaultdict
from functools import partial

import numpy as np

BLACK = 0
WHITE = 1


class Board:
    def __init__(self, dims: tuple[int, int] = (8, 8)):
        self.dims = dims
        self.pieces = np.zeros((2, dims[0], dims[1]))  # the first dim represents the piece color, black is 0
        self.turn = BLACK
        self.game_over_str = ''

    def push_move(self, coord: tuple[int, int]) -> bool:
        # check for game over
        if self.game_over_str != '':
            return False

        # check for coord already occupied
        if self.pieces[BLACK][coord[0]][coord[1]] != 0 or self.pieces[WHITE][coord[0]][coord[1]] != 0:
            return False

        self.pieces[self.turn][coord[0]][coord[1]] = 1
        self.check_game_over()
        self.turn ^= 1
        return True

    def check_game_over(self) -> None:
        # check if winner or draw (all positions filled)
        if self.check_matrix_for_contiguous():
            self.game_over_str = f'GAME OVER: {"black" if self.turn == 0 else "white"} wins!'
        elif 0 not in self.pieces:
            self.game_over_str = 'GAME OVER: draw'

    def check_matrix_for_contiguous(self, num: int = 5) -> bool:
        cross_sections: set[tuple] = set()
        cols = self.groups(self.pieces[self.turn], lambda x, y: x)
        rows = self.groups(self.pieces[self.turn], lambda x, y: y)
        fdiag = self.groups(self.pieces[self.turn], lambda x, y: x + y)
        bdiag = self.groups(self.pieces[self.turn], lambda x, y: x - y)
        cols = [tuple(arr) for arr in cols]
        rows = [tuple(arr) for arr in rows]
        fdiag = [tuple(arr) for arr in fdiag]
        bdiag = [tuple(arr) for arr in bdiag]
        cross_sections.update(cols)
        cross_sections.update(rows)
        cross_sections.update(fdiag)
        cross_sections.update(bdiag)
        winning_cross_sections = set(filter(lambda arr: len(arr) >= num, cross_sections))  # cross-sections shorter than num can't be winning
        winning_cross_sections = set(filter(partial(self.check_array_for_contiguous, num), cross_sections))
        return len(winning_cross_sections) != 0

    @staticmethod
    def check_array_for_contiguous(num: int, array: np.ndarray) -> bool:
        num_contiguous = 0
        for x in array:
            if x == 1:
                num_contiguous += 1
            else:
                num_contiguous = 0
            if num_contiguous == num:
                return True
        return False

    # https://stackoverflow.com/a/43311126/1781821
    @staticmethod
    def groups(data: np.ndarray, func) -> list[np.ndarray]:
        grouping = defaultdict(list)
        for y in range(len(data)):
            for x in range(len(data[y])):
                grouping[func(x, y)].append(data[y][x])
        return list(map(grouping.get, sorted(grouping)))
