from typing import List
from Piece import *

class Game:
    board: List[List[Piece]]

    def __init__(self):
        Q = Queen
        K = King
        B = Bishop
        N = Knight
        R = Rook
        P = Pawn
        w = 'white'
        b = 'black'

        # self.board = [[None for _ in range(8)] for _ in range(8)]

        self.board =[
        [R(w), N(w), B(w), Q(w), K(w), B(w), N(w), R(w)],
        [P(w), P(w), P(w), P(w), P(w), P(w), P(w), P(w)],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [P(b), P(b), P(b), P(b), P(b), P(b), P(b), P(b)],
        [R(b), N(b), B(b), Q(b), K(b), B(b), N(b), R(b)]
        ]

        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece is not None:
                    piece.p = Position(x, y)
                    piece.g = self

    def print(self):
        output = ''
        for line in self.board:
            for piece in line:
                if piece is not None:
                    output += str(piece) + ' '
                else:
                    output += '  '
            output += '\n'
        print(output, end='')
    def is_checkmate(self) -> bool:
        # FIX ME
        return False
    
    def move_piece(self, src: Position, dst: Position) -> None:
        '''Move the piece to the destination, 
        if the move is not valid, raise an exception'''
        
        if not (0 <= src.x <= 7 and 0 <= src.y <= 7 and
                0 <= dst.x <= 7 and 0 <= dst.y <= 7):
            raise RuntimeError("Invalid move")
        
        piece = self.board[src.y][src.x]
        if piece is None:
            raise RuntimeError("No piece at the source position")
        valid_positions = piece.get_possible_moves()
        if dst not in valid_positions:
            raise RuntimeError("Invalid move") # why RuntimeError?
        self.board[dst.y][dst.x] = piece
        self.board[src.y][src.x] = None
        piece.p = dst

    
g = Game()
g.print()

p1 = Position(2, 3)
p2 = Position(2, 3)
print("Is p1 and p2 equal?", p1 == p2)

class PositionTwo:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
p1 = PositionTwo(2, 3)
p2 = PositionTwo(2, 3)
print("Is p1 and p2 equal?", p1 == p2)