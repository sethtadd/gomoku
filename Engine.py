from Board import DRAW, Board
from Player import Player


class Engine(Player):
    def __init__(self) -> None:
        pass

    # def evaluate_board(self, board: Board) -> float:
    #     # check for game over
    #     if board.winner is not None:
    #         if board.winner == DRAW:
    #             return 0
    #         elif board.winner == board.turn:
    #             return 1
    #         else:
    #             return -1
    #     # return random evaluation
    #     return (random() * 2 - 1) * 0.9  # interval [-0.9, 0.9)

    def evaluate_board_recursive(self, board: Board) -> tuple[tuple[int, int], float]:
        # check for game over
        if board.winner is not None:
            if board.winner == DRAW:
                return (-1, -1), 0
            elif board.winner == board.turn:
                return (-1, -1), 1
            else:
                return (-1, -1), -1
        # else do recursive evaluation
        moves: dict[tuple[int, int], float] = dict.fromkeys(board.get_open_positions())  # type: ignore
        for move in moves:
            board.push_move(move)
            _, evaluation = self.evaluate_board_recursive(board)
            moves[move] = -evaluation
            board.pop_move()
        best_move = max(moves, key=lambda k: best_move.get)  # type: ignore
        return best_move, moves[best_move]

    def get_move(self, board: Board) -> tuple[int, int]:
        best_move, evaluation = self.evaluate_board_recursive(board)
        print("evaluation:", evaluation)
        return best_move

    # def evaluate_moves(self, board: Board, move: tuple[int, int]):
    #     moves = dict.fromkeys(board.get_open_positions(), None)
    #     for move in moves:
    #         temp_board = board.deepcopy()
    #         temp_board.push_move(move)
    #         evaluation = self.evaluate_board(temp_board)
    #         moves[move] = evaluation

    # def evaluate_move(self, board: Board) -> float:
    #     moves = dict.fromkeys(board.get_open_positions(), None)
    #     for move in moves:
    #         temp_board = board.deepcopy()
    #         temp_board.push_move(move)
    #         evaluation = self.evaluate_board(temp_board)
    #         moves[move] = evaluation


if __name__ == "__main__":
    board = Board(dim=3, num_to_win=3)
    engine = Engine()
    board_eval_recursive = engine.evaluate_board_recursive(board)
    print("board_eval_recursive:", board_eval_recursive)
