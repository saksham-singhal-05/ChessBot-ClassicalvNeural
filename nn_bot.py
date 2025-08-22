import chess
import numpy as np
import tensorflow as tf
from board_encoding import encode_board
import random

class NNChessBot:
    def __init__(self, model_path, color=chess.WHITE, search_depth=2):
        self.model = tf.keras.models.load_model(model_path)
        self.color = color
        self.search_depth = search_depth

    def choose_move(self, board):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        # Use temperature 
        move_number = board.fullmove_number
        temperature = max(0.1, 1.5 - 0.06 * move_number)  

        scored_moves = []
        for move in legal_moves:
            board.push(move)
            score = self.nn_minimax(board, self.search_depth - 1, maximizing=(self.color == board.turn))
            board.pop()
            scored_moves.append((move, score))

        scores = np.array([score if self.color == chess.WHITE else -score for (_, score) in scored_moves])

        exp_scores = np.exp(scores / temperature)
        probs = exp_scores / np.sum(exp_scores)

        move = np.random.choice([m for (m, _) in scored_moves], p=probs)
        return move

    def nn_minimax(self, board, depth, maximizing):
        if depth == 0 or board.is_game_over():
            return self.get_evaluation(board)

        legal_moves = list(board.legal_moves)
        if maximizing:
            best_val = -float('inf')
            for move in legal_moves:
                board.push(move)
                value = self.nn_minimax(board, depth - 1, False)
                board.pop()
                if value > best_val:
                    best_val = value
            return best_val
        else:
            best_val = float('inf')
            for move in legal_moves:
                board.push(move)
                value = self.nn_minimax(board, depth - 1, True)
                board.pop()
                if value < best_val:
                    best_val = value
            return best_val

    def get_evaluation(self, board):
        """Always returns evaluation from bot's perspective: >0 is good for bot, <0 is bad for bot."""
        arr = encode_board(board)
        arr = np.expand_dims(arr, axis=0)
        value = float(self.model(arr, training=False).numpy()[0,0])
        # From Black's perspective, flip sign
        if self.color == chess.BLACK:
            value = -value
        return value
