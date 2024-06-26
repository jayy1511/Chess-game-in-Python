from typing import List
from Piece import *


class Game:
    board: List[List[Piece]]
    last_move: tuple[Position, Position] = None

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

        self.board = [
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

    def is_check(self) -> bool:
        king_position = None
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if isinstance(piece, King):
                    king_position = piece.p
                    break
            if king_position is not None:
                break

        if king_position is None:
            return False  # No king found

        # Iterate through opponent's pieces and see if any can attack the king
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece is not None and piece.color != self.board[king_position.y][king_position.x].color:
                    possible_moves = piece.get_possible_moves()
                    if king_position in possible_moves:
                        return True  # King is in check
        return False  # King is not in check

    def is_checkmate(self) -> bool:
        # Check if the king is in check
        if not self.is_check():
            return False

        # Find the king's position
        king_position = None
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if isinstance(piece, King) and piece.color == self.board[y][x].color:
                    king_position = piece.p
                    break
            if king_position is not None:
                break

        # Check if the king has any legal moves to escape check
        king = self.board[king_position.y][king_position.x]
        for move in king.get_possible_moves():
            if not self.move_puts_king_in_check(king_position, move):
                return False

        return True

    def move_puts_king_in_check(self, king_position: Position, dst: Position) -> bool:
        '''Check if a move puts the king in check'''
        src_piece = self.board[king_position.y][king_position.x]
        dst_piece = self.board[dst.y][dst.x]

        # Temporarily move the piece
        self.board[dst.y][dst.x] = src_piece
        self.board[king_position.y][king_position.x] = None
        src_piece.p = dst

        # Check if the king is in check after the move
        result = self.is_check()

        # Move the piece back
        self.board[king_position.y][king_position.x] = src_piece
        self.board[dst.y][dst.x] = dst_piece
        src_piece.p = king_position

        return result

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
            raise RuntimeError("Invalid move")
        self.board[dst.y][dst.x] = piece
        self.board[src.y][src.x] = None
        piece.p = dst
        if isinstance(piece, Pawn) and abs(dst.y - src.y) == 2:
            piece.has_moved = True
        if isinstance(piece, Pawn) and piece.can_be_en_passant():
            if piece.color == 'white':
                self.board[dst.y - 1][dst.x] = None
            else:
                self.board[dst.y + 1][dst.x] = None
        self.last_move = (src, dst)

    def is_empty(self, pos: Position) -> bool:
        return self.board[pos.y][pos.x] is None

    def is_enemy(self, pos: Position, color: str) -> bool:
        piece = self.board[pos.y][pos.x]
        return piece is not None and piece.color != color
    
    def get_en_passant_moves(self):
        en_passant_moves = []
        last_move = self.last_move
        if last_move:
            src, dst = last_move
            src_piece = self.board[src.y][src.x]
            dst_piece = self.board[dst.y][dst.x]
            if isinstance(src_piece, Pawn) and abs(dst.y - src.y) == 2:
                if src_piece.color == 'white':
                    en_passant_position = Position(dst.x, dst.y - 1)
                else:
                    en_passant_position = Position(dst.x, dst.y + 1)
                en_passant_moves.append((en_passant_position, dst))
        return en_passant_moves
    
    def castle(self, src: Position, dst: Position) -> None:
        king = self.board[src.y][src.x]
        if not isinstance(king, King):
            raise RuntimeError("Only the king can castle")
        
        # Ensure the move is legal for castling
        if abs(dst.x - src.x) != 2 or dst.y != src.y:
            raise RuntimeError("Invalid castling move")

        # Check if the path between the king and rook is clear
        if dst.x > src.x:  # King side castle
            rook_src = Position(7, src.y)
            rook_dst = Position(5, src.y)
        else:  # Queen side castle
            rook_src = Position(0, src.y)
            rook_dst = Position(3, src.y)

        if not self.is_empty(rook_dst):
            raise RuntimeError("Invalid castling move")

        # Move the king
        self.move_piece(src, dst)
        # Move the rook
        self.move_piece(rook_src, rook_dst)


g = Game()
g.print()
