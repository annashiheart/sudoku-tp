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
    if key == 'h': setActiveScreen('homeScreen')

def helpScreen_redrawAll(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
            fill=None, border='gainsboro', borderWidth = app.boardBorderWidth)
    instructions = ['press h to return to the home page',
                    'press g to return to your game',
                    'press s to use a hint (get a value)',
                    'press S to watch the solution (easy only)',
                    'press the right arrow to move to the next cell',
                    'press the backspace button to delete a move']
    for i in range(len(instructions)):
        drawLabel(instructions[i], app.width/2, app.boardTop + 40 + i*40, size=20, font = 'monospace')
    drawRightSide(app)
    drawLeftSide(app)

def drawRightSide(app):
    drawRect(app.boardRightSide, app.boardTop, app.buttonWidth, 2*app.buttonHeight, fill = 'lightGrey')
    drawLabel(f'{app.mistakes}', app.boardRightSide + app.buttonWidth/2, app.boardTop + app.buttonHeight, fill='black', size = 28, font = 'monospace')

def drawLeftSide(app):
    drawRect(app.boardLeftSide, app.boardTop + 200, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('home', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 200 + app.buttonHeight/2, fill='black', size = 28, font = 'monospace')
    drawRect(app.boardLeftSide, app.boardTop + 280, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('game', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 280 + app.buttonHeight/2, fill='black', size = 28, font = 'monospace')


def helpScreen_onMousePress(app, mouseX, mouseY):
    # left side
    if ((app.boardLeftSide <= mouseX <= app.boardLeftSide + app.buttonWidth) and 
        (app.boardTop + 200 <= mouseY <= app.boardTop + 200 + app.buttonHeight)):
        setActiveScreen('homeScreen')
    elif ((app.boardLeftSide <= mouseX <= app.boardLeftSide + app.buttonWidth) and 
        (app.boardTop + 280 <= mouseY <= app.boardTop + 280 + app.buttonHeight)):
        setActiveScreen('playScreen')