from shapeDetection import detectGrid
import numpy as np
import cv2


# TODO: move to parameterizzed testcase
screengrabs =  {
  "filename": "screengrabs/screen_05_05.png",
  "gridsize": {"x":5, "y":5},
  "expected_pairs": 5,
},{
  "filename": "screengrabs/screen_05_06.png",
  "gridsize": {"x":5, "y":6},
  "expected_pairs": 4,
},{
  "filename": "screengrabs/screen_06_06.png",
  "gridsize": {"x":6, "y":6},
  "expected_pairs": 5,
},{
  "filename": "screengrabs/screen_10_10.png",
  "gridsize": {"x":10, "y":10},
  "expected_pairs": 9,
}

for i in screengrabs:
  # load the image, clone it for output, and then convert it to grayscale
  image = cv2.imread(i["filename"])
  _, circles, rows, cols = detectGrid(image)
  print("Detecting circles in %s. Expecting %d circles: Found %d. Expecting %d columns: Found %d. Expecting %d rows: Found %d." % (i["filename"], i["expected_pairs"]*2, len(circles),i["gridsize"]["x"], cols, i["gridsize"]["y"], rows))
  
  if i["expected_pairs"]*2 ==  len(circles):
    print("number of circles match!")
  if i["gridsize"]["x"] == cols:
    print("number of columns match!")
  if i["gridsize"]["y"] == rows:
    print("number of rows match!")

  
