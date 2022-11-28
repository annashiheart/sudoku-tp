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
    drawLabel('helpScreen', app.width/2, 30, size=16)
    drawRect(app.width/2 - app.largeButtonWidth/2, 550, app.largeButtonWidth, app.largeButtonHeight, fill = 'gainsboro')
    drawLabel('return home', app.width/2, 550 + app.largeButtonHeight/2, size=48, font = 'monospace')

def helpScreen_onMousePress(app, mouseX, mouseY):
    # return home
    if ((app.width/2 - app.largeButtonWidth/2 <= mouseX <= app.width/2 + app.largeButtonWidth/2) and 
        (550 <= mouseY <= 550 + app.largeButtonHeight)):
        setActiveScreen('homeScreen')