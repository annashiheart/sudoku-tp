try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from playScreen import *
from screen1 import *

##################################
# main
##################################

def main():
    runAppWithScreens(initialScreen='playScreen', width = 1200, height = 800)

main()