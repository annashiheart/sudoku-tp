try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *

##################################
# homeScreen
##################################

def homeScreen_onScreenStart(app):
    app.width = 1200
    app.height = 800

def homeScreen_onKeyPress(app, key):
    if key == 's': setActiveScreen('playScreen')

def homeScreen_redrawAll(app):
    drawLabel('SUDOKU', app.width/2, 200, size=128)
    drawLabel('Press d to change direction of dot', app.width/2, 50, size=16)
    drawLabel('Press s to change the screen to screen1', app.width/2, 70, size=16)
