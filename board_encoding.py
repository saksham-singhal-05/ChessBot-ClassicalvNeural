import numpy as np
import chess

def encode_board(board):
    """Encode board as (8,8,12) float32 tensor: 6 pieces per color one-hot"""
    arr = np.zeros((8, 8, 12), dtype=np.float32)
    piece_map = {
        chess.PAWN: 0,
        chess.KNIGHT: 1,
        chess.BISHOP: 2,
        chess.ROOK: 3,
        chess.QUEEN: 4,
        chess.KING: 5,
    }
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            cidx = 0 if piece.color == chess.WHITE else 6
            pidx = piece_map[piece.piece_type]
            row = chess.square_rank(square)
            col = chess.square_file(square)
            arr[row, col, cidx + pidx] = 1
    return arr