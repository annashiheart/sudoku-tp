from cmu_cs3_graphics import *
import math


def onAppStart(app):
    app.rows = 9
    app.cols = 9
    app.boardLeft = 50
    app.boardTop = 50
    app.boardWidth = 300
    app.boardHeight = 300
    app.cellBorderWidth = 2
    app.selection = None
    appStarted(app)

def appStarted(app):
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.isGameOver = False
    app.paused = False
    app.stepsPerSecond = 1
    app.score = 0

def redrawAll(app):
    drawBoard(app)
    if not app.isGameOver:
        drawLabel('Tetris', 200, 15, size=16)
        drawLabel(f'Level: {app.score//100+1}', 
                200, 375, size=12)
    drawBoardBorder(app)
    if app.isGameOver:
        drawRect(app.boardLeft, app.boardTop, app.boardWidth, 
                app.boardHeight, fill= 'black', opacity = 80)
        drawLabel('Game Over!', 200, 180, size = 26, 
                    fill = 'white', bold = True)
        drawLabel(f'You scored {app.score} points!', 
                    200, 220, size = 20, fill = 'white')
        drawLabel('Press r to restart', 200, 320, size = 20,
                    fill = 'white')
    elif app.paused:
        drawLabel('Press p to unpause', 200, 30, size = 12)
        drawLabel(f'Score: {app.score}', 200, 390, size = 12)
    else:
        drawLabel('Press p to pause', 200, 30, size = 12)
        drawLabel(f'Score: {app.score}', 200, 390, size = 12)

def onMousePress(app, mouseX, mouseY):
    app.selection = None
    if not app.isGameOver:
        cell = getCell(app, mouseX, mouseY)
        if cell != None:
            row, col = cell
            if app.board[row][col] == None:
                makeMove(app, row, col)

def onMouseMove(app, mouseX, mouseY):
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell == None:
        app.selection = None
    else:
        row, col = selectedCell
        if app.board[row][col] == None:
            app.selection = selectedCell
        else:
            app.selection = None

def makeMove(app, row, col):
    app.board[row][col] = 'red'

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.board[row][col])

def drawBoardBorder(app):
    # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth/3, app.boardHeight/3,
           fill=None, border='brown',
           borderWidth=2*app.cellBorderWidth/3)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)


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


def main():
    runApp()

main()