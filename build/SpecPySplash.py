# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 19:36:14 2016

@author: juan
"""

#from PyQt4.uic import loadUiType

from PyQt4 import QtCore, QtGui
import GUI_data

app = QtGui.QApplication([])
# Create and display the splash screen
splash_pix = QtGui.QPixmap(':/SpecPy.png')
splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
splash.show()

app.processEvents()

from mainwindow import Ui_MainWindow
import sys
import SpecPy as specpy
import platform
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas)

#Ui_MainWindow, QMainWindow = loadUiType('mainwindow.ui')
CAMARA = "0"
CAPTUREWIDTH = 680
CAPTUREHEIGHT = 480
STREAMWIDTH = 100
STREAMHEIGHT = int(3*STREAMWIDTH/4)
PLATFORM = platform.system()
PATH = "../Captures"
POS = int(CAPTUREHEIGHT/2)
SIZE = int(POS/2)
BRIGHTNESS = 50
CONTRAST = 50
SATURATION = 50
HUE = 50
GAIN = 50
EXPOSURE = 50

class Main(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        
        icon = QtGui.QIcon(':/Icon.png')
        self.setWindowIcon(icon)
        
        self.coeffWH = CAPTUREHEIGHT/CAPTUREWIDTH
        
        self.objectName = self.objectLine.text()
        
        self.path = PATH
        self.directoryLine.setText(self.path)

        self.camara = CAMARA
        self.camaraLine.setText(self.camara)        
        
        self.status = False
        self.cam = None
        
        self.posSlider.valueChanged.connect(self.posChange)    
        
        self.sizeSlider.valueChanged.connect(self.sizeChange)    
        
        self.brightnessSlider.valueChanged.connect(self.brightnessChange)        
        self.contrastSlider.valueChanged.connect(self.contrastChange)
        self.saturationSlider.valueChanged.connect(self.saturationChange)
        self.hueSlider.valueChanged.connect(self.hueChange)        
        self.gainSlider.valueChanged.connect(self.gainChange)
        self.exposureSlider.valueChanged.connect(self.exposureChange)
        
        self.enable_camara_change.changed.connect(self.enableCamaraChangerAction)
        self.actionSave_in.triggered.connect(self.saveFiles)
        self.actionSave_in.setShortcut('Ctrl+S')
        self.aboutAction.triggered.connect(self.about)
        self.filesListWidget.currentRowChanged.connect(self.updateFileImage)
        
        self.startstopButton.clicked.connect(self.startStop)
        self.captureButton.clicked.connect(self.captureData)
        self.cleanButton.clicked.connect(self.cleanPlot)
        self.resetButton.clicked.connect(self.resetSettings)
        self.getFilesButton.clicked.connect(self.getfiles)
        self.analyzeButton.clicked.connect(self.analyzeImages)
        self.saveButton.clicked.connect(self.saveFiles)
        self.clearFilesButton.clicked.connect(self.clearFiles)
        self.comboBox_2.addItem("680 x 480")
        self.comboBox_2.addItem("1280 x 720")
#        self.comboBox_2.addItem("1920 x 1080")
         
        self.comboBox_2.activated[str].connect(self.resolutionBox)
        
        self.canvas = None
        self.filenames = []
        self.imagesFig = None
        self.namesOnly = []
        self.plot = None
        
    def enableCamaraChangerAction(self):
        value = self.enable_camara_change.isChecked()
        self.camaraLine.setEnabled(value)

    def startStop(self):
        self.camaraLine.setEnabled(False)
        if self.status:
            if self.cam != None:
                self.cam.closeInput()
                self.timer.stop()
                self.cam = None
            self.status = not self.status
            self.statusLabel.setText("Stopped")
            self.statusLabel.setStyleSheet('color: red')         
        else:
            self.status = not self.status
            self.videoStream()
            self.update()
            if self.cam != None:
                self.statusLabel.setText("Streaming")
                self.statusLabel.setStyleSheet('color: green')
            else:
                self.status = True
        
        if self.enable_camara_change.isChecked():
            self.enable_camara_change.setChecked(False)
        
    def videoStream(self):
        self.camara = self.camaraLine.text()
        if self.camara.isdigit():
            self.camara = int(self.camara)
        try:
            self.cam = specpy.GuiWindow("Stream", self.camara, self.objectName, STREAMWIDTH, STREAMHEIGHT, PATH, 
                                   POS, SIZE, BRIGHTNESS, CONTRAST, SATURATION, HUE,
                                   GAIN, EXPOSURE, "canvas")
            self.resolutionBox(self.comboBox_2.currentText())
            self.posChange()
            self.sizeChange()
            self.brightnessChange()
            self.contrastChange()
            self.saturationChange()
            self.hueChange()
            self.gainChange()
            self.exposureChange()
        except:
            w = QtGui.QWidget()
            QtGui.QMessageBox.critical(w, "Error", "An error has occurred. Try another camara")
            self.cam = None
        if self.cam != None:
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
            self.cleanPlot()
        elif keyPressed == QtCore.Qt.Key_R:
            self.resetSettings()
        elif keyPressed == QtCore.Qt.Key_Space:
            self.startStop()
        
    def updateImage(self):
        if self.cam == None:
            return
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
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateImage)
        self.timer.start(33)

        # Creates first plot
        self.updatePlot()
        
    def updatePlot(self):
        """
            Updates plot
        """
        def create():
            if self.cam == None:
                figure = self.imagesFig
            else:
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
        if self.cam == None and self.imagesFig == None:
            return
        if self.canvas == None:
            create()
        else:
            removePlot()
            create()
            
    def posSliderLimits(self):
        self.posSlider.setMinimum(0)
        temp = self.cam.analysisHeight
        self.posSlider.setMaximum(temp)
        self.posSlider.setValue(int(temp/2))
        
    def sizeSliderLimits(self):
        self.sizeSlider.setMinimum(0)
        temp = self.cam.analysisHeight
        self.sizeSlider.setMaximum(int(temp/2))
        self.sizeSlider.setValue(int(temp/4))
    
    def posChange(self):
        size = self.posSlider.value()
        if not self.status:
            self.camaraWarning()
            return
        self.cam.posTrackBar(size)
        
    def sizeChange(self):
        size = self.sizeSlider.value()
        if not self.status:
            self.camaraWarning()
            return
        self.cam.rangeTrackBar(size)
        
    def brightnessChange(self):
        size = self.brightnessSlider.value()
        if not self.status:
            self.camaraWarning()
            return
        self.cam.brightnessTrackBar(size)
        
    def contrastChange(self):
        size = self.contrastSlider.value()
        if not self.status:
            self.camaraWarning()
            return
        self.cam.contrastTrackBar(size)

    def saturationChange(self):
        size = self.saturationSlider.value()
        if not self.status:
            self.camaraWarning()
            return
        self.cam.saturationTrackBar(size)
        
    def hueChange(self):
        size = self.hueSlider.value()
        if not self.status:
            self.camaraWarning()
            return
        self.cam.hueTrackBar(size)
        
    def gainChange(self):
        size = self.gainSlider.value()
        if not self.status:
            self.camaraWarning()
            return
        self.cam.gainTrackBar(size)

    def exposureChange(self):
        size = self.exposureSlider.value()
        if not self.status:
            self.camaraWarning()
            return
        self.cam.exposureTrackBar(size)      
    
    def captureData(self):
        if not self.status:
            self.camaraWarning()
            return
        self.objectNameChanger()
        self.pathChanger()
        self.fig_num = self.cam.captureData(self.cam.notSquaredAnalysisFrame, self.fig_num)
        self.updatePlot()
        
    def resetSettings(self):
        if self.cam == None:
            self.camaraWarning()
            return
        self.cam.resetSettings(POS, SIZE, BRIGHTNESS, CONTRAST, SATURATION, HUE, GAIN, EXPOSURE)
        self.posSlider.setValue(POS)
        self.sizeSlider.setValue(SIZE)        
        self.brightnessSlider.setValue(BRIGHTNESS)
        self.contrastSlider.setValue(CONTRAST)
        self.saturationSlider.setValue(SATURATION)
        self.hueSlider.setValue(HUE)
        self.gainSlider.setValue(GAIN)
        self.exposureSlider.setValue(EXPOSURE)
#        self.path = PATH
#        self.directoryLine.setText(self.path)
        self.objectName = ""
        self.objectLine.setText(self.objectName)
        self.comboBox_2.setCurrentIndex(0)
        self.resolutionBox(self.comboBox_2.currentText())
        
    def closeEvent(self, event):
        if self.cam != None:
            self.cam.closeInput()
            self.timer.stop()
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
#        
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
                
    def cleanPlot(self):
        if self.plot != None:
            self.plot.cleanLines()
            self.updatePlot()
            
        if self.status:
            self.cam.cleanData()
            self.updatePlot()
            
        if self.plot == None and self.cam == None:
            self.camaraWarning()
        
    def about(self):            
        about = QtGui.QMessageBox()
        about.setIcon(QtGui.QMessageBox.Question)
        about.setWindowTitle("About")
        about.setText(
                    "Using a simple USB webcamara SpecPy is capable of recording frames "
                    + "as intensity data. With a Graphical User Interface based on Qt, "
                    + "camara settings are simple to control. Recorded frames are stored "
                    + "inside a dedicated folder, along with the generated data, thus "
                    + "allowing further analysis. <br><br>"
                    + "More in formation can be found at the <a href=https://github.com/jsbarbosa/SpecPy>repository</a>."
                    )
        about.exec()
        
    def camaraWarning(self):
        warning = QtGui.QMessageBox()
        warning.setIcon(QtGui.QMessageBox.Warning)
        warning.setWindowTitle("Warning")
        warning.setText("Please start streaming.")
        warning.exec()
        
    def getfiles(self):
        dlg = QtGui.QFileDialog()
        dlg.setFileMode(QtGui.QFileDialog.AnyFile)
        fileFilter = "Images (*.jpg *.jpeg *.png)"
        filenames = dlg.getOpenFileNames(self, filter = fileFilter)
        for file in filenames:
            self.filenames.append(file)
        self.filesListWidget.clear()
        self.updateFileList()
        
    def saveFiles(self):
        dlg = QtGui.QFileDialog()
        file = dlg.getExistingDirectory(self)
        while file == "":
            w = QtGui.QWidget()
            QtGui.QMessageBox.critical(w, "Error", "No path has been specified.")
            file = dlg.getExistingDirectory(self)
        self.path = file
        self.directoryLine.setText(self.path)
    
    def clearFiles(self):
        self.filenames = []
        self.filesListWidget.clear()
        
    def updateFileList(self):
        self.namesOnly = []
        if PLATFORM == "Linux":
            breaker = '/'
        else:
            breaker = '\\'
        for file in self.filenames:
            temp = file.rpartition(breaker)
            self.namesOnly.append(temp[-1])
            path = temp[:-1][0]
        self.inputLineEdit.setText(path)
        self.filesListWidget.addItems(self.namesOnly)
        
    def updateFileImage(self, pos):
        pix = QtGui.QPixmap(self.filenames[pos])

        coeff = pix.height()/pix.width()
        
        width = self.fileViewer.frameGeometry().width()
        height = int(coeff*width)
        realHeight = self.fileViewer.frameGeometry().height()
        if height > realHeight:
            width = int(realHeight/coeff)
            height = realHeight
        pix = pix.scaled(width, height, QtCore.Qt.KeepAspectRatio)
        self.fileViewer.setPixmap(pix)
        
    def analyzeImages(self):
        if self.cam != None:
            w = QtGui.QWidget()
            QtGui.QMessageBox.critical(w, "Error", "SpecPy is streaming.")
            return
            
        if self.filenames == []:
            w = QtGui.QWidget()
            QtGui.QMessageBox.critical(w, "Error", "No files loaded.")
            return
        
        class WorkThread(QtCore.QThread, Main):
            def __init__(self, plot, imagesFig, filenames, namesOnly, path):
                QtCore.QThread.__init__(self)
                
                self.plot = plot
                self.imagesFig = imagesFig
                self.filenames = filenames
                self.namesOnly = namesOnly
                self.path = path
            def __del__(self):
                self.wait()
                
            def run(self):             
                self.plot = specpy.RealTimePlot(1,1)
                i = 0       
                for (file, name) in zip(self.filenames, self.namesOnly):
                    capturedframe = specpy.CapturedFrame(file, name, "", None, None, self.path)
                    self.plot.width = capturedframe.width
                    self.plot.changeAxes()
                    self.plot.includeCapturedFrame(capturedframe)
                    self.imagesFig = self.plot.figureReturn()
                    if i <= 3:
                        self.plot.ax2.set_ylim(0, capturedframe.height*255)
                    i += 1                
                    self.emit(QtCore.SIGNAL('update(QString)'), str(i))
                self.terminate
                    
        self.pathCleaner(False) 
        number = len(self.filenames)
        progressBar_unit = int(100/number)
        def threadUpdate(pos):
            pos = int(pos)
            self.progressBar.setValue(pos*progressBar_unit)
            self.currentFileLabel.setText(self.namesOnly[pos-1])
            if pos == number:
                self.progressBar.setValue(100)
                self.plot = self.workThread.plot
                self.imagesFig = self.workThread.imagesFig
                self.updatePlot()
        
        self.workThread = WorkThread(self.plot, self.imagesFig, self.filenames, self.namesOnly, self.path)
        self.connect(self.workThread, QtCore.SIGNAL("update(QString)"), threadUpdate)
        self.workThread.start()

        
main = Main()
main.show()
splash.close()
sys.exit(app.exec_())
