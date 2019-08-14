import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\LAING3\\AppData\\Local\\Continuum\\anaconda3\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\LAING3\\AppData\\Local\\Continuum\\anaconda3\\tcl\\tk8.6"

from cx_Freeze import setup, Executable

base = None

executables = [Executable("ACTT Converter.py", base=base)]

packages = ["idna", "sys", "os", "subprocess", "tkinter"]
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name="ACTT Converter",
    options=options,
    version="0.1",
    description='Cleans ACTT files with |^| delimiters into proper .dsv files with a single | delimiter.',
    executables=executables
)
