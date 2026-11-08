"""Draw detection and solution overlays on top of Flow Free screenshots."""

import cv2
import numpy as np


def add_status(image, status, message):
    cv2.rectangle(image, (0, 0), (image.shape[1], 48), (24, 24, 24), -1)
    cv2.putText(image, status, (12, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(image, message[:100], (12, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (220, 220, 220), 1, cv2.LINE_AA)
    return image


def detection_overlay(image, squares, circles, rows, columns):
    overlay = image.copy()
    for (center_x, center_y), (column, row) in squares:
        cv2.drawMarker(overlay, (center_x, center_y), (0, 255, 0), cv2.MARKER_CROSS, 10, 2, cv2.LINE_AA)
        cv2.putText(overlay, f"{column},{row}", (center_x + 5, center_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1, cv2.LINE_AA)

    if circles is not None:
        for index, (center_x, center_y, radius) in enumerate(circles):
            cv2.circle(overlay, (int(center_x), int(center_y)), int(radius), (0, 220, 255), 2, cv2.LINE_AA)
            cv2.putText(overlay, str(index), (int(center_x) - 5, int(center_y) + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2, cv2.LINE_AA)

    circle_count = 0 if circles is None else len(circles)
    return add_status(overlay, "DETECTION", f"grid {columns}x{rows}; {len(squares)} cells; {circle_count} dots")


def solution_overlay(image, board, squares, solved, message):
    overlay = image.copy()
    if board is None:
        return add_status(overlay, "NOT SOLVED", message)

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
    return add_status(overlay, status, message)
