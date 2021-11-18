'''
This is a gui debugger to print a gameboard.
displays a pygame window and saves a .png file with the board.
'''

from gameboard import Piece, Field, GameBoard, Line
import pygame as pg

# pygame uses (r, g, b) color tuples
SILVER = (200, 200, 200)
GRAY = (40, 40, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BLUE = (12, 41, 254)
RED = (255, 0, 0)
GREEN = (0, 141, 0)
YELLOW = (234, 224, 0)
ORANGE = (251, 137, 0)
PURPLE = (128, 0, 128)
PINK = (255, 10, 201)
BROWN = (165, 42, 42)
CYAN = (0, 255, 255)


BLOCK_SIZE = 40
ROWS = 5
COLS = 5

# convert row/column to x/y based on the BLOCK_SIZE


def coordinate2pyGameCoordinate(x, y):
    return [(BLOCK_SIZE*x)-(BLOCK_SIZE//2), (BLOCK_SIZE*y)-(BLOCK_SIZE//2)]

# function to convert letter to colour


def getColor(color):
    if(color == 'R'):
        return RED
    if(color == 'G'):
        return GREEN
    if(color == 'Y'):
        return YELLOW
    if(color == 'B'):
        return BLUE
    if(color == 'O'):
        return ORANGE


def drawPiece(f: Field):
    # f.displayField()
    colour = getColor(f.piece.color)
    # draw a BLUE circle
    # center coordinates (x, y)
    center = coordinate2pyGameCoordinate(f.column, f.row)
    radius = round((BLOCK_SIZE//2)-2)

    # width of 0 (default) fills the circle
    # otherwise it is thickness of outline
    width = 0
    pg.draw.circle(win, colour, center, radius, width)


def drawLine(p: Line):
    #print( type(p))
    thickness = BLOCK_SIZE//4
    coordinates = []
    for cPos in p.path:
        coordinates.append(coordinate2pyGameCoordinate(cPos[0], cPos[1]))
    pg.draw.lines(win, getColor(p.color), False, coordinates, thickness)

# draw all pieces and lines in the gameboard


def drawContents(gb: GameBoard):
    drawPieces(gb)
    for l in gb.lines:
        drawLine(l)
# draw grid on gameboard


def drawGrid(screen, w, h):
    for x in range(0, BLOCK_SIZE * w, BLOCK_SIZE):
        for y in range(0, BLOCK_SIZE * h, BLOCK_SIZE):
            rect = pg.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pg.draw.rect(screen, SILVER, rect, 1)

# Draw pieces


def drawPieces(gameboard: GameBoard):
    for f in gameboard.fields:
        if(f.isOccupied()):
            if(f.piece is not None):
                drawPiece(f)


# initialize board
gb = GameBoard(COLS, ROWS)

# add pieces
gb.addPiece(1, 1, 'R')
gb.addPiece(2, 5, 'R')
gb.addPiece(3, 1, 'G')
gb.addPiece(2, 4, 'G')
gb.addPiece(3, 2, 'B')
gb.addPiece(3, 5, 'B')
gb.addPiece(5, 1, 'Y')
gb.addPiece(4, 4, 'Y')
gb.addPiece(5, 2, 'O')
gb.addPiece(4, 5, 'O')

# add lines
gb.addLine(Line('R', [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 5)]))
gb.addLine(Line('G', [(3, 1), (2, 1), (2, 2), (2, 3), (2, 4)]))
# TODO: solve this tricky situation - skips intermediate cells...
gb.addLine(Line('B', [(3, 2), (3, 5)]))
gb.addLine(Line('Y', [(5, 1), (4, 1), (4, 2), (4, 3), (4, 4)]))
gb.addLine(Line('O', [(5, 2), (5, 3), (5, 4), (5, 5), (4, 5)]))


# create the display window
win = pg.display.set_mode((COLS * BLOCK_SIZE, ROWS * BLOCK_SIZE))

# optional title bar caption
pg.display.set_caption("FlowFree %d ☓ %d" % (COLS, ROWS))

# default background is black, so make it WHITE
win.fill(GRAY)

drawGrid(win, COLS, ROWS)
drawContents(gb)


# now save the drawing
# can save as .bmp .tga .png or .jpg
fname = "output/FlowFree_%d☓%d.png" % (COLS, ROWS)
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
