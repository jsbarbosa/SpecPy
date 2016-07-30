# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:12:41 2016

@author: JuanBarbosa
"""

import cv2
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
#matplotlib.use('Agg')
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt

import platform
#import gc
import csv
 
# Folder in which to save the output data
#DELIMITER = ","
PATH = "Captures"
CAMARA = 0
STREAMWIDTH = 680
STREAMHEIGHT = 480
PLATFORM = platform.system()

"""
    Class that defines a frame that wants to be captured
"""
class CapturedFrame:
    def __init__(self, frame, objectName, identifier, center, interval, path):
        self.image = frame
        self.center = center
        self.interval = interval
        self.objectName = objectName
        self.identifier = identifier
        self.height = frame.shape[0]
        self.width = frame.shape[1]
        self.intensity = np.zeros(self.width)
        self.normalIntensity = np.zeros(self.width)
        self.path = path
        
        self.calculateIntensity()
        self.calculateNormalIntensity()
        self.saveData()
        
    def calculateIntensity(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        minValue = self.center - self.interval
        maxValue = self.center + self.interval
        if self.interval == 0:
            minValue = self.center - 1
            maxValue = self.center + 1
        if minValue < 0:
            minValue = 0
        if maxValue > self.height:
            maxValue = self.height            
        self.intensity = [sum(gray[minValue:maxValue, i]) for i in range(self.width)]
            
    def calculateNormalIntensity(self):
        max_value = max(self.intensity)
        self.normalIntensity = self.intensity/max_value
        
    def saveFrame(self):
        temp = self.path +"/"+ self.objectName + "_%02d"%self.identifier + ".jpg"
        cv2.imwrite(temp, self.image)
        
    def saveData(self):
        def csv2list(directory):
            temp = []
            file = open(directory, 'r')
            csvFile = csv.reader(file, delimiter=',')
            for item in csvFile:
                temp.append(item)
            file.close()
            return temp
            
        directories = [self.path + "/Regular.csv", self.path + "/Normal.csv"]
        data_arrays = (self.intensity, self.normalIntensity) 
        if not os.path.exists(directories[0]):
            for (inten, direc) in zip(data_arrays, directories):
                file = open(direc, "w")
                wr = csv.writer(file)
                wr.writerow(["x data", self.identifier])
                for (x, value) in enumerate(inten):
                    wr.writerow([x+1, value])
                file.close()
        else:
            for(inten, direc) in zip(data_arrays, directories):
                data = csv2list(direc)                
                num_rows = len(data) - 1        # Because of the information row
                columnNumber = len(data[0])
                num_inten_rows = len(inten)
                inten = list(inten)
                row_prototype = ["" for i in range(columnNumber)]
                
                if num_rows < num_inten_rows:
                    x = int(data[-1][0]) + 1              
                    while num_rows - 1 < num_inten_rows:
                        row = list(row_prototype)
                        row[0] = x
                        data.append(row)
                        num_rows += 1
                        x += 1
                        
                elif num_inten_rows < num_rows:
                    while num_inten_rows < num_rows:
                        inten.append("")
                        num_inten_rows += 1
                inten.insert(0,"")   
                i = 0
                for (line, value) in zip(data, inten):
                    if i == 0:
                        line.append(self.objectName + ' ' + str(self.identifier))
                    else:
                        line.append(str(value))
                    i += 1

                file = open(direc, 'w')
                wr = csv.writer(file)
                for row in data:
                    wr.writerow(row)
                file.close()
                    
        def changePath(self, path):
            self.path = path
            
"""
    Class which handles the real time information plotting
