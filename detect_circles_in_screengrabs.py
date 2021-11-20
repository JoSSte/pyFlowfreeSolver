from shapeDetection import detectCircles
import numpy as np
import cv2

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
  print("detecting circles in %s. expecting %d pairs" % (i["filename"], i["expected_pairs"]))
  circles = detectCircles(image)
  print("Found %d circles in %s" % (len(circles), i["filename"]))
  piece_size_guess = 0
  for idx,(x, y, r) in enumerate(circles):
    print("%d\tx: %d\ty: %d\tr: %d" % (idx, x, y, r))
  
