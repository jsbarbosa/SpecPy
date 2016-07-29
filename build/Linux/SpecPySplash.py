# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 19:36:14 2016

@author: juan
"""

from PyQt4.uic import loadUiType
from PyQt4 import QtCore, QtGui
import sys, image_qr
 
app = QtGui.QApplication(sys.argv)
# Create and display the splash screen
splash_pix = QtGui.QPixmap(':/SpecPy.png')
splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
splash.show()
app.processEvents()

import SpecPy as specpy
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas)

Ui_MainWindow, QMainWindow = loadUiType('mainwindow.ui')
CAMARA = 0
STREAMHEIGHT = 100
STREAMWIDTH = int(4/3*STREAMHEIGHT)#300

PATH = "Captures"

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        self.posSlider.valueChanged.connect(self.posChange)
        self.sizeSlider.valueChanged.connect(self.sizeChange)
        icon = QtGui.QIcon(':/SpecPy.png')
        self.setWindowIcon(icon)
        
        self.show()
        
    def videoStream(self):
        self.cam = specpy.GuiWindow("Stream", CAMARA, STREAMWIDTH, STREAMHEIGHT, PATH, "canvas")#, self.MainWindow)
        self.fig_num = 0
    def qImage(self, width, height, bytesPerLine):
        qImg = QtGui.QImage(self.cam.frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(qImg)
        return pix
        
    def update(self):
        i = 0
        while self.fig_num != None:
            height = self.CamaraStream.frameGeometry().height()
            width = int(4/3*height)            
            self.cam.changeHeight(height)
            self.cam.changeWidth(width)
            bytesPerLine = 3 * width
            answer = self.cam.eachPhotogram()
            if not answer:
                break
            if i == 0:
                self.updatePlot()
                i += 1
            else:
                self.removePlot()
                self.updatePlot()
            pix = self.qImage(width, height, bytesPerLine)
            self.CamaraStream.setPixmap(pix)
            
    def keyPressEvent(self, event):
        keyPressed = event.key() #& 0xff
        if keyPressed == QtCore.Qt.Key_Escape: 
            self.cam.closeInput()
            self.close()
        elif keyPressed == QtCore.Qt.Key_Enter - 1:
            self.fig_num = self.cam.captureData(self.cam.analysisFrame, self.fig_num)
        elif keyPressed == QtCore.Qt.Key_C:
            self.cam.cleanData()
    
    def updatePlot(self):
        self.canvas = FigureCanvas(self.cam.figure)
        self.figureFrame.addWidget(self.canvas)
        self.canvas.draw()
        
    def removePlot(self):
        self.figureFrame.removeWidget(self.canvas)
        self.canvas.close()
    
    def posChange(self):
        size = self.posSlider.value()
        self.cam.posTrackBar(size)
        
    def sizeChange(self):
        size = self.sizeSlider.value()
        self.cam.rangeTrackBar(size)
    
#aw = ApplicationWindow()
#aw.setWindowTitle("Try")
#aw.show()
splash.finish(None)
#app.exec_() 
app = QtGui.QApplication(sys.argv)
main = Main()
main.videoStream()    
main.update()
sys.exit()
#app.exec_()