'''
This is a gui debugger to print a gameboard.
displays a pygame window and saves a .png file with the board.
'''

import argparse
import time

from gameboard import GameBoard, Line
from guiTools import C, drawGameboard
from solverTools import solve_board

parser = argparse.ArgumentParser(description="Solve the 6x6 Flow Free debug board.")
parser.add_argument("--debug", action="store_true", help="Display connection and disconnection debug output.")
args = parser.parse_args()

COLS = 6
ROWS = 6

# initialize board
gb = GameBoard(COLS, ROWS)

# add pieces
gb.addPiece(3, 3, C.RED)
gb.addPiece(5, 5, C.RED)
gb.addPiece(4, 4, C.GREEN)
gb.addPiece(2, 5, C.GREEN)
gb.addPiece(6, 5, C.BLUE)
gb.addPiece(4, 6, C.BLUE)
gb.addPiece(2, 3, C.YELLOW)
gb.addPiece(6, 4, C.YELLOW)
gb.addPiece(6, 1, C.ORANGE)
gb.addPiece(4, 5, C.ORANGE)

#drawGameboard(gb)


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