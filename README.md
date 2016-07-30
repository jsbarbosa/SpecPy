# SpecPy
## Real time Spectrum Analyzer.
![SpecPy](https://github.com/jsbarbosa/SpecPy/blob/master/SpecPy.png)

Using a simple USB webcamara SpecPy is capable of recording frames as intensity data. With a Graphical User Interface based on Qt, camara settings are simple to control. Recorded frames are storage inside a dedicated folder, along with the generated data, thus allowing further analysis.

SpecPy allows the use of keyboard shortcuts:
- Press C to clear the plots
- Press Enter to capture current frame
- Press R to reset settings

SpecPy uses the following modules:
- OpenCV 3
- matplotlib
- os
- glob
- NumPy
- csv
