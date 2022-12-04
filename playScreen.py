from cmu_cs3_graphics import *
import math

from runAppWithScreens import *
from homeScreen import *

##################################
# playScreen
##################################

# delete this after debugging
def prettyPrint(L):
    for row in L:
        print(row)

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
    app.stepsPerSecond = 2
    app.undoList = []
    app.redoList = []
    app.bannedWrongLegalCoords = []

def playScreen_redrawAll(app):
    drawBoard(app)
    drawNumberBoxes(app)
    drawBoardBorder(app)
    drawRightSide(app)
    drawLeftSide(app)
    if app.isGameOver: 
        drawGameOver(app) # change this to screen?
        if app.contestMode:
            saveFile(app)

def drawGameOver(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, 
                app.boardHeight, fill = 'black', opacity = 80)
    if app.solutionBoard == None:
        drawLabel('Invalid board!', app.width/2, app.height/2 - 100, size = 40, 
                fill = 'white', bold = True, font = 'monospace')
        drawLabel(f'Return home to try again', 
                app.width/2, app.height/2 - 50, size = 30, fill = 'white', font = 'monospace')
    elif app.solutionBoard == app.board:
        drawLabel('You won!', app.width/2, app.height/2 - 100, size = 40, 
                fill = 'white', bold = True, font = 'monospace')
        mistakePlural = 'mistake' if app.mistakes==1 else 'mistakes'
        drawLabel(f'You made {app.mistakes} {mistakePlural}!', 
                app.width/2, app.height/2 - 50, size = 30, fill = 'white', font = 'monospace')
    elif app.mistakes > 0 and app.contestMode:
        drawLabel('You lost!', app.width/2, app.height/2 - 100, size = 40, 
                fill = 'white', bold = True, font = 'monospace')
        drawLabel(f'You made a mistake in a contest.', 
                app.width/2, app.height/2 - 50, size = 30, fill = 'white', font = 'monospace')


def drawNumberBoxes(app):
    cellWidth, cellHeight = getCellSize(app)
    for i in range(9):
        color = 'pink' if i+1 == app.hoverNumber else 'lavenderBlush'
        drawRect(app.boardLeft + i*(app.boardWidth/9), 
                app.boardTop + app.boardHeight + 20, 
                app.boardWidth/9, app.boardHeight/9, 
                fill = color, border = 'black', borderWidth = 1)
        drawLabel(i+1, app.boardLeft + i*(app.boardWidth/9) + cellWidth/2, 
                app.boardTop + app.boardHeight + 20 + cellHeight/2, size = 28,
                bold = True, font = 'monospace')
    # draw border 
    drawRect(app.boardLeft, app.boardTop + app.boardHeight + 20,
            app.boardWidth, app.boardHeight/9, fill = None, border = 'black',
            borderWidth = app.cellBorderWidth)
                
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
           fill=color, border='dimGray', borderWidth=app.cellBorderWidth)

def drawCellNum(app, row, col, cellNum):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if app.solutionBoard == None:
        color = 'grey'
    elif app.contestMode:
        color = 'black'
    elif cellNum == app.solutionBoard[row][col]:
        color = 'black'
    else:
        color = 'red'
    drawLabel(cellNum, cellLeft + cellWidth/2, cellTop + cellHeight/2, 
            fill=color, size = 28, font = 'monospace')

