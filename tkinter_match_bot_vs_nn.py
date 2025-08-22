

import tkinter as tk
from tkinter import messagebox
import chess
import time

from bot import ChessBot
from nn_bot import NNChessBot

class BotMatchGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ChessBot vs NNChessBot")
        self.root.geometry("700x650")

        self.board = chess.Board()
        self.smart_bot = ChessBot(depth=2)  # classical
        self.nn_bot = NNChessBot("chess_nn_model.keras", color=chess.BLACK)  # set correct path!
        self.smart_bot.set_color(chess.WHITE)
        self.nn_bot.color = chess.BLACK

        self.squares = {}
        self.light_color = "#F0D9B5"
        self.dark_color = "#B58863"

        self.create_board()
        self.update_board_display()
        self.status_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.status_label.pack(pady=10)
        tk.Button(self.root, text="Start Match", command=self.run_match).pack(pady=5)
        self.move_history = []

    def create_board(self):
        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=10)
        self.squares = {}
        files = "abcdefgh"
        ranks = range(8, 0, -1)
        for i, rank in enumerate(ranks):
            row_frame = tk.Frame(board_frame)
            row_frame.pack()
            for j, file_letter in enumerate(files):
                square_name = f"{file_letter}{rank}"
                bg_color = self.light_color if (i + j) % 2 else self.dark_color
                button = tk.Label(
                    row_frame,
                    width=4,
                    height=2,
                    bg=bg_color,
                    font=('Arial', 18)
                )
                button.pack(side=tk.LEFT)
                self.squares[square_name] = button

    def get_piece_symbol(self, piece):
        piece_symbols = {
            chess.PAWN: {"white": "♙", "black": "♟"},
            chess.ROOK: {"white": "♖", "black": "♜"},
            chess.KNIGHT: {"white": "♘", "black": "♞"},
            chess.BISHOP: {"white": "♗", "black": "♝"},
            chess.QUEEN: {"white": "♕", "black": "♛"},
            chess.KING: {"white": "♔", "black": "♚"},
        }
        if piece is None:
            return ""
        color = "white" if piece.color == chess.WHITE else "black"
        return piece_symbols[piece.piece_type][color]

    def update_board_display(self):
        files = "abcdefgh"
        ranks = range(8, 0, -1)
        for i, rank in enumerate(ranks):
            for j, file_letter in enumerate(files):
                square_name = f"{file_letter}{rank}"
                square = chess.parse_square(square_name)
                piece = self.board.piece_at(square)
                self.squares[square_name].config(text=self.get_piece_symbol(piece))

    def run_match(self):
        self.move_history = []
        self.board.reset()
        self.update_board_display()
        self.root.after(500, self.step_move)

    def step_move(self):
        if self.board.is_game_over():
            self.show_game_over()
            return

        turn = "ChessBot (White)" if self.board.turn == chess.WHITE else "NNChessBot (Black)"
        self.status_label.config(text=f"{turn} thinking...")

        # Decide which bot moves
        if self.board.turn == chess.WHITE:
            move = self.smart_bot.choose_move(self.board)
        else:
            move = self.nn_bot.choose_move(self.board)
        self.board.push(move)
        self.move_history.append(move)
        self.update_board_display()

        if self.board.is_game_over():
            self.show_game_over()
        else:
            # advance after brief delay
            self.root.after(500, self.step_move)

    def show_game_over(self):
        result = self.board.result()
        if result == "1-0":
            msg = "ChessBot (White) wins!"
        elif result == "0-1":
            msg = "NNChessBot (Black) wins!"
        else:
            msg = "It's a draw!"
        self.status_label.config(text=f"Match over: {msg} ({result})")
        messagebox.showinfo("Game Over", msg)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = BotMatchGUI()
    gui.run()
