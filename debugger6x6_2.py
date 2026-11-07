'''
This is a gui debugger to print a gameboard.
displays a pygame window and saves a .png file with the board.
'''

from gameboard import GameBoard, Line
from guiTools import C, drawGameboard
from solverTools import solve_board

COLS = 6
ROWS = 6

# initialize board
gb = GameBoard(COLS, ROWS)

# add pieces
gb.addPiece(4, 1, C.RED)
gb.addPiece(5, 2, C.RED)
gb.addPiece(2, 1, C.GREEN)
gb.addPiece(3, 5, C.GREEN)
gb.addPiece(5, 1, C.BLUE)
gb.addPiece(6, 4, C.BLUE)
gb.addPiece(1, 6, C.YELLOW)
gb.addPiece(6, 5, C.YELLOW)
gb.addPiece(3, 1, C.ORANGE)
gb.addPiece(4, 5, C.ORANGE)
gb.addPiece(2, 2, C.CYAN)
gb.addPiece(4, 4, C.CYAN)

solve_board(gb)

if(gb.isSolved()):
    print("HURRAH! WE SOLVED IT!")
else:
    print("NOT SOLVED YET!?")

drawGameboard(gb)