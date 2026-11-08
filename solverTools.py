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
        (0, 255, 0): "LIME",
        (12, 41, 254): "BLUE",
        (234, 224, 0): "YELLOW",
        (251, 137, 0): "ORANGE",
        (128, 0, 128): "PURPLE",
        (255, 10, 201): "PINK",
        (165, 42, 42): "BROWN",
        (160, 138, 81): "TAN",
        (159, 158, 189): "LAVENDER",
        (255, 255, 255): "WHITE",
        (0, 255, 255): "CYAN",
    }
    try:
        rgb = tuple(int(channel) for channel in color)
    except (TypeError, ValueError):
        return str(color)
    if len(rgb) != 3:
        return str(rgb)
    if rgb in color_names:
        return color_names[rgb]

    closest = min(
        color_names,
        key=lambda candidate: sum((rgb[index] - candidate[index]) ** 2 for index in range(3)),
    )
    distance_squared = sum((rgb[index] - closest[index]) ** 2 for index in range(3))
    if distance_squared <= 30**2:
        return color_names[closest]
    return f"RGB{rgb}"


def _neighbors(position, columns, rows):
    x, y = position
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 1 <= nx <= columns and 1 <= ny <= rows:
            yield (nx, ny)


def _touches_existing_path(position, previous, seen, board):
    return any(
        neighbor in seen and neighbor != previous
        for neighbor in _neighbors(position, board.columns, board.rows)
    )


def _can_extend_path(next_cell, current, end, path, seen, blocked, max_length, board):
    if next_cell in seen or next_cell in blocked:
        return False
    if _touches_existing_path(next_cell, current, seen, board):
        return False
    distance_to_end = abs(next_cell[0] - end[0]) + abs(next_cell[1] - end[1])
    return distance_to_end <= max_length - len(path)


def _candidate_paths(board: GameBoard, color, start, end, reserved, extra_steps=10, limit=None,
                     max_length=None):
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

    step_cap = abs(start[0] - end[0]) + abs(start[1] - end[1]) + extra_steps
    max_length = step_cap if max_length is None else min(max_length, step_cap)
    results = []

    def dfs(current, path, seen):
        if limit is not None and len(results) >= limit:
            return
        if len(path) > max_length:
            return
        if current == end:
            results.append(path[:])
            return

        for next_cell in _neighbors(current, board.columns, board.rows):
            if not _can_extend_path(next_cell, current, end, path, seen, blocked, max_length, board):
                continue
            seen.add(next_cell)
            path.append(next_cell)
            dfs(next_cell, path, seen)
            path.pop()
            seen.remove(next_cell)

    dfs(start, [start], {start})
    return results


def _straightness_key(path):
    runs = []
    previous_direction = None
    run_length = 0
    for current, following in zip(path, path[1:]):
        direction = (following[0] - current[0], following[1] - current[1])
        if direction == previous_direction:
            run_length += 1
        else:
            if run_length:
                runs.append(run_length)
            previous_direction = direction
            run_length = 1
    if run_length:
        runs.append(run_length)
    return max(runs, default=0), sum(run * run for run in runs), -len(runs)


def _order_candidate_paths(paths):
    if len(paths) < 2:
        return list(paths)

    remaining = list(paths)
    shortest_index = min(
        range(len(remaining)),
        key=lambda index: (len(remaining[index]), tuple(-score for score in _straightness_key(remaining[index]))),
    )
    ordered = [remaining.pop(shortest_index)]

    if remaining:
        straightest_index = max(
            range(len(remaining)),
            key=lambda index: (_straightness_key(remaining[index]), -len(remaining[index])),
        )
        ordered.append(remaining.pop(straightest_index))

    remaining.sort(key=lambda path: (len(path), tuple(-score for score in _straightness_key(path))))
    ordered.extend(remaining)
    return ordered


def _reachable_cells(board, start, allowed_cells):
    reachable = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in _neighbors(current, board.columns, board.rows):
            if neighbor in allowed_cells and neighbor not in reachable:
                reachable.add(neighbor)
                queue.append(neighbor)
    return reachable


