# SpecPy
## Real time Spectrum Analyzer.
![SpecPy](https://github.com/jsbarbosa/SpecPy/blob/master/SpecPy.png)

Using a simple USB webcamara SpecPy is capable of recording frames as intensity data. With a Graphical User Interface based on Qt, camara settings are simple to control. Recorded frames are stored inside a dedicated folder, along with the generated data, thus allowing further analysis.
![Linux](https://github.com/jsbarbosa/SpecPy/blob/master/additional/MainLinux.png)
SpecPy is now capable of analysing images.

SpecPy allows the use of keyboard shortcuts:
- Press C to clear the plots
- Press Enter to capture current frame
- Press R to reset settings
- Press Space bar to start/stop streaming
- Press Ctrl + S to select an output directory

SpecPy uses the following modules:
- OpenCV 3
- matplotlib
- os
- glob
- NumPy
- csv

SpecPy is free to use and distribute. Executables files are hosted by [SourceForge](http://sourceforge.net), [Linux](https://sourceforge.net/projects/specpy/files/Linux/) and [Windows](https://sourceforge.net/projects/specpy/files/Windows/) are currently soported.
