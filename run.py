"""Startup script for frozen executable."""
import os
import sys
from pathlib import Path

# Ensure we're in the right directory
if hasattr(sys, '_MEIPASS'):
    # PyInstaller path
    os.chdir(sys._MEIPASS)
else:
    # Normal execution
    os.chdir(Path(__file__).parent)

# Now import and run the app
from gui_app import main

if __name__ == "__main__":
    sys.exit(main())
