class Piece:
    'class to'
    pieceCount = 0
    def __init__(self, color):
        self.color = color
        Piece.pieceCount += 1

class Field:
    'class to contain a single field'
    fieldCount = 0

    
    def __init__(self, row, column):
        Field.fieldCount += 1
        self.number = Field.fieldCount
        self.row = row
        self.column = column

        #Contents
        self.piece = None
        self.line = None

        #Neighbours
        self.north = None
        self.south = None
        self.west = None
        self.east = None
    
    def addPiece(self, piece):
        self.piece = piece

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
        count=0
        if(self.north is not None):
            count +=1
        if(self.south is not None):
            count +=1
        if(self.east is not None):
            count +=1
        if(self.west is not None):
            count +=1
        return count
        

    # DisplayStuff
    def displayField(self):
        print("Field #%d, row: %d, col: %d, neighbours:%d" % (self.number, self.row, self.column, self.numNeighbours()))

    def showNeighbours(self):
        print("N: %s, S: %s, E: %s, W: %s" % (self.number, self.north is not None, self.south is not None, self.east is not None, self.west is not None ))
    
    def isOccupied(self):
        return self.piece is not None and self.line is not None

class GameBoard:
    def __init__(self, cols, rows):
        super().__init__()
        self.columns = cols
        self.rows = rows
        self.fields = []
        self.populateFields()
    
    def populateFields(self):
        
        for row in range(1, self.rows+1):
            for column in range(1, self.columns+1):
                self.fields.append(Field(row, column))
        
        # Set southern neighbours (also sets northern neighbours)
        for idx, f in enumerate(self.fields):
            if(idx < (len(self.fields)-self.columns)):
                f.setSouth(self.fields[idx + self.columns])
        
        # Set eastern neighbours
        for idx, f in enumerate(self.fields):
            if((idx +1) % self.columns != 0):
                f.setEast(self.fields[idx + 1])
        
    
    def printBoard(self):
        for f in self.fields:
            f.displayField()
            
gb = GameBoard(5,10)
gb.printBoard()

#f1 = Field(2,2)
#f2 = Field(4,4)
#f3 = Field(4,3)
#f1.addPiece(Piece('red'))
#f2.setWest(f3)
#
#print("%d pieces" % Piece.pieceCount)
#print("%d fields" % Field.fieldCount)
#
#f1.displayField()
#print(f1.isOccupied())
#print(f1.displayNeighbours())
#
#f2.displayField()
#print(f2.isOccupied())
#print(f2.displayNeighbours())
#
#f3.displayField()
#print(f3.isOccupied())
#print(f3.displayNeighbours())

