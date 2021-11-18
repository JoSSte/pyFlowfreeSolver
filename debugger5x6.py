'''
This is a gui debugger to print a gameboard.
displays a pygame window and saves a .png file with the board.
'''

from gameboard import GameBoard, Line
from guiTools import C, drawGameboard


COLS = 5
ROWS = 6

# initialize board
gb = GameBoard(COLS, ROWS)

# add pieces
gb.addPiece(2, 1, C.YELLOW)
gb.addPiece(4, 6, C.YELLOW)
gb.addPiece(5, 1, C.RED)
gb.addPiece(5, 6, C.RED)
#gb.addPiece(5, 2, C.GREEN)
gb.addPiece(3, 3, C.GREEN)
gb.addPiece(5, 3, C.BLUE)
gb.addPiece(3, 4, C.BLUE)

# add lines
gb.addLine(Line(C.YELLOW, [(2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 6), (3, 6), (4, 6)]))

if(gb.isSolved()):
    print("HURRAH! WE SOLVED IT!")
else:
    print("NOT SOLVED YET!?")

drawGameboard(gb)
