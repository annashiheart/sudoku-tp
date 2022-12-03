try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *

##################################
# helpScreen
##################################

def helpScreen_onScreenStart(app):
    app.largeButtonWidth = 600
    app.largeButtonHeight = 75

def helpScreen_onKeyPress(app, key):
    if key == 'escape': setActiveScreen('homeScreen')
    if key == 'r' and (app.board != None): setActiveScreen('playScreen')

def helpScreen_redrawAll(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
            fill=None, border='gainsboro', borderWidth = app.boardBorderWidth)
    instructions = ['press esc to return to the home page',
                    'press r to resume your game',
                    'press s to use a hint (show cell)',
                    'press S to autoplay a value',
                    'press e to toggle edit mode for initial board',
                    'press l to toggle show legals',
                    'press n to toggle edit mode for legals',
                    'press u to undo move',
                    'press r to redo move',
                    'use keyboard arrows to move across the board',
                    'use backspace to delete a number',]
    for i in range(len(instructions)):
        drawLabel(instructions[i], app.width/2, app.boardTop + 40 + i*20, size=16, font = 'monospace')
    # drawRightSide(app)
    drawLeftSide(app)

def drawRightSide(app): # delete this later
    drawRect(app.boardRightSide, app.boardTop, app.buttonWidth, 2*app.buttonHeight, fill = 'lightGrey')
    drawLabel(f'{app.mistakes}', app.boardRightSide + app.buttonWidth/2, app.boardTop + app.buttonHeight, fill='black', size = 20, font = 'monospace')

def drawLeftSide(app):
    drawRect(app.boardLeftSide, app.boardTop + 200, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('home(esc)', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 200 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')
    drawRect(app.boardLeftSide, app.boardTop + 280, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('resume(r)', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 280 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')

def helpScreen_onMousePress(app, mouseX, mouseY):
    # left side
    if ((app.boardLeftSide <= mouseX <= app.boardLeftSide + app.buttonWidth) and 
        (app.boardTop + 200 <= mouseY <= app.boardTop + 200 + app.buttonHeight)):
        setActiveScreen('homeScreen')
    elif ((app.boardLeftSide <= mouseX <= app.boardLeftSide + app.buttonWidth) and 
        (app.boardTop + 280 <= mouseY <= app.boardTop + 280 + app.buttonHeight) and
        (app.board != None)):
        setActiveScreen('playScreen')