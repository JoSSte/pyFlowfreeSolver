from guiTools import drawGameboard
from shapeDetection import detectGrid, parseBoard
from solverTools import dist, FieldPair
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread(args["image"])
squares, circles, rows, cols = detectGrid(image, False)
board = parseBoard(image, rows, cols, circles, squares)
# print(squares)
# print(circles)
# print(board)
print("%d rows\t%d columns\t%d squares" % (rows, cols, len(squares)))
print("%d circles" % (len(circles)))

# for f in board.fields:
#    if f.piece is not None:
#        print(f.piece.color)


def doneColor(list, target):
    for i in list:
        if i[0] == target[0] and i[1] == target[1] and i[2] == target[2]:
            return False
    return True

pieces = []
for f in board.fields:
    if f.piece is not None:
        print(f.piece)
        pieces.append(f.piece)
colors = []
sets =[]
for idx, p in enumerate(pieces):
    #p_curr = p
    #pieces.remove(p)
    print("__%d__: (%d,%d,%d)" %(idx, p.color[0], p.color[1], p.color[2]))
    if doneColor(colors, p.color):
        for p2 in pieces:
            if (p2.color[0] == p.color[0] and p2.color[1] == p.color[1] and p2.color[2] == p.color[2]) and (p2.row != p.row and p2.column != p.column):
                sets.append(FieldPair(p, p2))
                #pieces.remove(p2)
                colors.append(p.color)
                break
            else: 
                print("No match between : (%d,%d,%d) and (%d,%d,%d)" %( p.color[0], p.color[1], p.color[2], p2.color[0], p2.color[1], p2.color[2]))
    else: 
        print("done")

print(len(sets))
print(colors)


for s in sets:
    print("Distance between (%d,%d) and (%d,%d) is %d" % (s.p1.column,s.p1.row, s.p2.column, s.p2.row,  dist(s.p1, s.p2)))

drawGameboard(board)
