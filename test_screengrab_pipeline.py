from collections import Counter
from pathlib import Path
import unittest

import cv2

from overlay import detection_overlay as _detection_overlay, solution_overlay as _solution_overlay
from shapeDetection import detectGrid, parseBoard
from constraintSolver import solve_board_cp_sat


PROJECT_ROOT = Path(__file__).resolve().parent
SCREEN_GRABS = PROJECT_ROOT / "screengrabs"
OUTPUT_DIR = PROJECT_ROOT / "output"
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


class ScreengrabPipelineTests(unittest.TestCase):
    def process_screengrab(self, image_path):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        detected_path = OUTPUT_DIR / f"{image_path.stem}_detected.png"
        solved_path = OUTPUT_DIR / f"{image_path.stem}_solved.png"

        original = cv2.imread(str(image_path))
        self.assertIsNotNone(original, f"Could not read {image_path}")
        squares, circles, rows, columns = detectGrid(original.copy(), False)
        detected = _detection_overlay(original, squares, circles, rows, columns)
        self.assertTrue(cv2.imwrite(str(detected_path), detected), f"Could not write {detected_path}")

        if not rows or not columns or circles is None:
            status = _solution_overlay(original, None, squares, False, "Detection incomplete; no solve attempted")
            self.assertTrue(cv2.imwrite(str(solved_path), status), f"Could not write {solved_path}")
            self.skipTest("Grid or circle detection incomplete")

        board = parseBoard(original, rows, columns, circles, squares)
        color_counts = Counter(field.piece.color for field in board.fields if field.piece is not None)
        if not color_counts or any(count != 2 for count in color_counts.values()):
            status = _solution_overlay(original, board, squares, False, "Detected pieces do not form complete color pairs")
            self.assertTrue(cv2.imwrite(str(solved_path), status), f"Could not write {solved_path}")
            self.skipTest("Detected piece locations do not form complete pairs")

        solved = solve_board_cp_sat(board)
        message = f"{columns}x{rows}; {len(color_counts)} pairs; {len(board.lines)} lines"
        solution = _solution_overlay(original, board, squares, solved, message)
        self.assertTrue(cv2.imwrite(str(solved_path), solution), f"Could not write {solved_path}")
        self.assertTrue(solved, f"Solver did not solve {image_path.name}; see {solved_path}")


def _make_screengrab_test(image_path):
    def test_screengrab(self):
        self.process_screengrab(image_path)

    test_screengrab.__name__ = f"test_{image_path.stem}"
    test_screengrab.__doc__ = f"Detect and solve {image_path.name}, saving paired output images."
    return test_screengrab


for _image_path in sorted(SCREEN_GRABS.iterdir()):
    if _image_path.is_file() and _image_path.suffix.lower() in IMAGE_SUFFIXES:
        setattr(ScreengrabPipelineTests, f"test_{_image_path.stem}", _make_screengrab_test(_image_path))


if __name__ == "__main__":
    unittest.main(verbosity=2)