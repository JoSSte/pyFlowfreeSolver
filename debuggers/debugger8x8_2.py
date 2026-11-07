'''
This is a gui debugger to print a gameboard.
displays a pygame window and saves a .png file with the board.

The following files in the screengrabs folder are of the same level, but captured from Flow Free
  s7_screen_08_08.png
  s23_screen_08_08.jpg
  s23_screen_08_08_01_outside_first.jpg
  s23_screen_08_08_02_01_quickwins_first.jpg
  s23_screen_08_08_02_02_quickwins_first.jpg
  s23_screen_08_08_04_solved.jpg
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
gb.addPiece(5, 1, C.RED)
gb.addPiece(2, 8, C.RED)
gb.addPiece(7, 2, C.GREEN)
gb.addPiece(5, 3, C.GREEN)
gb.addPiece(5, 4, C.BLUE)
gb.addPiece(5, 6, C.BLUE)
gb.addPiece(8, 2, C.YELLOW)
gb.addPiece(6, 3, C.YELLOW)
gb.addPiece(4, 4, C.ORANGE)
gb.addPiece(5, 5, C.ORANGE)
gb.addPiece(5, 2, C.CYAN)
gb.addPiece(8, 3, C.CYAN)

#gb.addLine(Line(C.RED, [(5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 8)]))
#gb.addLine(Line(C.CYAN, [(5, 2), (4, 2), (3, 2), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (3, 7), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3)]))
#gb.addLine(Line(C.YELLOW, [(8, 2), (8, 1), (7, 1), (6, 1), (6, 2), (6, 3)]))
#gb.addLine(Line(C.GREEN, [(7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (6, 7), (5, 7), (4, 7), (4, 6), (3, 6), (3, 5), (3, 4), (3, 3), (4, 3), (5, 3)]))
run_debugger(gb, max_extra_steps=24)