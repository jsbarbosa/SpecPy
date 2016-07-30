# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 19:36:14 2016

@author: juan
"""

from PyQt4.uic import loadUiType
from PyQt4 import QtCore, QtGui
import sys, GUI_data#, time
 
app = QtGui.QApplication(sys.argv)
# Create and display the splash screen
splash_pix = QtGui.QPixmap(':/SpecPy.png')
splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
splash.show()
#time.sleep(3)
app.processEvents()

import SpecPy as specpy
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas)

Ui_MainWindow, QMainWindow = loadUiType('mainwindow.ui')
CAMARA = 0
CAPTUREWIDTH = 680
CAPTUREHEIGHT = 480
STREAMWIDTH = 100
STREAMHEIGHT = int(3*STREAMWIDTH/4)

PATH = "../Captures"
POS = int(CAPTUREHEIGHT/2)
SIZE = int(POS/2)
BRIGHTNESS = 50
CONTRAST = 50
SATURATION = 50
HUE = 50
GAIN = 50
EXPOSURE = 50

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        
        icon = QtGui.QIcon(':/Icon.png')
        self.setWindowIcon(icon)
        
        self.coeffWH = CAPTUREHEIGHT/CAPTUREWIDTH
        
        self.objectName = self.objectLine.text()
        
        self.path = PATH
        self.directoryLine.setText(self.path)        
        
        self.pathCleaner(True)
        self.videoStream()
        
        self.posSlider.valueChanged.connect(self.posChange)
        self.posSlider.setMinimum(0)
        self.posSlider.setMaximum(CAPTUREHEIGHT)
        self.posSlider.setValue(POS)        
        
        self.sizeSlider.valueChanged.connect(self.sizeChange)
        self.sizeSlider.setMinimum(0)
        self.sizeSlider.setMaximum(POS)
        self.sizeSlider.setValue(SIZE)        
        
        self.brightnessSlider.valueChanged.connect(self.brightnessChange)        
        self.contrastSlider.valueChanged.connect(self.contrastChange)
        self.saturationSlider.valueChanged.connect(self.saturationChange)
        self.hueSlider.valueChanged.connect(self.hueChange)        
        self.gainSlider.valueChanged.connect(self.gainChange)
        self.exposureSlider.valueChanged.connect(self.exposureChange)
        
        self.captureButton.clicked.connect(self.captureData)
        self.cleanButton.clicked.connect(self.cam.cleanData)
        self.resetButton.clicked.connect(self.resetSettings)
        
        self.comboBox_2.addItem("680 x 480")
        self.comboBox_2.addItem("1280 x 720")
#        self.comboBox_2.addItem("1920 x 1080")
         
        self.comboBox_2.activated[str].connect(self.resolutionBox)
        
        self.canvas = None
        
    def videoStream(self):
        self.cam = specpy.GuiWindow("Stream", CAMARA, self.objectName, STREAMWIDTH, STREAMHEIGHT, PATH, 
                                   POS, SIZE, BRIGHTNESS, CONTRAST, SATURATION, HUE,
                                   GAIN, EXPOSURE, "canvas")
        self.updateImage()
        self.fig_num = 0              
        
    def qImage(self, width, height, bytesPerLine):
        qImg = QtGui.QImage(self.cam.frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(qImg)
        return pix
        
    def keyPressEvent(self, event):
        keyPressed = event.key()
        if keyPressed == QtCore.Qt.Key_Alt + QtCore.Qt.Key_F4: 
            self.cam.closeInput()
            self.close()
        elif keyPressed == QtCore.Qt.Key_Enter - 1:
            self.captureData()
        elif keyPressed == QtCore.Qt.Key_C:
            self.cam.cleanData()
            self.updatePlot()
        elif keyPressed == QtCore.Qt.Key_R:
            self.resetSettings()
            
    def updateImage(self):
        width = self.CamaraStream.frameGeometry().width()
        height = int(self.coeffWH*width)
        realHeight = self.CamaraStream.frameGeometry().height()
        if height > realHeight:
            width = int(realHeight/self.coeffWH)
            height = realHeight
        self.cam.changeHeight(height)
        self.cam.changeWidth(width)
        bytesPerLine = 3*width
        answer = self.cam.eachPhotogram()
        if answer:
            pix = self.qImage(width, height, bytesPerLine)
            self.CamaraStream.setPixmap(pix)
        
    def update(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.updateImage)
        timer.start(33)

        # Creates first plot
        self.updatePlot()
        
    def updatePlot(self):
        def create():
            figure = self.cam.figure
            if figure != None:
                self.canvas = FigureCanvas(figure)
                self.figureFrame.addWidget(self.canvas)
                self.canvas.draw()
            else:
                self.canvas == None
                
        def removePlot():
            self.figureFrame.removeWidget(self.canvas)
            self.canvas.close()
            
        if self.canvas == None:
            create()
        else:
            removePlot()
            create()
            
    def posSliderLimits(self):
        self.posSlider.setMinimum(0)
        temp = self.cam.analysisHeight
        self.posSlider.setMaximum(temp)#CAPTUREHEIGHT)
        self.posSlider.setValue(int(temp/2))
        
    def sizeSliderLimits(self):
        self.sizeSlider.setMinimum(0)
        temp = self.cam.analysisHeight
        self.sizeSlider.setMaximum(int(temp/2))
        self.sizeSlider.setValue(int(temp/4))
    
    def posChange(self):
        size = self.posSlider.value()
        self.cam.posTrackBar(size)
        
    def sizeChange(self):
        size = self.sizeSlider.value()
        self.cam.rangeTrackBar(size)
        
    def brightnessChange(self):
        size = self.brightnessSlider.value()
        self.cam.brightnessTrackBar(size)
        
    def contrastChange(self):
        size = self.contrastSlider.value()
        self.cam.contrastTrackBar(size)

    def saturationChange(self):
        size = self.saturationSlider.value()
        self.cam.saturationTrackBar(size)
        
    def hueChange(self):
        size = self.hueSlider.value()
        self.cam.hueTrackBar(size)
        
    def gainChange(self):
        size = self.gainSlider.value()
        self.cam.gainTrackBar(size)

    def exposureChange(self):
        size = self.exposureSlider.value()
        self.cam.exposureTrackBar(size)      
    
    def captureData(self):
        self.objectNameChanger()
        self.pathChanger()
        self.fig_num = self.cam.captureData(self.cam.notSquaredAnalysisFrame, self.fig_num)
        self.updatePlot()
        
    def resetSettings(self):
        self.cam.resetSettings(POS, SIZE, BRIGHTNESS, CONTRAST, SATURATION, HUE, GAIN, EXPOSURE)
        self.posSlider.setValue(POS)
        self.sizeSlider.setValue(SIZE)        
        self.brightnessSlider.setValue(BRIGHTNESS)
        self.contrastSlider.setValue(CONTRAST)
        self.saturationSlider.setValue(SATURATION)
        self.hueSlider.setValue(HUE)
        self.gainSlider.setValue(GAIN)
        self.exposureSlider.setValue(EXPOSURE)
        self.path = PATH
        self.directoryLine.setText(self.path)
        self.objectName = ""
        self.objectLine.setText(self.objectName)
        self.comboBox_2.setCurrentIndex(0)
        self.resolutionBox(self.comboBox_2.currentText())
        
    def closeEvent(self, event):
        self.cam.closeInput()
        self.close()
        
    def resolutionBox(self, text):
        parted_line = text.rpartition('x')
        width, _, height = parted_line
        width = int(width)
        height = int(height)
        self.coeffWH = height/width
        self.cam.setCaptureHeight(height)
        self.cam.setCaptureWidth(width)
        self.posSliderLimits()
        self.sizeSliderLimits()
        
    def objectNameChanger(self):
        self.objectName = self.objectLine.text()
        self.cam.objectName = self.objectName
#        print(text)
        
    def pathChanger(self):
        self.path = self.directoryLine.text()
        self.cam.path = self.path
        self.pathCleaner(False)
        
    def pathCleaner(self, delete):
        import os, glob
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if delete:
            temp = glob.glob(self.path+'/*.jpg')
            temp2 = glob.glob(self.path+'/*.csv')
            temp += temp2
            for item in temp:
                os.remove(item)

main = Main()
main.show()
#pathCleaner()
splash.close()
main.update()
sys.exit(app.exec_())
