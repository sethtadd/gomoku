import logging

from ordered_set import OrderedSet

from Board import DRAW, Board
from Player import Player


class Engine(Player):
    def __init__(self) -> None:
        self.evaluated_boards = {}

    def evaluate_board_recursive(self, board: Board) -> tuple[tuple[int, int], float]:
        if board in self.evaluated_boards:
            return self.evaluated_boards[board]
        # check for game over
        if board.winner is not None:
            if board.winner == DRAW:
                return (-1, -1), 0
            else:  # if you're handed a board with game over, you've lost
                return (-1, -1), -1
        # else do recursive evaluation
        moves: OrderedSet[tuple[int, int]] = board.get_open_positions()
        move_evals_dict: dict[tuple[int, int], float] = {}
        for move in moves:
            if not board.push_move(move):
                logging.error("COULD NOT PUSH MOVE")
            _, evaluation = self.evaluate_board_recursive(board)
            move_evals_dict[move] = -evaluation
            board.pop_move()
        best_move = max(move_evals_dict, key=move_evals_dict.get)  # type: ignore
        evaluation = move_evals_dict[best_move]
        self.evaluated_boards[board] = (best_move, evaluation)
        return best_move, evaluation

    def get_move(self, board: Board) -> tuple[int, int]:
        logging.info("calculating move")
        best_move, evaluation = self.evaluate_board_recursive(board)
        logging.info(f"board states considered: {len(self.evaluated_boards)}")
        logging.info(f"move evaluation: {evaluation}")
        return best_move


if __name__ == "__main__":
    board = Board(dim=3, num_to_win=3)
    engine = Engine()
    board_eval_recursive = engine.evaluate_board_recursive(board)
    print("board_eval_recursive:", board_eval_recursive)
