# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:12:41 2016

@author: JuanBarbosa
"""

import cv2
import os
import glob
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv
 
# Folder in which to save the output data
#DELIMITER = ","
PATH = "Captures"
CAMARA = 0
STREAMWIDTH = 680
STREAMHEIGHT = 480

class CapturedFrame:
    def __init__(self, frame, identifier, center, interval, path):
        self.image = frame
        self.center = center
        self.interval = interval
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
        temp = self.path + "/%02d"%self.identifier + ".jpg"
        cv2.imwrite(temp, self.image)
        
    def saveData(self):
        directories = [self.path + "/Regular.csv", self.path + "/Normal.csv"]
        data_arrays = (self.intensity, self.normalIntensity) 
        if self.identifier == 0:
            for (inten, direc) in zip(data_arrays, directories):
                file = open(direc, "w")
                wr = csv.writer(file)
                wr.writerow(["x data", self.identifier])
                for (x, value) in enumerate(inten):
                    wr.writerow([x+1, value])
                file.close()
        else:
            for(inten, direc) in zip(data_arrays, directories):
                new_data = []
                file = open(direc, 'r')
                data = csv.reader(file, delimiter=',')
                i = 0
                for (line, value) in zip(data, inten):
                    if i == 0:
                        line.append(str(self.identifier))
                        temp = line
                    else:
                        line.append(str(value))
                        temp = line
                    new_data.append(temp)
                    i += 1
                file.close()
                file = open(direc, 'w')
                wr = csv.writer(file)
                for row in new_data:
                    wr.writerow(row)
                file.close()
                
class RealTimePlot:    
    fig, (ax1, ax2) = plt.subplots(2, figsize = (8, 4.5))
    ax1.set_ylabel("Normal intensity (a.u.)")
    ax2.set_ylabel("Intensity (a.u.)")
    ax2.set_xlabel("Pixel")
#    plt.tight_layout()
    linesNormal = []
    linesRegular = []
    def __init__(self, height, width, size = (8, 4.5)):
        self.fig.set_size_inches(size)
        self.height = height
        self.width = width
        self.ax1.set_xlim(0, self.width)
        self.ax1.set_ylim(0, 1)
        self.ax2.set_xlim(0, self.width)   
        self.ax2.set_ylim(0, self.height*200)
        self.ax1.hold(True)
        self.ax2.hold(True)
        self.ax1.grid()
        self.ax2.grid()
#        self.fig.canvas.manager.window.attributes('-topmost', 1)
        self.fig.show(False)
        plt.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.ax1.get_figure().bbox)
        self.x = np.linspace(0, self.width, self.width)    
        
    def includeCapturedFrame(self, captured_frame):
        intensity = captured_frame.intensity
        normalintensity= captured_frame.normalIntensity        
        style = "-"
        line = self.ax1.plot(self.x, normalintensity, style)[0]
        self.linesNormal.append(line)
        line = self.ax2.plot(self.x, intensity, style)[0]
        self.linesRegular.append(line)
        
    def plotRefresh(self):
        self.fig.canvas.restore_region(self.background)
        self.ax1.draw_artist(self.ax1.get_children()[0])
        for (line, lineR) in zip(self.linesNormal, self.linesRegular):
            self.ax1.draw_artist(line)
            self.ax2.draw_artist(lineR)
        self.fig.canvas.blit(self.ax1.clipbox)
        
    def cleanLines(self):
        for (lineN, lineR) in zip(self.linesNormal, self.linesRegular):
            lineN.set_data([],[])
            lineR.set_data([],[])
        self.ax1.set_prop_cycle(None)
        self.ax2.set_prop_cycle(None)
        
    def cleanPlot(self):
        self.cleanLines()
        self.linesNormal = []
        self.linesRegular = []
        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.ax1.get_figure().bbox)

    def close(self):
        plt.close()  
        
class GuiWindow:
    def __init__(self, name, camara, streamWidth, streamHeight, path):
        self.name = name
        self.trackBarName = "Settings"
        self.camara = camara
        self.path = path
        self.input = cv2.VideoCapture(camara)
        
        self.brightness = 50
        self.constrast = 50
        self.saturation = 50
        self.hue = 50
        self.gain = 50
        self.exposure = 50
        
        self.frame = self.input.read()[1]
        self.height, self.width, _ = self.frame.shape
        self.streamHeight = streamHeight
        self.streamWidth = streamWidth
        self.pixelLine = int(np.ceil(self.height/2))
        self.range = int(np.ceil(self.height/4))
        self.kbkey = 0
        self.createTrackBars()
        self.actualPlot = RealTimePlot(self.height, self.width)
        
        self.brightnessTrackBar(self.brightness)
        self.constrastTrackBar(self.constrast)
        self.saturationTrackBar(self.saturation)
        self.hueTrackBar(self.hue)
        self.gainTrackBar(self.gain)
        self.exposureTrackBar(self.exposure)
    
    def createTrackBars(self):
        cv2.namedWindow(self.trackBarName)
        cv2.createTrackbar("Position", self.trackBarName, self.pixelLine, self.height, self.posTrackBar)
        cv2.createTrackbar("Size", self.trackBarName, self.range, self.height, self.rangeTrackBar)
        cv2.createTrackbar("Brightness", self.trackBarName, self.brightness, 100, self.brightnessTrackBar)
        cv2.createTrackbar("Contrast", self.trackBarName, self.constrast, 100, self.constrastTrackBar)
        cv2.createTrackbar("Saturation", self.trackBarName, self.saturation, 100, self.saturationTrackBar)
        cv2.createTrackbar("Hue", self.trackBarName, self.hue, 100, self.hueTrackBar)
        cv2.createTrackbar("Gain", self.trackBarName, self.gain, 100, self.gainTrackBar)
        cv2.createTrackbar("Exposure", self.trackBarName, self.exposure*100, 100, self.exposureTrackBar)       
        
        cv2.resizeWindow(self.trackBarName, 100, 50)
        
    def squareInFrame(self):
        cv2.rectangle(self.frame, (0, self.pixelLine-self.range), (self.width-2, self.pixelLine+self.range), (0, 255, 255), 2)
        cv2.rectangle(self.frame, (0, self.pixelLine), (self.width-1, self.pixelLine), (0, 255, 0), 2)

    def textInFrame(self):
        cv2.putText(self.frame, "Esc to exit", (5, 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255)) 
        cv2.putText(self.frame, "c to clear plot", (5, 45), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255)) 
        cv2.putText(self.frame, "Enter to capture frame", (5, 65), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255)) 
        
    def posTrackBar(self, pos):
        self.pixelLine = pos
        
    def rangeTrackBar(self, size):
        self.range = size
        
    def brightnessTrackBar(self, brightness):
        self.brightness = brightness
        self.input.set(10, self.brightness/100)
        
    def constrastTrackBar(self, constrast):
        self.constrast = constrast
        self.input.set(11, self.constrast/100)
        
    def saturationTrackBar(self, saturation):
        self.saturation = saturation
        self.input.set(12, self.saturation/100)
        
    def hueTrackBar(self, hue):
        self.hue = hue
        self.input.set(13, self.hue/100)
        
    def gainTrackBar(self, gain):
        self.gain = gain
        self.input.set(14, self.gain/100)
        
    def exposureTrackBar(self, exposure):
        self.exposure = exposure
        self.input.set(15, self.exposure/100)
    
    def resize(self):
        self.frame = cv2.resize(self.frame, (self.streamWidth, self.streamHeight))
        
    def show(self):
        cv2.imshow(self.name, self.frame)
    
    def loop(self):
        fig_num = 0
        closed = False
        while True:
            self.frame = self.input.read()[1]
            temp_frame = self.frame.copy()
            self.squareInFrame()
            self.textInFrame()
            self.kbkey = cv2.waitKey(1) & 0xff
            if self.kbkey == 27:
                break
            
            elif self.kbkey == 10:
                temp = CapturedFrame(temp_frame, fig_num, self.pixelLine, self.range, self.path)
                self.actualPlot.includeCapturedFrame(temp)
                self.actualPlot.plotRefresh()
                temp.image = self.frame
                temp.saveFrame()
                fig_num += 1
                
            elif self.kbkey == ord('c'):
                self.actualPlot.cleanPlot()
            elif self.kbkey == 32:      # Space bar
                if closed:
                    self.createTrackBars()
                else:
                    cv2.destroyWindow(self.trackBarName)
                closed = not closed
            self.resize()
            self.show()
        self.actualPlot.close()
        cv2.destroyAllWindows()
        self.input.release()
        
if __name__ == "__main__":
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    else:
        temp = glob.glob(PATH+'/*.jpg')
        for item in temp:
            os.remove(item)
            
    camara = 0
    cam = GuiWindow("Stream", CAMARA, STREAMWIDTH, STREAMHEIGHT, PATH)
    cam.loop()
            
