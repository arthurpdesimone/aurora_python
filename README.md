# **Aurora**
## An software for aiding civil engineers to design reinforced concrete buildings.
![version](https://img.shields.io/badge/version-0.2.1-blue.svg)

### **Discord**
Join us at our Discord server 
https://discord.gg/72KvctMP

### **Standards**
NBR 6118:2014 - Design of concrete structures — Procedure

### **Documentation**
http://aurora-python.rtfd.io/

### **Projects**
PyNite - A linear elastic 3D structural engineering finite element analysis library for Python.
https://github.com/JWock82/PyNite


### **Dependencies**
Aurora dependencies
* **PyQt5**: PyQt5 is a comprehensive set of Python bindings for Qt v5.
* **qt_material**: This is another stylesheet for PySide6, PySide2 and PyQt5, which looks like Material Design (close enough).  
* **Panda3D**: Panda3D is a powerful 3D engine written in C++, with a complete set of Python bindings. 
* **tinybd**:TinyDB is a lightweight document oriented database optimized for your happiness.

Pynite dependencies
* **numpy**: used for matrix algebra and dense matrix solver
* **scipy**: used for sparse matrix solver to improve solution speed
* **matplotlib**: used for plotting member diagrams
* **PrettyTable** : used to format tabular output

### **To generate resources file**
pyrcc5 resources.qrc -o resources.py


### **To compile**

pyinstaller main.py --additional-hooks-dir=./pyinstaller_hooks --onefile


### **License**
MIT License
