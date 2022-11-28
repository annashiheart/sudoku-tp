try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from playScreen import *
from homeScreen import *

##################################
# main
##################################

def main():
    runAppWithScreens(initialScreen='homeScreen')

main()