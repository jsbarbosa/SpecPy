# Build Linux

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
