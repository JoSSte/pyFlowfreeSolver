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

def doneColor(list, target):
    for i in list:
        if i== target:
            return False
    return True

pieces = []
for f in board.fields:
    if f.piece is not None:
        print(f.piece)
        pieces.append(f.piece)
colors = []
sets =[]
for idx, p1 in enumerate(pieces):
    #p_curr = p1
    #pieces.remove(p1)
    print("__%d__: (%d,%d,%d)" %(idx, p1.color[0], p1.color[1], p1.color[2]))
    if doneColor(colors, p1.color):
        for p2 in pieces:
            if p1.color == p2.color and not(p2.row == p1.row and p2.column == p1.column):
                sets.append(FieldPair(p1, p2))
                #pieces.remove(p2)
                colors.append(p1.color)
                break
            else: 
                print("No match between : (%d,%d,%d) and (%d,%d,%d)" %( p1.color[0], p1.color[1], p1.color[2], p2.color[0], p2.color[1], p2.color[2]))
    else: 
        print("done")

print(len(sets))
print(colors)


for s in sets:
    print("Distance between (%d,%d) and (%d,%d) is %d" % (s.p1.column,s.p1.row, s.p2.column, s.p2.row,  dist(s.p1, s.p2)))

drawGameboard(board)
