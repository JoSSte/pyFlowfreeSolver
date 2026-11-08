'''
This is a gui debugger to print a gameboard.
displays a pygame window and saves a .png file with the board.
'''

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gameboard import GameBoard, Line
from guiTools import C
from debuggers.common import run_debugger

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

run_debugger(gb)
