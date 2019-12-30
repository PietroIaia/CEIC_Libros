########################################################################
# Tutorial: https://www.youtube.com/watch?v=r0oKJX_fMMw
# Gracias a dios por los Hindues
########################################################################

import sys
from cx_Freeze import setup, Executable

# Si es Windows (Pietro Approves)
if sys.platform == 'win32':
    base = 'Win32GUI'

build_exe_options = {
    "includes": ["passlib.handlers.bcrypt"] # <-- Include easy_gui
}

setup( name = "CEIC Libros", version = "1.0", 
       description = "done?", 
       options = {"build_exe": build_exe_options},
       executables = [Executable("CEIC_Libros.pyw", base = base)])