def drawRightSide(app):
    # top half
    drawRect(app.boardRightSide, app.boardTop, app.buttonWidth, 2*app.buttonHeight, fill = 'lightGrey')
    drawLabel(f'{app.mistakes}', app.boardRightSide + app.buttonWidth/2, app.boardTop + app.buttonHeight, fill='black', size = 20, font = 'monospace')
    drawRect(app.boardRightSide, app.boardTop + 130, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('delete(del)', app.boardRightSide + app.buttonWidth/2, app.boardTop + 130 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')
    drawRect(app.boardRightSide, app.boardTop + 205, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('undo(u)', app.boardRightSide + app.buttonWidth/2, app.boardTop + 205 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')
    drawRect(app.boardRightSide, app.boardTop + 280, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('redo(r)', app.boardRightSide + app.buttonWidth/2, app.boardTop + 280 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')
    # bottom half
    color = 'grey' if app.boardEditMode else 'lightGrey'
    drawRect(app.boardRightSide, app.boardTop + 400, app.buttonWidth, app.buttonHeight, fill = color)
    drawLabel('edit(e)', app.boardRightSide + app.buttonWidth/2, app.boardTop + 400 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')
    color = 'grey' if app.showLegals else 'lightGrey'
    drawRect(app.boardRightSide, app.boardTop + 475, app.buttonWidth, app.buttonHeight, fill = color)
    drawLabel('legals(l)', app.boardRightSide + app.buttonWidth/2, app.boardTop + 475 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')
    color = 'grey' if app.legalsEditMode else 'lightGrey'
    drawRect(app.boardRightSide, app.boardTop + 550, app.buttonWidth, app.buttonHeight, fill = color)
    drawLabel('notes(n)', app.boardRightSide + app.buttonWidth/2, app.boardTop + 550 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')

def drawLeftSide(app):
    color = 'grey' if app.contestMode else 'lightGrey'
    drawRect(app.boardLeftSide, app.boardTop + 120, app.buttonWidth, app.buttonHeight, fill = color)
    drawLabel('contest(c)', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 120 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')
    drawRect(app.boardLeftSide, app.boardTop + 40, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('save(f)', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 40 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')
    drawRect(app.boardLeftSide, app.boardTop + 200, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('home(esc)', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 200 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')
    drawRect(app.boardLeftSide, app.boardTop + 280, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('guide(g)', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 280 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')
    drawRect(app.boardLeftSide, app.boardTop + 360, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('autoplay(s)', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 360 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')
    drawRect(app.boardLeftSide, app.boardTop + 440, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('hint(h)', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 440 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')

def drawLegals(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    for i in range(9):
        cellLegals = app.legalsBoard[row][col]
        if str(i+1) in cellLegals.shownLegals:
            legalRow = i//3 + 1
            legalCol = i%3 + 1
            legalSpacing = (app.boardWidth//9) / 4
            drawLabel(i+1, cellLeft + legalCol*legalSpacing, 
                    cellTop + legalRow*legalSpacing, fill='grey',)
        elif (not app.contestMode and
            (str(i+1) in cellLegals.manualIllegals) and 
            (str(i+1) == app.solutionBoard[row][col]) and 
            ((row, col) in app.bannedWrongLegalCoords)):
            legalRow = i//3 + 1
            legalCol = i%3 + 1
            legalSpacing = (app.boardWidth//9) / 4
            drawLabel(i+1, cellLeft + legalCol*legalSpacing, 
                    cellTop + legalRow*legalSpacing, fill='maroon')

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
        elif (selectedNum != None) and (app.selection != None):
            selectedNum = str(selectedNum)
            # input custom board
            if app.boardEditMode:
                row, col = app.selection
                app.solutionBoard[row][col] = selectedNum
                app.board[row][col] = selectedNum
                cellLegals = app.legalsBoard[row][col]
                app.legalsBoard = findInitialLegalsBoard(app)
            # change legals
            elif app.legalsEditMode:
                row, col = app.selection
                cellLegals = app.legalsBoard[row][col]
                setAndBanLegals(cellLegals, selectedNum)
                # user bans legal that is in solution
                if ((selectedNum == app.solutionBoard[row][col]) and 
                    (selectedNum in cellLegals.manualIllegals)):
                    app.bannedWrongLegalCoords.append((row, col))
            # input actual value
            else:
                addNumber(app, selectedNum)
    # left side
    if ((app.boardLeftSide <= mouseX <= app.boardLeftSide + app.buttonWidth) and 
        (app.boardTop + 120 <= mouseY <= app.boardTop + 120 + app.buttonHeight)):
        app.contestMode = not app.contestMode
    elif ((app.boardLeftSide <= mouseX <= app.boardLeftSide + app.buttonWidth) and 
        (app.boardTop + 40 <= mouseY <= app.boardTop + 40 + app.buttonHeight)):
        saveFile(app)
    elif ((app.boardLeftSide <= mouseX <= app.boardLeftSide + app.buttonWidth) and 
        (app.boardTop + 200 <= mouseY <= app.boardTop + 200 + app.buttonHeight)):
        setActiveScreen('homeScreen')
    elif ((app.boardLeftSide <= mouseX <= app.boardLeftSide + app.buttonWidth) and 
        (app.boardTop + 280 <= mouseY <= app.boardTop + 280 + app.buttonHeight)):
        setActiveScreen('helpScreen')
    elif ((app.boardLeftSide <= mouseX <= app.boardLeftSide + app.buttonWidth) and 
        (app.boardTop + 360 <= mouseY <= app.boardTop + 360 + app.buttonHeight)):
        hint1(app, True)
    elif ((app.boardLeftSide <= mouseX <= app.boardLeftSide + app.buttonWidth) and 
        (app.boardTop + 440 <= mouseY <= app.boardTop + 440 + app.buttonHeight)):
        hint1(app, False)

    # right side
    # top half
    elif ((app.selection != None) and
        (app.boardRightSide <= mouseX <= app.boardRightSide + app.buttonWidth) and 
        (app.boardTop + 130 <= mouseY <= app.boardTop + 130 + app.buttonHeight)):
        addNumber(app, '0')
    elif ((app.boardRightSide <= mouseX <= app.boardRightSide + app.buttonWidth) and 
        (app.boardTop + 205 <= mouseY <= app.boardTop + 205 + app.buttonHeight)):
        undoMove(app)
    elif ((app.boardRightSide <= mouseX <= app.boardRightSide + app.buttonWidth) and 
        (app.boardTop + 280 <= mouseY <= app.boardTop + 280 + app.buttonHeight)):
        redoMove(app)
    # bottom half
    elif ((app.boardRightSide <= mouseX <= app.boardRightSide + app.buttonWidth) and 
        (app.boardTop + 400 <= mouseY <= app.boardTop + 400 + app.buttonHeight)):
        app.solutionBoard = solveSudoku(app, app.board)
        if app.solutionBoard == None:
            app.isGameOver = True
        app.initialVals = findInitialVals(app.board)
        app.boardEditMode = not app.boardEditMode
    elif ((app.boardRightSide <= mouseX <= app.boardRightSide + app.buttonWidth) and 
        (app.boardTop + 475 <= mouseY <= app.boardTop + 475 + app.buttonHeight)):
        app.showLegals = not app.showLegals
    elif ((app.boardRightSide <= mouseX <= app.boardRightSide + app.buttonWidth) and 
        (app.boardTop + 550 <= mouseY <= app.boardTop + 550 + app.buttonHeight)):
        app.legalsEditMode = not app.legalsEditMode

def playScreen_onMouseMove(app, mouseX, mouseY):
    if not app.isGameOver:
        selectedCell = getCell(app, mouseX, mouseY)
        selectedNum = getNumberFromBox(app, mouseX, mouseY)
        if (selectedCell != None) and (selectedCell != app.selection):
            app.hoverSelection = selectedCell
            app.hoverNumber = None
        elif (selectedNum != None):
            app.hoverSelection = None
            app.hoverNumber = selectedNum
        else: # add hover over number boxes
            app.hoverSelection = None
            app.hoverNumber = None

def playScreen_onKeyPress(app, key):
    # debugging functions
    print(key)
    if key == 'p':
        if app.selection != None:
            row, col = app.selection
        print(findNextEmptyCellFromHere(app, app.board,  -1, app.cols))
    # game functions
    if key == 'c':
        app.contestMode = not app.contestMode
    if key == 'f':
        saveFile(app)
    if key == 'escape':
        setActiveScreen('homeScreen')
    if key == 'g':
        setActiveScreen('helpScreen')
    if key == 'l':
        app.showLegals = not app.showLegals
    if key == 'e':
        app.solutionBoard = solveSudoku(app, app.board)
        if app.solutionBoard == None:
            app.isGameOver = True
        app.initialVals = findInitialVals(app.board)
        app.boardEditMode = not app.boardEditMode
    if key == 'h':
        hint1(app, False)
    if key == 's': # check this later
        hint1(app, True)
    # add key for 'A', autoplay all singletons
    if key == 'u': # undo
        undoMove(app)
    if key == 'r': # redo
        redoMove(app)
    if key == 'n':
        app.legalsEditMode = not app.legalsEditMode 
    if app.selection != None:
        row, col = app.selection
        if key in {'right', 'left', 'up', 'down'}:
            app.selection = findNextEditableCellFromHere(app, row, col, key)
        if key in '123456789':
            if app.boardEditMode:
                row, col = app.selection
                app.solutionBoard[row][col] = key
                app.board[row][col] = key
                cellLegals = app.legalsBoard[row][col]
                app.legalsBoard = findInitialLegalsBoard(app)
            elif app.legalsEditMode:
                row, col = app.selection
                cellLegals = app.legalsBoard[row][col]
                setAndBanLegals(cellLegals, key)
                # user bans legal that is in solution
                if ((key == app.solutionBoard[row][col]) and 
                    (key in cellLegals.manualIllegals)):
                    app.bannedWrongLegalCoords.append((row, col))

            else:
                addNumber(app, key)
        if key == 'backspace':
            if app.boardEditMode:
                row, col = app.selection
                app.solutionBoard[row][col] = '0'
                app.board[row][col] = '0'
            elif not app.legalsEditMode:
                addNumber(app, '0')
    if app.selection == None:
        if key == 'right':
            app.selection = findNextEmptyCellFromHere(app, app.board, -1, app.cols)

def playScreen_onStep(app):
    if app.autoPlayOn and findNextSingletonCell(app, app.board, -1, app.cols) != None:
        hint1(app, True)
        
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
# FIND CELLS
##################################

def findNextEditableCellFromHere(app, givenRow, givenCol, dir):
    if dir == 'right':
        for row in range(givenRow, app.rows):
            for col in range(app.cols):
                if (row, col) not in app.initialVals and not (row == givenRow and col <= givenCol):
                    return row, col
    elif dir == 'left':
        for row in range(givenRow, -1, -1):
            for col in range(app.cols, -1, -1):
                if (row, col) not in app.initialVals and not (row == givenRow and col >= givenCol):
                    return row, col
    elif dir == 'up':
        for col in range(givenCol, -1, -1):
            for row in range(app.rows, -1, -1):
                if (row, col) not in app.initialVals and not (row >= givenRow and col == givenCol):
                    return row, col
    elif dir == 'down':
        for col in range(givenCol, app.cols):
            for row in range(app.rows):
                if (row, col) not in app.initialVals and not (row <= givenRow and col == givenCol):
                    return row, col
    return None

##################################
# PLAYER MOVES
##################################

def addNumber(app, number):
    row, col = app.selection
    prevValue = app.board[row][col]
    # do nothing if new number same as current
    if prevValue == number:
        return
    # save previous board
    app.undoList.append(State(app.board, row, col, prevValue)) 
    # clear redo moves
    app.redoList = []
    # update board value
    app.board[row][col] = number
    # check if mistake
    if (number != app.solutionBoard[row][col]) and (number != '0'):
            app.mistakes += 1
    # check if player lost (contest mode)
    if app.mistakes > 0 and app.contestMode:
        app.isGameOver = True
    # check if player won
    if app.board == app.solutionBoard:
        app.isGameOver = True
        app.selection = None
        app.hoverSelection = None
    # update legals after move
    updateLegals(app, number, row, col, prevValue)

def undoMove(app):
    if app.undoList != []:
        prevState = app.undoList.pop()
        # save current state to redo
        currValue = app.board[prevState.row][prevState.col]
        app.redoList.append(State(app.board, prevState.row, prevState.col, currValue))
        # reinstate previous state
        app.board = prevState.board
        app.selection = (prevState.row, prevState.col)
        # update legals
        updateLegals(app, prevState.val, prevState.row, prevState.col, currValue)

def redoMove(app):
    if app.redoList != []:
        nextState = app.redoList.pop()
        # save current state to undo
        prevValue = app.board[nextState.row][nextState.col]
        app.undoList.append(State(app.board, nextState.row, nextState.col, prevValue))
        # reinstate redo state
        app.board = nextState.board
        app.selection = (nextState.row, nextState.col)
        # update legals
        updateLegals(app, nextState.val, nextState.row, nextState.col, prevValue)

def updateLegals(app, number, row, col, prevValue):
    app.bannedWrongLegalCoords = []
    block = row//3 * 3 + col//3
    for rowIndex in range(len(app.legalsBoard)):
        for colIndex in range(len(app.legalsBoard[rowIndex])):
            blockIndex = rowIndex//3 * 3 + colIndex//3
            cellLegals = app.legalsBoard[rowIndex][colIndex]
            if number == '0': # fix
                if (rowIndex == row) or (colIndex == col) or (blockIndex == block) and not ((rowIndex == row) and (colIndex == col)):
                    if prevValue not in cellLegals.shownLegals and prevValue in cellLegals.legals:
                        cellLegals.manualIllegals.remove(prevValue)
                    cellLegals.shownLegals = (cellLegals.legals | cellLegals.manualLegals) - cellLegals.manualIllegals
            else:
                if ((rowIndex == row) or (colIndex == col) or (blockIndex == block)) and not ((rowIndex == row) and (colIndex == col)) :
                    if number in cellLegals.legals and number in cellLegals.shownLegals:
                        cellLegals.manualIllegals.add(number)
                    cellLegals.shownLegals = (cellLegals.legals | cellLegals.manualLegals) - cellLegals.manualIllegals
                    if prevValue != number and prevValue in cellLegals.legals and number not in cellLegals.shownLegals:
                        cellLegals.manualIllegals.remove(prevValue)
                    cellLegals.shownLegals = (cellLegals.legals | cellLegals.manualLegals) - cellLegals.manualIllegals

##################################
# PROVIDE HINTS
##################################

def hint1(app, setValue):
    if app.contestMode:
        return
    if app.selection == None:
        row, col = -1, app.cols
    else:
        row, col = app.selection
    if findNextSingletonCell(app, app.board, row, col) != None:
        singletonRow, singletonCol, value = findNextSingletonCell(app, app.board, row, col)
        app.selection = singletonRow, singletonCol
        if setValue:
            addNumber(app, value)
    app.autoPlayOn = False
"""
def hint2(app): # finish this.
    import itertools
    L = [ col1, col2, col3, row1, row2, row3, block1, block2, block3, etc.]
    print('Here are all the regions (lists of cells and legals):')
    print('Here are all the combinations of 2-5 legals in a region:')
    # loop through regions
        for N in range(2,6):
            for M in itertools.combinations(L, N):
                # for combination of certain cells of size N
                # want to see if they have a combination of N legals
                # if N = 2, and two cells have 5, 6 and 5, 6 as legals
                # highlight the cells
                # check each cell's legals
                # add to cell
"""
##################################
# STATE CLASS
##################################

class State():
    def __init__(self, board, row, col, val):
        self.board = copy.deepcopy(board) 
        self.legals = [] # fix this to undo/redo legal set/ban
        self.row = row
        self.col = col
        self.val = val
