import logging
from collections import defaultdict
from functools import partial

import numpy as np
from ordered_set import OrderedSet

BLACK = 0
WHITE = 1
DRAW = -1


class Board:
    def __init__(self, dim: int = 8, num_to_win: int = 5):
        logging.info("initializing Board")
        self.dim = dim
        self.num_to_win = num_to_win
        self.pieces = np.zeros(
            (2, dim, dim)
        )  # the first dim represents the piece color, black is 0
        self.turn = BLACK
        self.winner = None
        self.move_history = []

    def deepcopy(self):
        board_copy = Board()
        board_copy.dim = self.dim
        board_copy.num_to_win = self.num_to_win
        board_copy.pieces = self.pieces.copy()
        board_copy.turn = self.turn
        board_copy.winner = self.winner
        board_copy.move_history = self.move_history.copy()
        return board_copy

    def push_move(self, move: tuple[int, int]) -> bool:
        # check for game over
        if self.winner is not None:
            return False

        # check for move position already occupied
        if (
            self.pieces[BLACK][move[0]][move[1]] != 0
            or self.pieces[WHITE][move[0]][move[1]] != 0
        ):
            return False

        self.move_history.append(move)
        self.pieces[self.turn][move[0]][move[1]] = 1
        self.check_game_over()
        self.turn ^= 1
        return True

    def pop_move(self) -> tuple[int, int]:
        move = self.move_history.pop()
        self.turn ^= 1
        self.winner = None
        self.pieces[self.turn][move[0]][move[1]] = 0
        return move

    def check_game_over(self) -> bool:
        # check if winner or draw (all positions filled)
        if self.check_matrix_for_contiguous():
            self.winner = self.turn
            return True
        elif len(self.get_open_positions()) == 0:
            self.winner = DRAW
            return True
        else:
            return False

    def get_closed_positions(
        self,
    ) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        black_positions = np.transpose(np.array(np.nonzero(self.pieces[BLACK])))
        white_positions = np.transpose(np.array(np.nonzero(self.pieces[WHITE])))
        black_positions = [tuple(coord) for coord in black_positions]
        white_positions = [tuple(coord) for coord in white_positions]
        return (black_positions, white_positions)

    def get_open_positions(self) -> OrderedSet[tuple[int, int]]:
        all_positions = OrderedSet(
            [
                (i, j)
                for i in range(self.pieces.shape[1])
                for j in range(self.pieces.shape[2])
            ]
        )
        # remove all occupied positions
        black_positions, white_positions = self.get_closed_positions()
        closed_positions = OrderedSet(black_positions + white_positions)
        open_positions: OrderedSet = OrderedSet(all_positions - closed_positions)
        return open_positions

    def check_matrix_for_contiguous(self) -> bool:
        cross_sections = set()
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
        # cross-sections shorter than self.num_to_win can't be winning
        winning_cross_sections = set(
            filter(lambda arr: len(arr) >= self.num_to_win, cross_sections)
        )
        winning_cross_sections = set(
            filter(
                partial(self.check_array_for_contiguous, self.num_to_win),
                cross_sections,
            )
        )
        return len(winning_cross_sections) != 0

    def __hash__(self) -> int:
        return hash(tuple(self.pieces.flatten()))

    # write docs explaining that move order does not affect Board uniqueness, just the piece positions
    def __eq__(self, other) -> bool:
        if type(other) is type(self):
            return tuple(self.pieces.flatten()) == tuple(other.pieces.flatten())
        return False

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
    def groups(data: np.ndarray, func) -> list:
        grouping = defaultdict(list)
        for y in range(len(data)):
            for x in range(len(data[y])):
                grouping[func(x, y)].append(data[y][x])
        return list(map(grouping.get, sorted(grouping)))
