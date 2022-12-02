try: from cmu_cs3_graphics import *
except: from cmu_graphics import *
import random
import copy

from runAppWithScreens import *

##################################
# homeScreen
##################################

def homeScreen_onScreenStart(app):
    app.width = 1200
    app.height = 800
    app.largeButtonWidth = 600
    app.largeButtonHeight = 75
    app.smallButtonWidth = 120
    app.smallButtonHeight = 50
    app.level = None
    app.board = None
    app.inputTextMode = False
    app.inputText = ''

def homeScreen_onKeyPress(app, key):
    if app.inputTextMode: 
        if key == 'backspace':
            app.inputText = app.inputText[:-1]
        elif key != 'enter':
            app.inputText += key
        elif key == 'enter':
            app.inputTextMode = False
            newBoard = readFile(f'tp-starter-files/boards/{app.inputText}.png.txt')
            app.board = boardTo2DList(newBoard)
            app.solutionBoard = solveSudoku(app, app.board)
            app.initialVals = findInitialVals(app.board)
            app.boardEditMode = False
            app.legalsBoard = findInitialLegalsBoard(app)
            appStarted(app)
            setActiveScreen('playScreen')

    elif key == 'e': 
        app.level = 'easy'
        createBoard(app)
        setActiveScreen('playScreen')
    elif key == 'm': 
        app.level = 'medium'
        createBoard(app)
        setActiveScreen('playScreen')
    elif key == 'h': 
        app.level = 'hard'
        createBoard(app)
        setActiveScreen('playScreen')
    elif key == 'v': 
        app.level = 'evil'
        createBoard(app)
        setActiveScreen('playScreen')
    elif key == 'c': 
        app.level = 'custom'
        createBoard(app)
        setActiveScreen('playScreen')
    elif key == 'u': 
        app.inputTextMode = True
    elif key == 'r' and app.board!=None: setActiveScreen('playScreen')
    elif key == 'g': setActiveScreen('helpScreen')


def homeScreen_redrawAll(app):
    drawLabel('sudoku', app.width/2, 150, size=140, font = 'monospace',)
    drawRect(app.width/2 - app.largeButtonWidth/2, 250, app.largeButtonWidth, 2*app.largeButtonHeight, fill = 'gainsboro')

    # go to play
    drawLabel('new game', app.width/2, 250 + app.largeButtonHeight/2, size=48, font = 'monospace')
    drawRect(app.width/2 - 2*app.smallButtonWidth - 36, 325, app.smallButtonWidth, app.smallButtonHeight, fill = 'whiteSmoke')
    drawRect(app.width/2 - app.smallButtonWidth - 12, 325, app.smallButtonWidth, app.smallButtonHeight, fill = 'whiteSmoke')
    drawRect(app.width/2 + 12, 325, app.smallButtonWidth, app.smallButtonHeight, fill = 'whiteSmoke')
    drawRect(app.width/2 + app.smallButtonWidth + 36, 325, app.smallButtonWidth, app.smallButtonHeight, fill = 'whiteSmoke')
    drawLabel('easy(e)', app.width/2 - 1.5*app.smallButtonWidth - 36, 350, size=20, font = 'monospace')
    drawLabel('medium(m)', app.width/2 - 0.5*app.smallButtonWidth - 12, 350, size=20, font = 'monospace')
    drawLabel('hard(d)', app.width/2 + 0.5*app.smallButtonWidth + 12, 350, size=20, font = 'monospace')
    drawLabel('evil(v)', app.width/2 + 1.5*app.smallButtonWidth + 36, 350, size=20, font = 'monospace')

    # create game
    drawRect(app.width/2 - app.largeButtonWidth/2, 420, 2*app.smallButtonWidth + 48, app.largeButtonHeight, fill = 'gainsboro')
    drawLabel('create (c)', app.width/2 - app.smallButtonWidth - 36, 420 + app.largeButtonHeight/2, size=30, font = 'monospace')

    # upload game
    drawRect(app.width/2 + 12, 420, 2*app.smallButtonWidth + 48, app.largeButtonHeight, fill = 'gainsboro')
    drawLabel('upload (u)', app.width/2 + 36 + app.smallButtonWidth, 420 + app.largeButtonHeight/2, size=30, font = 'monospace')
    
    if app.inputTextMode:
        drawRect(app.width/2 - app.largeButtonWidth/2, 610, app.largeButtonWidth, app.largeButtonHeight, fill = 'gainsboro')
        drawLabel('write level-number:', app.width/2, 635, size=20, font = 'monospace')
        drawLabel(app.inputText, app.width/2, 665, size=20, font = 'monospace')

    # resume board
    drawRect(app.width/2 - app.largeButtonWidth/2, 515, 2*app.smallButtonWidth + 48, app.largeButtonHeight, fill = 'gainsboro')
    drawLabel('resume (r)', app.width/2 - app.smallButtonWidth - 36, 515 + app.largeButtonHeight/2, size=30, font = 'monospace')

    # go to help
    drawRect(app.width/2 + 12, 515, 2*app.smallButtonWidth + 48, app.largeButtonHeight, fill = 'gainsboro')
    drawLabel('guide (g)', app.width/2 + 36 + app.smallButtonWidth, 515 + app.largeButtonHeight/2, size=30, font = 'monospace')


