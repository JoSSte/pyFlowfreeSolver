from gameboard import GameBoard, Line
from ortools.sat.python import cp_model


def solve_board_cp_sat(board: GameBoard, debug=False, on_update=None, max_time_seconds=60):
    color_pairs = {}
    for field in board.fields:
        if field.piece is not None:
            color_pairs.setdefault(field.piece.color, []).append((field.column, field.row))

    if not color_pairs or any(len(positions) != 2 for positions in color_pairs.values()):
        return False
    if any(field.line is not None for field in board.fields):
        raise ValueError("CP-SAT currently expects a board without pre-drawn lines")

    colors = list(color_pairs)
    cells = [(field.column, field.row) for field in board.fields]
    cell_index = {cell: index for index, cell in enumerate(cells)}
    cell_count = len(cells)
    model = cp_model.CpModel()

    assigned = {
        (color_index, cell): model.NewBoolVar(f"assigned_{color_index}_{cell}")
        for color_index in range(len(colors))
        for cell in range(cell_count)
    }
    for cell in range(cell_count):
        model.AddExactlyOne(assigned[color_index, cell] for color_index in range(len(colors)))

    color_arcs = {}
    for color_index, color in enumerate(colors):
        start, end = color_pairs[color]
        start_index = cell_index[start]
        end_index = cell_index[end]
        model.Add(assigned[color_index, start_index] == 1)
        model.Add(assigned[color_index, end_index] == 1)

        arcs = [
            (cell, cell, assigned[color_index, cell].Not())
            for cell in range(cell_count)
        ]
        directed_edges = {}
        for cell in cells:
            first = cell_index[cell]
            for neighbor in ((cell[0] + 1, cell[1]), (cell[0], cell[1] + 1)):
                if neighbor not in cell_index:
                    continue
                second = cell_index[neighbor]
                forward = model.NewBoolVar(f"arc_{color_index}_{first}_{second}")
                backward = model.NewBoolVar(f"arc_{color_index}_{second}_{first}")
                model.Add(forward <= assigned[color_index, first])
                model.Add(forward <= assigned[color_index, second])
                model.Add(backward <= assigned[color_index, first])
                model.Add(backward <= assigned[color_index, second])
                model.Add(assigned[color_index, first] + assigned[color_index, second] <= 1 + forward + backward)
                arcs.extend(((first, second, forward), (second, first, backward)))
                directed_edges[first, second] = forward
                directed_edges[second, first] = backward

        dummy = cell_count
        close_to_dummy = model.NewBoolVar(f"close_{color_index}")
        close_to_start = model.NewBoolVar(f"start_{color_index}")
        model.Add(close_to_dummy == 1)
        model.Add(close_to_start == 1)
        arcs.extend(((end_index, dummy, close_to_dummy), (dummy, start_index, close_to_start)))
        model.AddCircuit(arcs)
        color_arcs[color] = (start_index, end_index, directed_edges)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_time_seconds
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        if debug:
            print(f"CP-SAT did not find a solution: {solver.StatusName(status)}")
        return False

    if debug:
        print(
            f"CP-SAT found a solution: {solver.StatusName(status)}; "
            f"branches={solver.NumBranches()}; conflicts={solver.NumConflicts()}"
        )

    solved_paths = []
    for color in colors:
        start_index, end_index, directed_edges = color_arcs[color]
        path = [cells[start_index]]
        current = start_index
        while current != end_index:
            next_cells = [
                second
                for (first, second), arc in directed_edges.items()
                if first == current and solver.BooleanValue(arc)
            ]
            if len(next_cells) != 1:
                return False
            current = next_cells[0]
            path.append(cells[current])
            if len(path) > cell_count:
                return False
        solved_paths.append((color, path))

    for color, path in solved_paths:
        board.addLine(Line(color, path))
        if on_update is not None:
            on_update(board, f"{color} connected ({len(path)} cells)")
    return board.isSolved()
