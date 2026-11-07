import unittest

from gameboard import GameBoard, Line
from guiTools import C
from solverTools import (
    _candidate_paths,
    _partial_board_failure,
    _priority_moves,
    _same_axis_short_paths,
    solve_board,
)


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


def build_8x8_quickwins_board():
    board = GameBoard(8, 8)
    color_pairs = {
        C.RED: [(5, 1), (2, 8)],
        C.GREEN: [(7, 2), (5, 3)],
        C.BLUE: [(5, 4), (5, 6)],
        C.YELLOW: [(8, 2), (6, 3)],
        C.ORANGE: [(4, 4), (5, 5)],
        C.CYAN: [(5, 2), (8, 3)],
    }
    for color, positions in color_pairs.items():
        for x, y in positions:
            board.addPiece(x, y, color)

    paths = [
        (C.RED, [(5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 8)]),
        (C.YELLOW, [(8, 2), (8, 1), (7, 1), (6, 1), (6, 2), (6, 3)]),
        (C.GREEN, [(7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (6, 7), (5, 7), (4, 7), (4, 6), (3, 6), (3, 5), (3, 4), (3, 3), (4, 3), (5, 3)]),
    ]
    for color, path in paths:
        board.addLine(Line(color, path))
    return board


class SolverTests(unittest.TestCase):
    def test_partial_board_rejects_separated_color_mates(self):
        board = GameBoard(3, 3)
        board.addPiece(1, 2, C.RED)
        board.addPiece(3, 2, C.RED)
        board.addLine(Line(C.BLUE, [(2, 1), (2, 2), (2, 3)]))

        failure = _partial_board_failure(board, {C.RED: [(1, 2), (3, 2)]}, [C.RED])

        self.assertIn("RED endpoints are disconnected", failure)

    def test_partial_board_rejects_enclosed_orphan_cell(self):
        board = GameBoard(5, 5)
        board.addPiece(1, 1, C.RED)
        board.addPiece(5, 5, C.RED)
        board.addLine(Line(C.CYAN, [(2, 2), (3, 2), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4), (2, 3)]))

        failure = _partial_board_failure(board, {C.RED: [(1, 1), (5, 5)]}, [C.RED])

        self.assertEqual(failure, "an empty region has no remaining color endpoint")

    def test_partial_board_rejects_single_cell_kink(self):
        board = GameBoard(3, 3)
        board.addPiece(3, 1, C.RED)
        board.addPiece(3, 3, C.RED)
        board.getField(1, 1).addLine(C.BLUE)
        board.getField(1, 3).addLine(C.BLUE)

        failure = _partial_board_failure(board, {C.RED: [(3, 1), (3, 3)]}, [C.RED])

        self.assertIn("cannot be part of a complete path", failure)

    def test_partial_board_rejects_orange_route_forcing_red_self_touch(self):
        board = GameBoard(10, 10)
        color_pairs = {
            C.RED: [(1, 6), (7, 5)],
            C.GREEN: [(1, 2), (7, 4)],
            C.BLUE: [(1, 7), (4, 4)],
            C.YELLOW: [(2, 2), (5, 7)],
            C.ORANGE: [(2, 4), (2, 7)],
            C.CYAN: [(7, 8), (8, 1)],
        }
        for color, positions in color_pairs.items():
            for x, y in positions:
                board.addPiece(x, y, color)
        board.addLine(Line(C.ORANGE, [(2, 4), (3, 4), (3, 5), (3, 6), (3, 7), (2, 7)]))

        failure = _partial_board_failure(
            board,
            color_pairs,
            [C.RED, C.GREEN, C.BLUE, C.YELLOW, C.CYAN],
        )

        self.assertIn("forced RED path touches itself", failure)

    def test_partial_board_rejects_shared_one_cell_bottleneck(self):
        board = GameBoard(3, 3)
        board.addPiece(1, 1, C.RED)
        board.addPiece(3, 1, C.RED)
        board.addPiece(1, 3, C.GREEN)
        board.addPiece(3, 3, C.GREEN)
        board.getField(2, 1).addLine(C.BLUE)
        board.getField(2, 3).addLine(C.BLUE)
        color_pairs = {
            C.RED: [(1, 1), (3, 1)],
            C.GREEN: [(1, 3), (3, 3)],
        }

        failure = _partial_board_failure(board, color_pairs, [C.RED, C.GREEN])

        self.assertIn("bottleneck cell", failure)

    def test_candidate_paths_do_not_touch_themselves(self):
        board = GameBoard(3, 3)
        paths = _candidate_paths(board, C.RED, (1, 1), (3, 3), set(), extra_steps=3)

        self.assertTrue(paths)
        for path in paths:
            self.assertEqual(len(path), len(set(path)))
            for index, cell in enumerate(path):
                for later_cell in path[index + 2:]:
                    distance = abs(cell[0] - later_cell[0]) + abs(cell[1] - later_cell[1])
                    self.assertNotEqual(distance, 1)

    def test_5x5_board_solves(self):
        board = build_5x5_board()
        solve_board(board)
        self.assertTrue(board.isSolved())
        self.assertEqual(len(board.lines), 5)

    def test_5x6_board_solves(self):
        board = build_5x6_board()
        solve_board(board)
        self.assertTrue(board.isSolved())
        self.assertEqual(len(board.lines), 4)

    def test_6x6_board_solves(self):
        board = build_6x6_board()
        solve_board(board)
        self.assertTrue(board.isSolved())
        self.assertEqual(len(board.lines), 5)

    def test_8x8_quickwins_board_solves_remaining_colors(self):
        board = build_8x8_quickwins_board()
        solve_board(board, max_extra_steps=18)
        self.assertTrue(board.isSolved())
        self.assertEqual(len(board.lines), 6)
        cyan_line = next(line for line in board.lines if line.color == C.CYAN)
        self.assertEqual(len(cyan_line.path), 21)

    def test_selects_diagonal_one_cell_connection_first(self):
        color_pairs = {
            C.RED: [(5, 1), (2, 8)],
            C.GREEN: [(7, 2), (5, 3)],
            C.BLUE: [(5, 4), (5, 6)],
            C.YELLOW: [(8, 2), (6, 3)],
            C.ORANGE: [(4, 4), (5, 5)],
            C.CYAN: [(5, 2), (8, 3)],
        }
        board = GameBoard(8, 8)
        for color, positions in color_pairs.items():
            for x, y in positions:
                board.addPiece(x, y, color)

        moves = _priority_moves(board, color_pairs, list(color_pairs), set())

        self.assertEqual(moves[0][0], C.ORANGE)
        self.assertEqual(len(moves[0][1]), 3)
        red_path = next(path for color, path in moves if color == C.RED)
        self.assertEqual(
            red_path,
            [(5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 8)],
        )
        blue_path = next(path for color, path in moves if color == C.BLUE)
        self.assertEqual(blue_path, [(5, 4), (6, 4), (6, 5), (6, 6), (5, 6)])

    def test_same_row_gap_prioritizes_straight_and_two_bend_paths(self):
        board = GameBoard(5, 5)
        paths = _same_axis_short_paths(board, (2, 3), (4, 3), set())

        self.assertEqual([len(path) for path in paths], [3, 5, 5])


if __name__ == "__main__":
    unittest.main()
