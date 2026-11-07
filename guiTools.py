from gameboard import Piece, Field, GameBoard, Line
from datetime import datetime
from pathlib import Path
import pygame as pg

"""
Tools to display a gameboard.
Not needed for solving, but useful to display the internal gameboard
"""

# pygame uses (r, g, b) colour tuples
class C:
    SILVER = (200, 200, 200)
    GRAY = (40, 40, 40)
    DARKGRAY = (20, 20, 20)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    #Colours from ingame
    BLUE = (12, 41, 254)
    RED = (255, 0, 0)
    GREEN = (0, 141, 0)
    YELLOW = (234, 224, 0)
    ORANGE = (251, 137, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 10, 201)
    BROWN = (165, 42, 42)
    CYAN = (0, 255, 255)


# convert row/column to x/y based on the BLOCK_SIZE
def coordinate2pyGameCoordinate(x, y):
    return [(BLOCK_SIZE*x)-(BLOCK_SIZE//2), (BLOCK_SIZE*y)-(BLOCK_SIZE//2)]

# function to convert letter to colour


def drawPiece(win, f: Field):
    center = coordinate2pyGameCoordinate(f.column, f.row)
    radius = round((BLOCK_SIZE//2)-(BLOCK_SIZE//15))
    pg.draw.circle(win, f.piece.color, center, radius, 0)


def drawLine(win, p: Line):
    thickness = BLOCK_SIZE//4
    coordinates = []
    #translate grid coordinates to pygame coordinates
    for cPos in p.path:
        coordinates.append(coordinate2pyGameCoordinate(cPos[0], cPos[1]))
    pg.draw.lines(win, p.color, False, coordinates, thickness)


# draw all pieces and lines in the gameboard
def drawContents(win, gb: GameBoard):
    for f in gb.fields:
        if(f.isOccupied()):
            if(f.piece is not None):
                drawPiece(win, f)
    for l in gb.lines:
        drawLine(win, l)


# draw grid on gameboard
def drawGrid(screen, w, h):
    for x in range(0, BLOCK_SIZE * w, BLOCK_SIZE):
        for y in range(0, BLOCK_SIZE * h, BLOCK_SIZE):
            rect = pg.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pg.draw.rect(screen, C.SILVER, rect, 1)


def _output_filename(board):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = "FlowFree_%d☓%d_%s.png" % (board.columns, board.rows, timestamp)
    return str(output_dir / filename)


class LiveGameboard:
    def __init__(self, board, block_size=60, update_delay=80):
        global BLOCK_SIZE
        pg.init()
        BLOCK_SIZE = block_size
        self.board = board
        self.update_delay = update_delay
        self.width = board.columns * block_size
        self.height = board.rows * block_size
        self.screen = pg.display.set_mode((self.width, self.height + 32))
        pg.display.set_caption("FlowFree %d x %d - solving" % (board.columns, board.rows))
        self.font = pg.font.Font(None, 22)
        self._draw("Preparing solve")

    def _process_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                raise SystemExit

    def _draw(self, message):
        self.screen.fill(C.DARKGRAY)
        drawGrid(self.screen, self.board.columns, self.board.rows)
        drawContents(self.screen, self.board)
        label = self.font.render(message, True, C.WHITE)
        self.screen.blit(label, (8, self.height + 7))
        pg.display.flip()
        self._process_events()

    def update(self, board, message):
        self.board = board
        self._draw(message)
        if self.update_delay:
            pg.time.delay(self.update_delay)

    def finish(self, board, solved):
        self.board = board
        message = "Solved - close window or press Esc" if solved else "No solution - close window or press Esc"
        self._draw(message)
        filename = _output_filename(board)
        image = self.screen.subsurface((0, 0, self.width, self.height)).copy()
        pg.image.save(image, filename)
        print("file {} has been saved".format(filename))

        while True:
            self._process_events()
            pg.time.wait(50)


def drawGameboard(board, block_size = 40):
    global BLOCK_SIZE
    BLOCK_SIZE = block_size
    # create the display window
    win = pg.display.set_mode((board.columns * block_size, board.rows * block_size))

    # optional title bar caption
    pg.display.set_caption("FlowFree %d ☓ %d" % (board.columns, board.rows))

    # default background is black, so make it WHITE
    win.fill(C.DARKGRAY)

    drawGrid(win, board.columns, board.rows)
    drawContents(win, board)


    # now save the drawing
    # can save as .bmp .tga .png or .jpg
    fname = _output_filename(board)
    pg.image.save(win, fname)
    print("file {} has been saved".format(fname))

    # update the display window to show the drawing
    pg.display.flip()

    # event loop and exit conditions
    # (press escape key or click window title bar x to exit)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # most reliable exit on x click
                pg.quit()
                raise SystemExit
            elif event.type == pg.KEYDOWN:
                # optional exit with escape key
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    raise SystemExit
        # pg.display.update()