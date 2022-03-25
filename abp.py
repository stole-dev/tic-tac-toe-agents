import time

MAX, MIN = 1000, -1000


class ABP:
    def __init__(self, abp_cache=None):
        self.abp_cache = abp_cache or {}

    def play_abp_training(self, state):
        start_time = time.time()

        def get_moves_values(state, alpha, beta):
            moves = state.get_legal_moves()
            moves_values = []
            for move in moves:
                new_state = state.play_move(move)
                if (result := new_state.get_game_result()) < 2:
                    moves_values.append([move, result * 100])
                    self.abp_cache[new_state.board.tobytes()] = result * 100
                    if state.get_turn() == 1:
                        best = result * 100
                        if best >= beta:
                            break
                        alpha = max(alpha, best)
                    else:
                        best = result * 100
                        if best <= alpha:
                            break
                        beta = min(beta, best)
                    continue
                new_moves_values = get_moves_values(new_state, alpha, beta)
                new_best_move = self.min_or_max(new_state)(new_moves_values, key=lambda x: x[1])
                moves_values.append(new_best_move)
                if state.get_turn() == 1:
                    best = new_best_move[1]
                    if best >= beta:
                        break
                    alpha = max(alpha, best)

                else:
                    best = new_best_move[1]
                    if best <= alpha:
                        break
                    beta = min(beta, best)

                # moves_values.append(self.min_or_max(new_state)(new_moves_values, key=lambda x: x[1]))
            self.abp_cache[state.board.tobytes()] = self.min_or_max(state)(moves_values, key=lambda x: x[1])[1]
            return moves_values

        move_values = get_moves_values(state, MIN, MAX)
        end_time = time.time()
        print(f"Training time: {end_time - start_time})")
        return move_values

    def play_abp_move(self, state):
        if self.abp_cache.get(state.board.tobytes()) is None:
            self.play_abp_training(state)

        moves = []
        for move in state.get_legal_moves():
            move_value = self.abp_cache.get(state.play_move(move).board.tobytes())
            if move_value is not None:
                moves.append([move, move_value])

        best_move = max(moves, key=lambda x: x[1])
        return best_move

    @staticmethod
    def min_or_max(state):
        turn = state.get_turn()
        if turn == 1:
            return max
        return min
