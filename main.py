from cmu_cs3_graphics import *
import math

def onAppStart(app):
    app.rows = 9
    app.cols = 9
    app.boardLeft = 50
    app.boardTop = 50
    app.boardWidth = 300
    app.boardHeight = 300
    app.cellBorderWidth = 1
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
        drawLabel('Sudoku', 200, 20, size=16)
        drawLabel('Term project', 200, 36, size = 12)
    drawBoardBorder(app)
    if app.isGameOver:
        drawGameOver(app)

def drawGameOver(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, 
            app.boardHeight, fill= 'black', opacity = 80)
    drawLabel('Game Over!', 200, 180, size = 26, 
            fill = 'white', bold = True)
    drawLabel(f'You scored {app.score} points!', 
            200, 220, size = 20, fill = 'white')
    drawLabel('Press r to restart', 200, 320, size = 20,
            fill = 'white')

def onMousePress(app, mouseX, mouseY):
    if not app.isGameOver:
        selectedCell = getCell(app, mouseX, mouseY)
        if selectedCell != None:
            if selectedCell == app.selection:
                app.selection = None
            else:
                app.selection = selectedCell

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
        app.board[row][col] = None


def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)
            num = app.board[row][col]
            if num != None:
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
    color = 'lavenderBlush' if (row, col) == app.selection else None
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


def main():
    runApp()

main()