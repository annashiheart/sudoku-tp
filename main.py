try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from homeScreen import *
from playScreen import * 
from helpScreen import *

##################################
# main
##################################

def main():
    runAppWithScreens(initialScreen='homeScreen')

main()