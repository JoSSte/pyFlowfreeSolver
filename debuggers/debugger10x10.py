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
run_debugger(gb, max_extra_steps=18)