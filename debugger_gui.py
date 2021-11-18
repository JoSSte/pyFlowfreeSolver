'''
This is a gui debugger to print a gameboard.
displays a pygame window and saves a .png file with the board.
'''

from gameboard import GameBoard, Line
from guiTools import C, drawItAll

ROWS = 5
COLS = 5

# initialize board
gb = GameBoard(COLS, ROWS)

# add pieces
gb.addPiece(1, 1, C.RED)
gb.addPiece(2, 5, C.RED)
gb.addPiece(3, 1, C.GREEN)
gb.addPiece(2, 4, C.GREEN)
gb.addPiece(3, 2, C.BLUE)
gb.addPiece(3, 5, C.BLUE)
gb.addPiece(5, 1, C.YELLOW)
gb.addPiece(4, 4, C.YELLOW)
gb.addPiece(5, 2, C.ORANGE)
gb.addPiece(4, 5, C.ORANGE)

# add lines
gb.addLine(Line(C.RED, [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 5)]))
gb.addLine(Line(C.GREEN, [(3, 1), (2, 1), (2, 2), (2, 3), (2, 4)]))
# TODO: solve this tricky situation - skips intermediate cells...
gb.addLine(Line(C.BLUE, [(3, 2), (3, 5)]))
gb.addLine(Line(C.YELLOW, [(5, 1), (4, 1), (4, 2), (4, 3), (4, 4)]))
gb.addLine(Line(C.ORANGE, [(5, 2), (5, 3), (5, 4), (5, 5), (4, 5)]))

drawGameboard(gb)