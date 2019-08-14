import sys
import os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = "C:\\Users\\LAING3\\AppData\\Local\\Continuum\\anaconda3\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\LAING3\\AppData\\Local\\Continuum\\anaconda3\\tcl\\tk8.6"

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    executables = [Executable('HelloWorld.py', base=base)]

setup(name='Hello World!',
    version='0.1',
    description='Hello World!',
    executables=executables
    )



