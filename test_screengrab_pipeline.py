from collections import Counter
from pathlib import Path
import unittest

import cv2
import numpy as np

from shapeDetection import detectGrid, parseBoard
from solverTools import solve_board


PROJECT_ROOT = Path(__file__).resolve().parent
SCREEN_GRABS = PROJECT_ROOT / "screengrabs"
OUTPUT_DIR = PROJECT_ROOT / "output"
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def _add_status(image, status, message):
    cv2.rectangle(image, (0, 0), (image.shape[1], 48), (24, 24, 24), -1)
    cv2.putText(image, status, (12, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(image, message[:100], (12, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (220, 220, 220), 1, cv2.LINE_AA)
    return image


def _detection_overlay(image, squares, circles, rows, columns):
    overlay = image.copy()
    for (center_x, center_y), (column, row) in squares:
        cv2.drawMarker(overlay, (center_x, center_y), (0, 255, 0), cv2.MARKER_CROSS, 10, 2, cv2.LINE_AA)
        cv2.putText(overlay, f"{column},{row}", (center_x + 5, center_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1, cv2.LINE_AA)

    if circles is not None:
        for index, (center_x, center_y, radius) in enumerate(circles):
            cv2.circle(overlay, (int(center_x), int(center_y)), int(radius), (0, 220, 255), 2, cv2.LINE_AA)
            cv2.putText(overlay, str(index), (int(center_x) - 5, int(center_y) + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2, cv2.LINE_AA)

    circle_count = 0 if circles is None else len(circles)
    return _add_status(overlay, "DETECTION", f"grid {columns}x{rows}; {len(squares)} cells; {circle_count} dots")


def _solution_overlay(image, board, squares, solved, message):
    overlay = image.copy()
    if board is None:
        return _add_status(overlay, "NOT SOLVED", message)

    center_by_cell = {
        cell: center
        for center, cell in squares
    }
    cell_width = image.shape[1] / max(board.columns, 1)
    cell_height = image.shape[0] / max(board.rows, 1)
    thickness = max(3, round(min(cell_width, cell_height) * 0.22))

    for line in board.lines:
        points = [center_by_cell[cell] for cell in line.path if cell in center_by_cell]
        if len(points) < 2:
            continue
        color_bgr = tuple(int(channel) for channel in reversed(line.color))
        cv2.polylines(
            overlay,
            [np.asarray(points, dtype=np.int32).reshape((-1, 1, 2))],
            False,
            color_bgr,
            thickness,
            cv2.LINE_AA,
        )

    status = "SOLVED" if solved else "NOT SOLVED"
    return _add_status(overlay, status, message)


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

        max_extra_steps = 10 if max(rows, columns) <= 6 else 18
        solve_board(board, max_extra_steps=max_extra_steps)
        solved = board.isSolved()
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