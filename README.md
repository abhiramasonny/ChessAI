# ChessAI

This repository contains a Python-based chess-playing AI that can make intelligent moves using a combination of a minimax algorithm and an opening book. The AI is implemented using the chess library for board representation and move generation.

## Features

- Minimax algorithm with alpha-beta pruning for intelligent move selection during the game.
- Opening book support using Polyglot format (`.bin`).
- Evaluation function to assess the strength of the board position.
- Endgame detection to handle checkmate and draw scenarios.

## Dependencies

Before running the code, make sure you install the requirements.
```bash
pip3 install -r requirements.txt
```


## Usage
   ```sh
   git clone https://github.com/abhiramasonny/ChessAI
   cd ChessAI
   pip3 install -r requirements.txt
   python3 main.py
   ```
   The program will start a chess match between you and the BOT. *Make sure to win!!*