from gameboard import Piece, Field, GameBoard
import colored

"""

Testing board and solver
========================

Layout: 

1,1 red
3,1 green
5,1 yellow

3,2 blue
5,2 orange

2,4 green
4,4 yellow

2,5 red
3,5 blue
4,5 orange


Red path: 
1,1 -> 1,2 -> 1,3 -> 1,4 -> 1,5 -> 2,5
S,S,S,S,E

Green path: 
3,1 -> 2,1 -> 2,2 -> 2,3 -> 2,4
W,S,S,S

"""


def getColor(color):
    if(color == 'R'):
        return colored.fg(1)
    if(color == 'G'):
        return colored.fg(2)
    if(color == 'Y'):
        return colored.fg(3)
    if(color == 'B'):
        return colored.fg(4)
    if(color == 'O'):
        return colored.fg(214)

def prettyPrintFields(fields, columns):
    for idx, f in enumerate(fields):
        ender = ''
        if((idx + 1) % columns == 0):
            ender  = "\n"
        if(f.isOccupied()):
            if(f.piece is not None):
                print(getColor(f.piece.color) + f.piece.color, end = ender)
            if(f.line is not None):
                print(getColor(f.line) + '-', end = ender)
        else:
            print(colored.fg(15) + '_', end = ender)

gb = GameBoard(5, 5)
gb.fields[ 0].addPiece(Piece('R')) #Red
gb.fields[21].addPiece(Piece('R')) #Red
gb.fields[ 2].addPiece(Piece('G')) #Green
gb.fields[16].addPiece(Piece('G')) #Green
gb.fields[ 7].addPiece(Piece('B')) #Blue
gb.fields[22].addPiece(Piece('B')) #Blue
gb.fields[ 4].addPiece(Piece('Y')) #Yellow
gb.fields[18].addPiece(Piece('Y')) #Yellow
gb.fields[ 9].addPiece(Piece('O')) #Orange
gb.fields[23].addPiece(Piece('O')) #Orange

# red line for visual:
gb.fields[ 5].addLine('R') #Red
gb.fields[10].addLine('R') #Red
gb.fields[15].addLine('R') #Red
gb.fields[20].addLine('R') #Red

# Green line for visual
gb.fields[ 1].addLine('G') #Green
gb.fields[ 6].addLine('G') #Green
gb.fields[11].addLine('G') #Green

#gb.printBoard()
prettyPrintFields(gb.fields, gb.columns)