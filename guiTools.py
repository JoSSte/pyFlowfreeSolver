from gameboard import Piece, Field, GameBoard, Line
import pygame as pg


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
    fname = "output/FlowFree_%d☓%d.png" % (board.columns, board.rows)
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