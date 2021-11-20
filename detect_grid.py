from shapeDetection import detectGrid
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread(args["image"])
squares, circles, rows, cols = detectGrid(image, True)
print(squares)
print(circles)
print ("%d rows\t%d columns\t%d squares" % (rows, cols, len(squares)))
print ("%d circles" % ( len(circles)))


