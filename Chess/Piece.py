from abc import ABC, abstractmethod
from dataclasses import dataclass
    

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
    def get_possible_moves(self) -> list[Position]:
        pass


@dataclass
class Pawn(Piece):

    def __str__(self) -> str:
        return "♙" if self.color == "white" else "♟"

    def get_possible_moves(self) -> list[Position]:
        if self.color == "white":
            if self.p.y == 1 and self.g.board[self.p.y + 1][self.p.x] is None:
                positions = [
                    Position(self.p.x, self.p.y + 1),
                    Position(self.p.x, self.p.y + 2),
                ]
            else:
                positions = [Position(self.p.x, self.p.y + 1)]
        else:
            if self.p.y == 6 and self.g.board[self.p.y - 1][self.p.x] is None:
                positions = [
                    Position(self.p.x, self.p.y - 1),
                    Position(self.p.x, self.p.y - 2),
                ]
            else:
                positions = [Position(self.p.x, self.p.y - 1)]
        empty_positions = []
        for p in positions:
            if not (0 <= p.x <= 7 and 0 <= p.y <= 7):
                continue
            if self.g.board[p.y][p.x] is None:
                empty_positions.append(p)
        return empty_positions


class Rook(Piece):
    def get_possible_moves(self) -> list[Position]:
        positions = []
        for i in range(self.p.x + 1, 8):
            if self.g.board[self.p.y][i] is None:
                positions.append(Position(i, self.p.y))
            else:
                if self.g.board[self.p.y][i].color != self.color:
                    positions.append(Position(i, self.p.y))
                break
        for i in range(self.p.x - 1, -1, -1):
            if self.g.board[self.p.y][i] is None:
                positions.append(Position(i, self.p.y))
            else:
                if self.g.board[self.p.y][i].color != self.color:
                    positions.append(Position(i, self.p.y))
                break
        for i in range(self.p.y + 1, 8):
            if self.g.board[i][self.p.x] is None:
                positions.append(Position(self.p.x, i))
            else:
                if self.g.board[i][self.p.x].color != self.color:
                    positions.append(Position(self.p.x, i))
                break
        for i in range(self.p.y - 1, -1, -1):
            if self.g.board[i][self.p.x] is None:
                positions.append(Position(self.p.x, i))
            else:
                if self.g.board[i][self.p.x].color != self.color:
                    positions.append(Position(self.p.x, i))
                break
        return positions

    def __str__(self) -> str:
        return "♖" if self.color == "white" else "♜"


class Knight(Piece):

    def __str__(self) -> str:
        return "♘" if self.color == "white" else "♞"

    def get_possible_moves(self) -> list[Position]:
        if self.g is None:
            return [] 
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
                    self.g.board[new_y][new_x] is None
                    or self.g.board[new_y][new_x].color != self.color
                ):
                    positions.append(Position(new_x, new_y))
        return positions


class Bishop(Piece):

    def __str__(self) -> str:
        return "♗" if self.color == "white" else "♝"

    def get_possible_moves(self) -> list[Position]:
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
                if self.g.board[new_y][new_x] is None:
                    positions.append(Position(new_x, new_y))
                else:
                    if self.g.board[new_y][new_x].color != self.color:
                        positions.append(Position(new_x, new_y))
                    break
                new_x += offset[0]
                new_y += offset[1]
        return positions

        # for offset in offsets:
        #     x = self.p.x + offset[0]
        #     y = self.p.y + offset[1]
        #     if self.g.board[x][y].color != self.color:
        #         positions.append(Position(x, y))
        #         break
        #     x += offset[0]
        #     y += offset[1]
        # return positions

class Queen(Piece):
    def __str__(self) -> str:
        return "♕" if self.color == "white" else "♛"

    def get_possible_moves(self) -> list[Position]:
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
                if self.g.board[new_y][new_x] is None:
                    positions.append(Position(new_x, new_y))
                else:
                    if self.g.board[new_y][new_x].color != self.color:
                        positions.append(Position(new_x, new_y))
                    break
                new_x += offset[0]
                new_y += offset[1]

        # horizontal and vertical moves
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            dx, dy = direction
            x, y = self.p.x + dx, self.p.y + dy
            while 0 <= x <= 7 and 0 <= y <= 7:
                if self.g.board[y][x] is None:
                    positions.append(Position(x, y))
                else:
                    if self.g.board[y][x].color != self.color:
                        positions.append(Position(x, y))
                    break
                x += dx
                y += dy
        return positions


class King(Piece):
    def __str__(self) -> str:
        return "♔" if self.color == "white" else "♚"

    def get_possible_moves(self) -> list[Position]:
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
                    self.g.board[new_y][new_x] is None
                    or self.g.board[new_y][new_x].color != self.color
                ):
                    positions.append(Position(new_x, new_y))
        return positions
    