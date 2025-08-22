
# ChessBot vs NNChessBot

A Python-based chess engine matchup: traditional alpha-beta minimax bot vs. a neural network-based evaluation bot. Includes a Tkinter GUI for automated matches and a full training pipeline for the neural network evaluation function.

## Features

- **Classic Minimax Bot:** Alpha-beta pruned search up to configurable depth using a handcrafted evaluation function.
- **Neural Network Bot:** Uses a convolutional neural network (CNN) trained on Stockfish-evaluated positions.
- **Hybrid NN-Minimax Search:** The NN bot uses a shallow minimax search with its NN evaluation for much stronger and more varied play.
- **Softmax Temperature for NN:** Add variety—games do not repeat.
- **Tkinter GUI:** Visual board, automatic match cycle, real-time results.
- **Training Pipeline:** Generate training data from PGNs using Stockfish, train the CNN model, save models for easy swapping/experimenting.
- **Modular Design:** Swap out evaluation functions, adjust search/training parameters easily.

## Requirements

- Python 3.8+
- `python-chess`
- `tensorflow` (for neural network)
- `numpy`
- `tkinter` (for GUI; usually included with Python)
- Stockfish binary (for training) :https://stockfishchess.org/download/


Install requirements via pip:
```bash
pip install python-chess tensorflow numpy
```

## Files Overview

- `bot.py` — Classical minimax bot implementation.
- `nn_bot.py` — Neural network bot with minimax and temperature-based move selection.
- `board_encoding.py` — Board-to-tensor encoder for NN input.
- `evaluation.py` — Handcrafted position evaluation.
- `search.py` — Alpha-beta minimax search routines.
- `nn_model.py` — Model architecture for the neural network.
- `nn_training.py` — Script to generate training data & train the NN model.
- `tkinter_match_bot_vs_nn.py` — GUI for head-to-head bot matches.

## Usage

### 1. Train the Neural Network Model

You need a PGN of games and Stockfish binary.

```bash
python nn_training.py
```
- Adjust PGN path, Stockfish path, and number of games as needed in `nn_training.py`.
- When finished, a `.keras` model is saved (default: `chess_nn_model.keras`).

### 2. Run the Bot Match GUI

```bash
python tkinter_match_bot_vs_nn.py
```
- The GUI pops up and you can start a full match between the bots.
- Game status, move history, and result are displayed.

### 3. Adjust Bot Strength & Variety

- **Depths:** Change search depth in `ChessBot` or `NNChessBot` constructors for stronger, slower engines.
- **NN Variety:** The NN bot varies its play by default—lower the temperature in `nn_bot.py` to make it greedier, raise to make it more diverse.

## Example: Comparing Bots

```python
from nn_bot import NNChessBot
from bot import ChessBot

nn_bot = NNChessBot("chess_nn_model.keras", color=chess.BLACK, search_depth=2)
classic_bot = ChessBot(depth=4)
```

## Data & Training

- Training labels come from Stockfish; positions are from actual games.
- By default, labels are normalized using `tanh`; feel free to experiment!
- Add more positions for a smarter NN.

## Notes/Tips

- **Model Size:** Model quality is tied to your training data and evaluation depth.
- **Speed:** The NN bot’s search depth trades off speed for quality—good settings: depth=2.
- **Evaluation:** NN always evaluates from its color’s perspective. No need to flip signs manually.
- **Opening Book:** Add your own by randomizing a few opening moves for more diversity.

## Troubleshooting

- If you see “no legal moves,” make sure the board is in a valid state.
- If TensorFlow complains, double-check your installed version.

