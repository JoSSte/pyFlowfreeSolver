import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from guiTools import LiveGameboard, drawGameboard
from constraintSolver import solve_board_cp_sat
from solverTools import solve_board


def run_debugger(board, max_extra_steps=10):
    parser = argparse.ArgumentParser(
        description=f"Solve the {board.columns}x{board.rows} Flow Free debug board."
    )
    parser.add_argument("--debug", action="store_true", help="Display solver debug output.")
    parser.add_argument("--gui", action="store_true", help="Show the solver's progress in a live window.")
    parser.add_argument("--dfs", action="store_true", help="Use the path-search solver instead of CP-SAT.")
    args = parser.parse_args()

    start = time.process_time_ns()
    print("Starting solve")
    live_gui = LiveGameboard(board) if args.gui else None
    on_update = live_gui.update if live_gui else None
    if args.dfs:
        solve_board(board, max_extra_steps=max_extra_steps, debug=args.debug, on_update=on_update)
    else:
        solve_board_cp_sat(board, debug=args.debug, on_update=on_update)
    end = time.process_time_ns()

    solved = board.isSolved()
    print("HURRAH! WE SOLVED IT!" if solved else "NOT SOLVED YET!?")
    print("Time taken: " + str(end - start) + " ns")

    if live_gui:
        live_gui.finish(board, solved)
    else:
        drawGameboard(board)

    return board
