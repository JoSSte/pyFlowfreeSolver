from collections import defaultdict, deque
import math

from gameboard import Piece, Field, GameBoard, Line


def dist(f1: Field, f2: Field):
    c = max([f1.column, f2.column]) - min([f1.column, f2.column])
    r = max([f1.row, f2.row]) - min([f1.row, f2.row])
    d = int(math.sqrt(c**2 + r**2))
    return d


class FieldPair:
    def __init__(self, p1: Piece, p2: Piece):
        self.color = p1.color
        self.p1 = p1
        self.p2 = p2


def _color_name(color):
    color_names = {
        (255, 0, 0): "RED",
        (0, 141, 0): "GREEN",
        (12, 41, 254): "BLUE",
        (234, 224, 0): "YELLOW",
        (251, 137, 0): "ORANGE",
        (128, 0, 128): "PURPLE",
        (255, 10, 201): "PINK",
        (165, 42, 42): "BROWN",
        (0, 255, 255): "CYAN",
    }
    if isinstance(color, tuple):
        return color_names.get(color, str(color))
    return str(color)


def _neighbors(position, columns, rows):
    x, y = position
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 1 <= nx <= columns and 1 <= ny <= rows:
            yield (nx, ny)


def _candidate_paths(board: GameBoard, color, start, end, reserved, extra_steps=10):
    blocked = {
        (field.column, field.row)
        for field in board.fields
        if field.piece is not None and field.piece.color != color
    }
    blocked |= {
        (field.column, field.row)
        for field in board.fields
        if field.line is not None and field.line != color
    }
    blocked |= set(reserved)

    max_length = abs(start[0] - end[0]) + abs(start[1] - end[1]) + extra_steps
    results = []

    def dfs(current, path, seen):
        if len(path) > max_length:
            return
        if current == end:
            results.append(path[:])
            return

        for next_cell in _neighbors(current, board.columns, board.rows):
            if next_cell in seen or next_cell in blocked:
                continue
            if abs(next_cell[0] - end[0]) + abs(next_cell[1] - end[1]) > max_length - len(path):
                continue
            seen.add(next_cell)
            path.append(next_cell)
            dfs(next_cell, path, seen)
            path.pop()
            seen.remove(next_cell)

    dfs(start, [start], {start})
    return results


def _remove_path_from_board(board: GameBoard, color, path):
    board.lines = [line for line in board.lines if line.color != color or line.path != path]
    for x, y in path:
        field = board.getField(x, y)
        if field.piece is None and field.line == color:
            field.line = None
            field.occupied = False


def solve_board(board: GameBoard, max_extra_steps=10, debug=False):
    color_pairs = defaultdict(list)
    for field in board.fields:
        if field.piece is not None:
            color_pairs[field.piece.color].append((field.column, field.row))

    remaining = [
        color for color, positions in color_pairs.items()
        if len(positions) == 2 and not any(field.line == color for field in board.fields)
    ]
    reserved = {(field.column, field.row) for field in board.fields if field.line is not None}

    if not remaining:
        return board

    chosen_paths = {}

    def backtrack(colors_left, used_cells):
        if not colors_left:
            return True

        best_color = None
        best_paths = None
        for color in colors_left:
            start, end = color_pairs[color]
            paths = _candidate_paths(board, color, start, end, used_cells, max_extra_steps)
            if not paths:
                return False
            if best_paths is None or len(paths) < len(best_paths):
                best_color = color
                best_paths = paths

        for path in best_paths:
            next_used = set(used_cells)
            next_used.update(path)
            if debug:
                print(f"Trying {_color_name(best_color)} with line length {len(path)}")
            board.addLine(Line(best_color, path))
            chosen_paths[best_color] = path
            if backtrack([color for color in colors_left if color != best_color], next_used):
                if debug:
                    print(f"{_color_name(best_color)} connected with line length {len(path)}")
                return True
            if debug:
                print(f"{_color_name(best_color)} disconnected")
            _remove_path_from_board(board, best_color, path)
            del chosen_paths[best_color]

        return False

    backtrack(remaining, reserved)
    return board
