"""Run the detector and solver on the s21 11x13 screenshot."""

from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import cv2

from debuggers.common import run_debugger
from shapeDetection import detectGrid, parseBoard


PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMAGE_PATH = PROJECT_ROOT / "screengrabs" / "s21_screen_11_13.jpg"

image = cv2.imread(str(IMAGE_PATH))
if image is None:
    raise FileNotFoundError(f"Could not read screenshot: {IMAGE_PATH}")

squares, circles, rows, columns = detectGrid(image.copy())
if rows != 13 or columns != 11 or circles is None:
    raise ValueError(
        f"Expected an 11x13 grid with detected dots; got {columns}x{rows} "
        f"and {0 if circles is None else len(circles)} dots"
    )

board = parseBoard(image, rows, columns, circles, squares)
color_counts = Counter(
    field.piece.color for field in board.fields if field.piece is not None
)
if len(color_counts) != 13 or any(count != 2 for count in color_counts.values()):
    raise ValueError(f"Expected 13 complete color pairs; detected {dict(color_counts)}")

print(f"Detected {columns}x{rows} grid and {len(color_counts)} color pairs from {IMAGE_PATH.name}")
run_debugger(board, max_extra_steps=18)
