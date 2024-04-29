from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Piece(ABC):
    color: str
    p: Position = None
    g: "Game" = None

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def get_possible_moves(self) -> List[Position]:
        pass

    def can_be_en_passant(self) -> bool:
        return False


@dataclass
class Pawn(Piece):
    has_moved: bool = False

    def __str__(self) -> str:
        return "♙" if self.color == "white" else "♟"

    def get_possible_moves(self) -> List[Position]:
        if self.color == "white":
            direction = 1
            start_row = 1
            en_passant_row = 4
        else:
            direction = -1
            start_row = 6
            en_passant_row = 3

        positions = []
        if self.p.y == start_row and not self.has_moved:
            # Pawn can move two squares forward from starting position
            positions.append(Position(self.p.x, self.p.y + 2 * direction))

        positions.append(Position(self.p.x, self.p.y + direction))

        # Capture moves
        for dx in [-1, 1]:
            new_x = self.p.x + dx
            new_y = self.p.y + direction
            if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                piece = self.g.board[new_y][new_x]
                if piece is not None and piece.color != self.color:
                    positions.append(Position(new_x, new_y))
                elif piece is None and self.can_be_en_passant():
                    positions.append(Position(new_x, new_y))

        empty_positions = [p for p in positions if self.g.is_empty(p)]
        return empty_positions

    def can_be_en_passant(self) -> bool:
        if self.g.last_move is None:
            return False
        last_move_src, last_move_dst = self.g.last_move
        last_move_piece = self.g.board[last_move_dst.y][last_move_dst.x]
        return (
            isinstance(last_move_piece, Pawn)
            and last_move_piece.color != self.color
            and abs(last_move_dst.y - last_move_src.y) == 2
            and last_move_dst.y == self.p.y
            and abs(last_move_dst.x - self.p.x) == 1
        )


class Rook(Piece):
    def get_possible_moves(self) -> List[Position]:
        positions = []
        for i in range(self.p.x + 1, 8):
            if self.g.is_empty(Position(i, self.p.y)):
                positions.append(Position(i, self.p.y))
            else:
                if self.g.is_enemy(Position(i, self.p.y), self.color):
                    positions.append(Position(i, self.p.y))
                break
        for i in range(self.p.x - 1, -1, -1):
            if self.g.is_empty(Position(i, self.p.y)):
                positions.append(Position(i, self.p.y))
            else:
                if self.g.is_enemy(Position(i, self.p.y), self.color):
                    positions.append(Position(i, self.p.y))
                break
        for i in range(self.p.y + 1, 8):
            if self.g.is_empty(Position(self.p.x, i)):
                positions.append(Position(self.p.x, i))
            else:
                if self.g.is_enemy(Position(self.p.x, i), self.color):
                    positions.append(Position(self.p.x, i))
                break
        for i in range(self.p.y - 1, -1, -1):
            if self.g.is_empty(Position(self.p.x, i)):
                positions.append(Position(self.p.x, i))
            else:
                if self.g.is_enemy(Position(self.p.x, i), self.color):
                    positions.append(Position(self.p.x, i))
                break
        return positions

    def __str__(self) -> str:
        return "♖" if self.color == "white" else "♜"


class Knight(Piece):

    def __str__(self) -> str:
        return "♘" if self.color == "white" else "♞"

    def get_possible_moves(self) -> List[Position]:
        positions = []
        offsets = [
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1),
        ]
        for offset in offsets:
            new_x = self.p.x + offset[0]
            new_y = self.p.y + offset[1]
            if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                if (
                    self.g.is_empty(Position(new_x, new_y))
                    or self.g.is_enemy(Position(new_x, new_y), self.color)
                ):
                    positions.append(Position(new_x, new_y))
        return positions


class Bishop(Piece):

    def __str__(self) -> str:
        return "♗" if self.color == "white" else "♝"

    def get_possible_moves(self) -> List[Position]:
        positions = []
        offsets = [
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        for offset in offsets:
            new_x = self.p.x + offset[0]
            new_y = self.p.y + offset[1]
            while 0 <= new_x <= 7 and 0 <= new_y <= 7:
                if self.g.is_empty(Position(new_x, new_y)):
                    positions.append(Position(new_x, new_y))
                else:
                    if self.g.is_enemy(Position(new_x, new_y), self.color):
                        positions.append(Position(new_x, new_y))
                    break
                new_x += offset[0]
                new_y += offset[1]
        return positions


class Queen(Piece):
    def __str__(self) -> str:
        return "♕" if self.color == "white" else "♛"

    def get_possible_moves(self) -> List[Position]:
        positions = []

        # cross move 
        offsets = [
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        for offset in offsets:
            new_x = self.p.x + offset[0]
            new_y = self.p.y + offset[1]
            while 0 <= new_x <= 7 and 0 <= new_y <= 7:
                if self.g.is_empty(Position(new_x, new_y)):
                    positions.append(Position(new_x, new_y))
                else:
                    if self.g.is_enemy(Position(new_x, new_y), self.color):
                        positions.append(Position(new_x, new_y))
                    break
                new_x += offset[0]
                new_y += offset[1]

        # horizontal and vertical moves
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            dx, dy = direction
            x, y = self.p.x + dx, self.p.y + dy
            while 0 <= x <= 7 and 0 <= y <= 7:
                if self.g.is_empty(Position(x, y)):
                    positions.append(Position(x, y))
                else:
                    if self.g.is_enemy(Position(x, y), self.color):
                        positions.append(Position(x, y))
                    break
                x += dx
                y += dy
        return positions


class King(Piece):
    def __str__(self) -> str:
        return "♔" if self.color == "white" else "♚"

    def get_possible_moves(self) -> List[Position]:
        positions = []
        offsets = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        for offset in offsets:
            new_x = self.p.x + offset[0]
            new_y = self.p.y + offset[1]
            if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                if (
                    self.g.is_empty(Position(new_x, new_y))
                    or self.g.is_enemy(Position(new_x, new_y), self.color)
                ):
                    positions.append(Position(new_x, new_y))
        return positions
