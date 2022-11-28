from cmu_cs3_graphics import *
import math
import random
import copy

##################################
# FOR DEBUGGING PURPOSES
##################################
def prettyPrint(L):
    for row in L:
        print(row)

##################################
# CHOOSE AND READ FILE
##################################

def chooseRandomNumber(level):
    if level == 4:
        randomBoardNumber = random.choice(range(25)) + 1
    else:
        randomBoardNumber = random.choice(range(50)) + 1
    if randomBoardNumber < 10:
        randomBoardNumber = '0' + str(randomBoardNumber)
    return str(randomBoardNumber)

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def boardTo2DList(board):
    L = []
    for line in board.splitlines():
        M = line.split(' ')
        L.append(M)
    return L

def findInitialVals(board):
    initialVals = set()
    for row in range(len(board)):
        for col in range(len(board[0])):
            initialNum = board[row][col]
            if (initialNum != '0'):
                initialVals.add((row, col))
    return initialVals

##################################
# ANIMATION VIEW
##################################

def playScreen_onScreenStart(app):
    app.width = 1200
    app.height = 800
    app.rows = 9
    app.cols = 9
    app.boardLeft = 300
    app.boardTop = 50
    app.boardWidth = 600
    app.boardHeight = 600
    app.cellBorderWidth = 2
    app.blockBorderWidth = 1.5 * app.cellBorderWidth
    app.boardBorderWidth = 2 * app.blockBorderWidth
    app.boardLeftSide = app.boardLeft - app.boardWidth/9 - 150
    app.boardRightSide = app.boardLeft + app.boardWidth/9*10
    app.buttonWidth = 150
    app.buttonHeight = 50
    appStarted(app)

def appStarted(app):
    # randomize this for level
    newBoard = readFile(f'tp-starter-files/boards/easy-{chooseRandomNumber(1)}.png.txt')
    app.board = boardTo2DList(newBoard)
    app.solutionBoard = solveSudoku(app, app.board)
    app.initialVals = findInitialVals(app.board)
    app.selection = None
    app.hoverSelection = None
    app.hoverNumber = None
    app.isGameOver = False
    app.paused = False
    app.mistakes = 0
    app.showLegals = False

def playScreen_redrawAll(app):
    if app.isGameOver:
        drawGameOver(app) # change this to a screen!
    else:
        drawBoard(app)
        drawNumberBoxes(app)
        drawBoardBorder(app)
        drawRightSide(app)
        drawLeftSide(app)

def drawGameOver(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, 
            app.boardHeight, fill = 'black', opacity = 50)
    drawLabel('You won!', app.width/2, app.height/2 - 100, size = 40, 
            fill = 'white', bold = True)
    drawLabel(f'You made {app.mistakes} mistakes!', 
            app.width/2, app.height/2 + 100, size = 30, fill = 'white')

def drawNumberBoxes(app):
    cellWidth, cellHeight = getCellSize(app)
    for i in range(9):
        color = 'pink' if i+1 == app.hoverNumber else 'lavenderBlush'
        drawRect(app.boardLeft + i*(app.boardWidth/9), 
                app.boardTop + app.boardHeight + 20, 
                app.boardWidth/9, app.boardHeight/9, 
                fill = color, border = 'black', borderWidth = 1)
        drawLabel(i+1, app.boardLeft + i*(app.boardWidth/9) + cellWidth/2, 
                app.boardTop + app.boardHeight + 20 + cellHeight/2, size = 28)
    # draw border for number boxes
    drawRect(app.boardLeft, app.boardTop + app.boardHeight + 20,
            app.boardWidth, app.boardHeight/9, fill = None, border = 'black',
            borderWidth = app.cellBorderWidth)
    # draw delete symbol
    trashSymbol = chr(0x1f5d1)
    drawRect(app.boardLeft + 9.5 * (app.boardWidth/9), app.boardTop + app.boardHeight + 20, 
            app.boardWidth/9, app.boardHeight/9, 
            fill = 'gainsboro', border = 'black', borderWidth = app.cellBorderWidth)
    drawLabel(trashSymbol, app.boardLeft + 9.5*(app.boardWidth/9) + cellWidth/2, 
            app.boardTop + app.boardHeight + 20 + cellHeight/2, size = 28, font='symbols')
                
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)
            cellNum = app.board[row][col]
            if (cellNum != '0'):
                drawCellNum(app, row, col, cellNum)
            elif app.showLegals:
                drawLegals(app, row, col)