def _pair_connectivity_failure(board, color_pairs, remaining, open_cells):
    for color in remaining:
        start, end = color_pairs[color]
        other_endpoints = {
            position
            for other_color in remaining
            if other_color != color
            for position in color_pairs[other_color]
        }
        if end not in _reachable_cells(board, start, open_cells - other_endpoints):
            return f"{_color_name(color)} endpoints are disconnected"
    return None


def _orphan_region_failure(board, open_cells, endpoints):
    unvisited = set(open_cells)
    while unvisited:
        component = set()
        queue = deque([unvisited.pop()])
        while queue:
            current = queue.popleft()
            component.add(current)
            for neighbor in _neighbors(current, board.columns, board.rows):
                if neighbor in unvisited:
                    unvisited.remove(neighbor)
                    queue.append(neighbor)
        if not component.intersection(endpoints):
            return "an empty region has no remaining color endpoint"
    return None


def _cell_degree_failure(board, open_cells):
    for field in board.fields:
        position = (field.column, field.row)
        if position not in open_cells:
            continue
        degree = sum(neighbor in open_cells for neighbor in _neighbors(position, board.columns, board.rows))
        if field.piece is None and degree < 2:
            return f"empty cell {position} cannot be part of a complete path"
        if field.piece is not None and degree < 1:
            return f"endpoint {position} has no available path neighbor"
    return None


def _components_without_cell(board, open_cells, cut_cell):
    labels = {}
    component_id = 0
    for cell in open_cells:
        if cell == cut_cell or cell in labels:
            continue
        queue = deque([cell])
        labels[cell] = component_id
        while queue:
            current = queue.popleft()
            for neighbor in _neighbors(current, board.columns, board.rows):
                if neighbor != cut_cell and neighbor in open_cells and neighbor not in labels:
                    labels[neighbor] = component_id
                    queue.append(neighbor)
        component_id += 1
    return labels


def _bottleneck_failure(board, color_pairs, remaining, open_cells):
    if len(remaining) < 2:
        return None
    for cut_cell in open_cells:
        components = _components_without_cell(board, open_cells, cut_cell)
        crossing_colors = sum(
            components.get(color_pairs[color][0]) != components.get(color_pairs[color][1])
            for color in remaining
        )
        if crossing_colors > 1:
            return f"bottleneck cell {cut_cell} is needed by multiple color pairs"
    return None


def _build_forced_neighbors(board, open_cells):
    forced_neighbors = {cell: set() for cell in open_cells}
    for field in board.fields:
        position = (field.column, field.row)
        if position not in open_cells or field.piece is not None:
            continue
        available = [
            neighbor
            for neighbor in _neighbors(position, board.columns, board.rows)
            if neighbor in open_cells
        ]
        if len(available) == 2:
            for neighbor in available:
                forced_neighbors[position].add(neighbor)
                forced_neighbors[neighbor].add(position)
    return forced_neighbors


def _forced_degree_failure(board, forced_neighbors):
    for cell, neighbors in forced_neighbors.items():
        field = board.getField(*cell)
        required_degree = 1 if field.piece is not None else 2
        if len(neighbors) > required_degree:
            return f"forced paths require too many connections at {cell}"
    return None


def _forced_components(forced_neighbors):
    unvisited = set(forced_neighbors)
    while unvisited:
        component = set()
        queue = deque([unvisited.pop()])
        while queue:
            current = queue.popleft()
            component.add(current)
            for neighbor in forced_neighbors[current]:
                if neighbor in unvisited:
                    unvisited.remove(neighbor)
                    queue.append(neighbor)
        yield component


