from gameboard import Piece, Field, GameBoard, Line
import math


def dist(f1: Field, f2: Field):
    c = max([f1.column, f2.column]) - min([f1.column, f2.column])
    r = max([f1.row, f2.row]) - min([f1.row, f2.row])
    d = int(math.sqrt(c**2 + r**2))
    return d

class FieldPair:
    def __init__(self, p1:Piece, p2: Piece):
        self.color = p1.color
        self.p1 = p1
        self.p2 = p2