def drawBoardBorder(app):
    # draw the blocks
    for i in range(3):
        for j in range(3):
            drawRect(app.boardLeft + i*(app.boardWidth/3), 
                    app.boardTop + j*(app.boardHeight/3), 
                    app.boardWidth/3, app.boardHeight/3,
                    fill=None, border='black',
                    borderWidth = app.blockBorderWidth)
    # draw the outer border
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
            fill=None, border='black', borderWidth = app.boardBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    # differentiate initial and player numbers
    if (row, col) in app.initialVals:
        color = 'gainsboro'
    elif (row, col) == app.selection:
        color = 'lightBlue'
    elif (row, col) == app.hoverSelection:
        color = 'aliceBlue'
    else:
        color = None
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
           fill=color, border='black', borderWidth=app.cellBorderWidth)

def drawCellNum(app, row, col, cellNum):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    # change number color if right or wrong
    if cellNum == app.solutionBoard[row][col]:
        color = 'black'
    else:
        color = 'red'
    drawLabel(cellNum, cellLeft + cellWidth/2, cellTop + cellHeight/2, 
            fill=color, size = 28,)

def drawRightSide(app):
    drawRect(app.boardRightSide, app.boardTop, app.buttonWidth, 2*app.buttonHeight, fill = 'lightGrey')
    drawLabel(f'{app.mistakes}', app.boardRightSide + app.buttonWidth/2, app.boardTop + app.buttonHeight, fill='black', size = 28,)
    drawRect(app.boardRightSide, app.boardTop + 130, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('hint', app.boardRightSide + app.buttonWidth/2, app.boardTop + 130 + app.buttonHeight/2, fill='black', size = 28,)

def drawLeftSide(app):
    drawRect(app.boardLeftSide, app.boardTop + 200, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('home', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 200 + app.buttonHeight/2, fill='black', size = 28,)
    drawRect(app.boardLeftSide, app.boardTop + 280, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('help', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 280 + app.buttonHeight/2, fill='black', size = 28,)
    drawRect(app.boardLeftSide, app.boardTop + 360, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('legals on', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 360 + app.buttonHeight/2, fill='black', size = 28,)

def drawLegals(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    for i in range(9):
        block = row//3 * 3 + col//3
        # will likely have to move this so that it doesn't reset every time it's drawn
        cellLegals = Legals(app.board, row, col, block)
        if str(i+1) in cellLegals.legals:
            legalRow = i//3 + 1
            legalCol = i%3 + 1
            legalSpacing = (app.boardWidth//9) / 4
            drawLabel(i+1, cellLeft + legalCol*legalSpacing, 
                    cellTop + legalRow*legalSpacing, fill='grey',)


##################################
# ANIMATION KEY AND MOUSE
##################################

def playScreen_onMousePress(app, mouseX, mouseY):
    if not app.isGameOver:
        selectedCell = getCell(app, mouseX, mouseY)
        selectedNum = getNumberFromBox(app, mouseX, mouseY)
        if (selectedCell != None) and (selectedCell not in app.initialVals):
            if selectedCell != app.selection:
                app.selection = selectedCell
            else:
                app.selection = None
        # fill cell by mouse
        elif (selectedNum != None) and (app.selection != None):
            selectedNum = str(selectedNum)
            addNumber(app, selectedNum)
        # delete number by mouse
        elif ((app.selection != None) and
            (app.boardLeft + 9.5 * (app.boardWidth/9) <= mouseX <= app.boardLeft + 10.5 * (app.boardWidth/9)) and 
            (app.boardTop + app.boardHeight + 20 <= mouseY <= app.boardTop + app.boardHeight + 20 + app.boardHeight/9)):
            addNumber(app, '0')

def playScreen_onMouseMove(app, mouseX, mouseY):
    if not app.isGameOver:
        selectedCell = getCell(app, mouseX, mouseY)
        selectedNum = getNumberFromBox(app, mouseX, mouseY)
        if (selectedCell != None) and (selectedCell != app.selection):
            app.hoverSelection = selectedCell
        elif (selectedNum != None):
            app.hoverNumber = selectedNum
        else: # add hover over number boxes
            app.hoverSelection = None
            app.hoverNumber = None

def playScreen_onKeyPress(app, key):
    if key == 'l':
        app.showLegals = not app.showLegals
    if app.selection != None:
        row, col = app.selection
        if key == 'right':
            app.selection = findNextEmptyCellFromHere(app, app.board, row, col)
        if key in '123456789':
            addNumber(app, key)
        if key == 'backspace':
            addNumber(app, '0')
        if key == 's':
            row, col = app.selection
            block = row//3 * 3 + col//3
            cellLegals = Legals(app.board, row, col, block)
            if len(cellLegals.legals) == 1:
                for value in cellLegals.legals:
                    app.board[row][col] = value
            else:
                app.selection = findNextEmptyCellFromHere(app, app.board, row, col)
    if app.selection == None:
        if key == 'right':
            app.selection = findNextEmptyCellFromHere(app, app.board, -1, app.cols)
        if key == 's':
            app.selection = findNextEmptyCellFromHere(app, app.board, -1, app.cols)



##################################
# ANIMATION CONTROLLER
##################################

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
        return (row, col)
    else:
        return None

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def getNumberFromBox(app, x, y):
    for i in range(9):
        if ((app.boardLeft + i*(app.boardWidth/9) <= x <= app.boardLeft + (i+1)*(app.boardWidth/9)) and
            (app.boardTop + app.boardHeight + 5 <= y <= app.boardTop + app.boardHeight + 5 + app.boardHeight/9)):
            return i+1
    return None


##################################
# FIND BOARD SOLUTION
##################################

def solveSudoku(app, board):
    board = copy.deepcopy(board) # is this bad
    if findNextEmptyCellFromHere(app, board, 0, 0) == None:
        return board
    else:
        row, col = findNextEmptyCellFromHere(app, board, 0, 0)
        for i in range(1,10):
            board[row][col] = str(i)
            if isBoardLegal(app, board):
                solution = solveSudoku(app, board) 
                if solution != None:
                    return solution
            board[row][col] = '0'
        return None

def findNextEmptyCellFromHere(app, board, givenRow, givenCol):
    for row in range(givenRow, app.rows):
        for col in range(app.cols):
            if board[row][col] == '0' and not (row == givenRow and col <= givenCol):
                return row, col
    return None

def isBoardLegal(app, board):
    for row in range(app.rows):
        if not isLegalRow(board, row):
            return False
    for col in range(app.cols):
        if not isLegalCol(board, col):
            return False
    blocks = app.rows
    for block in range(blocks):
        if not isLegalBlock(board, block):
            return False
    return True

def areLegalValues(L):
    seen = set()
    for value in L:
        if value != '0' and value in seen:
            return False
        seen.add(value)
    return True

def isLegalRow(board, row):
    return areLegalValues(board[row])
    
def isLegalCol(board, col):
    rows = len(board)
    values = [board[row][col] for row in range(rows)]
    return areLegalValues(values)

def isLegalBlock(board, block):
    blockSize = 3
    startRow = block // blockSize * blockSize
    startCol = block % blockSize * blockSize
    values = []
    for drow in range(blockSize):
        for dcol in range(blockSize):
            row, col = startRow + drow, startCol + dcol
            values.append(board[row][col])
    return areLegalValues(values)

##################################
# CHECK FOR WIN
##################################

def addNumber(app, number):
    row, col = app.selection
    app.board[row][col] = number
    # check if mistake
    if (number != app.solutionBoard[row][col]) and (number != '0'):
            app.mistakes += 1
    # check if game over
    if app.board == app.solutionBoard:
        app.isGameOver = True


##################################
# FIND LEGALS
##################################

class Legals():
    def __init__(self, board, row, col, block):
        self.board = board
        self.row = row
        self.col = col
        self.block = block
        illegalSet = findValuesinRow(self.board, self.row) | findValuesinCol(self.board, self.col) | findValuesinBlock(self.board, self.block)
        self.legals = {'1','2','3','4','5','6','7','8','9'} - illegalSet
    
    def printLegals(self):
        print(self.legals)
    
    def setLegal(self, num):
        self.legals.add(num)
    
    def banLegal(self, num):
        self.legals.remove(num)

def findValues(L):
    seen = set()
    for value in L:
        if value != '0':
            seen.add(value)
    return seen

def findValuesinRow(board, row):
    return findValues(board[row])
    
def findValuesinCol(board, col):
    rows = len(board)
    values = [board[row][col] for row in range(rows)]
    return findValues(values)

def findValuesinBlock(board, block):
    blockSize = 3
    startRow = block // blockSize * blockSize
    startCol = block % blockSize * blockSize
    values = []
    for drow in range(blockSize):
        for dcol in range(blockSize):
            row, col = startRow + drow, startCol + dcol
            values.append(board[row][col])
    return findValues(values)
"""
##################################
# RUN APP
##################################

def main():
    runApp()

main()
"""