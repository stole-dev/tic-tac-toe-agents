import time


class Minimax:
    def __init__(self, minimax_cache=None):
        self.minimax_cache = minimax_cache or {}

    def play_minimax_training(self, state):
        start_time = time.time()
        def get_moves_values(state):
            moves = state.get_legal_moves()
            moves_values = []
            for move in moves:
                new_state = state.play_move(move)
                if (result := new_state.get_game_result()) < 2:
                    moves_values.append([move, result * 100])
                    self.minimax_cache[new_state.board.tobytes()] = result * 100
                    continue
                new_moves_values = get_moves_values(new_state)
                moves_values.append(self.min_or_max(new_state)(new_moves_values, key=lambda x: x[1]))
            self.minimax_cache[state.board.tobytes()] = self.min_or_max(state)(moves_values, key=lambda x: x[1])[1]
            return moves_values

        move_values = get_moves_values(state)
        end_time = time.time()
        print(f"Training time: {end_time - start_time})")
        return move_values

    def play_minimax_move(self, state):
        moves = state.get_legal_moves()
        best_move = max([[move, self.minimax_cache.get(state.play_move(move).board.tobytes())] for move in moves], key=lambda x: x[1])
        return best_move

    @staticmethod
    def min_or_max(state):
        turn = state.get_turn()
        if turn == 1:
            return max
        return min
