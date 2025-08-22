import chess
import chess.engine
import numpy as np
from board_encoding import encode_board
from nn_model import create_nn_model
import tensorflow as tf
def generate_training_data(pgn_path, stockfish_path, max_games=100):
    import chess.pgn
    X, y = [], []
    with open(pgn_path) as f, chess.engine.SimpleEngine.popen_uci(stockfish_path) as stockfish:
        for gi in range(max_games):
            game = chess.pgn.read_game(f)
            if game is None: break
            board = game.board()
            for move in game.mainline_moves():
                board.push(move)
                arr = encode_board(board)
                info = stockfish.analyse(board, chess.engine.Limit(depth=12))  
                score = info["score"].white().score(mate_score=10000)
                score = np.tanh(score / 500.0)  
                X.append(arr)
                y.append(score)
                if len(X) >= 10000: break  
            if len(X) >= 10000: break
    X = np.array(X)
    y = np.array(y)
    return X, y

def train_and_save(X, y, save_path):
    model = create_nn_model()

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss', 
            patience=10, 
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss', 
            factor=0.5, 
            patience=5
        )
    ]
    
    model.fit(
        X, y, 
        epochs=100,  
        batch_size=32,  
        validation_split=0.2,  
        callbacks=callbacks,
        verbose=1
    )
    model.save(save_path)

if __name__ == "__main__":
    X, y = generate_training_data('game.pgn', r'C:\stockfish\stockfish-windows-x86-64-avx2.exe')
    train_and_save(X, y, 'chess_nn_model.keras')
