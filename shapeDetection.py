try:
    from win32api import GetSystemMetrics
except ImportError:
    GetSystemMetrics = None
import numpy as np
import math
import cv2

from gameboard import GameBoard

# the maximum width/height of a table in cell count
MAX_TABLE_DIMENSION = 15

def _screen_size(img):
    """Return (width, height) of the smallest monitor, so windows fit on any of them."""
    if GetSystemMetrics is not None:
        return GetSystemMetrics(0), GetSystemMetrics(1)
    try:
        import pygame
        pygame.display.init()
        sizes = pygame.display.get_desktop_sizes()
        if sizes:
            return min(w for w, _ in sizes), min(h for _, h in sizes)
    except Exception:
        pass
    return img.shape[1], img.shape[0]


#resize image to fit on the screen
def get_resized_for_display_img(img):
    screen_w, screen_h = _screen_size(img)
    #print("screen size", screen_w, screen_h)
    if(len(img.shape) == 2) :
        h, w = img.shape
    else: 
        h, w, _ = img.shape
    # img get w of screen and adapt h
    h = h * (screen_w / w)
    w = screen_w
    if h > screen_h:  # if img h still too big
        # img get h of screen and adapt w
        w = w * (screen_h / h)
        h = screen_h
    w, h = w*0.9, h*0.9  # because you don't want it to be that big, right ?
    w, h = int(w), int(h)  # you need int for the cv2.resize
    return cv2.resize(img, (w, h))

#TODO: make limits relative to screen size instead of hard-coded
def detectCircles(image, displayImage=False, minRadius=45, maxRadius=120, minDistance=40, param2=40):
    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detect circles in the image
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        1,
        minDistance,
        param1=50,
        param2=param2,
        minRadius=minRadius,
        maxRadius=maxRadius,
    )
    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        if(displayImage):
            # loop over the (x, y) coordinates and radius of the circles
            for idx, (x, y, r) in enumerate(circles):
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5),(x + 5, y + 5), (0, 128, 255), -1)
                cv2.putText(output, str(idx), (x - 7, y - 7), cv2.FONT_HERSHEY_SIMPLEX, 1, (60,60,60), 2, cv2.LINE_AA )
                #print("x: %d\ty: %d\tr: %d" % (x, y, r))
        # show the output image
            cv2.imshow("output", get_resized_for_display_img(np.hstack([image, output])))
            cv2.waitKey(0)
        
        if(circles is None):
            circles = []
        return circles

def roundx(num: int)-> int:
    return int(round(num/20))*20

def uniquelist(llist, minDist = 0):
    llist = list(set(llist))
    llist.sort()
    return llist

def _projection_line_centers(mask, axis):
    projection = mask.sum(axis=axis).astype(float)
    if projection.size == 0 or projection.max() == 0:
        return []

    indices = np.flatnonzero(projection >= projection.max() * 0.6)
    groups = np.split(indices, np.where(np.diff(indices) > 1)[0] + 1)
    return [int(round(float(group.mean()))) for group in groups if len(group)]


def _line_extent(line_mask, centers, axis, size):
    """Return (start, end) of the grid along the direction the lines run.

    Each detected line in ``line_mask`` (vertical lines for ``axis=0``,
    horizontal lines for ``axis=1``) is measured from its first to its last
    pixel. Real grid lines all span the whole grid while pipe edges are
    shorter, so the median start and end give the grid's extent. Falls back
    to the full ``size``.
    """
    starts, ends = [], []
    for center in centers:
        band = line_mask[:, max(0, center - 2):center + 3] if axis == 0 else line_mask[max(0, center - 2):center + 3, :]
        covered = np.flatnonzero(band.any(axis=1 if axis == 0 else 0))
        if covered.size:
            starts.append(covered[0])
            ends.append(covered[-1])
    if not starts:
        return 0, size
    return int(np.median(starts)), int(np.median(ends))


