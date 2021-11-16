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
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)

BLOCK_SIZE = 40
ROWS = 5
COLS = 5

"""

Testing board and solver
========================

Layout: 

1,1 red
3,1 green
5,1 yellow

3,2 blue
5,2 orange

2,4 green
4,4 yellow

2,5 red
3,5 blue
4,5 orange


Red path: 
1,1 -> 1,2 -> 1,3 -> 1,4 -> 1,5 -> 2,5
S,S,S,S,E

Green path: 
3,1 -> 2,1 -> 2,2 -> 2,3 -> 2,4
W,S,S,S

"""


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
    center = coordinate2pyGameCoordinate(f.column,f.row)
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


gb = GameBoard(COLS, ROWS)
gb.fields[0].addPiece(Piece('R'))  # Red
gb.fields[21].addPiece(Piece('R')) #Red
gb.fields[ 2].addPiece(Piece('G')) #Green
gb.fields[16].addPiece(Piece('G')) #Green
gb.fields[ 7].addPiece(Piece('B')) #Blue
gb.fields[22].addPiece(Piece('B')) #Blue
gb.fields[ 4].addPiece(Piece('Y')) #Yellow
gb.fields[18].addPiece(Piece('Y')) #Yellow
gb.fields[ 9].addPiece(Piece('O')) #Orange
gb.fields[23].addPiece(Piece('O')) #Orange

# red line for visual:
gb.fields[ 5].addLine('R') #Red
gb.fields[10].addLine('R') #Red
gb.fields[15].addLine('R') #Red
gb.fields[20].addLine('R') #Red
#redpath = Path('R', (1,1), ['S','S','S','S','E'])
redline = Line('R', [(1,1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 5)])
greenline = Line('G', [(3,1), (2, 1), (2, 2), (2, 3), (2, 4)])

# Green line for visual
gb.fields[ 1].addLine('G') #Green
gb.fields[ 6].addLine('G') #Green
gb.fields[11].addLine('G') #Green


# create the display window
win = pg.display.set_mode((COLS * BLOCK_SIZE, ROWS * BLOCK_SIZE))

# optional title bar caption
pg.display.set_caption("FlowFree %d ☓ %d" % (COLS, ROWS))

# default background is black, so make it WHITE
win.fill(GRAY)

drawGrid(win, COLS, ROWS)
drawPieces(gb)
drawLine(redline)
drawLine(greenline)

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
