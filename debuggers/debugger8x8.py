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
gb.addPiece(1, 6, C.RED)
gb.addPiece(7, 5, C.RED)
gb.addPiece(1, 2, C.GREEN)
gb.addPiece(7, 4, C.GREEN)
gb.addPiece(1, 7, C.BLUE)
gb.addPiece(4, 4, C.BLUE)
gb.addPiece(2, 2, C.YELLOW)
gb.addPiece(5, 7, C.YELLOW)
gb.addPiece(2, 4, C.ORANGE)
gb.addPiece(2, 7, C.ORANGE)
gb.addPiece(7, 8, C.CYAN)
gb.addPiece(8, 1, C.CYAN)
run_debugger(gb)