def homeScreen_onMousePress(app, mouseX, mouseY):
    # new game
    if ((app.width/2 - 2*app.smallButtonWidth - 36 <= mouseX <= app.width/2 - app.smallButtonWidth - 36) and 
        (325 <= mouseY <= 325 + app.smallButtonHeight)):
        app.level = 'easy'
        createBoard(app)
        setActiveScreen('playScreen')
    elif ((app.width/2 - app.smallButtonWidth - 12 <= mouseX <= app.width/2 - 12) and 
        (325 <= mouseY <= 325 + app.smallButtonHeight)):
        app.level = 'medium'
        createBoard(app)
        setActiveScreen('playScreen')
    elif ((app.width/2 + 12 <= mouseX <= app.width/2 + app.smallButtonWidth + 12) and 
        (325 <= mouseY <= 325 + app.smallButtonHeight)):
        app.level = 'hard'
        createBoard(app)
        setActiveScreen('playScreen')
    elif ((app.width/2 + app.smallButtonWidth + 36 <= mouseX <= app.width/2 + 2*app.smallButtonWidth + 36) and 
        (325 <= mouseY <= 325 + app.smallButtonHeight)):
        app.level = 'evil'
        createBoard(app)
        setActiveScreen('playScreen')

    # create
    if ((app.width/2 - app.largeButtonWidth/2 <= mouseX <= app.width/2 - app.largeButtonWidth/2 + 2*app.smallButtonWidth + 48) and 
        (420 <= mouseY <= 420 + app.largeButtonHeight)):
        app.level = 'custom'
        createBoard(app)
        setActiveScreen('playScreen')
    # upload
    elif ((app.width/2 + 12 <= mouseX <= app.width/2 + 60 + 2*app.smallButtonWidth) and 
        (420 <= mouseY <= 420 + app.largeButtonHeight)):
        app.inputTextMode = True
    # resume
    elif ((app.width/2 - app.largeButtonWidth/2 <= mouseX <= app.width/2 - app.largeButtonWidth/2 +  2*app.smallButtonWidth + 48) and 
        (515 <= mouseY <= 515 + app.largeButtonHeight)):
        if app.board != None:
            setActiveScreen('playScreen')
    # guide
    if ((app.width/2 + 12 <= mouseX <= app.width/2 + 60 + 2*app.smallButtonWidth) and 
        (515 <= mouseY <= 515 + app.largeButtonHeight)):
        setActiveScreen('helpScreen') 

##################################
# CHOOSE AND READ FILE
##################################

def chooseRandomNumber(app):
    if app.level == 'evil':
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

##################################
# CREATE BOARDS
##################################

def createBoard(app):
    if app.level != 'custom':
        randomNumber = chooseRandomNumber(app)
        newBoard = readFile(f'tp-starter-files/boards/{app.level}-{randomNumber}.png.txt')
        app.board = boardTo2DList(newBoard)
        app.solutionBoard = solveSudoku(app, app.board)
        app.initialVals = findInitialVals(app.board)
        app.boardEditMode = False
    else:
        app.board = [['0' for v in range(app.cols)] for w in range(app.rows)]
        app.boardEditMode = True
        app.solutionBoard = copy.deepcopy(app.board)
        app.initialVals = set()
    app.legalsBoard = findInitialLegalsBoard(app)
    appStarted(app)

def appStarted(app):
    app.selection = None
    app.hoverSelection = None
    app.hoverNumber = None
    app.isGameOver = False
    app.paused = False
    app.mistakes = 0
    app.showLegals = False
    app.legalsEditMode = False 
    app.autoPlayOn = False

def findInitialVals(board):
    initialVals = set()
    for row in range(len(board)):
        for col in range(len(board[0])):
            initialNum = board[row][col]
            if (initialNum != '0'):
                initialVals.add((row, col))
    return initialVals

def findInitialLegalsBoard(app):
    board = [[None for v in range(app.rows)] for y in range(app.cols)]
    for row in range(app.rows):
        for col in range(app.cols):
            block = row//3 * 3 + col//3
            cellLegals = Legals(app.board, row, col, block)
            board[row][col] = cellLegals
            if app.board[row][col] != '0':
                board[row][col].legals = {app.board[row][col]}
    return board

##################################
# FIND LEGALS
##################################

class Legals():
    def __init__(self, board, row, col, block):
        self.board = board
        self.row = row
        self.col = col
        self.block = block
        self.illegals = findValuesinRow(self.board, self.row) | findValuesinCol(self.board, self.col) | findValuesinBlock(self.board, self.block)
        self.legals = {'1','2','3','4','5','6','7','8','9'} - self.illegals
        self.manualLegals = set()
        self.manualIllegals = set()
        self.shownLegals = (self.legals | self.manualLegals) - self.manualIllegals

def setAndBanLegals(cellLegals, key):
    if key in cellLegals.manualLegals:
        cellLegals.manualLegals.remove(key)
    elif key in cellLegals.manualIllegals:
        cellLegals.manualIllegals.remove(key)
    elif key in cellLegals.legals:
        cellLegals.manualIllegals.add(key)
    elif key in cellLegals.illegals:
        cellLegals.manualLegals.add(key)
    cellLegals.shownLegals = (cellLegals.legals | cellLegals.manualLegals) - cellLegals.manualIllegals

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

##################################
# FIND BOARD SOLUTION
##################################

def solveSudoku(app, board):
    board = copy.deepcopy(board)
    if findNextEmptyCellFromHere(app, board, -1, app.cols) == None:
        return board
    else:
        if findNextEmptyCellFromHere
        row, col = findNextEmptyCellFromHere(app, board, -1, app.cols)
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

def findNextSingletonCell(app, board, givenRow, givenCol):
    app.selection = findNextEmptyCellFromHere(app, app.board, givenRow, givenCol)
    if app.selection == None:
        return None
    row, col = app.selection
    cellLegals = app.legalsBoard[row][col]
    if len(cellLegals.shownLegals) == 1:
        for value in cellLegals.shownLegals:
            return row, col, app.solutionBoard[row][col]
    else:
        return findNextSingletonCell(app, app.board, row, col)
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
