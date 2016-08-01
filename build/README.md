# Build necessary files Linux

Embedding images required by Qt:

```
pyrcc4 -o -py3 GUI_data.py GUI_data.qrc
```

To generate py from ui:
```
pyuic4 mainwindow.ui > mainwindow.py
```
One file compilation of SpecPy.

Includes Splash Screen.

# Compile. Both Platforms.
```
pyinstaller SpecPySplash_Windows.spec # On Windows
pyinstaller SpecPySplash_Linux.spec # On Linux
```
Take into account the location of the files.
