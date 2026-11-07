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

COLS = 8
ROWS = 8

# initialize board
gb = GameBoard(COLS, ROWS)

# add pieces
gb.addPiece(7, 2, C.RED)
gb.addPiece(4, 8, C.RED)
gb.addPiece(6, 8, C.GREEN)
gb.addPiece(2, 4, C.GREEN)
gb.addPiece(2, 6, C.BLUE)
gb.addPiece(5, 8, C.BLUE)
gb.addPiece(5, 4, C.YELLOW)
gb.addPiece(8, 7, C.YELLOW)
gb.addPiece(8, 8, C.ORANGE)
gb.addPiece(3, 4, C.ORANGE)
gb.addPiece(1, 2, C.CYAN)
gb.addPiece(8, 3, C.CYAN)
gb.addPiece(3, 3, C.PINK)
gb.addPiece(7, 3, C.PINK)
run_debugger(gb)