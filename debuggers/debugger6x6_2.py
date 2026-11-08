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

run_debugger(gb)