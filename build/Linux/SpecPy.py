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

PATH = "Captures"

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
    def __init__(self, name, camara, path):
        self.name = name
        self.camara = camara
        self.path = path
        self.input = cv2.VideoCapture(camara)
        self.frame = self.input.read()[1]
        self.height, self.width, _ = self.frame.shape
        self.pixelLine = 0
        self.range = 1
        self.kbkey = 0
        self.createTrackBars()
        self.actualPlot = RealTimePlot(self.height, self.width)
    
    def createTrackBars(self):
        cv2.namedWindow(self.name)
        cv2.createTrackbar("Position", self.name, 0, self.height, self.posTrackBar)
        cv2.createTrackbar("Size", self.name, 1, self.height, self.rangeTrackBar)
        
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
        
    def show(self):
        cv2.imshow(self.name, self.frame)
    
    def loop(self):
        fig_num = 0
        while True:
            self.frame = self.input.read()[1]
            temp_frame = self.frame.copy()
            self.squareInFrame()
            self.textInFrame()
            closed = True
            try:
                cv2.getWindowProperty(self.name, 0)
                closed = False
            except:
                pass
            if closed:
                self.createTrackBars()
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
    cam = GuiWindow("Stream", camara, PATH)
    cam.loop()
            
