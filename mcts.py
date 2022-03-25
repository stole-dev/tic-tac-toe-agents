import math
import random

import numpy as np
from typing import List


class Node:

    def __init__(self, board, parents=None):
        self.wins = 0
        self.loses = 0
        self.draws = 0
        self.visits = 0
        self.board = board
        self.parents = parents
        self.is_win = False
        self.is_loss = False
        self.is_draw = False

        if not parents:
            self.parents = []

    @property
    def node_value(self):
        return (self.wins + self.draws) / self.visits


class MonteCarloTreeSearch:

    def __init__(self):
        self.board = ""

    def rollout(self):
        pass

    def get_move(self):
        pass


def play_mcts_move(board, board_cache):
    preform_training_playout(board, board_cache)
    return choose_move(board, board_cache)


def preform_training_playout(board, board_cache):
    for i in range(4000):
        preform_game_playout(board, board_cache)


def preform_game_playout(board, board_cache):
    game_history = [board]
    while not is_leaf_node(board, board_cache) and (result := board.get_game_result()) > 1:
        move = choose_move(board, board_cache)
        board = board.play_move(move[0])
        game_history.append(board)

    if is_leaf_node(board, board_cache) and (result := board.get_game_result()) > 1:
        leaf_nodes = create_leaf_nodes(board, board_cache)
        board = pick_node_for_rollout(leaf_nodes)[0].board
        result = rollout(board)
        game_history.append(board)

    backpropagate(game_history, result, board_cache)


def create_leaf_nodes(parent_board, board_cache):
    moves = get_legal_moves(parent_board)
    leaf_nodes = []
    parent_node = find_or_create_node(parent_board, board_cache)
    for move in moves:
        board = parent_board.play_move(move)
        leaf_nodes.append(create_node(board, board_cache, parent_node))
    return leaf_nodes


def pick_node_for_rollout(leaf_nodes: List):
    rollout_node = max([[node, calculate_node_value(node)] for node in leaf_nodes], key=lambda x: x[1])
    return rollout_node


def is_leaf_node(board, board_cache):
    node = board_cache.get(board.board.tobytes())
    if node and node.visits > 0:
        return False
    return True


def rollout(board):
    while (result := board.get_game_result()) > 1:
        move = choose_random_move(board)
        board = board.play_move(move)
    return result


def choose_random_move(board):
    moves = get_legal_moves(board)
    return random.choice(moves)


def play_move(board, board_cache):
    node = Node(board)
    legal_moves = get_legal_moves(board)
    if not node.visits:
        pass
    return ''


def find_or_create_node(board, board_cache):
    node = board_cache.get(board.board.tobytes())
    if not node:
        node = Node(board)
        result = board.get_game_result()
        if result == 1:
            node.is_win = True
        elif result == -1:
            node.is_loss = True
        elif result == 0:
            node.is_draw = True
        board_cache[board.board.tobytes()] = node
    return node


def create_node(board, board_cache, parent_node):
    node = Node(board)
    result = board.get_game_result()
    if result == 1:
        node.is_win = True
    elif result == -1:
        node.is_loss = True
    elif result == 0:
        node.is_draw = True
    if parent_node not in node.parents:
        node.parents.append(parent_node)
    board_cache[board.board.tobytes()] = node
    return node


def find_node(board, board_cache):
    return board_cache[board.board.tobytes()]


def choose_move(board, board_cache):
    moves = [calculate_value(i, board, board_cache) for i in get_legal_moves(board)]
    return max(moves, key=lambda x: x[1])


def calculate_value(move, parent_board, board_cache):
    board = parent_board.play_move(move)
    node = find_or_create_node(board, board_cache)
    if node.visits == 0:
        if (parent_node := find_node(parent_board, board_cache)) not in node.parents:
            node.parents.append(parent_node)
        return [move, math.inf]

    # elif node.is_win:
    #     return [move, math.inf]
    #
    # elif node.is_loss:
    #     return [move, -math.inf]
    #
    # elif node.is_draw:
    #     return [move, 1000]
    new_value = node.node_value + (math.sqrt(2) * math.sqrt(math.log(get_root_node_visits(board_cache)) / node.visits))
    return [move, new_value, node]


def calculate_node_value(node):
    if node.visits == 0 or node.is_win:
        return math.inf

    elif node.is_loss:
        return -math.inf

    elif node.is_draw:
        return 1000
    value = node.node_value + (1.4 * math.sqrt(math.log(get_parent_visits(node)) / node.visits))
    return value


def backpropagate(game_history, value, board_cache):
    # This won't work because there can be many ways to come to the same state and therefore
    # not right parents will be updated
    # for parent in node.parents:
    #     update_node_with_result(parent, value)
    #     backpropagate(parent, value)
    for board in game_history:
        update_node_with_result(find_node(board, board_cache), value)



def get_legal_moves(board):
    return list(zip(*np.where(board.board == 0)))


def get_parent_visits(node):
    visits = 0
    for parent in node.parents:
        visits += get_parent_visits(parent)
    return visits


def get_root_node_visits(board_cache):
    root_board = np.array([0] * 9).reshape(3,3)
    root_node = board_cache.get(root_board.tobytes())
    if root_node:
        return root_node.visits
    return 1


def update_node_with_result(node, value):
    if value == 1:
        node.wins += 1
    elif value == 0:
        node.draws += 1
    else:
        node.loses += 1
    node.visits += 1
