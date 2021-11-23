from guiTools import drawGameboard
from shapeDetection import detectGrid, parseBoard
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread(args["image"])
squares, circles, rows, cols = detectGrid(image, True)
board = parseBoard(image, rows, cols, circles, squares)
#print(squares)
#print(circles)
#print(board)
print ("%d rows\t%d columns\t%d squares" % (rows, cols, len(squares)))
print ("%d circles" % ( len(circles)))

drawGameboard(board)
