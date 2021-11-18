'''
This is a gui debugger to print a gameboard.
displays a pygame window and saves a .png file with the board.
'''

from gameboard import GameBoard, Line
from guiTools import C, drawGameboard

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


if(gb.isSolved()):
    print("HURRAH! WE SOLVED IT!")
else:
    print("NOT SOLVED YET!?")

drawGameboard(gb)