def _forced_component_failure(board, color_pairs, remaining, forced_neighbors, component):
    edge_count = sum(len(forced_neighbors[cell]) for cell in component) // 2
    if edge_count >= len(component):
        return "forced path cells create a loop"

    component_colors = {
        color
        for color in remaining
        if any(endpoint in component for endpoint in color_pairs[color])
    }
    if len(component_colors) > 1:
        return "forced path would connect different colors"

    for cell in component:
        for neighbor in _neighbors(cell, board.columns, board.rows):
            if neighbor in component and neighbor not in forced_neighbors[cell]:
                color = next(iter(component_colors), "line")
                return f"forced {_color_name(color)} path touches itself"
    return None


def _forced_path_failure(board, color_pairs, remaining, open_cells):
    forced_neighbors = _build_forced_neighbors(board, open_cells)
    failure = _forced_degree_failure(board, forced_neighbors)
    if failure is not None:
        return failure
    for component in _forced_components(forced_neighbors):
        failure = _forced_component_failure(
            board, color_pairs, remaining, forced_neighbors, component
        )
        if failure is not None:
            return failure
    return None


def _partial_board_failure(board, color_pairs, colors_left):
    remaining = set(colors_left)
    open_cells = {
        (field.column, field.row)
        for field in board.fields
        if field.line is None and (field.piece is None or field.piece.color in remaining)
    }
    if not remaining:
        return "unfilled cells remain without any unconnected colors" if open_cells else None

    endpoints = {position for color in remaining for position in color_pairs[color]}
    failure = _pair_connectivity_failure(board, color_pairs, remaining, open_cells)
    if failure is not None:
        return failure
    failure = _orphan_region_failure(board, open_cells, endpoints)
    if failure is not None:
        return failure
    failure = _cell_degree_failure(board, open_cells)
    if failure is not None:
        return failure
    failure = _forced_path_failure(board, color_pairs, remaining, open_cells)
    if failure is not None:
        return failure
    return _bottleneck_failure(board, color_pairs, remaining, open_cells)


def _remove_path_from_board(board: GameBoard, color, path):
    board.lines = [line for line in board.lines if line.color != color or line.path != path]
    for x, y in path:
        field = board.getField(x, y)
        if field.piece is None and field.line == color:
            field.line = None
            field.occupied = False


def _diagonal_quick_paths(board, start, end, reserved):
    if abs(start[0] - end[0]) != 1 or abs(start[1] - end[1]) != 1:
        return []

    paths = []
    for middle in ((start[0], end[1]), (end[0], start[1])):
        field = board.getField(*middle)
        if middle not in reserved and field.piece is None and field.line is None:
            paths.append([start, middle, end])
    return paths


def _path_is_available(board, path, endpoints, reserved):
    for cell in path:
        if cell in endpoints:
            continue
        x, y = cell
        if not (1 <= x <= board.columns and 1 <= y <= board.rows):
            return False
        field = board.getField(x, y)
        if cell in reserved or field.piece is not None or field.line is not None:
            return False
    return True


def _edge_route_paths(board, start, end, reserved):
    boundary = (
        [(column, 1) for column in range(1, board.columns + 1)]
        + [(board.columns, row) for row in range(2, board.rows + 1)]
        + [(column, board.rows) for column in range(board.columns - 1, 0, -1)]
        + [(1, row) for row in range(board.rows - 1, 1, -1)]
    )
    if start not in boundary or end not in boundary:
        return []

    start_index = boundary.index(start)
    end_index = boundary.index(end)
    routes = []
    for direction in (1, -1):
        path = [start]
        index = start_index
        while index != end_index:
            index = (index + direction) % len(boundary)
            path.append(boundary[index])
        routes.append(path)

    endpoints = {start, end}
    available_routes = []
    seen_routes = set()
    for path in routes:
        path_key = tuple(path)
        if path_key in seen_routes:
            continue
        seen_routes.add(path_key)
        if _path_is_available(board, path, endpoints, reserved):
            available_routes.append(path)
    return sorted(available_routes, key=len)


