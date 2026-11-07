import unittest

from gameboard import GameBoard, Line
from guiTools import C
from solverTools import solve_board


def build_5x6_board():
    board = GameBoard(5, 6)
    board.addPiece(2, 1, C.YELLOW)
    board.addPiece(4, 6, C.YELLOW)
    board.addPiece(5, 1, C.RED)
    board.addPiece(5, 6, C.RED)
    board.addPiece(5, 2, C.GREEN)
    board.addPiece(3, 3, C.GREEN)
    board.addPiece(5, 3, C.BLUE)
    board.addPiece(3, 4, C.BLUE)
    board.addLine(Line(C.YELLOW, [(2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 6), (3, 6), (4, 6)]))
    return board


def build_6x6_board():
    board = GameBoard(6, 6)
    board.addPiece(3, 3, C.RED)
    board.addPiece(5, 5, C.RED)
    board.addPiece(4, 4, C.GREEN)
    board.addPiece(2, 5, C.GREEN)
    board.addPiece(6, 5, C.BLUE)
    board.addPiece(4, 6, C.BLUE)
    board.addPiece(2, 3, C.YELLOW)
    board.addPiece(6, 4, C.YELLOW)
    board.addPiece(6, 1, C.ORANGE)
    board.addPiece(4, 5, C.ORANGE)
    return board


def build_5x5_board():
    board = GameBoard(5, 5)
    board.addPiece(1, 1, C.RED)
    board.addPiece(2, 5, C.RED)
    board.addPiece(3, 1, C.GREEN)
    board.addPiece(2, 4, C.GREEN)
    board.addPiece(3, 2, C.BLUE)
    board.addPiece(3, 5, C.BLUE)
    board.addPiece(5, 1, C.YELLOW)
    board.addPiece(4, 4, C.YELLOW)
    board.addPiece(5, 2, C.ORANGE)
    board.addPiece(4, 5, C.ORANGE)

    board.addLine(Line(C.RED, [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 5)]))
    board.addLine(Line(C.GREEN, [(3, 1), (2, 1), (2, 2), (2, 3), (2, 4)]))
    board.addLine(Line(C.BLUE, [(3, 2), (3, 3), (3, 4), (3, 5)]))
    board.addLine(Line(C.YELLOW, [(5, 1), (4, 1), (4, 2), (4, 3), (4, 4)]))
    board.addLine(Line(C.ORANGE, [(5, 2), (5, 3), (5, 4), (5, 5), (4, 5)]))
    return board


class SolverTests(unittest.TestCase):
    def test_5x5_board_solves(self):
        board = build_5x5_board()
        solve_board(board)
        self.assertTrue(board.isSolved())
        self.assertEqual(5, len(board.lines))

    def test_5x6_board_solves(self):
        board = build_5x6_board()
        solve_board(board)
        self.assertTrue(board.isSolved())
        self.assertEqual(4, len(board.lines))

    def test_6x6_board_solves(self):
        board = build_6x6_board()
        solve_board(board)
        self.assertTrue(board.isSolved())
        self.assertEqual(5, len(board.lines))


if __name__ == "__main__":
    unittest.main()
