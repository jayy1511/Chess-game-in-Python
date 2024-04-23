# Chess-game-in-Python

This is a simple command-line based Chess game implemented in Python. It includes the game logic, piece movements, and basic user interface for playing chess.

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/jayy1511/Chess-game-in-Python.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Chess-game-in-Python
    ```

3. Run the main file to start the game:

    ```bash
    python main.py
    ```

## Features

- **Full Chess Game:** Play a complete game of chess against another player on the command line.
- **Piece Movement:** Implementations for all chess pieces (Pawn, Rook, Knight, Bishop, Queen, King) with valid moves.
- **Check and Checkmate Detection:** Detects when a player is in check or checkmate.

## How to Play

1. Run the `main.py` file.
2. Enter the source position (e.g., a2) and destination position (e.g., a4) to move a piece.
3. Play alternates between white and black pieces.
4. The game continues until a player is in checkmate.

## Files

- **ChessBoard.py:** Contains the `Game` class which represents the chess board and game logic.
- **Piece.py:** Contains implementations for all chess pieces (Pawn, Rook, Knight, Bishop, Queen, King).
- **main.py:** Main file to run the chess game and handle user input.
- **test_Game.py:** Unit tests for the chess game logic.
- **test_Piece.py:** Unit tests for the chess pieces.

## Unit Tests

Unit tests are provided to ensure the correctness of game logic and piece movements. To run the tests:

```bash
python -m unittest