"""
class RealTimePlot:    
    def __init__(self, height, width):
        self.fig = Figure()
        print(self.fig)
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        self.ax1.set_ylabel("Normalized intensity") 
        self.ax2.set_ylabel("Intensity")
        self.ax2.set_xlabel("Pixel")
        self.fig.set_facecolor("None")
        self.height = height
        self.width = width
        self.ax1.set_xlim(0, self.width)
        self.ax1.set_ylim(0, 1)
        self.ax2.set_xlim(0, self.width)   
        self.ax2.set_ylim(0, self.height*255)

        self.ax1.grid()
        self.ax2.grid()
        
        self.normalLines = []
        self.regularLines = []

        self.x = np.linspace(0, self.width, self.width)    
        self.changeAxesFontSize(self.ax1)
        self.changeAxesFontSize(self.ax2)
        
    def includeCapturedFrame(self, captured_frame):
        intensity = captured_frame.intensity
        normalintensity = captured_frame.normalIntensity        
        style = "-"
        
        self.normalLines.append(self.ax1.plot(self.x, normalintensity, style)[0])#)
        self.regularLines.append(self.ax2.plot(self.x, intensity, style)[0])#)
        
    def cleanLines(self):
        for (lineN, lineR) in zip(self.normalLines, self.regularLines):
            lineN.set_data([],[])
            lineR.set_data([],[])
        self.ax1.set_prop_cycle(None)
        self.ax2.set_prop_cycle(None)
        
    def cleanPlot(self):
        self.cleanLines()
        self.linesNormal = []
        self.linesRegular = []
#        self.fig.canvas.draw()

    def figureReturn(self):
        return self.fig
        
    def changeAxesFontSize(self, axes):
        for item in ([axes.title, axes.xaxis.label, axes.yaxis.label] +
             axes.get_xticklabels() + axes.get_yticklabels()):
            item.set_fontsize(10)
            
    def changeAxes(self):
        self.ax1.set_xlim(0, self.width)
        self.ax2.set_xlim(0, self.width)
        self.x = np.linspace(0, self.width, self.width)
        
class GuiWindow:
    def __init__(self, name, camara, objectName, streamWidth, streamHeight,
                 path, pos = 0, size = 0, brightness = 50, contrast = 50, saturation = 50, 
                 hue = 50, gain = 50, exposure = 50, window = None):
        self.name = name
        self.trackBarName = "Settings"
        self.camara = camara
        self.path = path
        self.input = cv2.VideoCapture(camara)
        self.objectName = objectName
        self.resetSettings(pos, size, brightness, contrast, saturation, hue, 
                           gain, exposure)
        """
        Frame is presented one
        """
        self.analysisFrame = self.input.read()[1]
        self.analysisHeight, self.analysisWidth, _ = self.analysisFrame.shape
        self.streamHeight = streamHeight
        self.streamWidth = streamWidth
        self.pixelLine = int(np.ceil(self.analysisHeight/2))
        self.range = int(np.ceil(self.analysisHeight/4))
        self.kbkey = 0

        self.actualPlot = RealTimePlot(self.analysisHeight, self.analysisWidth)
        self.figure = self.actualPlot.figureReturn()
        
    def squareInFrame(self):
        cv2.rectangle(self.analysisFrame, (0, self.pixelLine-self.range), (self.analysisWidth, self.pixelLine-self.range), (0, 255, 255), 3)
        cv2.rectangle(self.analysisFrame, (0, self.pixelLine+self.range), (self.analysisWidth, self.pixelLine+self.range), (0, 255, 255), 3)
        cv2.rectangle(self.analysisFrame, (0, self.pixelLine), (self.analysisWidth, self.pixelLine), (0, 255, 0), 3)
        
    def resize(self):
        self.frame = cv2.resize(self.analysisFrame, (self.streamWidth, self.streamHeight))
   
    def captureData(self, temp_frame, fig_num):
        temp_frameY, temp_frameX, _ = temp_frame.shape
        if self.actualPlot.width != temp_frameX:
            self.actualPlot.width = temp_frameX
            self.actualPlot.changeAxes()
        temp = CapturedFrame(temp_frame, self.objectName, fig_num, self.pixelLine, self.range, self.path)
        try:        
            self.actualPlot.includeCapturedFrame(temp)
            self.actualPlot.plotRefresh()
        except:
            pass
        temp.image = self.analysisFrame
        temp.saveFrame()
        fig_num += 1
        return fig_num
    
    def cleanData(self):
        self.actualPlot.cleanPlot()
        
    def eachPhotogram(self):
        ans, self.analysisFrame = self.input.read()
        if not ans or any(value is np.nan for value in self.analysisFrame):
            return False
        self.notSquaredAnalysisFrame = self.analysisFrame.copy()
        self.squareInFrame()            
        self.figure = self.actualPlot.figureReturn()
        self.resize()
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        return True
        
    def closeInput(self):
#        self.actualPlot.close()
        cv2.destroyAllWindows()
        self.input.release()
        
    def changeWidth(self, width):
        self.streamWidth = width
       
    def changeHeight(self, height):
        self.streamHeight = height
        
    def posTrackBar(self, pos):
        self.pixelLine = pos
        
    def rangeTrackBar(self, size):
        self.range = size
        
    def brightnessTrackBar(self, brightness):
        self.brightness = brightness
        if PLATFORM == "Linux":
            self.brightness *= 1/100
        self.input.set(10, self.brightness)
        
    def contrastTrackBar(self, contrast):
        self.contrast = contrast
        if PLATFORM == "Linux":
            self.contrast *= 1/100
        self.input.set(10, self.contrast)
        
    def saturationTrackBar(self, saturation):
        self.saturation = saturation
        if PLATFORM == "Linux":
            self.saturation *= 1/100
        self.input.set(12, self.saturation)
            
    def hueTrackBar(self, hue):
        self.hue = hue
        if PLATFORM == "Linux":
            self.hue *= 1/100
        self.input.set(13, self.hue)
        
    def gainTrackBar(self, gain):
        self.gain = gain
        if PLATFORM == "Linux":
            self.gain *= 1/100
        self.input.set(14, self.gain)
        
    def exposureTrackBar(self, exposure):
        self.exposure = exposure
        if PLATFORM == "Linux":
            self.exposure *= 1/100
        self.input.set(15, self.exposure)
        
    def setCaptureWidth(self, width):
        self.analysisWidth = width
        self.input.set(3, self.analysisWidth)
        
    def setCaptureHeight(self, height):
        self.analysisHeight = height
        self.input.set(4, self.analysisHeight)
        
    def resetSettings(self, pos, size, brightness, contrast, saturation, 
                      hue, gain, exposure):
        self.posTrackBar(pos)
        self.rangeTrackBar(size)
        self.brightnessTrackBar(brightness)
        self.contrastTrackBar(contrast)
        self.saturationTrackBar(saturation)
        self.hueTrackBar(hue)
        self.gainTrackBar(gain)
        self.exposureTrackBar(exposure)

"""
GUI
"""                                
        
if __name__ == "__main__":
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    else:
        temp = glob.glob(PATH+'/*.jpg')
        for item in temp:
            os.remove(item)
