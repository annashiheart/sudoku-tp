try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from homeScreen import *
from playScreen import *

##################################
# prefScreen
##################################

def prefScreen_onScreenStart(app):
    app.largeButtonWidth = 600
    app.largeButtonHeight = 75

def prefScreen_onKeyPress(app, key):
    if key == 'escape': setActiveScreen('homeScreen')

def prefScreen_redrawAll(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
            fill=None, border='gainsboro', borderWidth = app.boardBorderWidth)
    instructions =  [f'contest mode: {app.contestMode}',
                    f'show legals: {app.showLegals}',
                    f'edit legals: {app.legalsEditMode}',
                    f'font color: {app.legalsEditMode}',
                    f'selection color: {app.legalsEditMode}',
                    f'hover color: {app.legalsEditMode}',
                    f'hint color: {app.legalsEditMode}',
                    f'incorrect color: {app.legalsEditMode}',]
    toggles =       ['c',
                    'l',
                    'n',
                    'f',
                    's',
                    'o',
                    'h',
                    'i',]
    for i in range(len(instructions)):
        drawLabel(instructions[i], app.boardLeft + 40, app.boardTop + 40 + i*20, size=16, align='left-top', font = 'monospace')
        drawLabel(toggles[i], app.boardRight - 40, app.boardTop + 40 + i*20, size=16, align='left-top', font = 'monospace')

    # drawRightSide(app)
    drawLeftSide(app)

def drawRightSide(app): # delete this later
    drawRect(app.boardRightSide, app.boardTop, app.buttonWidth, 2*app.buttonHeight, fill = 'lightGrey')
    drawLabel(f'{app.mistakes}', app.boardRightSide + app.buttonWidth/2, app.boardTop + app.buttonHeight, fill='black', size = 20, font = 'monospace')

def drawLeftSide(app):
    drawRect(app.boardLeftSide, app.boardTop + 200, app.buttonWidth, app.buttonHeight, fill = 'lightGrey')
    drawLabel('home(esc)', app.boardLeftSide + app.buttonWidth/2, app.boardTop + 200 + app.buttonHeight/2, fill='black', size = 20, font = 'monospace')

def prefScreen_onMousePress(app, mouseX, mouseY):
    # left side
    if ((app.boardLeftSide <= mouseX <= app.boardLeftSide + app.buttonWidth) and 
        (app.boardTop + 200 <= mouseY <= app.boardTop + 200 + app.buttonHeight)):
        setActiveScreen('homeScreen')
