import unittest

from shapeDetection import detectGrid
import numpy as np
import cv2
from gameboard import Piece, Field, GameBoard


class TestField(unittest.TestCase):
    def testField(self):
        """
        test that we can create a field
        """
        f1 = Field(2, 3)
        #print("%d fields found" % Field.fieldCount)
        #self.assertEqual(Field.fieldCount, 1)
        self.assertEqual(f1.row, 3)
        self.assertEqual(f1.column, 2)
        self.assertFalse(f1.isOccupied())

    def testNeighbours(self):
        """
        test that we add neighbours correctly
        """
        f1 = Field(1, 1)
        f2 = Field(1, 2)
        f3 = Field(1, 3)
        f2.setWest(f1)
        f3.setWest(f2)

        #print("%d fields found" % Field.fieldCount)
        #self.assertEqual(Field.fieldCount, 1)
        self.assertEqual(f1.row, 1)
        self.assertEqual(f1.column, 1)

        self.assertEqual(f1.numNeighbours(), 1)
        self.assertEqual(f2.numNeighbours(), 2)
        self.assertEqual(f3.numNeighbours(), 1)

    def testBoard(self):
        cols = 3
        rows = 5
        expected = rows*cols
        gb = GameBoard(cols, rows)
        #print("%d filds in board" % len(gb.fields))
        self.assertEqual(gb.rows, rows)
        self.assertEqual(gb.columns, cols)
        self.assertEqual(len(gb.fields), expected)
        # TODO: test neighbours, edge pieces, etc

    def testPiece(self):
        f1 = Field(2, 2)
        self.assertFalse(f1.isOccupied())
        f1.addPiece(Piece('red'))
        self.assertTrue(f1.isOccupied())
        f2 = Field(1, 1)
        self.assertFalse(f2.isOccupied())
        f2.addLine('red')
        self.assertTrue(f2.isOccupied())
        f2.clearLine()
        self.assertFalse(f2.isOccupied())

    screengrabs =  {
      "filename": "screengrabs/s7_screen_05_05.png",
      "gridsize": {"x":5, "y":5},
      "expected_pairs": 5
    },{
      "filename": "screengrabs/s7_screen_05_05_2.png",
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
      "filename": "screengrabs/s7_screen_06_06_2.png",
      "gridsize": {"x":6, "y":6},
      "expected_pairs": 6
    },{
      "filename": "screengrabs/s7_screen_07_07.png",
      "gridsize": {"x":7, "y":7},
      "expected_pairs": 6
    },{
      "filename": "screengrabs/s7_screen_08_08.png",
      "gridsize": {"x":8, "y":8},
      "expected_pairs": 6
    },{
      "filename": "screengrabs/s7_screen_09_09.png",
      "gridsize": {"x":9, "y":9},
      "expected_pairs": 9
    },{
      "filename": "screengrabs/s7_screen_10_10.png",
      "gridsize": {"x":10, "y":10},
      "expected_pairs": 9
    },{
      "filename": "screengrabs/s7_screen_10_10_2.png",
      "gridsize": {"x":10, "y":10},
      "expected_pairs": 9
    },{
      "filename": "screengrabs/s21_screen_05_05.jpg",
      "gridsize": {"x":5, "y":5},
      "expected_pairs": 5
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
    }

    screengrabs_non_passing = {
      "filename": "screengrabs/s7_screen_12_15.png",
      "gridsize": {"x":12, "y":15},
      "expected_pairs": 9
    },{
      "filename": "screengrabs/s7_screen_12_12.png",
      "gridsize": {"x":12, "y":12},
      "expected_pairs": 9
    },{
      "filename": "screengrabs/s7_screen_11_14.png",
      "gridsize": {"x":11, "y":14},
      "expected_pairs": 12
    },{
      "filename": "screengrabs/s21_screen_09_09.jpg",
      "gridsize": {"x":9, "y":9},
      "expected_pairs": 6
    },{
      "filename": "screengrabs/s21_screen_10_10.jpg",
      "gridsize": {"x":10, "y":10},
      "expected_pairs": 6
    },{
      "filename": "screengrabs/s21_screen_11_11.jpg",
      "gridsize": {"x":11, "y":11},
      "expected_pairs": 6
    },{
      "filename": "screengrabs/s21_screen_12_12.jpg",
      "gridsize": {"x":12, "y":12},
      "expected_pairs": 6
    },{
      "filename": "screengrabs/s21_screen_13_13.jpg",
      "gridsize": {"x":13, "y":13},
      "expected_pairs": 6
    },{
      "filename": "screengrabs/s21_screen_14_14.jpg",
      "gridsize": {"x":14, "y":14},
      "expected_pairs": 6
    },{
      "filename": "screengrabs/s21_screen_15_15.jpg",
      "gridsize": {"x":15, "y":15},
      "expected_pairs": 6
    }

    def testDetection(self):
        for i in self.screengrabs:
            image = cv2.imread(i["filename"])
            _, circles, rows, cols = detectGrid(image)
            #print("Detecting circles in %s. Expecting %d circles: Found %d. Expecting %d columns: Found %d. Expecting %d rows: Found %d." % (i["filename"], i["expected_pairs"]*2, len(circles),i["gridsize"]["x"], cols, i["gridsize"]["y"], rows))
            self.assertEqual(len(circles), i["expected_pairs"]*2)
            self.assertEqual(cols, i["gridsize"]["x"])
            self.assertEqual(rows, i["gridsize"]["y"])

if __name__ == '__main__':
    unittest.main()
