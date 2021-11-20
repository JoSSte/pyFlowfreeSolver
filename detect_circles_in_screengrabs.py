from shapeDetection import detectGrid
import numpy as np
import cv2


# TODO: move to parameterizzed testcase
screengrabs =  {
  "filename": "screengrabs/s7_screen_05_05.png",
  "gridsize": {"x":5, "y":5},
  "expected_pairs": 5
},{
  "filename": "screengrabs/s7_screen_05_06.png",
  "gridsize": {"x":5, "y":6},
  "expected_pairs": 4
},{
  "filename": "screengrabs/s7_screen_06_06.png",
  "gridsize": {"x":6, "y":6},
  "expected_pairs": 5
},{
  "filename": "screengrabs/s7_screen_10_10.png",
  "gridsize": {"x":10, "y":10},
  "expected_pairs": 9
},{
  "filename": "screengrabs/s21_screen_05_05.jpg",
  "gridsize": {"x":5, "y":5},
  "expected_pairs": 6
},{
  "filename": "screengrabs/s21_screen_06_06.jpg",
  "gridsize": {"x":6, "y":6},
  "expected_pairs": 6
},{
  "filename": "screengrabs/s21_screen_07_07.jpg",
  "gridsize": {"x":7, "y":7},
  "expected_pairs": 6
},{
  "filename": "screengrabs/s21_screen_08_08.jpg",
  "gridsize": {"x":8, "y":8},
  "expected_pairs": 6
}#,{
#  "filename": "screengrabs/s21_screen_09_09.jpg",
#  "gridsize": {"x":9, "y":9},
#  "expected_pairs": 6
#},{
#  "filename": "screengrabs/s21_screen_10_10.jpg",
#  "gridsize": {"x":10, "y":10},
#  "expected_pairs": 6
#},{
#  "filename": "screengrabs/s21_screen_11_11.jpg",
#  "gridsize": {"x":11, "y":11},
#  "expected_pairs": 6
#},{
#  "filename": "screengrabs/s21_screen_12_12.jpg",
#  "gridsize": {"x":12, "y":12},
#  "expected_pairs": 6
#},{
#  "filename": "screengrabs/s21_screen_13_13.jpg",
#  "gridsize": {"x":13, "y":13},
#  "expected_pairs": 6
#},{
#  "filename": "screengrabs/s21_screen_14_14.jpg",
#  "gridsize": {"x":14, "y":14},
#  "expected_pairs": 6
#},{
#  "filename": "screengrabs/s21_screen_15_15.jpg",
#  "gridsize": {"x":15, "y":15},
#  "expected_pairs": 6
#}

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

  
