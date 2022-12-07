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

def prefScreen_redrawAll(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
            fill=None, border='gainsboro', borderWidth = app.boardBorderWidth)
    instructions =  [f'contest mode: {app.contestMode}',
                    f'show legals: {app.showLegals}',
                    f'edit legals: {app.legalsEditMode}',
                    f'font color: {app.fontColor}',
                    f'selection color: {app.selectionColor}',
                    f'hover color: {app.hoverColor}',
                    f'number selection color: {app.selectionColorNum}',
                    f'number hover color: {app.hoverColorNum}',
                    f'hint color: {app.hintColor}',
                    f'incorrect color: {app.incorrectColor}',]
    toggles =       ['c',
                    'l',
                    'n',
                    'f',
                    's',
                    'o',
                    't',
                    'v',
                    'h',
                    'i',]
    drawLabel('Press the key on the left to change the setting', app.boardLeft + 40, app.boardTop + 40, size=16, align='left-top', font = 'monospace')
    for i in range(len(instructions)):
        drawLabel(instructions[i], app.boardLeft + 80, app.boardTop + 60 + i*20, size=16, align='left-top', font = 'monospace')
        drawLabel(toggles[i], app.boardLeft + 40, app.boardTop + 60 + i*20, size=16, align='left-top', font = 'monospace')

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

def prefScreen_onKeyPress(app, key):
    if key == 'escape': setActiveScreen('homeScreen')
    elif key == 'c':
        app.contestMode = not app.contestMode
    elif key == 'l':
        app.showLegals = not app.showLegals
    elif key == 'n':
        app.legalsEditMode = not app.legalsEditMode
    elif key == 'f':
        app.fontColor = app.getTextInput('new font color')
    elif key == 's':
        app.selectionColor = app.getTextInput('new selection color')
    elif key == 'o':
        app.hoverColor = app.getTextInput('new hover color')
    elif key == 'h':
        app.hintColor = app.getTextInput('new hint color')
    elif key == 'i':
        app.fontColor = app.getTextInput('new incorrect color')
