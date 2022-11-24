from cmu_cs3_graphics import *
import math
import random

def onAppStart(app):
    app.rows = 9
    app.cols = 9
    app.boardLeft = 50
    app.boardTop = 50
    app.boardWidth = 300
    app.boardHeight = 300
    app.cellBorderWidth = 1
    app.selection = None
    app.hoverSelection = None
    appStarted(app)

def appStarted(app):
    # randomize this later
    newBoard = readFile('tp-starter-files/boards/easy-01.png.txt')
    app.board = boardTo2DList(newBoard)
    app.initialVals = findInitialVals(app.board)
    app.isGameOver = False
    app.paused = False
    app.stepsPerSecond = 1
    app.score = 0

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
            num = board[row][col]
            if (num != '0'):
                initialVals.add((row, col))
    return initialVals

def redrawAll(app):
    drawGameLabels(app)
    drawBoard(app)
    drawBoardBorder(app)
    drawNumberBoxes(app)
    if app.isGameOver:
        drawGameOver(app)

def drawGameLabels(app):
    if not app.isGameOver:
        drawLabel('Sudoku', 200, 20, size=16)
        drawLabel('Term project', 200, 36, size = 12)

def drawGameOver(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, 
            app.boardHeight, fill= 'black', opacity = 80)
    drawLabel('Game Over!', 200, 180, size = 26, 
            fill = 'white', bold = True)
    drawLabel(f'You scored {app.score} points!', 
            200, 220, size = 20, fill = 'white')
    drawLabel('Press r to restart', 200, 320, size = 20, fill = 'white')

def drawNumberBoxes(app):
    cellWidth, cellHeight = getCellSize(app)
    for i in range(9):
        drawRect(app.boardLeft + i*(app.boardWidth/9), 
                app.boardTop + app.boardHeight + 5, 
                app.boardWidth/9, app.boardHeight/9, 
                fill = 'lavenderBlush', border = 'black', borderWidth = 1)
        drawLabel(i+1, app.boardLeft + i*(app.boardWidth/9) + cellWidth/2, 
                app.boardTop + app.boardHeight + 5 + cellHeight/2, size = 16)
    drawRect(app.boardLeft, app.boardTop + app.boardHeight + 5,
            app.boardWidth, app.boardHeight/9, fill = None, border = 'black')

def onMousePress(app, mouseX, mouseY):
    if not app.isGameOver:
        selectedCell = getCell(app, mouseX, mouseY)
        selectedNum = getNumberFromBox(app, mouseX, mouseY)
        if (selectedCell != None) and (selectedCell not in app.initialVals):
            if selectedCell != app.selection:
                app.selection = selectedCell 
            else:
                app.selection = None
        elif (selectedNum != None) and (app.selection != None):
            row, col = app.selection
            app.board[row][col] = str(selectedNum)

def onMouseMove(app, mouseX, mouseY):
    if not app.isGameOver:
        selectedCell = getCell(app, mouseX, mouseY)
        if (selectedCell != None) and (selectedCell != app.selection):
            app.hoverSelection = selectedCell
        else:
            app.hoverSelection = None

def onKeyPress(app, key):
    if key == 'd':
        print(app.selection)
    if key == 'b':
        print(app.board)
    if (app.selection != None) and (key in '123456789'):
        row, col = app.selection
        app.board[row][col] = key
    if (app.selection != None) and (key == 'backspace'):
        row, col = app.selection
        app.board[row][col] = '0'
                
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)
            num = app.board[row][col]
            if (num != '0'):
                drawNum(app, row, col, num)

def drawBoardBorder(app):
    # draw the board outline (with double-thickness):
    for i in range(3):
        for j in range(3):
            drawRect(app.boardLeft + i*(app.boardWidth/3), 
                    app.boardTop + j*(app.boardHeight/3), 
                    app.boardWidth/3, app.boardHeight/3,
                    fill=None, border='black',
                    borderWidth=2*app.cellBorderWidth)
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
            fill=None, border='black', borderWidth=4*app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    # add diff color for initial vals and added vals
    if (row, col) in app.initialVals:
        color = 'gainsboro'
    elif (row, col) == app.selection:
        color = 'pink'
    elif (row, col) == app.hoverSelection:
        color = 'lavenderBlush'
    else:
        color = None
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
           fill=color, border='black',
           borderWidth=app.cellBorderWidth)

def drawNum(app, row, col, num):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    color = 'black'
    drawLabel(num, cellLeft + cellWidth/2, cellTop + cellHeight/2, 
            fill=color, size = 16)

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

def main():
    runApp()

main()