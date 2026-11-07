'''
This is a gui debugger to print a gameboard.
displays a pygame window and saves a .png file with the board.
'''

import argparse
import time

from gameboard import GameBoard, Line
from guiTools import C, drawGameboard
from solverTools import solve_board

parser = argparse.ArgumentParser(description="Solve the 5x6 Flow Free debug board.")
parser.add_argument("--debug", action="store_true", help="Display connection and disconnection debug output.")
args = parser.parse_args()

COLS = 5
ROWS = 6

# initialize board
gb = GameBoard(COLS, ROWS)

# add pieces
gb.addPiece(2, 1, C.YELLOW)
gb.addPiece(4, 6, C.YELLOW)
gb.addPiece(5, 1, C.RED)
gb.addPiece(5, 6, C.RED)
gb.addPiece(5, 2, C.GREEN)
gb.addPiece(3, 3, C.GREEN)
gb.addPiece(5, 3, C.BLUE)
gb.addPiece(3, 4, C.BLUE)

# add lines
gb.addLine(Line(C.YELLOW, [(2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 6), (3, 6), (4, 6)]))

start = time.process_time_ns()



print("Starting solve")
solve_board(gb, debug=args.debug)
end = time.process_time_ns()

if(gb.isSolved()):
    print("HURRAH! WE SOLVED IT!")
else:
    print("NOT SOLVED YET!?")

print("Time taken: " + str(end - start) + " ns")


drawGameboard(gb)
