try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

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

def homeScreen_onKeyPress(app, key):
    if key == 's': setActiveScreen('playScreen')

def homeScreen_redrawAll(app):
    drawLabel('sudoku', app.width/2, 250, size=140, font = 'monospace',)
    drawRect(app.width/2 - app.largeButtonWidth/2, 350, app.largeButtonWidth, 2*app.largeButtonHeight, fill = 'gainsboro')

    # go to play
    drawLabel('new game', app.width/2, 350 + app.largeButtonHeight/2, size=48, font = 'monospace')
    drawRect(app.width/2 - 2*app.smallButtonWidth - 36, 425, app.smallButtonWidth, app.smallButtonHeight, fill = 'whiteSmoke')
    drawRect(app.width/2 - app.smallButtonWidth - 12, 425, app.smallButtonWidth, app.smallButtonHeight, fill = 'whiteSmoke')
    drawRect(app.width/2 + 12, 425, app.smallButtonWidth, app.smallButtonHeight, fill = 'whiteSmoke')
    drawRect(app.width/2 + app.smallButtonWidth + 36, 425, app.smallButtonWidth, app.smallButtonHeight, fill = 'whiteSmoke')
    drawLabel('easy', app.width/2 - 1.5*app.smallButtonWidth - 36, 450, size=24, font = 'monospace')
    drawLabel('medium', app.width/2 - 0.5*app.smallButtonWidth - 12, 450, size=24, font = 'monospace')
    drawLabel('hard', app.width/2 + 0.5*app.smallButtonWidth + 12, 450, size=24, font = 'monospace')
    drawLabel('evil', app.width/2 + 1.5*app.smallButtonWidth + 36, 450, size=24, font = 'monospace')

    # go to help
    drawRect(app.width/2 - app.largeButtonWidth/2, 550, app.largeButtonWidth, app.largeButtonHeight, fill = 'gainsboro')
    drawLabel('how to play', app.width/2, 550 + app.largeButtonHeight/2, size=48, font = 'monospace')

def homeScreen_onMousePress(app, mouseX, mouseY):
    # new game
    if ((app.width/2 - 2*app.smallButtonWidth - 36 <= mouseX <= app.width/2 - app.smallButtonWidth - 36) and 
        (425 <= mouseY <= 425 + app.smallButtonHeight)):
        setActiveScreen('playScreen')
    # open help
    if ((app.width/2 - app.largeButtonWidth/2 <= mouseX <= app.width/2 + app.largeButtonWidth/2) and 
        (550 <= mouseY <= 550 + app.largeButtonHeight)):
        setActiveScreen('helpScreen')