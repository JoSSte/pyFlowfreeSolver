#!/usr/bin/env python3
"""Grab Flow Free screens from an Android device and solve them in real time.

Each frame is captured over ADB, the grid and endpoint dots are detected, and
the board is solved with CP-SAT. The live window shows the solution overlaid
on the screenshot. A second window shows a static image of the solved grid:
it is pinned when a new puzzle is first solved and does not change while you
play. When a new puzzle appears, ``livegrabs/`` gets the raw grab (``live_<time>.png``), the
solved overlay (``live_<time>_solved.png``) and the cropped solved board
(``live_<time>_board.png``).

Usage:
    python flow.py                 # live loop, press q or Esc to quit
    python flow.py --once          # grab, solve and save a single frame
    python flow.py --no-window     # live loop without a display window
"""

import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path
import time

import cv2
import numpy as np
from ppadb.client import Client as AdbClient

from constraintSolver import solve_board_cp_sat
from overlay import add_status, solution_overlay
from shapeDetection import detectGrid, get_resized_for_display_img, parseBoard


PROJECT_ROOT = Path(__file__).resolve().parent
LIVE_GRABS = PROJECT_ROOT / "livegrabs"
WINDOW_NAME = "Flow Free live solver"
BOARD_WINDOW_NAME = "Solved board"


def connect_device(host="127.0.0.1", port=5037):
    devices = AdbClient(host=host, port=port).devices()
    if not devices:
        raise SystemExit("No Android device attached (check `adb devices`).")
    return devices[0]


