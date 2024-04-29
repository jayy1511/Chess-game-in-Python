import unittest
from ChessBoard import Game, Position
from Piece import *


class TestCheckmate(unittest.TestCase):
    def test_checkmate(self):
        game = Game()
        game.board[0][0] = King("black", Position(0, 0), game)
        game.board[1][1] = Queen("white", Position(1, 1), game)
        is_checkmate = game.is_checkmate()
        self.assertTrue(is_checkmate)

    def test_not_checkmate(self):
        game = Game()
        game.board[0][0] = King("black", Position(0, 0), game)
        game.board[1][1] = Rook("white", Position(1, 1), game)
        is_checkmate = game.is_checkmate()
        self.assertFalse(is_checkmate)

    def test_king_in_corner(self):
        game = Game()
        game.board[0][0] = King("black", Position(0, 0), game)
        game.board[7][1] = Rook("white", Position(1, 7), game)
        is_checkmate = game.is_checkmate()
        self.assertFalse(is_checkmate)

if __name__ == "__main__":
    unittest.main()