def _fit_lattice(lines, pitch, anchor, tolerance, extent):
    """Match evenly spaced positions through ``anchor`` against detected lines.

    Returns (score, -deviation, positions): positions run across the grid
    extent, using the detected line where one is close enough and the
    predicted position otherwise; score is matched minus missing positions
    and deviation the total distance of matched lines from the lattice.
    """
    low, high = extent[0] - tolerance, extent[1] + tolerance
    first = anchor - math.floor((anchor - low) / pitch) * pitch
    positions, matched, deviation = [], 0, 0.0
    position = first
    while position <= high:
        index = int(np.searchsorted(lines, position))
        nearest = min(
            (lines[i] for i in (index - 1, index) if 0 <= i < len(lines)),
            key=lambda line: abs(line - position),
        )
        if abs(nearest - position) <= tolerance:
            positions.append(int(nearest))
            matched += 1
            deviation += abs(nearest - position)
        else:
            positions.append(int(round(position)))
        position += pitch
    return matched - (len(positions) - matched), -deviation, positions


def _candidate_pitches(lines, span):
    """Pitches implied by pairs of detected lines, within plausible cell sizes."""
    min_pitch = span / (MAX_TABLE_DIMENSION + 1)
    max_pitch = span / 4
    pitches = set()
    for i, first in enumerate(lines):
        for second in lines[i + 1:]:
            for steps in range(1, MAX_TABLE_DIMENSION + 1):
                pitch = (second - first) / steps
                if pitch < min_pitch:
                    break
                if pitch <= max_pitch:
                    pitches.add(round(pitch * 2) / 2)
    return pitches


def _best_lattice(lines, extent, pitch):
    """Best (score, -deviation, positions) for a fixed pitch over all anchors."""
    best = None
    for anchor in lines:
        fit = _fit_lattice(lines, pitch, anchor, pitch * 0.1, extent)
        if best is None or fit[:2] > best[:2]:
            best = fit
    return best


def _square_grid_lines(raw_columns, column_extent, raw_rows, row_extent):
    """Fit evenly spaced column and row lines that share one cell pitch.

    Drawn pipes and highlighted cells add bright edges that show up as extra
    "grid lines", and a pipe running along a grid line can hide it. Real grid
    lines form a lattice of square cells, so this finds the single pitch whose
    column and row lattices best match the detected lines (matched minus
    missing, then least deviation, then larger pitch). Lines off the lattice
    are dropped and hidden lines are filled in.
    """
    if len(raw_columns) < 3 or len(raw_rows) < 3:
        return raw_columns, raw_rows
    columns = np.asarray(sorted(raw_columns), dtype=float)
    rows = np.asarray(sorted(raw_rows), dtype=float)
    column_span = column_extent[1] - column_extent[0]
    row_span = row_extent[1] - row_extent[0]
    if column_span <= 0 or row_span <= 0:
        return raw_columns, raw_rows

    pitches = _candidate_pitches(columns, column_span) | _candidate_pitches(rows, row_span)
    best_key, best = None, (raw_columns, raw_rows)
    for pitch in pitches:
        column_fit = _best_lattice(columns, column_extent, pitch)
        row_fit = _best_lattice(rows, row_extent, pitch)
        key = (column_fit[0] + row_fit[0], column_fit[1] + row_fit[1], pitch)
        if best_key is None or key > best_key:
            best_key, best = key, (column_fit[2], row_fit[2])
    return best