def _same_axis_short_paths(board, start, end, reserved):
    if start[0] == end[0] and abs(start[1] - end[1]) == 2:
        step = 1 if end[1] > start[1] else -1
        middle = (start[0], start[1] + step)
        paths = [[start, middle, end]]
        for side_offset in (-1, 1):
            side_column = start[0] + side_offset
            paths.append([
                start,
                (side_column, start[1]),
                (side_column, middle[1]),
                (side_column, end[1]),
                end,
            ])
    elif start[1] == end[1] and abs(start[0] - end[0]) == 2:
        step = 1 if end[0] > start[0] else -1
        middle = (start[0] + step, start[1])
        paths = [[start, middle, end]]
        for side_offset in (-1, 1):
            side_row = start[1] + side_offset
            paths.append([
                start,
                (start[0], side_row),
                (middle[0], side_row),
                (end[0], side_row),
                end,
            ])
    else:
        return []

    endpoints = {start, end}
    return [
        path
        for path in paths
        if _path_is_available(board, path, endpoints, reserved)
    ]


def _priority_moves(board, color_pairs, colors_left, reserved):
    moves = []
    for color in colors_left:
        start, end = color_pairs[color]
        moves.extend(
            (color, path)
            for path in _diagonal_quick_paths(board, start, end, reserved)
        )
    for color in colors_left:
        start, end = color_pairs[color]
        moves.extend(
            (color, path)
            for path in _edge_route_paths(board, start, end, reserved)
        )
    for color in colors_left:
        start, end = color_pairs[color]
        moves.extend(
            (color, path)
            for path in _same_axis_short_paths(board, start, end, reserved)
        )
    return moves


COUNT_LIMIT = 64


def _area_length_cap(board, color_pairs, colors_left, color, used_cells):
    """Upper bound on the number of cells a path for ``color`` can use.

    The path lies inside the open region containing its endpoints. Every other
    remaining color with endpoints in that region needs at least
    ``manhattan + 1`` of those cells, so the rest is the most this path can
    take. This never excludes a valid route and tightens as the board fills.
    """
    start, _ = color_pairs[color]
    open_cells = {
        (field.column, field.row)
        for field in board.fields
        if (field.column, field.row) not in used_cells and field.line is None
        and (field.piece is None or field.piece.color in colors_left)
    }
    region = _reachable_cells(board, start, open_cells)
    reserved_by_others = 0
    for other in colors_left:
        if other == color:
            continue
        a, b = color_pairs[other]
        if a in region and b in region:
            reserved_by_others += abs(a[0] - b[0]) + abs(a[1] - b[1]) + 1
    return len(region) - reserved_by_others


def _color_paths(board, color_pairs, colors_left, color, used_cells, max_extra_steps,
                 limit=COUNT_LIMIT):
    """Return the candidate paths for a color.

    Paths are bounded by the area-based cap, which is exact, and enumeration
    stops at ``limit``. Only if a color has too many routes to enumerate does
    it fall back to the tighter ``max_extra_steps`` cap.
    """
    start, end = color_pairs[color]
    area_cap = _area_length_cap(board, color_pairs, colors_left, color, used_cells)
    unbounded = board.columns * board.rows
    paths = _candidate_paths(board, color, start, end, used_cells, unbounded, limit, area_cap)
    if len(paths) < limit:
        return paths
    return _candidate_paths(board, color, start, end, used_cells, max_extra_steps, None, area_cap)


def _select_color(board, color_pairs, colors_left, used_cells, max_extra_steps):
    """Pick the most constrained color (fewest candidate paths).

    Counting stops early once a color cannot beat the current best, so only the
    chosen color has its full candidate list enumerated.
    """
    best_color = None
    best_paths = None
    for color in colors_left:
        limit = COUNT_LIMIT if best_paths is None else len(best_paths)
        start, end = color_pairs[color]
        area_cap = _area_length_cap(board, color_pairs, colors_left, color, used_cells)
        paths = _candidate_paths(
            board, color, start, end, used_cells, board.columns * board.rows, limit, area_cap
        )
        if not paths:
            return None, None
        if best_paths is None or len(paths) < len(best_paths):
            best_color, best_paths = color, paths
            if len(paths) == 1:
                break
    if len(best_paths) >= COUNT_LIMIT:
        best_paths = _color_paths(
            board, color_pairs, colors_left, best_color, used_cells, max_extra_steps, COUNT_LIMIT
        )
    return best_color, _order_candidate_paths(best_paths)


