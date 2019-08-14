import sys
import os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = "C:\\Users\\LAING3\\AppData\\Local\\Continuum\\anaconda3\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\LAING3\\AppData\\Local\\Continuum\\anaconda3\\tcl\\tk8.6"

additional_mods = ['numpy.core._methods', 'numpy.lib.format']
exclude_mods = ["tkinter", "PyQt4.QtSql", "sqlite3", 
                                  "scipy.lib.lapack.flapack",
                                  "PyQt4.QtNetwork",
                                  "PyQt4.QtScript",
                                  "numpy.core._dotblas", 
                                  "PyQt5"]

modules = ["sys", "os", "subprocess", "numpy", "time", "pandas", "urllib", "bs4", "tkinter"]

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    executables = [Executable('IPLookup.py', base=base)]

setup(name='IP Address WHOIS Lookup',
    version='0.1',
    description='This small program performs a WHOIS query on a list of IP Addresses.',
    options = {'build_exe' : {'packages': modules}},
    executables=executables
    )



