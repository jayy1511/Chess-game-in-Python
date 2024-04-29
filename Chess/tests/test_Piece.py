import unittest
from Piece import *
from ChessBoard import Game


class PawnTest(unittest.TestCase):
    def test_first_row(self):
        p = Pawn("white", Position(1, 1), Game())
        pos = p.get_possible_moves()
        expected = [Position(1, 2), Position(1, 3)]
        self.assertEqual(pos, expected)

    def test_last_row(self):
        p = Pawn("white", Position(1, 7), Game())
        pos = p.get_possible_moves()
        expected = []
        self.assertEqual(pos, expected)

    def test_white_destination(self):
        p1 = Pawn("white", Position(1, 1))
        p2 = Rook("white", Position(1, 2))
        g = Game()
        g.board[1][1] = p1
        g.board[2][1] = p2
        p1.g = g
        excepted = []
        self.assertEqual(p1.get_possible_moves(), excepted)

    def test_white_destination_2(self):
        p1 = Pawn("white", Position(1, 1))
        p2 = Rook("white", Position(1, 3))
        g = Game()
        g.board[1][1] = p1
        g.board[3][1] = p2
        p1.g = g
        excepted = [Position(1, 2)]
        self.assertEqual(p1.get_possible_moves(), excepted)

    def test_black_destination(self):
        g = Game()
        p1 = Pawn("black", Position(1, 6), g)
        p2 = Rook("black", Position(1, 5), g)
        g.board[6][1] = p1
        g.board[5][1] = p2
        p1.g = g
        excepted = []
        self.assertEqual(p1.get_possible_moves(), excepted)

    def test_black_destination_2(self):
        g = Game()
        p1 = Pawn("black", Position(1, 6), g)
        p2 = Rook("black", Position(1, 4), g)
        g.board[6][1] = p1
        g.board[4][1] = p2
        p1.g = g
        excepted = [Position(1, 5)]
        self.assertEqual(p1.get_possible_moves(), excepted)

    def test_en_passant(self):
        g = Game()
        p1 = Pawn("white", Position(1, 4), g)
        p2 = Pawn("black", Position(3, 5), g)
        g.board[4][1] = p1
        g.board[5][2] = p2
        p1.g = g
        p2.g = g
        g.move_piece(Position(1, 4), Position(3, 4))
        moves = p2.get_possible_moves()
        self.assertIn(Position(2, 3), moves)
        self.assertIn(Position(2, 5), moves)


class RookTest(unittest.TestCase):
    def test_first_row(self):
        r = Rook("white", Position(0, 0), Game())
        pos = r.get_possible_moves()
        expected = []
        self.assertEqual(pos, expected)

    def test_last_row(self):
        r = Rook("white", Position(0, 7), Game())
        pos = r.get_possible_moves()
        expected = [Position(1, 7), Position(0, 6)]
        self.assertEqual(pos, expected)

    def test_white_destination(self):
        r1 = Rook("white", Position(0, 0))
        r2 = Pawn("white", Position(0, 1))
        g = Game()
        g.board[0][0] = r1
        g.board[0][1] = r2
        r1.g = g
        excepted = []
        self.assertEqual(r1.get_possible_moves(), excepted)

    def test_black_destination(self):
        g = Game()
        r1 = Rook("black", Position(0, 7), g)
        r2 = Pawn("black", Position(0, 6), g)
        g.board[7][0] = r1
        g.board[7][1] = r2
        r1.g = g
        excepted = []
        self.assertEqual(r1.get_possible_moves(), excepted)


class KnightTest(unittest.TestCase):
    def test_first_row(self):
        n = Knight("white", Position(1, 0), Game())
        pos = n.get_possible_moves()
        expected = [Position(x=2, y=2), Position(x=0, y=2)]
        self.assertEqual(pos, expected)

    def test_edge_of_board(self):
        n = Knight("black", Position(0, 0), Game())
        pos = n.get_possible_moves()
        expected = [Position(1, 2), Position(2, 1)]
        self.assertEqual(pos, expected)

    def test_center_of_board(self):
        n = Knight("white", Position(4, 4), Game())
        pos = n.get_possible_moves()
        expected = [
            Position(6, 5),
            Position(5, 6),
            Position(3, 6),
            Position(2, 5),
            Position(2, 3),
            Position(3, 2),
            Position(5, 2),
            Position(6, 3),
        ]
        self.assertEqual(pos, expected)


class BishopTest(unittest.TestCase):
    def test_first_row(self):
        b = Bishop("white", Position(2, 0), Game())
        pos = b.get_possible_moves()
        expected = []
        self.assertEqual(pos, expected)


class QueenTest(unittest.TestCase):
    def test_first_row(self):
        q = Queen("white", Position(3, 0), Game())
        pos = q.get_possible_moves()
        expected = []
        self.assertEqual(pos, expected)


class KingTest(unittest.TestCase):
    def test_first_row(self):
        k = King("white", Position(4, 0), Game())
        pos = k.get_possible_moves()
        expected = []
        self.assertEqual(pos, expected)


if __name__ == "__main__":
    unittest.main()