def _report_event(debug, on_update, board, debug_message, gui_message):
    if debug:
        print(debug_message)
    if on_update is not None:
        on_update(board, gui_message)


def _try_candidate(board, color_pairs, colors_left, used_cells, color, path,
                   max_extra_steps, debug, on_update, failed_states):
    next_used = used_cells | set(path)
    next_colors = [remaining_color for remaining_color in colors_left if remaining_color != color]
    color_name = _color_name(color)
    length = len(path)

    board.addLine(Line(color, path))
    _report_event(
        debug, on_update, board,
        f"Trying {color_name} with line length {length}",
        f"Trying {color_name} ({length} cells)",
    )
    failure = _partial_board_failure(board, color_pairs, next_colors)
    if failure is not None:
        _report_event(debug, on_update, board, f"Pruned {color_name}: {failure}", f"Pruned: {failure}")
        solved = False
    else:
        solved = _search_paths(
            board, color_pairs, next_colors, next_used, max_extra_steps, debug, on_update,
            failed_states,
        )

    if solved:
        _report_event(
            debug, on_update, board,
            f"{color_name} connected with line length {length}",
            f"{color_name} connected ({length} cells)",
        )
        return True

    _report_event(debug, on_update, board, f"{color_name} disconnected", f"{color_name} disconnected")
    _remove_path_from_board(board, color, path)
    return False


def _search_paths(board, color_pairs, colors_left, used_cells, max_extra_steps, debug, on_update,
                  failed_states=None):
    if not colors_left:
        return _partial_board_failure(board, color_pairs, colors_left) is None

    # The remaining sub-problem depends only on which cells are occupied, so a
    # state that failed once fails again no matter which order produced it.
    if failed_states is None:
        failed_states = set()
    state_key = frozenset(used_cells)
    if state_key in failed_states:
        _report_event(debug, on_update, board, "Skipping already-failed state", "Skipped known dead end")
        return False

    # Branch on a single color: every solution must contain some path for it,
    # so this stays complete while avoiding re-exploring color permutations.
    # Colors with a "quick win" route (diagonal, edge, short straight) are
    # branched on first; otherwise pick the most constrained color.
    quick_moves = _priority_moves(board, color_pairs, colors_left, used_cells)
    if quick_moves:
        color = quick_moves[0][0]
        paths = _color_paths(board, color_pairs, colors_left, color, used_cells, max_extra_steps)
        paths = _order_candidate_paths(paths) if paths else None
        if paths is None:
            color = None
    else:
        color, paths = _select_color(board, color_pairs, colors_left, used_cells, max_extra_steps)
    if color is not None:
        priority = [path for move_color, path in quick_moves if move_color == color]
        seen = set()
        for path in priority + paths:
            key = tuple(path)
            if key in seen:
                continue
            seen.add(key)
            if _try_candidate(
                board, color_pairs, colors_left, used_cells, color, path,
                max_extra_steps, debug, on_update, failed_states,
            ):
                return True

    failed_states.add(state_key)
    return False


def solve_board(board: GameBoard, max_extra_steps=10, debug=False, on_update=None):
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

    # Widen the path-length cap when a search fails: a too-tight cap can
    # exclude the only valid route for a color.
    open_cells = sum(field.line is None for field in board.fields)
    extra_steps = max_extra_steps
    while True:
        if _search_paths(board, color_pairs, remaining, reserved, extra_steps, debug, on_update, set()):
            break
        if extra_steps >= open_cells:
            break
        extra_steps = min(open_cells, extra_steps * 2)
        _report_event(
            debug, on_update, board,
            f"Retrying with max_extra_steps={extra_steps}",
            f"Widening path cap to {extra_steps}",
        )
    return board
