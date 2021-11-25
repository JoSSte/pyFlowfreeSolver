class Piece:
    'class to'
    pieceCount = 0

    def __init__(self, color):
        self.color = color
        self.column = 0
        self.row = 0
        Piece.pieceCount += 1
    
    def __str__(self):
     return "[%d,%d] (%d,%d,%d)" % (self.column, self.row, self.color[0], self.color[1], self.color[2])



class Line:
    path = []
    color = ''

    def __init__(self, color, coords) -> None:
        self.path = coords
        self.color = color

    def addCoordinate(self, coord):
        self.path.append(coord)


class Field:
    'class to contain a single field'
    fieldCount = 0

    def __init__(self, column, row):
        Field.fieldCount += 1
        self.number = Field.fieldCount
        self.row = row
        self.column = column
        self.occupied = False

        # Contents
        self.piece = None
        self.line = None

        # Neighbours
        self.north = None
        self.south = None
        self.west = None
        self.east = None

        # coordinates of square in FlowFree
        self.x = 0
        self.y = 0
    
    def __str__(self):
     return "#%d\tR:%d C:%d\tPiece:%s" % (self.number,self.row, self.column, self.piece)
    
    def addCoordinate(self, x, y):
        self.x = x
        self.y = y

    def addPiece(self, piece):
        # no check for line presence since this is not drawn after lines...
        self.occupied = True
        self.piece = piece
        self.piece.row = self.row
        self.piece.column = self.column

    def addLine(self, colour):
        if(self.occupied):
            print("Already occupied")
            return False
        else:
            self.occupied = True
            self.line = colour

    def clearLine(self):
        if(not self.occupied):
            return False
        else:
            self.line = None
            self.occupied = False
            return True

    def getRow(self):
        return self.row

    def getColumn(self):
        return self.column

    def getX(self):
        return self.column

    def getY(self):
        return self.row

    # Set Neighbours

    def setNorth(self, field):
        self.north = field
        if field.getSouth() is None:
            field.setSouth(self)

    def setSouth(self, field):
        self.south = field
        if field.getNorth() is None:
            field.setNorth(self)

    def setEast(self, field):
        self.east = field
        if field.getWest() is None:
            field.setWest(self)

    def setWest(self, field):
        self.west = field
        if field.getEast() is None:
            field.setEast(self)

    # Get Neighbours
    def getNorth(self):
        return self.north

    def getSouth(self):
        return self.south

    def getEast(self):
        return self.east

    def getWest(self):
        return self.west

    def numNeighbours(self):
        count = 0
        if(self.north is not None):
            count += 1
        if(self.south is not None):
            count += 1
        if(self.east is not None):
            count += 1
        if(self.west is not None):
            count += 1
        return count

    # DisplayStuff

    def displayField(self):
        print("Field #%d, col: %d, row: %d, neighbours: %d, Occupied: %d" % (
            self.number, self.column, self.row, self.numNeighbours(), self.isOccupied()))

    def showNeighbours(self):
        print("N: %s, S: %s, E: %s, W: %s" % (self.number, self.north is not None,
              self.south is not None, self.east is not None, self.west is not None))

    def isOccupied(self):
        return self.occupied


class GameBoard:
    def __init__(self, cols, rows):
        super().__init__()
        self.columns = cols
        self.rows = rows
        self.fields = []
        self.lines = []

        # Create fields
        for row in range(1, self.rows+1):
            for column in range(1, self.columns+1):
                self.fields.append(Field(column, row))

        # Set southern neighbours (also sets northern neighbours)
        for idx, f in enumerate(self.fields):
            if(idx < (len(self.fields)-self.columns)):
                f.setSouth(self.fields[idx + self.columns])

        # Set eastern neighbours
        for idx, f in enumerate(self.fields):
            if((idx + 1) % self.columns != 0):
                f.setEast(self.fields[idx + 1])

    def printBoard(self):
        for f in self.fields:
            f.displayField()

    def coords2Offset(self, x: int, y: int) -> int:
        return (y-1) * self.columns + (x - 1)

    def getField(self, x:int, y:int)-> Field:
        return self.fields[self.coords2Offset(x,y)]

    def addPiece(self, x: int, y: int, colour):
        f = self.fields[self.coords2Offset(x, y)]
        if(not f.isOccupied()):
            f.addPiece(Piece(colour))
        else:
            raise Exception("Cell %d,%d is already ocuppied" % (x, y))

    def addLine(self, l: Line):
        for segment in l.path:
            f = self.getField(segment[0], segment[1])
            if(f.isOccupied()):
                # occupied. OK if piece and is same colour
                if(f.piece is not None):
                    if(not f.piece.color == l.color):
                        print("%d, %d is occupied already" % (segment[0], segment[1]))
                        raise Exception("Cell %d,%d is already occupied" % (segment[0], segment[1]))
            else:
                f.addLine(l.color)
        #TODO: Check that end and start are on a piece...
        
        # if we get to here, all cells in the line are free
        self.lines.append(l)

    def isSolved(self)->bool:
        solved = True
        if(len(self.fields)/2 != len(self.lines)):
            #print("Number of piece-pairs does not match number of lines. Not solved...")
            solved = False
        for f in self.fields:
            if (not f.isOccupied()):
                #print("%d, %d is unoccupied" % (f.getX(), f.getY()))
                solved = False

        return solved