def grab_frame(device):
    """Capture the device screen as a BGR image (same layout as cv2.imread)."""
    png = device.screencap()
    image = cv2.imdecode(np.frombuffer(png, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise RuntimeError("Could not decode screenshot from device")
    return image


def normalize_brightness(image, dim_threshold=128):
    """Stretch a dimmed frame back to full range.

    A phone that is dimming before sleep (or using an "extra dim" overlay)
    returns screencaps at a fraction of normal brightness, which defeats the
    grid and dot detection. Normal frames are returned unchanged.
    """
    peak = int(image.max())
    if peak == 0 or peak >= dim_threshold:
        return image
    return cv2.convertScaleAbs(image, alpha=255.0 / peak)


def board_signature(board):
    """Identify a puzzle by which endpoint cells are paired together.

    Exact colors drift between frames and a stray empty row or column can be
    detected while playing, so neither is part of the identity.
    """
    pairs = {}
    for field in board.fields:
        if field.piece is not None:
            pairs.setdefault(field.piece.color, set()).add((field.column, field.row))
    return frozenset(frozenset(cells) for cells in pairs.values())


def crop_board(image, squares):
    """Cut the grid out of a frame, dropping the game's menu and buttons."""
    if not squares:
        return None
    xs = sorted(center[0] for center, _ in squares)
    ys = sorted(center[1] for center, _ in squares)
    columns = max(cell[0] for _, cell in squares)
    rows = max(cell[1] for _, cell in squares)
    half_width = (xs[-1] - xs[0]) / max(columns - 1, 1) / 2
    half_height = (ys[-1] - ys[0]) / max(rows - 1, 1) / 2
    top = max(0, int(ys[0] - half_height))
    bottom = min(image.shape[0], int(ys[-1] + half_height) + 1)
    left = max(0, int(xs[0] - half_width))
    right = min(image.shape[1], int(xs[-1] + half_width) + 1)
    return image[top:bottom, left:right].copy()


def process_frame(image):
    """Detect and solve a frame.

    Returns (overlay, board_view, signature, solved, message). board_view is
    the solved grid cropped from the overlay, or None when there is no board;
    signature is None when no complete board was detected.
    """
    image = normalize_brightness(image)
    squares, circles, rows, columns = detectGrid(image.copy(), False)
    if not rows or not columns or circles is None:
        return add_status(image.copy(), "NO BOARD", "Waiting for a Flow Free board"), None, None, False, "no board"

    board = parseBoard(image, rows, columns, circles, squares)
    color_counts = Counter(field.piece.color for field in board.fields if field.piece is not None)
    if not color_counts or any(count != 2 for count in color_counts.values()):
        message = f"{columns}x{rows}; detected dots do not form complete pairs"
        return solution_overlay(image, None, squares, False, message), None, None, False, message

    started = time.perf_counter()
    solved = solve_board_cp_sat(board)
    elapsed = time.perf_counter() - started
    message = f"{columns}x{rows}; {len(color_counts)} pairs; solved in {elapsed:.2f}s"
    overlay = solution_overlay(image, board, squares, solved, message)
    board_view = crop_board(overlay, squares)
    return overlay, board_view, board_signature(board), solved, message


def save_grab(image, overlay, board_view):
    """Save the grab and its solution side by side in livegrabs/."""
    LIVE_GRABS.mkdir(parents=True, exist_ok=True)
    stem = "live_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    images = {"grab": (LIVE_GRABS / f"{stem}.png", image),
              "solved": (LIVE_GRABS / f"{stem}_solved.png", overlay)}
    if board_view is not None:
        images["board"] = (LIVE_GRABS / f"{stem}_board.png", board_view)
    saved = {}
    for name, (path, picture) in images.items():
        if cv2.imwrite(str(path), picture):
            saved[name] = path
        else:
            print(f"Could not write {path}")
    return saved


def report_saved(image, overlay, board_view, solved, message):
    saved = save_grab(image, overlay, board_view)
    status = "SOLVED" if solved else "NOT SOLVED"
    lines = "".join(f"\n  {name + ':':7} {path}" for name, path in saved.items())
    print(f"{status}: {message}{lines}")


def show(overlay, board_view, wait_for_key):
    """Display the overlay and solved board; return True when the user asked to quit."""
    # Both windows are scaled to fit the screen and stay resizable.
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.imshow(WINDOW_NAME, get_resized_for_display_img(overlay))
    if board_view is not None:
        cv2.namedWindow(BOARD_WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.imshow(BOARD_WINDOW_NAME, get_resized_for_display_img(board_view))
    key = cv2.waitKey(0 if wait_for_key else 1) & 0xFF
    return key in (ord("q"), 27)


# A new puzzle must be solved with the same layout in this many consecutive
# frames before it replaces the pinned solution, so one misdetected frame
# while playing cannot change it.
CONFIRM_FRAMES = 2


def run(once=False, show_window=True, interval=0.0, host="127.0.0.1", port=5037):
    device = connect_device(host, port)
    print(f"Connected to {device.serial}")
    pinned_signature = None
    pinned_view = None
    candidate_signature, candidate_count = None, 0

    while True:
        image = grab_frame(device)
        overlay, board_view, signature, solved, message = process_frame(image)

        if solved and signature != pinned_signature:
            if signature == candidate_signature:
                candidate_count += 1
            else:
                candidate_signature, candidate_count = signature, 1
        else:
            candidate_signature, candidate_count = None, 0

        # Pin (and save) the solve only once a new puzzle is confirmed.
        if once or candidate_count >= CONFIRM_FRAMES:
            report_saved(image, overlay, board_view, solved, message)
            if solved:
                pinned_signature, pinned_view = signature, board_view
            candidate_signature, candidate_count = None, 0

        if show_window and show(overlay, pinned_view, wait_for_key=once):
            break
        if once:
            break
        time.sleep(interval)

    if show_window:
        cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--once", action="store_true", help="Grab and solve a single frame, then exit.")
    parser.add_argument("--no-window", action="store_true", help="Do not open a display window.")
    parser.add_argument("--interval", type=float, default=0.0, help="Seconds to wait between grabs.")
    parser.add_argument("--host", default="127.0.0.1", help="ADB server host.")
    parser.add_argument("--port", type=int, default=5037, help="ADB server port.")
    args = parser.parse_args()
    run(once=args.once, show_window=not args.no_window, interval=args.interval,
        host=args.host, port=args.port)


if __name__ == "__main__":
    main()
