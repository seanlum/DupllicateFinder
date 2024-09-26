#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.abspath('../DupllicateFinder'))

from DupllicateFinder import DFApplication

def run():
    app = DFApplication(sys.argv)
    sys.exit(app.exec_())

