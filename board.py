import numpy as np
import itertools

from abp import ABP
from mcts import *
from minimax import Minimax

PLAYER_SIGN = {1: "X", -1: 'O', 0: '-'}
CELL_X = 1
CELL_O = -1
CELL_EMPTY = 0
X_WINS = 1
O_WINS = -1
DRAW = 0
NOT_OVER = 2
PLAYERS = itertools.cycle([CELL_X, CELL_O])


class Board:

    def __init__(self, dim_x=3, dim_y=3, board_copy=None):
        self.dim_x = dim_x
        self.dim_y = dim_y

        if board_copy is not None:
            self.board = board_copy.reshape(self.dim_x, self.dim_y)
        else:
            self.board = np.array([CELL_EMPTY] * self.dim_x * self.dim_y).reshape(self.dim_x, self.dim_y)

    def get_game_result(self):
        lines = get_lines(self.board)
        lines_sums = list(map(sum, lines))

        if max(lines_sums) == 3:
            return X_WINS

        if min(lines_sums) == -3:
            return O_WINS

        if CELL_EMPTY not in self.board:
            return DRAW

        return NOT_OVER

    def get_turn(self):
        non_zero = np.count_nonzero(self.board)
        return CELL_X if is_even(non_zero) else CELL_O

    def play_move(self, move):
        board_copy = np.copy(self.board)
        board_copy[move] = self.get_turn()
        return Board(board_copy=board_copy)

    def get_legal_moves(self):
        return list(zip(*np.where(self.board == 0)))


class BoardCache:

    def __init__(self):
        self.history = []
        self.cache = {}


def play_game():
    board = Board()
    board_cache = BoardCache().cache
    # minimax = Minimax(board_cache)
    # minimax.play_minimax_training(board)
    abp = ABP(board_cache)
    abp.play_abp_training(board)

    while (result := board.get_game_result()) > 1:
        # move = play_mcts_move(board, board_cache)
        # move = minimax.play_minimax_move(board)
        move = abp.play_abp_move(board)
        board = board.play_move(move[0])
        print_board(board.board)
        if (result := board.get_game_result()) > 1:
            move = tuple([int(i) for i in input()])
            board = board.play_move(move)
            print_board(board.board)
        else:
            break

    print(result)


def is_even(value: int):
    return (value % 2 + 1) % 2


def get_lines(board):
    return get_rows_and_diagonal(board) + get_cols_and_antidiagonal(board)


def get_rows_and_diagonal(board):
    return [row for row in board] + [board.diagonal()]


def get_cols_and_antidiagonal(board):
    rotated_board = np.rot90(board)
    return get_rows_and_diagonal(rotated_board)


def print_board(board_to_print):
    board_str = '\n'
    for i in range(3):
        board_str += '|'
        for j in range(3):
            board_str += PLAYER_SIGN[board_to_print[i, j]] + '|'
        board_str += '\n'
    print(board_str)
