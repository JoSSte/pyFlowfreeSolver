'''
This is a gui debugger to print a gameboard.
displays a pygame window and saves a .png file with the board.
'''

import time

from gameboard import GameBoard, Line
from guiTools import C, drawGameboard
from solverTools import solve_board

COLS = 10
ROWS = 10

# initialize board
gb = GameBoard(COLS, ROWS)

# add pieces
gb.addPiece(10, 10, C.RED)
gb.addPiece( 3,  7, C.RED)
gb.addPiece( 2,  9, C.GREEN)
gb.addPiece( 6,  5, C.GREEN)
gb.addPiece( 9,  5, C.BLUE)
gb.addPiece(10,  9, C.BLUE)
gb.addPiece( 3,  4, C.YELLOW)
gb.addPiece( 8,  3, C.YELLOW)
gb.addPiece( 2,  5, C.ORANGE)
gb.addPiece( 4,  9, C.ORANGE)
gb.addPiece( 7,  5, C.PURPLE)
gb.addPiece( 4,  7, C.PURPLE)
gb.addPiece( 2,  4, C.CYAN)
gb.addPiece( 9,  4, C.CYAN)
gb.addPiece( 6,  6, C.PINK)
gb.addPiece( 5,  7, C.PINK)
gb.addPiece( 2, 10, C.BROWN)
gb.addPiece(10,  8, C.BROWN)
start = time.process_time_ns()



print("Starting solve")
solve_board(gb)
end = time.process_time_ns()

if(gb.isSolved()):
    print("HURRAH! WE SOLVED IT!")
else:
    print("NOT SOLVED YET!?")

print("Time taken: " + str(end - start) + " ns")


drawGameboard(gb)