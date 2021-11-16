import unittest

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


if __name__ == '__main__':
    unittest.main()
