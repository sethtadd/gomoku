import logging
import random

import numpy as np
from ordered_set import OrderedSet

from Board import DRAW, Board
from Player import Player, process


class MonteCarloEngine(Player):
    def __init__(self) -> None:
        pass

    def playout_score(self, board: Board) -> float:
        # escape if game over
        if board.winner is not None:
            if board.winner == DRAW:
                return 0
            return -1

        # recursively choose random move
        moves: OrderedSet[tuple[int, int]] = board.get_open_positions()
        move = random.choice(moves)
        board.push_move(move)
        score = -self.playout_score(board)
        board.pop_move()
        # store score

        return score

    def monte_carlo_value(self, board: Board, rollouts: int):
        scores = [self.playout_score(board) for _ in range(rollouts)]
        return np.mean(scores)

    def best_move(self, board: Board) -> tuple[int, int]:
        moves: OrderedSet[tuple[int, int]] = board.get_open_positions()
        move_scores = {}
        for move in moves:
            board.push_move(move)
            score = -self.monte_carlo_value(board, rollouts=1000)
            move_scores[move] = score
            board.pop_move()
        return max(move_scores, key=move_scores.get)  # type: ignore

    def get_move(self, board: Board) -> tuple[int, int]:
        logging.info("calculating move")
        best_move = self.best_move(board)
        return best_move


if __name__ == "__main__":
    board = Board(dim=3, num_to_win=3)
    board.push_move((0, 0))
    engine = MonteCarloEngine()
    board_eval_recursive = engine.get_move(board)
    print("board_eval_recursive:", board_eval_recursive)
