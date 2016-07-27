# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 03:19:22 2016

@author: juan
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys, time
import image_qr

app = QApplication(sys.argv)
# Create and display the splash screen
splash_pix = QPixmap(':/SpecPy.png')
splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
#progressBar = QProgressBar(splash)
#splash.setMask(splash_pix.mask())
splash.show()
time.sleep(3)
app.processEvents()
#for i in range(0, 20):
#    progressBar.setValue(i)
#    t = time.time()
#    while time.time() < t + 0.1:
#       app.processEvents()

#time.sleep(2)
#app.processEvents()

# Simulate something that takes time
from SpecPy import *

if not os.path.exists(PATH):
    os.makedirs(PATH)
else:
    temp = glob.glob(PATH+'/*.jpg')
    for item in temp:
        os.remove(item)
   
camara = 0
#time.sleep(3)
cam = GuiWindow("Stream", camara, PATH)
splash.finish(None)
cam.loop()
sys.exit()
#sys.exit(app.exec_())