def detectGrid(image, displayImage=False):
    if image is None or image.size == 0:
        raise ValueError("detectGrid requires a non-empty image")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    threshold = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return [], None, 0, 0

    # Pick the board by bounding-box area, not enclosed contour area: overlays
    # such as a scrollbar or a highlighted row can break the board outline so
    # the contour no longer encloses the grid, letting a small button win.
    # The board is rectangular, so its bounding box is the region to use.
    def bounding_area(contour):
        _, _, contour_width, contour_height = cv2.boundingRect(contour)
        return contour_width * contour_height

    board_contour = max(contours, key=bounding_area)
    x, y, width, height = cv2.boundingRect(board_contour)
    if width == 0 or height == 0:
        return [], None, 0, 0

    board_gray = gray[y:y + height, x:x + width]
    binary = cv2.threshold(board_gray, 35, 255, cv2.THRESH_BINARY)[1]

    vertical_length = max(20, height // 30)
    horizontal_length = max(20, width // 30)
    vertical_lines = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_length)),
    )
    horizontal_lines = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_length, 1)),
    )
    # The grid's extent along one axis is where the other axis' lines run;
    # the bounding box can include menus or touch glow beyond the grid.
    raw_columns = _projection_line_centers(vertical_lines, axis=0)
    raw_rows = _projection_line_centers(horizontal_lines, axis=1)
    column_lines, row_lines = _square_grid_lines(
        raw_columns, _line_extent(horizontal_lines, raw_rows, axis=1, size=width),
        raw_rows, _line_extent(vertical_lines, raw_columns, axis=0, size=height),
    )
    if len(column_lines) < 2 or len(row_lines) < 2:
        return [], None, 0, 0

    columns = len(column_lines) - 1
    rows = len(row_lines) - 1
    cell_width = float(np.median(np.diff(column_lines)))
    cell_height = float(np.median(np.diff(row_lines)))
    cell_pitch = min(cell_width, cell_height)
    if cell_pitch <= 0:
        return [], None, 0, 0

    squares = []
    for row in range(rows):
        center_y = y + int(round((row_lines[row] + row_lines[row + 1]) / 2))
        for column in range(columns):
            center_x = x + int(round((column_lines[column] + column_lines[column + 1]) / 2))
            squares.append(((center_x, center_y), (column + 1, row + 1)))

    min_radius = max(10, int(round(cell_pitch * 0.28)))
    max_radius = max(min_radius + 1, int(round(cell_pitch * 0.52)))
    circles = detectCircles(
        cv2.cvtColor(board_gray, cv2.COLOR_GRAY2BGR),
        minRadius=min_radius,
        maxRadius=max_radius,
        minDistance=max(20, int(round(cell_pitch * 0.5))),
    )
    if circles is not None:
        circles[:, 0] += x
        circles[:, 1] += y
    else:
        print("No circles found!! fatal error!")

    if displayImage:
        overlay = image.copy()
        for (center_x, center_y), _ in squares:
            cv2.drawMarker(overlay, (center_x, center_y), (0, 255, 0), cv2.MARKER_CROSS, 10, 2)
        if circles is not None:
            for center_x, center_y, radius in circles:
                cv2.circle(overlay, (int(center_x), int(center_y)), int(radius), (0, 255, 0), 2)
        cv2.imshow("Final Image", get_resized_for_display_img(overlay))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return squares, circles, rows, columns

#function to take the input from a screengrab and put into the solvable Gameboard format
def parseBoard(image, rows, cols, circles, squares)-> GameBoard:
    gb = GameBoard(cols, rows)
    for cidx, (x,y,r) in enumerate(circles):
        #Detect color
        color = (image[y,x][2], image[y,x][1], image[y,x][0])

        # Detect Cell
        for ((sx,sy),(bx,by)) in squares:
            distance = np.sqrt((sx-x)**2 + (sy-y)**2)
            
            #print("checking #%d %d, %d in cell %d, %d (%d, %d)\t[distance: %d]\twith color %s" % (cidx, x,y, bx,by, sx,sy, distance, color))
            # If center of square withing radius of circle form circle coordinate, we are in the same cell...
            if(distance <= r):
                #print("Adding #%d %d, %d in cell %d, %d (%d, %d)\t[distance: %d]\twith color %s" % (cidx, x,y, bx,by, sx,sy, distance, color))
                # Add it to the gameboard
                try:
                    gb.addPiece(bx, by, color)
                    # We found the cell, no need to check other cells
                    break
                except Exception as a:
                    print("Cell [%d,%d] occupied (adding %s) %s"% (bx, by, color, a))
    #print(circles)
    return gb