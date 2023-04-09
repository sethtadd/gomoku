import logging
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from typing import cast

import numpy as np
from ordered_set import OrderedSet

from Board import DRAW, Board
from Player import Player, process


class UctEngine(Player):
    def __init__(self) -> None:
        self.board_visits = {}
        self.board_score_sum = {}
        self.exploration = 1.5

    def record(self, board: Board, score: float):
        self.board_visits["total"] = self.board_visits.get("total", 1) + 1
        self.board_visits[hash(board)] = self.board_visits.get(hash(board), 0) + 1
        self.board_score_sum[hash(board)] = self.board_score_sum.get(hash(board), 0)

    def heuristic_score(self, board):
        N = self.board_visits.get("total", 1)
        ni = self.board_visits.get(hash(board), 1)
        si = self.board_score_sum.get(hash(board), 0)
        C = self.exploration
        Vi = si / ni + C * np.sqrt(np.log(N) / ni)
        return Vi

    def playout_score(self, board: Board) -> float:
        # escape if game over
        if board.winner is not None:
            if board.winner == DRAW:
                score = 0
            else:
                score = -1
            self.record(board, score)
            return score

        move_scores = {}
        for move in board.get_open_positions():
            board.push_move(move)
            score = self.heuristic_score(board)
            move_scores[move] = score
            board.pop_move()

        move = max(move_scores, key=move_scores.get)  # type: ignore
        board.push_move(move)
        score = -self.playout_score(board)
        board.pop_move()
        self.record(board, score)
        return score

    def monte_carlo_value(self, board: Board, rollouts: int) -> float:
        scores = [self.playout_score(board) for _ in range(rollouts)]
        return np.mean(scores)

    # FIXME get this to work
    # def mp_value(self, board: Board, rollouts: int) -> float:
    #     for _ in range(rollouts):
    #         self.playout_score(board)
    #     return self.board_score_sum[hash(board)] / self.board_visits[hash(board)]

    def best_move(self, board: Board) -> tuple[int, int]:
        moves: OrderedSet[tuple[int, int]] = board.get_open_positions()
        move_scores = {}
        for move in moves:
            board.push_move(move)
            # score = -self.mp_value(board, rollouts=100)
            score = -self.monte_carlo_value(board, rollouts=100)
            move_scores[move] = score
            board.pop_move()
        return max(move_scores, key=move_scores.get)  # type: ignore

    def get_move(self, board: Board) -> tuple[int, int]:
        logging.info("calculating move")
        best_move = self.best_move(board)
        return best_move
