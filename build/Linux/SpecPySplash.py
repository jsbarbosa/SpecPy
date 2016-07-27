# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 03:19:22 2016

@author: juan
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys, time
import image_qr
import itertools

#def variablename(var):
#    return [tpl[0] for tpl in itertools.filter(lambda x: var is x[1], globals().items())]

SETTINGS_FILE = "settings.cpy"
CAMARA = 0
PATH = "Captured"
STREAMWIDTH = 680
STREAMHEIGHT = 480

app = QApplication(sys.argv)
# Create and display the splash screen
splash_pix = QPixmap(':/SpecPy.png')
splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
splash.show()
time.sleep(3)
app.processEvents()

from SpecPy import *
        
def settingsReader(settingsfile):
    instructions = []
    file = open(settingsfile, 'r')
    lines = file.readlines()
    for line in lines:
        parted_line = line.rpartition('=')
        command = parted_line[0].replace(' ', '')
        value = parted_line[-1].replace(' ', '').replace('\n', '')
        instructions.append((command, value))
    file.close()
    return instructions

def settingsApplier(instructions):
    global CAMARA, PATH, STREAMWIDTH, STREAMHEIGHT
    for instruction in instructions:
        command, value = instruction
        if command == "camara":
            if value.isdigit():
                CAMARA = int(value)
            else:
                CAMARA = value
            print("Camara set to: ", value)
        elif command == "path":
            PATH = value
            print("Path set to:", value)
        elif command == "streamheight":
            STREAMHEIGHT = int(value)
            print("Stream height set to:", value)
        elif command == "streamwidth":
            STREAMWIDTH = int(value)
            print("Stream width set to:", value)

def settingsHandler(settingsfile):
    if os.path.exists(settingsfile):
        instructions = settingsReader(settingsfile)
    else:
        file = open(settingsfile, "w")
        file.write("camara =" + str(0)+"\n")
        file.write("path = " + PATH + "\n")
        file.write("streamheight = " + str(STREAMHEIGHT) + "\n")
        file.write("streamwidth = " + str(STREAMWIDTH) + "\n")
        file.close()
        instructions = settingsReader(settingsfile)
    settingsApplier(instructions)
    
settingsHandler(SETTINGS_FILE)

if not os.path.exists(PATH):
    os.makedirs(PATH)
else:
    temp = glob.glob(PATH+'/*.jpg')
    for item in temp:
        os.remove(item)
        
cam = GuiWindow("Stream", CAMARA, STREAMWIDTH, STREAMHEIGHT, PATH)
splash.finish(None)
cam.loop()
sys.exit()
